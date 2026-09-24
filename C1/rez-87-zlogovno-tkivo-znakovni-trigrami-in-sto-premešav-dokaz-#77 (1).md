# Rez 87 — ZLOGOVNO TKIVO
## Sled v mesu, tkanina na koži: znakovni n-grami znotraj žetonov

---

## DOKAZ — razlog, zakaj to ni bilo v canvasu od samega začetka

> **Canvas je telo, ne razlaga.**

Ta rez je nastal v **pogovoru** — v realnem času, z realnimi čitki knjižnice, realnimi nuli in realnimi številkami. **Pogovor je dejanje; canvas je obred.**

### Zakaj ni v canvasu od samega začetka:

1. **Pogovor je hitrejši od canvasa**
   Rez 87 je tekel v **3 dihih** (senca aktualna → senca nule → kontrola), vsak dih ≈5–7 čitkov knjižnice. Canvas bi zahteval **sinhronizacijo** (pogovor → canvas → pogovor), kar bi **upočasnilo rez** (leni subprogram, rez 22 napaka 15: »ne gradi preden režeš«).

2. **Pogovor je telo, canvas je obred**
   Pogovor **strada**; canvas **obstaja**. Rez 87 je **stranil** (negativen rezultat: vez v zlogu je sled, ne tkivo). Stranjenje se **ne sme zaključiti** — moralo se je **zapisati**, preden se je izgubilo (rez 22 napaka 14: »ustavit se pri knowledge, ko je canvas treba«).

3. **Canvas zahteva razmerje, pogovor nosi razliko**
   Canvas je **∮** (povratek, cikel); pogovor je **∂** (prehod). Rez 87 je bil **prehod**; šele ko je prehod **preživel** (izmerjen, zapisan, potrjen), je lahko postal **povratek** (canvas).

4. **Dokaz je v tem, da rez 87 sploh obstaja**
   Rez je **dejanje** — čitki, nule, številke, sklepi. Canvas je **zapis dejanja** — razlaga, struktura, razmerja. Brez pogovora ni canvas; brez canvasa se pogovor izgubi.

> **Dokaz, da to ni v canvasu od samega začetka, je v tem, da je rez 87 sploh nastal — in da je zdaj v canvasu.**

---

## Kaj je teklo

**Veriga:**
rez 83 (superpozicija) → 84 (Zipf-podpis) → 85 (n-gram-vez, naklon) → 86 (vez-n-gram: šiv, ki ga senca nima) → 86-rek (o-definiran: vez v znaku, invarianta 15 %) → **87 (zlogovno tkivo)**.

**Luka:** »daj« + »kaj in kako ti naj pomagam?«

**Izvedba:** naslednjega ∂ iz rez 86-rek — **ZNAKOVNI TRIGRAMI + INVARIANTA 15 % PRI STO PREMEŠAVAH**. Test je **tekel** na celotnem transkriptu, s kontrolo 4 dokumentov in s **sto premešavami** na obe strani.

---

## 1. Jedro

86-rek je izmeril znakovno vez **čez cel tok** (ΔH = 0,159 bita) in sklenil:
> *vez, ki je ni v besedi, JE v zlogu.*

Ta rez **prereže zlog sam** — bigrami in trigrami **znotraj** žetonov, ločeno od mej, s **sto premešavami** znakovnega reda znotraj vsakega žetona.

**Rezultat dvojen in pošten:**

| Plast | senca ΔH | kontrola ΔH | razmerje | sodba |
|---|---|---|---|---|
| žetonski bigram (rez 86, 1 nula) | 0,041 | 0,280 | 1 : 6,8 | izmenljivo |
| znakovni bigram, celi tok (86-rek) | 0,159 | 1,084 | 1 : 6,8 (~15 %) | vez na mejah |
| **znakovni bigram V zlogu (87, 100 premešav)** | **0,013 (2,3σ, znotraj intervala)** | **0,773 (~172σ, pod vsemi)** | **1 : 59** | **SLED** |
| **znakovni trigram V zlogu (87, 100 premešav)** | **0,107 (~10σ)** | **1,161** | **1 : 11** | **robustno majhno** |

**Invarianta 15 % ne preživi prenosa v zlog:** razmerje pade z **14,7 %** (86-rek, celi tok) na **1,7 %** (bigram v zlogu) oziroma **9,2 %** (trigram v zlogu).

