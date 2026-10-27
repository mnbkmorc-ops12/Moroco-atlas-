"""MIZAN CORE governance state machine.

Pure, deterministic policy primitives. This module does not execute external actions.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any


class Decision(str, Enum):
    AUTHORIZED = "AUTHORIZED"
    DENIED = "DENIED"
    UNRESOLVED = "UNRESOLVED"


class ExecutionStatus(str, Enum):
    PENDING = "PENDING"
    CLAIMED = "CLAIMED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"
    CANCELLED = "CANCELLED"


TERMINAL = {ExecutionStatus.SUCCEEDED, ExecutionStatus.FAILED, ExecutionStatus.UNKNOWN, ExecutionStatus.CANCELLED}
ALLOWED = {
    ExecutionStatus.PENDING: {ExecutionStatus.CLAIMED, ExecutionStatus.CANCELLED},
    ExecutionStatus.CLAIMED: {ExecutionStatus.RUNNING, ExecutionStatus.PENDING, ExecutionStatus.UNKNOWN, ExecutionStatus.CANCELLED},
    ExecutionStatus.RUNNING: {ExecutionStatus.SUCCEEDED, ExecutionStatus.FAILED, ExecutionStatus.UNKNOWN},
    ExecutionStatus.UNKNOWN: set(),  # reconcile explicitly; never retry automatically
    ExecutionStatus.SUCCEEDED: set(),
    ExecutionStatus.FAILED: set(),
    ExecutionStatus.CANCELLED: set(),
}


class GovernanceError(ValueError):
    pass


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    source: str
    digest_sha256: str
    independently_verified: bool = False

    def valid(self) -> bool:
        return bool(self.evidence_id.strip() and self.source.strip() and
                    len(self.digest_sha256) == 64 and
                    all(c in "0123456789abcdef" for c in self.digest_sha256.lower()))


@dataclass(frozen=True)
class DecisionRecord:
    intent_id: str
    decision: Decision
    rule_id: str
    evidence: tuple[Evidence, ...]
    rationale: str


def evaluate_request(*, intent_id: str, rule_id: str, rationale: str,
                     required_evidence: tuple[str, ...],
                     evidence: tuple[Evidence, ...],
                     explicit_rule_match: bool) -> DecisionRecord:
    """Authorize only when the rule match and required independently verified evidence exist."""
    if not intent_id.strip() or not rule_id.strip() or not rationale.strip():
        raise GovernanceError("intent_id, rule_id and rationale are required")
    by_id = {item.evidence_id: item for item in evidence if item.valid()}
    required_present = all(
        key in by_id and by_id[key].independently_verified
        for key in required_evidence
    )
    if not explicit_rule_match:
        decision = Decision.DENIED
    elif not required_present:
        decision = Decision.UNRESOLVED
    else:
        decision = Decision.AUTHORIZED
    return DecisionRecord(intent_id, decision, rule_id, evidence, rationale)


def transition(current: ExecutionStatus, target: ExecutionStatus,
               *, reconciliation_recorded: bool = False) -> ExecutionStatus:
    if current == ExecutionStatus.UNKNOWN:
        if not reconciliation_recorded:
            raise GovernanceError("UNKNOWN requires explicit reconciliation before any new action")
        raise GovernanceError("Reconciliation must create a new intent; terminal UNKNOWN cannot be reopened")
    if target not in ALLOWED[current]:
        raise GovernanceError(f"illegal execution transition: {current.value} -> {target.value}")
    if target == ExecutionStatus.PENDING and current == ExecutionStatus.CLAIMED:
        # Releasing a claim is only safe before the external action starts.
        return target
    return target


def decision_to_dict(record: DecisionRecord) -> dict[str, Any]:
    return {
        "intent_id": record.intent_id,
        "decision": record.decision.value,
        "rule_id": record.rule_id,
        "rationale": record.rationale,
        "evidence": [
            {"evidence_id": e.evidence_id, "source": e.source,
             "digest_sha256": e.digest_sha256,
             "independently_verified": e.independently_verified}
            for e in record.evidence
        ],
    }
