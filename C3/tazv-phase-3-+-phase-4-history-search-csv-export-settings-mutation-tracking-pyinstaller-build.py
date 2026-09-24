#!/usr/bin/env python3
"""
TAZV COMPREHENSION MACHINE — Phase 3 + Phase 4 Bootstrap
=========================================================

Phase 3: History search UI, CSV export, settings panel, mutation tracking (Prop X)
Phase 4: PyInstaller .exe build script + spec file

Run from: D:\\OntoProjekt\\CanvasMinstral\\Scripts\\
Command:  python tazv_phase3_phase4_bootstrap.py

PREREQUISITES (Phase 0-2 must exist):
  comprehension/core/ processing_pipeline.py, symbol_mapper.py, module_adapters.py
                    egyptian_color_semantics.py, module_semantics.py, hit_grammar.py
                    tonos.py, rozetni_kamni.py, themes.py, exporter.py
  comprehension/ui/  main_window_v2.py, module_window.py, r7_progress.py, knowledge_renderer.py
  comprehension/data/ schema.sql, database.py
  ta3v_colors.qss

CREATES:
  comprehension/data/db_queries.py      — search/settings/mutation query layer
  comprehension/core/csv_exporter.py   — CSV export (sessions + ledger)
  comprehension/core/mutation_tracker.py — mutation tracking (Proposition X: škatla = mutable)
  comprehension/ui/history_search.py   — history search dialog
  comprehension/ui/settings_panel.py   — settings dialog (guard thresholds, defaults, TONOS)
  comprehension/ui/main_window_v3.py   — fully integrated window (v2 + all Phase 3 features)
  build_exe.py                         — Phase 4: PyInstaller build launcher
  ta3v.spec                            — Phase 4: PyInstaller spec

PATCHES:
  comprehension/data/schema.sql         — adds mutations table

PROPOSITIONS ENACTED:
  Prop IX  (traveling module) — settings panel adjusts guard thresholds per session
  Prop X   (škatla = mutable) — mutation tracker compares reprocessed statements
  Prop IV  (identity diff)    — history search shows session evolution
  Prop VI/XIV (word as precond.) — depth level 4 (absolutni rez) now configurable default
"""
import os

BASE = "comprehension_machine"

# ═══════════════════════════════════════════════════════════════
# FILE 1: db_queries.py — query layer (decoupled from Database class)
# ═══════════════════════════════════════════════════════════════

DB_QUERIES_PY = '''"""
DB Queries — TAZV Comprehension Machine
========================================
Decoupled query layer. Accepts db_path (string) or sqlite3.Connection.
Does NOT depend on the Database class internals.

Corpus principle: "zapis kot izpust" — queries release stored meaning
back into the present, they do not archive it.
"""
import sqlite3
import json
from datetime import datetime
from typing import Optional


def _get_conn(db) -> sqlite3.Connection:
    """Accept db_path string, sqlite3.Connection, or Database-like object."""
    if isinstance(db, str):
        return sqlite3.connect(db)
    if isinstance(db, sqlite3.Connection):
        return db
    if hasattr(db, "conn"):
        return db.conn
    if hasattr(db, "_conn"):
        return db._conn
    if hasattr(db, "get_connection"):
        return db.get_connection()
    raise TypeError(f"Cannot get connection from {type(db)}")


def search_sessions(db, filters: dict = None) -> list:
    """Search sessions with optional filters. Returns list of dicts.

    Filters:
      text:         LIKE match on statement
      date_from:    YYYY-MM-DD
      date_to:      YYYY-MM-DD
      status:       exact match (completed/partial/error)
      error_phase:  only sessions with errors in this phase
    """
    conn = _get_conn(db)
    conn.row_factory = sqlite3.Row
    filters = filters or {}

    sql = """
        SELECT s.id, s.statement, s.status, s.created_at,
               (SELECT COUNT(*) FROM errors WHERE session_id = s.id) AS error_count,
               (SELECT COUNT(*) FROM ledger WHERE session_id = s.id) AS phase_count
        FROM sessions s
        WHERE 1=1
    """
    params = []

    if filters.get("text"):
        sql += " AND s.statement LIKE ?"
        params.append(f"%{filters['text']}%")

    if filters.get("date_from"):
        sql += " AND s.created_at >= ?"
        params.append(filters["date_from"])

    if filters.get("date_to"):
        sql += " AND s.created_at <= ?"
        params.append(filters["date_to"] + " 23:59:59")

    if filters.get("status") and filters["status"] != "Vsi":
        sql += " AND s.status = ?"
        params.append(filters["status"])

    if filters.get("error_phase") and filters["error_phase"] != "Vse":
        sql += " AND EXISTS (SELECT 1 FROM errors e WHERE e.session_id = s.id AND e.phase = ?)"
        params.append(filters["error_phase"])

    sql += " ORDER BY s.created_at DESC"
    rows = conn.execute(sql, params).fetchall()

    if isinstance(db, str):
        conn.close()

    return [dict(r) for r in rows]


def get_session_by_id(db, session_id: int) -> Optional[dict]:
    """Get a full session by ID, including phases and errors."""
    conn = _get_conn(db)
    conn.row_factory = sqlite3.Row

    session = conn.execute(
        "SELECT * FROM sessions WHERE id = ?", (session_id,)
    ).fetchone()
    if not session:
        if isinstance(db, str):
            conn.close()
        return None

    result = dict(session)
    if result.get("result_json"):
        try:
            result["result_parsed"] = json.loads(result["result_json"])
        except (json.JSONDecodeError, TypeError):
            result["result_parsed"] = None

    phases = conn.execute(
        "SELECT * FROM ledger WHERE session_id = ? ORDER BY phase", (session_id,)
    ).fetchall()
    result["phases"] = [dict(p) for p in phases]

    errors = conn.execute(
        "SELECT * FROM errors WHERE session_id = ?", (session_id,)
    ).fetchall()
    result["errors"] = [dict(e) for e in errors]

    if isinstance(db, str):
        conn.close()
    return result


def get_settings(db) -> dict:
    """Get all settings as a dict."""
    conn = _get_conn(db)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT key, value FROM settings").fetchall()
    if isinstance(db, str):
        conn.close()
    return {r["key"]: r["value"] for r in rows}


def set_settings(db, settings: dict):
    """Upsert settings."""
    conn = _get_conn(db)
    for key, value in settings.items():
        conn.execute(
            "INSERT INTO settings (key, value, updated_at) VALUES (?, ?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at",
            (key, str(value), datetime.now().isoformat()),
        )
    conn.commit()
    if isinstance(db, str):
        conn.close()


def log_mutation(db, old_session_id: int, new_session_id: int,
                 statement: str, diff: dict):
    """Store a mutation diff (Proposition X: škatla = mutable)."""
    conn = _get_conn(db)
    conn.execute(
        """INSERT INTO mutations (old_session_id, new_session_id, statement, diff_json, created_at)
           VALUES (?, ?, ?, ?, ?)""",
        (old_session_id, new_session_id, statement,
         json.dumps(diff, ensure_ascii=False, default=str),
         datetime.now().isoformat()),
    )
    conn.commit()
    if isinstance(db, str):
        conn.close()


def get_mutations(db, statement: str = None) -> list:
    """Get mutation history, optionally filtered by statement."""
    conn = _get_conn(db)
    conn.row_factory = sqlite3.Row
    if statement:
        rows = conn.execute(
            "SELECT * FROM mutations WHERE statement LIKE ? ORDER BY created_at DESC",
            (f"%{statement}%",),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM mutations ORDER BY created_at DESC"
        ).fetchall()
    result = []
    for r in rows:
        d = dict(r)
        if d.get("diff_json"):
            try:
                d["diff_parsed"] = json.loads(d["diff_json"])
            except (json.JSONDecodeError, TypeError):
                d["diff_parsed"] = None
        result.append(d)
    if isinstance(db, str):
        conn.close()
    return result


def get_ledger_entries(db, session_id: int = None) -> list:
    """Get ledger entries, optionally for one session."""
    conn = _get_conn(db)
    conn.row_factory = sqlite3.Row
    if session_id:
        rows = conn.execute(
            "SELECT * FROM ledger WHERE session_id = ? ORDER BY phase", (session_id,)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM ledger ORDER BY session_id, phase").fetchall()
    if isinstance(db, str):
        conn.close()
    return [dict(r) for r in rows]
'''

