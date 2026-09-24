PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY, name TEXT NOT NULL, created_at TEXT NOT NULL, config_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS ledger (
    id TEXT PRIMARY KEY, session_id TEXT NOT NULL, statement TEXT NOT NULL,
    module TEXT NOT NULL, phase TEXT NOT NULL, data_json TEXT, kpi_json TEXT,
    status TEXT NOT NULL DEFAULT 'completed', duration_ms REAL DEFAULT 0, timestamp TEXT NOT NULL,
    FOREIGN KEY(session_id) REFERENCES sessions(id)
);
CREATE TABLE IF NOT EXISTS errors (
    id TEXT PRIMARY KEY, session_id TEXT, module TEXT NOT NULL, phase TEXT,
    error_text TEXT NOT NULL, traceback TEXT, severity TEXT NOT NULL DEFAULT 'error', timestamp TEXT NOT NULL,
    FOREIGN KEY(session_id) REFERENCES sessions(id)
);
CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS schema_version (version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL);
INSERT OR IGNORE INTO schema_version (version, applied_at) VALUES (1, datetime('now'));
CREATE INDEX IF NOT EXISTS idx_ledger_session ON ledger(session_id);
CREATE INDEX IF NOT EXISTS idx_ledger_statement ON ledger(statement);
CREATE INDEX IF NOT EXISTS idx_ledger_module ON ledger(module);
CREATE INDEX IF NOT EXISTS idx_ledger_phase ON ledger(phase);
CREATE INDEX IF NOT EXISTS idx_ledger_timestamp ON ledger(timestamp);
CREATE INDEX IF NOT EXISTS idx_errors_session ON errors(session_id);
CREATE INDEX IF NOT EXISTS idx_errors_module ON errors(module);
CREATE INDEX IF NOT EXISTS idx_errors_timestamp ON errors(timestamp);

-- ═══════════════════════════════════════════════════════════════
-- KNOWLEDGE INDEX TABLES (Phase 2 addition)
-- Extends existing schema with tradition mapping storage
-- ═══════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS traditions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    element_count INTEGER,
    ring INTEGER DEFAULT 1,
    corpus_source TEXT,
    added_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tradition_mappings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tradition_id INTEGER NOT NULL,
    native_term TEXT NOT NULL,
    root_operator TEXT NOT NULL,
    math_property TEXT,
    FOREIGN KEY(tradition_id) REFERENCES traditions(id)
);

CREATE TABLE IF NOT EXISTS tonos_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    glyph TEXT NOT NULL,
    frequency REAL,
    note TEXT,
    played_at TEXT NOT NULL,
    FOREIGN KEY(session_id) REFERENCES sessions(id)
);

-- ═══════════════════════════════════════════════════════════════
-- PREVERBA TABLES (iz korpusa: topic_15, Obs1)
-- "dokazna sled" — append-only dnevnik
-- ═══════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS proof_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id TEXT UNIQUE,
    modul TEXT NOT NULL,
    statement TEXT NOT NULL,
    phase TEXT NOT NULL,
    result TEXT NOT NULL,
    soma TEXT,
    dokaz TEXT,
    doctrinarium TEXT,
    trainarium TEXT,
    kanon_status TEXT DEFAULT 'KANDIDAT',
    timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ring INTEGER DEFAULT 1
);

CREATE INDEX IF NOT EXISTS idx_proof_log_test_id ON proof_log(test_id);
CREATE INDEX IF NOT EXISTS idx_proof_log_modul ON proof_log(modul);
CREATE INDEX IF NOT EXISTS idx_proof_log_statement ON proof_log(statement);
CREATE INDEX IF NOT EXISTS idx_proof_log_phase ON proof_log(phase);
CREATE INDEX IF NOT EXISTS idx_proof_log_timestamp ON proof_log(timestamp);
CREATE INDEX IF NOT EXISTS idx_proof_log_kanon_status ON proof_log(kanon_status);

-- TRAINARIUM TABLES
-- "Drill, ki sistem trenira, da se izogne poti neuspeha naslednjič"

CREATE TABLE IF NOT EXISTS trainarium_drills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    drill_id TEXT UNIQUE NOT NULL,
    test_id TEXT NOT NULL,
    modul TEXT NOT NULL,
    statement TEXT NOT NULL,
    sikanje TEXT NOT NULL,
    fail_reason TEXT NOT NULL,
    fail_type TEXT NOT NULL,
    beseda TEXT NOT NULL,
    stavek TEXT NOT NULL,
    dejanje TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'ACTIVE',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TEXT,
    applied_count INTEGER DEFAULT 0,
    success_count INTEGER DEFAULT 0,
    ring INTEGER DEFAULT 1,
    priority TEXT DEFAULT 'S2'
);

CREATE INDEX IF NOT EXISTS idx_drills_drill_id ON trainarium_drills(drill_id);
CREATE INDEX IF NOT EXISTS idx_drills_modul ON trainarium_drills(modul);
CREATE INDEX IF NOT EXISTS idx_drills_status ON trainarium_drills(status);
CREATE INDEX IF NOT EXISTS idx_drills_created_at ON trainarium_drills(created_at);

-- KADENCA TABLES
-- "Ritem, ne tišina. Fraktalni R-7"

CREATE TABLE IF NOT EXISTS kadenca_state (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skala TEXT NOT NULL,
    current_phase TEXT NOT NULL,
    step_count INTEGER DEFAULT 0,
    cycle_count INTEGER DEFAULT 0,
    last_cycle_time TEXT,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_kadenca_skala ON kadenca_state(skala);

-- POSODOBITEV VERZIJE SHEME
INSERT OR IGNORE INTO schema_version (version, applied_at) VALUES (2, datetime('now'));
