# Rez 87 — ZLOGOVNO TKIVO
## Sled v mesu, tkanina na koži: znakovni n-grami znotraj žetonov

Nadaljevanje: rez 83 (superpozicija) → 84 (Zipf-podpis) → 85 (n-gram-vez, naklon) → 86 (vez-n-gram: šiv, ki ga senca nima) → 86-rek (o-definiran: vez v znaku, invarianta 15 %) → **87 (zlogovno tkivo)**.

Luka: »daj« + »kaj in kako ti naj pomagam?« — izvedba ∂ iz rez 86-rek: **ZNAKOVNI TRIGRAMI + INVARIANTA 15 % PRI STO PREMEŠAVAH**. Test je tekel na celotnem transkriptu, s kontrolo 4 dokumentov in s sto premešavami.

---

## 1. Jedro

86-rek je izmeril znakovno vez čez cel tok (ΔH 0,159 bita) in sklenil: *vez, ki je ni v besedi, JE v zlogu.* Ta rez prereže zlog sam — bigrami in trigrami **znotraj** žetonov, ločeno od mej, s sto premešavami znakovnega reda znotraj vsakega žetona.

**Rezultat dvojen in pošten:**

| Plast | senca ΔH | kontrola ΔH | razmerje | sodba |
|---|---|---|---|---|
| žetonski bigram (rez 86, 1 nula) | 0,041 | 0,280 | 1 : 6,8 | izmenljivo |
| znakovni bigram, celi tok (86-rek) | 0,159 | 1,084 | 1 : 6,8 (~15 %) | vez na mejah |
| **znakovni bigram V zlogu (87, 100 premešav)** | **0,013 (2,3σ, znotraj intervala)** | **0,773 (~172σ, pod vsemi)** | **1 : 59** | **SLED** |
| **znakovni trigram V zlogu (87, 100 premešav)** | **0,107 (~10σ)** | **1,161** | **1 : 11** | **robustno majhno** |

**Invarianta 15 % ne preživi prenosa v zlog:** razmerje pade z 14,7 % na 1,7 % (bigram) oziroma 9,2 % (trigram). Invarianto so nosili znaki, ki se dotikajo **čez robove** žetonov — ločila, zapiralna družina (rez 85), foliacija — ne znakovni red znotraj njih.

> Vez, ki jo je 86-rek našel v znaku, živi **na koži zloga**. V mesu je sled.

---

## 2. Metoda (ponovljiva)

- **Vir:** celoten transkript — 99.001 znakov, 6 zaporednih čitkov. Reproducibilnost proti rez 85: 21.597 žetonov ✓, 4.257 vrstic ✓, io;o ×14 surovo / ×9 kot žeton ✓, tcr ×2 ✓.
- **Tokenizacija (rez 86 projekcija):** vrstica = enota; ločila odstranjena na robovih žetona (io;o ostane cel); male črke; čisti simbolni žetoni odpadejo → **15.885 žetonov**, od tega **8.366 večznakovnih** in **7.519 enočrkovnih (47 %!)** — senca je na ravni žetona že razrezana.
- **Znakovni n-grami znotraj žetonov** (ne prečkajo žetonov): bigrami 21.847 (različnih 2.321 = 10,6 %), trigrami 13.481 (različnih 8.394), abeceda 84.
- **Nula:** Fisher–Yates premešava znakov **znotraj vsakega žetona** — isti žetoni, isti znaki, uničen notranji red. **100 premešav**, deterministični LCG (seme 555777333). Rez 86: ena premešava na žetonski ravni; ta rez nulo spusti eno raven navzdol in jo pomnoži s sto.
- **Kontrola:** 4 slovenska dokumenta BreaKing (eno-to, ontofíza, gnostika-i, seciranje-mithos; 55.189 znakov, 7.669 žetonov — komparabilno seriji 49–52 tisoč; izbor zapisan po imenih).

## 3. Rezultati

**Senca:** H(X₂|X₁) 4,6993 proti nuli 4,7125 (σ 0,0057; interval 4,6972–4,7287) → ΔH 0,0132 (aktualna ZNOTRAJ intervala sto premešav — krhko). H(X₃|X₁X₂) 3,0077 proti 3,1150 (σ 0,0106) → ΔH 0,1073 (~10σ — robustno majhno). Ponovljivi bigrami 0,9626 proti 0,9641 — brez obogatitve (−0,0015).

**Kontrola:** H(X₂|X₁) 3,5384 proti 4,3116 (σ 0,0045; 4,3013–4,3225) → ΔH 0,7732 (~172σ; aktualna pod VSEMI stotimi premešavami). H(X₃|X₁X₂) 2,4017 proti 3,5622 → ΔH 1,1605. Ponovljivi 0,9931 proti 0,9859.

**Pari v zlogu (lift, prag ≥ 10 pojavov):**

| par | pojavi | lift | branje |
|---|---|---|---|
| io | 170 | **0,97** | naključno — i in o hodita skupaj, kolikor hoče naključje |
| tc | 44 | 0,52 | pod naključjem |
| tr | 64 | 1,02 | naključno |
| ct | 78 | 0,92 | naključno |
| cr | 56 | 2,05 | šibko |
| ;o / o; | 37 | **13,0** | vez JE v ločilu (P(o|;) 4,8× iz 86-rek potrjeno v zlogu) |
| :o | 29 | 11,4 | ločilo |
| fe | 214 | **12,2** | največja črkovna grudica — roka bralca / OCR |
| 10 / 11 | 69 / 38 | 18,5 / 18,1 | foliacija |
| 00 | 12 | 10,9 | OCR |

Trigrami: io; ×17, o;o ×29, **tcr ×2** (skoraj nič).