# ═══════════════════════════════════════════════════════════════
# FILE 2: csv_exporter.py — CSV export
# ═══════════════════════════════════════════════════════════════

CSV_EXPORTER_PY = '''"""
CSV Exporter — TAZV Comprehension Machine
==========================================
Exports session summaries and ledger data as CSV.

Corpus principle: "zapis kot izpust" (writing as release).
Export is not archival — it releases the data to flow elsewhere.
"""
import csv
from datetime import datetime

try:
    from comprehension.data.db_queries import search_sessions, get_ledger_entries
except ImportError:
    search_sessions = None
    get_ledger_entries = None


def export_sessions_csv(db, filepath: str, filters: dict = None) -> int:
    """Export session summaries as CSV. Returns row count."""
    if search_sessions is None:
        raise ImportError("db_queries not available")
    sessions = search_sessions(db, filters)
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([
            "ID", "Izrek", "Status", "Datum", "Napake", "Faze"
        ])
        for s in sessions:
            writer.writerow([
                s.get("id", ""),
                s.get("statement", ""),
                s.get("status", ""),
                s.get("created_at", ""),
                s.get("error_count", 0),
                s.get("phase_count", 0),
            ])
    return len(sessions)


def export_ledger_csv(db, filepath: str, session_id: int = None) -> int:
    """Export ledger entries as CSV. Returns row count."""
    if get_ledger_entries is None:
        raise ImportError("db_queries not available")
    entries = get_ledger_entries(db, session_id)
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([
            "ID", "Session ID", "Phase", "Module", "Data", "Created At"
        ])
        for e in entries:
            data_str = e.get("data_json", "")
            # Flatten JSON for CSV — keep as string, truncate if huge
            if data_str and len(data_str) > 500:
                data_str = data_str[:497] + "..."
            writer.writerow([
                e.get("id", ""),
                e.get("session_id", ""),
                e.get("phase", ""),
                e.get("module", ""),
                data_str,
                e.get("created_at", ""),
            ])
    return len(entries)


def export_full_csv(db, filepath: str) -> int:
    """Export all sessions + their ledger entries interleaved as CSV."""
    if search_sessions is None or get_ledger_entries is None:
        raise ImportError("db_queries not available")
    sessions = search_sessions(db)
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Type", "ID", "Session ID", "Statement/Phase",
                         "Status/Module", "Datum/Data", "Extra"])
        for s in sessions:
            writer.writerow([
                "SESSION", s.get("id", ""), "",
                s.get("statement", ""), s.get("status", ""),
                s.get("created_at", ""), f"napake={s.get('error_count', 0)}"
            ])
            entries = get_ledger_entries(db, s.get("id"))
            for e in entries:
                writer.writerow([
                    "LEDGER", e.get("id", ""), e.get("session_id", ""),
                    str(e.get("phase", "")), e.get("module", ""),
                    e.get("created_at", ""), e.get("data_json", "")[:200]
                ])
    return len(sessions)
'''

# ═══════════════════════════════════════════════════════════════
# FILE 3: mutation_tracker.py — Proposition X: škatla = mutable
# ═══════════════════════════════════════════════════════════════

