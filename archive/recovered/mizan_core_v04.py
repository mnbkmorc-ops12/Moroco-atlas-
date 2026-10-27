#!/usr/bin/env python3
"""
MIZAN Core v0.4
Evidence-aware registry and validation gate.

Scope:
- Computes PASS / FAIL / UNKNOWN from explicit requirements and evidence.
- Evidence records require provenance metadata and a SHA-256 digest of supplied content.
- Parameter writes go through one enforcement path.
- Software self-tests are kept separate from project validation results.

This is an audit framework, NOT validation of vehicle physics or hardware.
Python 3.10+
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
import re
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional


SCHEMA_VERSION = "mizan.snapshot.v1"
ID_PATTERN = re.compile(r"^[A-Z][A-Z0-9_-]{2,63}$")
SHA256_PATTERN = re.compile(r"^[a-f0-9]{64}$")


class Status(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"


class EvidenceType(str, Enum):
    ASSUMPTION = "ASSUMPTION"
    CALCULATION = "CALCULATION"
    SIMULATION = "SIMULATION"
    MEASUREMENT = "MEASUREMENT"
    INDEPENDENT_TEST = "INDEPENDENT_TEST"


class Decision(str, Enum):
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    DEFER = "DEFER"


class ValidationError(ValueError):
    """Expected, user-correctable validation error."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False
    ).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str
    evidence_type: EvidenceType
    title: str
    source: str
    report_id: str
    created_at: str
    author: str
    reviewer: str
    content_sha256: str
    content_size_bytes: int
    independent_lab: Optional[str] = None
    scope: str = ""

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not ID_PATTERN.fullmatch(self.evidence_id):
            errors.append("evidence_id has invalid format")
        for name in ("title", "source", "report_id", "created_at", "author", "reviewer"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{name} is required")
        if not isinstance(self.evidence_type, EvidenceType):
            errors.append("evidence_type must be an EvidenceType")
        if not isinstance(self.content_sha256, str) or not SHA256_PATTERN.fullmatch(self.content_sha256):
            errors.append("content_sha256 must be a lowercase SHA-256 hex digest")
        if type(self.content_size_bytes) is not int or self.content_size_bytes < 0:
            errors.append("content_size_bytes must be a non-negative integer")
        if self.evidence_type == EvidenceType.INDEPENDENT_TEST:
            if not isinstance(self.independent_lab, str) or not self.independent_lab.strip():
                errors.append("INDEPENDENT_TEST requires independent_lab")
            if self.author.strip() == self.reviewer.strip():
                errors.append("independent test author and reviewer must differ")
        try:
            parsed = datetime.fromisoformat(self.created_at.replace("Z", "+00:00"))
            if parsed.tzinfo is None:
                errors.append("created_at must include a timezone")
        except Exception:
            errors.append("created_at must be ISO-8601 with timezone")
        return errors


@dataclass
class Parameter:
    parameter_id: str
    value: Any
    unit: str
    evidence_refs: list[str]
    required_evidence: list[EvidenceType]
    description: str = ""


@dataclass
class ProjectCheck:
    check_id: str
    status: Status
    summary: str
    evidence_refs: list[str]
    rationale: str


class MizanCore:
    def __init__(self, project_id: str, audit_path: str = "mizan_audit.jsonl"):
        if not isinstance(project_id, str) or not ID_PATTERN.fullmatch(project_id):
            raise ValidationError("project_id has invalid format")
        self.project_id = project_id
        self.audit_path = Path(audit_path)
        self.parameters: dict[str, Parameter] = {}
        self.evidence: dict[str, EvidenceRecord] = {}
        self.checks: dict[str, ProjectCheck] = {}
        self.decisions: list[dict[str, Any]] = []
        self._sequence = 0
        self._audit_head = "0" * 64
        self._append_audit("SYSTEM_INIT", {"schema_version": SCHEMA_VERSION})

    def _append_audit(self, event: str, payload: dict[str, Any], actor: str = "system",
                      reason: str = "") -> None:
        if not actor or not isinstance(actor, str):
            raise ValidationError("actor is required")
        if not isinstance(reason, str):
            raise ValidationError("reason must be text")
        self._sequence += 1
        entry = {
            "sequence": self._sequence,
            "timestamp": utc_now(),
            "project_id": self.project_id,
            "actor": actor,
            "event": event,
            "reason": reason,
            "payload": payload,
            "previous_hash": self._audit_head,
        }
        entry["entry_hash"] = sha256_bytes(canonical_json(entry))
        self.audit_path.parent.mkdir(parents=True, exist_ok=True)
        with self.audit_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, ensure_ascii=False, allow_nan=False) + "\n")
            handle.flush()
            # Best effort durability; does not guarantee storage hardware integrity.
            import os
            os.fsync(handle.fileno())
        self._audit_head = entry["entry_hash"]

    def register_evidence(self, record: EvidenceRecord, content: bytes,
                          actor: str, reason: str) -> None:
        if not isinstance(record, EvidenceRecord):
            raise ValidationError("record must be EvidenceRecord")
        if not isinstance(content, bytes):
            raise ValidationError("evidence content must be bytes")
        errors = record.validate()
        if errors:
            raise ValidationError("; ".join(errors))
        if record.evidence_id in self.evidence:
            raise ValidationError(f"duplicate evidence_id: {record.evidence_id}")
        actual_hash = sha256_bytes(content)
        if actual_hash != record.content_sha256:
            raise ValidationError("evidence content SHA-256 mismatch")
        if len(content) != record.content_size_bytes:
            raise ValidationError("evidence content size mismatch")
        self.evidence[record.evidence_id] = record
        self._append_audit(
            "EVIDENCE_REGISTERED",
            {"evidence_id": record.evidence_id, "evidence_type": record.evidence_type.value,
             "content_sha256": actual_hash, "content_size_bytes": len(content)},
            actor=actor, reason=reason
        )

    def set_parameter(self, parameter_id: str, value: Any, unit: str,
                      evidence_refs: list[str], required_evidence: list[EvidenceType],
                      actor: str, reason: str, description: str = "") -> Status:
        """Single enforcement point: invalid writes are audited and rejected."""
        errors: list[str] = []
        if not isinstance(parameter_id, str) or not ID_PATTERN.fullmatch(parameter_id):
            errors.append("parameter_id has invalid format")
        if type(value) not in (int, float) or not math.isfinite(float(value)):
            errors.append("value must be a finite int or float (bool is not accepted)")
        if not isinstance(unit, str) or not unit.strip():
            errors.append("unit is required")
        if not isinstance(evidence_refs, list) or any(not isinstance(x, str) for x in evidence_refs):
            errors.append("evidence_refs must be a list of IDs")
            evidence_refs = []
        if len(set(evidence_refs)) != len(evidence_refs):
            errors.append("duplicate evidence references")
        if not isinstance(required_evidence, list) or any(not isinstance(x, EvidenceType) for x in required_evidence):
            errors.append("required_evidence must contain EvidenceType values")
            required_evidence = []
        if not isinstance(actor, str) or not actor.strip():
            errors.append("actor is required")
        if not isinstance(reason, str) or not reason.strip():
            errors.append("reason is required")
        for ref in evidence_refs:
            if ref not in self.evidence:
                errors.append(f"unknown evidence reference: {ref}")

        if errors:
            self._append_audit(
                "PARAMETER_WRITE_REJECTED",
                {"parameter_id": str(parameter_id), "errors": errors},
                actor=actor if isinstance(actor, str) and actor.strip() else "invalid-actor",
                reason=reason if isinstance(reason, str) else ""
            )
            return Status.FAIL

        candidate = Parameter(
            parameter_id=parameter_id, value=value, unit=unit,
            evidence_refs=list(evidence_refs),
            required_evidence=list(required_evidence),
            description=description
        )
        self.parameters[parameter_id] = candidate
        self._append_audit(
            "PARAMETER_WRITE_ACCEPTED",
            {"parameter_id": parameter_id, "value": value, "unit": unit,
             "evidence_refs": list(evidence_refs),
             "required_evidence": [e.value for e in required_evidence]},
            actor=actor, reason=reason
        )
        return Status.PASS

    def _evidence_gate(self, parameter: Parameter) -> tuple[Status, list[str]]:
        errors: list[str] = []
        resolved = [self.evidence[ref] for ref in parameter.evidence_refs if ref in self.evidence]
        if len(resolved) != len(parameter.evidence_refs):
            errors.append("one or more evidence references are unresolved")
        types = {record.evidence_type for record in resolved}
        for required in parameter.required_evidence:
            matching = [r for r in resolved if r.evidence_type == required]
            if not matching:
                errors.append(f"missing required evidence type: {required.value}")
                continue
            # A registered label is not sufficient for independent validation:
            # require the explicit metadata and a distinct author/reviewer.
            if required == EvidenceType.INDEPENDENT_TEST:
                qualified = [
                    r for r in matching
                    if r.independent_lab and r.author.strip() != r.reviewer.strip()
                    and r.report_id.strip() and r.content_sha256
                ]
                if not qualified:
                    errors.append("INDEPENDENT_TEST lacks qualifying lab/report/reviewer metadata")
        if errors:
            return Status.UNKNOWN, errors
        return Status.PASS, []

    def validate_parameter(self, parameter_id: str) -> ProjectCheck:
        if parameter_id not in self.parameters:
            result = ProjectCheck(
                check_id=f"CHK-{parameter_id}", status=Status.UNKNOWN,
                summary="Parameter is not registered", evidence_refs=[],
                rationale="No registered parameter exists; no claim can be made."
            )
            self.checks[result.check_id] = result
            return result

        parameter = self.parameters[parameter_id]
        evidence_status, evidence_errors = self._evidence_gate(parameter)
        if evidence_status != Status.PASS:
            result = ProjectCheck(
                check_id=f"CHK-{parameter_id}", status=Status.UNKNOWN,
                summary="Evidence requirements are not satisfied",
                evidence_refs=list(parameter.evidence_refs),
                rationale="; ".join(evidence_errors)
            )
        else:
            result = ProjectCheck(
                check_id=f"CHK-{parameter_id}", status=Status.PASS,
                summary="Registry and declared evidence requirements passed",
                evidence_refs=list(parameter.evidence_refs),
                rationale="This checks registry/evidence metadata only; it does not validate physical correctness."
            )
        self.checks[result.check_id] = result
        self._append_audit(
            "PARAMETER_VALIDATED",
            {"parameter_id": parameter_id, "status": result.status.value,
             "rationale": result.rationale},
            actor="validator", reason="validate_parameter"
        )
        return result

    def add_check(self, check_id: str, status: Status, summary: str,
                  evidence_refs: list[str], rationale: str,
                  actor: str, reason: str) -> Status:
        errors = []
        if not ID_PATTERN.fullmatch(check_id) if isinstance(check_id, str) else True:
            errors.append("check_id has invalid format")
        if not isinstance(status, Status):
            errors.append("status must be Status enum")
        if not isinstance(summary, str) or not summary.strip():
            errors.append("summary is required")
        if not isinstance(evidence_refs, list):
            errors.append("evidence_refs must be a list")
            evidence_refs = []
        for ref in evidence_refs:
            if ref not in self.evidence:
                errors.append(f"unknown evidence reference: {ref}")
        if check_id in self.checks:
            errors.append(f"duplicate check_id: {check_id}")
        if errors:
            self._append_audit("CHECK_REJECTED", {"check_id": str(check_id), "errors": errors},
                               actor=actor or "invalid-actor", reason=reason or "")
            return Status.FAIL
        check = ProjectCheck(check_id, status, summary, list(evidence_refs), rationale)
        self.checks[check_id] = check
        self._append_audit("CHECK_REGISTERED", {"check_id": check_id, "status": status.value},
                           actor=actor, reason=reason)
        return Status.PASS

    def overall_status(self) -> Status:
        """FAIL dominates; otherwise UNKNOWN until at least one check exists and all pass."""
        if not self.checks:
            return Status.UNKNOWN
        statuses = [check.status for check in self.checks.values()]
        if Status.FAIL in statuses:
            return Status.FAIL
        if Status.UNKNOWN in statuses:
            return Status.UNKNOWN
        return Status.PASS

    def report(self) -> dict[str, Any]:
        status = self.overall_status()
        return {
            "schema_version": SCHEMA_VERSION,
            "project_id": self.project_id,
            "overall_status": status.value,
            "claim_scope": "registry and evidence metadata only; not physical vehicle validation",
            "counts": {
                "parameters": len(self.parameters),
                "evidence_records": len(self.evidence),
                "project_checks": len(self.checks),
                "pass": sum(c.status == Status.PASS for c in self.checks.values()),
                "fail": sum(c.status == Status.FAIL for c in self.checks.values()),
                "unknown": sum(c.status == Status.UNKNOWN for c in self.checks.values()),
            },
            "parameters": {
                key: {
                    "value": p.value, "unit": p.unit,
                    "evidence_refs": list(p.evidence_refs),
                    "required_evidence": [e.value for e in p.required_evidence],
                    "description": p.description,
                } for key, p in self.parameters.items()
            },
            "checks": {
                key: {
                    "status": c.status.value, "summary": c.summary,
                    "evidence_refs": list(c.evidence_refs), "rationale": c.rationale,
                } for key, c in self.checks.items()
            },
            "audit_head_hash": self._audit_head,
            "generated_at": utc_now(),
        }

    def create_snapshot(self) -> dict[str, Any]:
        """Detached snapshot: callers cannot mutate live state through returned references."""
        return copy.deepcopy({
            "schema_version": SCHEMA_VERSION,
            "project_id": self.project_id,
            "parameters": self.report()["parameters"],
            "evidence": {
                key: {**asdict(record), "evidence_type": record.evidence_type.value}
                for key, record in self.evidence.items()
            },
            "checks": self.report()["checks"],
            "decisions": self.decisions,
            "audit_head_hash": self._audit_head,
            "audit_sequence": self._sequence,
            "generated_at": utc_now(),
        })

    def export_snapshot(self, path: str) -> str:
        snapshot = self.create_snapshot()
        payload = canonical_json(snapshot)
        Path(path).write_bytes(payload)
        return sha256_bytes(payload)


