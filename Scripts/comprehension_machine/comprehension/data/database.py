"""SQLite database manager - WAL mode, CRUD, history search."""

import sqlite3, json, uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_PATH = Path(__file__).parent / "schema.sql"


class Database:
    def __init__(self, db_path="data/sessions.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.execute("PRAGMA foreign_keys=ON;")
        if SCHEMA_PATH.exists():
            self.conn.executescript(SCHEMA_PATH.read_text())
            self.conn.commit()

    def create_session(self, name, config):
        sid = str(uuid.uuid4())
        self.conn.execute("INSERT INTO sessions (id,name,created_at,config_json) VALUES (?,?,?,?)",
                          (sid, name, datetime.now(timezone.utc).isoformat(), json.dumps(config, default=str)))
        self.conn.commit()
        return sid

    def log_phase(self, session_id, statement, module, phase, data, kpi, status="completed", duration_ms=0.0):
        eid = str(uuid.uuid4())
        self.conn.execute(
            "INSERT INTO ledger (id,session_id,statement,module,phase,data_json,kpi_json,status,duration_ms,timestamp)"
            " VALUES (?,?,?,?,?,?,?,?,?,?)",
            (eid, session_id, statement, module, phase, json.dumps(data, default=str),
             json.dumps(kpi, default=str), status, duration_ms, datetime.now(timezone.utc).isoformat()))
        self.conn.commit()
        return eid

    def search_ledger(self, statement_contains="", module="", phase="", start_date="", end_date="", limit=100):
        q, p = "SELECT * FROM ledger WHERE 1=1", []
        if statement_contains: q += " AND statement LIKE ?"; p.append(f"%{statement_contains}%")
        if module: q += " AND module = ?"; p.append(module)
        if phase: q += " AND phase = ?"; p.append(phase)
        if start_date: q += " AND timestamp >= ?"; p.append(start_date)
        if end_date: q += " AND timestamp <= ?"; p.append(end_date)
        q += " ORDER BY timestamp DESC LIMIT ?"; p.append(limit)
        return [dict(r) for r in self.conn.execute(q, p).fetchall()]

    def log_error(self, module, error_text, session_id="", phase="", traceback_str="", severity="error"):
        eid = str(uuid.uuid4())
        self.conn.execute(
            "INSERT INTO errors (id,session_id,module,phase,error_text,traceback,severity,timestamp)"
            " VALUES (?,?,?,?,?,?,?,?)",
            (eid, session_id or None, module, phase or None, error_text, traceback_str, severity,
             datetime.now(timezone.utc).isoformat()))
        self.conn.commit()
        return eid

    def set_setting(self, key, value):
        self.conn.execute(
            "INSERT INTO settings (key,value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, json.dumps(value, default=str)))
        self.conn.commit()

    def get_setting(self, key, default=None):
        row = self.conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
        return json.loads(row["value"]) if row else default

    def close(self): self.conn.close()
    def __enter__(self): return self
    def __exit__(self, *a): self.conn.close()
