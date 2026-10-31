#!/usr/bin/env python3
"""Authenticated single-owner coordinator API; Python standard library only."""
import hmac
import json
import os
import re
import sqlite3
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

DB_PATH = os.environ.get("ORCHESTRATOR_DB", "orchestrator.sqlite3")
TOKEN = os.environ.get("ORCHESTRATOR_OWNER_TOKEN", "")
HOST = os.environ.get("ORCHESTRATOR_HOST", "127.0.0.1")
PORT = int(os.environ.get("ORCHESTRATOR_PORT", "8080"))
MAX_BODY = 1_000_000
VALID_PRIORITIES = {"low", "normal", "high", "urgent"}
VALID_RESULTS = {"completed", "partial", "blocked", "failed"}
ID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")

def now():
    return datetime.now(timezone.utc).isoformat()

def connect():
    db = sqlite3.connect(DB_PATH, timeout=15)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    db.execute("PRAGMA journal_mode=WAL")
    return db

def initialize():
    with connect() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS instructions(
          id TEXT PRIMARY KEY, idempotency_key TEXT UNIQUE NOT NULL,
          origin TEXT NOT NULL, original_text TEXT NOT NULL,
          project TEXT, priority TEXT NOT NULL, status TEXT NOT NULL,
          created_at TEXT NOT NULL, updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS tasks(
          id TEXT PRIMARY KEY, instruction_id TEXT NOT NULL REFERENCES instructions(id),
          title TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'queued',
          result_json TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS tasks_queue ON tasks(status, created_at);
        CREATE TABLE IF NOT EXISTS audit(
          id INTEGER PRIMARY KEY AUTOINCREMENT, actor TEXT NOT NULL,
          action TEXT NOT NULL, resource_id TEXT NOT NULL, at TEXT NOT NULL,
          detail_json TEXT NOT NULL
        );
        """)

def record(db, action, resource_id, detail):
    db.execute("INSERT INTO audit(actor,action,resource_id,at,detail_json) VALUES(?,?,?,?,?)",
               ("owner_or_worker", action, resource_id, now(),
                json.dumps(detail, ensure_ascii=False, separators=(",", ":"))))

def submit_instruction(payload):
    text = payload.get("text")
    if not isinstance(text, str) or not text.strip() or len(text) > 20000:
        raise ValueError("text must contain 1-20000 characters")
    key = payload.get("idempotency_key") or str(uuid.uuid4())
    if not isinstance(key, str) or not key.strip() or len(key) > 200:
        raise ValueError("invalid idempotency_key")
    origin = payload.get("origin", "bridge")
    project = payload.get("project")
    priority = payload.get("priority", "normal")
    if not isinstance(origin, str) or not origin.strip() or len(origin) > 100:
        raise ValueError("invalid origin")
    if project is not None and (not isinstance(project, str) or len(project) > 100):
        raise ValueError("invalid project")
    if priority not in VALID_PRIORITIES:
        raise ValueError("invalid priority")
    with connect() as db:
        existing = db.execute("SELECT * FROM instructions WHERE idempotency_key=?", (key,)).fetchone()
        if existing:
            return dict(existing), True
        ident, stamp = str(uuid.uuid4()), now()
        db.execute("INSERT INTO instructions VALUES(?,?,?,?,?,?,?,?,?)",
                   (ident, key, origin.strip(), text.strip(), project, priority, "received", stamp, stamp))
        task_id = str(uuid.uuid4())
        db.execute("INSERT INTO tasks(id,instruction_id,title,status,created_at,updated_at) VALUES(?,?,?,?,?,?)",
                   (task_id, ident, text.strip()[:160], "queued", stamp, stamp))
        record(db, "instruction.received", ident, {"task_id": task_id, "project": project})
        return dict(db.execute("SELECT * FROM instructions WHERE id=?", (ident,)).fetchone()), False

class Handler(BaseHTTPRequestHandler):
    server_version = "OrquestadorCentral"
    sys_version = ""

    def send_json(self, code, obj):
        raw = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(raw)

    def send_empty(self, code):
        self.send_response(code)
        self.send_header("Content-Length", "0")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

    def authorized(self):
        supplied = self.headers.get("Authorization", "")
        return bool(TOKEN) and hmac.compare_digest(supplied, "Bearer " + TOKEN)

    def body(self):
        raw_size = self.headers.get("Content-Length")
        if raw_size is None or not raw_size.isdigit():
            raise ValueError("valid Content-Length required")
        size = int(raw_size)
        if size < 1 or size > MAX_BODY:
            raise ValueError("body size invalid")
        try:
            data = json.loads(self.rfile.read(size))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("invalid JSON body") from exc
        if not isinstance(data, dict):
            raise ValueError("JSON object required")
        return data

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == "/health":
            return self.send_json(200, {"status": "ok", "service": "orquestador-central", "version": "0.1.1"})
        if not self.authorized():
            return self.send_json(401, {"error": "unauthorized"})
        match = re.fullmatch(r"/v1/instructions/([0-9a-f-]{36})", path)
        if match:
            ident = match.group(1)
            with connect() as db:
                row = db.execute("SELECT * FROM instructions WHERE id=?", (ident,)).fetchone()
                tasks = db.execute("SELECT * FROM tasks WHERE instruction_id=? ORDER BY created_at", (ident,)).fetchall()
            if not row:
                return self.send_json(404, {"error": "not_found"})
            return self.send_json(200, {"instruction": dict(row), "tasks": [dict(x) for x in tasks]})
        return self.send_json(404, {"error": "not_found"})

    def do_POST(self):
        if not self.authorized():
            return self.send_json(401, {"error": "unauthorized"})
        try:
            path = urlsplit(self.path).path
            payload = self.body()
            if path == "/v1/instructions":
                row, duplicate = submit_instruction(payload)
                return self.send_json(200 if duplicate else 201, {"instruction": row, "duplicate": duplicate})
            if path == "/v1/tasks/claim":
                worker = payload.get("worker", "worker")
                if not isinstance(worker, str) or not worker.strip() or len(worker) > 100:
                    raise ValueError("invalid worker")
                with connect() as db:
                    db.execute("BEGIN IMMEDIATE")
                    task = db.execute("SELECT * FROM tasks WHERE status='queued' ORDER BY created_at,id LIMIT 1").fetchone()
                    if not task:
                        self.send_empty(204)
                        return
                    stamp = now()
                    db.execute("UPDATE tasks SET status='running',updated_at=? WHERE id=? AND status='queued'",
                               (stamp, task["id"]))
                    db.execute("UPDATE instructions SET status='running',updated_at=? WHERE id=?",
                               (stamp, task["instruction_id"]))
                    record(db, "task.claimed", task["id"], {"worker": worker.strip()})
                    claimed = dict(db.execute("SELECT * FROM tasks WHERE id=?", (task["id"],)).fetchone())
                return self.send_json(200, {"task": claimed, "worker": worker.strip()})
            match = re.fullmatch(r"/v1/tasks/([0-9a-f-]{36})/result", path)
            if match:
                task_id = match.group(1)
                status = payload.get("status")
                if status not in VALID_RESULTS:
                    raise ValueError("invalid result status")
                evidence = json.dumps(payload, ensure_ascii=False)
                with connect() as db:
                    db.execute("BEGIN IMMEDIATE")
                    task = db.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
                    if not task:
                        return self.send_json(404, {"error": "not_found"})
                    if task["status"] != "running":
                        return self.send_json(409, {"error": "task_not_running", "current_status": task["status"]})
                    stamp = now()
                    db.execute("UPDATE tasks SET status=?,result_json=?,updated_at=? WHERE id=?",
                               (status, evidence, stamp, task_id))
                    db.execute("UPDATE instructions SET status=?,updated_at=? WHERE id=?",
                               (status, stamp, task["instruction_id"]))
                    record(db, "task.result", task_id, payload)
                return self.send_json(200, {"task_id": task_id, "status": status})
            return self.send_json(404, {"error": "not_found"})
        except ValueError as exc:
            return self.send_json(400, {"error": str(exc)})
        except Exception:
            return self.send_json(500, {"error": "internal_error"})

    def log_message(self, fmt, *args):
        print("%s - %s" % (self.log_date_time_string(), fmt % args), flush=True)

def main():
    if not TOKEN:
        raise SystemExit("ORCHESTRATOR_OWNER_TOKEN is required")
    initialize()
    print(f"Coordinator listening on {HOST}:{PORT}", flush=True)
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()

if __name__ == "__main__":
    main()
