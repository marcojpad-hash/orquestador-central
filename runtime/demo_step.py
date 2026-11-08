#!/usr/bin/env python3
"""Deterministic demo adapter used to exercise the runner end-to-end."""
import argparse, json
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument("--input",required=True); p.add_argument("--output",required=True)
a=p.parse_args()
data=json.loads(Path(a.input).read_text(encoding="utf-8"))
Path(a.output).parent.mkdir(parents=True,exist_ok=True)
Path(a.output).write_text("SEQUENTIAL-VERIFIABLE demo PASS\n"+json.dumps({"id":data["id"],"project":data["project"]},ensure_ascii=False)+"\n",encoding="utf-8")
print("demo output written")