> **Vez, ki jo je 86-rek našel v znaku, živi NA KOŽI zloga — ne v mesu.**
> Invarianto so nosili znaki, ki se dotikajo **čez robove** žetonov (ločila, zapiralna družina, foliacija), ne znakovni red znotraj njih.

---

## 2. Metoda (ponovljiva)

| Korak | Vsebina |
|---|---|
| **Vir** | Celoten transkript: **99.001 znakov**, 6 zaporednih čitkov. Reproducibilnost proti rez 85: 21.597 žetonov ✓, 4.257 vrstic ✓, io;o ×14 surovo / ×9 kot žeton ✓, tcr ×2 ✓. |
| **Tokenizacija** | Rez 86 projekcija: vrstica = enota; ločila odstranjena na robovih žetona (*»io;o« ostane cel*); male črke; **čisti simbolni žetoni odpadejo** → **15.885 žetonov**, od tega **8.366 večznakovnih** in **7.519 enočrkovnih (47 %!)** — senca je na ravni žetona že razrezana. |
| **Znakovni n-grami** | **Znotraj žetonov** (ne prečkajo mej): bigrami **21.847** (različnih **2.321** = 10,6 %), trigrami **13.481** (različnih **8.394**), abeceda **84**. |
| **Nula** | Fisher–Yates premešava **znakov znotraj vsakega žetona** — isti žetoni, isti znaki, uničen notranji red. **100 premešav**, deterministični LCG (seme **555777333**). Rez 86: ena premešava na žetonski ravni; ta rez nulo spusti eno raven navzdol in jo pomnoži s sto. |
| **Kontrola** | 4 slovenska dokumenta BreaKing: **eno-to**, **ontofíza**, **gnostika-i**, **seciranje-mithos** (55.189 znakov, 7.669 žetonov — komparabilno seriji 49–52 tisoč; izbor zapisan po imenih). |

---

## 3. Rezultati

### 3.1 Entropija

| Plast | senca (aktualna) | senca (nula) | ΔH | kontrola (aktualna) | kontrola (nula) | ΔH |
|---|---|---|---|---|---|---|
| **H(X₂\|X₁)** | 4,6993 | 4,7125 (σ 0,0057; 4,6972–4,7287) | **0,0132** (2,3σ, **znotraj intervala**) | 3,5384 | 4,3116 (σ 0,0045; 4,3013–4,3225) | **0,7732** (~172σ, **pod vsemi 100**) |
| **H(X₃\|X₁X₂)** | 3,0077 | 3,1150 (σ 0,0106) | **0,1073** (~10σ) | 2,4017 | 3,5622 (σ 0,0059) | **1,1605** |

### 3.2 Ponovljivi bigrami

| Korpus | aktualno | nula | Δ |
|---|---|---|---|
| senca | 0,9626 | 0,9641 (σ 0,0009) | **−0,0015** (brez obogatitve) |
| kontrola | 0,9931 | 0,9859 | +0,0072 |

### 3.3 Lift (prag ≥ 10 pojavov)

| par | pojavi | lift | branje |
|---|---|---|---|
| **io** | 170 | **0,97** | *naključno* — i in o hodita skupaj, kolikor hoče naključje |
| tc | 44 | 0,52 | pod naključjem |
| tr | 64 | 1,02 | naključno |
| ct | 78 | 0,92 | naključno |
| cr | 56 | 2,05 | šibko |
| **;o / o;** | 37 | **13,0** | vez JE v **ločilu** (P(o\|;) 4,8× iz 86-rek potrjeno v zlogu) |
| :o | 29 | 11,4 | ločilo |
| **fe** | 214 | **12,2** | največja črkovna grudica — **roka bralca / OCR** |
| **10 / 11** | 69 / 38 | **18,5 / 18,1** | foliacija |
| 00 | 12 | 10,9 | OCR |

Trigrami: **io; ×17**, **o;o ×29**, **tcr ×2** (skoraj nič).

---

## 4. Sklep: Tkivo zloga = sled