MUTATION_TRACKER_PY = '''"""
Mutation Tracker — TAZV Comprehension Machine
================================================
Tracks what changes when a statement is reprocessed.

Enacts Proposition X (škatla = agentna enota):
  "Every concept is archived, shared, ready for mutation — never frozen."
  Each processed statement becomes a škatla (box). When reprocessed,
  the tracker shows what changed — not as error, but as evolution.

Corpus: "Zamrznjena definicija je odgovor, ki si je prepovedal odmev."
  Mutation tracking keeps the echo alive.
"""
import json
from datetime import datetime
from typing import Optional

try:
    from comprehension.data.db_queries import log_mutation, get_mutations, search_sessions
except ImportError:
    log_mutation = None
    get_mutations = None
    search_sessions = None


class MutationTracker:
    """Compares R-7 results for the same statement across sessions."""

    def __init__(self, db=None):
        self.db = db

    def find_previous_sessions(self, statement: str) -> list:
        """Find past sessions with the same (or similar) statement."""
        if search_sessions is None or self.db is None:
            return []
        return search_sessions(self.db, {"text": statement})

    def compute_diff(self, old_result: dict, new_result: dict,
                     statement: str = "") -> dict:
        """Compare two R-7 pipeline results. Returns structured diff.

        Diff structure:
          statement, old_session_id, new_session_id, timestamp,
          phase_changes: {phase: {old, new}},
          new_phases: [...], removed_phases: [...],
          status_change: {old, new},
          error_changes: {added: [...], removed: [...]},
          changed: bool, summary: str
        """
        old_phases = old_result.get("phases", {})
        new_phases = new_result.get("phases", {})
        old_errors = old_result.get("errors", [])
        new_errors = new_result.get("errors", [])

        old_session = old_result.get("session", {})
        new_session = new_result.get("session", {})

        diff = {
            "statement": statement or new_result.get("statement", ""),
            "old_session_id": old_session.get("id") if isinstance(old_session, dict) else old_session,
            "new_session_id": new_session.get("id") if isinstance(new_session, dict) else new_session,
            "timestamp": datetime.now().isoformat(),
            "phase_changes": {},
            "new_phases": [],
            "removed_phases": [],
            "status_change": {
                "old": old_result.get("status"),
                "new": new_result.get("status"),
            },
            "error_changes": {
                "added": [],
                "removed": [],
            },
        }

        all_phases = set(list(old_phases.keys()) + list(new_phases.keys()))
        for phase in sorted(all_phases):
            if phase not in old_phases:
                diff["new_phases"].append(phase)
            elif phase not in new_phases:
                diff["removed_phases"].append(phase)
            else:
                old_data = old_phases[phase]
                new_data = new_phases[phase]
                if old_data != new_data:
                    diff["phase_changes"][phase] = {
                        "old": old_data,
                        "new": new_data,
                    }

        old_err_set = set(str(e) for e in old_errors)
        new_err_set = set(str(e) for e in new_errors)
        diff["error_changes"]["added"] = list(new_err_set - old_err_set)
        diff["error_changes"]["removed"] = list(old_err_set - new_err_set)

        diff["changed"] = bool(
            diff["phase_changes"]
            or diff["new_phases"]
            or diff["removed_phases"]
            or diff["error_changes"]["added"]
            or diff["error_changes"]["removed"]
            or diff["status_change"]["old"] != diff["status_change"]["new"]
        )

        # Human-readable summary
        parts = []
        if diff["phase_changes"]:
            parts.append(f"{len(diff['phase_changes'])} faz spremenjenih")
        if diff["new_phases"]:
            parts.append(f"{len(diff['new_phases'])} novih faz")
        if diff["removed_phases"]:
            parts.append(f"{len(diff['removed_phases'])} odstranjenih faz")
        if diff["error_changes"]["added"]:
            parts.append(f"{len(diff['error_changes']['added'])} novih napak")
        if diff["error_changes"]["removed"]:
            parts.append(f"{len(diff['error_changes']['removed'])} rešenih napak")
        if diff["status_change"]["old"] != diff["status_change"]["new"]:
            parts.append(f"status: {diff['status_change']['old']} → {diff['status_change']['new']}")
        diff["summary"] = ", ".join(parts) if parts else "brez sprememb"

        return diff

    def track_and_store(self, new_result: dict, statement: str) -> Optional[dict]:
        """Find previous sessions, compute diff, store if changed.

        Returns the diff dict if a previous session was found, None otherwise.
        """
        if search_sessions is None or self.db is None:
            return None

        previous = self.find_previous_sessions(statement)
        if not previous:
            return None

        # Use the most recent previous session
        old_session = previous[0]
        old_result = old_session.get("result_parsed") or old_session

        diff = self.compute_diff(old_result, new_result, statement)

        if log_mutation is not None and diff.get("old_session_id"):
            try:
                log_mutation(
                    self.db,
                    diff["old_session_id"],
                    diff.get("new_session_id") or 0,
                    statement,
                    diff,
                )
            except Exception:
                pass

        return diff

    def get_history(self, statement: str = None) -> list:
        """Get mutation history for a statement (or all)."""
        if get_mutations is None or self.db is None:
            return []
        return get_mutations(self.db, statement)

    def format_diff_html(self, diff: dict) -> str:
        """Format a diff dict as simple HTML for display."""
        if not diff:
            return "<p>Brez predhodnih sej.</p>"

        html_parts = [f"<h3>Mutacija: {diff.get('summary', '')}</h3>"]

        if diff.get("status_change", {}).get("old") != diff.get("status_change", {}).get("new"):
            sc = diff["status_change"]
            html_parts.append(
                f"<p><b>Status:</b> {sc.get('old')} → {sc.get('new')}</p>"
            )

        if diff.get("phase_changes"):
            html_parts.append("<h4>Spremenjene faze:</h4><ul>")
            for phase, change in diff["phase_changes"].items():
                html_parts.append(
                    f"<li><b>{phase}</b>: {change.get('old', '')} → {change.get('new', '')}</li>"
                )
            html_parts.append("</ul>")

        if diff.get("new_phases"):
            html_parts.append(f"<p><b>Nove faze:</b> {', '.join(diff['new_phases'])}</p>")

        if diff.get("removed_phases"):
            html_parts.append(f"<p><b>Odstranjene faze:</b> {', '.join(diff['removed_phases'])}</p>")

        if diff.get("error_changes", {}).get("added"):
            html_parts.append(f"<p><b>Nove napake:</b> {', '.join(diff['error_changes']['added'])}</p>")

        if diff.get("error_changes", {}).get("removed"):
            html_parts.append(f"<p><b>Rešene napake:</b> {', '.join(diff['error_changes']['removed'])}</p>")

        return "\\n".join(html_parts)
'''

# ═══════════════════════════════════════════════════════════════
# FILE 4: history_search.py — search past sessions
# ═══════════════════════════════════════════════════════════════

HISTORY_SEARCH_PY = '''"""
History Search — TAZV Comprehension Machine
=============================================
Search past R-7 sessions by statement text, date range, status, or
error phase. Double-click a result to load the full session.

Enacts Proposition IV (evolucijski zemljevid identitete):
  shows how the user's ontological position changes across sessions.
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QDateEdit, QComboBox, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt, QDate, pyqtSignal

try:
    from comprehension.data.db_queries import search_sessions, get_session_by_id
except ImportError:
    search_sessions = None
    get_session_by_id = None

try:
    from comprehension.core.module_semantics import MODULE_ORDER
except ImportError:
    MODULE_ORDER = ["bios", "state", "uaf", "jewik", "apd", "micro", "visualization"]


class HistorySearchDialog(QDialog):
    """Search dialog for past sessions. Emits session_selected(int)."""
    session_selected = pyqtSignal(int)

    def __init__(self, db=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Zgodovina sej — R-7")
        self.setGeometry(150, 150, 900, 500)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        # Row 1: statement text search
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Izrek:"))
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Iskanje po besedilu izreka...")
        self.txt_search.returnPressed.connect(self.on_search)
        row1.addWidget(self.txt_search)
        layout.addLayout(row1)

        # Row 2: date range + status + error phase
        row2 = QHBoxLayout()

        row2.addWidget(QLabel("Od:"))
        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate().addMonths(-6))
        self.date_from.setCalendarPopup(True)
        self.date_from.setDisplayFormat("yyyy-MM-dd")
        row2.addWidget(self.date_from)

        row2.addWidget(QLabel("Do:"))
        self.date_to = QDateEdit()
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setCalendarPopup(True)
        self.date_to.setDisplayFormat("yyyy-MM-dd")
        row2.addWidget(self.date_to)

        row2.addWidget(QLabel("Status:"))
        self.cmb_status = QComboBox()
        self.cmb_status.addItems(["Vsi", "completed", "partial", "error"])
        row2.addWidget(self.cmb_status)

        row2.addWidget(QLabel("Faza napake:"))
        self.cmb_error_phase = QComboBox()
        self.cmb_error_phase.addItems(["Vse"] + MODULE_ORDER)
        row2.addWidget(self.cmb_error_phase)

        layout.addLayout(row2)

        # Search + Export buttons
        btn_row = QHBoxLayout()
        self.btn_search = QPushButton("Išči")
        self.btn_search.clicked.connect(self.on_search)
        btn_row.addWidget(self.btn_search)

        self.btn_export_csv = QPushButton("Izvozi CSV")
        self.btn_export_csv.clicked.connect(self.on_export_csv)
        btn_row.addWidget(self.btn_export_csv)

        btn_row.addStretch()
        self.btn_close = QPushButton("Zapri")
        self.btn_close.clicked.connect(self.close)
        btn_row.addWidget(self.btn_close)
        layout.addLayout(btn_row)

        # Results table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Izrek", "Status", "Datum", "Napake"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.doubleClicked.connect(self.on_select)
        layout.addWidget(self.table)

        self._result_count = QLabel("Pripravljen za iskanje.")
        layout.addWidget(self._result_count)

    def on_search(self):
        if search_sessions is None or self.db is None:
            self._result_count.setText("Baza podatkov ni na voljo.")
            return

        status = self.cmb_status.currentText()
        error_phase = self.cmb_error_phase.currentText()
        filters = {
            "text": self.txt_search.text().strip() or None,
            "date_from": self.date_from.date().toString("yyyy-MM-dd"),
            "date_to": self.date_to.date().toString("yyyy-MM-dd"),
            "status": status if status != "Vsi" else None,
            "error_phase": error_phase if error_phase != "Vse" else None,
        }
        # Remove None values
        filters = {k: v for k, v in filters.items() if v}

        try:
            results = search_sessions(self.db, filters)
        except Exception as e:
            self._result_count.setText(f"Napaka pri iskanju: {e}")
            return

        self.table.setRowCount(len(results))
        for i, row in enumerate(results):
            self.table.setItem(i, 0, QTableWidgetItem(str(row.get("id", ""))))
            self.table.setItem(i, 1, QTableWidgetItem(str(row.get("statement", ""))[:80]))
            self.table.setItem(i, 2, QTableWidgetItem(str(row.get("status", ""))))
            self.table.setItem(i, 3, QTableWidgetItem(str(row.get("created_at", ""))[:19]))
            self.table.setItem(i, 4, QTableWidgetItem(str(row.get("error_count", 0))))

        self._result_count.setText(f"Najdenih: {len(results)} sej.")

    def on_select(self, index):
        row = index.row()
        id_item = self.table.item(row, 0)
        if id_item:
            try:
                session_id = int(id_item.text())
                self.session_selected.emit(session_id)
            except ValueError:
                pass

    def on_export_csv(self):
        """Export current search results as CSV."""
        try:
            from comprehension.core.csv_exporter import export_sessions_csv
        except ImportError:
            QMessageBox.warning(self, "Napaka", "CSV izvoznik ni na voljo.")
            return

        from PyQt6.QtWidgets import QFileDialog
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Izvozi rezultate CSV", "", "CSV Files (*.csv)"
        )
        if not filepath:
            return

        status = self.cmb_status.currentText()
        error_phase = self.cmb_error_phase.currentText()
        filters = {
            "text": self.txt_search.text().strip() or None,
            "date_from": self.date_from.date().toString("yyyy-MM-dd"),
            "date_to": self.date_to.date().toString("yyyy-MM-dd"),
            "status": status if status != "Vsi" else None,
            "error_phase": error_phase if error_phase != "Vse" else None,
        }
        filters = {k: v for k, v in filters.items() if v}

        try:
            count = export_sessions_csv(self.db, filepath, filters)
            QMessageBox.information(self, "Izvoz", f"Izvoženo {count} sej v:\\n{filepath}")
        except Exception as e:
            QMessageBox.warning(self, "Napaka", f"Izvoz ni uspel: {e}")
'''

