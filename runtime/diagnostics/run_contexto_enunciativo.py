"""JSON CLI adapter for the agnostic enunciative-context diagnostic."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from lateral_contexto_enunciativo import analyze


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="JSON file with a records array")
    parser.add_argument("--output", required=True, help="JSON output path")
    args = parser.parse_args()
    source = Path(args.input)
    destination = Path(args.output)
    payload = json.loads(source.read_text(encoding="utf-8"))
    records = payload.get("records")
    if not isinstance(records, list):
        raise ValueError("input must contain a records array")
    result = analyze(records)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "COMPLETED", "output": str(destination), "observations": len(result["observaciones"]),
                      "signals": len(result["senales"]), "can_decide_H": False}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