def run_self_tests() -> list[dict[str, Any]]:
    """Tests are isolated from project checks and never affect project PASS counts."""
    results: list[dict[str, Any]] = []

    def check(name: str, fn) -> None:
        try:
            fn()
            results.append({"test": name, "status": "PASS"})
        except Exception as exc:
            results.append({"test": name, "status": "FAIL", "error": str(exc)})

    def test_unknown_empty():
        core = MizanCore("TEST-PROJECT", audit_path="/tmp/mizan_test_empty.jsonl")
        assert core.overall_status() == Status.UNKNOWN

    def test_bad_value_rejected():
        core = MizanCore("TEST-PROJECT", audit_path="/tmp/mizan_test_bad.jsonl")
        status = core.set_parameter("SUS-SPRING", "abc", "N/m", [], [],
                                    "test-runner", "negative test")
        assert status == Status.FAIL
        assert "SUS-SPRING" not in core.parameters

    def test_nan_rejected():
        core = MizanCore("TEST-PROJECT", audit_path="/tmp/mizan_test_nan.jsonl")
        status = core.set_parameter("SUS-SPRING", float("nan"), "N/m", [], [],
                                    "test-runner", "negative test")
        assert status == Status.FAIL

    def test_required_evidence_unknown():
        core = MizanCore("TEST-PROJECT", audit_path="/tmp/mizan_test_gate.jsonl")
        assert core.set_parameter("SUS-SPRING", 30000.0, "N/m", [], [EvidenceType.INDEPENDENT_TEST],
                                  "test-runner", "register placeholder") == Status.PASS
        assert core.validate_parameter("SUS-SPRING").status == Status.UNKNOWN

    def test_snapshot_detached():
        core = MizanCore("TEST-PROJECT", audit_path="/tmp/mizan_test_snap.jsonl")
        core.decisions.append({"decision": Decision.DEFER.value})
        snap = core.create_snapshot()
        snap["decisions"].append({"decision": "CORRUPTED"})
        assert len(core.decisions) == 1

    check("empty_registry_is_unknown", test_unknown_empty)
    check("non_numeric_value_rejected", test_bad_value_rejected)
    check("nan_value_rejected", test_nan_rejected)
    check("missing_independent_evidence_is_unknown", test_required_evidence_unknown)
    check("snapshot_is_detached", test_snapshot_detached)
    return results


