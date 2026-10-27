"""MIZAN CORE external-effect reconciliation policy model.

UNKNOWN is terminal for the original execution and never permission to retry.
Reconciliation returns a separate observation about the external system; it
does not mutate/reopen the original execution and is not a durable journal.
Persist observations through SQLiteReconciliationJournal.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Outcome(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"
    CANCELLED = "CANCELLED"


class ReconciliationError(ValueError):
    """Raised when an observation lacks the required evidence or state."""


@dataclass(frozen=True)
class ExecutionOutcome:
    execution_id: str
    status: Outcome = Outcome.PENDING
    evidence_ref: str | None = None
    note: str | None = None


@dataclass(frozen=True)
class ReconciliationObservation:
    """Evidence-backed observation, distinct from the immutable execution state."""
    execution_id: str
    prior_status: Outcome
    observed_outcome: Outcome
    evidence_ref: str
    note: str


_TERMINAL = {
    Outcome.SUCCEEDED, Outcome.FAILED, Outcome.UNKNOWN, Outcome.CANCELLED
}


def start(record: ExecutionOutcome) -> ExecutionOutcome:
    if record.status is not Outcome.PENDING:
        raise ReconciliationError("only PENDING executions may start")
    return ExecutionOutcome(record.execution_id, Outcome.RUNNING)


def mark_unknown(record: ExecutionOutcome, reason: str) -> ExecutionOutcome:
    if record.status not in {Outcome.RUNNING, Outcome.PENDING}:
        raise ReconciliationError("only PENDING/RUNNING executions may become UNKNOWN")
    if not isinstance(reason, str) or not reason.strip():
        raise ReconciliationError("UNKNOWN requires a non-empty reason")
    return ExecutionOutcome(record.execution_id, Outcome.UNKNOWN, note=reason.strip())


def reconcile(
    record: ExecutionOutcome,
    *,
    observed_outcome: Outcome,
    evidence_ref: str,
) -> ReconciliationObservation:
    """Record a model observation; the original execution stays terminal UNKNOWN."""
    if record.status is not Outcome.UNKNOWN:
        raise ReconciliationError("reconciliation is allowed only from UNKNOWN")
    if observed_outcome not in {Outcome.SUCCEEDED, Outcome.FAILED}:
        raise ReconciliationError("evidence must resolve to SUCCEEDED or FAILED")
    if not isinstance(evidence_ref, str) or not evidence_ref.strip():
        raise ReconciliationError("an evidence reference is required")
    return ReconciliationObservation(
        execution_id=record.execution_id,
        prior_status=record.status,
        observed_outcome=observed_outcome,
        evidence_ref=evidence_ref.strip(),
        note=f"observation for terminal UNKNOWN execution; prior note: {record.note or 'none'}",
    )


def may_dispatch(record: ExecutionOutcome) -> bool:
    """Only a new PENDING record may be dispatched; UNKNOWN is never retried."""
    return record.status is Outcome.PENDING


def terminal(record: ExecutionOutcome) -> bool:
    return record.status in _TERMINAL