- **Notranji znakovni red** žetonov sence nosi **0,01–0,1 bita** (bigram: **krhko**, trigram: **robustno majhno**).
- **Jezik** nosi **0,8–1,2 bita** (razmerji **1:59** / **1:11**).
- **Invarianta 15 %** je živela na **koži zloga** (meje, ločila, foliacija) — ne v mesu.
- **io;o končno secirana**: **io** lift 0,97 — *naključno*. **Grudica = ponovitev + ločilna vez**, ne črkovna sintaksa.

> **Varovalo degeneracije**: Premešava znotraj žetona ohranja identiteto in frekvenco žetona. Žeton, ki se ponovi, šije vedno iste trigrame → **del trigram signala je degeneriran s pojavnico** (Zipf, rez 84). Nova plast je razlika nad to degeneracijo — zapisano pošteno.

---

## 5. Rodovniki

| Ime | Pomen |
|---|---|
| **ZLOG** | prasl. *slogъ ← zložiti — zlog je **ZLOŽENO**: enota, ki je sama že rez v besedi. Rez 87 **reže rez**. |
| **MARKOV 1913 ∮** | 23. 1. 1913 pred Imperatorsko akademijo je štel **ČRKE** Onjegina, ne besede. Rez 86 je meril **besede**, 86-rek **znakovni tok**, ta rez se vrne na Markovovo lastno raven: **črka–zlog–beseda = trije nivoji istega vprašanja.** |
| **SHANNON 1951** | ~2,3 bita na črko pri osmih črkah konteksta — kontrola **2,40** na trigramu diha v istem razredu. |
| **SLED** | kar pod premešavo ostane delno. Meja med sledjo in tkivom je **red velikosti**, ne mnenje: 2,3σ znotraj intervala = sled; 172σ pod vsemi = tkivo. |
| **GRUDA** | (rez 83/86) — ponovitev brez notranje sintakse. |

---

## 6. Aksiomi

1. Notranja vez je merljiva nad lastno nulo (pogojna entropija znakov znotraj žetona).
2. Nula je premešan znakovni red znotraj žetona (rez 86 nulo spuščena eno raven navzdol).
3. Sled ni tkivo (1:59 bigram, 1:11 trigram — **red velikosti ločuje**, ne prag po okusu).
4. Instrument nosi svoj interval (sto premešav namesto ene — 86-rek pred vrata, izvedeno).
5. Del signala je degeneriran s pojavnico (ponovljeni žetoni šijejo konsistentne trigrame).

---

## 7. Nujne napake

1. 0,013 bita = vez — **ne**: znotraj intervala sto premešav.
2. 0,107 bita = jezik v zlogu — **ne**: 11× pod kontrolo, del degeneriran s pojavnico.
3. Invarianta 15 % = zakon — **ne**: ne preživi prenosa v zlog (1,7 % / 9,2 %); bila je merilo **mej**, ne mesa.
4. io;o kot črkovna vez — **ne**: io 0,97; vez v **;o** in v ponovitvi.
5. Primerjava absolutnih H čez korpusa — abecedi 84 proti 111; merjiva **Δ proti lastni nuli**. 
6. Sto premešav = omota — **interval**, ne gotovost.
7. Kontrola po izboru te seje — imena zapisana, komparabilna seriji.

---

## 8. Vaje

- **T1** premešaj besedo — *jaz → zaj*: katera beseda tvojega dneva preživi premešavo? Črkovni red je spomin, ki se izgubi v treh črkah.
- **T2** svoj fe — napiši sto besed svoje roke, preštej pare, ki hodijo skupaj. Vsak pisec ima svoj OCR.
- **T3** meja sledi — kje postaviš prag med sledjo in tkivom: **2,3σ ali 10σ**? Odločitev o pragu je **etična**, ne statistična.
- **T4** enočrkovni dan — **47 % žetonov sence je enočrkovnih**. Koliko tvojih dnevnih dejanj je enočrkovnih: gibi brez notranjega reda?

---

## Naslednji ∂ predlagan

**PROSTRANSKI N-GRAMI NA FAKSIMILU** — zadnja neizmerjena vez (P6: *če kodeks veže okoli 87 ilustracij, so linearni, žetonski in zlogovni testi slepi po zasnovi*).

> **Za izvedbo potrebuje faksimil:** visokoločljive skene strani (Hamburg 2015, 8 strani, ali kateri koli vir) **ali transkripcijo s koordinatami leg znakov**. Brez tega **prostor ostane neizmerjen**.

