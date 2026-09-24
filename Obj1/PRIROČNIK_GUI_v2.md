# 📖 PRIROČNIK - SISTEM ∅→∆→∂→∮ v2.0
**Polna Namizna Aplikacija**

---

## 🎯 UVOD

Dobrodošli v **SISTEM ∅→∆→∂→∮ v2.0** - polni namizni sistem za delo s teorijo rozetnih kamnov in univerzalnim okvirjem ∅→∆→∂→∮.

Ta priročnik ti bo pomagal razumeti vse funkcije in možnosti aplikacije.

---

## 📋 KAJ JE NOVO V v2.0

### 🎨 Izboljšave v v2.0:
- ✅ **Polna GUI aplikacija** s 8 zavihemi
- ✅ **Urejevalnik z avtomatskim dopolnjevanjem** markerjev
- ✅ **Preverjanje T1-T4 v realnem času**
- ✅ **Napredni iskalnik** po vseh dokumentih
- ✅ **Vizualizacija mreže** (DOT → PNG/HTML)
- ✅ **SQL poizvedbe** nad SQLite bazo
- ✅ **Izvoz v PDF, ZIP, JSON, HTML**
- ✅ **Podpora vseh markerjev** (∅, ∆, ∂, ∮, ⧖, ⟡, ∅↑, ∅↓, itd.)
- ✅ **Povezave med kamni**
- ✅ **Teme (temna/svetla)**
- ✅ **Bližnjice na tipkovnici**
- ✅ **Obvestila in priporočila**

---

## 🚀 HITRI ZAČETKI

### 1. Prva namestitev

```bash
# Prejmi produkcijo
cd D:\OntoProjekt\CanvasMinstral\Obj1

# Namesti zahtevane knjižnjice
pip install -r requirements.txt

# Namesti dodatne knjižnjice (opcijsko)
pip install markdown2 Pillow pyinstaller

# Zaženi aplikacijo
python sistem_gui_v2.py
```

### 2. Hitro učenje

1. **Generiraj nov kamen**: Odpri zavihe "Generiraj" → Vnesi številko, naslov, opis → Klikni "GENERIRAJ"
2. **Preveri T1-T4**: Odpri zavihe "Preveri" → Klikni "PREVERI VSE"
3. **Uredi dokument**: Odpri zavihe "Urejevalnik" → Izberi datoteko → Uredi in shrani
4. **Išči**: Odpri zavihe "Išči" → Vnesi iskalni izraz → Klikni "ISKI"

---

## 📑 ZAVIHE IN NJIHOVA UPORABA

### 📝 1. GENERIRAJ (Generiranje novih kamnov)

**Namestitev:**
- Ustvari nove kamne (CX, CXI, CXII, CXIII, CXIV, ...)
- Polna predloga z vsemi poglavji
- Minimalna predloga za hitro začetko
- Avtomatska posodobitev baze podatkov

**Kako uporabiti:**
1. Vnesi **številko** kamna (npr. 114)
2. Vnesi **naslov** (npr. "Labirint")
3. Vnesi **opis** (npr. "zapis kot pot")
4. Izberi **predlogo** (Polna ali Minimalna)
5. Klikni **"✨ GENERIRAJ KAMEN"**
6. Rezultat: Nov kamen dokument!

**Hitre izbire:**
- **CXIV (114): Labirint - zapis kot pot**
- **CXV (115): Zrcalo - zapis kot odsev**
- **CXVI (116): Vezava - zapis kot povezava**

**Tip:** Uporabi gumb **"➡️ GENERIRAJ + ODRI"** za hitro generiranje in urejanje!

---

### ✅ 2. PREVERI (Preverjanje T1-T4)

**Namestitev:**
- Preveri, ali dokumenti ustrezajo vsem 4 kriterijem
- Prikaz rezultatov v tabeli
- Podrobno poročilo o manjkajočih elementih

**Kriteriji T1-T4:**

| Kriterij | Pomen | primer |
|----------|-------|--------|
| **T1** | Vsi osnovni markerji | ∅, ∆, ∂, ∮ |
| **T2** | Vsaj 3 poudarjene besede | **pečat**, **DA₂**, **izročitev** |
| **T3** | Vsebuje tri globine | pečat, DA₂, izročitev |
| **T4** | Vsaj eno ∂ vprašanje | ∂ 68, ∂ 69, ∂ 70 |