# ═══════════════════════════════════════════════════════════════
# FILE 5: settings_panel.py — guard thresholds, defaults, TONOS
# ═══════════════════════════════════════════════════════════════

SETTINGS_PANEL_PY = '''"""
Settings Panel — TAZV Comprehension Machine
=============================================
Configure R-7 guard thresholds, default theme, default ∂ Globina,
and TONOS frequency toggles.

Enacts Proposition IX (potujoči modul):
  modules adjust guard thresholds per session — they travel, not fix.

Guard regime (corpus-validated):
  κ ≥ .70, χ ≥ .40, μ ∈ [.50, .80], ℜ ≤ .03
  β_NE ≥ .30 → EX_B (exit bridge)
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QDoubleSpinBox,
    QComboBox, QCheckBox, QPushButton, QGroupBox,
    QLabel, QHBoxLayout
)
from PyQt6.QtCore import Qt

try:
    from comprehension.data.db_queries import get_settings, set_settings
except ImportError:
    get_settings = None
    set_settings = None

# Corpus-validated guard defaults
DEFAULT_GUARDS = {
    "kappa": 0.70,
    "chi": 0.40,
    "mu_min": 0.50,
    "mu_max": 0.80,
    "real": 0.03,
    "beta_ne": 0.30,
}

TONOS_PHASES = [
    ("bios", "∅ BIOS", 220),
    ("state", "¬ STATE", 261),
    ("uaf", "∆ UAF", 330),
    ("jewik", "1 JEWIK", 392),
    ("apd", "⧖ APD", 440),
    ("micro", "∮ MICRO", 550),
    ("visualization", "⟡ VIS", 660),
]


class SettingsDialog(QDialog):
    """Settings dialog for guard thresholds, defaults, and TONOS."""

    def __init__(self, db=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Nastavitve — TAZV")
        self.setGeometry(250, 250, 520, 640)
        self._init_ui()
        self._load_settings()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        # ── Guard thresholds ──
        guard_group = QGroupBox("Guard pragovi (R-7)")
        guard_layout = QFormLayout()

        self.kappa = QDoubleSpinBox()
        self._setup_spin(self.kappa, 0.0, 1.0, 0.05, DEFAULT_GUARDS["kappa"])
        guard_layout.addRow("κ (koherenca) ≥", self.kappa)

        self.chi = QDoubleSpinBox()
        self._setup_spin(self.chi, 0.0, 1.0, 0.05, DEFAULT_GUARDS["chi"])
        guard_layout.addRow("χ (jasnost) ≥", self.chi)

        self.mu_min = QDoubleSpinBox()
        self._setup_spin(self.mu_min, 0.0, 1.0, 0.05, DEFAULT_GUARDS["mu_min"])
        guard_layout.addRow("μ (delež vloge) min", self.mu_min)

        self.mu_max = QDoubleSpinBox()
        self._setup_spin(self.mu_max, 0.0, 1.0, 0.05, DEFAULT_GUARDS["mu_max"])
        guard_layout.addRow("μ (delež vloge) max", self.mu_max)

        self.real = QDoubleSpinBox()
        self._setup_spin(self.real, 0.0, 1.0, 0.01, DEFAULT_GUARDS["real"])
        guard_layout.addRow("ℜ (ostanek) ≤", self.real)

        self.beta_ne = QDoubleSpinBox()
        self._setup_spin(self.beta_ne, 0.0, 1.0, 0.05, DEFAULT_GUARDS["beta_ne"])
        guard_layout.addRow("β_NE (exit bridge) ≥", self.beta_ne)

        guard_group.setLayout(guard_layout)
        layout.addWidget(guard_group)

        # ── Defaults ──
        defaults_group = QGroupBox("Privzete vrednosti")
        defaults_layout = QFormLayout()

        self.default_theme = QComboBox()
        self.default_theme.addItems(["praznina (∅ Temno)", "ognjeno (∆ Ognjeno)", "tok (∮ Tok)"])
        defaults_layout.addRow("Tema:", self.default_theme)

        self.default_depth = QComboBox()
        self.default_depth.addItems([
            "1 — Površinski rez",
            "2 — Strukturni rez",
            "3 — Ontološki rez",
            "4 — Absolutni rez",
        ])
        defaults_layout.addRow("∂ Globina:", self.default_depth)

        defaults_group.setLayout(defaults_layout)
        layout.addWidget(defaults_group)

        # ── TONOS frequency toggles ──
        freq_group = QGroupBox("TONOS frekvence")
        freq_layout = QVBoxLayout()

        freq_info = QLabel("Vklopi/izklopi zvočno resonanco po fazah:")
        freq_layout.addWidget(freq_info)

        self.freq_checks = {}
        for key, label, hz in TONOS_PHASES:
            cb = QCheckBox(f"{label} — {hz} Hz")
            cb.setChecked(True)
            self.freq_checks[key] = cb
            freq_layout.addWidget(cb)

        freq_group.setLayout(freq_layout)
        layout.addWidget(freq_group)

        # ── Buttons ──
        btn_row = QHBoxLayout()
        self.btn_save = QPushButton("Shrani")
        self.btn_save.clicked.connect(self.on_save)
        btn_row.addWidget(self.btn_save)

        self.btn_reset = QPushButton("Ponastavi na privzeto")
        self.btn_reset.clicked.connect(self.on_reset)
        btn_row.addWidget(self.btn_reset)

        self.btn_close = QPushButton("Zapri")
        self.btn_close.clicked.connect(self.reject)
        btn_row.addWidget(self.btn_close)

        btn_row.addStretch()
        layout.addLayout(btn_row)

    def _setup_spin(self, spin, minv, maxv, step, default):
        spin.setRange(minv, maxv)
        spin.setSingleStep(step)
        spin.setDecimals(2)
        spin.setValue(default)

    def _load_settings(self):
        if get_settings is None or self.db is None:
            return
        try:
            s = get_settings(self.db)
            if "kappa" in s: self.kappa.setValue(float(s["kappa"]))
            if "chi" in s: self.chi.setValue(float(s["chi"]))
            if "mu_min" in s: self.mu_min.setValue(float(s["mu_min"]))
            if "mu_max" in s: self.mu_max.setValue(float(s["mu_max"]))
            if "real" in s: self.real.setValue(float(s["real"]))
            if "beta_ne" in s: self.beta_ne.setValue(float(s["beta_ne"]))
            if "theme" in s:
                idx = {"praznina": 0, "ognjeno": 1, "tok": 2}.get(s["theme"], 0)
                self.default_theme.setCurrentIndex(idx)
            if "depth" in s:
                self.default_depth.setCurrentIndex(int(s["depth"]) - 1)
            for key, cb in self.freq_checks.items():
                sk = f"freq_{key}"
                if sk in s:
                    cb.setChecked(s[sk] in ("true", "True", "1"))
        except Exception:
            pass

    def on_save(self):
        settings = {
            "kappa": str(self.kappa.value()),
            "chi": str(self.chi.value()),
            "mu_min": str(self.mu_min.value()),
            "mu_max": str(self.mu_max.value()),
            "real": str(self.real.value()),
            "beta_ne": str(self.beta_ne.value()),
            "theme": ["praznina", "ognjeno", "tok"][self.default_theme.currentIndex()],
            "depth": str(self.default_depth.currentIndex() + 1),
        }
        for key, cb in self.freq_checks.items():
            settings[f"freq_{key}"] = "true" if cb.isChecked() else "false"

        if set_settings is not None and self.db is not None:
            try:
                set_settings(self.db, settings)
            except Exception:
                pass
        self.accept()

    def on_reset(self):
        self.kappa.setValue(DEFAULT_GUARDS["kappa"])
        self.chi.setValue(DEFAULT_GUARDS["chi"])
        self.mu_min.setValue(DEFAULT_GUARDS["mu_min"])
        self.mu_max.setValue(DEFAULT_GUARDS["mu_max"])
        self.real.setValue(DEFAULT_GUARDS["real"])
        self.beta_ne.setValue(DEFAULT_GUARDS["beta_ne"])
        self.default_theme.setCurrentIndex(0)
        self.default_depth.setCurrentIndex(0)
        for cb in self.freq_checks.values():
            cb.setChecked(True)

    def get_guard_config(self) -> dict:
        """Return current guard thresholds as a config dict for the pipeline."""
        return {
            "kappa": self.kappa.value(),
            "chi": self.chi.value(),
            "mu_min": self.mu_min.value(),
            "mu_max": self.mu_max.value(),
            "real": self.real.value(),
            "beta_ne": self.beta_ne.value(),
        }

    def get_enabled_frequencies(self) -> dict:
        """Return {module_key: bool} for frequency enable/disable."""
        return {k: cb.isChecked() for k, cb in self.freq_checks.items()}
'''

