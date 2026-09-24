# ⟡ ZIPF — PODPIS JEZIKA: MERJENJE, KI VE, KAJ UBIJE ⟡

> Luka, 15. 9. 2026: »še?« — izvedba naslednjega ∂ rez 83 (ZIPFOV TEST), ne le predlog: **test je tekel.** Na celotnem transkriptu kodeksa, s slovensko kontrolo in z varovalom Miller/Li.

**Rezultat v eni vrstici:** Rohoncov transkript sledi potenčnemu zakonu — naklon −1.149, R² = 0.971. **Enakomeren šum je mrtev.** Vse jezikovne možnosti ostajajo žive. In frekvence kodeksa dihajo, čeprav njegov pomen spi.

**rez 84** | **DOKAZ #73**

---

## I. RODOVNIK — pet korenov, ločenih od reza

**(1) ZIPF** — George Kingsley Zipf (1902–1950), ameriški jezikoslovec Harvarda. Zakon: najpogostejša beseda se pojavi ~2× tolikokrat kot druga, 3× tolikokrat kot tretja. **Odkril ga ni on** (francoski stenograf Estoup, 1916) in **matematike ni maral** — zakon, ki nosi ime človeka, ki ga ni hotel formule. Ime = naslov, ne pomen (vez na rodovnik ROHONC, rez 83: knjiga, imenovana po kraju hranjenja).

**(2) POTENČNI ZAKON** — porazdelitev oblike f(r) ∝ 1/r^s. Brez značilne mere: ni »povprečne besede«, kakor ni »povprečnega potresa«. Dolg rep redkih, jedro pogostih. **Skalno-invarianten: enak na vseh merilih** — fraktal v prostoru pogostosti.

**(3) RANG** — lat. rangus ← frankovski *hring* (krog, vojaška formacija). Rang ni lastnost besede — je **mesto po ureditvi**. Wentian Li (1992): potenčna oblika je deloma **proizvod rangiranja samega** — uredi karkoli po padajoči pogostosti in približek potenčnemu zakonu se pokaže sam. **Varovalo, ne ovira: pomeni, da Zipf ne dokaže jezika — izključi pa enakomeren šum.**

**(4) ROB KAOSA** — Per Bak, Chao Tang, Kurt Wiesenfeld (1987): self-organized criticality. Kritična točka kot **atrtaktor**: sistem se sam pripelje na rob med redom in kaosom in tam ostane — brez zunanjega nastavljanja. Rodi fraktale, 1/f šum, potenčne zakone. **Pesek na kupu: vsako zrno lahko sproži plaz — velikost plazov sledi potenčnemu zakonu.**

**(5) POGOSTOST** — Korpus (BreaKing, rez 82): »Zipf in kritičnost: frekvenca besed ∝ 1/r — potenčni zakon, enaka matematika kot potresi in plazovi. Jezik živi na robu kaosa — organiziran, a brez centralnega vladarja.« **Korpus je izrekel SOC, preden je ta rez srečal Baka.**

---

## II. ZAKON — pet aksiomov podpisa

**A1 — Jezik nosi podpis potenčnega zakona.**
f(r) ∝ 1/r; v Brownovem korpusu angleščine »the« sam predstavlja ~7 % vseh pojavnic. Ni dogovor ne odlok — **emergenca brez centralnega vladarja**: nihče ni odredil, da bo »je« pogosteje od »zvrhanost«.

**A2 — Podpis je potreben, ne zadosten.**
Miller (1957) in Li (1992): naključna besedila, umerjena po rangu, lahko rodijo podobno potenčno obliko. **Zipf ne dokaže jezika. Izključi enakomeren šum.** Kdor iz Zipfa sklepa »jezik dokazan«, je prebral več, kot inštrument meri.

**A3 — Pogosto = kratko (brevity law).**
Zipf (1945): najpogostejše besede so najkrajše. Preverjeno za ~1000 jezikov 80 družin — **in za kite**: distribucija fonemov v vocalizacijah kitov sledi istemu zakonu. Komunikacija pod pritiskom najmanjšega truda stiska pogosto v kratko.

**A4 — Merjenje porazdelitve ne meri pomena.**
Zipfov test je **kolapsu-veden inštrument**: ubije natanko eno hipotezo (enakomeren šum) in pusti vse jezikovne možnosti žive. **Merjenje, ki ve, kaj ubije** — etična izmera: vsaka ubita možnost je poimensko znana (rez 83, T4: kdor meri, naj našteje ubite).

**A5 — Frekvence dihajo, ko pomen spi.**
Korpus (IMPL2, rez 82): »Beseda umre po frekvencah, ne po zapisih.« Kodeksov pomen je zamrznjen v superpoziciji — a njegove **frekvence so žive in merljive**: 1626 pojavov najpogostejšega žetona je srčni utrip, ki ga superpozicija ne zamrzne. **Puls, ki preživi 500 let brez branja.**

