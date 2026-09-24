#!/usr/bin/env python3
"""
Auto-generiraj kamne za sistem ∅→∆→∂→∮
Avtomatizirano ustvarjanje novih kamnov z osnovno strukturo
"""

import os
import sys
import json
import subprocess
from datetime import datetime

# Konfiguracija
STONE_DIR = "."
TOOLS_SCRIPT = "tools.py"
DATABASE_FILE = "database.json"

# Seznam predlaganih kamnov (ime, opis, teme)
STONE_TEMPLATES = [
    (120, "Krog", "zapis kot cikel", "Kelti/Slavi + Grčija"),
    (121, "Vektor", "zapis kot smer", "Matematika + Fizika"),
    (122, "Val", "zapis kot nihanje", "Fizika + Glazba"),
    (123, "Točka", "zapis kot izvor", "Geometrija + filozofija"),
    (124, "Črta", "zapis kot pot", "Pisava + Kartografija"),
    (125, "Ravnina", "zapis kot površina", "Matematika + Umetnost"),
    (126, "Prostor", "zapis kot dimenzija", "Fizika + Arhitektura"),
    (127, "Čas", "zapis kot trajanje", "Filozofija + Zgodovina"),
    (128, "Svetloba", "zapis kot vidnost", "Fizika + Simbolika"),
    (129, "Tema", "zapis kot praznina", "Filozofija + Arhitektura"),
    (130, "Zrcaljenje", "zapis kot podvojenje", "Optika + Psihologija"),
]


def load_database():
    """Naloži baza kamnov"""
    if not os.path.exists(DATABASE_FILE):
        return {"kamni": []}
    with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_next_stone_id(db):
    """Vrni naslednjo prosto številko kamna"""
    existing_ids = [k['id'] for k in db['kamni'] if k['id'].isdigit()]
    if not existing_ids:
        return 100
    return max(int(x) for x in existing_ids) + 1


def generate_stone(stone_id, naslov, opis, tema=None):
    """Generiraj nov kamen"""
    cmd = [
        sys.executable, TOOLS_SCRIPT, "generate",
        str(stone_id),
        naslov,
        opis
    ]
    if tema:
        cmd.append(tema)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=STONE_DIR)
        if result.returncode == 0:
            print(f"✅ Ustvarjen kamen {stone_id}: {naslov}")
            return True
        else:
            print(f"❌ Napaka pri generiranju kamna {stone_id}: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Napaka: {e}")
        return False


def batch_generate(count=5):
    """Generiraj več kamnov hkrati"""
    db = load_database()
    next_id = get_next_stone_id(db)
    
    generated = 0
    for i in range(count):
        stone_num = next_id + i
        if stone_num in [t[0] for t in STONE_TEMPLATES]:
            # Uporabi preddefinirano predlogo
            template = [t for t in STONE_TEMPLATES if t[0] == stone_num][0]
            if generate_stone(template[0], template[1], template[2], template[3]):
                generated += 1
        else:
            # Ustvari generično predlogo
            if generate_stone(
                stone_num,
                f"Kamen {stone_num}",
                f"zapis kot koncept {stone_num}"
            ):
                generated += 1
    
    print(f"\n📊 Ustvarjenih: {generated}/{count} kamnov")
    return generated


def verify_all():
    """Preveri vse kamne"""
    print("\n🔍 Preverjanje vseh kamnov...")
    result = subprocess.run(
        [sys.executable, TOOLS_SCRIPT, "verify"],
        capture_output=True,
        text=True,
        cwd=STONE_DIR
    )
    print(result.stdout)
    return result.returncode == 0


def update_database():
    """Posodobi baza podatek"""
    print("\n📥 Posodabljanje baze...")
    result = subprocess.run(
        [sys.executable, "db_manager.py", "sync"],
        capture_output=True,
        text=True,
        cwd=STONE_DIR
    )
    print(result.stdout)
    return result.returncode == 0


def rebuild_exe():
    """Ponovno zgradi GUI izvršljivo datoteko"""
    print("\n🏗️ Ponovna gradnja GUI...")
    result = subprocess.run(
        [sys.executable, "-m", "PyInstaller", "sistem_gui.spec", "--clean"],
        capture_output=True,
        text=True,
        cwd=STONE_DIR
    )
    print(result.stdout)
    if result.stderr:
        print("⚠️  Opomnik:", result.stderr)
    return result.returncode == 0


def main():
    print("=" * 60)
    print("AUTO-GENERATOR ZA SISTEM ∅→∆→∂→∮")
    print("=" * 60)
    
    # Preveri stanje
    print("\n📁 Trenutna mapa:")
    stones = [f for f in os.listdir(STONE_DIR) if f.startswith(tuple(f"{i:02d}-" for i in range(100)))]
    print(f"   Obstoječi kamni: {len(stones)}")
    
    # Generiraj nove kamne
    batch_generate(3)  # Generiraj 3 nove kamne
    
    # Preveri vse
    if not verify_all():
        print("⚠️  Neustreza T1-T4 v nekaterih dokumentih")
    
    # Posodobi baza
    update_database()
    
    # Ponovno zgradi GUI
    rebuild_exe()
    
    print("\n" + "=" * 60)
    print("✅ Avtomatizirani postopek končan!")
    print("=" * 60)


if __name__ == "__main__":
    main()
