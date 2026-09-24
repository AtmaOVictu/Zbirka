#!/usr/bin/env python3
"""
Indexer za sistem ∅→∆→∂→∮
Avtomatsko indeksiranje in iskanje v vseh dokumentih
"""

import os
import re
import json
import sqlite3
from pathlib import Path
from collections import defaultdict

# Konfiguracija
PROJECT_DIR = Path(__file__).parent
INDEX_FILE = PROJECT_DIR / "index.json"
INDEX_DB = PROJECT_DIR / "index.db"


def extract_keywords(text):
    """Izvleči ključne besede iz besedila"""
    # Markerji
    markers = [
        r'∅', r'∆', r'∂', r'∮', r'⧖',
        r'∅↑', r'∅↓', r'∆→', r'∂↔', r'∮∞'
    ]
    
    # Najdi vse markerje
    found_markers = set()
    for marker in markers:
        if re.search(marker, text):
            found_markers.add(marker)
    
    # matematični simbole
    math_symbols = set(re.findall(r'\$[^\$]+\$', text))
    
    # Kamni (CXI, CXII, itd.)
    stones = set(re.findall(r'\bC[A-Z]{1,3}?\d{1,3}\b', text))
    
    # Aksiomi (236-265+)
    aksiomi = set(re.findall(r'\b\d{3,4}\b', text))
    
    # ∂ vprašanja
    vprašanja = set(re.findall(r'∂\s*\d+', text))
    
    return {
        'markerji': list(found_markers),
        'matematika': list(math_symbols),
        'kamni': list(stones),
        'aksiomi': list(aksiomi),
        'vprašanja': list(vprašanja)
    }


