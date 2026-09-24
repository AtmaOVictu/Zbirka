# 🎯 START HERE - SISTEM ∅→∆→∂→∮ v2.0
**Polna Namizna Aplikacija - Hitri Start**

---

## 🚀 **HITRI START (30 sekund)**

### **1. Odpri Command Prompt**
```cmd
cd /d/OntoProjekt/CanvasMinstral/Obj1
```

### **2. Zaženi OBOJE (GUI + EXE)**
```cmd
ZAGNI_OBOJE.bat
```

**→ To bo:**
- ✅ Namestilo vse potrebe knjižnjice
- ✅ Ustvarilo ikono
- ✅ Zaželo GUI aplikacijo
- ✅ Zgradilo EXE v ozadju

---

## 📋 **ALTERNATIVNI NAČINI**

| Želja | Ukaz | Opis |
|-------|------|-------|
| **Samo GUI** | `python sistem_gui_v2.py` | Hitro zaženi GUI |
| **Samo EXE Build** | `pyinstaller Sistem_v2.spec --clean --onefile --windowed` | Zgradi EXE |
| **Samo EXE Run** | `start dist\Sistem_v2.exe` | Zaženi že zgrajen EXE |
| **Menu** | `build_and_run.bat` | Interaktivni menu z 12 izbiami |

---

## 🎨 **KAJ JE NOVO V v2.0**

### **Polna GUI Aplikacija**
- ✅ **8 zavihov** (Generiraj, Preveri, Uredi, Baza, Vizualizacija, Poizvedbe, Išči, Izvoz, Pomoč)
- ✅ **40+ markerjev** (∅, ∆, ∂, ∮, ⧖, ⟡, DA₂, ∅↑, itd.)
- ✅ **7 bližnjic** (Ctrl+N, Ctrl+S, Ctrl+F, itd.)
- ✅ **2 temi** (Temna, Svetla)
- ✅ **Avtomatsko shranjevanje** vsakih 30 sekund
- ✅ **Preverjanje T1-T4** ob shranjevanju

### **Nove Datoteke**
| Datoteka | Namestitev | Velikost |
|----------|------------|----------|
| `sistem_gui_v2.py` | Glavna GUI aplikacija | 38.7 KB |
| `Sistem_v2.spec` | PyInstaller spec | 2.0 KB |
| `markerji_extended.py` | Simbolski register | 12.6 KB |
| `create_icon.py` | Generator ikone | 2.5 KB |
| `ZAGNI_OBOJE.bat` | Avtomatski start | 6.9 KB |
| `build_and_run.bat` | Interaktivni menu | 14.8 KB |
| `PRIROČNIK_GUI_v2.md` | Priročnik | 15.1 KB |
| `POVZETEK_IZBOLJŠAV_v2.md` | Povzetek | 12.4 KB |

---

## 📚 **DOKUMENTACIJA**

### **Za hitro učenje:**
1. **PRIROČNIK_GUI_v2.md** - Kompleten vodič (15 KB)
   - Vse funkcije po zavihih
   - Primeri uporabe
   - Reševanje težav

2. **POVZETEK_IZBOLJŠAV_v2.md** - Seznam vseh izboljšav (12 KB)
   - Kaj je novo
   - Statistika
   - Tehnične zahteve

### **Za razvoj:**
- **sistem_gui_v2.py** - Glavna aplikacija (dokumentirana)
- **markerji_extended.py** - Vsi markerji z opisi
- **Sistem_v2.spec** - PyInstaller konfiguracija

---

## 🎯 **PRVI KORAKI**

### **1. Generiraj nov kamen**
```
Zavihe: Generiraj
Stevilka: 114
Naslov: Labirint
Opis: zapis kot pot
Predloga: Polna
→ Klikni: GENERIRAJ KAMEN
```

### **2. Preveri T1-T4**
```
Zavihe: Preveri
→ Klikni: PREVERI VSE
```

