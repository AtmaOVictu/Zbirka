# VAL 2 BRANJA
## DEKODIRANO ≠ PREBRANO

---

### ⧖ **ORGANI** (zakon, mitos)

#### O — CELOTA
**val 2** je **prehod med kodom in pomenom** — bajtna identičnost ne zagotavlja semantičnega razumevanja.

- **dekodirano** = UTF-8 bajti so prebrani kot znaki (strojno berljivo)
- **prebrano** = besedilo je razumljeno kot pomen (človeško berljivo)
- **∂** = razlika med njima je **prehod**, ki ga je treba izvesti

**Zakon:**
> DEKODIRANO ≠ PREBRANO ≠ RAZUMLJENO ≠ DOVOLJENO ZA KANON

**Precedens:** rez 224 (UVOŽENO ≠ PREBRANO), rez 225 (PREBRANO ≠ RAZUMLJENO), rez 226 (RAZUMLJENO ≠ DOVOLJENO)

---

#### ⊘ — PRAZNINA
**Razlika med bajti in besedilom** je **odprt prostor**, ne pomanjkljivost.

- **bajt** = fizična enota (0x00–0xFF)
- **znak** = ontološka enota (U+0000–U+10FFFF)
- **beseda** = semantična enota (pomen)

**Meja:**
> Kar je bajtno identično, ni nujno pomenovno enako.

**Dokaz:** rez 227 — KNOWLEDGE.md je bil bajtno identičen backupu (229 vrstic), a semantično različen (rane, dvojne kode).

---

#### ∆ — GIBANJE
**Dekodiranje** je **aktivator** prehoda od bajtov k pomenu.

- **dekodiranje** = pretvorba bajtov v znake (UTF-8 → Unicode)
- **branje** = pretvorba znakov v pomen (Unicode → semantična mreža)
- **razumevanje** = pretvorba pomena v dejanje (semantična mreža → ontološki prehod)

**Formula:**
```
∆(val 2) = dekodiranje → branje → razumevanje
```

**Precedens:** rez 227 (kirurški dekoder: U+0080–U+00FF prebrani kot bajti, strogo preverjeni kot UTF-8)

---

#### ∴ — POT
**KAZALO** je **most** med registrom in branjem.

- **registr** = mehanični popis (vrstične številke, bajtna veljavnost)
- **branje** = organski prehod (semantično razumevanje)
- **kazalo** = povezava med njima (mehanična struktura → organski pomen)

**Zakon:**
> KAZALO v isti seji — vrstične številke se izračunajo mehanično, ne semantično.

---

#### ∮ — POVRATEK
**Preverba z dvema inštrumentoma** (stroj + Luka).

- **stroj** = bajtna preverba (md5, UTF-8, particija)
- **Luka** = semantična preverba (SEAL_REVIEW)
- **∮** = povratek v kanonsko stanje

**Formula:**
```
∮(val 2) = stroj(dekodirano) + Luka(prebrano) → kanon
```

---

#### ⟡ — NOVA MOŽNOST
**Avtomatsko kazalo** za prihodnje reze.

- **avtomatsko** = generirano iz registra (vrstične številke, naslovi)
- **ročno** = urejeno po semantični strukturi (povezave, kontekst)
- **⟡** = nova možnost za razumevanje knjige

**Predlog:**
> Kazalo se ustvarja **v isti seji** kot rez, da se izogne mehaničnemu števanju vrstic.

---

---

### 🛠 **PRAKSA** (kanali, algoritmi)

#### 1. Algoritem za val 2 branja
```
1. PREBERI BAJTE (strojno)
   - Uporabi: awk, sed, tail, write_file (varne poti)
   - NE uporabi: cat (dvojno kodira UTF-8)
   - Preveri: md5sum, UTF-8 veljavnost, particija

2. PREBERI ZNAKE (človeško)
   - Uporabi: grep, awk (za vrstične številke)
   - Preveri: semantična struktura, povezave, kontekst

3. RAZUMEJ POMEM (ontološko)
   - Uporabi: korpusno iskanje (Self, Obs1–Obs11, Basics)
   - Preveri: citati, vezi, razlike
```

