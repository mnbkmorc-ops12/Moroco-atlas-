"""MIZAN CORE external-effect reconciliation state machine.

An UNKNOWN outcome is not permission to retry. Reconciliation requires explicit
independent evidence and records the evidence reference supplied by the caller.
This module is a reference model, not a distributed transaction guarantee.
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
    """Raised when a transition lacks authority or evidence."""


@dataclass(frozen=True)
class ExecutionOutcome:
    execution_id: str
    status: Outcome = Outcome.PENDING
    evidence_ref: str | None = None
    note: str | None = None


_TERMINAL = {Outcome.SUCCEEDED, Outcome.FAILED, Outcome.CANCELLED}


def start(record: ExecutionOutcome) -> ExecutionOutcome:
    if record.status is not Outcome.PENDING:
        raise ReconciliationError("only PENDING executions may start")
    return ExecutionOutcome(record.execution_id, Outcome.RUNNING)


def mark_unknown(record: ExecutionOutcome, reason: str) -> ExecutionOutcome:
    if record.status not in {Outcome.RUNNING, Outcome.PENDING}:
        raise ReconciliationError("only PENDING/RUNNING executions may become UNKNOWN")
    if not reason.strip():
        raise ReconciliationError("UNKNOWN requires a non-empty reason")
    return ExecutionOutcome(record.execution_id, Outcome.UNKNOWN, note=reason.strip())


def reconcile(
    record: ExecutionOutcome,
    *,
    observed_outcome: Outcome,
    evidence_ref: str,
) -> ExecutionOutcome:
    """Resolve UNKNOWN only with explicit evidence; never dispatches/retries work."""
    if record.status is not Outcome.UNKNOWN:
        raise ReconciliationError("reconciliation is allowed only from UNKNOWN")
    if observed_outcome not in {Outcome.SUCCEEDED, Outcome.FAILED}:
        raise ReconciliationError("evidence must resolve to SUCCEEDED or FAILED")
    if not evidence_ref or not evidence_ref.strip():
        raise ReconciliationError("an evidence reference is required")
    return ExecutionOutcome(
        execution_id=record.execution_id,
        status=observed_outcome,
        evidence_ref=evidence_ref.strip(),
        note=f"reconciled from UNKNOWN; prior note: {record.note or 'none'}",
    )


def may_dispatch(record: ExecutionOutcome) -> bool:
    """Dispatch is permitted only for a new PENDING record; UNKNOWN is never retried."""
    return record.status is Outcome.PENDING


def terminal(record: ExecutionOutcome) -> bool:
    return record.status in _TERMINAL
