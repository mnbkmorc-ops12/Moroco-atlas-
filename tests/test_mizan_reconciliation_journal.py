from __future__ import annotations

import hashlib
import sqlite3
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from mizan_execution_store import SQLiteExecutionStore
from mizan_governance import ExecutionStatus
from mizan_reconciliation_journal import (
    ReconciliationJournalError,
    SQLiteReconciliationJournal,
)


def sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


class SQLiteReconciliationJournalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp.name) / "mizan.sqlite3"
        self.store = SQLiteExecutionStore(self.db_path)
        self.journal = SQLiteReconciliationJournal(self.store)
        self._make_unknown("exec-001")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _make_unknown(self, execution_id: str) -> None:
        suffix = execution_id
        self.store.create_execution(
            execution_id=execution_id,
            intent_id=f"intent-{suffix}",
            idempotency_key=f"idem-{suffix}",
            request_digest=sha(f"request-{suffix}"),
            now="2026-10-27T00:00:00Z",
        )
        claimed = self.store.claim_once(
            execution_id=execution_id,
            worker_id="worker-a",
            now="2026-10-27T00:01:00Z",
        )
        self.assertTrue(claimed.claimed)
        self.store.transition(
            execution_id=execution_id,
            expected=ExecutionStatus.CLAIMED,
            target=ExecutionStatus.UNKNOWN,
            actor="worker-a",
            now="2026-10-27T00:02:00Z",
            detail="remote request timed out; external outcome not known",
        )

    def _record(self, execution_id: str = "exec-001", observed: str = "SUCCEEDED"):
        return self.journal.record(
            execution_id=execution_id,
            observed_outcome=observed,
            evidence_ref=f"provider-audit://receipt/{execution_id}",
            evidence_sha256=sha(f"independently-collected-evidence:{execution_id}:{observed}"),
            actor="witness-verifier-01",
            now="2026-10-27T00:03:00Z",
        )

    def test_records_observation_without_reopening_or_retrying(self) -> None:
        record = self._record()
        self.assertEqual(record.observed_outcome, "SUCCEEDED")
        self.assertEqual(self.store.get("exec-001").status, ExecutionStatus.UNKNOWN)
        self.assertFalse(self.store.claim_once(
            execution_id="exec-001", worker_id="worker-b",
            now="2026-10-27T00:04:00Z",
        ).claimed)
        self.assertTrue(self.journal.verify_chain()["ok"])
        self.assertEqual(self.journal.get("exec-001"), record)

    def test_rejects_non_unknown_source_execution(self) -> None:
        self.store.create_execution(
            execution_id="exec-pending",
            intent_id="intent-pending",
            idempotency_key="idem-pending",
            request_digest=sha("pending-request"),
            now="2026-10-27T00:00:00Z",
        )
        with self.assertRaisesRegex(ReconciliationJournalError, "UNKNOWN"):
            self._record("exec-pending")
        self.assertEqual(self.journal.verify_chain()["verified_events"], 0)

    def test_requires_outcome_evidence_reference_and_digest(self) -> None:
        common = {
            "execution_id": "exec-001",
            "actor": "witness",
            "now": "2026-10-27T00:03:00Z",
            "evidence_ref": "provider-ticket:123",
            "evidence_sha256": sha("evidence"),
        }
        with self.assertRaisesRegex(ReconciliationJournalError, "SUCCEEDED or FAILED"):
            self.journal.record(**common, observed_outcome="UNKNOWN")
        with self.assertRaisesRegex(ReconciliationJournalError, "evidence_ref"):
            self.journal.record(**{**common, "evidence_ref": " "},
                                observed_outcome="FAILED")
        with self.assertRaisesRegex(ReconciliationJournalError, "SHA-256"):
            self.journal.record(**{**common, "evidence_sha256": "not-a-digest"},
                                observed_outcome="FAILED")
        self.assertTrue(self.journal.verify_chain()["ok"])
        self.assertEqual(self.journal.verify_chain()["verified_events"], 0)

    def test_only_one_reconciliation_record_per_execution(self) -> None:
        self._record()
        with self.assertRaisesRegex(ReconciliationJournalError, "already recorded"):
            self._record(observed="FAILED")
        self.assertEqual(self.journal.verify_chain()["verified_events"], 1)

    def test_concurrent_records_have_unique_contiguous_sequence(self) -> None:
        execution_ids = [f"exec-{i:03d}" for i in range(2, 14)]
        for execution_id in execution_ids:
            self._make_unknown(execution_id)

        def write(execution_id: str):
            return self.journal.record(
                execution_id=execution_id,
                observed_outcome="FAILED" if execution_id.endswith(("2", "4", "6")) else "SUCCEEDED",
                evidence_ref=f"provider-audit://receipt/{execution_id}",
                evidence_sha256=sha(f"evidence:{execution_id}"),
                actor=f"witness-{execution_id}",
                now="2026-10-27T00:10:00Z",
            )

        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(write, execution_ids))
        self.assertEqual(len({item.event_seq for item in results}), len(execution_ids))
        verification = self.journal.verify_chain()
        self.assertTrue(verification["ok"], verification)
        self.assertEqual(verification["verified_events"], len(execution_ids))

    def test_concurrent_duplicate_reconciliation_has_one_winner(self) -> None:
        def write(_index: int):
            try:
                self._record()
                return "recorded"
            except ReconciliationJournalError:
                return "rejected"

        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(write, range(16)))
        self.assertEqual(results.count("recorded"), 1)
        self.assertEqual(results.count("rejected"), 15)
        self.assertEqual(self.journal.verify_chain()["verified_events"], 1)

    def test_verifier_detects_tampered_evidence_digest(self) -> None:
        self._record()
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                "UPDATE execution_reconciliations SET evidence_sha256=? WHERE execution_id=?",
                (sha("tampered"), "exec-001"),
            )
        result = self.journal.verify_chain()
        self.assertFalse(result["ok"])
        self.assertEqual(result["reason"], "EVENT_HASH_MISMATCH")


if __name__ == "__main__":
    unittest.main()
