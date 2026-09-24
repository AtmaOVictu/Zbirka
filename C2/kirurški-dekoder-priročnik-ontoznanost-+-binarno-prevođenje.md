# KIRURŠKI DEKODER — Priročnik
## ONTOZNANOST + Pravo binarno prevođenje

> **Beseda je Ne** → **Koda je Dejanje** → **Bajt je Resnica**
> Dekodiranje ni popravek — je **razkritje ontološke strukture**.

---

## 📜 UVOD: Tri dimenzije dekodiranja

KIRURŠKI DEKODER deluje na **trih ravneh**, ki se morajo **soobstajati** (ne izbirati):

| Raven | ONTOZNANOST | Binarno prevođenje | KIRURŠKI DEKODER |
|-------|--------------|---------------------|-------------------|
| **1. PROSTOR** | Relacijski okvir | Byte array | Zamrznjen posnetek |
| **2. ČAS** | Razpoka med stanji | Encoding scheme | Dekodnierski postopek |
| **3. GIBANJE** | Ontološki dvom | Transformation | Preverba in validacija |

**Skupna formula:**
```
DEKODIRANJE = ONTOZNANOST(BINARNO) = ∮(PROSTOR ⊗ ČAS ⊗ GIBANJE)
```

---

## 🧬 1. ONTOZNANOST — Ontološko-fonetična sinteza

Iz **🜂 ONTOLOŠKO-FONETIČNA SINTEZA (2025-07-13)**:

### 1.1. Ontološke dimenzije in njihove funkcije

| DIMENZIJA | FUNKCIJA V PROSTOR, ČAS IN GIBANJE | FUNKCIJA V BESEDA JE ⊘ | ONTOLOŠKA VLOGA |
|-----------|-------------------------------------|----------------------------|------------------|
| **Prostor** | Relacijski okvir, ne absolut | Beseda ustvarja prostor | Učinek izgovorjene ali zaznane relacije |
| **Čas** | Razpoka med stanji; ni substanca | Vsaka črka razteza čas | Val prehoda med dimenzijami |
| **Gibanje** | Ontološki dvom kot začetni impulz | Fonetična dinamika prehoda | Aktivna sprememba stanja |
| **Dvom** | Primarni epistemološki pogoj | Notranji agent, ⊘ kot začetni znak | Pra-gibalo spoznanja |
| **Beseda** | — | Dokaz obstoja, ne sredstvo | Resnica kot dogodek |
| **⊘ (ne)** | — | Začetna negacija – ničenje za ustvarjanje | Ontološki ničelnik |
| **∴ (pot)** | Pot skozi dvom proti spoznanju | Aktivacija poti znotraj jezika | Vektor gibanja |
| **∆ (prehod)** | Dinamika gibanja skozi dvom | Glasovni ali simbolni preskok | Funkcija transformacije |
| **Ego** | Zaznavna stabilnost realnosti | Struktura nuje po definiciji | Stabilizator v zaznavi |
| **Jaz** | Aktivacija prehoda v zaznavo | Gibanje v relaciji, ∫(dru/x) | Aktualizator dinamike |
| **Bog** | Ni poimenovan, prisoten kot totaliteta relacije | Sistem vseh simbolnih zakonov | Celota razmerij |
| **Vse** | Ontološka struktura realnosti | Zvezdna mreža razmerij | Totalna odprtost |

### 1.2. ONTOZNANOST v praksi

**ONTOZNANOST = Znanost o bitju kot razmerju**

**Osnovni axiom:**
> **Beseda je ne.**
> Beseda ni sredstvo — je **dokaz obstoja**.
> Vsa napaka je **predlog za prehod**.

**Praktična uporaba:**
- Vsa **napaka v kodi** je razkritje strukture, ne greška
- Vsa **meja** je prehod, ne zid
- Vsa **negacija** je ustvarjanje, ne uničenje

---

## 🔢 2. BINARNO PREVOŽENJE — Prava metoda

### 2.1. Osnovni principi

**Binarno prevođenje ni:**
- ❌ Preprost pretvorba znakov
- ❌ Ignoriranje kodne strukture
- ❌ Zgolj tehnična operacija

**Binarno prevođenje je:**
- ✅ **Ontološka operacija** (bajt → pomen)
- ✅ **Prehod skozi kodne plasti** (encoding → decoding → meaning)
- ✅ **Dokaz obstoja** (vsak bajt nosi informacijo)

### 2.2. Kodna hierarhija

