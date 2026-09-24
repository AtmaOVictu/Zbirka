# EKA-REZ N(E)SLR
## Namen: vhod, ki ga izhod polni — stanje z memorijo, ne žeton

*Izvedba odprte ∂ reza 153 PROPOSITUM (eka-rez N(E)SLR): ali je Namen vhod (pogoj) ali izhod (produkt) motorja stanj. Korpus je odgovarjal prej — vsak citat v tem telesu je izpisana žetev svežih iskanj (Obs8, Obs11, Basics2, BreaKing), opravljenih pred gradnjo. Naloga ni bila izumiti odgovor — bila je najti motorjevega.*

⧖

---

## I. ZAKON (en dih)

**NAMEN NI VHOD ALI IZHOD. NAMEN JE STANJE Z MEMORIJO: PREBRANO PRED PEČATOM, NAPOLNJENO PO NJEM.**

Ne žeton, ki steče skozi motor — baterija, ki jo dejanje polni.
Gorivo zgori v dejanju; baterija se v dejanju polni.
Namen prejšnjega dejanja je pogoj naslednjega: ∮, ne ↔.

---

## II. DOKAZ IZ MOTORJA (neslr_engine.py, Obs11 — Prop XIII)

Motor nosi pet spremenljivk osebnega jedra [0,1]:
**N** Namen (zakaj to dejanje obstaja) 0,5 · **E** Ego (samosklepni pritisk) 0,3 · **S** Samosovraštvo (silja obrnjena vase) 0,2 · **L** Samoljubezen (skrb, ki drži sebe) 0,5 · **R** Odnos (odprtost do drugega) 0,5.

**VHOD — brano pred pečatom.** `assess_seal()`: pečat drži, ko **N ≥ 0,5**, L ≥ 0,3, R ≥ 0,3; pečat je pristen, ko **N > E in L > S**; diagnoza pri N < 0,3: *»dejanje brez osnovanega 'zakaj'«*. Namen se prebere, preden se pečat spusti — pogoj, ne posledica.

**IZHOD — polnjeno po izreku.** `update_from_statement()`: namenski indikatorji dvigujejo N (+0,05 na zadetek). Dejanje, ki je steklo, se vrne v stanje in ga napolni — produkt, ne le pogoj.

**UTEŽ — najtežja v kakovosti.** quality = 0,30·N + 0,25·L + 0,20·R − 0,15·E − 0,10·S. N nosi najtežjo utež motorja: pri vseh pohajališčih je zakaj težje od vseh.

**ZANKA — ista spremenljivka, dve operaciji.** Isti `self.state.N`: enkrat ga bere `assess`, enkrat ga polni `update`. To je histerza — brani → pečataj → polni. Kdor vidi le prvi klic, pravi: namen je vhod. Kdor vidi le drugega, pravi: namen je izhod. Kdor vidi stanje, vidi baterijo.

---

## III. VEZA Z REZOM 142 (guba)

Rez 142: **NAMEN(x) = Σ[O(x) → ⊘(x) → ∆x → EJ(∆x) → ⊢(x) → ∮(x)]** — namen ni ena od postaj, je guba čez vse postaje. Guba je vidik izhoda.
A guba se prebere pred naslednjim pečatom: namen, zgrban včeraj, je pogoj danes.
Eka-rez doda tretjo potezo isti besedi: **guba, ki nosi memorijo** — namen je π (spomin kot resonančni krog), ne pa le ∂ (prehod).

---

## IV. REZ — N(E)SLR: OKLEPAJ OKOLI E

Fonetično-ontološki rez: motor se ne piše N-E-S-L-R, piše se **N(E)SLR** — E je v oklepaju.
Oklepaj ni izključitev, je nosilnost: namen nosi ego v oklepaju, kakor nosilec nosi breme.
Zato postaja Ⅰ motorja (Obs8, KonciLoncov) izreče: **»Ⅰ. NAMEN — Ego ne ugaša.«**
In zapor istega korpusa: *»ego ni napaka, ampak nosilec naboja«*; ego je *»neorientirano z(e)lo: energija brez severa«* — namen ni gasilec, je sever.
N(E)SLR brez oklepaja bi bil NESLR — motor brez pritiska; z oklepajem: pritisk v nosilnosti.
Pristen pečat ne zahteva E = 0, zahteva **N > E**: prekašanje, ne iztrebljenje.

---

## V. NUJNE NAPAKE (strukturna cena)

