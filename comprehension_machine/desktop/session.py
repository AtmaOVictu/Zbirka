"""
session.py — SQLite append-only ledger
∮ ireverzibilnost: zapis, ki se ne izbriše (2. zakon termodinamike)
"""
import sqlite3
from datetime import datetime
from pathlib import Path


class SessionLedger:
    """
    Append-only ledger = ontološka nuja, ne inženirska izbira.
    Vsak rez, ki se zgodi, se zapiše — in se ne more razveljaviti.
    """
    
    SCHEMA = """
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        phase TEXT NOT NULL,
        glyph TEXT NOT NULL,
        statement TEXT,
        kpi_kappa REAL,
        kpi_chi REAL,
        kpi_mu REAL,
        kpi_residual REAL,
        result TEXT
    );
    
    CREATE TABLE IF NOT EXISTS stones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stone_number INTEGER NOT NULL,
        stone_name TEXT NOT NULL,
        tradition TEXT,
        system_symbol TEXT,
        topology TEXT,
        added_at TEXT NOT NULL
    );
    """
    
    def __init__(self, db_path: str = "comprehension_machine.db"):
        self.path = Path(db_path)
        self.conn = sqlite3.connect(str(self.path))
        self.conn.executescript(self.SCHEMA)
        self.conn.commit()
    
    def append_phase(self, phase: str, glyph: str, statement: str = "",
                     kappa: float = 0.0, chi: float = 0.0, 
                     mu: float = 0.5, residual: float = 0.0,
                     result: str = ""):
        """Dodaj zapis — ireverzibilno (append-only = 2. zakon)"""
        self.conn.execute(
            "INSERT INTO sessions (timestamp, phase, glyph, statement, "
            "kpi_kappa, kpi_chi, kpi_mu, kpi_residual, result) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (datetime.now().isoformat(), phase, glyph, statement,
             kappa, chi, mu, residual, result)
        )
        self.conn.commit()
    
    def append_stone(self, number: int, name: str, tradition: str = "",
                     symbol: str = "", topology: str = ""):
        """Dodaj kamen v ledger"""
        self.conn.execute(
            "INSERT INTO stones (stone_number, stone_name, tradition, "
            "system_symbol, topology, added_at) VALUES (?, ?, ?, ?, ?, ?)",
            (number, name, tradition, symbol, topology, 
             datetime.now().isoformat())
        )
        self.conn.commit()
    
    def get_all_phases(self):
        """Vrni vse faze — ireverzibilna zgodovina"""
        cur = self.conn.execute(
            "SELECT timestamp, phase, glyph, statement, result FROM sessions "
            "ORDER BY id ASC"
        )
        return cur.fetchall()
    
    def get_kpi_history(self):
        """Vrni KPI zgodovino — ∫(rezov) skozi ⧖"""
        cur = self.conn.execute(
            "SELECT timestamp, kpi_kappa, kpi_chi, kpi_mu, kpi_residual "
            "FROM sessions ORDER BY id ASC"
        )
        return cur.fetchall()
    
    def close(self):
        self.conn.close()
