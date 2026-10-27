"""MIZAN CORE — durable execution journal.

SQLite reference implementation for idempotent claiming and explicit outcomes.
A claimed execution is never returned to PENDING automatically. UNKNOWN is terminal.
This module records local software state; it cannot guarantee exactly-once effects
in an external system unless that system also supports idempotency/reconciliation.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from mizan_governance import ExecutionStatus, GovernanceError

GENESIS = "0" * 64
_ALLOWED = {
    ExecutionStatus.PENDING: {ExecutionStatus.CLAIMED, ExecutionStatus.CANCELLED},
    ExecutionStatus.CLAIMED: {
        ExecutionStatus.RUNNING, ExecutionStatus.UNKNOWN, ExecutionStatus.CANCELLED
    },
    ExecutionStatus.RUNNING: {
        ExecutionStatus.SUCCEEDED, ExecutionStatus.FAILED, ExecutionStatus.UNKNOWN
    },
    ExecutionStatus.SUCCEEDED: set(),
    ExecutionStatus.FAILED: set(),
    ExecutionStatus.UNKNOWN: set(),
    ExecutionStatus.CANCELLED: set(),
}


class ExecutionStoreError(RuntimeError):
    """Raised when an execution identity or state invariant is violated."""


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False)


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ExecutionRecord:
    execution_id: str
    intent_id: str
    idempotency_key: str
    request_digest: str
    status: ExecutionStatus
    worker_id: str | None
    created_at: str
    updated_at: str
    created: bool = True


@dataclass(frozen=True)
class ClaimResult:
    claimed: bool
    record: ExecutionRecord


class SQLiteExecutionStore:
    """Durable SQLite store with atomic claim_once and a hash-chained event log."""

    def __init__(self, path: str | Path):
        self.path = str(path)
        if self.path == ":memory:":
            raise ValueError(
                "SQLiteExecutionStore requires a file path; per-operation connections "
                "cannot share a plain :memory: database"
            )
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        con = sqlite3.connect(self.path, timeout=20.0, isolation_level=None)
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA busy_timeout=20000")
        con.execute("PRAGMA foreign_keys=ON")
        return con

    def _initialize(self) -> None:
        with closing(self._connect()) as con:
            con.execute("PRAGMA journal_mode=WAL")
            con.executescript("""
                CREATE TABLE IF NOT EXISTS executions (
                    execution_id TEXT PRIMARY KEY,
                    intent_id TEXT NOT NULL,
                    idempotency_key TEXT NOT NULL UNIQUE,
                    request_digest TEXT NOT NULL,
                    status TEXT NOT NULL CHECK(status IN (
                        'PENDING','CLAIMED','RUNNING','SUCCEEDED','FAILED','UNKNOWN','CANCELLED'
                    )),
                    worker_id TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS execution_events (
                    event_seq INTEGER PRIMARY KEY AUTOINCREMENT,
                    execution_id TEXT NOT NULL REFERENCES executions(execution_id),
                    from_status TEXT,
                    to_status TEXT NOT NULL,
                    actor TEXT NOT NULL,
                    occurred_at TEXT NOT NULL,
                    detail TEXT NOT NULL,
                    prev_hash TEXT NOT NULL,
                    hash TEXT NOT NULL UNIQUE
                );
            """)

    @staticmethod
    def _record(row: sqlite3.Row, *, created: bool = True) -> ExecutionRecord:
        return ExecutionRecord(
            execution_id=row["execution_id"], intent_id=row["intent_id"],
            idempotency_key=row["idempotency_key"], request_digest=row["request_digest"],
            status=ExecutionStatus(row["status"]), worker_id=row["worker_id"],
            created_at=row["created_at"], updated_at=row["updated_at"], created=created,
        )

    @staticmethod
    def _validate_digest(digest: str) -> bool:
        return (isinstance(digest, str) and len(digest) == 64 and
                all(ch in "0123456789abcdef" for ch in digest.lower()))

    def _append_event(self, con: sqlite3.Connection, *, execution_id: str,
                      from_status: str | None, to_status: str, actor: str,
                      occurred_at: str, detail: str) -> None:
        last = con.execute(
            "SELECT event_seq, hash FROM execution_events ORDER BY event_seq DESC LIMIT 1"
        ).fetchone()
        seq = (last["event_seq"] + 1) if last else 1
        prev_hash = last["hash"] if last else GENESIS
        fields = {
            "schema": "mizan.execution-event.v1", "event_seq": seq,
            "execution_id": execution_id, "from_status": from_status,
            "to_status": to_status, "actor": actor, "occurred_at": occurred_at,
            "detail": detail, "prev_hash": prev_hash,
        }
        digest = _sha256(_canonical(fields))
        con.execute("""
            INSERT INTO execution_events
                (event_seq,execution_id,from_status,to_status,actor,occurred_at,
                 detail,prev_hash,hash)
            VALUES(?,?,?,?,?,?,?,?,?)
        """, (seq, execution_id, from_status, to_status, actor, occurred_at,
              detail, prev_hash, digest))

    def create_execution(self, *, execution_id: str, intent_id: str,
                         idempotency_key: str, request_digest: str,
                         now: str) -> ExecutionRecord:
        for name, value in (
            ("execution_id", execution_id), ("intent_id", intent_id),
            ("idempotency_key", idempotency_key), ("now", now),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} is required")
        if not self._validate_digest(request_digest):
            raise ValueError("request_digest must be a 64-character SHA-256 hex digest")

        con = self._connect()
        try:
            con.execute("BEGIN IMMEDIATE")
            existing = con.execute(
                "SELECT * FROM executions WHERE execution_id=?", (execution_id,)
            ).fetchone()
            if existing:
                identity = (existing["intent_id"], existing["idempotency_key"],
                            existing["request_digest"])
                supplied = (intent_id, idempotency_key, request_digest)
                if identity != supplied:
                    raise ExecutionStoreError(
                        "execution_id is immutable and already bound to different request data"
                    )
                con.execute("COMMIT")
                return self._record(existing, created=False)

            key_owner = con.execute(
                "SELECT execution_id FROM executions WHERE idempotency_key=?",
                (idempotency_key,),
            ).fetchone()
            if key_owner:
                raise ExecutionStoreError(
                    "idempotency_key already belongs to a different execution_id"
                )

            con.execute("""
                INSERT INTO executions
                    (execution_id,intent_id,idempotency_key,request_digest,status,
                     worker_id,created_at,updated_at)
                VALUES(?,?,?,?,?,?,?,?)
            """, (execution_id, intent_id, idempotency_key, request_digest,
                  ExecutionStatus.PENDING.value, None, now, now))
            self._append_event(
                con, execution_id=execution_id, from_status=None,
                to_status=ExecutionStatus.PENDING.value, actor="system",
                occurred_at=now, detail="execution created",
            )
            row = con.execute(
                "SELECT * FROM executions WHERE execution_id=?", (execution_id,)
            ).fetchone()
            con.execute("COMMIT")
            return self._record(row)
        except Exception:
            if con.in_transaction:
                con.execute("ROLLBACK")
            raise
        finally:
            con.close()

    def get(self, execution_id: str) -> ExecutionRecord | None:
        with closing(self._connect()) as con:
            row = con.execute(
                "SELECT * FROM executions WHERE execution_id=?", (execution_id,)
            ).fetchone()
            return self._record(row) if row else None

    def claim_once(self, *, execution_id: str, worker_id: str, now: str) -> ClaimResult:
        if not isinstance(worker_id, str) or not worker_id.strip():
            raise ValueError("worker_id is required")
        if not isinstance(now, str) or not now.strip():
            raise ValueError("now is required")
        con = self._connect()
        try:
            con.execute("BEGIN IMMEDIATE")
            row = con.execute(
                "SELECT * FROM executions WHERE execution_id=?", (execution_id,)
            ).fetchone()
            if row is None:
                raise ExecutionStoreError("execution_id not found")
            if row["status"] != ExecutionStatus.PENDING.value:
                con.execute("COMMIT")
                return ClaimResult(False, self._record(row))
            con.execute("""
                UPDATE executions SET status=?,worker_id=?,updated_at=?
                WHERE execution_id=? AND status=?
            """, (ExecutionStatus.CLAIMED.value, worker_id, now, execution_id,
                  ExecutionStatus.PENDING.value))
            updated = con.execute(
                "SELECT * FROM executions WHERE execution_id=?", (execution_id,)
            ).fetchone()
            if updated["status"] != ExecutionStatus.CLAIMED.value or updated["worker_id"] != worker_id:
                raise ExecutionStoreError("atomic claim invariant violated")
            self._append_event(
                con, execution_id=execution_id, from_status=ExecutionStatus.PENDING.value,
                to_status=ExecutionStatus.CLAIMED.value, actor=worker_id,
                occurred_at=now, detail="claim_once",
            )
            con.execute("COMMIT")
            return ClaimResult(True, self._record(updated))
        except Exception:
            if con.in_transaction:
                con.execute("ROLLBACK")
            raise
        finally:
            con.close()

    def transition(self, *, execution_id: str, expected: ExecutionStatus,
                   target: ExecutionStatus, actor: str, now: str,
                   detail: str = "") -> ExecutionRecord:
        if not isinstance(actor, str) or not actor.strip():
            raise ValueError("actor is required")
        if not isinstance(now, str) or not now.strip():
            raise ValueError("now is required")
        if target is ExecutionStatus.CLAIMED:
            raise GovernanceError(
                "CLAIMED can only be acquired through claim_once"
            )
        if target not in _ALLOWED[expected]:
            raise GovernanceError(
                f"illegal execution transition: {expected.value} -> {target.value}"
            )
        con = self._connect()
        try:
            con.execute("BEGIN IMMEDIATE")
            row = con.execute(
                "SELECT * FROM executions WHERE execution_id=?", (execution_id,)
            ).fetchone()
            if row is None:
                raise ExecutionStoreError("execution_id not found")
            if row["status"] != expected.value:
                raise ExecutionStoreError(
                    f"compare-and-set failed: expected {expected.value}, found {row['status']}"
                )
            if expected in {ExecutionStatus.CLAIMED, ExecutionStatus.RUNNING}:
                if row["worker_id"] != actor:
                    raise ExecutionStoreError(
                        "worker ownership mismatch: only the claimed worker may transition this execution"
                    )
            con.execute("""
                UPDATE executions SET status=?,updated_at=?
                WHERE execution_id=? AND status=?
            """, (target.value, now, execution_id, expected.value))
            self._append_event(
                con, execution_id=execution_id, from_status=expected.value,
                to_status=target.value, actor=actor, occurred_at=now,
                detail=detail,
            )
            updated = con.execute(
                "SELECT * FROM executions WHERE execution_id=?", (execution_id,)
            ).fetchone()
            con.execute("COMMIT")
            return self._record(updated)
        except Exception:
            if con.in_transaction:
                con.execute("ROLLBACK")
            raise
        finally:
            con.close()

    def verify_event_chain(self) -> dict[str, Any]:
        """Verify hash links, legal per-execution transitions, and current snapshots."""
        with closing(self._connect()) as con:
            rows = con.execute(
                "SELECT * FROM execution_events ORDER BY event_seq"
            ).fetchall()
            executions = con.execute(
                "SELECT execution_id, status FROM executions"
            ).fetchall()

        expected_prev = GENESIS
        last_status: dict[str, str] = {}
        verified = 0
        for expected_seq, row in enumerate(rows, start=1):
            if row["event_seq"] != expected_seq:
                return {"ok": False, "reason": "SEQUENCE_GAP", "verified_events": verified}
            if row["prev_hash"] != expected_prev:
                return {"ok": False, "reason": "PREVIOUS_HASH_MISMATCH",
                        "verified_events": verified}
            fields = {
                "schema": "mizan.execution-event.v1", "event_seq": row["event_seq"],
                "execution_id": row["execution_id"], "from_status": row["from_status"],
                "to_status": row["to_status"], "actor": row["actor"],
                "occurred_at": row["occurred_at"], "detail": row["detail"],
                "prev_hash": row["prev_hash"],
            }
            actual = _sha256(_canonical(fields))
            if row["hash"] != actual:
                return {"ok": False, "reason": "EVENT_HASH_MISMATCH",
                        "verified_events": verified}

            execution_id = row["execution_id"]
            target = row["to_status"]
            source = row["from_status"]
            if execution_id not in last_status:
                if source is not None or target != ExecutionStatus.PENDING.value:
                    return {"ok": False, "reason": "INVALID_INITIAL_STATE",
                            "verified_events": verified}
            else:
                current = last_status[execution_id]
                if source != current:
                    return {"ok": False, "reason": "EVENT_STATE_DISCONTINUITY",
                            "verified_events": verified}
                try:
                    legal = ExecutionStatus(target) in _ALLOWED[ExecutionStatus(current)]
                except (ValueError, KeyError):
                    legal = False
                if not legal:
                    return {"ok": False, "reason": "ILLEGAL_STATE_TRANSITION",
                            "verified_events": verified}
            last_status[execution_id] = target
            expected_prev = actual
            verified += 1

        snapshot = {row["execution_id"]: row["status"] for row in executions}
        if set(snapshot) != set(last_status):
            return {"ok": False, "reason": "EXECUTION_EVENT_COVERAGE_MISMATCH",
                    "verified_events": verified}
        for execution_id, status in snapshot.items():
            if last_status.get(execution_id) != status:
                return {"ok": False, "reason": "CURRENT_STATE_MISMATCH",
                        "verified_events": verified, "execution_id": execution_id}
        return {"ok": True, "reason": "EVENT_CHAIN_AND_STATE_CONSISTENT",
                "verified_events": verified, "executions": len(snapshot),
                "tip_hash": expected_prev}
