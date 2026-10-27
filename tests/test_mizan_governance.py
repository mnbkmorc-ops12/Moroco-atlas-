import unittest
from mizan_governance import (
    Decision, Evidence, ExecutionStatus, GovernanceError,
    evaluate_request, transition,
)


class GovernanceTests(unittest.TestCase):
    def setUp(self):
        self.evidence = Evidence("ev-1", "independent-test-report", "a" * 64, True)

    def test_missing_evidence_is_unresolved(self):
        result = evaluate_request(intent_id="i1", rule_id="r1", rationale="test",
                                  required_evidence=("ev-1",), evidence=(),
                                  explicit_rule_match=True)
        self.assertEqual(result.decision, Decision.UNRESOLVED)

    def test_unverified_evidence_is_unresolved(self):
        evidence = Evidence("ev-1", "report", "a" * 64, False)
        result = evaluate_request(intent_id="i1", rule_id="r1", rationale="test",
                                  required_evidence=("ev-1",), evidence=(evidence,),
                                  explicit_rule_match=True)
        self.assertEqual(result.decision, Decision.UNRESOLVED)

    def test_explicit_rule_mismatch_is_denied(self):
        result = evaluate_request(intent_id="i1", rule_id="r1", rationale="test",
                                  required_evidence=(), evidence=(),
                                  explicit_rule_match=False)
        self.assertEqual(result.decision, Decision.DENIED)

    def test_verified_evidence_and_rule_match_authorize(self):
        result = evaluate_request(intent_id="i1", rule_id="r1", rationale="test",
                                  required_evidence=("ev-1",), evidence=(self.evidence,),
                                  explicit_rule_match=True)
        self.assertEqual(result.decision, Decision.AUTHORIZED)

    def test_unknown_cannot_be_retried(self):
        with self.assertRaises(GovernanceError):
            transition(ExecutionStatus.UNKNOWN, ExecutionStatus.PENDING)

    def test_running_cannot_return_to_pending(self):
        with self.assertRaises(GovernanceError):
            transition(ExecutionStatus.RUNNING, ExecutionStatus.PENDING)

    def test_pending_can_be_claimed(self):
        self.assertEqual(transition(ExecutionStatus.PENDING, ExecutionStatus.CLAIMED),
                         ExecutionStatus.CLAIMED)


if __name__ == "__main__":
    unittest.main()
