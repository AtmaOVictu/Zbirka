#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# preveri_0124.py - Preveri T1-T4 za kamne ∅→∆→∂→∮

import sys
import re


def preveri_T1(text: str) -> tuple:
    """
    T1: Izbriši pogoj → sistem se prekine
    Preveri: Ali so prisotni vsi markerji (∅, ∆, ∂, ∮)?
    """
    markerji = ['∅', '∆', '∂', '∮']
    najdeni = [m for m in markerji if m in text]
    manjkajo = [m for m in markerji if m not in text]
    passed = len(manjkajo) == 0
    return (passed, f"Markerji: {'✓'.join(najdeni)} {'✗'.join(manjkajo)}" if manjkajo else "Vsi markerji (∅∆∂∮) prisotni")


def preveri_T2(text: str) -> tuple:
    """
    T2: Branje na glas → ni sram
    Preveri: Ali so prisotne revolucionarne zvezde **...** (∆ markerji)
    """
    pattern = r'\*\*.*?\*\*'
    matches = re.findall(pattern, text)
    passed = len(matches) >= 3  # vsaj 3 ∆ markerje
    return (passed, f"{len(matches)} ∆ markerjev (potrebno ≥3)")


def preveri_T3(text: str) -> tuple:
    """
    T3: Tri globine (pečat, DA₂, izročitev)
    Preveri: Ali so prisotne vse tri globine?
    """
    globine = ['pečat', 'DA₂', 'izročitev']
    najdene = [g for g in globine if g.lower() in text.lower()]
    manjkajo = [g for g in globine if g.lower() not in text.lower()]
    passed = len(manjkajo) == 0
    return (passed, f"Globine: {'✓'.join(najdene)} {'✗'.join(manjkajo)}" if manjkajo else "Vse tri globine prisotne")


def preveri_T4(text: str) -> tuple:
    """
    T4: ∂ vprašanja ostanejo v telesu
    Preveri: Ali so ∂ vprašanja oštevilčena (∂ 68, ∂ 69, ...)?
    """
    pattern = r'∂\s*\d+'
    matches = re.findall(pattern, text)
    passed = len(matches) >= 1  # vsaj eno ∂ vprašanje
    return (passed, f"{len(matches)} ∂ vprašanj (najdena: {', '.join(matches)})")


def preveri_dokument(filepath: str) -> dict:
    """
    Preveri vsa T1-T4 za datoteko
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        return {
            'error': f'Datoteka {filepath} ne obstaja',
            'T1': (False, ''),
            'T2': (False, ''),
            'T3': (False, ''),
            'T4': (False, '')
        }
    
    return {
        'file': filepath,
        'T1': preveri_T1(text),
        'T2': preveri_T2(text),
        'T3': preveri_T3(text),
        'T4': preveri_T4(text)
    }


def izpisi_rezultat(rezultat: dict):
    """Izpiše rezultat preverjanja"""
    if 'error' in rezultat:
        print(f"❌ {rezultat['error']}")
        return
    
    print(f"\n📄 Preverjanje: {rezultat['file']}")
    print("=" * 60)
    
    for test in ['T1', 'T2', 'T3', 'T4']:
        passed, msg = rezultat[test]
        status = "✅" if passed else "❌"
        print(f"{test}: {status} | {msg}")
    
    # Povzetek
    all_passed = all(rezultat[test][0] for test in ['T1', 'T2', 'T3', 'T4'])
    print("=" * 60)
    if all_passed:
        print("🎉 **VSI TESTI PASIRAJO!** Dokument ustreza ∅→∆→∂→∮")
    else:
        print("⚠️  Neusti test/i. Preveri in popravi dokument.")
    print()


def main():
    if len(sys.argv) != 2:
        print("Uporaba:")
        print("  python preveri_0124.py <pot_do_datoteke.md>")
        print("\nPrimer:")
        print("  python preveri_0124.py 01-12-resnicami-rozetni-kamni-x.md")
        sys.exit(1)
    
    filepath = sys.argv[1]
    rezultat = preveri_dokument(filepath)
    izpisi_rezultat(rezultat)


if __name__ == '__main__':
    main()