**Kako uporabiti:**
1. Klikni **"🔎 PREVERI VSE"** - Preveri vsa dokumenta
2. Izberi datoteko in klikni **"📄 PREVERI IZBRANO"** - Preveri le izbrani dokument
3. Poglej rezultate v tabeli

**Prikaz rezultatov:**
- ✅ = Kriterij izpolnjen
- ❌ = Kriterij ni izpolnjen
- 🎉 **"VSIH X DOKUMENTOV PASIRA!"** = Vsi dokumenti so v redu!

---

### ✏️ 3. UREDNIK (Urejanje dokumentov)

**Namestitev:**
- Uredi obstoječe dokumente v realnem času
- Avtomatsko dopolnjevanje markerjev
- Hitri gumbi za vstavljanje markerjev
- Avtomatsko shranjevanje
- Preverjanje T1-T4 ob shranjevanju

**Kako uporabiti:**
1. Izberi datoteko iz razpadne menija
2. Klikni **"📖 OD_PRI"** za nalaganje
3. Uredi vsebino
4. Uporabi gumbce markerjev za hitro vstavljanje
5. Klikni **"💾 SHRANI"** ali pritisni **Ctrl+S**

**Markerji gumbi:**
- ∅ ∆ ∂ ∮ ⧖ ⟡ ⊗ ⊘ ⊢ ⟁ DA₂
- Klikni na gumb za vstavljanje markerja

**Tip:** Uporabi **Tab** za avtomatsko dopolnjevanje markerjev!

---

### 🗃️ 4. BAZA (Upravljanje baze podatkov)

**Namestitev:**
- Pregled vseh kamnov v bazi
- Podatki o kamnih, aksiomih, vprašanjih
- Osveževanje in statistika

**Kako uporabiti:**
1. Klikni **"🔄 OSVEŽI"** - Naloži podatke iz baze
2. Klikni **"📊 STATISTIKA"** - Prikaži statistiko sistema
3. Preglej tabelo s podatki

**Stolpci tabele:**
- **ID**: Identifikator kamna (npr. CX, CXI)
- **Naslov**: Naslov kamna
- **Status**: Stanje (NOV, ODPRT, IZROČEN)
- **Datoteka**: Ime datoteke
- **#**: Število aksiomov
- **Datum**: Datum ustvarjanja

---

### 🖼️ 5. VIZUALIZACIJA (Mreža povezav)

**Namestitev:**
- Ustvari DOT datoteko za vizualizacijo povezav
- Pretvorba v PNG (z Graphviz)
- Ustvari HTML prikaz mreže

**Kako uporabiti:**
1. Klikni **"📊 USTVARI DOT"** - Ustvari mreza.dot
2. Prikaz DOT kode v oknu
3. Klikni **"🎨 USTVARI PNG"** - Pretvori v sliko (potreben Graphviz)

