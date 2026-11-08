#!/usr/bin/env python3
"""Mechanical output verifier."""
import argparse
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument("--path",required=True); p.add_argument("--min-bytes",type=int,default=1)
a=p.parse_args(); f=Path(a.path)
assert f.is_file(), f"missing file: {f}"
assert f.stat().st_size>=a.min_bytes, f"file too short: {f.stat().st_size}"
assert "SEQUENTIAL-VERIFIABLE demo PASS" in f.read_text(encoding="utf-8"), "missing success marker"
print(f"verified {f} ({f.stat().st_size} bytes)")