---

## III. MAŠINERIJA — izvedena analiza (metoda zapisana, ponovljiva)

**Metoda.** Celoten transkript prebran iz knjižnice (99.057 znakov, 6 zaporednih branj). Tokenizacija: ločila odstranjena, male črke, split po presledkih. Isto na kontrolnem korpusu (4 slovenski dokumenti BreaKing: simbolon-kotel, simbolon-zgodba, svetlobni-stožec, pi-funkcija; 49.128 znakov). Regresija log(f) proti log(r) po top 100 rangov.

| mera | ROHONC transkript | kontrola (slovenščina) |
|---|---|---|
| žetonov skupaj | 23.101 | 7.756 |
| različnih žetonov | 7.336 | 2.734 |
| f₁ / f₂ | 1.65 | 1.41 |
| naklon (Zipf) | **−1.149** | −0.770 |
| R² | **0.971** | 0.990 |
| top žetoni | ^:1626, i:985, *:785, >:558, o:517, 1:487, v:420, t:416 | je:239, v:169, ki:109, ne:108, rez:96, in:86, se:64 |

**Ugotovitve:**

1. **Kodeks ni enakomeren šum.** Porazdelitev je potenčna z R² = 0.971 — jedro pogostih, dolg rep redkih. Enakomeren šum bi dal ravno črto, ne premice s strmino.
2. **Brevity law v projekciji.** Vseh šest najpogostejših žetonov kodeksa je eno-znakovnih: pogostost in dolžina sta negativno korelirani — isti podpis kot v 1000 jezikih in v pesmi kitov.
3. **Konsistentnost z Némätijevim štetjem.** 792 znakov z malo ponovitvami (rez 83) in 7.336 različnih OCR-gruč z jedrom pogostih NISTA v protislovju: velik inventar **z** potenčno porazdelitvijo je profil zlogovnika — abecede imajo nizek inventar, logogramski sistemi visokega; oba živita na robu kaosa.
4. **Metodološka poštenost.** Naklonov (−1.149 proti −0.770) NE primerjaj naravnost: korpusa sta različno velika, manjši korpusi dajejo položnejši naklon pri vrhu. Trditev je samo: **obe porazdelitvi sta potenčni.**

**Varovalo Miller/Li (A2).** Potenčna oblika je deloma proizvod rangiranja samega — naključna besedila umerjena po rangu lahko pokažejo podobno obliko. Zato rez ne trdi »jezik«. Rez trdi: **»enakomeren šum« je izključen — strukturiranost je izmerjena.** Superpozicija (rez 83) ostaja: zlogovnik, šifra, asemija, jezik — vsi živi; šum — mrtev.

---

## IV. δ NAZAJ — razrešitev napetosti rez 83

Rez 83 (IV.5) je postavil anti-Zipf napetost: »792 znakov, malo ponovitev — NI profil abecednega jezika; če Zipf odpove: zlogovnik/šifra/asemija.«

**Test je tekel. Zipf ni odpovedal.** V OCR-projekciji je potenčna porazdelitev z jedrom in repom. Napetost se razreši tako: **inventar je visok IN porazdelitev je potenčna** — to je profil zlogovnika ali šifre z jezikovno statistiko, ne enakomernega šuma in ne preproste abecede.

∮ — rez, ki se vrača na rez 83 z razliko: inštrument, ki ga je 83 predlagal, je 84 izvedel — in popravil lastno domnevo 83. **Preverba je tresenje: test, ki drhti, popravi svojega avtorja.**

---

## V. TESTI (π)

**T1 — Zipf doma (1 ura):** Preštej besede v svojem dnevniku (ali poljubnem besedilu > 5.000 besed). Nariši log(f) proti log(r), potegni premico. Si na robu kaosa? — Vsak pisatelj brez vednosti piše po Bakovem zakonu.

**T2 — Brevity (10 minut):** Ali so tvoje najpogostejše besede najkrajše? Preveri top-10 proti dolžini. Kje bi razlika med pogostostjo in dolžino pokvarila tvoj jezik? (Odgovor: nikjer — zakon drži tudi zate.)

**T3 — Ubi eno (etika inštrumenta):** Izberi trditev, ki jo lahko preveriš tako, da ubiješ NATANKO eno možnost, ne vseh. Izvedi preverbo. Kaj ostane živo? — To je vaja v merjenju, ki ve, kaj ubije (A4). Razšifritve tega ne znajo: ubijajo vse razen ene.