def main() -> int:
    output_path = Path("behemoth_mizan_v04_snapshot.json")
    audit_path = Path("behemoth_mizan_v04_audit.jsonl")
    core = MizanCore("BEHEMOTH-ATLAS-ZENITH", str(audit_path))

    # Example placeholder only. No measurement or engineering validation is claimed.
    write_status = core.set_parameter(
        parameter_id="SUS-SPRING",
        value=30000.0,
        unit="N/m",
        evidence_refs=[],
        required_evidence=[EvidenceType.MEASUREMENT, EvidenceType.INDEPENDENT_TEST],
        actor="project-config",
        reason="placeholder retained for schema demonstration; not a vehicle specification",
        description="UNVERIFIED placeholder. Replace only with traceable engineering data."
    )
    check = core.validate_parameter("SUS-SPRING")
    digest = core.export_snapshot(str(output_path))
    tests = run_self_tests()
    test_failures = sum(t["status"] != "PASS" for t in tests)

    print(json.dumps({
        "write_status": write_status.value,
        "project_status": core.overall_status().value,
        "parameter_check": {
            "status": check.status.value,
            "rationale": check.rationale
        },
        "snapshot": str(output_path),
        "snapshot_sha256": digest,
        "audit_jsonl": str(audit_path),
        "self_tests": tests,
        "self_test_failures": test_failures,
        "scope_warning": "This run validates registry/evidence metadata only, not vehicle physics."
    }, indent=2, ensure_ascii=False))

    # Strict CI gate: fail on software test failures OR any project status other than PASS.
    # The default placeholder intentionally yields UNKNOWN, so this demo exits non-zero.
    return 1 if test_failures or core.overall_status() != Status.PASS else 0


if __name__ == "__main__":
    raise SystemExit(main())