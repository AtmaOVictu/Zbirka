#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# generate_kamen_enhanced.py - Razširjen generator kamnov
# NOVE ZMOŽNOSTI:
# - Podpora za generiranje poljubnih kamnov
# - Avtomatsko dodajanje v database.json
# - Izpis v DOT formatu za vizualizacijo
# - Preverjanje T1-T4 po generiranju
# - Batch mode za generiranje več kamnov

import argparse
import json
import os
import sys

# Standardni template za kamne
TEMPLATE = """# {header}

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
| T3 | Tri globine: **pečat**, **DA₂**, **izročitev** | ⬜ |
| T4 | **∂** vprašanja ostanejo v telesu | ⬜ |

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
*Naslednji kamen: {next_stone}. Naslednja vrstica: {next_line}. Naslednje ∂ vprašanje: {next_q}. 
Kopičiti dokler se ponavljanje ne potrdi. **∮***