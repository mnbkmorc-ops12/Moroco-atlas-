"""Software regression tests for recovered MIZAN Core v0.4.

These tests cover metadata/evidence behavior only. They do not validate vehicle
physics, PostgreSQL concurrency, deployment security, or production behavior.
"""
import importlib.util
import tempfile
import unittest
from pathlib import Path

SOURCE = Path(__file__).parents[1] / "archive" / "recovered" / "mizan_core_v04.py"
SPEC = importlib.util.spec_from_file_location("mizan_core_v04", SOURCE)
mizan = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mizan)


class MizanCoreV04Tests(unittest.TestCase):
    def make_core(self):
        tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(tempdir.cleanup)
        return mizan.MizanCore("TEST-PROJECT", str(Path(tempdir.name) / "audit.jsonl"))

    def test_empty_registry_is_unknown(self):
        self.assertEqual(self.make_core().overall_status(), mizan.Status.UNKNOWN)

    def test_non_numeric_parameter_is_rejected(self):
        core = self.make_core()
        result = core.set_parameter("SUS-SPRING", "abc", "N/m", [], [],
                                    "test-runner", "negative regression test")
        self.assertEqual(result, mizan.Status.FAIL)
        self.assertNotIn("SUS-SPRING", core.parameters)

    def test_nan_parameter_is_rejected(self):
        result = self.make_core().set_parameter("SUS-SPRING", float("nan"), "N/m", [], [],
                                                "test-runner", "negative regression test")
        self.assertEqual(result, mizan.Status.FAIL)

    def test_missing_required_evidence_remains_unknown(self):
        core = self.make_core()
        result = core.set_parameter("SUS-SPRING", 30000.0, "N/m", [],
                                    [mizan.EvidenceType.INDEPENDENT_TEST],
                                    "test-runner", "register placeholder")
        self.assertEqual(result, mizan.Status.PASS)
        self.assertEqual(core.validate_parameter("SUS-SPRING").status, mizan.Status.UNKNOWN)

    def test_snapshot_is_detached(self):
        core = self.make_core()
        core.decisions.append({"decision": mizan.Decision.DEFER.value})
        snapshot = core.create_snapshot()
        snapshot["decisions"].append({"decision": "CORRUPTED"})
        self.assertEqual(len(core.decisions), 1)


if __name__ == "__main__":
    unittest.main()
