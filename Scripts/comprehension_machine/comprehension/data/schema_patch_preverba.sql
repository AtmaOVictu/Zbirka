-- TAZV Preverba — SQL patch (dodaj k schema.sql)

CREATE TABLE IF NOT EXISTS proof_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id TEXT UNIQUE,
    modul TEXT NOT NULL,
    statement TEXT NOT NULL,
    phase TEXT NOT NULL,
    result TEXT NOT NULL,
    ego_flag INTEGER DEFAULT 0,
    soma TEXT,
    dokaz TEXT,
    seriousness TEXT DEFAULT 'S1',
    kanon_status TEXT DEFAULT 'KANDIDAT',
    rezultati_5 TEXT,
    rezultati_aj TEXT,
    kriteriji TEXT,
    doctrinarium_id TEXT,
    trainarium_id TEXT,
    ring INTEGER DEFAULT 1,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS kanon_entry (
    id TEXT PRIMARY KEY,
    modul TEXT NOT NULL,
    statement TEXT NOT NULL,
    status TEXT DEFAULT 'KANDIDAT',
    dokaz_nivo TEXT,
    soma_status TEXT,
    ring INTEGER DEFAULT 1,
    zgodovina TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS doctrinarium_log (
    id TEXT PRIMARY KEY,
    tip TEXT NOT NULL,
    parent_id TEXT,
    modul TEXT,
    trditev TEXT,
    rezultat TEXT,
    podrobnosti TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cadence_log (
    id TEXT PRIMARY KEY,
    tip TEXT NOT NULL,
    modul TEXT,
    operacija TEXT,
    rezultat TEXT,
    faza_glyph TEXT,
    dan_v_ciklu INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_proof_modul ON proof_log(modul);
CREATE INDEX IF NOT EXISTS idx_proof_result ON proof_log(result);
CREATE INDEX IF NOT EXISTS idx_kanon_status ON kanon_entry(status);
CREATE INDEX IF NOT EXISTS idx_doctrinarium_tip ON doctrinarium_log(tip);
