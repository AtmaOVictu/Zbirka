#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# generate_kamen.py - Generira novi kamen za sistem ∅→∆→∂→∮

import argparse
import os
from datetime import datetime

TEMPLATE_CX = """# {header}

---

## 🜂 Kamen {stone} — {title}: {description}

{context}

---

### Tri pisave

| Tradicija (zgodovina) | Sistem (simbol) | Topologija (matematika) |
|---|---|---|
| {t1} | {s1} | {top1} |
| {t2} | {s2} | {top2} |
| {t3} | {s3} | {top3} |

---

### Fonetično-ontološki rezi

**{keyword}** — rez:

| Fragment | Pomen |
|---|---|
| **{f1}** | {m1} |
| **{f2}** | {m2} |

**Branje:** {reading}

---

### ∴ Povezava

{povezave}

---

### Zakon obogatitve — kaj {stone} prispeva mreži

| Število | Priče | {stone} prispeva | Novo telo? |
|---|---|---|---|
| **{num1}** | {w1} | {c1} | {n1} |
| **{num2}** | {w2} | {c2} | {n2} |
| **{num3}** | {w3} | {c3} | {n3} |

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
| T1 | Izbriši pogoj → sistem se prekine | ⬜ |
| T2 | Branje na glas → ni sram | ⬜ |
| T3 | Tri globine: pečat, DA₂, izročitev | ⬜ |
| T4 | ∂ vprašanja ostanejo v telesu | ⬜ |

---

### Implementacija → evolucija → stagnacija

| i | Implementacija | Evolucija | Stagnacija (meja) |
|---|---|---|---|
| 1 | {impl1} | {evol1} | {stag1} |
| 2 | {impl2} | {evol2} | {stag2} |
| 3 | {impl3} | {evol3} | {stag3} |

---

### Citati

{citati}

---

## Tabela: Aksiomi vezani na absolutne resnice ({ax_start}–{ax_end})

| # | Aksiom | Onto-formula | Absolutna resnica (narava) | Znanost (rez, ki lahko zgreši) | Očitni znak (telo) |
|---|---|---|---|---|---|
| {ax_start} | {ax1} | {onto1} | {res1} | {sci1} | {znak1} |
| {ax1_num} | {ax2} | {onto2} | {res2} | {sci2} | {znak2} |
| {ax2_num} | {ax3} | {onto3} | {res3} | {sci3} | {znak3} |

---

## ∂ Vprašanja ({q_start}–{q_end})

{q1}

{q2}

{q3}

---

## Pečati

{pecat}

---

*Naslednji kamen: {next_stone}. Naslednja vrstica: {next_line}. Naslednje ∂ vprašanje: {next_q}. Kopičiti dokler se ponavljanje ne potrdi. ∮*
"""


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