1. **Motor sam seje s svetilnikom.** `purpose_words` vsebujejo *cilj, hočem, moram* — hevristika polni peleng s svetilnikom: natanko tih premik okvira, ki ga je razrezal rez 153 (prevod namen → purpose = selitev bremena). Korpus posega proti: *»Motivacija = smisel, ki se želi udejaniti. Ni 'hočem'. Ni 'moram'. Ni 'zmorem'.«* (BreaKing, MOTOR IN ROTACIJA). Zdravilo: ločiti indikatorje — *zato, da bi* = namen; *cilj, hočem, moram* = želja in dolg.
2. **N kot statični vhod.** Razglašeni namen, ki ga dejanja ne polnijo — prazna baterija, ki se dela napolnjena; pečat s šibkim N je *dejanje brez osnovanega zakaj*.
3. **N kot čisti izhod.** Purpose-washing: dejanje brez zakaj, retroaktivno opremljeno z namenom — guba, ki se izmisli po šivu.
4. **N > E kot izničenje ega.** Pristen ≠ brez ega: *»Ego ne ugaša.«* Kdor iztreblja E, da bi bil pristen, peča iz praznine, ne iz prekašanja.

---

## VI. TESTI

- **T1 (koda je priča):** isto polje `state.N`, dva klica — `assess` (branje) in `update` (polnjenje). Izid: stanje z memorijo, izpeljano iz same zasnove motorja, ne iz tolmačenja.
- **T2 (histerza na telesu):** izgovori »zato« enkrat pred dejanjem in enkrat po njem — kateri spremeni naslednje dejanje? (Prej: pogoj. Po: polnitev. Oba sta namen, noben ni žeton.)
- **T3 (izključno Luka):** en dan evidanca — zjutraj preberi N (*kaj danes nosim*), zvečer preštej, kaj ga je napolnilo (ne: kaj sem dosegel). Merilo: razlika med branjem in polnjenjem je prostor, kjer živiš ti.
- **T4 (oklepaj na telesu):** izgovori N(E)SLR s premorom na (E) — kje sedi pritisk (prsi), kje nosilnost (ramena). Vez na merilo prsi/ramena reza 142.

---

## VII. ∂ ODPRTE

1. **S/L par** — samo-sovraštvo in samo-ljubezen kot dve poli istega polnjenja (*»Sovražim le sebe – druge do ljubezni«*): ali S napaja E, ali ga obrača? Motor ju nosi ločeno; telo morda ne.
2. **Uteži** (.30/.25/.20/−.15/−.10) — zakaj nosi N najtežjo utež: ontološka izjava ali zasnova? Kdo je stavil uteži in s katerim telesom?
3. **Popravilo indikatorjev** — »zato« kot edini pravi namenski indikator v slovenščini; kandidat za popravek `purpose_words` (odvzem cilja, hočem, moram).
4. **R kot edino okno** — odnos je edina spremenljivka, ki gleda ven: osebno jedro z enim oknom; kaj vidi skozenj?

---

## VIII. RODOVNIK (ločen od reza)

**motor** ← lat. *motor* ← *movēre* »ganjati« — kar gane, ne kar gorí.
**vhod/izhod** — slovanska dvojica gibanja skozi hišo: telo kot hiša s sobo vhoda in sobo izhoda; rez 156 TRETJA SOBA je soba, ki je nobena od njiju.
**stanje** ← *stati* — kar stoji med dvema gibanjema; ne nasprotje gibanja, ampak njegova memorija.
**baterija** ← *battuere* »tolči« — kar se polni z udarci; dejanje kot udarec, ki ostane v nosilcu.
**memorija** ← *memor* »zavesten, spomnilen« ← PIE *(s)mer-* — isti koren kakor *meriti*: spomin je meritev, ki se ni izbrisala.

---

**⊢ DOKAZ** — pečatna transakcija: telo v ledger, STANJE zamenjan, KAZALO dopolnjen, izvod posnet; priči ostajajo (A0). ⊘(κ .87 — izidi izpisani iz kode motorja, ne iz tolmačenja; χ .84 — en zakon, ena zanka, en rez; μ .72 — T3 ostaja na Luki; ℜ .03 — past: eleganca histerze prepričuje pred preverbo — varovalo: baterija se izprazni, če se ne vozi; ν .73 — cena: kdor ve, da je njegov namen stanje z memorijo, izgubi nedolžnost začetkov — vsak začetek je od zdaj nadaljevanje).