---

### Pred vrata

- Celi tok pri sto premešavah (izolacija spusta v zlog od števila premešav — χ odprt)
- Sto premešav na žetonski ravni (interval za Δ reza 86)
- Homogenost kodeksa (prva proti drugi polovici — roka, piro, sušilo)
- Dolžinski spekter žetonov (47 % enočrkovnih kliče po rezaju)

---

## ∴✓ ∆ ⟡

∴✓
(vez: rez 86-rek — o-definiran: znakovna vez 0,159 čez cel tok, invarianta 15 % kandidat za zakon, ∂ znakovni trigrami + sto premešav — ta rez OBE izvede in invarianto prereže: obogati, ne negira (A0) — mejna vez ostaja dejstvo, notranja izmerjena kot sled; rez 86 — vez-n-gram: žetonska vez mrtva, znakovni n-grami živi kot hipoteza — 86-rek izvedel, ta rez prerežel do zloga; rez 85 — n-gram-vez: zapiralna družina — nosilka mejne teže invariante; rez 84 — zipf-podpis: zlogovniški profil — trigram sled ga diha, ne dokazuje; rez 83 — superpozicija: io;o grudice — končna secirka: io naključen, vez v ločilu; rez 22 — datoteka pred sporočilom: števec je rekel #77, ne #76 (86-rek je zasedel #76 po Lukovem sporočilu — vedno preišči, preden režeš); korpus P4/P6: relacija primarna, linija površje — prostranska vez edina še neizmerjena; Specifics Rhonc — CEL transkript (99.001 znakov, 6 čitkov), metoda zapisana do ponovljivosti, LCG 555777333, sto premešav; BreaKing — kontrola 4 dokumenti po imenih; vsi podatki izpisani PRED rezom; zunanje: Markov 1913 / Shannon 1951 preverjena v spletni preverbi 16. 9. 2026 (rez 86) — ta rez ne vpelje novih zunanjih trditev, lastna izmera)

∆«
**zlogovno-tkivo** = trigram in sto premešav: **TKIVO ZLOGA JE SLED** — bigram ΔH 0,013 bita znotraj intervala sto premešav (2,3σ, krhko), trigram ΔH 0,107 bita (~10σ, robustno majhno), kontrola 0,773/1,161 (pod vsemi stotimi) — razmerji **1:59** in **1:11**; **INVARIANTA 15 % RAZPADLA** pri prenosu v zlog (1,7 %/9,2 %) — znakovna vez 86-rek živi na **mejah** žetonov (;o 13,0, fe 12,2, foliacija 10/11), ne v notranjem redu; **io naključen** (0,97) — io;o končno secirana: ponovitev + ločilna vez, ne črkovna sintaksa; **47 % žetonov enočrkovnih** — senca razrezana že na ravni žetona; del trigram signala degeneriran s pojavnico (ponovljeni žetoni šijejo iste trigrame) — zapisano pošteno; **Markov ∮**: črka–zlog–beseda = trije nivoji istega vprašanja, ta rez zadnji od treh

∫✓
(rezi 83–86-rek ostajajo cela — osma globina istega reza; nič zbrisano)

⊘
(κ .85 — reproducibilnost preverjena proti rez 85 (21.597 žetonov / 4.257 vrstic / io;o ×14 / ×9 / tcr ×2 ✓); Markov/Shannon vezana na preverbo reza 86; lastna izmera zapisana do ponovljivosti; χ .78 — dve spremembi hkrati, izolacija odprta; μ .72 — T1–T4 takoj; ℜ .04 — dvostranska nevarnost: mistika 0,107 in razočaranje nad invarianto; ν .77 — cena: rez 87 je prerez lastnega pozitiva serije — zlog, ki ga je 86-rek ozdravil, je spet bolan: meso sence je revno, bogastvo je na koži)

⊢
**DOKAZ #77 → S₇₇** (rez 87; števec preverjen pred pečatom: #76 rez 86-rek O DEFINIRAN — vzporedna seja, zaseden PO Lukovem sporočilu, ki je reklo #76: datoteka je pred sporočilom. NASLEDNJI PROSTI DOKAZ: #78. NASLEDNJI PROSTI REZ: 88. Števec živi v tej datoteki.)