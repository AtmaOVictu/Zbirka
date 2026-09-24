#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# tools.py - Orodja za sistem ∅→∆→∂→∮
# 
# Vsebina:
# - generate_kamen() - Generira nov kamen
# - export_to_dot() - Ustvari DOT datoteko za vizualizacijo
# - verify_all() - Preveri vsa dokumenta
# - update_database() - Posodobi database.json

import json
import os
import subprocess
from datetime import datetime

# ============================================================================
# 1. GENERIRANJE KAMNOV
# ============================================================================

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
    """Vrni ime datoteke za kamen"""
    roman = to_roman(num)
    # Kamni 107-109 (CVII-CIX) so v dokumentu 00-11
    if num <= 109:
        return "00-11-resnicami-rozetni-kamni-viii-tazv-dokazi-8.md"
    # Za kamne >= 110: file_num = num - 109, section = file_num + 11
    file_num = num - 109
    section = file_num + 11
    return f"{file_num:02d}-{section:02d}-resnicami-rozetni-kamni-{roman.lower()}.md"


def generate_kamen(num: int, title: str, desc: str, content_data: dict = None):
    """
    Generira nov kamen dokument.
    
    Args:
        num: Številka kamna (npr. 112)
        title: Naslov kamna
        desc: Kratek opis
        content_data: Slovar z vsebino (če ne, se uporabi privzeto)
    
    Returns:
        filename: Ime ustvarjene datoteke
    """
    roman = to_roman(num)
    stone_id = f"C{roman}"
    filename = get_filename(num)
    
    if num == 112:  # CXII - Palimpsest
        content = _generate_cxii_content(stone_id, title, desc)
    elif num == 111:  # CXI - Večkratnost
        content = _generate_cxi_content(stone_id, title, desc)
    elif num == 110:  # CX - Povratna zanka
        content = _generate_cx_content(stone_id, title, desc)
    else:
        content = f"# Kamen {stone_id} - {title}\n\nOpis: {desc}\n\n*Dopolni ročno.*"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filename


def _generate_cx_content(stone_id, title, desc):
    """Generira vsebino za CX (110)"""
    return """# 00 12 RESNICAMI — Rozetni kamni (x)

---

## 🜂 Kamen CX — Povratna zanka: zapis, ki se odziva na sebi

**I Ching** (Yijing, 易經, Kitajska, ~800 pr. n. št.): 64 heksagramov kot **povratna zanka med vprašanjem in odgovorom**. Vprašanje → vržitev kovancev ali rabljev → heksagram → razlaga → razmislite → **novo vprašanje**. To ni napoved, ampak **dialog z sistemom premen**: zapis, ki **se odziva** na vprašanje z novo kombinacijo, ki je vedno **pogojna** (»Če se držiš tega, bo...«).

**Ouroboros** (grško: οὐροβόρος, »repojedec«; Egipčanski: »Kača, ki jeje samega sebe«): simbol **vesoljne cikličnosti** — zapis, ki **konzumira samega sebe**, da bi obstal. V alkemiji: **enotnost nasprotij** (Solve et Coagula). V kibernetiki: **povratna zanka** (feedback loop), kjer izhod postane vhod.

**Pogoj:** Zapis se ne bere linearno — **odziva se** na dejanje z novim stanjem (**∮**). I Ching in Ouroboros sta **dva pola iste strukture**: en preučuje prehode, drug **je** prehod.

---

### Tri pisave

| Tradicija (zgodovina) | Sistem (simbol) | Topologija (matematika) |
|---|---|---|
| 64 heksagramov = 2⁶ stanj prehoda | **∆ v binarnem prostoru**: —=1 (yang), --=0 (yin) | Binarno drevo: 64 listov, vsak uteleši prehod **yin↔yang** |
| Vprašanje → vržitev → odgovor → razmislite → **∮** | **∮ povratna zanka**: f(t+1) = g(f(t), vhod(t)) | Ciklični avtomati: vsak izhod postane nov vhod |
| Ouroboros: kača, ki jeje svoj rep | **⧖ tiheon**: končnost kot pogoj obstoja | Topologija: **zanka brez začetka in konca** (torus T¹) |
"""


