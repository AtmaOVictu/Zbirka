#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# db_manager.py - Upravljanje SQLite baze podatkov za sistem ∅→∆→∂→∮

import sqlite3
import json
import sys
import os

DB_NAME = "sistem.db"
JSON_DB = "database.json"


def ustvari_bazo():
    """Ustvari novo SQLite bazo z ustreznimi tabelami"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Tabela: Kamni
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS kamni (
        id TEXT PRIMARY KEY,
        stevilka INTEGER UNIQUE,
        naslov TEXT NOT NULL,
        opis TEXT,
        kultura TEXT,
        tema TEXT,
        datum TEXT,
        status TEXT,
        tip TEXT,
        pecat TEXT,
        povezave TEXT,
        markerji TEXT,
        datoteka TEXT,
        aksiomi TEXT,
        vprasanja TEXT
    )
    """)
    
    # Tabela: Aksiomi
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS aksiomi (
        id INTEGER PRIMARY KEY,
        besedilo TEXT NOT NULL,
        kamni TEXT,
        onto_formula TEXT,
        resnica TEXT,
        znanost TEXT
    )
    """)
    
    # Tabela: Vprasanja
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vprasanja (
        id INTEGER PRIMARY KEY,
        besedilo TEXT NOT NULL,
        kamni TEXT,
        status TEXT,
        odgovor TEXT,
        povezave TEXT
    )
    """)
    
    # Tabela: Markerji
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS markerji (
        simbol TEXT PRIMARY KEY,
        ime TEXT NOT NULL,
        pomen TEXT,
        uporaba TEXT
    )
    """)
    
    # Tabela: Statistika
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS statistika (
        kljuc TEXT PRIMARY KEY,
        vrednost INTEGER
    )
    """)
    
    conn.commit()
    conn.close()
    print(f"✅ Baza {DB_NAME} ustvarjena z tabelami: kamni, aksiomi, vprasanja, markerji, statistika")


