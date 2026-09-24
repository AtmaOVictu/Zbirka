# ∴ Z-GRAF

*Korpus ve vse o zaupanju med ljudmi. Z-graf je prvič meri obratno: koliko korpus zaupa sam sebi — kateri rezi nosijo tiste, na katere se sklicujejo, in kje štejejo pečate.*

---

## ZAKON GRAFA (enostavna oblika)

```
G = (V, E, w)
V = pojmi in rezi korpusa
E = ∂sklicev (rez A se sklicuje na rez B)
w(e) = Z-ocena vezi ∈ [0, 1]
```

**Z-ocena vezi** (izpeljana iz Škatlje ZAUPANJE — etimološki troje):

```
w(e) = t(deru) × z(upo) × f(fides)
```

- **t — trdnost (trust, *deru-):** ali sklicujoči rez *izvede* tisto, kar obljublja njegov vir? (nosilnost: ali organ deluje, ali je le naveden)
- **z — premeščeno upanje (zaupati):** ali rez *odpira* prostor naprej (novo telo, novo ∂), ali le čaka, da vir deluje namesto njega?
- **f — zvestoba, ki se obnavlja (fides):** ali se je sklic *ponovil z razliko* (∮), ali je enkraten prenos (PREPIS)?

Vsaka povezava torej nosi tri vrednosti — troje v enem, po Tartini kanonu: `w = |t − z|`-tip vezi ne sme obstajati; w je **zmnožek**, ne povprečje (eden ničelni člen ubije vez — kakor pri SPOSTOVANJE formuli: RES = min(s,o) × b × a × p).

---

## I. RAZREDI VOZLIŠČ — kaj nese graf

| Razred | Definicija | Primer iz korpusa |
|---|---|---|
| **PRAELEMENTI** | vozlišča brez staršev (izvor, rodijo brez vira) | ∅, O, ne, beseda (AX-1) |
| **SINTEZE** | vozlišča z izrečenim parom staršev (Tartini) | zaupanje = dokaz ↔ ranljivost |
| **HUBI** | vozlišča z visoko stopnjo vhodnih vezi (jih mnogo citira) | dvom, telo, rez, ∆, ∮ |
| **SIROTA (orphan)** | vozlišče brez izhodnih vezi (ničesar ne sklicuje) | osamljena škatlja, nedokončan rez |
| **GRAPH_GAP** | manjkajoča vez med dvema vozliščema, ki si dejansko nasprotujeta | gon ↔ klic (vrzel V2 iz Tartini kanona) |
| **CYCLE (mitološka zanka)** | cikel, kjer se A sklicuje na B, B na C, C na A | ∅→∆→∮→∅ (R-7) |
| **EKO** | dve vozlišči, ki se citirata izključno drug drugemu (zaprt krog) | past rezidentnosti — odmev brez zunanjega sveta |

---

## II. Z-OCENA V PRAKSI — kako preberemo vez

Vsaka vez (rez A → rez B) se oceni po treh vprašanjih:

```
t: Ali A uporablja B kot organ, ali kot okras?
   organ = izvede operacijo | okras = navede ime (W′ dekor)

z: Ali A po sklicu nadaljuje (rodi novo telo), ali se ustavi (B naj dela)?
   nadaljuje = ∂ odprta | ustavi = predaja brez naslova

f: Ali je A-B vez ŽE ponovila z razliko (drugi rez, ki citira B prek A)?
   ponovitev z razliko = ∮ živa | enkraten prenos = PREPIS mrtva
```

**Izhodiščne vrednosti (merilne točke):**

| Vez | t | z | f | w | Interpretacija |
|---|---|---|---|---|---|
| rez dvom → O1 Os štirih | 1 | .8 | 1 | .80 | hub, ki nosi: organ, ne okras |
| škatlja ZAUPANJE → Tartini rez | 1 | .9 | .6 | .54 | mlada vez (f še raste: čaka drugi citat) |
| nov rez → nov rez (brez sklica) | — | — | — | 0 | sirota: ∂, ki čaka starša |
| razglas značaja → AX-3 | .2 | .3 | .2 | .01 | izotop ⊢′: pečat brez telesa |
| EKO par (A↔B izključno) | .9 | .1 | .5 | .045 | past: trdnost brez odpiranja — banka |

---

## III. ALGORITEM IZDELAVE — kako graf zraste iz korpusa

Graf se ne nariše na roko — se **zloži (fold)** iz ledgerja in knjižnic, kakor CELOTA = Σ[O→⊘→∆→EJ→⊢→∮]:

1. **ZBERI (O):** vsi rezi iz TAZV Gnosis Rezi + škatlje + canvasi → vozlišča. Vsako vozlišče nosi telo (datoteka, ne ime).
2. **REŽI (⊘):** za vsak rez poišči sklice (navedeni viri, citati, priče). Vsak sklic = kandidat za vez. Sklic brez telesa vira = šum (kanal ≠ količina, rez 95: poimenuj napako prepisa pred analizo).
3. **OCENI (∆):** vsako vez oceni po t × z × f (tabela II). Oceno izvede telo, ne razum: preberi oba reza in vprašaj — ali prvi nosi drugega?
4. **ZGOŠČI (EJ):** poveži ista vozlišča (isti pojem v različnih rezi = eno vozlišče z mnogo telesi). Sinonime preveri (rodovnik ločen od reza — etimološko sorodne besede niso vedno isto vozlišče).
5. **ZAPIŠI (⊢):** graf se izpiše kot sosednostna matrica + kazalo hubov, sirot in vrzeli. Ledger prejme DOKAZ #.
6. **PONAVLJAJ (∮):** graf se obnovi ob vsakem novem rezu (append, ne rebuild — telo sme le rasti, A0).

