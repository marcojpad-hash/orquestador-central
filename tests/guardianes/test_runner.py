import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("run_acceptance.py")
SPEC = importlib.util.spec_from_file_location("guardian_acceptance_runner", SCRIPT)
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


class AcceptanceRunnerTests(unittest.TestCase):
    def setUp(self):
        self.case = {
            "id": "T-01", "guardian": "sample", "input": "x",
            "must": ["criterion A"], "must_not": ["bad behavior"]
        }

    def test_missing_adapter_is_blocked_not_pass(self):
        result = runner.run_case(self.case, {})
        self.assertEqual(result["status"], "BLOCKED_NO_ADAPTER")
        self.assertFalse(result["passed"])

    def test_complete_adapter_contract_passes(self):
        def adapter(_case):
            return {"status": "EXECUTED", "satisfied": ["criterion A"],
                    "violations": [], "marks": [{"code": "FLAG", "trace": "input[0:1]"}],
                    "can_decide_H": False}
        result = runner.run_case(self.case, {"sample": adapter})
        self.assertEqual(result["status"], "PASS")

    def test_missing_criterion_fails(self):
        def adapter(_case):
            return {"status": "EXECUTED", "satisfied": [], "violations": [],
                    "marks": [], "can_decide_H": False}
        result = runner.run_case(self.case, {"sample": adapter})
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("criterion A", result["missing_criteria"])

    def test_mark_without_trace_fails(self):
        def adapter(_case):
            return {"status": "EXECUTED", "satisfied": ["criterion A"],
                    "violations": [], "marks": [{"code": "FLAG"}],
                    "can_decide_H": False}
        result = runner.run_case(self.case, {"sample": adapter})
        self.assertEqual(result["status"], "FAIL")

    def test_adapter_cannot_decide_h(self):
        def adapter(_case):
            return {"status": "EXECUTED", "satisfied": ["criterion A"],
                    "violations": [], "marks": [], "can_decide_H": True}
        result = runner.run_case(self.case, {"sample": adapter})
        self.assertEqual(result["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