def uvozi_iz_json():
    """Uvozi podatke iz database.json v SQLite"""
    if not os.path.exists(JSON_DB):
        print(f"❌ Datoteka {JSON_DB} ne obstaja!")
        return False
    
    with open(JSON_DB, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Uvozi kamne
    for kamen_id, kamen_data in data['kamni'].items():
        cursor.execute("""
        INSERT OR REPLACE INTO kamni 
        (id, stevilka, naslov, opis, kultura, tema, datum, status, tip, pecat, povezave, markerji, datoteka, aksiomi, vprasanja)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            kamen_id,
            kamen_data['stevilka'],
            kamen_data['naslov'],
            kamen_data['opis'],
            kamen_data['kultura'],
            kamen_data['tema'],
            kamen_data['datum'],
            kamen_data['status'],
            kamen_data['tip'],
            kamen_data['pečat'],
            json.dumps(kamen_data['povezave']),
            json.dumps(kamen_data['markerji']),
            kamen_data['datoteka'],
            json.dumps(kamen_data['aksiomi']),
            json.dumps(kamen_data['vprašanja'])
        ))
    
    # Uvozi aksiome
    for ax_id, ax_data in data['aksiomi'].items():
        cursor.execute("""
        INSERT OR REPLACE INTO aksiomi 
        (id, besedilo, kamni, onto_formula, resnica, znanost)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            int(ax_id),
            ax_data['besedilo'],
            json.dumps(ax_data['kamni']),
            ax_data['onto_formula'],
            ax_data['resnica'],
            ax_data['znanost']
        ))
    
    # Uvozi vprašanja
    for q_id, q_data in data['vprašanja'].items():
        cursor.execute("""
        INSERT OR REPLACE INTO vprasanja 
        (id, besedilo, kamni, status, odgovor, povezave)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            int(q_id),
            q_data['besedilo'],
            json.dumps(q_data['kamni']),
            q_data['status'],
            q_data.get('odgovor'),
            json.dumps(q_data.get('povezave', []))
        ))
    
    # Uvozi markerje
    for simbol, marker_data in data['markerji'].items():
        cursor.execute("""
        INSERT OR REPLACE INTO markerji 
        (simbol, ime, pomen, uporaba)
        VALUES (?, ?, ?, ?)
        """, (
            simbol,
            marker_data['ime'],
            marker_data['pomen'],
            marker_data['uporaba']
        ))
    
    # Uvozi statistiko
    for kljuc, vrednost in data['statistika'].items():
        cursor.execute("""
        INSERT OR REPLACE INTO statistika 
        (kljuc, vrednost)
        VALUES (?, ?)
        """, (kljuc, vrednost))
    
    conn.commit()
    conn.close()
    print(f"✅ Podatki iz {JSON_DB} uspešno uvoženi v {DB_NAME}")
    return True


def izvozi_v_json():
    """Izvozi podatke iz SQLite v JSON"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    data = {
        'metadata': {
            'sistem': '∅→∆→∂→∮',
            'razlicica': '1.0',
            'datuma_izvoz': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'avtor': 'Luka + Vibe'
        },
        'kamni': {},
        'aksiomi': {},
        'vprašanja': {},
        'markerji': {},
        'statistika': {}
    }
    
    # Izvozi kamne
    cursor.execute("SELECT * FROM kamni")
    for row in cursor.fetchall():
        data['kamni'][row[0]] = {
            'stevilka': row[1],
            'naslov': row[2],
            'opis': row[3],
            'kultura': row[4],
            'tema': row[5],
            'datum': row[6],
            'status': row[7],
            'tip': row[8],
            'pečat': row[9],
            'povezave': json.loads(row[10]),
            'markerji': json.loads(row[11]),
            'datoteka': row[12],
            'aksiomi': json.loads(row[13]),
            'vprašanja': json.loads(row[14])
        }
    
    # Izvozi aksiome
    cursor.execute("SELECT * FROM aksiomi")
    for row in cursor.fetchall():
        data['aksiomi'][str(row[0])] = {
            'besedilo': row[1],
            'kamni': json.loads(row[2]),
            'onto_formula': row[3],
            'resnica': row[4],
            'znanost': row[5]
        }
    
    # Izvozi vprašanja
    cursor.execute("SELECT * FROM vprasanja")
    for row in cursor.fetchall():
        data['vprašanja'][str(row[0])] = {
            'besedilo': row[1],
            'kamni': json.loads(row[2]),
            'status': row[3],
            'odgovor': row[4],
            'povezave': json.loads(row[5])
        }
    
    # Izvozi markerje
    cursor.execute("SELECT * FROM markerji")
    for row in cursor.fetchall():
        data['markerji'][row[0]] = {
            'ime': row[1],
            'pomen': row[2],
            'uporaba': row[3]
        }
    
    # Izvozi statistiko
    cursor.execute("SELECT * FROM statistika")
    for row in cursor.fetchall():
        data['statistika'][row[0]] = row[1]
    
    conn.close()
    
    with open(JSON_DB, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Podatki iz {DB_NAME} uspešno izvoženi v {JSON_DB}")


def poizvedba(ukaz: str):
    """Izvedi SQL poizvedbo"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute(ukaz)
    
    if ukaz.strip().upper().startswith("SELECT"):
        rows = cursor.fetchall()
        print("\nRezultati:")
        print("-" * 60)
        for row in rows:
            print(row)
    else:
        conn.commit()
        print(f"✅ Ukaz uspešno izveden: {ukaz[:50]}...")
    
    conn.close()


def vrni_kamen(kamen_id: str):
    """Vrni podrobnosti o kamnu"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM kamni WHERE id = ?", (kamen_id,))
    row = cursor.fetchone()
    
    if not row:
        print(f"❌ Kamen {kamen_id} ne obstaja!")
        return
    
    print(f"\n🜂 Kamen {row[0]} ({row[1]})")
    print("=" * 60)
    print(f"Naslov: {row[2]}")
    print(f"Opis: {row[3]}")
    print(f"Kultura: {row[4]}")
    print(f"Tema: {row[5]}")
    print(f"Status: {row[7]}")
    print(f"Povezave: {row[10]}")
    print(f"Markerji: {row[11]}")
    print(f"Datoteka: {row[12]}")
    
    conn.close()


