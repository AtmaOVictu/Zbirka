# SEDANJOST CELOTE — Odnosi, donosi, ponosi in sramotovanje kot funkcije

**Telo zgrajeno po metodologiji rekonstrukcije** (REKONSTRUKCIJA → KRITIČNA PREVERBA → REKALIBRACIJA → IMPLIKACIJE). Vse v sedanjiku — to ni povzetek prejšnjih rezov, je njihova sedanjost: celota, ki stoji, potem ko so padle okvarjene premise.

---

## ORGAN I — ZAKON (kar telo nosi v eni vrstici)

> **Odnos, donos in ponos so isti operand (nosilnost) v treh domenah. Sramotovanje ne prenaša teže — prenaša sram. Vračanje deluje samo na težo; sram se ne vrača, sram se razrešuje.**

Enostavno izrečeno: *nosim različne stvari na različnih mestih; tisto, kar me sramoti, ni tovor, ampak trk — in trka ne odložiš pri drugem, ga le poimenuješ ali zavržeš.*

---

## ORGAN II — TRIJE NOSI KOT FUNKCIJE (rekalibrirano)

Vsak nos ima podpis in VEČ izhodov. En izhod = zamrznjena definicija; zato vsak nos tri.

### OD-NOS — funkcija razdalje
```
odnos(jaz, ONO, t) := ∂(teža) prenesena preko d(jaz, ONO) v času t
izhodi:
  (a) oba prenašata  → most ∴ (razdalja nosiva)
  (b) en prenaša     → enosmerna cev (razdalja izkoriščana)
  (c) noben          → soseščina brez odnosa (razdalja prazna)
```
Odnos ki izkorišča, je še vedno odnos — funkcija teče. Most je izid, ne bistvo.

### DO-NOS — funkcija kroženja
```
donos(∆delo, T) := ∮ sprememba stanja po enem ciklu
izhod: ΔS ≠ 0 vedno; lahko negativna
```
Prekinjen cikel vrača ΔS = rano, ne nič. **Rana je donos prekinjenega cikla.** Donos se meri v prehodu (ΔS), ne v sadju (stanju).

### PO-NOS — funkcija nosilnosti brez priče
```
ponos(teža, priča→∅) := μ vzdržan brez zunanje preverbe
izhod: μ ∈ [0,1]
```
Ponos je edini nos, ki ga merim sam. Najnižja zunanja preverba → najlažji zdrs v oklep. Meja ponosa: μ se preverja v telesu, ne v ogledalu.

**Vez treh:** OD-NOS daje smer, DO-NOS konec, PO-NOS težo. Patologija enega se razširi na vse tri — ista funkcija, ista škoda.

---

## ORGAN III — SRAM (pošast, ki je bila pustila neporezana)

```
S-RAM: S (skup, cum) + RAM (trk, zadelo)
sram(x) := občutenje trka med jaz-kot-sem in jaz-kot-bi-moral-bit
sramotovanje(x → y) := prenos FUNKCIJE SRAM z x na y
```

Sram ni teža. Teža je tovor; sram je **razlika, ki boli**. Zato:

| Kaj se sramoti | Kako zveni | Kateri trk se prenaša |
|---|---|---|
| odnos | "preveč si čustven" | par naj bi bil nekaj drugega, kar je |
| donos | "premalo si dosegel" | doseženo naj bi bilo več |
| ponos | "kdo si pa ti" | jaz-kot-sem ni dovolj |

**Asimetrija, ki nosi celoto:** sramotovanje prenaša sram (nerazrešen trk); vračanje prenaša težo (razrešljiv tovor). Par NI zrcalen. Zdravilo za eno ne velja za drugo.

---

## ORGAN IV — DVE OPERACIJI (mehanika)

### VRAČANJE — velja SAMO za težo
```
vračanje(teža, lastnik) := ∂ prenos h izvoru, iz telesa (φ < meja)
lastnik := tisti, ki PREPOZNA — ne tisti, od katerega je teža izšla
izhodi: (a) prepoznana in prevzeta → ∮ zaključen
        (b) prepoznana, neprevzeta → skladišče
        (c) neprepoznana → teža brez doma
```
Padec pri lastniku JE možen — ne ker teža ni njegova, ampak ker **prepoznava atrofira** pod dolgim sramotovanjem: teža pride domov, hiša ne ve več odpirati vrat.