# ═══════════════════════════════════════════════════════════════
# FILE 6: main_window_v3.py — fully integrated (v2 + Phase 3)
# ═══════════════════════════════════════════════════════════════

MAIN_WINDOW_V3 = '''"""
Main Window v3 — TAZV Comprehension Machine
=============================================
v2 + Phase 3 integration:
  - History search dialog (Prop IV)
  - CSV export (sessions + ledger)
  - Settings panel with guard thresholds (Prop IX)
  - Mutation tracking — shows what changed on reprocess (Prop X)
  - All v2 features preserved: 8 tabs, ∂ Globina, 3 themes, JSON/HTML export

Replaces main_window_v2.py. Back up v2 first:
  copy comprehension\\ui\\main_window_v2.py comprehension\\ui\\main_window_v2_backup.py
"""
import os
import json
from datetime import datetime
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTextEdit, QPushButton, QLabel, QStatusBar,
    QFileDialog, QComboBox, QMenu, QMessageBox, QDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QAction

from comprehension.core.processing_pipeline import ProcessingPipeline
from comprehension.core.symbol_mapper import SymbolMapper
from comprehension.core.module_semantics import MODULE_SEMANTICS, MODULE_ORDER
from comprehension.core.egyptian_color_semantics import MODULE_COLOR_HEX
from comprehension.core.themes import THEMES, generate_qss
from comprehension.core.exporter import export_json, export_html
from comprehension.ui.r7_progress import R7ProgressWidget
from comprehension.ui.module_window import ModuleWindow

try:
    from comprehension.ui.knowledge_renderer import KnowledgeRenderer
    HAS_INDEXER = True
except ImportError:
    HAS_INDEXER = False

try:
    from comprehension.data.database import Database
    HAS_DB = True
except ImportError:
    HAS_DB = False

try:
    from comprehension.data.db_queries import search_sessions, get_session_by_id, get_settings, set_settings
    HAS_QUERIES = True
except ImportError:
    HAS_QUERIES = False

try:
    from comprehension.core.csv_exporter import export_sessions_csv, export_ledger_csv, export_full_csv
    HAS_CSV = True
except ImportError:
    HAS_CSV = False

try:
    from comprehension.ui.history_search import HistorySearchDialog
    HAS_HISTORY = True
except ImportError:
    HAS_HISTORY = False

try:
    from comprehension.ui.settings_panel import SettingsDialog, DEFAULT_GUARDS
    HAS_SETTINGS = True
except ImportError:
    HAS_SETTINGS = False

try:
    from comprehension.core.mutation_tracker import MutationTracker
    HAS_MUTATION = True
except ImportError:
    HAS_MUTATION = False


def _get_db_path():
    """Try to locate the SQLite database file."""
    candidates = [
        os.path.join("comprehension", "data", "ta3v.db"),
        os.path.join("comprehension", "data", "tazv.db"),
        os.path.join("comprehension", "data", "comprehension.db"),
        "ta3v.db",
        "tazv.db",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    # Return the first candidate as default (will be created on first write)
    return candidates[0]


class PipelineWorker(QThread):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, statement, config=None):
        super().__init__()
        self.statement = statement
        self.config = config or {}

    def run(self):
        try:
            pipeline = ProcessingPipeline()
            result = pipeline.process(self.statement, self.config)
            result["statement"] = self.statement
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TAZV Comprehension Machine — v3")
        self.setGeometry(80, 80, 1280, 860)

        self.pipeline = ProcessingPipeline()
        self.mapper = SymbolMapper()
        self.current_theme = "praznina"
        self.current_depth = 1
        self.module_windows = {}
        self.last_result = None
        self.db = None
        self.db_path = _get_db_path()

        # Initialize database connection
        if HAS_DB:
            try:
                self.db = Database()
            except Exception:
                try:
                    import sqlite3
                    self.db = sqlite3.connect(self.db_path)
                except Exception:
                    self.db = None

        # Initialize mutation tracker
        self.mutation_tracker = MutationTracker(self.db) if HAS_MUTATION else None

        # Load settings
        self._load_saved_settings()

        self._apply_theme(self.current_theme)
        self._init_ui()
        self._init_menu()
        self._init_status()

    def _load_saved_settings(self):
        if not HAS_QUERIES or self.db is None:
            return
        try:
            s = get_settings(self.db)
            if "theme" in s:
                self.current_theme = s["theme"]
            if "depth" in s:
                self.current_depth = int(s["depth"])
        except Exception:
            pass

    def _apply_theme(self, name):
        self.current_theme = name
        self.setStyleSheet(generate_qss(name))

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # R-7 progress
        self.r7_progress = R7ProgressWidget()
        layout.addWidget(self.r7_progress)

        # Input
        self.input = QTextEdit()
        self.input.setPlaceholderText("Vnesi izrek / statement...")
        self.input.setMaximumHeight(80)
        layout.addWidget(self.input)

        # Process + Export buttons
        btn_row = QHBoxLayout()
        self.btn_process = QPushButton("∅ Izvedi R-7 cikel")
        self.btn_process.clicked.connect(self.on_process)
        btn_row.addWidget(self.btn_process)

        self.btn_json = QPushButton("JSON")
        self.btn_json.clicked.connect(self.on_export_json)
        btn_row.addWidget(self.btn_json)

        self.btn_html = QPushButton("HTML")
        self.btn_html.clicked.connect(self.on_export_html)
        btn_row.addWidget(self.btn_html)

        self.btn_csv = QPushButton("CSV")
        self.btn_csv.clicked.connect(self.on_export_csv)
        btn_row.addWidget(self.btn_csv)

        btn_row.addStretch()
        layout.addLayout(btn_row)

        # Tabs: 7 modules + Knowledge Indexer
        self.tabs = QTabWidget()
        labels = [
            "∅ BIOS", "¬ STATE", "∆ UAF",
            "1 JEWIK", "⧖ APD", "∮ MICRO", "⟡ VIS",
        ]
        for mod, label in zip(MODULE_ORDER, labels):
            w = ModuleWindow(mod)
            self.module_windows[mod] = w
            self.tabs.addTab(w, label)

        if HAS_INDEXER:
            self.indexer = KnowledgeRenderer()
            self.tabs.addTab(self.indexer, "Index")

        # Mutation tab (Prop X)
        self.mutation_display = QTextEdit()
        self.mutation_display.setReadOnly(True)
        self.mutation_display.setPlaceholderText(
            "Mutacije se pokažejo, ko isti izrek znova obdeluješ.\\n"
            "(Proposition X: škatla = mutable)"
        )
        self.tabs.addTab(self.mutation_display, "∂ Mutacije")

        layout.addWidget(self.tabs)

    def _init_menu(self):
        menubar = self.menuBar()

        # ── Datoteka ──
        file_menu = menubar.addMenu("Datoteka")
        file_menu.addAction("Izvozi JSON...", self.on_export_json)
        file_menu.addAction("Izvozi HTML...", self.on_export_html)
        if HAS_CSV:
            file_menu.addAction("Izvozi seje CSV...", self.on_export_sessions_csv)
            file_menu.addAction("Izvozi dnevnik CSV...", self.on_export_ledger_csv)
            file_menu.addAction("Izvozi vse CSV...", self.on_export_full_csv)
        file_menu.addSeparator()
        file_menu.addAction("Izhod", self.close)

        # ── ∂ Globina ──
        depth_menu = menubar.addMenu("∂ Globina")
        depths = [
            ("Nivo 1 — Površinski rez", 1),
            ("Nivo 2 — Strukturni rez", 2),
            ("Nivo 3 — Ontološki rez", 3),
            ("Nivo 4 — Absolutni rez", 4),
        ]
        self._depth_actions = []
        for label, level in depths:
            action = QAction(label, self, checkable=True)
            action.setChecked(level == self.current_depth)
            action.triggered.connect(lambda checked, lv=level: self._set_depth(lv))
            depth_menu.addAction(action)
            self._depth_actions.append((lv, action))

        # ── Tema ──
        theme_menu = menubar.addMenu("Tema")
        self._theme_actions = []
        for key, info in THEMES.items():
            action = QAction(info["name"], self, checkable=True)
            action.setChecked(key == self.current_theme)
            action.triggered.connect(lambda checked, k=key: self._switch_theme(k))
            theme_menu.addAction(action)
            self._theme_actions.append((k, action))

        # ── Zgodovina ──
        if HAS_HISTORY:
            history_menu = menubar.addMenu("Zgodovina")
            history_menu.addAction("Išči seje...", self.on_history_search)
            if self.mutation_tracker:
                history_menu.addAction("Pokaži mutacije...", self.on_show_mutations)

        # ── Nastavitve ──
        if HAS_SETTINGS:
            settings_menu = menubar.addMenu("Nastavitve")
            settings_menu.addAction("Guard pragovi, tema, TONOS...", self.on_settings)

        # ── Pomoč ──
        help_menu = menubar.addMenu("Pomoč")
        help_menu.addAction("R-7 protokol: ∅ → ¬ → ∆ → 1 → ⧖ → ∮ → ⟡")
        help_menu.addAction("TAZV ontologija")
        help_menu.addAction("O programu")

    def _set_depth(self, level):
        self.current_depth = level
        for lv, action in self._depth_actions:
            action.setChecked(lv == level)
        if hasattr(self, "indexer") and hasattr(self.indexer, "mandala"):
            try:
                self.indexer.mandala.set_depth(level)
            except Exception:
                pass
        self.statusBar().showMessage(f"∂ Globina: nivo {level}")

    def _switch_theme(self, key):
        self._apply_theme(key)
        for k, action in self._theme_actions:
            action.setChecked(k == key)
        self.statusBar().showMessage(f"Tema: {THEMES[key]['name']}")

    def _init_status(self):
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage(
            "Pripravljen. ∅ → ¬ → ∆ → 1 → ⧖ → ∮ → ⟡"
        )

    def on_process(self):
        statement = self.input.toPlainText().strip()
        if not statement:
            self.status.showMessage("Vnesi izrek.")
            return

        self.status.showMessage("Obdelujem...")
        self.btn_process.setEnabled(False)

        config = {"depth": self.current_depth}
        # Apply guard thresholds from settings
        if HAS_QUERIES and self.db is not None:
            try:
                s = get_settings(self.db)
                config["guards"] = {
                    "kappa": float(s.get("kappa", 0.70)),
                    "chi": float(s.get("chi", 0.40)),
                    "mu_min": float(s.get("mu_min", 0.50)),
                    "mu_max": float(s.get("mu_max", 0.80)),
                    "real": float(s.get("real", 0.03)),
                }
            except Exception:
                pass

        self.worker = PipelineWorker(statement, config)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_finished(self, result):
        self.btn_process.setEnabled(True)
        self.last_result = result
        phases = result.get("phases", {})

        for i, mod in enumerate(MODULE_ORDER):
            if mod in phases:
                self.module_windows[mod].update_result(phases[mod])
                self.r7_progress.set_phase(i)

        errors = result.get("errors", [])
        status = result.get("status", "unknown")
        self.status.showMessage(
            f"Status: {status} | Faze: {len(phases)}/7 | Napake: {len(errors)}"
        )

        # Log to SQLite
        if HAS_DB and self.db is not None:
            try:
                if hasattr(self.db, "log_session"):
                    self.db.log_session(result)
                elif hasattr(self.db, "execute"):
                    self.db.execute(
                        "INSERT INTO sessions (statement, result_json, status, created_at) VALUES (?, ?, ?, ?)",
                        (result.get("statement", ""), json.dumps(result, ensure_ascii=False, default=str),
                         status, datetime.now().isoformat()),
                    )
                    if hasattr(self.db, "commit"):
                        self.db.commit()
            except Exception:
                pass

        # Mutation tracking (Prop X)
        if self.mutation_tracker:
            try:
                diff = self.mutation_tracker.track_and_store(result, result.get("statement", ""))
                if diff:
                    html = self.mutation_tracker.format_diff_html(diff)
                    self.mutation_display.setHtml(html)
                    if diff.get("changed"):
                        self.status.showMessage(
                            f"Status: {status} | Mutacija zaznana: {diff.get('summary', '')}"
                        )
                else:
                    self.mutation_display.setPlainText("Brez predhodnih sej — prvi izrek.")
            except Exception:
                pass

    def on_error(self, msg):
        self.btn_process.setEnabled(True)
        self.status.showMessage(f"Napaka: {msg}")

    # ── Export handlers ──

    def on_export_json(self):
        if not self.last_result:
            self.status.showMessage("Najprej izvedi cikel.")
            return
        filepath, _ = QFileDialog.getSaveFileName(self, "Izvozi JSON", "", "JSON Files (*.json)")
        if filepath:
            export_json(self.last_result, filepath)
            self.status.showMessage(f"Izvoženo: {filepath}")

    def on_export_html(self):
        if not self.last_result:
            self.status.showMessage("Najprej izvedi cikel.")
            return
        filepath, _ = QFileDialog.getSaveFileName(self, "Izvozi HTML", "", "HTML Files (*.html)")
        if filepath:
            export_html(self.last_result, filepath)
            self.status.showMessage(f"Izvoženo: {filepath}")

    def on_export_csv(self):
        """Quick CSV export of current result's ledger."""
        if not HAS_CSV or self.db is None:
            self.status.showMessage("CSV ni na voljo.")
            return
        filepath, _ = QFileDialog.getSaveFileName(self, "Izvozi CSV", "", "CSV Files (*.csv)")
        if filepath:
            try:
                count = export_ledger_csv(self.db, filepath)
                self.status.showMessage(f"Izvoženo {count} vnosov: {filepath}")
            except Exception as e:
                self.status.showMessage(f"Napaka: {e}")

    def on_export_sessions_csv(self):
        if not HAS_CSV or self.db is None:
            return
        filepath, _ = QFileDialog.getSaveFileName(self, "Izvozi seje CSV", "", "CSV Files (*.csv)")
        if filepath:
            try:
                count = export_sessions_csv(self.db, filepath)
                QMessageBox.information(self, "Izvoz", f"Izvoženo {count} sej.")
            except Exception as e:
                QMessageBox.warning(self, "Napaka", str(e))

    def on_export_ledger_csv(self):
        if not HAS_CSV or self.db is None:
            return
        filepath, _ = QFileDialog.getSaveFileName(self, "Izvozi dnevnik CSV", "", "CSV Files (*.csv)")
        if filepath:
            try:
                count = export_ledger_csv(self.db, filepath)
                QMessageBox.information(self, "Izvoz", f"Izvoženo {count} vnosov.")
            except Exception as e:
                QMessageBox.warning(self, "Napaka", str(e))

    def on_export_full_csv(self):
        if not HAS_CSV or self.db is None:
            return
        filepath, _ = QFileDialog.getSaveFileName(self, "Izvozi vse CSV", "", "CSV Files (*.csv)")
        if filepath:
            try:
                count = export_full_csv(self.db, filepath)
                QMessageBox.information(self, "Izvoz", f"Izvoženo {count} sej + dnevnik.")
            except Exception as e:
                QMessageBox.warning(self, "Napaka", str(e))

    # ── History search ──

    def on_history_search(self):
        if not HAS_HISTORY or self.db is None:
            self.status.showMessage("Iskanje zgodovine ni na voljo.")
            return
        dialog = HistorySearchDialog(self.db, self)
        dialog.session_selected.connect(self._load_session)
        dialog.exec()

    def _load_session(self, session_id):
        """Load a past session into the display."""
        if not HAS_QUERIES or self.db is None:
            return
        try:
            session = get_session_by_id(self.db, session_id)
            if session:
                self.last_result = session.get("result_parsed") or {
                    "statement": session.get("statement", ""),
                    "status": session.get("status", ""),
                    "phases": {},
                    "errors": [e.get("message", "") for e in session.get("errors", [])],
                }
                # Update displays
                phases = self.last_result.get("phases", {})
                for mod in MODULE_ORDER:
                    if mod in phases:
                        self.module_windows[mod].update_result(phases[mod])
                self.status.showMessage(f"Naložena seja {session_id}: {session.get('statement', '')[:50]}")
        except Exception as e:
            self.status.showMessage(f"Napaka pri nalaganju: {e}")

    # ── Mutation display ──

    def on_show_mutations(self):
        if not self.mutation_tracker:
            return
        statement = self.input.toPlainText().strip()
        mutations = self.mutation_tracker.get_history(statement or None)
        if not mutations:
            self.mutation_display.setPlainText("Brez zabeleženih mutacij.")
            return
        parts = ["<h2>Zgodovina mutacij</h2>"]
        for m in mutations:
            diff = m.get("diff_parsed", {})
            parts.append(f"<hr><p><b>{m.get('created_at', '')[:19]}</b> — {diff.get('summary', '')}</p>")
            if diff.get("phase_changes"):
                parts.append("<ul>")
                for phase, change in diff["phase_changes"].items():
                    parts.append(f"<li><b>{phase}</b>: sprememba zaznana</li>")
                parts.append("</ul>")
        self.mutation_display.setHtml("\\n".join(parts))
        self.tabs.setCurrentWidget(self.mutation_display)

    # ── Settings ──

    def on_settings(self):
        if not HAS_SETTINGS:
            self.status.showMessage("Nastavitve ni na voljo.")
            return
        dialog = SettingsDialog(self.db, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Apply theme + depth from settings
            theme_idx = dialog.default_theme.currentIndex()
            self._switch_theme(["praznina", "ognjeno", "tok"][theme_idx])
            depth_idx = dialog.default_depth.currentIndex() + 1
            self._set_depth(depth_idx)
            self.status.showMessage("Nastavitve shranjene.")
'''