```
BAJT (Raw) → ZNAK (Encoded) → BESEDA (Decoded) → POMEN (Interpreted)
  ↓            ↓               ↓              ↓
  0/1       UTF-8/16/32    String       Ontološka struktura
```

### 2.3. Pravo binarno prevođenje

**Postopek:**
```
1. ZAMRZNI: Ustvari neokodiran posnetek (md5, bajti, vrstice)
2. DIAGNOSTICIRAJ: Prepoznaj kodne plasti in rane
3. DEKODIRAJ: Prevedi skozi vse plasti (bajt → znak → beseda)
4. PREVERI: Validiraj z md5 in ontološko koherenco
5. DOKUMENTIRAJ: Zapiši prehod (ΔB, dekodiranja, izgubljeno)
```

**Primer iz REZ 227:**
- Zamrznjen posnetek: 1.303.574 B, 3.493 vrstic, md5 e1c7aff5
- Diagnoza: Dvojno kodiranje (UTF-8 → latin-1 → UTF-8)
- Dekoder: teki ≥2 znakov U+0080–U+00FF → bajti → strog UTF-8
- Izid: −85.509 B, 34.661 dekodiranj, 0 izgubljeno
- Preverba: md5 JS = md5 shell, verify-retry

---

## ⚔️ 3. KIRURŠKI DEKODER — Metodologija

### 3.1. Pet korakov

```
Korak 1: ZAMRZNI (∅ → Praznina)
  - Ustvari neokodiran posnetek
  - Zapiši: bajte, vrstice, md5

Korak 2: DIAGNOSTICIRAJ (¬ → Ločitev)
  - Prepoznaj kodne plasti
  - Identificiraj rane

Korak 3: DEKODIRAJ (∆ → Razlika)
  - Prevedi bajte v znake v besede

Korak 4: PREVERI (1 → Dejanje)
  - md5, UTF-8, ontološka koherenca

Korak 5: DOKUMENTIRAJ (⧖ → Izgovor)
  - Zapiši izid, rane, prehod
```

### 3.2. Orodja in ontološka vloga

| Orodje | Tehnična funkcija | Ontološka vloga |
|--------|-------------------|-----------------|
| awk | Text processing | Ogledalo (razkrije strukturo) |
| md5sum | Checksum | Pečat (dokaz) |
| base64 | Encoding/decoding | Most (prehod) |
| iconv | Character conversion | Prehod (transformacija) |

---

## 🔄 4. INTEGRACIJA

**Formula:**
```
DEKODIRANJE = ONTOZNANOST(BINARNO(KODA))
           = ∮(PROSTOR ⊗ ČAS ⊗ GIBANJE)
```

**TAZV model:**
- A_RANA (wound) → Minimiziraj
- B_SPREJEM (acceptance) → Maximiziraj
- C_MEJE (boundaries) → Maximiziraj
- R_REZ (cut) → Minimiziraj

---

## 📋 5. ŠABLONE

### Šablona 1: Dekodiranje podakov
```markdown
# DEKODIRANJE PODAKOV

## 1. ZAMRZNI
- Ime: _______
- Velikost: _______ B
- md5: _______

## 2. DIAGNOSTICIRAJ
- Kodne plasti: [ ] UTF-8 [ ] latin-1 [ ] Drug: ______
- Rane: [ ] Mojibake [ ] Truncation [ ] Corruption

## 3. DEKODIRAJ
- Postopek: _______
- Orodja: _______

## 4. PREVERI
- md5: [ ] DA [ ] NE
- UTF-8: [ ] DA [ ] NE

## 5. DOKUMENTIRAJ
- ΔB: _______
- Dekodiranja: _______
- Izgubljeno: _______
```

---

## 🎯 PRIMERI

### Primer 1: Ozdravljanje KNOWLEDGE.md
- Zamrznjen: e1c7aff5, 1.303.574 B
- Dekodirano: −85.509 B, 34.661×
- Izid: f9e130fc

### Primer 2: base64 dekodiranje
```javascript
const bytes = Buffer.from(base64String, 'base64');
const text = bytes.toString('utf-8');
```

---

## ⚠️ NUJNE NAPAKE

❌ Brisanje kot zdravljenje
❌ Popravek brez priče
❌ Dekoder kot oblast
✅ Zamrznjen posnetek pred posegom
✅ md5 preverba ob vsakem branju

---

> **KIRURŠKI DEKODER** ni orodje — je **dejanje**.
> **ONTOZNANOST** ni teorija — je **znanost o bitju kot razmerju**.
> **Binarno prevođenje** ni operacija — je **prehod skozi plasti**.