def index_file(filepath):
    """Indeksiraj eno datoteko"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    filename = filepath.name
    
    # Izvleči osnovne podatke
    title_match = re.search(r'^#\s+(.+)', content)
    title = title_match.group(1).strip() if title_match else filename
    
    # Izvleči aksiome
    aksiom_matches = re.finditer(r'\|\s*(\d{3,4})\s*\|', content)
    aksiomi = [m.group(1) for m in aksiom_matches]
    
    # Izvleči ∂ vprašanja
    vprašanje_matches = re.finditer(r'(?:∂|vprašanju)\s*(\d{1,3})', content)
    vprašanja = [m.group(1) for m in vprašanje_matches]
    
    # Izvleči kamne
    stone_matches = re.finditer(r'(C[A-Z]+\d{1,3})', content)
    kamni = list(set(m.group(1) for m in stone_matches))
    
    # Izvleči markerje
    marker_matches = re.finditer(r'(∅|∆|∂|∮|⧖|∅↑|∅↓|∆→|∂↔|∮∞)', content)
    markerji = list(set(m.group(1) for m in marker_matches))
    
    # Izvleči ključne koncepte
    concepts = re.findall(r'\*\*([^\*]+)\*\*', content)
    
    return {
        'filename': filename,
        'path': str(filepath),
        'title': title,
        'size': len(content),
        'aksiomi': aksiomi,
        'vprašanja': vprašanja,
        'kamni': kamni,
        'markerji': markerji,
        'concepts': concepts[:20],  # Prvih 20 konceptov
        'content_preview': content[:500]  # Predogled
    }


def build_index():
    """Zgradi indeks vseh dokumentov"""
    print("🔍 Gradim indeks...")
    
    index = {
        'files': [],
        'stats': {
            'total_files': 0,
            'total_aksiomi': 0,
            'total_vprašanj': 0,
            'total_kamnov': 0,
            'all_markerji': set(),
            'all_concepts': set()
        }
    }
    
    # Indeksiraj vse kamne
    stone_files = list(PROJECT_DIR.glob("*resnicami-rozetni-kamni-*.md"))
    stone_files.sort()
    
    for filepath in stone_files:
        doc_index = index_file(filepath)
        index['files'].append(doc_index)
        
        index['stats']['total_files'] += 1
        index['stats']['total_aksiomi'] += len(doc_index['aksiomi'])
        index['stats']['total_vprašanj'] += len(doc_index['vprašanja'])
        index['stats']['total_kamnov'] += len(doc_index['kamni'])
        index['stats']['all_markerji'].update(doc_index['markerji'])
        index['stats']['all_concepts'].update(doc_index['concepts'])
    
    # Pretvori sete v liste
    index['stats']['all_markerji'] = sorted(list(index['stats']['all_markerji']))
    index['stats']['all_concepts'] = sorted(list(index['stats']['all_concepts']))[:50]
    
    # Shrani indeks
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print(f"   ✅ Indeksiranih: {index['stats']['total_files']} datotek")
    print(f"   ✅ Aksiomi: {index['stats']['total_aksiomi']}")
    print(f"   ✅ Vprašanja: {index['stats']['total_vprašanj']}")
    print(f"   ✅ Kamni: {index['stats']['total_kamnov']}")
    print(f"   ✅ Markerji: {len(index['stats']['all_markerji'])}")
    
    return index


def create_sqlite_index():
    """Ustvari SQLite indeks"""
    print("\n🗃️ Ustvarjam SQLite indeks...")
    
    if INDEX_DB.exists():
        os.remove(INDEX_DB)
    
    conn = sqlite3.connect(INDEX_DB)
    cursor = conn.cursor()
    
    # Ustvari tabele
    cursor.execute('''
        CREATE TABLE documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE,
            path TEXT,
            title TEXT,
            size INTEGER
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE aksiomi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_id INTEGER,
            aksiom_number TEXT,
            FOREIGN KEY (doc_id) REFERENCES documents(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE vprašanja (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_id INTEGER,
            vprašanje_number TEXT,
            FOREIGN KEY (doc_id) REFERENCES documents(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE kamni (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_id INTEGER,
            kamen TEXT,
            FOREIGN KEY (doc_id) REFERENCES documents(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE markerji (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_id INTEGER,
            marker TEXT,
            FOREIGN KEY (doc_id) REFERENCES documents(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE concepts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_id INTEGER,
            concept TEXT,
            FOREIGN KEY (doc_id) REFERENCES documents(id)
        )
    ''')
    
    # Indeksiraj in vnesi
    index = build_index()
    
    for doc in index['files']:
        cursor.execute(
            "INSERT INTO documents (filename, path, title, size) VALUES (?, ?, ?, ?)",
            (doc['filename'], doc['path'], doc['title'], doc['size'])
        )
        doc_id = cursor.lastrowid
        
        for a in doc['aksiomi']:
            cursor.execute(
                "INSERT INTO aksiomi (doc_id, aksiom_number) VALUES (?, ?)",
                (doc_id, a)
            )
        
        for v in doc['vprašanja']:
            cursor.execute(
                "INSERT INTO vprašanja (doc_id, vprašanje_number) VALUES (?, ?)",
                (doc_id, v)
            )
        
        for k in doc['kamni']:
            cursor.execute(
                "INSERT INTO kamni (doc_id, kamen) VALUES (?, ?)",
                (doc_id, k)
            )
        
        for m in doc['markerji']:
            cursor.execute(
                "INSERT INTO markerji (doc_id, marker) VALUES (?, ?)",
                (doc_id, m)
            )
        
        for c in doc['concepts']:
            cursor.execute(
                "INSERT INTO concepts (doc_id, concept) VALUES (?, ?)",
                (doc_id, c)
            )
    
    conn.commit()
    conn.close()
    
    print(f"   ✅ SQLite indeks ustvarjen: {INDEX_DB}")
    return True


def search(query, index_file=INDEX_FILE):
    """Išči v indeksu"""
    if not INDEX_FILE.exists():
        build_index()
    
    with open(index_file, 'r', encoding='utf-8') as f:
        index = json.load(f)
    
    results = []
    query_lower = query.lower()
    
    for doc in index['files']:
        score = 0
        
        # Preveri naslov
        if query_lower in doc['title'].lower():
            score += 10
        
        # Preveri filename
        if query_lower in doc['filename'].lower():
            score += 5
        
        # Preveri aksiome
        if any(query_lower == a for a in doc['aksiomi']):
            score += 20
        
        # Preveri vprašanja
        if any(query_lower == v for v in doc['vprašanja']):
            score += 20
        
        # Preveri kamne
        if any(query_lower in k.lower() for k in doc['kamni']):
            score += 15
        
        # Preveri markerje
        if any(query in m for m in doc['markerji']):
            score += 15
        
        # Preveri koncepte
        if any(query_lower in c.lower() for c in doc['concepts']):
            score += 10
        
        # Preveri vsebino (predogled)
        if query_lower in doc['content_preview'].lower():
            score += 5
        
        if score > 0:
            results.append({
                'document': doc['filename'],
                'title': doc['title'],
                'score': score,
                'path': doc['path']
            })
    
    # Sortiraj po relevanci
    results.sort(key=lambda x: x['score'], reverse=True)
    
    return results


def main():
    print("=" * 60)
    print("INDEXER ZA SISTEM ∅→∆→∂→∮")
    print("=" * 60)
    
    # Ustvari indeks
    build_index()
    
    # Ustvari SQLite indeks
    create_sqlite_index()
    
    # Test iskanja
    print("\n🔎 Test iskanja...")
    test_queries = ['∅', '245', '∂ 68', 'DA₂', 'povratna']
    
    for query in test_queries:
        results = search(query)
        print(f"\n   Iskanje: '{query}'")
        for r in results[:3]:  # Prvi 3 rezultat
            print(f"     ✅ {r['title']} ({r['score']})")
    
    print("\n" + "=" * 60)
    print("✅ INDEXIRANJE KONČANO!")
    print("=" * 60)
    print(f"\n📁 Indeks: {INDEX_FILE}")
    print(f"🗃️  SQLite: {INDEX_DB}")


if __name__ == "__main__":
    main()
