#!/usr/bin/env python3
"""Validate explicit YAML frontmatter contract metadata in Markdown."""
import argparse, re, sys
from pathlib import Path
import yaml
def main():
 p=argparse.ArgumentParser(); p.add_argument("file"); p.add_argument("--archetype",default="sequential-verifiable-v1"); a=p.parse_args()
 text=Path(a.file).read_text(encoding="utf-8")
 if not text.startswith("---\n"): raise SystemExit("BLOCK: missing YAML frontmatter opening delimiter")
 m=re.match(r"^---\n(.*?)\n---\n",text,re.S)
 if not m: raise SystemExit("BLOCK: malformed or unclosed YAML frontmatter")
 data=yaml.safe_load(m.group(1)) or {}
 for key in ("name","description","archetype"):
  if not isinstance(data.get(key),str) or not data[key].strip(): raise SystemExit(f"BLOCK: missing frontmatter field {key}")
 if data["archetype"]!=a.archetype: raise SystemExit("BLOCK: unrecognized archetype")
 print(f"PASS: frontmatter recognized; archetype={data['archetype']}")
if __name__=="__main__": main()