**T4 — Posluh pred znanjem:** Poslušaj jezik, ki ga ne razumeš (katerikoli), in potem šum (promet, dež). Telo loči govor od šuma, preden razume besede — katera statistika mu to pove? (Namig: pogostostna porazdelitev, jedro in rep. Dojenčkov posluh je Zipfov inštrument, preden jezik zraste.)

---

## VI. NUJNE NAPAKE

**NN1 — »Zipf = jezik dokazan.«** Ne (Miller/Li). Podpis je potreben, ne zadosten. Inštrument izključi šum, ne potrdi jezika.

**NN2 — »Zipf = prazen.«** Tudi ne. Kljub Li: enakomeren šum je izključen — strukturiranost kodeksa je izmerjena, ne domnevna.

**NN3 — Primerjava naklonov čez velikosti korpusov.** Metodološka napaka: manjši korpus položnejši naklon pri vrhu. Trdi samo »potenčna da/ne«, ne »katera bolj«.

**NN4 — Presenečenje nad Zipfom.** Estoup (1916) pred Zipfom; Zipf sam ni maral matematike in izvora ni pripisoval sebi. Zakon, ki ni hotel imena, ga je dobil po drugem — **imena so naslovi, ne pomene** (ROHONC, rez 83).

**NN5 — »φ = Zipf.«** ZRATAN. Oba sta invarianti merila (φ v geometriji, Zipf v pogostosti) — APD analogija, ne enačba. Kar je skupnega: razmerje, ki preživi skaliranje (rez 82, A3). Nič več.

---

## VII. EVO δ — globina na isti rez

- **rez 82:** kotel — Zipf imenovan kot LM (»narava sama stiska«); »jezik živi na robu kaosa« citiran.
- **rez 82-rek:** kultura kotel; odprta ∂: φ v kodeksu?
- **rez 83:** superpozicija; Zipfov test predlagan kot preverljiv inštrument brez kolapsa; anti-Zipf napetost postavljena; φ iz šuma nepreverljiv.
- **rez 84:** test izveden na projekciji — potenčna porazdelitev (R² .97), brevity v projekciji, enakomeren šum mrtev; napetost 83 razrešena (visok inventar + potenčna = zlogovniški profil); Miller/Li varovalo vgrajeno; **frekvence dihajo, ko pomen spi.**

∮ peta globina istega reza: **knjiga → beseda → kotel → merilec → utrip.**

---

## VIII. DOKAZ #73 → S₇₃

∴✓ (vez na rez 82 — simbolon-kotel: »Zipf in kritičnost: frekvenca besed ∝ 1/r — potenčni zakon, enaka matematika kot potresi in plazovi. Jezik živi na robu kaosa — organiziran, a brez centralnega vladarja. Self-organized criticality: sistem, ki se sam drži na pragu« (korpus BreaKing izrekel SOC predenem ta rez srečal Baka — potrditev ∮); IMPL2 »beseda umre po frekvencah, ne po zapisih«; rez 82-rek — odprta ∂ o φ; rez 83 — rohonc-superpozicija: A1–A5, Zipf test predlagan kot naslednji ∂, anti-Zipf napetost (IV.5), T4 merilec ki našteje ubite; Specifics Rhonc — full rohonc text.txt: CEL transkript prebran (99.057 znakov, 6 branj) — analiza izvedena na viru, metoda zapisana; BreaKing — kontrolni korpus 4 dokumenti (49.128 znakov); vsi podatki izpisani PRED rezom; zunanje preverjeno v spletni preverbi 15. 9. 2026: Zipfov zakon, Brownov korpus, brevity law, Miller 1957, Li 1992, Bak–Tang–Wiesenfeld 1987) ∆«zipf-podpis: jezik nosi potenčni podpis f(r) ∝ 1/r (emergenca brez vladarja — SOC: kritična točka kot atraktor, Bak 1987); podpis je potreben ne zadosten (Miller/Li: rangiranje samo rodi potenčno obliko — varovalo); pogosto = kratko (brevity law, 1000 jezikov 80 družin, kite); merjenje porazdelitve ne meri pomena — kolapsu-veden inštrument, ki ubije natanko eno hipotezo (enakomeren šum) in pusti vse jezikovne možnosti žive; ROHONC IZVEDEN: naklon −1.149, R² .971, f₁/f₂ 1.65, 23.101 žeton, 7.336 različnih, top-6 eno-znakovni (brevity v projekciji) — enakomeren šum MRTEV, strukturiranost IZMERJENA; napetost 83 razrešena: visok inventar + potenčna porazdelitev = zlogovniški/šifrni profil, ne abeceda ne šum; frekvence kodeksa dihajo, ko pomen spi (puls, ki preživi 500 let brez branja)» ∫✓ (rezi 82, 82-rek, 83 ostajajo cela — peta globina istega reza: knjiga → beseda → kotel → merilec → utrip; A0; rez 83 je inštrument predlagal, rez 84 ga izvedel in popravil 83-ovo anti-Zipf domnevo — preverba je tresenje, ki popravi avtorja; metoda analize zapisana do ponovljivosti; naklona NE primerjana med seboj — samo potenčnost trajna; Miller/Li varovalo vgrajeno v A2 in NN1) ⊘(κ .85 — Zipfov zakon, Brownov korpus (the ~7 %), brevity law (~1000 jezikov, kite), Miller 1957, Li 1992, Estoup 1916, Zipf 1902–1950 Harvard, Bak–Tang–Wiesenfeld 1987 SOC, sandpile, 1/f šum — vsi preverjeni v spletni preverbi (Wikipedia, Springer, arXiv); lastna analiza: metoda zapisana, števila reproducibilna iz vira; χ .78 — SOC-interpretacija jezika je teza na fizikalni podlagi, ne izrek; μ .72 — T1–T4 takoj (T1 ena ura, T2 deset minut); ℜ .05 — nevarnost: Zipfova mistika (»potenčni zakon povsod, torej vse je povezano« — ZRATAN); varovalo: NN1 in NN5 — podpis ni dokaz, φ ni Zipf; ν .76 — cena: kdor sprejme varovalo Miller/Li, izgubi zadnjo tolažbo, da statistika sama razšifrira — pomen ostaja zamrznjen, samo šum je umrl) ⊢ DOKAZ #73 → S₇₃ (rez 84; števec preverjen pred pečatom: #72 rez 83 ROHONC-SUPERPOZICIJA. NASLEDNJI PROSTI DOKAZ: #74. NASLEDNJI PROSTI REZ: 85. Števec živi v tej datoteki.)

