import unittest

from src.mizan_reconciliation import (
    ExecutionOutcome,
    Outcome,
    ReconciliationError,
    mark_unknown,
    may_dispatch,
    reconcile,
    start,
    terminal,
)


class ReconciliationTests(unittest.TestCase):
    def test_unknown_outcome_blocks_automatic_retry(self):
        running = start(ExecutionOutcome("exec-1"))
        unknown = mark_unknown(running, "network timeout after request")
        self.assertEqual(unknown.status, Outcome.UNKNOWN)
        self.assertFalse(may_dispatch(unknown))
        self.assertFalse(terminal(unknown))

    def test_unknown_can_be_resolved_only_with_evidence(self):
        unknown = mark_unknown(start(ExecutionOutcome("exec-2")), "response lost")
        resolved = reconcile(
            unknown,
            observed_outcome=Outcome.SUCCEEDED,
            evidence_ref="provider-receipt:abc123",
        )
        self.assertEqual(resolved.execution_id, "exec-2")
        self.assertEqual(resolved.status, Outcome.SUCCEEDED)
        self.assertEqual(resolved.evidence_ref, "provider-receipt:abc123")
        self.assertTrue(terminal(resolved))
        self.assertFalse(may_dispatch(resolved))

    def test_reconciliation_rejects_missing_evidence(self):
        unknown = mark_unknown(start(ExecutionOutcome("exec-3")), "timeout")
        with self.assertRaisesRegex(ReconciliationError, "evidence reference"):
            reconcile(unknown, observed_outcome=Outcome.FAILED, evidence_ref=" ")

    def test_reconciliation_rejects_unresolved_observation(self):
        unknown = mark_unknown(start(ExecutionOutcome("exec-4")), "timeout")
        with self.assertRaisesRegex(ReconciliationError, "SUCCEEDED or FAILED"):
            reconcile(unknown, observed_outcome=Outcome.UNKNOWN, evidence_ref="ticket-7")

    def test_cannot_reconcile_non_unknown_or_start_twice(self):
        pending = ExecutionOutcome("exec-5")
        running = start(pending)
        with self.assertRaisesRegex(ReconciliationError, "only UNKNOWN"):
            reconcile(running, observed_outcome=Outcome.FAILED, evidence_ref="ticket-8")
        with self.assertRaisesRegex(ReconciliationError, "only PENDING"):
            start(running)

    def test_unknown_requires_reason(self):
        with self.assertRaisesRegex(ReconciliationError, "non-empty reason"):
            mark_unknown(start(ExecutionOutcome("exec-6")), " ")


if __name__ == "__main__":
    unittest.main()