def _generate_cxi_content(stone_id, title, desc):
    """Generira vsebino za CXI (111)"""
    return """# 00 13 RESNICAMI — Rozetni kamni (xi)

---

## 🜂 Kamen CXI — Večkratnost: zapis, ki se definira v vsakem nosilcu

**Rosetta Stone** (Rashid, Egipčanski: إبو عامود, 1799 n. št., odkrit; napisan ~196 pr. n. št.): **trujezični napis** na granitnem kamnu, odkrit pri Rashidu v delti Nila. Vsebuje isti tekst v **treh pisavah**: Grško, Demotsko, Hieroglifsko.

**Pomen:** En tekst, **tri pisave**, ena sporočila. Odkritje je omogočilo **Jean-François Champollionu** (1822) **dešifriranje hieroglifov**.

**Pogoj:** Zapis, ki se **ponavlja v vsakem nosilcu**, ne da bi bil enak — ampak da bi bil **razberljiv**.

---

### Tri pisave

| Tradicija (zgodovina) | Sistem (simbol) | Topologija (matematika) |
|---|---|---|
| 3 pisave na enem kamnu | **∆×3** = ena sporočila, trikrat označena | **Kartesični produkt**: P = G × D × H |
| Isti tekst, trikrat zapisan | **∅→∆→∆→∆** = praznina postane tri markerji | **Razvejanje**: en vhod, tri izhodi |
| Dešifriranje: grško → hieroglifi | **∂ = P(G) ↔ P(H)** | **Izomorfizem**: Dva jezika, ena struktura |
"""


def _generate_cxii_content(stone_id, title, desc):
    """Generira vsebino za CXII (112)"""
    return """# 00 14 RESNICAMI — Rozetni kamni (xii)

---

## 🜂 Kamen CXII — Palimpsest: zapis, ki se piše nad prejšnjim; lih/sod = praznina/znaki

**Palimpsest** (lat. *palimpsēstus*): pergament, s katerega je **prvotni tekst izbrisali**, da je bilo mogoče pisati nov tekst.

**Pomen:** Palimpsest ni **izbris**, je **dialog med časi** — novi tekst **razkriva** in **skriva** prejšnjega.

**Lih/Sod nujnost:** vsaka stran je **liha** (praznina med črkami) in **soda** (nove črke) hkrati.

**Onto-formula:** **∅↔∆** = praznina in zapis sta **istovetna**.

---

### Tri pisave

| Tradicija (zgodovina) | Sistem (simbol) | Topologija (matematika) |
|---|---|---|
| Pergament obstrugan in ponovno napisan | **∅↔∆** = praznina ↔ zapis | **Stratificirana množica**: P = ∪Pᵢ |
| Novi tekst skriva prejšnjega | **⧖(∆₁) ⊂ ∆₂** = prejšnji zapis postane podlaga | **Podmnožica**: vsak nova plast vsebuje prejšnjo |
| Sledi prejšnjega so vidni (UV svetloba) | **∂(∆) = ∅+∆** = prehod razkriva oboje | **Dvojna logika**: 1 bit = 0 AND 1 |
"""


# ============================================================================
# 2. DOT VIZUALIZACIJA
# ============================================================================