**io;o — končna secirka:** io naključen (0,97), vez v ;o (13,0), ponovitev ×14. Grudica = ponovitev + ločilna vez. Ne črkovna sintaksa.

## 4. Varovalo degeneracije

Premešava znotraj žetona ohranja identiteto in frekvenco žetona. Žeton, ki se ponovi, šije vedno iste trigrame — **del trigram signala je degeneriran s pojavnico** (Zipf, rez 84). Nove plasti je razlika nad to degeneracijo; zapisano pošteno.

## 5. Rodovniki

- **ZLOG** (prasl. *slogъ ← zložiti) — zlog je ZLOŽENO: enota, ki je sama že rez v besedi. Rez 87 reže rez.
- **MARKOV 1913 ∮** — 23. 1. 1913 je štel ČRKE Onjegina, ne besede. Rez 86 je meril besede, 86-rek znakovni tok, ta rez se vrne na Markovovo lastno raven: **črka–zlog–beseda = trije nivoji istega vprašanja.**
- **SHANNON 1951** — ~2,3 bita na črko pri osmih črkah konteksta; kontrola 2,40 na trigramu diha v istem razredu.
- **SLED** — kar pod premešavo ostane delno. Meja med sledjo in tkivom je red velikosti, ne mnenje: 2,3σ znotraj intervala = sled; 172σ pod vsemi = tkivo.
- **GRUDA** (rez 83/86) — ponovitev brez notranje sintakse.

## 6. Aksiomi

- **A1** notranja vez je merljiva nad lastno nulo (pogojna entropija znakov znotraj žetona).
- **A2** nula je premešan znakovni red znotraj žetona (rez 86 nulo spuščena eno raven navzdol).
- **A3** sled ni tkivo (1 : 59 bigram, 1 : 11 trigram — red velikosti ločuje, ne prag po okusu).
- **A4** instrument nosi svoj interval (sto premešav namesto ene — 86-rek pred vrata, izvedeno).
- **A5** del signala je degeneriran s pojavnico (ponovljeni žetoni šijejo konsistentne trigrame).

## 7. Nujne napake

1. 0,013 bita = vez — ne: znotraj intervala sto premešav.
2. 0,107 bita = jezik v zlogu — ne: 11× pod kontrolo, del degeneriran s pojavnico.
3. Invarianta 15 % = zakon — ne: ne preživi prenosa v zlog (1,7 % / 9,2 %); bila je merilo mej, ne mesa.
4. io;o kot črkovna vez — ne: io 0,97; vez v ;o in v ponovitvi.
5. Primerjava absolutnih H čez korpusa — abecedi 84 proti 111; merjiva Δ proti lastni nuli.
6. Sto premešav = omota — interval, ne gotovost.
7. Kontrola po izboru te seje — imena zapisana, komparabilna seriji.

## 8. Vaje

- **T1 premešaj besedo** — jaz → zaj: katera beseda tvojega dneva preživi premešavo? Črkovni red je spomin, ki se izgubi v treh črkah.
- **T2 svoj fe** — napiši sto besed svoje roke, preštej pare, ki hodijo skupaj. Vsak pisec ima svoj OCR.
- **T3 meja sledi** — kje postaviš prag med sledjo in tkivom: 2,3σ ali 10σ? Odločitev o pragu je etična, ne statistična.
- **T4 enočrkovni dan** — 47 % žetonov sence je enočrkovnih. Koliko tvojih dnevnih dejanj je enočrkovnih: gibi brez notranjega reda?

---

## Naslednji ∂ predlagan

**PROSTRANSKI N-GRAMI NA FAKSIMILU** — zadnja neizmerjena vez (P6: če kodeks veže okoli 87 ilustracij, so linearni, žetonski in zlogovni testi slepi po zasnovi). **Za izvedbo potrebuje faksimil: visokoločljive skene strani (Hamburg 2015 ali drug vir) ali transkripcijo s koordinatami leg znakov.**

**Pred vrata:** celi tok pri sto premešavah (izolacija spusta v zlog od števila premešav — χ odprt) · sto premešav na žetonski ravni (interval za Δ reza 86) · homogenost kodeksa (prva proti drugi polovici — roka, piro, sušilo) · dolžinski spekter žetonov (47 % enočrkovnih kliče po rezaju).

---

∴✓ (rez 86-rek — obe ∂ izvedeni, invarianta prerežena z merili, A0: mejna vez ostaja dejstvo; rez 86, 85, 84, 83 — veriga cela; rez 22 — datoteka pred sporočilom: števec je rekel #77, ne #76) ∆«zlogovno-tkivo: tkivo zloga je sled — bigram 0,013 bita znotraj intervala, trigram 0,107 bita ~10σ, kontrola 0,773/1,161 pod vsemi stotimi; invarianta 15 % živela na koži (mejah), ne v mesu; io;o secirana do konca: ponovitev + ločilo; Markov ∮ črka–zlog–beseda» ∫✓ (rezi 83–86-rek ostajajo cela — osma globina istega reza; nič zbrisano) ⊘(κ .85 — reproducibilnost ✓, metoda zapisana; χ .78 — dve spremembi hkrati, izolacija odprta; μ .72 — T1–T4 takoj; ℜ .04 — dvostranska nevarnost: mistika 0,107 in razočaranje nad invarianto; ν .77 — cena: rez je prerez lastnega pozitiva serije) ⊢ **DOKAZ #77 → S₇₇** (rez 87; števec preverjen pred pečatom: #76 rez 86-rek. NASLEDNJI PROSTI DOKAZ: #78. NASLEDNJI PROSTI REZ: 88. Števec živi v rezi datoteki.)