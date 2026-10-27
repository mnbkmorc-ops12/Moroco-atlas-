"""
BEHEMOTH — Atlas Zenith
MIZAN Core v0.1
Engineering registry, evidence tracking, validation checks, decision log,
and a simple quarter-car suspension simulation.

Python: 3.10+
Standard library only.

IMPORTANT:
- This is an engineering-software scaffold, not a validated vehicle model.
- Default parameters are illustrative and must not be treated as vehicle specifications.
- PASS means only that a defined software check passed, not that a vehicle is safe.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any
import csv
import json
import math


PROJECT_NAME = "BEHEMOTH — Atlas Zenith"
CORE_VERSION = "0.1"


class Status(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"


class EvidenceType(str, Enum):
    ASSUMPTION = "ASSUMPTION"
    CALCULATION = "CALCULATION"
    SIMULATION = "SIMULATION"
    MEASUREMENT = "MEASUREMENT"
    DOCUMENT = "DOCUMENT"


@dataclass
class Parameter:
    name: str
    value: float
    unit: str
    evidence_type: EvidenceType
    source: str
    note: str = ""

    def validate(self) -> list[str]:
        errors = []
        if not self.name.strip():
            errors.append("Parameter name is empty.")
        if not math.isfinite(self.value):
            errors.append(f"{self.name}: value must be finite.")
        if not self.unit.strip():
            errors.append(f"{self.name}: unit is missing.")
        if not self.source.strip():
            errors.append(f"{self.name}: evidence source is missing.")
        return errors


@dataclass
class Subsystem:
    component_id: str
    name: str
    version: str
    description: str
    parameters: list[Parameter]
    status: Status = Status.UNKNOWN

    def validate(self) -> list[str]:
        errors = []
        if not self.component_id.startswith("MZN-"):
            errors.append(f"{self.component_id}: ID must start with MZN-.")
        if not self.name.strip():
            errors.append(f"{self.component_id}: name is missing.")
        if not self.version.strip():
            errors.append(f"{self.component_id}: version is missing.")
        for parameter in self.parameters:
            errors.extend(parameter.validate())
        return errors


@dataclass
class CheckResult:
    check_id: str
    description: str
    status: Status
    details: str
    timestamp_utc: str


class MizanCore:
    def __init__(self, project_name: str = PROJECT_NAME):
        self.project_name = project_name
        self.version = CORE_VERSION
        self.subsystems: dict[str, Subsystem] = {}
        self.checks: list[CheckResult] = []
        self.decisions: list[dict[str, Any]] = []

    @staticmethod
    def timestamp() -> str:
        return datetime.now(timezone.utc).isoformat()

    def register(self, subsystem: Subsystem) -> None:
        if subsystem.component_id in self.subsystems:
            raise ValueError(f"Duplicate component ID: {subsystem.component_id}")
        self.subsystems[subsystem.component_id] = subsystem

    def run_registry_checks(self) -> list[CheckResult]:
        results = []
        for component_id, subsystem in self.subsystems.items():
            errors = subsystem.validate()
            status = Status.FAIL if errors else Status.PASS
            details = "; ".join(errors) if errors else (
                "Registry structure and parameter metadata checks passed. "
                "This does not validate the physical design."
            )
            results.append(CheckResult(
                check_id=f"REG-{component_id}",
                description=f"Registry validation for {subsystem.name}",
                status=status,
                details=details,
                timestamp_utc=self.timestamp(),
            ))
        self.checks.extend(results)
        return results

    def record_check(
        self, check_id: str, description: str, status: Status, details: str
    ) -> CheckResult:
        result = CheckResult(
            check_id=check_id,
            description=description,
            status=status,
            details=details,
            timestamp_utc=self.timestamp(),
        )
        self.checks.append(result)
        return result

    def record_decision(
        self, title: str, decision: str, rationale: str,
        evidence_refs: list[str] | None = None
    ) -> None:
        self.decisions.append({
            "timestamp_utc": self.timestamp(),
            "title": title,
            "decision": decision,
            "rationale": rationale,
            "evidence_refs": evidence_refs or [],
        })

    def export_json(self, filename: str = "mizan_project.json") -> None:
        payload = {
            "project_name": self.project_name,
            "core_version": self.version,
            "exported_at_utc": self.timestamp(),
            "disclaimer": (
                "Registry and simulation scaffold only; not a vehicle safety "
                "certification or proof of physical performance."
            ),
            "subsystems": {
                key: {
                    **asdict(value),
                    "status": value.status.value,
                    "parameters": [
                        {
                            **asdict(p),
                            "evidence_type": p.evidence_type.value,
                        }
                        for p in value.parameters
                    ],
                }
                for key, value in self.subsystems.items()
            },
            "checks": [
                {**asdict(c), "status": c.status.value}
                for c in self.checks
            ],
            "decisions": self.decisions,
        }
        Path(filename).write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def export_checks_csv(self, filename: str = "mizan_checks.csv") -> None:
        fields = [
            "check_id", "description", "status", "details", "timestamp_utc"
        ]
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            for check in self.checks:
                row = asdict(check)
                row["status"] = check.status.value
                writer.writerow(row)

    def print_summary(self) -> None:
        print(f"\n{self.project_name} | MIZAN Core v{self.version}")
        print(f"Subsystems registered: {len(self.subsystems)}")
        print(f"Checks recorded: {len(self.checks)}")
        for status in Status:
            count = sum(c.status == status for c in self.checks)
            print(f"{status.value}: {count}")
        print("Reminder: software PASS is not physical vehicle validation.")


# ---------------------------------------------------------------------
# Quarter-car simulation: simple linear vertical dynamics model
# ---------------------------------------------------------------------

@dataclass
class QuarterCarConfig:
    sprung_mass_kg: float = 350.0
    unsprung_mass_kg: float = 45.0
    spring_stiffness_N_m: float = 30000.0
    damper_coefficient_N_s_m: float = 2500.0
    tire_stiffness_N_m: float = 220000.0
    duration_s: float = 5.0
    dt_s: float = 0.001
    bump_start_s: float = 1.0
    bump_duration_s: float = 0.20
    bump_height_m: float = 0.04


def validate_quarter_car(cfg: QuarterCarConfig) -> None:
    for name in (
        "sprung_mass_kg", "unsprung_mass_kg", "spring_stiffness_N_m",
        "damper_coefficient_N_s_m", "tire_stiffness_N_m",
        "duration_s", "dt_s", "bump_duration_s"
    ):
        value = getattr(cfg, name)
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f"{name} must be finite and > 0.")
    if cfg.bump_start_s < 0 or cfg.bump_height_m < 0:
        raise ValueError("Bump start and height cannot be negative.")


def road_height(t: float, cfg: QuarterCarConfig) -> float:
    if cfg.bump_start_s <= t <= cfg.bump_start_s + cfg.bump_duration_s:
        phase = math.pi * (t - cfg.bump_start_s) / cfg.bump_duration_s
        return cfg.bump_height_m * math.sin(phase)
    return 0.0


def state_derivative(t: float, y: tuple[float, float, float, float],
                     cfg: QuarterCarConfig) -> tuple[float, float, float, float]:
    body_z, body_v, wheel_z, wheel_v = y
    road_z = road_height(t, cfg)

    spring_force = -cfg.spring_stiffness_N_m * (body_z - wheel_z)
    damper_force = -cfg.damper_coefficient_N_s_m * (body_v - wheel_v)
    tire_force = -cfg.tire_stiffness_N_m * (wheel_z - road_z)

    body_a = (spring_force + damper_force) / cfg.sprung_mass_kg
    wheel_a = (-spring_force - damper_force + tire_force) / cfg.unsprung_mass_kg
    return body_v, body_a, wheel_v, wheel_a


def rk4_step(t: float, y: tuple[float, float, float, float],
             dt: float, cfg: QuarterCarConfig) -> tuple[float, float, float, float]:
    def add(a, b, scale):
        return tuple(x + scale * z for x, z in zip(a, b))

    k1 = state_derivative(t, y, cfg)
    k2 = state_derivative(t + dt / 2, add(y, k1, dt / 2), cfg)
    k3 = state_derivative(t + dt / 2, add(y, k2, dt / 2), cfg)
    k4 = state_derivative(t + dt, add(y, k3, dt), cfg)

    return tuple(
        yi + dt * (a + 2*b + 2*c + d) / 6
        for yi, a, b, c, d in zip(y, k1, k2, k3, k4)
    )


def simulate_quarter_car(
    cfg: QuarterCarConfig,
    filename: str = "behemoth_suspension.csv"
) -> dict[str, float | int | str]:
    validate_quarter_car(cfg)
    state = (0.0, 0.0, 0.0, 0.0)
    rows = []
    t = 0.0
    steps = math.ceil(cfg.duration_s / cfg.dt_s)

    for _ in range(steps + 1):
        body_z, body_v, wheel_z, wheel_v = state
        road_z = road_height(t, cfg)
        body_a = state_derivative(t, state, cfg)[1]

        rows.append({
            "time_s": t,
            "road_height_m": road_z,
            "body_displacement_m": body_z,
            "body_velocity_m_s": body_v,
            "body_acceleration_m_s2": body_a,
            "wheel_displacement_m": wheel_z,
            "wheel_velocity_m_s": wheel_v,
            "suspension_travel_m": body_z - wheel_z,
            "tire_deflection_m": wheel_z - road_z,
        })

        if t >= cfg.duration_s:
            break
        step = min(cfg.dt_s, cfg.duration_s - t)
        state = rk4_step(t, state, step, cfg)
        t += step

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    return {
        "model": "linear quarter-car simulation",
        "result_class": "SIMULATION_NOT_MEASUREMENT",
        "samples": len(rows),
        "peak_abs_body_acceleration_m_s2": max(
            abs(r["body_acceleration_m_s2"]) for r in rows
        ),
        "peak_abs_suspension_travel_m": max(
            abs(r["suspension_travel_m"]) for r in rows
        ),
        "peak_abs_tire_deflection_m": max(
            abs(r["tire_deflection_m"]) for r in rows
        ),
        "csv_file": filename,
    }


def build_default_project() -> MizanCore:
    core = MizanCore()

    illustrative = EvidenceType.ASSUMPTION
    core.register(Subsystem(
        "MZN-CHS-001", "Chassis", "0.1",
        "Chassis requirements registry; geometry not yet defined.",
        [Parameter("vehicle_mass", 0.0, "kg", illustrative,
                   "UNDEFINED", "Placeholder only; not a vehicle mass.")],
    ))
    core.register(Subsystem(
        "MZN-SUS-001", "Suspension", "0.1",
        "Quarter-car simulation scaffold; not a double-wishbone CAD model.",
        [
            Parameter("sprung_mass_per_corner", 350.0, "kg", illustrative,
                      "ILLUSTRATIVE_DEFAULT", "Must be replaced with measured/design data."),
            Parameter("spring_stiffness", 30000.0, "N/m", illustrative,
                      "ILLUSTRATIVE_DEFAULT", "Linear model parameter."),
            Parameter("damper_coefficient", 2500.0, "N*s/m", illustrative,
                      "ILLUSTRATIVE_DEFAULT", "Constant damping approximation."),
        ],
    ))
    core.register(Subsystem(
        "MZN-PWR-001", "Energy & Powertrain", "0.1",
        "Architecture undecided; no performance claims recorded.",
        [Parameter("architecture_selected", 0.0, "boolean_encoded_as_0_or_1",
                   illustrative, "UNDECIDED", "0 means not selected.")],
    ))
    core.register(Subsystem(
        "MZN-THM-001", "Thermal Management", "0.1",
        "Thermal architecture and heat loads not yet established.",
        [Parameter("thermal_load", 0.0, "W", illustrative,
                   "UNDEFINED", "Placeholder; no thermal calculation yet.")],
    ))
    core.register(Subsystem(
        "MZN-AER-001", "Aerodynamics", "0.1",
        "Aerodynamic coefficients not yet measured or simulated.",
        [Parameter("drag_coefficient", 0.0, "dimensionless", illustrative,
                   "UNDEFINED", "Zero is a placeholder, not a physical estimate.")],
    ))
    core.register(Subsystem(
        "MZN-VAL-001", "Validation Engine", "0.1",
        "Tracks evidence and software checks; does not certify physical safety.",
        [Parameter("physical_validation_complete", 0.0, "boolean_encoded_as_0_or_1",
                   illustrative, "NOT_TESTED", "0 means no physical validation recorded.")],
    ))
    return core


def main() -> None:
    core = build_default_project()

    print("Running MIZAN registry checks...")
    for result in core.run_registry_checks():
        print(f"{result.status.value:7} {result.check_id}: {result.details}")

    print("\nRunning illustrative suspension simulation...")
    simulation = simulate_quarter_car(QuarterCarConfig())
    core.record_check(
        "SIM-SUS-001",
        "Quarter-car numerical simulation completed",
        Status.UNKNOWN,
        (
            "The software run completed, but physical validity is UNKNOWN until "
            "model assumptions and outputs are compared against measured data. "
            f"Summary: {simulation}"
        ),
    )

    core.record_decision(
        "Powertrain architecture",
        "DEFER",
        "Compare electric and hybrid architectures after requirements and constraints are defined.",
        ["MZN-PWR-001"],
    )

    core.export_json()
    core.export_checks_csv()
    core.print_summary()
    print("\nFiles created: mizan_project.json, mizan_checks.csv, behemoth_suspension.csv")
    print("All physical performance and safety claims remain UNVALIDATED.")


if __name__ == "__main__":
    main()