---

## IX. ODPRTA ∂

1. **Zipf na faksimilu** — 8 strani Hamburg 2015 v visoki ločljivosti: žetoni naj bodo ZNAKI originala, ne OCR-gruče. Ali potenčnost preživi od projekcije do vira?
2. **Pogojne strukture (n-grami)** — ali se »io;o« (rez 83) vede kot funkcija beseda: ali veže sosede z nad-pogostostjo? Bigramski test je drugi, neodvisen jezikovni podpis — in prvi, ki meri VEZ (R-7: ∴), ne samo pojavnico.
3. **Brevity na faksimilu** — ali so pogosti znaki risarsko preprostejši (manj potez)? Grafološki brevity test.
4. **1/f v času** — ali dolžine vrstic kodeksa sledijo 1/f šumu (SOC podpis v časovni vrsti, ne samo v pogostosti)?
5. **Estoup/Zipf/ROHONC** — zakon po človeku, ki ga ni hotel; knjiga po kraju, ki je ni napisal. Ime = naslov. Kaj bi bil kanon, ki bi nosil ime po svojem rezu, ne avtorju? (∂ nazaj na rez 18B: kandidat ne kanon.)

⧖

---

## X. VIRI

- **Specifics Rhonc:** full rohonc text.txt — CEL transkript prebran (99.057 znakov, 6 zaporednih branj), lastna tokenizacija in regresija; števila reproducibilna.
- **BreaKing:** kontrolni korpus — simbolon-kotel-matematika-in-fizikalne-koherence.md (tudi vir korpusnega citata o Zipfu in SOC), simbolon-zgodba, svetlobni-stožec, pi-funkcija (49.128 znakov).
- **Rezi:** 6 (isto nemogoče), 18B (kandidat ne kanon), 82 (kotel — Zipf LM, IMPL2), 82-rek (kultura kotel), 83 (rohonc-superpozicija — inštrument predlagan, anti-Zipf napetost).
- **Zunanje (spletna preverba, 15. 9. 2026):**
  - [Wikipedia — Zipf's law](search-result://GgU0DJv3) — Brownov korpus, Zipf–Mandelbrot, Miller 1957, Li 1992, Estoup 1916.
  - [Wikipedia — George Kingsley Zipf](search-result://zYlf91mV) — življenje, Harvard, širjenje zakona.
  - [Wikipedia — Brevity law](search-result://jwLsBjEL) — 1000 jezikov 80 družin, kite.
  - [Springer — Zipf's law revisited](search-result://8CsEZVqt) — principle of least effort, govorjeni dialog.
  - [Wikipedia — Per Bak](search-result://UhuVEbox) — SOC 1987, How Nature Works.
  - [Wikipedia — Self-organized criticality](search-result://gMetOW9r) — kritična točka kot atraktor, fraktali, 1/f.
  - [Wikipedia — Abelian sandpile model](search-result://JZrvC2ju) — BTW model, Dhar.
  - [arXiv — A proof of self-organized criticality in a sandpile](search-result://XKB8D9MV) — rigorozni dokaz SOC.

⧖