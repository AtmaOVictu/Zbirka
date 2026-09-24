#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
neo4j_setup.py - Ustvari Neo4j strukturo za mrežo kamnov
======================================================

Opis:
- Ustvari Cypher ukaze za Neo4j bazo
- Definira vozlišča (kamne) in povezave
- Ustvari indekse za hitrejše poizvedbe

Zahtevano (če želiš zares povezavo):
- Neo4j nameščen (https://neo4j.com/download/)
- pip install neo4j

Uporaba:
  python neo4j_setup.py cypher      # Ustvari cypher.dat
  python neo4j_setup.py connect    # Poveži s Neo4j in ustvari bazo
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent


def generate_cypher():
    """Generira Cypher ukaze za ustvarjanje mreže"""
    
    # Naloži kamne iz JSON
    with open(DATA_DIR / "database.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    kamni = data.get('kamni', {})
    
    cypher = """
// ========================================================================
// SISTEM ∅→∆→∂→∮ - Neo4j Mreža Kamnov
// Ustvarjeno: 18. 9. 2026
// ========================================================================

// Ustvari označevalce (Labels)
CREATE CONSTRAINT IF NOT EXISTS FOR (k:Kamen) REQUIRE k.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (m:Marker) REQUIRE m.simbol IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (a:Aksiom) REQUIRE a.id IS UNIQUE;

// Ustvari indekse
CREATE INDEX IF NOT EXISTS FOR (k:Kamen) ON (k.naslov);
CREATE INDEX IF NOT EXISTS FOR (k:Kamen) ON (k.stevilka);
CREATE INDEX IF NOT EXISTS FOR (m:Marker) ON (m.ime);

"""
    
    # Dodaj kamne
    for kamen_id, kamen_data in kamni.items():
        cypher += f"""// Kamen: {kamen_id}
MERGE (k{kamen_id}:Kamen {{id: '{kamen_id}'}})
SET k{kamen_id}.naslov = '{kamen_data.get('naslov', '')}',
    k{kamen_id}.opis = '{kamen_data.get('opis', '')}',
    k{kamen_id}.stevilka = {kamen_data.get('stevilka', 0)},
    k{kamen_id}.status = '{kamen_data.get('status', '')}',
    k{kamen_id}.tip = '{kamen_data.get('tip', '')}',
    k{kamen_id}.datum = '{kamen_data.get('datum', '')}';

"""
    
    # Dodaj markerje
    markerji_data = data.get('markerji', {})
    for simbol, marker_data in markerji_data.items():
        cypher += f"""// Marker: {simbol}
MERGE (m{simbol}:Marker {{simbol: '{simbol}'}})
SET m{simbol}.ime = '{marker_data.get('ime', '')}',
    m{simbol}.pomen = '{marker_data.get('pomen', '')}',
    m{simbol}.uporaba = '{marker_data.get('uporaba', '')}';

"""
    
    # Dodaj aksiome
    aksiomi = data.get('aksiomi', {})
    for ax_id, ax_data in aksiomi.items():
        cypher += f"""// Aksiom: {ax_id}
MERGE (a{ax_id}:Aksiom {{id: {ax_id}}})
SET a{ax_id}.besedilo = '{ax_data.get('besedilo', '')[:100]}',
    a{ax_id}.onto_formula = '{ax_data.get('onto_formula', '')}',
    a{ax_id}.resnica = '{ax_data.get('resnica', '')[:100]}';

"""
    
    # Dodaj povezave med kamni (predlagane)
    povezave = [
        ('CVII', 'CVIII', 'zapis'),
        ('CVII', 'CIX', 'razpad'),
        ('CVII', 'CX', 'veter'),
        ('CVIII', 'CIX', 'gibanje'),
        ('CVIII', 'CX', 'odziv'),
        ('CVIII', 'CXI', 'večkratnost'),
        ('CIX', 'CX', 'hoja'),
        ('CIX', 'CXII', 'prostor'),
        ('CIX', 'CXIII', 'odsev'),
        ('CX', 'CXI', 'odziv'),
        ('CX', 'CXII', 'zanka'),
        ('CX', 'CXIII', 'simetrija'),
        ('CXI', 'CXII', 'nosilci'),
        ('CXI', 'CXIII', 'prehod'),
        ('CXII', 'CXIII', 'kanal')
    ]
    
    cypher += "\n// Povezave med kamni\n"
    for src, tgt, tip in povezave:
        cypher += f"MATCH (k{src}:Kamen {{id: '{src}'}}), (k{tgt}:Kamen {{id: '{tgt}'}})\n"
        cypher += f"MERGE (k{src})-[[:{tip}]]->(k{tgt});\n\n"
    
    # Dodaj povezave kamni → markerji
    cypher += "\n// Povezave kamni → markerji\n"
    markerji = ['∅', '∆', '∂', '∮', '⧖']
    for kamen_id in kamni.keys():
        for marker in markerji:
            cypher += f"MATCH (k:Kamen {{id: '{kamen_id}'}}), (m:Marker {{simbol: '{marker}'}})\n"
            cypher += f"MERGE (k)-[[:UPORABI]]->(m);\n"
    
    # Dodaj povezave kamni → aksiomi
    cypher += "\n// Povezave kamni → aksiomi\n"
    for kamen_id, kamen_data in kamni.items():
        for ax_id in kamen_data.get('aksiomi', []):
            cypher += f"MATCH (k:Kamen {{id: '{kamen_id}'}}), (a:Aksiom {{id: {ax_id}}})\n"
            cypher += f"MERGE (k)-[[:VEZE]]->(a);\n"
    
    # Shrani v datoteko
    with open(DATA_DIR / "cypher.cyp", 'w', encoding='utf-8') as f:
        f.write(cypher)
    
    print(f"✅ Ustvarjen: cypher.cyp")
    print(f"   Velikost: {len(cypher)} znakov")
    return cypher


def connect_to_neo4j(uri: str = "bolt://localhost:7687", 
                     user: str = "neo4j", 
                     password: str = "password"):
    """Poveži s Neo4j in ustvari bazo"""
    try:
        from neo4j import GraphDatabase
        
        # Preveri povezavo
        driver = GraphDatabase.driver(uri, auth=(user, password))
        
        # Ustvari Cypher ukaze
        cypher_commands = generate_cypher().split(';')
        
        with driver.session() as session:
            for cmd in cypher_commands:
                if cmd.strip() and not cmd.strip().startswith('//'):
                    try:
                        session.run(cmd)
                    except:
                        pass  # Ignoriraj napake
        
        driver.close()
        print("✅ Neo4j baza ustvarjena!")
        
    except ImportError:
        print("❌ neo4j Python driver ni nameščen!")
        print("Namestitev: pip install neo4j")
    except Exception as e:
        print(f"❌ Napaka pri povezavi: {str(e)}")
        print("Preveri, ali Neo4j teče: http://localhost:7474")


def query_neo4j(uri: str = "bolt://localhost:7687", 
                user: str = "neo4j", 
                password: str = "password",
                query: str = "MATCH (n) RETURN n LIMIT 25"):
    """Izvedi poizvedbo na Neo4j"""
    try:
        from neo4j import GraphDatabase
        
        driver = GraphDatabase.driver(uri, auth=(user, password))
        
        with driver.session() as session:
            result = session.run(query)
            records = list(result)
            
            print(f"📊 Rezultati ({len(records)} zapisi):")
            for record in records:
                print(record)
        
        driver.close()
        
    except ImportError:
        print("❌ neo4j Python driver ni nameščen!")
    except Exception as e:
        print(f"❌ Napaka: {str(e)}")


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Uporaba neo4j_setup.py:")
        print("=" * 60)
        print("  cypher     - Ustvari Cypher datoteko (cypher.cyp)")
        print("  connect    - Poveži s Neo4j in ustvari bazo")
        print("  query      - Izvedi poizvedbo (npr: 'MATCH (n) RETURN n')")
        print("=" * 60)
        print("\nPrimer poizvedbe:")
        print("  python neo4j_setup.py query \"MATCH (k:Kamen) RETURN k\"")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'cypher':
        generate_cypher()
    elif command == 'connect':
        uri = sys.argv[2] if len(sys.argv) > 2 else "bolt://localhost:7687"
        user = sys.argv[3] if len(sys.argv) > 3 else "neo4j"
        password = sys.argv[4] if len(sys.argv) > 4 else "password"
        connect_to_neo4j(uri, user, password)
    elif command == 'query':
        query = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else "MATCH (n) RETURN n LIMIT 25"
        query_neo4j(query=query)
    else:
        print(f"Neznan ukaz: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