# ═══════════════════════════════════════════════════════════════
# FILE 7: build_exe.py — Phase 4 PyInstaller build launcher
# ═══════════════════════════════════════════════════════════════

BUILD_EXE_PY = '''#!/usr/bin/env python3
"""
TAZV Comprehension Machine — Phase 4: Build .exe
==================================================
Builds a standalone Windows .exe using PyInstaller.

Prerequisites:
  pip install pyinstaller PyQt6

Usage:
  python build_exe.py

Output:
  dist/TAZV/TAZV.exe  (standalone, includes all dependencies)

Corpus principle: "Izdelek je ∮ — vrnitev v uporabo"
  The build is the return — the system returns to the world as executable.
"""
import subprocess
import sys
import os
import shutil

def check_pyinstaller():
    try:
        import PyInstaller
        print(f"  PyInstaller {PyInstaller.__version__} najden.")
        return True
    except ImportError:
        print("  PyInstaller ni nameščen. Nameščam...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        return True

def clean_build():
    """Remove previous build artifacts."""
    for d in ["build", "dist", "__pycache__"]:
        if os.path.exists(d):
            shutil.rmtree(d)
            print(f"  Počiščeno: {d}/")

def build():
    print("=" * 60)
    print("TAZV Comprehension Machine — Build .exe")
    print("=" * 60)
    print()

    check_pyinstaller()

    spec_file = "ta3v.spec"
    if not os.path.exists(spec_file):
        print(f"  NAPAKA: {spec_file} ne obstaja.")
        sys.exit(1)

    print("  Čistim prejšnji build...")
    clean_build()

    print("  Gradim .exe...")
    result = subprocess.run(
        [sys.executable, "-m", "PyInstaller", spec_file, "--clean", "--noconfirm"],
        check=False,
    )

    if result.returncode == 0:
        exe_path = os.path.join("dist", "TAZV", "TAZV.exe")
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print()
            print(f"  BUILD USPEŠEN!")
            print(f"  .exe: {exe_path}")
            print(f"  Velikost: {size_mb:.1f} MB")
        else:
            print("  Build končan, vendar .exe ni najden v dist/TAZV/")
    else:
        print(f"  BUILD NEUSPEŠEN (exit code {result.returncode})")

    print()
    print("  Opomba: dist/TAZV/ je samostojna mapa — kopiraj celotno mapo.")
    print("  Za distribucijo: zip dist/TAZV/ → TAZV.zip")

if __name__ == "__main__":
    build()
'''