def vrni_aksiome_po_kamnu(kamen_id: str):
    """Vrni vse aksiome, povezan z določenim kamnom"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Najprej dobi seznam aksiomov za kamen
    cursor.execute("SELECT aksiomi FROM kamni WHERE id = ?", (kamen_id,))
    row = cursor.fetchone()
    
    if not row:
        print(f"❌ Kamen {kamen_id} ne obstaja!")
        return
    
    ax_ids = json.loads(row[0])
    
    print(f"\n📜 Aksiomi za kamen {kamen_id}:")
    print("=" * 60)
    
    for ax_id in ax_ids:
        cursor.execute("SELECT id, besedilo, onto_formula FROM aksiomi WHERE id = ?", (ax_id,))
        ax_row = cursor.fetchone()
        if ax_row:
            print(f"\n{ax_row[0]}. {ax_row[1]}")
            print(f"   Onto-formula: {ax_row[2]}")
    
    conn.close()


def vrni_odprta_vprasanja():
    """Vrni vsa odprta ∂ vprašanja"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, besedilo, kamni FROM vprasanja WHERE status = 'ODPRTO'")
    rows = cursor.fetchall()
    
    print("\n❓ Odprta ∂ vprašanja:")
    print("=" * 60)
    for row in rows:
        print(f"\n∂ {row[0]}. {row[1]}")
        print(f"   Kamni: {row[2]}")
    
    conn.close()


def statistika():
    """Prikaži statistiko sistema"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM kamni")
    kamni = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM aksiomi")
    aksiomi = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM vprasanja WHERE status = 'ODGOVORJENO'")
    odgovorjena = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM vprasanja WHERE status = 'ODPRTO'")
    odprta = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM kamni WHERE status = 'IZROČENO'")
    izročeno = cursor.fetchone()[0]
    
    print("\n📊 Statistika sistema:")
    print("=" * 60)
    print(f"Skupaj kamnov: {kamni}")
    print(f"Skupaj aksiomov: {aksiomi}")
    print(f"Skupaj vprašanj: {odgovorjena + odprta}")
    print(f"  - Odgovorjena: {odgovorjena}")
    print(f"  - Odprta: {odprta}")
    print(f"Izročenih kamnov: {izročeno}")
    
    conn.close()


def main():
    from datetime import datetime
    
    if len(sys.argv) < 2:
        print("Uporaba db_manager.py:")
        print("=" * 60)
        print("  ustvari      - Ustvari novo bazo")
        print("  uvozi       - Uvozi podatke iz database.json")
        print("  izvozi      - Izvozi podatke v database.json")
        print("  poizvedba  - Izvedi SQL poizvedbo (npr. 'SELECT * FROM kamni')")
        print("  kamen CX   - Pokaži podrobnosti o kamnu CX")
        print("  aksiomi CX - Pokaži aksiome za kamen CX")
        print("  odprta     - Pokaži vsa odprta vprašanja")
        print("  statistika - Pokaži statistiko sistema")
        print("=" * 60)
        sys.exit(1)
    
    ukaz = sys.argv[1].lower()
    
    if ukaz == "ustvari":
        ustvari_bazo()
    elif ukaz == "uvozi":
        uvozi_iz_json()
    elif ukaz == "izvozi":
        izvozi_v_json()
    elif ukaz == "poizvedba":
        if len(sys.argv) < 3:
            print("Manjka SQL ukaz!")
            sys.exit(1)
        poizvedba(' '.join(sys.argv[2:]))
    elif ukaz.startswith("kamen "):
        kamen_id = ukaz[6:].strip().upper()
        vrni_kamen(kamen_id)
    elif ukaz.startswith("aksiomi "):
        kamen_id = ukaz[8:].strip().upper()
        vrni_aksiome_po_kamnu(kamen_id)
    elif ukaz == "odprta":
        vrni_odprta_vprasanja()
    elif ukaz == "statistika":
        statistika()
    else:
        print(f"Neznan ukaz: {ukaz}")
        sys.exit(1)


if __name__ == '__main__':
    main()