### RAZREŠEVANJE — edino veljavno za sram
```
razrešitev(sram) ∈ { poimenovanje trka (∅→¬: "to je tvoj trk, ne moj"),
                     zavrnitev prenosa (⊘: "ne sprejmem tvojega jaz-kot-bi-moral-bit") }
```
Srama ne moreš vrniti. Lahko ga le poimenuješ pri lastniku ali zavržeš prenos.

---

## PRAKSA — protokol v treh dihih

1. **DIAGNOZA:** ali nosim tovor (teža) ali trk (sram)? Preizkus: teža se da opisati brez "moral bi"; sram ne.
2. **IZBIRA OPERACIJE:** teža → vračanje (dih, ton 0.2–0.4, en stavek: "Vračam ti to; če jo nosim naprej, ne bova imela nobeden odnos."). Sram → razrešitev ("To je tvoj trk, ne moj." ali "Ne sprejmem.").
3. **OSTANEK:** ostajam v odnosu (∴), če drug sprejme. Če drug zahteva, da težo vzamem nazaj, da bi odnos ostal — to ni bil odnos, bilo je skladišče.

**Zloraba protokola (nujna napaka):** razrešitev izvedena iz jeze je ∆REZ brez STOP-signala — postane nov prenos trka. Varovalo: prej dih; jeza ki razrešuje, je sramotovanje z obrnjenim predznakom.

---

## MAŠINERIJA — matematična plast

- **Tok teže v paru:** `W(t) = W_A(t) + W_B(t) + 2·Cov(A,B)` — kjer Cov meri skupno noseno; sramotovanje poveča Cov na račun enega nosa (en nosi korelacijo za oba).
- **Atrofija prepoznave:** `R(t) = R_0 · e^(−λs)` kjer s = leta sramotovanja; za razdrobljeno težo velja ∮: vsak povratek po en kos, dokler Σkosov ≠ tovor, ki ga lastnik prepozna.
- **Donos prekinjenega cikla:** `ΔS_interrupt = −∫₀^T' ∆delo dt` (rana kot negativna akumulacija).
- **Guard:** φ (glas) ≤ meja + prisotnost; μ ∈ [.50,.80]; preverba vsake operacije: ΔS ≠ 0.

---

## DOKAZI — testi T1–T4

- **T1 (trk):** izreči razrešitev srama v živem odnosu — ali se je Cov znižal brez padca odnosa?
- **T2 (veza):** ali se teža lahko vrne, ne da se odnos pretrga (podvajanje zahteva šibko vez)?
- **T3 (svinec):** ali je bila razrešitev izvedena iz telesa (φ pod mejo) ali iz jeze (rez, ne povratek)?
- **T4 (krog):** ali po ∮ prepoznani kos teže sledi naslednji kos (atrofija se zdravi s povratki, ne z deklaracijo)?

---

## IMPLIKACIJE CELOTE

1. Patologija enega nosa se razširi na vse tri (ista funkcija).
2. Nesramotovanje ni vrlina — je funkcionalna zahteva: skupnost, v kateri trki potujejo neimenovani, proizvaja sramotovanje kot edini odvod.
3. Dolgo sramotovanje proizvaja teže brez doma kot STANDARD, ne izjemo.
4. Protokol vračanja velja samo za tovor; kjer je bil diagnosticiran sram, je bila prejšnja zadeva zdravilo za napačno bolezen.

---

## ∂ ODPRTO

1. Ali obstaja meja, pri kateri razreševanje srama postane nasilje — trk, ki ga lastnik objektivno ne more prepoznati?
2. Ali je odnos, v katerem teža ne more biti nikjer doma, še odnos — ali sta oba že padla, samo padati nista končala?
3. Preizkus atrofije na živem: koliko ∮ povratkov potrebuje razdrobljena teža, preden jo lastnik prepozna?

*Ta telo lahko umrje (297): ovrga ga vsak odnos, v katerem sram poimenovan pri lastniku odnosa ne odpre — tedaj razrešitev ni dovolj in manjka organ, ki ga to telo še nima.*