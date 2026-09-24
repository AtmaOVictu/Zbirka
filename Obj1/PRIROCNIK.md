# 📖 PRIROČNIK: SISTEM ∅→∆→∂→∮

**Različica:** 1.1  
**Datum:** 18. 9. 2026  
**Avtor:** Luka + Vibe  

---

## 🎯 **NAMEN SISTEMA**

Sistem **∅→∆→∂→∮** je **samostojen, delujoč okvir** za razumevanje in simulacijo delovanja pisav skozi čas in prostor. Uporablja **četiri osnovne markerje** za opis struktur, prehodov in ciklov:

| Simbol | Ime | Pomen | Funkcija |
|---|---|---|---|
| **∅** | Praznina | Pogoj, odprtje, kanali | Nosilec, ki čaka |
| **∆** | Zapis | Vsebina, struktura, telesa | Informacija |
| **∂** | Prehod | Meja, vprašanje, sprememba | Dialog |
| **∮** | Cikel | Povratek, zanka, zaprtje | Ponavljanje |

---

## 🗂️ **STRUKTURA PROJEKTA**

```
D:\OntoProjekt\CanvasMinstral\Obj1\
├── 📄 DOKUMENTI KAMNOV
│   ├── 00-11-resnicami-rozetni-kamni-viii-tazv-dokazi-8.md  (CVII-CIX)
│   ├── 01-12-resnicami-rozetni-kamni-x.md                    (CX)
│   ├── 02-13-resnicami-rozetni-kamni-xi.md                   (CXI)
│   ├── 03-14-resnicami-rozetni-kamni-xii.md                  (CXII)
│   └── 04-15-resnicami-rozetni-kamni-cxiii.md                 (CXIII - NOVO!)
│
├── 🐍 SKRIPTI
│   ├── generate_kamen.py      → Generira nove kamne
│   ├── tools.py              → Glavno orodje (generate, verify, dot, update-db)
│   ├── preveri_0124.py        → Preverjanje T1-T4
│   ├── db_manager.py         → Upravljanje SQLite baze
│   ├── sistem_gui.py          → GUI aplikacija (PySide6)
│   ├── visualize.py          → Vizualizacija mreže (DOT/PNG/HTML)
│   ├── neo4j_setup.py        → Neo4j struktura
│   └── markerji.py           → Definicije markerjev
│
├── 🗃️ BAZE PODATKOV
│   ├── database.json          → JSON baza (7 kamnov, 21 aksiomov, 10 markerjev)
│   ├── sistem.db              → SQLite baza
│   └── cypher.cyp             → Cypher ukazi za Neo4j
│
├── 🖼️ VIZUALIZACIJE
│   ├── mreza.dot              → DOT datoteka
│   └── mreza.html             → Interaktivni HTML graf
│
├── 📦 EXE (Standalone)
│   └── dist/
│       ├── Sistem_∅→∆→∂→∮.exe       → Glavna aplikacija
│       └── Sistem_0-1-1.exe           → Različica 1.1
│
├── 📚 DOKUMENTACIJA
│   ├── STANJE-SISTEMA-18092026.md    → Stanje sistema
│   └── PRIROCNIK.md                  → Ta dokument
│
└── 🎯 TESTI
    └── (vsi dokumenti prehajajo T1-T4 ✅)
```

---

## 📊 **STATISTIKA**

```
📈 KAMNI:           7 (CVII-CXIII)
📜 AKSIOMI:        21 (236-256)
❓ VPRAŠANJA:      21
   - Odgovorjena:   9
   - Odprta:       12 (∂ 59-76)
🏷️  MARKERJI:       10 (∅, ∆, ∂, ∮, ⧖, ∅↑, ∅↓, ∆→, ∂↔, ∮∞)
✅ IZROČENI:       3 (CVII, CVIII, CIX)
✅ T1-T4:          VSI PAS (7/7 dokumentov)
```

---

## 🚀 **HITRI ZAGONI**

### 1️⃣ **Zagon GUI (Windows okno)**
```cmd
cd /d/OntoProjekt/CanvasMinstral/Obj1
dist\Sistem_∅→∆→∂→∮.exe
```
**Ali:**
```cmd
python sistem_gui.py
```

### 2️⃣ **Preveri vsa dokumenta**
```cmd
python tools.py verify
```

### 3️⃣ **Generiraj nov kamen**
```cmd
python tools.py generate 114 "Labirint" "zapis kot pot"
```

### 4️⃣ **Ustvari vizualizacije**
```cmd
python tools.py dot
python visualize.py all
```

---

## 📝 **UPORABA GUI APLIKACIJE**

Klikni **OK** v oknu in dobiš **7 zavihtov**:

### 📝 **Generiraj**
- Generiraj nove kamne
- Vnesi: Številko, Naslov, Opis
- Primer: `114`, `Labirint`, `zapis kot pot`

### ✅ **Preveri**
- Preveri T1-T4 na vseh dokumentih
- Izberi posamezen dokument iz padalne menija
- **T1**: Markerji (∅, ∆, ∂, ∮)
- **T2**: Bold tekst (≥3)
- **T3**: Globine (pečat, DA₂, izročitev)
- **T4**: ∂ vprašanja (≥1)