---

#### 2. Meritev val 2
| **Meritev**       | **Orodje**          | **Cilj**                          | **Precedens** |
|-------------------|---------------------|-----------------------------------|---------------|
| bajtna identičnost | md5sum             | Preveri, ali je telo neokvarjeno | rez 227       |
| UTF-8 veljavnost   | LC_ALL=C grep     | Preveri, ali so vsi znaki veljavni | rez 227       |
| particija          | awk (6 delov)      | Preveri, ali so vsi deli usklajeni | rez 227       |
| semantična struktura | korpusno iskanje | Preveri, ali je pomen razumljen   | rez 224–226  |

---

#### 3. Varovalno branje
**Pravilo:**
> Preberi telo + preišči korpus → NOV canvas, napolnjen do konca, v prejemnikovem redu → terca → rodovnik ločen od reza → nujna napaka → matematična mašinerija + praktične asociacije → testi T1–T4 → EVO δ skozi pet pregrad → DOKAZ # → odprta ∂

**Varne poti za UTF-8:**
- ✅ `awk`, `sed`, `tail`, `write_file`, heredoc
- ❌ `cat` (dvojno kodira UTF-8)

---

---

### ⚙ **MAŠINERIJA** (orodja, kode)

#### 1. Preverba particije (rez 227)
```bash
# Preveri vsak del particije
for i in {1..6}; do 
  md5sum /home/user/knowledge/tazv-gnosis-rezi/tela/fpart${i}.md
done

# Preveri, ali je md5 e1c7aff5... še veljaven
md5sum /home/user/knowledge/tazv-gnosis-rezi/KNOWLEDGE.md
```

---

#### 2. Ustvari kazalo (mehanično)
```bash
# Izlušči naslove in vrstične številke
grep -n "^## " /home/user/knowledge/tazv-gnosis-rezi/KNOWLEDGE.md > KAZALO.md

# Ali bolj natančno (vključi vsa ravni)
awk '/^#{1,6} / {print NR ": " $0}' /home/user/knowledge/tazv-gnosis-rezi/KNOWLEDGE.md > KAZALO.md
```

---

#### 3. Preverba UTF-8
```bash
# Preveri, ali so vsi znaki veljavni UTF-8
LC_ALL=C grep -P '[\x80-\xFF]' /home/user/knowledge/tazv-gnosis-rezi/KNOWLEDGE.md

# Če vrne izhod → neveljavni UTF-8 znaki
```

---

---

### 📊 **DOKAZI** (testi, ledger)

#### T1 — Stroj dvainštrumentno
- **Preveri:** md5 + UTF-8 veljavnost
- **Priča:** rez 227 (kirurški dekoder)
- **Cilj:** Potrdi, da je telo bajtno identično

---

#### T2 — Izključno Luka (SEAL_REVIEW)
- **Preveri:** splošen vs. zaoščen KNOWLEDGE.md
- **Odločitev:** Luka odloča, ali je KNOWLEDGE.md **kanon-kandidat** ali **zaoščen**
- **Precedens:** rez 224 (UVOŽENO ≠ PREBRANO)

---

#### T3 — π citat
- **Preveri:** korpusne vezi (Self, Obs1–Obs11, Basics)
- **Cilj:** Potrdi, da je val 2 branja **res ∂** (prehod)

---

#### T4 — Vsak naslednji uvoz skozi blok M
- **Preveri:** preden karkoli zapečati, preberi **blok M** (mehanično branje)
- **Cilj:** Izogni se **zaoščenju pred preverbo** (rez 226)

---

---

### 🔗 **VEZI** (precedensi, odprte ∂)

