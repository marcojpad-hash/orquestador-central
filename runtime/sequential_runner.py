#!/usr/bin/env python3
"""Contract-aware sequential runner. Executes only repository-local Python adapters."""
from __future__ import annotations
import argparse, datetime as dt, json, os, shlex, subprocess, sys, time
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]; RUNS=ROOT/"runtime"/"runs"
SCHEMA_URI="https://github.com/marcojpad-hash/orquestador-central/blob/main/schemas/sequential-verifiable-v1.schema.json"
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def emit(log,event,**data):
 row={"ts":now(),"event":event,**data}; log.parent.mkdir(parents=True,exist_ok=True)
 with log.open("a",encoding="utf-8") as f:f.write(json.dumps(row,ensure_ascii=False)+"\n")
 print(json.dumps(row,ensure_ascii=False))
def safe_path(value):
 p=(ROOT/value).resolve()
 if p!=ROOT and ROOT not in p.parents: raise ValueError(f"path escapes workspace: {value}")
 return p
def validate(x):
 import jsonschema
 if x.get("$schema")!=SCHEMA_URI: raise ValueError("unrecognized or missing $schema contract marker")
 schema=json.loads((ROOT/"schemas/sequential-verifiable-v1.schema.json").read_text(encoding="utf-8"))
 jsonschema.Draft202012Validator.check_schema(schema)
 errors=sorted(jsonschema.Draft202012Validator(schema).iter_errors(x),key=lambda e:list(map(str,e.path)))
 if errors: raise ValueError("JSON Schema violation: "+"; ".join(f"{list(e.path)}: {e.message}" for e in errors))
 if x.get("_contract")!="SEQUENTIAL-VERIFIABLE-v1": raise ValueError("wrong _contract")
def check(c):
 p=safe_path(c["path"])
 if c["kind"]=="exists": return p.exists()
 if c["kind"]=="min_bytes": return p.is_file() and p.stat().st_size>=int(c["value"])
 if c["kind"]=="contains": return p.is_file() and str(c["value"]) in p.read_text(encoding="utf-8")
 raise ValueError("unsupported condition kind: "+c["kind"])
def command(value):
 forbidden=[";","&&","||","|",">","<","$(","\x60"]
 if any(t in value for t in forbidden): raise ValueError("shell syntax forbidden")
 argv=shlex.split(value)
 if len(argv)<2 or argv[0] not in ("python","python3"): raise ValueError("only direct python adapter commands are enabled")
 script=safe_path(argv[1])
 if not script.is_file() or script.suffix!=".py": raise ValueError(f"adapter not found: {argv[1]}")
 argv[1]=str(script); return argv
def run_command(value,log,step,phase,timeout):
 argv=command(value); emit(log,"command_start",step=step,phase=phase,argv=argv,timeout_seconds=timeout); start=time.monotonic()
 try:p=subprocess.run(argv,cwd=ROOT,env={"PATH":os.environ.get("PATH",""),"PYTHONIOENCODING":"utf-8","PYTHONDONTWRITEBYTECODE":"1"},capture_output=True,text=True,timeout=timeout)
 except subprocess.TimeoutExpired: emit(log,"command_timeout",step=step,phase=phase); return False
 emit(log,"command_end",step=step,phase=phase,exit_code=p.returncode,elapsed_seconds=round(time.monotonic()-start,3),stdout=p.stdout[-3000:],stderr=p.stderr[-3000:])
 return p.returncode==0
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--input",default="examples/sequential-verifiable-v1.example.json"); ap.add_argument("--timeout",type=int,default=120); a=ap.parse_args()
 rid=dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")+"-"+str(os.getpid()); log=RUNS/rid/"events.jsonl"
 emit(log,"run_start",run_id=rid,input=a.input)
 try:
  x=json.loads(safe_path(a.input).read_text(encoding="utf-8")); validate(x); emit(log,"contract_valid",contract=x["_contract"],project=x["project"],steps=len(x["steps"]))
  for i,s in enumerate(x["steps"],1):
   emit(log,"step_start",index=i,name=s["name"])
   for c in s["preconditions"]:
    if not check(c): raise ValueError(f"precondition failed in {s['name']}: {c}")
   if not run_command(s["action"],log,s["name"],"action",a.timeout): raise RuntimeError(f"action failed: {s['name']}")
   if not run_command(s["verify"],log,s["name"],"verify",a.timeout): raise RuntimeError(f"verification command failed: {s['name']}")
   for c in s["postconditions"]:
    if not check(c): raise RuntimeError(f"postcondition failed in {s['name']}: {c}")
   emit(log,"step_passed",index=i,name=s["name"])
  out=x["expected_output"]; p=safe_path(out["path"])
  if out["type"]=="file" and (not p.is_file() or p.stat().st_size<int(out["min_length"])): raise RuntimeError("declared output missing or below min_length")
  if out["type"]=="files":
   matches=list(p.glob("*")) if p.is_dir() else []
   if len(matches)<int(out["min_count"]): raise RuntimeError("declared output count below min_count")
  emit(log,"output_verified",path=out["path"]); emit(log,"run_passed",run_id=rid); return 0
 except Exception as e: emit(log,"run_error",error=type(e).__name__,message=str(e)); emit(log,"run_failed",run_id=rid); return 1
if __name__=="__main__":sys.exit(main())