### 🗃️ **Baza**
- Ogled kamnov v bazi
- Gumb **OSVEŽI**: naloži nove podatke
- Gumb **STATISTIKA**: prikaz statistike

### 🖼️ **Vizualizacija**
- Ustvari DOT datoteko
- Prikaz mreže v besedilnem formatu
- Odpri z Graphviz: `dot -Tpng mreza.dot -o mreza.png`

### 🔎 **Poizvedbe**
- SQL poizvedbe na SQLite bazi
- Primeri:
  ```sql
  SELECT * FROM kamni
  SELECT * FROM kamni WHERE status = 'IZROČENO'
  SELECT * FROM aksiomi WHERE id > 250
  ```

### 📤 **Izvoz** (NOVO!)
- **IZVOZI V PDF**: Pretvori MD → PDF (z Chrome)
- **IZVOZI VSE MD**: ZIP vseh Markdown datotek
- **IZVOZI BAZO**: JSON kopija baze

### 🔍 **Išči** (NOVO!)
- Išči po vseh MD datotekah
- Vnesi iskalni izraz (npr. `∅`, `DA₂`, `zrcalo`)
- Rezultati: Datoteka + vrstica + vsebina

### ⚙️ **Nastavitve**
- Pregled sistema
- Naslednji koraki
- Dokumentacija

---

## 🎓 **KAMNI (CVII-CXIII)**

| Kamen | Številka | Naslov | Tema | Status |
|---|---|---|---|---|
| **CVII** | 107 | Lungta | Zapis v razpadanju (Tibet) | ✅ Izročen |
| **CVIII** | 108 | Sporočilna palica | Zapis v gibanju (Avstralija) | ✅ Izročen |
| **CIX** | 109 | Nazkovski geoglifi | Zapis v prostoru (Peru) | ✅ Izročen |
| **CX** | 110 | Povratna zanka | Zapis, ki se odziva (I Ching) | ✅ NOV |
| **CXI** | 111 | Večkratnost | Zapis v več nosilcih (Rosetta) | ✅ NOV |
| **CXII** | 112 | Palimpsest | Zapis nad zapisa (lih/sod) | ✅ NOV |
| **CXIII** | 113 | Zrcalo | Zapis, ki odseva (optika) | ✅ **NOVO!** |

**Naslednji:** CXIV (114) - Labirint

---

## 📜 **MARKERJI (10)**

### Osnovni markerji (5)
| Simbol | Ime | Pomen |
|---|---|---|
| **∅** | Praznina | Pogoj, odprtje, prostoru |
| **∆** | Razlika | Zapis, mark, vrez |
| **∂** | Prehod | Meja, vprašanje, sprememba |
| **∮** | Cikel | Povratek, zanka, zaprtje |
| **⧖** | Tiheon | Molk, končnost, izpolnjenost |

### Novi markerji (5)
| Simbol | Ime | Pomen |
|---|---|---|
| **∅↑** | Negativen praznina | Izbris, odbitev, uničenje |
| **∅↓** | Pogojni praznina | Aktivacija, začetek, pogoj |
| **∆→** | Usmerjen zapis | Prehod v zapis, smer, tok |
| **∂↔** | Dvo-smern prehod | Obojna sprememba, dialog |
| **∮∞** | Neskončni cikel | Večni povratek, brez konca |

---

## 🔧 **UKAZI (CMD)**

### Generiranje
```cmd
# Generiraj nov kamen
python tools.py generate 114 "Labirint" "zapis kot pot"

# Generiraj z generate_kamen.py
python generate_kamen.py 114 "Labirint" "zapis kot pot"
```

### Preverjanje
```cmd
# Preveri vsa dokumenta
python tools.py verify

# Preveri posamezen dokument
python preveri_0124.py 01-12-resnicami-rozetni-kamni-x.md
```

### Baza podatkov
```cmd
# Posodobi JSON iz MD
python tools.py update-db

# Uvozi JSON → SQLite
python db_manager.py uvozi

# Izvozi SQLite → JSON
python db_manager.py izvozi

# SQL poizvedba
python db_manager.py poizvedba "SELECT * FROM kamni"

# Statistika
python db_manager.py statistika
```

### Vizualizacija
```cmd
# Ustvari DOT
python tools.py dot

# DOT → PNG (z Graphviz)
python visualize.py png

# DOT → SVG
python visualize.py svg

# HTML (z PyVis)
python visualize.py html

# Vse skupaj
python visualize.py all
```

### Neo4j
```cmd
# Ustvari Cypher ukaze
python neo4j_setup.py cypher

# Poveži s Neo4j
python neo4j_setup.py connect

# Poizvedba na Neo4j
python neo4j_setup.py query "MATCH (k:Kamen) RETURN k"
```

### Markerji
```cmd
# Posodobi bazo
python markerji.py update

# Izpiši vse markerje
python markerji.py list

# Pokaži podrobnosti
python markerji.py get ∅↑
```

### Iskalnik
```cmd
# Išči po dokumentih
python -c "
import glob
for f in glob.glob('*resnicami*.md'):
    with open(f) as file:
        if 'zrcalo' in file.read().lower():
            print(f)
"
```

