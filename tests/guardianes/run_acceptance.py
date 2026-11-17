#!/usr/bin/env python3
"""Run the independent guardian acceptance fixtures against registered adapters.

Adapter contract:
  module:function receives one case dict and returns a dict:
    {
      "status": "EXECUTED",
      "satisfied": ["exact criterion text from case.must", ...],
      "violations": ["exact criterion text from case.must_not", ...],
      "marks": [{"code": "...", "trace": "..."}],
      "can_decide_H": false
    }

No built-in fake guardian is provided. Missing adapters are BLOCKED, never PASS.
"""
from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FIXTURES = ROOT / "tests/guardianes/acceptance_cases.json"
DEFAULT_REGISTRY = ROOT / "tests/guardianes/adapters.json"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_adapter(spec: str):
    if ":" not in spec:
        raise ValueError(f"adapter must be module:function, got {spec!r}")
    module_name, function_name = spec.split(":", 1)
    if not module_name or not function_name:
        raise ValueError(f"invalid adapter spec: {spec!r}")
    module = importlib.import_module(module_name)
    adapter = getattr(module, function_name)
    if not callable(adapter):
        raise TypeError(f"adapter is not callable: {spec}")
    return adapter


def validate_suite(suite: dict) -> list[dict]:
    if suite.get("suite_id") != "GUARDIANES_ACCEPTANCE_V1":
        raise ValueError("unknown suite_id")
    cases = suite.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("suite must contain a non-empty cases array")
    ids = [case.get("id") for case in cases]
    if len(ids) != len(set(ids)) or any(not item for item in ids):
        raise ValueError("case IDs must be present and unique")
    for case in cases:
        for field in ("guardian", "input", "must", "must_not"):
            if field not in case:
                raise ValueError(f"{case.get('id')}: missing {field}")
        if not isinstance(case["must"], list) or not isinstance(case["must_not"], list):
            raise ValueError(f"{case['id']}: must/must_not must be arrays")
    return cases


def run_case(case: dict, adapters: dict[str, Any]) -> dict:
    guardian = case["guardian"]
    adapter = adapters.get(guardian)
    if adapter is None:
        return {"id": case["id"], "guardian": guardian, "status": "BLOCKED_NO_ADAPTER",
                "passed": False, "missing_adapter": True}
    try:
        result = adapter(case)
    except Exception as exc:  # adapter failure must never be interpreted as a clean result
        return {"id": case["id"], "guardian": guardian, "status": "ERROR",
                "passed": False, "error": f"{type(exc).__name__}: {exc}"}
    if not isinstance(result, dict):
        return {"id": case["id"], "guardian": guardian, "status": "ERROR",
                "passed": False, "error": "adapter result must be a JSON-like object"}
    required = set(case["must"])
    forbidden = set(case["must_not"])
    satisfied = set(result.get("satisfied", []))
    violations = set(result.get("violations", []))
    missing = sorted(required - satisfied)
    prohibited = sorted(forbidden & violations)
    marks = result.get("marks", [])
    marks_without_trace = [m for m in marks if not isinstance(m, dict) or not m.get("trace")]
    if result.get("status") != "EXECUTED":
        state_error = f"adapter status must be EXECUTED, got {result.get('status')!r}"
    else:
        state_error = None
    if result.get("can_decide_H") is not False:
        state_error = state_error or "can_decide_H must be false"
    errors = []
    if state_error:
        errors.append(state_error)
    if missing:
        errors.append("required criteria not satisfied")
    if prohibited:
        errors.append("prohibited behavior reported")
    if marks_without_trace:
        errors.append("one or more marks lack trace")
    passed = not errors
    return {"id": case["id"], "guardian": guardian,
            "status": "PASS" if passed else "FAIL", "passed": passed,
            "missing_criteria": missing, "prohibited_behaviors": prohibited,
            "errors": errors, "marks": marks}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, default=DEFAULT_FIXTURES)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--json-out", type=Path, help="write complete machine-readable report")
    args = parser.parse_args(argv)

    try:
        suite = load_json(args.fixtures)
        cases = validate_suite(suite)
        registry = load_json(args.registry) if args.registry.exists() else {}
        if not isinstance(registry, dict):
            raise ValueError("adapter registry must be a JSON object")
        adapters = {}
        adapter_errors = {}
        for guardian, spec in registry.items():
            try:
                adapters[guardian] = load_adapter(spec)
            except Exception as exc:
                adapter_errors[guardian] = f"{type(exc).__name__}: {exc}"
        results = [run_case(case, adapters) for case in cases]
        for item in results:
            if item["guardian"] in adapter_errors and item["status"] == "BLOCKED_NO_ADAPTER":
                item["status"] = "ERROR"
                item["error"] = adapter_errors[item["guardian"]]
        passed = sum(item["status"] == "PASS" for item in results)
        blocked = sum(item["status"] == "BLOCKED_NO_ADAPTER" for item in results)
        failed = len(results) - passed - blocked
        report = {"suite_id": suite["suite_id"], "case_count": len(results),
                  "passed": passed, "failed": failed, "blocked": blocked,
                  "overall": "PASS" if passed == len(results) else
                             ("BLOCKED" if passed == 0 and failed == 0 else "FAIL"),
                  "results": results}
        rendered = json.dumps(report, ensure_ascii=False, indent=2)
        print(rendered)
        if args.json_out:
            args.json_out.parent.mkdir(parents=True, exist_ok=True)
            args.json_out.write_text(rendered + "\n", encoding="utf-8")
        if report["overall"] == "PASS":
            return 0
        return 2 if report["overall"] == "BLOCKED" else 1
    except Exception as exc:
        print(json.dumps({"overall": "ERROR", "error": f"{type(exc).__name__}: {exc}"},
                         ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