### **3. Uredi dokument**
```
Zavihe: Urejevalnik
→ Izberi datoteko
→ Uredi
→ Klikni: SHRANI (Ctrl+S)
```

### **4. Išči po dokumentih**
```
Zavihe: Išči
Iskalni izraz: ∅
→ Klikni: ISKI V VSEH
```

### **5. Izvozi v PDF**
```
Zavihe: Izvoz
→ Klikni: IZVOZI V PDF
→ Izberi ime datoteke
```

---

## 🔧 **TEHNIČNE ZAHTEVE**

| Zahteva | Minimalno | Priporočeno |
|---------|-----------|-------------|
| **OS** | Windows 10 | Windows 10/11 (64-bit) |
| **Python** | 3.10 | 3.10+ |
| **RAM** | 4 GB | 8 GB |
| **Disk** | 500 MB | 1 GB |

### **Zahtevane knjižnjice (avtomatsko nameščene z ZAGNI_OBOJE.bat):**
```
PySide6>=6.4.0      # GUI
Pillow              # Ikona
markdown2           # PDF izvoz
pyinstaller         # EXE build
```

---

## 🖼️ **PREGLED SISTEMA**

```
SISTEM ∅→∆→∂→∮ v2.0
├── GUI Aplikacija (sistem_gui_v2.py)
│   ├── 8 Zavihov
│   ├── 40+ Markerjev
│   ├── 7 Bližnjic
│   ├── 2 Temi
│   └── Avtomatsko shranjevanje
│
├── EXE Aplikacija (dist/Sistem_v2.exe)
│   └── Samostojna (brez Python)
│
├── Baza Podatkov
│   ├── database.json (JSON)
│   └── sistem.db (SQLite)
│
├── Kamni (MD datoteke)
│   ├── 00-11-resnicami-rozetni-kamni-viii-tazv-dokazi-8.md
│   ├── 01-12-resnicami-rozetni-kamni-x.md
│   ├── ...
│   └── 11-22-resnicami-rozetni-kamni-cxx.md
│
└── Orodja
    ├── tools.py
    ├── db_manager.py
    ├── generate_kamen.py
    └── preveri_0124.py
```

---

## 🎨 **ZMOGLOSTI**

### **✅ Generiranje**
- Ustvari nove kamne (CX, CXI, CXII, CXIII, CXIV...)
- Polna predloga z vsemi poglavji
- Minimalna predloga
- Hitre izbire
- Avtomatska posodobitev baze

### **✅ Urejanje**
- Uredi obstoječe dokumente
- Avtomatsko dopolnjevanje markerjev
- Hitri gumbi za markerje
- Preverjanje T1-T4 ob shranjevanju

### **✅ Preverjanje**
- Preveri vsa dokumenta hkrati
- Preveri posamezni dokument
- Prikaz rezultatov v tabeli
- Podrobno poročilo

### **✅ Iskanje**
- Išči po vseh MD dokumentih
- Prikaz rezultatov z vrstico
- Iskanje markerjev
- Razlikovanje velikih/malih črk

### **✅ Vizualizacija**
- Ustvari DOT datoteko
- Pretvori v PNG (z Graphviz)
- Ustvari HTML prikaz

### **✅ Izvoz**
- PDF (z markdown2)
- ZIP (vse MD datoteke)
- JSON (baza podatkov)
- HTML (spletna stran)

### **✅ Baza Podatkov**
- JSON baza
- SQLite baza
- SQL poizvedbe
- Statistika

---

## 🏆 **PRIMER UPORABE**

### **Scenario: Ustvari nov kamen CXIV (Labirint)**

1. **Zaženi aplikacijo:**
   ```cmd
   ZAGNI_OBOJE.bat
   ```

2. **Generiraj kamen:**
   - Zavihe: **Generiraj**
   - Stevilka: `114`
   - Naslov: `Labirint`
   - Opis: `zapis kot pot`
   - Predloga: **Polna**
   - Klikni: **✨ GENERIRAJ KAMEN**

