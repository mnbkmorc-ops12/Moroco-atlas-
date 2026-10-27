from __future__ import annotations

import hashlib
import sqlite3
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from mizan_execution_store import ExecutionStoreError, SQLiteExecutionStore
from mizan_governance import ExecutionStatus, GovernanceError


def digest() -> str:
    return hashlib.sha256(b"fixed test request").hexdigest()


class SQLiteExecutionStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp.name) / "execution.sqlite3"
        self.store = SQLiteExecutionStore(self.db_path)
        self.store.create_execution(
            execution_id="exec-001", intent_id="intent-001",
            idempotency_key="idem-001", request_digest=digest(),
            now="2026-10-27T00:00:00Z",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_only_one_concurrent_worker_can_claim(self) -> None:
        # Each call creates its own SQLite connection. BEGIN IMMEDIATE serializes claims.
        workers = [f"worker-{i:02d}" for i in range(24)]

        def claim(worker: str):
            return self.store.claim_once(
                execution_id="exec-001", worker_id=worker,
                now="2026-10-27T00:01:00Z",
            )

        with ThreadPoolExecutor(max_workers=12) as pool:
            results = list(pool.map(claim, workers))

        winners = [result for result in results if result.claimed]
        self.assertEqual(len(winners), 1)
        self.assertEqual(sum(not result.claimed for result in results), len(workers) - 1)
        self.assertEqual(self.store.get("exec-001").status, ExecutionStatus.CLAIMED)
        self.assertEqual(self.store.verify_event_chain()["ok"], True)

    def test_execution_identity_is_immutable(self) -> None:
        duplicate = self.store.create_execution(
            execution_id="exec-001", intent_id="intent-001",
            idempotency_key="idem-001", request_digest=digest(),
            now="2026-10-27T00:02:00Z",
        )
        self.assertFalse(duplicate.created)
        self.assertEqual(duplicate.status, ExecutionStatus.PENDING)
        with self.assertRaises(ExecutionStoreError):
            self.store.create_execution(
                execution_id="exec-001", intent_id="intent-changed",
                idempotency_key="idem-001", request_digest=digest(),
                now="2026-10-27T00:03:00Z",
            )

    def test_idempotency_key_cannot_bind_two_execution_ids(self) -> None:
        with self.assertRaises(ExecutionStoreError):
            self.store.create_execution(
                execution_id="exec-002", intent_id="intent-002",
                idempotency_key="idem-001", request_digest=digest(),
                now="2026-10-27T00:04:00Z",
            )

    def test_unknown_is_terminal_and_never_reclaimed(self) -> None:
        claim = self.store.claim_once(
            execution_id="exec-001", worker_id="worker-a",
            now="2026-10-27T00:05:00Z",
        )
        self.assertTrue(claim.claimed)
        self.store.transition(
            execution_id="exec-001", expected=ExecutionStatus.CLAIMED,
            target=ExecutionStatus.UNKNOWN, actor="worker-a",
            now="2026-10-27T00:06:00Z",
            detail="external outcome uncertain; reconcile before new intent",
        )
        another = self.store.claim_once(
            execution_id="exec-001", worker_id="worker-b",
            now="2026-10-27T00:07:00Z",
        )
        self.assertFalse(another.claimed)
        self.assertEqual(another.record.status, ExecutionStatus.UNKNOWN)
        with self.assertRaises(GovernanceError):
            self.store.transition(
                execution_id="exec-001", expected=ExecutionStatus.UNKNOWN,
                target=ExecutionStatus.RUNNING, actor="worker-b",
                now="2026-10-27T00:08:00Z",
            )
        self.assertTrue(self.store.verify_event_chain()["ok"])

    def test_compare_and_set_rejects_wrong_expected_status(self) -> None:
        with self.assertRaises(ExecutionStoreError):
            self.store.transition(
                execution_id="exec-001", expected=ExecutionStatus.RUNNING,
                target=ExecutionStatus.SUCCEEDED, actor="worker-a",
                now="2026-10-27T00:09:00Z",
            )
        self.assertEqual(self.store.get("exec-001").status, ExecutionStatus.PENDING)

    def test_claim_transition_cannot_bypass_claim_once(self) -> None:
        with self.assertRaisesRegex(GovernanceError, "claim_once"):
            self.store.transition(
                execution_id="exec-001", expected=ExecutionStatus.PENDING,
                target=ExecutionStatus.CLAIMED, actor="worker-a",
                now="2026-10-27T00:09:30Z",
            )
        self.assertEqual(self.store.get("exec-001").status, ExecutionStatus.PENDING)
        self.assertTrue(self.store.verify_event_chain()["ok"])

    def test_only_claim_owner_can_transition_claimed_or_running_execution(self) -> None:
        self.assertTrue(self.store.claim_once(
            execution_id="exec-001", worker_id="worker-a",
            now="2026-10-27T00:09:40Z",
        ).claimed)
        with self.assertRaisesRegex(ExecutionStoreError, "worker ownership mismatch"):
            self.store.transition(
                execution_id="exec-001", expected=ExecutionStatus.CLAIMED,
                target=ExecutionStatus.RUNNING, actor="worker-b",
                now="2026-10-27T00:09:50Z",
            )
        self.assertEqual(self.store.get("exec-001").status, ExecutionStatus.CLAIMED)
        self.store.transition(
            execution_id="exec-001", expected=ExecutionStatus.CLAIMED,
            target=ExecutionStatus.RUNNING, actor="worker-a",
            now="2026-10-27T00:09:55Z",
        )
        with self.assertRaisesRegex(ExecutionStoreError, "worker ownership mismatch"):
            self.store.transition(
                execution_id="exec-001", expected=ExecutionStatus.RUNNING,
                target=ExecutionStatus.SUCCEEDED, actor="worker-b",
                now="2026-10-27T00:09:57Z",
            )
        self.assertEqual(self.store.get("exec-001").status, ExecutionStatus.RUNNING)
        self.assertTrue(self.store.verify_event_chain()["ok"])

    def test_terminal_success_cannot_transition_again(self) -> None:
        self.store.claim_once(execution_id="exec-001", worker_id="worker-a",
                              now="2026-10-27T00:10:00Z")
        self.store.transition(execution_id="exec-001", expected=ExecutionStatus.CLAIMED,
                              target=ExecutionStatus.RUNNING, actor="worker-a",
                              now="2026-10-27T00:11:00Z")
        self.store.transition(execution_id="exec-001", expected=ExecutionStatus.RUNNING,
                              target=ExecutionStatus.SUCCEEDED, actor="worker-a",
                              now="2026-10-27T00:12:00Z", detail="test-only success")
        with self.assertRaises(GovernanceError):
            self.store.transition(execution_id="exec-001", expected=ExecutionStatus.SUCCEEDED,
                                  target=ExecutionStatus.RUNNING, actor="worker-a",
                                  now="2026-10-27T00:13:00Z")
        self.assertTrue(self.store.verify_event_chain()["ok"])

    def test_missing_execution_cannot_be_claimed(self) -> None:
        with self.assertRaises(ExecutionStoreError):
            self.store.claim_once(execution_id="missing", worker_id="worker-a",
                                  now="2026-10-27T00:14:00Z")


    def test_verifier_detects_snapshot_changed_without_audit_event(self) -> None:
        # Simulate an out-of-band database mutation that bypasses the journal API.
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                "UPDATE executions SET status=? WHERE execution_id=?",
                (ExecutionStatus.SUCCEEDED.value, "exec-001"),
            )
        result = self.store.verify_event_chain()
        self.assertFalse(result["ok"])
        self.assertEqual(result["reason"], "CURRENT_STATE_MISMATCH")


    def test_plain_memory_database_is_rejected(self) -> None:
        # This implementation opens a fresh connection per operation, so a plain
        # :memory: database would silently lose its schema between calls.
        with self.assertRaises(ValueError):
            SQLiteExecutionStore(":memory:")


if __name__ == "__main__":
    unittest.main()