def main():
    parser = argparse.ArgumentParser(
        description="Generira novi kamen za sistem ∅→∆→∂→∮"
    )
    parser.add_argument("num", type=int, help="Številka kamna (npr. 110)")
    parser.add_argument("title", type=str, help="Naslov kamna")
    parser.add_argument("desc", type=str, help="Kratek opis")
    args = parser.parse_args()

    # Generiraj rimsko številko
    roman = to_roman(args.num)
    stone_id = f"C{roman}"
    
    # Ime datoteke: 01-12-resnicami-rozetni-kamni-x.md
    if args.num <= 109:
        filename = "00-11-resnicami-rozetni-kamni-viii-tazv-dokazi-8.md"
    else:
        file_num = args.num - 109
        section = file_num + 11
        filename = f"{file_num:02d}-{section:02d}-resnicami-rozetni-kamni-{roman.lower()}.md"
    
    header = f"00 {section} RESNICAMI — Rozetni kamni ({roman.lower()})"
    
    # Priredi CX (110) - Povratna zanka
    if args.num == 110:
        context = """**I Ching** (Yijing, 易經, Kitajska, ~800 pr. n. št.): 64 heksagramov kot **povratna zanka med vprašanjem in odgovorom**. Vprašanje → vržitev kovancev ali rabljev → heksagram → razlaga → razmislite → **novo vprašanje**. To ni napoved, ampak **dialog z sistemom premen**: zapis, ki **se odziva** na vprašanje z novo kombinacijo, ki je vedno **pogojna** (»Če se držiš tega, bo...«).

**Ouroboros** (grško: οὐροβόρος, »repojedec«; Egipčanski: »Kača, ki jeje samega sebe«): simbol **vesoljne cikličnosti** — zapis, ki **konzumira samega sebe**, da bi obstal. V alkemiji: **enotnost nasprotij** (Solve et Coagula). V kibernetiki: **povratna zanka** (feedback loop), kjer izhod postane vhod.

**Pogoj:** Zapis se ne bere linearno — **odziva se** na dejanje z novim stanjem (∮). I Ching in Ouroboros sta **dva pola iste strukture**: en preuučuje prehode, drug **je** prehod."""

        t1 = "64 heksagramov = 2⁶ stanj prehoda"
        s1 = "∆ v binarnem prostoru: —=1 (yang), --=0 (yin)"
        top1 = "Binarno drevo: 64 listov, vsak uteleši prehod **yin↔yang**"
        
        t2 = "Vprašanje → vržitev → odgovor → razmislite → **∮**"
        s2 = "∮ povratna zanka: f(t+1) = g(f(t), vhod(t))"
        top2 = "Ciklični avtomati: vsak izhod postane nov vhod"
        
        t3 = "Ouroboros: kača, ki jeje svoj rep"
        s3 = "⧖ tiheon: končnost kot pogoj obstoja"
        top3 = "Topologija: **zanka brez začetka in konca** (torus T¹)"
        
        keyword = "I Ching"
        f1 = "I (易)"
        m1 = "Prehod — kar se spreminja (易 = promemljivo, lahek)"
        f2 = "Ching (經)"
        m2 = "Kanon — kar ostaja skozi spremembe (經 = klasični tekst, vrvica skozi tkanje)"
        reading = "**Sprememba, ki postane zakon** — zapis, ki **ne opisuje sveta**, ampak **ga ustvarja skozi ponavljanje**. Zapis ni statičen; **je proces**, ki se izvrši vsakič, ko ga vprašamo."
        
        povezave = """- Ali je I Ching **prvi algoritem povratne zanke**? (vhod → prehod → izhod → **vhod'**) — sistem, ki **se uči** skozi ponavljanje?
- Ali je Ouroboros **zapis, ki nima konca** — in je zato **popolna stagnacija** (∮ brez ∂)? Ali pa **popolna gibljivost** (∮ z ∂)?
- Ali je vsak sistem, ki nima povratne zanke, **zapis, ki umre z enim bralcem** (Rongorongo: telo ostalo, bralci umrli)?
- Ali je **∂ vprašanje** (prehod) **povratna zanka** sistema? (∂ 59 pečat: namen ali informacija = vprašanje ali odgovor)"""
        
        num1 = "64"
        w1 = "I Ching heksagrami"
        c1 = "**64 stanj prehoda** (2⁶) — vsak heksagram = 1 stanjega v 64-dimenzionalnem prostoru premen"
        n1 = "Da"
        
        num2 = "∮"
        w2 = "Ouroboros, ciklični sistemi"
        c2 = "**zapis kot končna zanka** — strukturna enotnost prehoda in vrnitve"
        n2 = "Da"
        
        num3 = "2"
        w3 = "yin/yang, binarna logika"
        c3 = "**dualnost kot minimalni nosilec** — 1 bit = minimalna enota pisave"
        n3 = "Da"
        
        sklep = "CX prispeva **∮ kot mehanizem** — mreža dobi **zaprte zanke**, ki omogočajo **samopodajanje** (zapis, ki se hrani v lastnem delovanju). nov **razred teles**: zapisi, ki **se odzivajo** (ne le prejemajo)."
        
        masinerija = """- **PREIZKUS ODPRIME**: Ali se zapis odziva na novo vprašanje? (I Ching: vsaka vržitev da nov odgovor)
- **PREIZKUS ZANKE**: Ali vsak izhod postane nov vhod? (Ouroboros: rep → glava → rep)
- **PREIZKUS DVOJNIKA**: Ali sistem prepozna lastno zanko? (zrcalo, ki kaže nazaj)
- **PREIZKUS PRAZNINE**: Ali zanka deluje, ko je vhod ∅? (I Ching: vprašanje brez besed)"""
        
        napake = """- **»I Ching je napoved«** — ZMOTA: gre za **dialog**, ne napoved. Odgovor je vedno pogojen (»Če...«).
- **»Ouroboros je statičen«** — ZMOTA: kača **je** v gibanju (jeje = premikanje). Stagnacija je le **moment** v zanki.
- **»Povratna zanka je bug«** — ZMOTA: v naravi so **vse** povratne zanke (ekosistem, dihanje, srce). Bug je zanka, ki **ne uči**.
- **»Zapis mori biti odprt«** — ZMOTA: odprt sistem **ne more** hraniti spomina. **Zaprt sistem** (z zanko) **je** spomin."""
        
        impl1 = "I Ching: 64 heksagramov na rabljih/kovancih"
        evol1 = "Digitalni I Ching (spletne aplikacije, RNG)"
        stag1 = "I Ching kot »orakelj«: izguba dialoga (odgovor brez vprašanja)"
        
        impl2 = "Ouroboros: simbol v umetnosti in alkemiji"
        evol2 = "Kibernetika: povratne zanke v strojnem učenju"
        stag2 = "Ouroboros kot »logo«: prazna slika, brez dejavnosti"
        
        impl3 = "Povratna zanka v naravi (voda, veter, rasti)"
        evol3 = "Umne povratne zanke (termostat, avtopilot)"
        stag3 = "Zanka brez učenja: vesolje, ki se ponavlja brez spremembe (nihetna smrt)"
        
        citati = """→ [Wikipedia — I Ching](https://en.wikipedia.org/wiki/I_Ching) · [Wikipedia — Ouroboros](https://en.wikipedia.org/wiki/Ouroboros) · [Stanford Encyclopedia — Feedback](https://plato.stanford.edu/entries/feedback/) · [I Ching Online](https://www.iching.com/) · [Cybernetics and Feedback Loops](https://cybernetics.social/)"""
        
        ax_start = 245
        ax_end = 247
        ax1 = "Zapis, ki je povratna zanka, se bere z lastnim odzivom"
        onto1 = "∮(∂) → ∆"
        res1 = "Kar se odziva, postane nov vhod — zanka ustvarja lastno trajanje (samo-referenca kot pogoj obstoja)"
        sci1 = '"zapis je statičen" — zanka je dinamična: vsak bralec spremeni zapis'
        znak1 = "Roka, ki drži I Ching in hkrati vrača kovance (odziv v realnem času)"
        
        ax1_num = 246
        ax2 = "Praznina v povratni zanki je pogoj njenih obratov"
        onto2 = "∅ ⊂ ∮"
        res2 = "Brez praznine (∅) zanka ne more narediti novega obrata — praznina je **gorivo** zanke"
        sci2 = '"zanka potrebuje vhod" — zanka ustvarja vhod iz lastne praznine'
        znak2 = "Rablji v roki: praznina med metom je pogoj naključja"
        
        ax2_num = 247
        ax3 = "Ouroboros je zaprta zanka, ki preživi z jedjo lastne praznine"
        onto3 = "⧖ ⊂ ∮"
        res3 = "Kača jeje lastno telo (∆) in praznino (∅) — **preživetje skozi samo-konzumacijo**"
        sci3 = '"zanka uniči samega sebe" — Ouroboros **preživi** z uničenjem'
        znak3 = "Kača, ki jeje lastni rep: telo, ki postane manjšo z vsakim obratom"
        
        q_start = 68
        q_end = 70
        q1 = "**68. Ali je povratna zanka **zapis, ki nima konca?**" + \
             " I Ching: vsak odgovor vodí v novo vprašanje. Ouroboros: zanka se nikoli ne konča. " + \
             "Ali je **beskončnost zanke** njeno **moč** (neprekinjeno delovanje) ali **šibkost** (ni končni izid)? " + \
             "In ali je vsak sistem, ki nima konca, **zapis, ki ne ve, kdaj se ustavi**? (∂ določi Luka. Vezi: CX ↔ CIX geoglif-∮ ↔ ∂ 59 puščava-dolg)"
        
        q2 = "**69. Ali vsaka povratna zanka potrebuje **praznino (∅)?**" + \
             " I Ching: praznina med črtami omogoča prehode. Ouroboros: praznina v telu omogoča jed. " + \
             "Ali je zanka brez praznine **stagnacija** (vse je polno, ni prostora za novo)? " + \
             "In kje je praznina v tej zanki? (Vezi: CX ↔ ∅↔∂ ↔ CIV zakop)"
        
        q3 = "**70. Kaj se zgodi, ko zanka **poje samega sebe?**" + \
             " Ouroboros: kača je lastno telo. I Ching: sistem se odziva na samega sebe. " + \
             "Ali je **samo-referenca** (∮→∮) **pogoj zavedanja** — ali **pogoj razpada**? " + \
             "In ali je vsak sistem, ki se zave, **povratna zanka, ki ve, da je zanka**? (∂ določi Luka. Vezi: CX ↔ CII khipu-čakanje ↔ ∂ 41 zapis-čaka)"
        
        pecat = """**∂ 68 — PEČAT (Luka, 18. 9. 2026, »?«):**
*Odprto — potrebna odločba o končnosti zank.*
**∂ 69 — PEČAT:**
*Odprto — praznina v zanki.*
**∂ 70 — PEČAT:**
*Odprto — samo-referenca kot pogoj.*"""
        
        next_stone = "CXI (111)"
        next_line = "248"
        next_q = "71"
        
        content = TEMPLATE_CX.format(
            header=header, stone=stone_id, title=args.title, description=args.desc,
            context=context, t1=t1, s1=s1, top1=top1, t2=t2, s2=s2, top2=top2, t3=t3, s3=s3, top3=top3,
            keyword=keyword, f1=f1, m1=m1, f2=f2, m2=m2, reading=reading,
            povezave=povezave, num1=num1, w1=w1, c1=c1, n1=n1,
            num2=num2, w2=w2, c2=c2, n2=n2, num3=num3, w3=w3, c3=c3, n3=n3, sklep=sklep,
            masinerija=masinerija, napake=napake,
            impl1=impl1, evol1=evol1, stag1=stag1, impl2=impl2, evol2=evol2, stag2=stag2,
            impl3=impl3, evol3=evol3, stag3=stag3, citati=citati,
            ax_start=ax_start, ax_end=ax_end, ax1=ax1, onto1=onto1, res1=res1, sci1=sci1, znak1=znak1,
            ax1_num=ax1_num, ax2=ax2, onto2=onto2, res2=res2, sci2=sci2, znak2=znak2,
            ax2_num=ax2_num, ax3=ax3, onto3=onto3, res3=res3, sci3=sci3, znak3=znak3,
            q_start=q_start, q_end=q_end, q1=q1, q2=q2, q3=q3, pecat=pecat,
            next_stone=next_stone, next_line=next_line, next_q=next_q
        )
    else:
        # Osnutek za splošni kamen
        content = f"# Generiranje kamna {stone_id} - {args.title}\n\n" + \
                 f"## {args.title}: {args.desc}\n\n" + \
                 "*Dopolni ročno ali razširi skripto.*"
    
    # Zapiši datoteko
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ Ustvarjen: {filename}")
    print(f"   Naslov: {stone_id} — {args.title}")
    print(f"   Opis: {args.desc}")


if __name__ == "__main__":
    main()