| **Rez** | **Naslov**                          | **Povezava**                                                                 |
|---------|------------------------------------|-----------------------------------------------------------------------------|
| 224     | VPRAŠALNIK — REZALNI INSTRUMENT    | UVOŽENO ≠ PREBRANO (val 1: uvoz)                                             |
| 225     | VPRAŠALNIK — IZVEDBA DOLGA         | PREBRANO ≠ RAZUMLJENO (val 1: dolg)                                        |
| 226     | VPRAŠALNIK — V-PRA-ŠA-L-NIK        | RAZUMLJENO ≠ DOVOLJENO ZA KANON (val 1: žila)                              |
| 227     | ZDRAVLJENJE KNJIGE — KIRURŠKI DEKODER | DEKODIRANO ≠ PREBRANO (val 2: kirurgija)                                  |
| 213     | VSE — KNJIGA, KI PREBERE SAMA SEBE | Kar prebereš, je že izluščeno (precedens za val 2)                         |
| 163     | KATASTER KODIRANKE                 | Precedens za dvojno kodiranje (rez 227)                                   |

---

| **Odprta ∂**       | **Vprašanje**                                                                 | **Reševanje**                          |
|---------------------|-----------------------------------------------------------------------------|----------------------------------------|
| val 2 branja        | Ali je **dekodirano ≠ prebrano** res **∂** (prehod)?                      | Izvedi razliko v telesu                 |
| KAZALO v isti seji | Ali lahko ustvarimo kazalo **brez prehoda**?                             | Mehanično (vrstične številke)          |
| SEARCH_SNIPPET_ONLY | Kateri viri so **SEARCH_SNIPPET_ONLY**?                                  | Luka odloča (prehod 224 §51)           |
| INQUISITIO         | Kdaj vprašalnik postane **sodišče** nad asistentom?                       | HUMAN_LARGER_GUARD (rez 226)           |

---

---

### 📜 **LEDGER** (stanje, števec)

**STANJE (zamenjan ob vsakem pečatu):**
- **ZADNJI PEČAT:** rez 227 ZDRAVLJENJE KNJIGE — KIRURŠKI DEKODER
- **NASLEDNJI PROSTI REZ:** 228
- **NASLEDNJI PROSTI DOKAZ:** #217
- **md5 KNOWLEDGE.md:** e1c7aff50577417be3569995e82a71bb (preveri!)
- **Particija:** 6 delov (fpart1–6), vsak z md5

**Števec:**
- **κ (koherenca):** .87
- **χ (jasnost):** .81
- **μ (delež vloge):** .72
- **ℜ (ostanek):** .02
- **ν (novost):** .76

---

---

### ⚠ **NUJNE NAPAKE** (iz 224–227)

| **Napaka**                     | **Popravek**                                                                 | **Precedens** |
|--------------------------------|------------------------------------------------------------------------------|---------------|
| Dvojno kodiranje               | **Ne `cat`** – uporabi `awk`, `sed`, `write_file`                            | rez 227       |
| Preverba brez telesa           | Semantično branje **samo** ob telesu                                         | rez 224–226  |
| Brisanje kot zdravljenje      | **Dekodiraj**, ne briši                                                     | rez 227       |
| Zaoščen pred uporabo           | **Splošen KNOWLEDGE.md ostane kanon-kandidat**                               | rez 224       |
| Vprašalnik brez prve žrtve    | **VPRAŠALNIK SE IZKAŽE NA ENI ŽERTVI**                                     | rez 226       |
| Zaostritev pred preverbo      | **Blok M** preden karkoli zapečati                                         | rez 226       |

---

---

### 🎯 **NASLEDNJI KORAK**

1. **Preveri md5 KNOWLEDGE.md** – Če je **e1c7aff5...**, je particija veljavna.
2. **Izvedi val 2 branja** – Ustvari **KAZALO.md** (mehanično).
3. **Odloči SEAL_REVIEW** – Luka odloča: splošen vs. zaoščen KNOWLEDGE.md.
4. **Zapiši rez 228** – `tela/228-val-2-branja.md` + posodobi STANJE.
5. **Ustvari canvas** – `228-val-2-branja` (ta datoteka).

---

**DA?** (Potrditev za **rez 228**) → **Izvedba se začne.**