#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
markerji.py - Definicije markerjev za sistem ∅→∆→∂→∮
======================================================

Novi markerji:
- ∅↑ : Negativen marker (izbris, odbitev, uničenje)
- ∅↓ : Pogojni marker (aktivacija, začetek)
- ∆→ : Prehod v zapis (usmerjen prehod)
- ∂↔ : Dvo-smern prehod
- ∮∞ : Neskončni cikel

Uporaba:
  python markerji.py update   # Posodobi database.json
  python markerji.py list    # Izpiši vse markerje
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent
JSON_FILE = DATA_DIR / "database.json"

# Definicije vseh markerjev
MARKERJI = {
    "∅": {
        "ime": "praznina",
        "pomen": "pogoj, odprtje, prostoru",
        "uporaba": "pred pisavo, v zanki, kot gorivo"
    },
    "∆": {
        "ime": "razlika/marker",
        "pomen": "zapis, mark, vrez",
        "uporaba": "v binarnem prostoru, kot heksagram, kot črta"
    },
    "∂": {
        "ime": "prehod",
        "pomen": "meja, vprašanje, sprememba",
        "uporaba": "v vprašanjih, kot pečat, kot pogoj"
    },
    "∮": {
        "ime": "cikel",
        "pomen": "povratek, zanka, zaprtje",
        "uporaba": "v zankah, kot hoja, kot odgovor"
    },
    "⧖": {
        "ime": "tiheon",
        "pomen": "molk, končnost, izpolnjenost",
        "uporaba": "kot odprtje, kot pogoj obstoja"
    },
    # NOVI MARKERJI
    "∅↑": {
        "ime": "negativen praznina",
        "pomen": "izbris, odbitev, uničenje, negacija",
        "uporaba": "izbris zapisa, odbitev pogoja, uničenje nosilca"
    },
    "∅↓": {
        "ime": "pogojni praznina",
        "pomen": "aktivacija, začetek, pogoj",
        "uporaba": "začetek pisave, aktivacija zank, pogoj za prehod"
    },
    "∆→": {
        "ime": "usmerjen zapis",
        "pomen": "prehod v zapis, smer, tok",
        "uporaba": "prehod iz ∅ v ∆, tok informacije, usmerjeni graf"
    },
    "∂↔": {
        "ime": "dvo-smern prehod",
        "pomen": "obojna sprememba, dialog, zrcaljenje",
        "uporaba": "odziv v obojno smer, dialog med zapisi, zrcalni prehod"
    },
    "∮∞": {
        "ime": "neskončni cikel",
        "pomen": "večni povratek, brez konca, univerzalna zanka",
        "uporaba": "zanka brez začetka in konca, vesolje kot zanka"
    }
}


def update_database():
    """Posodobi database.json z novimi markerji"""
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        data = {
            'metadata': {'sistem': '∅→∆→∂→∮', 'razlicica': '1.0'},
            'kamni': {}, 'aksiomi': {}, 'vprašanja': {}, 'markerji': {}, 'statistika': {}
        }
    
    # Posodobi markerje
    data['markerji'] = MARKERJI
    
    # Posodobi statistiko
    if 'statistika' not in data:
        data['statistika'] = {}
    data['statistika']['skupaj_markerjev'] = len(MARKERJI)
    
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ database.json posodobljen z {len(MARKERJI)} markerji")
    return len(MARKERJI)


def list_markerji():
    """Izpiši vse markerje"""
    print("\n📋 MARKERJI SISTEMA ∅→∆→∂→∮")
    print("=" * 70)
    for simbol, marker_data in MARKERJI.items():
        print(f"\n{simbol}")
        print(f"  Ime: {marker_data['ime']}")
        print(f"  Pomen: {marker_data['pomen']}")
        print(f"  Uporaba: {marker_data['uporaba']}")
    print("\n" + "=" * 70)
    print(f"Skupaj: {len(MARKERJI)} markerjev")


def get_marker(simbol: str) -> dict:
    """Vrni podrobnosti markerja"""
    return MARKERJI.get(simbol, {})


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Uporaba markerji.py:")
        print("=" * 60)
        print("  update   - Posodobi database.json")
        print("  list    - Izpiši vse markerje")
        print("  get ∅↑  - Pokaži podrobnosti markerja")
        print("=" * 60)
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'update':
        count = update_database()
        print(f"\n📊 Posodobljeno: {count} markerjev")
    elif command == 'list':
        list_markerji()
    elif command.startswith('get '):
        simbol = command[4:].strip()
        marker = get_marker(simbol)
        if marker:
            print(f"\n{simbol}:")
            for k, v in marker.items():
                print(f"  {k}: {v}")
        else:
            print(f"❌ Marker {simbol} ne obstaja!")
    else:
        print(f"Neznan ukaz: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
