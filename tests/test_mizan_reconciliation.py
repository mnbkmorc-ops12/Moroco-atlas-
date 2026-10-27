import pytest

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


def test_unknown_outcome_blocks_automatic_retry():
    running = start(ExecutionOutcome("exec-1"))
    unknown = mark_unknown(running, "network timeout after request")
    assert unknown.status is Outcome.UNKNOWN
    assert may_dispatch(unknown) is False
    assert terminal(unknown) is False


def test_unknown_can_be_resolved_only_with_evidence():
    unknown = mark_unknown(start(ExecutionOutcome("exec-2")), "response lost")
    resolved = reconcile(
        unknown,
        observed_outcome=Outcome.SUCCEEDED,
        evidence_ref="provider-receipt:abc123",
    )
    assert resolved.execution_id == "exec-2"
    assert resolved.status is Outcome.SUCCEEDED
    assert resolved.evidence_ref == "provider-receipt:abc123"
    assert terminal(resolved)
    assert not may_dispatch(resolved)


def test_reconciliation_rejects_missing_evidence():
    unknown = mark_unknown(start(ExecutionOutcome("exec-3")), "timeout")
    with pytest.raises(ReconciliationError, match="evidence reference"):
        reconcile(unknown, observed_outcome=Outcome.FAILED, evidence_ref=" ")


def test_reconciliation_rejects_unresolved_observation():
    unknown = mark_unknown(start(ExecutionOutcome("exec-4")), "timeout")
    with pytest.raises(ReconciliationError, match="SUCCEEDED or FAILED"):
        reconcile(unknown, observed_outcome=Outcome.UNKNOWN, evidence_ref="ticket-7")


def test_cannot_reconcile_non_unknown_or_start_twice():
    pending = ExecutionOutcome("exec-5")
    running = start(pending)
    with pytest.raises(ReconciliationError, match="only UNKNOWN"):
        reconcile(running, observed_outcome=Outcome.FAILED, evidence_ref="ticket-8")
    with pytest.raises(ReconciliationError, match="only PENDING"):
        start(running)


def test_unknown_requires_reason():
    with pytest.raises(ReconciliationError, match="non-empty reason"):
        mark_unknown(start(ExecutionOutcome("exec-6")), " ")