**Pogoji:**
- Za PNG pretvorbo je potreben **Graphviz**
- Namestitev Graphviz:
  - Windows: Prejmi od [graphviz.org](https://graphviz.org/download/)
  - macOS: `brew install graphviz`
  - Linux: `sudo apt install graphviz`

**Alternativa:**
- Uporabi [Graphviz Online](https://dreampuf.github.io/GraphvizOnline/) za vizualizacijo DOT kode

---

### 🔎 6. POIZVEDBE (SQL Poizvedbe)

**Namestitev:**
- Izvedba SQL poizvedb nad SQLite bazo
- Pregled rezultatov v tabeli

**Kako uporabiti:**
1. Vnesi SQL poizvedbo v polje
2. Klikni **"▶ IZVEDI POIZVEDBO"**
3. Preglej rezultate v tabeli

**Primeri poizvedb:**
```sql
-- Vsi kamni
SELECT * FROM kamni ORDER BY stevilka

-- Kamni z določenim statusom
SELECT * FROM kamni WHERE status = 'NOV'

-- Aksiomi
SELECT * FROM aksiomi WHERE id > 245

-- Vprašanja
SELECT * FROM vprasanja
```

---

### 🔍 7. IŠČI (Napredni iskalnik)

**Namestitev:**
- Išči po vseh MD dokumentih
- Prikaz rezultatov z vrstico in datoteko
- Iskanje markerjev

**Kako uporabiti:**
1. Vnesi iskalni izraz (npr. "∅", "∆", "pečat", "DA₂")
2. Klikni **"🔎 ISKI V VSEH"**
3. Preglej rezultate v oknu

**Posebne funkcije:**
- **"🎯 ISKI MARKERJE"** - Išči vseh markerjev hkrati
- **Razlikovanje velikih/malih črk** - Vklopiš z gumbom "A/a"

**Tip:** Uporabi **Ctrl+F** za hitro odpiranje iskalnika!

---

### 📤 8. IZVOZ (Izvoz dokumentov)

**Namestitev:**
- Izvoz v različne formate
- Izvoz posameznih ali vseh dokumentov

**Formati izvoza:**

| Format | Opis | Gumb |
|--------|------|------|
| **PDF** | Izvoz v PDF format | 📄 IZVOZI V PDF |
| **ZIP** | Arhiv vseh MD datotek | 📦 IZVOZI VSE MD |
| **JSON** | Izvoz baze podatkov | 🗃️ IZVOZI BAZO |
| **DOT** | Izvoz mreže | 📊 IZVOZI DOT |

**Kako uporabiti:**
1. Izberi format
2. Izberi ime izhodne datoteke
3. Klikni gumb za izvoz

**Opombe:**
- Za PDF izvoz potrebuješ **markdown2** ali **weasyprint**
- Namestitev: `pip install markdown2 weasyprint`

---

### ❓ 8. POMOČ (Priročnik in informacije)

**Namestitev:**
- Priročnik za uporabo
- Seznam vseh markerjev
- Bližnjice na tipkovnici

**Vsebina:**
1. **📖 Priročnik** - Osnovne funkcije in navodila
2. **🔤 Markerji** - Seznam vseh markerjev z opisi
3. **⌨️ Bližnjice** - Seznam vseh bližnjic

---

## ⌨️ BLIŽNJICE NA TIKOVNICI

| Bližnjica | Dejanje | Opis |
|-----------|---------|------|
| **Ctrl+N** | Nov kamen | Odpre dialog za nov kamen |
| **Ctrl+O** | Odpri | Odpre datoteko v urejevalniku |
| **Ctrl+S** | Shrani | Shrani trenutno datoteko |
| **Ctrl+V** | Preveri vsa | Preveri vsa dokumenta |
| **Ctrl+F** | Išči | Odpre iskalnik |
| **Ctrl+Q** | Izhod | Zapre aplikacijo |
| **F1** | Pomoč | Odpre zavihe Pomoč |

---

## 🔤 MARKERJI V SISTEMU

### Osnovni markerji (∅→∆→∂→∮)

| Marker | Ime | Pomen | Unicode | HTML | LaTeX |
|--------|-----|-------|---------|------|-------|
| ∅ | Praznina | Izvor, nič, prazen prostor | U+2205 | `&empty;` | `\emptyset` |
| ∆ | Razlika | Prehod, sprememba, razlika | U+2206 | `&Delta;` | `\Delta` |
| ∂ | Vprašanje | Rez, vprašanje, ločitev | U+2202 | `&part;` | `\partial` |
| ∮ | Povratek | Cikel, povratek, zaključek | U+222E | `&int;` | `\oint` |

### Razširjeni markerji

| Marker | Ime | Pomen | Kategorija |
|--------|-----|-------|-----------|
| ⧖ | Tiheon | Molk, praznina, ničnost kot izpolnjenost | tiheon |
| ⟡ | Resonanca | Odziv, resonanca, sozvočje | resonanca |
| ⊗ | Križ | Križišče, produkt, presečišče | operacije |
| ⊘ | Prazni krog | Prazna operacija, ničelna operacija | operacije |
| ⊢ | Izpeljava | Logična izpeljava, posledica | logika |

### Pečati in potrditve

| Marker | Ime | Pomen | Kategorija |
|--------|-----|-------|-----------|
| DA₂ | Pečat DA₂ | Potrditev, izročitev, sklenjen dogovor | pečati |
| ☑ | Kvadrat | Pečat, potrditev, checkbox | pečati |
| ✓ | Križec | Potrjeno, DA | pečati |
| ✗ | Križ | Zavrtnjeno, NE | pečati |

### Smeri in prehodi

| Marker | Ime | Pomen | Kategorija |
|--------|-----|-------|-----------|
| ∅↑ | Odprava | Odstranitev, prekinitev, uničenje | smeri |
| ∅↓ | Vrnitev v praznino | Reset, ponastavitev | smeri |
| ∆→ | Prehod naprej | Napredek, razvoj, rast | smeri |
| ∆← | Prehod nazaj | Povratek, razgradnja | smeri |

### Matematični simboli

| Marker | Ime | Pomen | Kategorija |
|--------|-----|-------|-----------|
| ≠ | Ne enako | Negacija, razlika | matematika |
| ≡ | Enako | Identiteta, enakost | matematika |
| ∈ | Pripada | Element množice | množice |
| ∉ | Ne pripada | Ni element množice | množice |
| ⊆ | Podmnožica | Hierarhija, vsebovanost | množice |
| ⊇ | Nadmnožica | Vsebovanje | množice |
| ∩ | Presek | Skupni del | operacije |
| ∪ | Unija | Združitev | operacije |

### Grške črke

| Marker | Ime | Pomen | Kategorija |
|--------|-----|-------|-----------|
| Δ | Delta | Razlika, prehod | grske |
| Ω | Omega | Celota, končnost | grske |
| α | Alpha | Začetek, izvor | grske |
| ω | omega | Končni rezultat | grske |

---

## 📊 STATISTIKA IN PREGLED

### Trenutno stanje sistema:
- **Kamni:** 13+ (CVII-CXVI+)
- **Aksiomi:** 250+
- **Vprašanja:** 70+
- **Markerji:** 30+
- **Datoteke:** 20+

### Povezave med kamni:
```
CVII (Lungta) → CX (Povratna zanka) → CXI (Večkratnost) → CXII (Palimpsest)
   ↓         ↑         ↓         ↓
CVIII (Palica) ← CIX (Geoglifi) ← CXIII (Zrcalo)
```

---

## 🎨 NASTAVITVE

### Teme

Aplikacija podpira dve temi:

1. **🌙 Temna tema** (privzeta)
   - Ozadje: #2e3440 (temno modro)
   - Besedilo: #e0e0e0 (svetlo sivo)
   - Poudarjeno: #88c0d0 (svetlo modro)

2. **☀️ Svetla tema**
   - Ozadje: #ffffff (belo)
   - Besedilo: #2e3440 (temno modro)
   - Poudarjeno: #3498db (modro)

**Kako zamenjati temo:**
1. Menu **Prikaz** → **Temna tema** ali **Svetla tema**
2. Tema se shrani za prihodnje zagon

---

## 🔧 TEHNIČNE ZAHTEVE

### Minimalne zahteve:
- **Operacijski sistem:** Windows 10/11 (64-bit)
- **Python:** 3.10 ali novejši
- **RAM:** 4 GB (priporočeno 8 GB)
- **Disk:** 500 MB prosto

### Zahtevane knjižnjice:
```
# Osnovne
pip install PySide6>=6.4.0

# Za PDF izvoz
pip install markdown2 weasyprint

# Za ikono
pip install Pillow

# Za build EXE
pip install pyinstaller
```

### Opcijska odvisnost:
- **Graphviz** - Za PNG vizualizacijo mreže

---

## 📦 BUILD EXE

### Koraki za build:

1. **Namesti PyInstaller:**
   ```bash
   pip install pyinstaller
   ```

2. **Ustvari ikono:**
   ```bash
   python create_icon.py
   ```

3. **Zgradi EXE:**
   ```bash
   pyinstaller Sistem_v2.spec --clean --onefile --windowed
   ```

4. **Izhod:** `dist/Sistem_v2.exe`

### Parametri PyInstaller:
- `--clean` - Odstrani predhodne datoteke
- `--onefile` - Vse v eno EXE datoteko
- `--windowed` - Brez konzole
- `--icon=icon.ico` - Uporabi ikono

---

## 🐛 REŠEVANJE TEŽAV

### Pogoste težave:

| Težava | Rešitev |
|--------|---------|
| PySide6 ni nameščen | `pip install PySide6` |
| PyInstaller ni nameščen | `pip install pyinstaller` |
| Graphviz ni nameščen | Namesti Graphviz iz [graphviz.org](https://graphviz.org) |
| markdown2 ni nameščen | `pip install markdown2` |
| EXE se ne zgradi | Preveri, ali so vse datoteke prisotne |
| Ikonica ne deluje | Ustvari ikono z `python create_icon.py` |
| Unicode napake | Namesti Python z UTF-8 podporo |

### Diagnostika:

1. **Preveri nameščene knjižnjice:**
   ```bash
   pip list
   ```

2. **Preveri Python različico:**
   ```bash
   python --version
   ```

3. **Testiraj PySide6:**
   ```bash
   python -c "from PySide6.QtWidgets import QApplication; print('PySide6 OK')"
   ```

---

## 📚 DODATNI VIR

### Dokumentacija:
- **PRIROCNIK.md** - Osnovni priročnik sistema
- **STANJE-SISTEMA-POLNO-18092026.md** - Trenutno stanje sistema
- **PREDLAGE-ZA-KONSISTENTNO-RAZLAGANJE.md** - Predlogi za razumevanje

### Pomembne datoteke:
- **sistem_gui_v2.py** - Glavna GUI aplikacija
- **Sistem_v2.spec** - PyInstaller specifikacija
- **database.json** - Baza podatkov (JSON)
- **sistem.db** - Baza podatkov (SQLite)
- **tools.py** - Orodja za delo z dokumenti
- **db_manager.py** - Upravljanje baze
- **markerji_extended.py** - Simbolski register
- **create_icon.py** - Ustvari ikono

---

## 🎯 NASVETI IN TRIKI

### 1. Hitro generiranje kamnov
- Uporabi **hitro izbiro** gumbov za generiranje novih kamnov
- Gumb **"➡️ GENERIRAJ + ODRI"** hitro odpre urejevalnik

### 2. Avtomatsko shranjevanje
- Aplikacija avtomatsko shrani vsakih 30 sekund
- Vedno shrani ročno s **Ctrl+S**

### 3. Iskanje po dokumentih
- Uporabi **Ctrl+F** za hitro iskanje
- Išči po **markerjih** s posebnim gumbom

### 4. Vizualizacija mreže
- Za najboljše rezultate namesti **Graphviz**
- Uporabi [Graphviz Online](https://dreampuf.github.io/GraphvizOnline/) za hitro vizualizacijo

### 5. Preverjanje T1-T4
- Vedno preveri dokument pred shranjevanjem
- Aplikacija te avtomatsko opozori na manjkajoče elemente

---

## 📞 PODPORA

### Kontakt:
- **Avtor:** Luka + Vibe
- **Sistem:** ∅→∆→∂→∮ v2.0
- **Datum:** 19. 9. 2026

### Poročanje napak:
1. Preveri, ali so vse zahtevane knjižnjice nameščene
2. Preveri, ali so vse datoteke prisotne
3. Poskusi ponoviti operacijo
4. Preveri konzolo za napake

---

## 🔮 PRIHOJNOST

### Prihodnje funkcije:
- [ ] Avtomatsko dopolnjevanje v urejevalniku
- [ ] Podpora za večka datotek hkrati
- [ ] Sinhronizacija z oblakom
- [ ] Mobilna aplikacija
- [ ] Sodelovalno urejanje
- [ ] Učenje z AI
- [ ] Generiranje poizvedb z naravnim jezikom

---

## 📜 ZGODOVINA RAZLIČIC

| Različica | Datum | Spremembe |
|-----------|-------|-----------|
| **v1.0** | 18. 9. 2026 | Osnovna GUI aplikacija |
| **v2.0** | 19. 9. 2026 | Polna GUI z vsi funkcijami |

---

## 🎉 ZAKLJUČEK

SISTEM ∅→∆→∂→∮ v2.0 je **polna namizna aplikacija** za delo s teorijo rozetnih kamnov. Z njo lahko:

✅ **Generiraš** nove kamne
✅ **Preverjaš** T1-T4 kriterije
✅ **Urejaš** obstoječe dokumente
✅ **Iščeš** po vseh dokumentih
✅ **Vizualiziraš** mreže povezav
✅ **Izvažaš** v različne formate
✅ **Upravljaš** bazo podatkov

**Uživaj v raziskovanju!** 🚀

---

*© 2026 SISTEM ∅→∆→∂→∮ - Vse pravice pridržane*
