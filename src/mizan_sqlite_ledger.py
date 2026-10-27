"""MIZAN CORE v0.5 — transactional SQLite audit ledger.

This module is a local reference implementation for software tests. It is not a
replacement for the Supabase production/test database and does not certify safety.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any


GENESIS = "0" * 64
SCHEMA_VERSION = "mizan.sqlite-ledger.v1"


class LedgerError(RuntimeError):
    pass


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class AppendResult:
    seq: int
    event_id: str
    idempotency_key: str
    prev_hash: str
    hash: str
    duplicate: bool = False


class SQLiteAuditLedger:
    """Append-only ledger using SQLite BEGIN IMMEDIATE and unique idempotency keys."""

    def __init__(self, path: str | Path):
        self.path = str(path)
        if self.path != ":memory:":
            Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        con = sqlite3.connect(self.path, timeout=15.0, isolation_level=None)
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA busy_timeout = 15000")
        con.execute("PRAGMA foreign_keys = ON")
        # Use full commit durability for this audit reference ledger.
        con.execute("PRAGMA synchronous = FULL")
        return con

    def _initialize(self) -> None:
        with self._connect() as con:
            con.execute("PRAGMA journal_mode = WAL")
            con.executescript("""
                CREATE TABLE IF NOT EXISTS ledger (
                    seq INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id TEXT NOT NULL UNIQUE,
                    idempotency_key TEXT NOT NULL UNIQUE,
                    event_type TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    recorded_at TEXT NOT NULL,
                    prev_hash TEXT NOT NULL,
                    hash TEXT NOT NULL UNIQUE
                );
                CREATE TABLE IF NOT EXISTS ledger_head (
                    singleton INTEGER PRIMARY KEY CHECK (singleton = 1),
                    seq INTEGER NOT NULL,
                    hash TEXT NOT NULL
                );
                INSERT OR IGNORE INTO ledger_head(singleton, seq, hash)
                    VALUES (1, 0, '0000000000000000000000000000000000000000000000000000000000000000');
            """)

    @staticmethod
    def _hash_fields(seq: int, event_id: str, idempotency_key: str,
                     event_type: str, payload_json: str, recorded_at: str,
                     prev_hash: str) -> str:
        # Hash canonical fields as one canonical JSON object to avoid delimiter ambiguity.
        body = canonical_json({
            "schema": SCHEMA_VERSION, "seq": seq, "event_id": event_id,
            "idempotency_key": idempotency_key, "event_type": event_type,
            "payload_json": payload_json, "recorded_at": recorded_at,
            "prev_hash": prev_hash,
        })
        return sha256_text(body)

    def append(self, *, event_id: str, idempotency_key: str,
               event_type: str, payload: dict[str, Any], recorded_at: str) -> AppendResult:
        for name, value in (("event_id", event_id), ("idempotency_key", idempotency_key),
                            ("event_type", event_type), ("recorded_at", recorded_at)):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} is required")
        payload_json = canonical_json(payload)
        con = self._connect()
        try:
            con.execute("BEGIN IMMEDIATE")
            existing = con.execute(
                """SELECT seq,event_id,idempotency_key,event_type,payload_json,recorded_at,
                          prev_hash,hash
                   FROM ledger WHERE idempotency_key=?""",
                (idempotency_key,),
            ).fetchone()
            if existing:
                # Idempotency means replaying the same intent, not silently accepting
                # a changed payload under a previously used key.
                same_intent = (
                    existing["event_id"] == event_id
                    and existing["event_type"] == event_type
                    and existing["payload_json"] == payload_json
                    and existing["recorded_at"] == recorded_at
                )
                if not same_intent:
                    raise LedgerError(
                        "idempotency key was reused with a different event intent"
                    )
                con.execute("COMMIT")
                return AppendResult(
                    seq=existing["seq"],
                    event_id=existing["event_id"],
                    idempotency_key=existing["idempotency_key"],
                    prev_hash=existing["prev_hash"],
                    hash=existing["hash"],
                    duplicate=True,
                )

            duplicate_id = con.execute(
                "SELECT idempotency_key FROM ledger WHERE event_id=?", (event_id,)
            ).fetchone()
            if duplicate_id:
                raise LedgerError("event_id already exists with a different idempotency key")

            head = con.execute("SELECT seq,hash FROM ledger_head WHERE singleton=1").fetchone()
            if not head:
                raise LedgerError("ledger head missing")
            tip = con.execute("SELECT seq,hash FROM ledger ORDER BY seq DESC LIMIT 1").fetchone()
            if head["seq"] == 0:
                if tip is not None or head["hash"] != GENESIS:
                    raise LedgerError("genesis head does not match empty ledger")
            elif not tip or tip["seq"] != head["seq"] or tip["hash"] != head["hash"]:
                raise LedgerError("ledger head does not match ledger tip")

            seq = head["seq"] + 1
            prev_hash = head["hash"]
            digest = self._hash_fields(seq, event_id, idempotency_key, event_type,
                                       payload_json, recorded_at, prev_hash)
            con.execute("""
                INSERT INTO ledger(seq,event_id,idempotency_key,event_type,payload_json,
                                   recorded_at,prev_hash,hash)
                VALUES(?,?,?,?,?,?,?,?)
            """, (seq,event_id,idempotency_key,event_type,payload_json,recorded_at,prev_hash,digest))
            con.execute("UPDATE ledger_head SET seq=?,hash=? WHERE singleton=1",
                        (seq,digest))
            con.execute("COMMIT")
            return AppendResult(seq,event_id,idempotency_key,prev_hash,digest,False)
        except Exception:
            if con.in_transaction:
                con.execute("ROLLBACK")
            raise
        finally:
            con.close()

    def verify(self) -> dict[str, Any]:
        con = self._connect()
        try:
            rows = con.execute("SELECT * FROM ledger ORDER BY seq").fetchall()
            head = con.execute("SELECT seq,hash FROM ledger_head WHERE singleton=1").fetchone()
            previous = GENESIS
            errors: list[str] = []
            expected_seq = 1
            for row in rows:
                if row["seq"] != expected_seq:
                    errors.append(f"sequence gap at {row['seq']}; expected {expected_seq}")
                if row["prev_hash"] != previous:
                    errors.append(f"previous hash mismatch at seq {row['seq']}")
                calculated = self._hash_fields(
                    row["seq"], row["event_id"], row["idempotency_key"], row["event_type"],
                    row["payload_json"], row["recorded_at"], row["prev_hash"])
                if calculated != row["hash"]:
                    errors.append(f"hash mismatch at seq {row['seq']}")
                previous = row["hash"]
                expected_seq += 1
            tip_seq = rows[-1]["seq"] if rows else 0
            tip_hash = rows[-1]["hash"] if rows else GENESIS
            if not head or head["seq"] != tip_seq or head["hash"] != tip_hash:
                errors.append("head does not match ledger tip")
            return {
                "ok": not errors,
                "status": "STRUCTURE_AND_CHAIN_CONSISTENT" if not errors else "FAIL",
                "rows": len(rows), "head_seq": head["seq"] if head else None,
                "errors": errors,
            }
        finally:
            con.close()

    def get_by_idempotency_key(self, key: str) -> dict[str, Any] | None:
        with self._connect() as con:
            row = con.execute("SELECT * FROM ledger WHERE idempotency_key=?", (key,)).fetchone()
            return dict(row) if row else None