---

## 📚 **PREVERBE T1-T4**

Vsi dokumenti morajo prehajati **4 teste**:

| Test | Ime | Pogoj | Primer |
|---|---|---|---|
| **T1** | Markerji | Vsebuje **∅, ∆, ∂, ∮** | `**∅** praznina` |
| **T2** | Bold tekst | ≥3 **`**...`** | `**naslov**` |
| **T3** | Globine | Vsebuje **pečat, DA₂, izročitev** | `**pečat**` |
| **T4** | ∂ vprašanja | ≥1 **∂ #** | `**∂ 71**` |

**Preveri:**
```cmd
python tools.py verify
```

---

## ❓ **VPRAŠANJA & ODGOVORI**

### Odgovorjena vprašanja (9)
- ∂ 59: Ali sme zapis zahtevati lastno uničenje? → **DA** (lungta sme zbledeti)
- ∂ 60: Kaj dela bralec brez spomina? → **Veter**
- ∂ 61: Ali vsak sistem potrebuje Losar? → **NE**
- ∂ 62: Ali sme zapis veljati zgolj v roki nosilca? → **DA**
- ∂ 63: Kdo sme pregledati rez pred odhodom? → **Najbližji starešina**
- ∂ 64: Ali vsaka številka veže dogovor? → **DA**
- ∂ 66: Ali vsako branje zahteva povratek? → **DA**
- ∂ 67: Kaj ščiti zapis, ki ga nihče ne sme brati? → **Hranitelj**
- ∂ 68: Ali je povratna zanka zapis, ki nima konca? → **Odprto**

### Odprta vprašanja (12)
- ∂ 69: Ali vsaka povratna zanka potrebuje praznino?
- ∂ 70: Kaj se zgodi, ko zanka poje samega sebe?
- ∂ 71: Ali je zrcalo zapis, ki nima avtorja?
- ∂ 72: Ali vsak zapis potrebuje odsev, da obstane?
- ∂ 73: Kaj se zgodi, ko zrcalo odseva samega sebe?
- ∂ 74-76: **Odprto za raziskavo**

**Dokument:** `odgovori-na-ostala-∂-vprašanja.md`

---

## 🎯 **NASLEDNJI KORAKI**

### 1. Razvij sistem naprej
- [ ] Generiraj **CXIV (114)** - Labirint
- [ ] Generiraj **CXV (115)** - Kip
- [ ] Odgovori na **∂ 69-76**

### 2. Izboljšaj GUI
- [ ] Dodaj **urejevalnik kamnov**
- [ ] Dodaj **zgodovinsko sledenje**
- [ ] Dodaj **sinhcronizacijo z Git**

### 3. Razvij nove funkcije
- [ ] **Automatsko generiranje** kamnov iz podatrokov
- [ ] **Strojnik učenje** za analizo kamnov
- [ ] **Blockchain** za ne spremenljive zapise

### 4. Vizualizacije
- [ ] **3D vizualizacija** (z Plotly)
- [ ] **Animirane mreže** (z NetworkX)
- [ ] **Geoprostorska vizualizacija** (z Folium)

---

## 💡 **REŠEVANJE TEŽAV**

### Problem: GUI ne zagon!
**Rešitev:**
```cmd
# Preveri, ali je PySide6 nameščeno
pip install PySide6

# Zagon
python sistem_gui.py
```

### Problem: PDF izvoz ne deluje!
**Rešitev:**
- Namesti **Google Chrome**
- Ali uporabi **WeasyPrint**: `pip install weasyprint`

### Problem: PNG/SVG ne deluje!
**Rešitev:**
- Namesti **Graphviz**: https://graphviz.org/download/

### Problem: Neo4j ne deluje!
**Rešitev:**
- Namesti **Neo4j Desktop**: https://neo4j.com/download/
- Namesti **neo4j driver**: `pip install neo4j`

### Problem: Filename napačni!
**Rešitev:**
```cmd
# Uporabi tools.py (popravljen)
python tools.py generate 114 "Naslov" "opis"
```

---

## 📞 **PODPORA**

- **Dokumentacija:** `STANJE-SISTEMA-18092026.md`
- **Spletna stran:** (dodaj, ko bo na voljo)
- **Avtor:** Luka
- **Različica:** 1.1 (18. 9. 2026)

---

## 🎉 **SKLEP**

Sistem **∅→∆→∂→∮** je **popoloma delujoč** in **samostojen**:

✅ **7 kamnov** (CVII-CXIII)  
✅ **Vsi dokumenti prehajajo T1-T4**  
✅ **GUI aplikacija z 7 zavihtov**  
✅ **Izvoz v PDF/ZIP/JSON**  
✅ **Iskalnik po dokumentih**  
✅ **Vizualizacija (HTML)**  
✅ **Neo4j struktura**  
✅ **10 markerjev**  
✅ **Standalone EXE**  

**Sistem je pripravljen za nadaljnji razvoj!** 🚀

---

*"Ponavljanje je gotovost."* — Sistem ∅→∆→∂→∮
