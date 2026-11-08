#!/usr/bin/env python3
"""Minimal sequential-verifiable runner. Commands execute without a shell."""
from __future__ import annotations
import argparse, datetime as dt, json, os, shlex, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "runtime" / "runs"

def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def emit(log, event, **data):
    row={"ts":now(),"event":event,**data}
    log.parent.mkdir(parents=True,exist_ok=True)
    with log.open("a",encoding="utf-8") as f: f.write(json.dumps(row,ensure_ascii=False)+"\n")
    print(json.dumps(row,ensure_ascii=False))

def safe_path(value):
    p=(ROOT/value).resolve()
    if p != ROOT and ROOT not in p.parents: raise ValueError(f"path escapes workspace: {value}")
    return p

def validate(x):
    required=["$schema","_contract","id","project","version","steps","expected_output"]
    missing=[k for k in required if k not in x]
    if missing: raise ValueError("missing fields: "+", ".join(missing))
    if x["_contract"]!="SEQUENTIAL-VERIFIABLE-v1": raise ValueError("wrong _contract")
    if "sequential-verifiable-v1.schema.json" not in x["$schema"]: raise ValueError("missing explicit schema marker")
    if not isinstance(x["steps"],list) or not x["steps"]: raise ValueError("steps must be a non-empty array")
    for i,s in enumerate(x["steps"],1):
        for k in ("name","action","expected","verify"):
            if not isinstance(s.get(k),str) or not s[k].strip(): raise ValueError(f"step {i}: invalid {k}")
    out=x["expected_output"]
    if out.get("type") not in ("file","files","text") or not out.get("path"): raise ValueError("invalid expected_output")
    if int(out.get("min_count",0))<1 or int(out.get("min_length",0))<1: raise ValueError("invalid output minima")

def command(text):
    # No shell: reject shell metacharacters and require an executable plus arguments.
    forbidden=[";","&&","||","|",">","<","$(", "`"]
    if any(t in text for t in forbidden): raise ValueError("shell syntax is forbidden; use a direct argv command")
    argv=shlex.split(text)
    if not argv: raise ValueError("empty command")
    if argv[0] not in ("python","python3"): raise ValueError("only python/python3 adapter commands are currently enabled")
    if len(argv)<2: raise ValueError("command must name a script")
    script=safe_path(argv[1])
    if not script.is_file() or script.suffix!=".py": raise ValueError(f"adapter script not found or not .py: {argv[1]}")
    argv[1]=str(script)
    return argv

def run_step(spec, log, timeout):
    for field in ("action","verify"):
        argv=command(spec[field])
        emit(log,"command_start",step=spec["name"],phase=field,argv=argv,timeout_seconds=timeout)
        started=time.monotonic()
        try:
            p=subprocess.run(argv,cwd=ROOT,env={"PATH":os.environ.get("PATH",""),"PYTHONIOENCODING":"utf-8","PYTHONDONTWRITEBYTECODE":"1"},capture_output=True,text=True,timeout=timeout)
        except subprocess.TimeoutExpired:
            emit(log,"command_timeout",step=spec["name"],phase=field,elapsed_seconds=round(time.monotonic()-started,3))
            return False
        emit(log,"command_end",step=spec["name"],phase=field,exit_code=p.returncode,elapsed_seconds=round(time.monotonic()-started,3),stdout=p.stdout[-4000:],stderr=p.stderr[-4000:])
        if p.returncode: return False
    return True

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",default="examples/sequential-verifiable-v1.example.json")
    ap.add_argument("--timeout",type=int,default=120)
    args=ap.parse_args()
    run_id=dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")+"-"+str(os.getpid())
    log=RUNS/run_id/"events.jsonl"
    emit(log,"run_start",run_id=run_id,input=args.input,timeout_seconds=args.timeout)
    try:
        src=safe_path(args.input); x=json.loads(src.read_text(encoding="utf-8")); validate(x)
        emit(log,"contract_valid",contract=x["_contract"],project=x["project"],step_count=len(x["steps"]))
        for index,step in enumerate(x["steps"],1):
            emit(log,"step_start",index=index,name=step["name"])
            if not run_step(step,log,args.timeout):
                emit(log,"step_failed",index=index,name=step["name"])
                emit(log,"run_failed",run_id=run_id,failed_step=step["name"])
                return 1
            emit(log,"step_passed",index=index,name=step["name"])
        out=safe_path(x["expected_output"]["path"])
        if not out.exists(): raise ValueError("expected output does not exist: "+x["expected_output"]["path"])
        if out.is_file():
            if out.stat().st_size<int(x["expected_output"]["min_length"]): raise ValueError("output shorter than min_length")
        emit(log,"output_verified",path=str(out.relative_to(ROOT)),bytes=out.stat().st_size if out.is_file() else None)
        emit(log,"run_passed",run_id=run_id)
        return 0
    except Exception as e:
        emit(log,"run_error",error=type(e).__name__,message=str(e))
        emit(log,"run_failed",run_id=run_id)
        return 2

if __name__=="__main__": sys.exit(main())