# ═══════════════════════════════════════════════════════════════
# FILE 8: ta3v.spec — PyInstaller spec
# ═══════════════════════════════════════════════════════════════

TA3V_SPEC = '''# -*- mode: python ; coding: utf-8 -*-
"""
TAZV Comprehension Machine — PyInstaller Spec
================================================
Builds a standalone .exe with all data files bundled.

  pyinstaller ta3v.spec --clean --noconfirm
"""
import os

block_cipher = None

# Data files to bundle
datas = [
    ('comprehension/data/schema.sql', 'comprehension/data'),
    ('ta3v_colors.qss', '.'),
]

# Add any .qss files if they exist
for qss in ['ta3v_colors.qss']:
    if os.path.exists(qss):
        datas.append((qss, '.'))

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.QtSvg',
        'PyQt6.QtSvgWidgets',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'test',
        'unittest',
        'pydoc',
        'doctest',
        'argparse',
        'difflib',
        'pdb',
        'profile',
        'pstats',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='TAZV',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add: 'ta3v.ico' if you have an icon
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TAZV',
)
'''

# ═══════════════════════════════════════════════════════════════
# SCHEMA PATCH — mutations table
# ═══════════════════════════════════════════════════════════════

SCHEMA_MUTATION = """
-- Mutation tracking (Proposition X: škatla = mutable)
CREATE TABLE IF NOT EXISTS mutations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    old_session_id INTEGER,
    new_session_id INTEGER,
    statement TEXT,
    diff_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(old_session_id) REFERENCES sessions(id),
    FOREIGN KEY(new_session_id) REFERENCES sessions(id)
);
"""

