"""Durable reconciliation journal for terminal UNKNOWN executions.

This journal records an externally observed outcome without reopening the original
execution. It shares the SQLite database owned by SQLiteExecutionStore and adds an
independent hash chain. Evidence references and digests are recorded, not magically
authenticated: a governance/witness process must verify the evidence itself.
"""
from __future__ import annotations

import hashlib
import json
import re
from contextlib import closing
from dataclasses import dataclass
from typing import Any

from mizan_execution_store import SQLiteExecutionStore


_ALLOWED_OBSERVATIONS = {"SUCCEEDED", "FAILED"}
_GENESIS = "0" * 64
_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


class ReconciliationJournalError(ValueError):
    """Raised when reconciliation cannot be safely recorded."""


@dataclass(frozen=True)
class ReconciliationRecord:
    event_seq: int
    execution_id: str
    observed_outcome: str
    evidence_ref: str
    evidence_sha256: str
    actor: str
    occurred_at: str
    prev_hash: str
    hash: str


def _canonical(value: Any) -> str:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"),
        ensure_ascii=False, allow_nan=False,
    )


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


class SQLiteReconciliationJournal:
    """Append-only-by-API observations; never changes execution status or dispatches."""

    def __init__(self, execution_store: SQLiteExecutionStore):
        if not isinstance(execution_store, SQLiteExecutionStore):
            raise TypeError("execution_store must be a SQLiteExecutionStore")
        self._store = execution_store
        with closing(self._store._connect()) as con:
            con.execute("""
                CREATE TABLE IF NOT EXISTS execution_reconciliations (
                    event_seq INTEGER PRIMARY KEY,
                    execution_id TEXT NOT NULL UNIQUE
                        REFERENCES executions(execution_id),
                    observed_outcome TEXT NOT NULL
                        CHECK(observed_outcome IN ('SUCCEEDED','FAILED')),
                    evidence_ref TEXT NOT NULL,
                    evidence_sha256 TEXT NOT NULL,
                    actor TEXT NOT NULL,
                    occurred_at TEXT NOT NULL,
                    prev_hash TEXT NOT NULL,
                    hash TEXT NOT NULL UNIQUE
                )
            """)

    @staticmethod
    def _validate_text(name: str, value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ReconciliationJournalError(f"{name} is required")
        return value.strip()

    @staticmethod
    def _fields(row: Any) -> dict[str, Any]:
        return {
            "schema": "mizan.execution-reconciliation.v1",
            "event_seq": row["event_seq"],
            "execution_id": row["execution_id"],
            "observed_outcome": row["observed_outcome"],
            "evidence_ref": row["evidence_ref"],
            "evidence_sha256": row["evidence_sha256"],
            "actor": row["actor"],
            "occurred_at": row["occurred_at"],
            "prev_hash": row["prev_hash"],
        }

    def record(
        self, *, execution_id: str, observed_outcome: str,
        evidence_ref: str, evidence_sha256: str, actor: str, now: str,
    ) -> ReconciliationRecord:
        """Record a verified observation while leaving the execution UNKNOWN."""
        execution_id = self._validate_text("execution_id", execution_id)
        evidence_ref = self._validate_text("evidence_ref", evidence_ref)
        actor = self._validate_text("actor", actor)
        now = self._validate_text("now", now)
        if observed_outcome not in _ALLOWED_OBSERVATIONS:
            raise ReconciliationJournalError(
                "observed_outcome must be SUCCEEDED or FAILED"
            )
        if not isinstance(evidence_sha256, str) or not _SHA256_RE.fullmatch(evidence_sha256):
            raise ReconciliationJournalError(
                "evidence_sha256 must be a 64-character SHA-256 hex digest"
            )
        evidence_sha256 = evidence_sha256.lower()

        con = self._store._connect()
        try:
            con.execute("BEGIN IMMEDIATE")
            execution = con.execute(
                "SELECT status FROM executions WHERE execution_id=?",
                (execution_id,),
            ).fetchone()
            if execution is None:
                raise ReconciliationJournalError("execution_id not found")
            if execution["status"] != "UNKNOWN":
                raise ReconciliationJournalError(
                    "only terminal UNKNOWN executions may be reconciled"
                )
            existing = con.execute(
                "SELECT event_seq FROM execution_reconciliations WHERE execution_id=?",
                (execution_id,),
            ).fetchone()
            if existing:
                raise ReconciliationJournalError(
                    "reconciliation already recorded for this execution"
                )

            previous = con.execute(
                "SELECT event_seq, hash FROM execution_reconciliations "
                "ORDER BY event_seq DESC LIMIT 1"
            ).fetchone()
            event_seq = previous["event_seq"] + 1 if previous else 1
            prev_hash = previous["hash"] if previous else _GENESIS
            payload = {
                "schema": "mizan.execution-reconciliation.v1",
                "event_seq": event_seq,
                "execution_id": execution_id,
                "observed_outcome": observed_outcome,
                "evidence_ref": evidence_ref,
                "evidence_sha256": evidence_sha256,
                "actor": actor,
                "occurred_at": now,
                "prev_hash": prev_hash,
            }
            event_hash = _sha256(_canonical(payload))
            con.execute("""
                INSERT INTO execution_reconciliations
                    (event_seq,execution_id,observed_outcome,evidence_ref,
                     evidence_sha256,actor,occurred_at,prev_hash,hash)
                VALUES(?,?,?,?,?,?,?,?,?)
            """, (
                event_seq, execution_id, observed_outcome, evidence_ref,
                evidence_sha256, actor, now, prev_hash, event_hash,
            ))
            # Critical invariant: the execution snapshot remains UNKNOWN.
            unchanged = con.execute(
                "SELECT status FROM executions WHERE execution_id=?",
                (execution_id,),
            ).fetchone()
            if unchanged["status"] != "UNKNOWN":
                raise ReconciliationJournalError(
                    "execution state changed during reconciliation"
                )
            con.execute("COMMIT")
            return ReconciliationRecord(
                event_seq, execution_id, observed_outcome, evidence_ref,
                evidence_sha256, actor, now, prev_hash, event_hash,
            )
        except Exception:
            if con.in_transaction:
                con.execute("ROLLBACK")
            raise
        finally:
            con.close()

    def get(self, execution_id: str) -> ReconciliationRecord | None:
        with self._store._connect() as con:
            row = con.execute(
                "SELECT * FROM execution_reconciliations WHERE execution_id=?",
                (execution_id,),
            ).fetchone()
        if row is None:
            return None
        return ReconciliationRecord(
            row["event_seq"], row["execution_id"], row["observed_outcome"],
            row["evidence_ref"], row["evidence_sha256"], row["actor"],
            row["occurred_at"], row["prev_hash"], row["hash"],
        )

    def verify_chain(self) -> dict[str, Any]:
        """Verify the chain, row digests, event coverage, and UNKNOWN source state."""
        with self._store._connect() as con:
            rows = con.execute(
                "SELECT * FROM execution_reconciliations ORDER BY event_seq"
            ).fetchall()
            executions = {
                row["execution_id"]: row["status"]
                for row in con.execute("SELECT execution_id,status FROM executions")
            }

        prev_hash = _GENESIS
        seen: set[str] = set()
        for expected_seq, row in enumerate(rows, start=1):
            if row["event_seq"] != expected_seq:
                return {"ok": False, "reason": "SEQUENCE_GAP",
                        "verified_events": expected_seq - 1}
            if row["execution_id"] in seen:
                return {"ok": False, "reason": "DUPLICATE_EXECUTION_RECONCILIATION",
                        "verified_events": expected_seq - 1}
            if row["execution_id"] not in executions:
                return {"ok": False, "reason": "EXECUTION_NOT_FOUND",
                        "verified_events": expected_seq - 1}
            if executions[row["execution_id"]] != "UNKNOWN":
                return {"ok": False, "reason": "SOURCE_EXECUTION_NOT_UNKNOWN",
                        "verified_events": expected_seq - 1}
            if row["observed_outcome"] not in _ALLOWED_OBSERVATIONS:
                return {"ok": False, "reason": "INVALID_OBSERVED_OUTCOME",
                        "verified_events": expected_seq - 1}
            if not row["evidence_ref"].strip() or not _SHA256_RE.fullmatch(row["evidence_sha256"]):
                return {"ok": False, "reason": "INVALID_EVIDENCE_REFERENCE",
                        "verified_events": expected_seq - 1}
            if row["prev_hash"] != prev_hash:
                return {"ok": False, "reason": "PREVIOUS_HASH_MISMATCH",
                        "verified_events": expected_seq - 1}
            actual_hash = _sha256(_canonical(self._fields(row)))
            if row["hash"] != actual_hash:
                return {"ok": False, "reason": "EVENT_HASH_MISMATCH",
                        "verified_events": expected_seq - 1}
            seen.add(row["execution_id"])
            prev_hash = actual_hash

        return {
            "ok": True,
            "reason": "RECONCILIATION_CHAIN_CONSISTENT",
            "verified_events": len(rows),
            "tip_hash": prev_hash,
            "reconciled_executions": len(seen),
        }