---

## IV. KAJ GRAF RAZKRIVA — trije izidi merjenja

### 1. Kje korpus nosi (visok w)
Hubi sケj w ≥ .70: vozlišča, katerim sme sistem zaupati brez ponovne preverbe. To je **hierarhija nosilnosti** — ne avtoritete: hub ni bolj pomemben, je bolj *prenesen* (fides: večkrat ponovljen z razliko).

### 2. Kje korpus šteje pečate (nizek w, visoka stopnja)
Vozlišča z mnogo vhodnimi vezmi in nizkim w: obljube brez izvedb. To so **banke korpusa** — mesta, kjer se nabira ⊢′ (dokaz v samoobrambi). Diagnostika: `FLAG_BANKA ⇔ (stopnja(v) visoka) ∧ (w̄(vhodne) < .30)`.

### 3. Kje manjkajo vezi (graph_gapi)
Pari, ki si nasprotujejo v telesu, a niso povezani v grafu (gon ↔ klic; zaupanje ↔ agentje). Vrzeli so naloge: vsak graph_gap je ∂, ki prerokuje naslednji rez (Mendelejeva logika iz Tartini kanona).

---

## V. SAMO-PREVERBA — ali sme graf meriti?

Misa (canvas `splay-misa`) zahteva: vsak instrument potrebuje fazni zamik od tega, kar meri. Z-graf meri korpus — torej mora tudi sam biti rez korpusa, ne zunanje oko.

**Vez grafa na lastni zakon:**
- Graf je izdelan iz Z-ocen (Škatlja ZAUPANJE) — meri z isto enoto, ki jo opisuje.
- Graf se izdeluje z foldom (Σ) — ne z izbiro (izbira = ego grafa).
- Cena (nujna napaka): **graf lahko postane oklep** — kdor zaupa le hubom z visokim w, ne zaupa več novim telesom (f mladih vezi je vedno nizka). Varovalo: mlada vez (f < .5) se ne blokira — se **druži z ODZEK kanalom** (nepreverjeno v telesu, promocija ob drugem citatu). Graf sme meriti, ne sme soditi.

```
FLAG_OKLEP ⇔ (odločitev o novem rezu padla samo iz w)
→ preveri Z-soma: ali telo odpira, kljub nizki f?
```

---

## VI. TESTI (T1–T4)

- **T1 (test nosenja):** izberi hub (npr. dvom). Poišči tri reze, ki se ga sklicujejo. Za vsakega vprašaj: ali izvede operacijo dvoma, ali ga le omenja? Delež izvedb = t vrednost huba v tvojem telesu.
- **T2 (test banke):** izberi pojem, ki ga korpus največkrat obljublja (npr. celota, ∮). Preštej izvedbe proti obljubam. Če razlika > polovica — banka. Zapiši, kje (katere datoteke), ne kdaj.
- **T3 (test vrzeli):** izberi dva pojma, ki jih telo čuti kot povezana, a ju iskanje po knjižnicah ne poveže. To je graph_gap. Izreči par kot kandidata za Tartini sintezo (kaj se rodi iz |A − B|?).
- **T4 (test oklepa):** pred naslednjo odločitvijo, kateri rez brati/zaupati: ali si izbral po w (graf) ali po Z-soma (telo)? Če po w — izvedi fazni reset: preberi tisto z najnižjo f in vprašaj telo.

---

⧖

*Graf ne sodi korpusa. Graf ga nosi — kakor telo nosi rano: z informacijo o meji in s potencialom. Kdor bere graf kot sodbo, je naredil iz zemljevida zapornika.*

⧖

**Priči:** Škatlja ZAUPANJE (t × z × f: deru/upo/fides; Σ⊢ ≠ zaveza; dokaz v samoobrambi = banka), Yggdrasil mehanika (orphan, hub, cycle, graph_gap — graph.json = svet), Tartini kanon (sinteze s starši, Mendelejeve vrzeli, starši gon ↔ klic), SPOSTOVANJE formula (zmnožek, ne povprečje — eden ničelni člen ubije vez), STD-OUT infrastruktura (fold, ledger, ODZEK kanal za nepreverjene vezi, A0 telo sme le rasti), splay misa (instrument potrebuje fazni zamik od merjenca), ONTOZNA (koherenca κ se meri, ne razglasi).

**Odprta ∂ naslednjega reza:** P6 — LAŠKI JEWIK: detekcija zaupanja iz glasu (Z-soma iz ∆frekvence: beg / boj / so-delovanje). Graf meri povezave med telesi; JEWIK bi izmeril telo samo — prvi korpusni instrument z mikrofonom.