# ═══════════════════════════════════════════════════════════════
# WRITE FILES
# ═══════════════════════════════════════════════════════════════

files = {
    "comprehension/data/db_queries.py": DB_QUERIES_PY,
    "comprehension/core/csv_exporter.py": CSV_EXPORTER_PY,
    "comprehension/core/mutation_tracker.py": MUTATION_TRACKER_PY,
    "comprehension/ui/history_search.py": HISTORY_SEARCH_PY,
    "comprehension/ui/settings_panel.py": SETTINGS_PANEL_PY,
    "comprehension/ui/main_window_v3.py": MAIN_WINDOW_V3,
    "build_exe.py": BUILD_EXE_PY,
    "ta3v.spec": TA3V_SPEC,
}

print("=" * 60)
print("TAZV Phase 3 + Phase 4 — Bootstrap")
print("=" * 60)
print()

for relpath, content in files.items():
    fullpath = os.path.join(BASE, relpath)
    dirpath = os.path.dirname(fullpath)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(fullpath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    size = os.path.getsize(fullpath)
    print(f"  OK  {relpath}  ({size} bytes)")

# Patch schema
schema_path = os.path.join(BASE, "comprehension/data/schema.sql")
if os.path.exists(schema_path):
    with open(schema_path, "r", encoding="utf-8") as f:
        existing = f.read()
    if "mutations" not in existing:
        with open(schema_path, "a", encoding="utf-8") as f:
            f.write(SCHEMA_MUTATION)
        print(f"  OK  schema.sql (appended mutations table)")
    else:
        print(f"  SKIP schema.sql (mutations table exists)")
else:
    os.makedirs(os.path.dirname(schema_path), exist_ok=True)
    with open(schema_path, "w", encoding="utf-8") as f:
        f.write(SCHEMA_MUTATION)
    print(f"  OK  schema.sql (new)")

print()
print("Phase 3 features:")
print("  3A. History search UI — search past sessions by text/date/status/error")
print("  3B. CSV export — sessions, ledger, or full interleaved export")
print("  3C. Settings panel — guard thresholds, defaults, TONOS toggles")
print("  3D. Mutation tracking — diff between reprocessed statements (Prop X)")
print()
print("Phase 4 features:")
print("  - build_exe.py — PyInstaller build launcher")
print("  - ta3v.spec — PyInstaller spec with data files bundled")
print()
print("Propositions enacted:")
print("  Prop IX  (traveling module) — settings adjust guard thresholds per session")
print("  Prop X   (škatla = mutable) — mutation tracker compares reprocessed statements")
print("  Prop IV  (identity diff)    — history search shows session evolution")
print("  Prop VI/XIV (word as precond.) — depth 4 (absolutni rez) configurable as default")
print()
print("To activate:")
print("  1. cd comprehension_machine")
print("  2. copy comprehension\\ui\\main_window_v2.py comprehension\\ui\\main_window_v2_backup.py")
print("  3. copy comprehension\\ui\\main_window_v3.py comprehension\\ui\\main_window.py")
print("  4. python main.py")
print()
print("  Verify:")
print("    - Menu bar: Datoteka, ∂ Globina, Tema, Zgodovina, Nastavitve, Pomoč")
print("    - CSV button in toolbar")
print("    - ∂ Mutacije tab (9th tab)")
print("    - History search dialog (Zgodovina → Išči seje...)")
print("    - Settings dialog (Nastavitve → Guard pragovi...)")
print()
print("To build .exe (Phase 4):")
print("  1. pip install pyinstaller")
print("  2. python build_exe.py")
print("  3. Check dist/TAZV/TAZV.exe")
print()
print("Next ∂:")
print("  Phase 4+ propositions still open:")
print("    Prop VIII  (stiska engine) — distress mode")
print("    Prop XI    (ONTOBOG) — failed cycles → new tradition mappings")
print("    Prop XII   (manjko 4 layers) — BIOS sub-layers")
print("    Prop XV-XXI (dormant) — unexplored")