3. **Uredi dokument:**
   - Zavihe: **Urejevalnik**
   - Izberi: `04-15-resnicami-rozetni-kamni-cxiv.md`
   - Dodaj vsebino (kulturni kontekst, pogoj, tri pisave, itd.)
   - Uporabi gumbce za markerje (∅, ∆, ∂, ∮, itd.)
   - Klikni: **💾 SHRANI**

4. **Preveri T1-T4:**
   - Zavihe: **Preveri**
   - Izberi datoteko: `04-15-resnicami-rozetni-kamni-cxiv.md`
   - Klikni: **📄 PREVERI IZBRANO**
   - Če so vsi ✅, je dokument v redu!

5. **Izvozi v PDF:**
   - Zavihe: **Izvoz**
   - Klikni: **📄 IZVOZI V PDF**
   - Izberi ime: `Labirint.pdf`
   - PDF se odpre avtomatsko

---

## 🐛 **REŠEVANJE TEŽAV**

| Težava | Rešitev |
|--------|---------|
| PySide6 ni nameščen | `pip install PySide6` |
| PyInstaller ni nameščen | `pip install pyinstaller` |
| Graphviz ni nameščen | Namesti od [graphviz.org](https://graphviz.org) |
| markdown2 ni nameščen | `pip install markdown2` |
| EXE se ne zgradi | Preveri, ali so vse datoteke prisotne |
| Ikonica ne deluje | `python create_icon.py` |

---

## 📅 **ČASOVNI NAČRT**

| Datum | Dejanje | Status |
|-------|---------|--------|
| 18. 9. 2026 | Začetek projekta | ✅ |
| 18. 9. 2026 | Obstoječe datoteke | ✅ |
| 19. 9. 2026 | **v2.0 Razvoj** | ✅ **KONČANO** |

---

## 🎯 **ZAKLJUČEK**

**SISTEM ∅→∆→∂→∮ v2.0 JE POLNO DELUJOČ, SAMOSTOJEN IN PRIPRAVLJEN ZA UPORABO!** 🚀

### **Kaj lahko narediš zdaj:**
1. ✅ **Zaženi GUI** → `ZAGNI_OBOJE.bat`
2. ✅ **Ustvari nove kamne** → CXIV, CXV, CXVI...
3. ✅ **Uredi obstoječe** → Popravi in izboljšaj
4. ✅ **Preveri T1-T4** → Zagotovljena kakovost
5. ✅ **Išči** → Najdi informacije
6. ✅ **Izvozi** → Deli rezultate
7. ✅ **Zgradi EXE** → Samostojna aplikacija

### **Sistem je:**
- ✅ **Delujoč** - Vse funkcije delujejo
- ✅ **Testiran** - Preverjeno na obstoječih dokumentih
- ✅ **Dokumentiran** - Priročnik in navodila
- ✅ **Samostojen** - Deluje kot EXE
- ✅ **Razširljiv** - Pripravljen za prihodnje izboljšave

---

## 📌 **POMOBNE DATOTEKE**

| Datoteka | Namestitev | Kdaj uporabiti |
|----------|------------|----------------|
| `ZAGNI_OBOJE.bat` | Avtomatski start GUI + EXE | **⭐ PRIPOROČENO** |
| `build_and_run.bat` | Interaktivni menu | Izberi funkcijo |
| `sistem_gui_v2.py` | GUI aplikacija | Ročno zaženi |
| `Sistem_v2.spec` | PyInstaller spec | Zgradi EXE |
| `PRIROČNIK_GUI_v2.md` | Priročnik | Uči se |

---

## 🚀 **ZAČNI!**

```cmd
cd /d/OntoProjekt/CanvasMinstral/Obj1
ZAGNI_OBOJE.bat
```

**→ To je vse! Aplikacija se bo odprla, EXE se bo zgradil, in lahko začneš delati!**

---

*© 2026 SISTEM ∅→∆→∂→∮ v2.0 - Vse pravice pridržane*
*Avtor: Luka + Vibe (Mistral AI)*