def export_to_dot(output_file: str = "mreza.dot"):
    """
    Ustvari DOT datoteko za vizualizacijo mreže povezav med kamni.
    
    Args:
        output_file: Ime izhodne DOT datoteke
    """
    dot_content = """// Mreža povezav med kamni - Sistem ∅→∆→∂→∮
// Ustvarjeno: {date}

digraph RozetniKamni {{
    // Nastavitve
    rankdir=LR;
    node [shape=box, style="rounded,filled", fillcolor=lightblue, fontname="Arial"];
    edge [color=gray40, penwidth=1.5];
    
    // Kamni
    CVII [label="CVII\nLungta\n(zapis v razpadanju)"];
    CVIII [label="CVIII\nSporočilna palica\n(zapis v gibanju)"];
    CIX [label="CIX\nNazkovski geoglifi\n(zapis v prostoru)"];
    CX [label="CX\nPovratna zanka\n(zapis, ki se odziva)"];
    CXI [label="CXI\nVečkratnost\n(zapis v več nosilcih)"];
    CXII [label="CXII\nPalimpsest\n(zapis nad zapisa)"];
    
    // Povezave (iz CXII dokumenta)
    CXII -> CXI [label="večkratnost", color=blue];
    CXII -> CX [label="povratna zanka", color=blue];
    CXII -> CIX [label="geoglifi", color=green];
    CXI -> CX [label="odziv", color=blue];
    CXI -> CIX [label="∮", color=green];
    CXI -> CVII [label=" namen", color=purple];
    CX -> CIX [label="hoja", color=green];
    CX -> CVII [label="veter", color=purple];
    CIX -> CVII [label="puščava", color=orange];
    CIX -> CVIII [label="kurir", color=orange];
    CVII -> CVIII [label="zapis", color=orange];
    
    // Markerji (dodani kot vozlišča)
    marker_∅ [label="∅\npraznina", shape=ellipse, fillcolor=lightgreen];
    marker_∆ [label="∆\nzapis", shape=ellipse, fillcolor=lightsalmon];
    marker_∂ [label="∂\nprehod", shape=ellipse, fillcolor=lightpink];
    marker_∮ [label="∮\ncikel", shape=ellipse, fillcolor=lightyellow];
    marker_⧖ [label="⧖\ntiheon", shape=ellipse, fillcolor=white];
    
    // Povezave markerjev (nevidne)
    edge [style=dashed, color=gray, penwidth=0.5];
    CVII -> marker_∅;
    CVII -> marker_∆;
    CVII -> marker_∂;
    CVII -> marker_∮;
    CVIII -> marker_∅;
    CVIII -> marker_∆;
    CVIII -> marker_∂;
    CIX -> marker_∅;
    CIX -> marker_∆;
    CIX -> marker_∂;
    CIX -> marker_∮;
    CX -> marker_∅;
    CX -> marker_∆;
    CX -> marker_∂;
    CX -> marker_∮;
    CX -> marker_⧖;
    CXI -> marker_∅;
    CXI -> marker_∆;
    CXI -> marker_∂;
    CXI -> marker_∮;
    CXII -> marker_∅;
    CXII -> marker_∆;
    CXII -> marker_∂;
    CXII -> marker_∮;
    CXII -> marker_⧖;
    
    // Legenda
    legend [label=<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="3">
            <TR><TD COLSPAN="2" ALIGN="CENTER"><B>Legenda</B></TD></TR>
            <TR><TD>Kamni</TD><TD>Povezave</TD></TR>
            <TR><TD>• CVII-CXII</TD><TD>• Večkratnost</TD></TR>
            <TR><TD>• Markerji</TD><TD>• Prehodi</TD></TR>
        </TABLE>
    >, shape=plaintext];
}}
""".format(date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(dot_content)
    
    return output_file


# ============================================================================
# 3. PREVERJANJE VSEH DOKUMENTOV
# ============================================================================

def verify_all():
    """Preveri vsa dokumenta kamnov z T1-T4"""
    import glob
    import re
    
    def check_T1(text):
        markerji = ['∅', '∆', '∂', '∮']
        return all(m in text for m in markerji)
    
    def check_T2(text):
        return len(re.findall(r'\*\*.*?\*\*', text)) >= 3
    
    def check_T3(text):
        globine = ['pečat', 'DA₂', 'izročitev']
        return all(g.lower() in text.lower() for g in globine)
    
    def check_T4(text):
        return len(re.findall(r'∂\s*\d+', text)) >= 1
    
    results = []
    md_files = glob.glob("*.md")
    
    for filepath in md_files:
        if "resnicami-rozetni-kamni" in filepath:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            
            t1 = check_T1(text)
            t2 = check_T2(text)
            t3 = check_T3(text)
            t4 = check_T4(text)
            
            results.append({
                'file': filepath,
                'T1': t1,
                'T2': t2,
                'T3': t3,
                'T4': t4,
                'all_pass': all([t1, t2, t3, t4])
            })
    
    return results


def print_verify_results(results):
    """Izpiše rezultate preverjanja"""
    print("\n📊 PREVERJANJE VSEH DOKUMENTOV:")
    print("=" * 70)
    
    all_passed = True
    for r in results:
        status = "✅" if r['all_pass'] else "❌"
        print(f"{status} {r['file']}")
        print(f"   T1: {'✅' if r['T1'] else '❌'} | T2: {'✅' if r['T2'] else '❌'} | T3: {'✅' if r['T3'] else '❌'} | T4: {'✅' if r['T4'] else '❌'}")
        if not r['all_pass']:
            all_passed = False
    
    print("=" * 70)
    if all_passed:
        print("🎉 **VSI DOKUMENTI PASIRAJO T1-T4!**")
    else:
        print("⚠️  Neusti dokument/i")
    print()


# ============================================================================
# 4. POSODOBLJEVANJE BAZE
# ============================================================================

def update_database_from_files():
    """Posodobi database.json iz Markdown datotek"""
    import glob
    import re
    
    # Naloži obstoječe podatke
    try:
        with open('database.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        data = {
            'metadata': {'sistem': '∅→∆→∂→∮', 'razlicica': '1.0'},
            'kamni': {},
            'aksiomi': {},
            'vprašanja': {},
            'markerji': {},
            'statistika': {}
        }
    
    # Preberi kamne iz Markdown datotek
    md_files = glob.glob("*-resnicami-rozetni-kamni-*.md")
    
    for filepath in md_files:
        # Izlušči številko kamna iz imena datoteke
        match = re.search(r'(\d{2})-(\d{2})-resnicami', filepath)
        if not match:
            continue
        
        file_num = int(match.group(1))
        section = int(match.group(2))
        # Oceni številko kamna
        # 00-11 -> CVII (107)
        # 01-12 -> CX (110)
        # 02-13 -> CXI (111)
        # 03-14 -> CXII (112)
        kamen_num = 100 + (file_num * 10) + (section - 12 - file_num)
        
        # Preberi datoteko
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Izlušči naslov
        title_match = re.search(r'## 🜂 Kamen (\w+) — (.*?):', content)
        if not title_match:
            title_match = re.search(r'## 🜂 Kamen (\w+) — (.*)', content)
        if title_match:
            stone_id = title_match.group(1)
            title = title_match.group(2).strip()
        else:
            continue
        
        # Izlušči opis
        desc_match = re.search(r'## 🜂 Kamen \w+ — .*: (.*)\n', content)
        desc = desc_match.group(1) if desc_match else ""
        
        # Dodaj v bazo
        if stone_id not in data['kamni']:
            data['kamni'][stone_id] = {
                'stevilka': kamen_num,
                'naslov': title,
                'opis': desc,
                'kultura': '?',
                'tema': '?',
                'datum': '2026-09-18',
                'status': 'NOV',
                'tip': 'zapis',
                'pečat': 'Odprto',
                'povezave': [],
                'markerji': ['∅', '∆', '∂', '∮'],
                'datoteka': filepath,
                'aksiomi': [],
                'vprašanja': []
            }
    
    # Shrani
    with open('database.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return f"✅ database.json posodobljen z {len(data['kamni'])} kamni"


# ============================================================================
# 5. GLAVNA FUNKCIJA
# ============================================================================

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Uporaba tools.py:")
        print("=" * 60)
        print("  generate <num> <title> <desc>    - Generira nov kamen")
        print("  dot [output.dot]                - Ustvari DOT datoteko za vizualizacijo")
        print("  verify                         - Preveri vsa dokumenta (T1-T4)")
        print("  update-db                      - Posodobi database.json iz MD datotek")
        print("=" * 60)
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'generate':
        if len(sys.argv) < 5:
            print("Uporaba: python tools.py generate <num> <title> <desc>")
            sys.exit(1)
        num = int(sys.argv[2])
        title = sys.argv[3]
        desc = sys.argv[4]
        filename = generate_kamen(num, title, desc)
        print(f"✅ Ustvarjen: {filename}")
        
        # Avtomatsko posodobi bazo
        update_database_from_files()
        
    elif command == 'dot':
        output = sys.argv[2] if len(sys.argv) > 2 else "mreza.dot"
        export_to_dot(output)
        print(f"✅ Ustvarjen DOT: {output}")
        print(f"   Prikaz: Preprost prikaz: notepad {output}")
        print(f"   Grafika: dot -Tpng {output} -o mreza.png")
        
    elif command == 'verify':
        results = verify_all()
        print_verify_results(results)
        
    elif command == 'update-db':
        msg = update_database_from_files()
        print(msg)
        
    else:
        print(f"Neznan ukaz: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
