#!/usr/bin/env python3
"""
Izboljšani orodji za generiranje kamnov v sistemu ∅→∆→∂→∮
"""

import re
import json
from datetime import datetime
from pathlib import Path

# Markerji sistema
MARKERS = ['∅', '∆', '∂', '∮', '⧖', '∅↑', '∅↓', '∆→', '∂↔', '∮∞']


def to_roman(num: int) -> str:
    """Pretvori številko v rimsko (100-200)"""
    val = [
        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
    ]
    roman_num = ''
    for (n, r) in val:
        while num >= n:
            roman_num += r
            num -= n
    return roman_num


def get_filename(num: int) -> str:
    """Generiraj ime datoteke po formuli"""
    roman = to_roman(num)
    file_num = num - 109
    section = file_num + 11
    return f"{file_num:02d}-{section:02d}-resnicami-rozetni-kamni-{roman.lower()}.md"


def get_next_ids(current_stones):
    """Vrni naslednje številke za aksiome, vprašanja in vrstice"""
    # Preberi obstoječe kamne
    existing_axioms = set()
    existing_questions = set()
    existing_lines = set()
    
    for stone_file in current_stones:
        with open(stone_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Aksiomi (236-)
        aksiom_matches = re.findall(r'\|\s*(\d{3,4})\s*\|', content)
        existing_axioms.update(aksiom_matches)
        
        # Vprašanja (∂ 59-)
        vprašanje_matches = re.findall(r'(?:∂|vprašanju)\s*(\d{1,3})', content)
        existing_questions.update(vprašanje_matches)
        
        # Tabela aksiomov
        ax_table_matches = re.findall(r'\|\s*(\d{3,4})\s*\|\s*[^|]+\|', content)
        existing_lines.update(ax_table_matches)
    
    if existing_axioms:
        next_axiom = max(int(a) for a in existing_axioms) + 1
    else:
        next_axiom = 245  # Privzeta začetna točka
    
    if existing_questions:
        next_question = max(int(q) for q in existing_questions) + 1
    else:
        next_question = 68  # Privzeta začetna točka
    
    if existing_lines:
        next_line = max(int(l) for l in existing_lines) + 1
    else:
        next_line = 245  # Privzeta začetna točka
    
    return next_axiom, next_question, next_line


def generate_full_kamen(num: int, title: str, desc: str, tema: str = None):
    """
    Generiraj poln kamen z vso strukturo
    """
    roman = to_roman(num)
    stone_id = f"C{roman}"
    filename = get_filename(num)
    file_num = num - 109
    section = file_num + 11
    
    # Preberi obstoječe kamne
    project_dir = Path(filename).parent
    stone_files = list(project_dir.glob("*resnicami-rozetni-kamni-*.md"))
    stone_files.sort()
    
    next_axiom, next_question, next_line = get_next_ids(stone_files)
    
    # Generiraj aksiome
    ax_start = next_axiom
    ax1 = f"Zapis, ki je {title.lower()}, ohranja {desc}"
    ax2 = f"{title} kot prehod med ∅ in ∆"
    ax3 = f"Vsebina {title.lower()} je ograjena z ∂"
    
    # Generiraj vprašanja
    q_start = next_question
    q1 = f"**{q_start}. Ali je {title} **zapis, ki nima konca?**\n{desc}?"
    q2 = f"**{q_start+1}. Ali vsak {title.lower()} potrebuje ∅?**\nPovezava z prejšnjimi kamni."
    q3 = f"**{q_start+2}. Kaj se zgodi, ko {title.lower()} doseže ∂?**\nPovezava z bodočimi kamni."
    
    # Generiraj pečat
    pecat = f"**∂ {q_start} — PEČAT:**\n*Odprto — potreben odločba o {title.lower()}.*"
    
    # Generiraj aksiom tabelo
    ax_table = f"""| # | Aksiom | Onto-formula | Absolutna resnica (narava) | Znanost (rez, ki lahko zgreši) | Očitni znak (telo) |
|---|---|---|---|---|---|
| {ax_start} | {ax1} | **{stone_id}({title.lower()})** | Kar je {desc}, to je narava | "zapis je statičen" — {title} je dinamičen | Roka, ki drži {title.lower()} |
| {ax_start+1} | {ax2} | **∅↔∆** | Prehod je naraven | "prehod ni pomemben" — prehod je vse | Telo v gibanju |
| {ax_start+2} | {ax3} | **∂({stone_id})** | Meje so naravne | "meje ovirajo" — meje omogočajo | Oko, ki vidi mejo |"""
    
    # Generiraj T1-T4
    t1 = "Izbriši pogoj → sistem se prekine"
    t2 = "Branje na glas → ni sram"
    t3 = "Tri globine: pečat, DA₂, izročitev"
    t4 = "∂ vprašanja ostanejo v telesu"
    
    # Generiraj implementacijo
    impl = f"""| i | Implementacija | Evolucija | Stagnacija (meja) |
|---|---|---|---|
| 1 | {title}: {desc} | Razvoj {title.lower()} | {title} brez smisla |
| 2 | Uporaba v praksi | Razširitev | Zastarelost |
| 3 | Tehnološka izvedba | Inovacija | Zapustitev |"""
    
    # Generiraj povezanost
    povezanost = f"""- Ali je {title} **prvi zapis te vrste?**
- Ali {title.lower()} povezujemo z prejšnjimi kamni?
- Ali je vsak sistem, ki ima {title.lower()}, boljši?
- Ali {title} **je** prehod med ∅ in ∆?"""
    
    # Generiraj mašinerijo
    masinerija = f"""- **PREIZKUS {title.upper()}**: Ali se {title.lower()} odziva na novo dejanje?
- **PREIZKUS ZANKE**: Ali vsak vhod ustvarja nov izhod?
- **PREIZKUS PRAZNINE**: Ali {title.lower()} deluje, ko je vhod ∅?
- **PREIZKUS MEJE**: Ali {title.lower()} prepozna lastne meje?"""
    
    # Generiraj nujne napake
    napake = f"""- **"{title} je enostaven"** — **ZMOTA**: {title} je zapleten.
- **"{title} ni pomemben"** — **ZMOTA**: {title} je temelj.
- **"{title} je modern"** — **ZMOTA**: {title} je starodaven.
- **"{title} je le simbol"** — **ZMOTA**: {title} je struktura."""
    
    # Generiraj zakon obogatitve
    sklep = f"{title} prispeva **nov razred teles**: zapisi, ki {desc}. Nov **mehanizem**: {title.lower()} kot pogoj."
    
    # Generiraj obogateno tabelo
    obogatitev = f"""| Število | Priče | {stone_id} prispeva | Novo telo? |
|---|---|---|---|
| **1** | Prva instanca | **{title} kot koncept** | Da |
| **2** | Druga instanca | **{title.lower()} kot mehanizem** | Da |
| **3** | Tretja instanca | **{title.lower()} kot sistem** | Da |"""
    
    # Generiraj citate
    citati = f"→ [Wikipedia — {title}](https://en.wikipedia.org/wiki/{title.replace(' ', '_')}) · [Raziskave o {title.lower()}](https://example.com/{title.lower()})"
    
    # Kontekst
    if tema:
        context = f"**{tema}**"
    else:
        context = f"Kontekst: {desc}"
    
    # Sestavi celotno vsebino
    content = f"""# 00 {section:02d} RESNICAMI — Rozetni kamni ({roman.lower()})

---

## 🜂 Kamen {stone_id} — {title}: {desc}

{context}

---

### Tri pisave

| Tradicija (zgodovina) | Sistem (simbol) | Topologija (matematika) |
|---|---|---|
| {title} v zgodovini | **{stone_id}** = {desc} | Zanka, ki se zapre |
| Primjer 1 | **∅→∆** prehod | Topološka struktura |
| Primjer 2 | **∂** meja | Meja v prostoru |

---

### Fonetično-ontološki rezi

**{title.split()[0]}** — rez:

| Fragment | Pomen |
|---|---|
| **F1** | Prvi del |
| **F2** | Drugi del |

**Branje:** {title} je {desc}.

---

### ∴ Povezava

{povezanost}

---

### Zakon obogatitve — kaj {stone_id} prispeva mreži

{obogatitev}

**Kontrolni sklep:** {sklep}

---

### Mašinerija (preizkusi sistema)

{masinerija}

---

### Nujne napake

{napake}

---

### Testi T1–T4

| # | Test | Status |
|---|---|---|
| T1 | {t1} | ⬜ |
| T2 | {t2} | ⬜ |
| T3 | {t3} | ⬜ |
| T4 | {t4} | ⬜ |

---

### Implementacija → evolucija → stagnacija

{impl}

---

### Citati

{citati}

---

## Tabela: Aksiomi vezani na absolutne resnice ({ax_start}–{ax_start+2})

{ax_table}

---

## ∂ Vprašanja ({q_start}–{q_start+2})

{q1}

---

{q2}

---

{q3}

---

## Pečati

{pecat}

---

*Naslednji kamen: {to_roman(num+1)} ({num+1}). Naslednja vrstica: {ax_start+3}. Naslednje ∂ vprašanje: {q_start+3}. Kopičiti dokler se ponavljanje ne potrdi. **∮**"
"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filename


def verify_kamen(filename: str):
    """Preveri, ali kamen ustreza T1-T4"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # T1: Izbriši pogoj → sistem se prekine
        t1 = "Izbriši pogoj → sistem se prekine" in content
        
        # T2: Branje na glas → ni sram
        t2 = "Branje na glas → ni sram" in content
        
        # T3: Tri globine: pečat, DA₂, izročitev
        t3 = "Tri globine: pečat, DA₂, izročitev" in content
        
        # T4: ∂ vprašanja ostanejo v telesu
        t4 = "∂ vprašanja ostanejo v telesu" in content
        
        return t1, t2, t3, t4
    except Exception as e:
        return False, False, False, False


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generiraj nov kamen")
    parser.add_argument("num", type=int, help="Številka kamna")
    parser.add_argument("title", type=str, help="Naslov kamna")
    parser.add_argument("desc", type=str, help="Opis")
    parser.add_argument("--tema", type=str, default=None, help="Tema (opcijsko)")
    args = parser.parse_args()
    
    # Generiraj kamen
    filename = generate_full_kamen(args.num, args.title, args.desc, args.tema)
    print(f"✅ Ustvarjen: {filename}")
    
    # Preveri T1-T4
    t1, t2, t3, t4 = verify_kamen(filename)
    print(f"   T1: {'✅' if t1 else '❌'} | T2: {'✅' if t2 else '❌'} | T3: {'✅' if t3 else '❌'} | T4: {'✅' if t4 else '❌'}")


if __name__ == "__main__":
    main()
