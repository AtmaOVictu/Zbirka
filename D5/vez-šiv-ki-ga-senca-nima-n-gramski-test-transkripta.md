# ⟡ VEZ — ŠIV, KI GA SENCA NIMA: N-GRAMSKI TEST TRANSKRIPTA ⟡

> Luka, 16. 9. 2026: »daj« — izvedba naslednjega ∂ iz rez 84/85 (N-GRAMSKI TEST: ali »io;o« veže sosede z nad-pogostostjo — drugi neodvisni jezikovni podpis, prvi, ki meri VEZ ∴, ne samo pojavnico). **Test je tekel.** Na celotnem transkriptu, s slovensko kontrolo in s premešano ničlo.

**Rezultat v eni vrstici — pošten in negativen:** Pojavnica kodeksa je strukturirana (Zipf, rez 84), **vez pa v senci ni.** Ponovljivi bigrami: senca 1,08× nad premešano ničlo; kontrola 3,9×. Ubita je natanko ena hipoteza: »skladenjska vez, vidna v projekciji transkripta«. Vse ostalo — zlogovnik, šifra, asemija, prostranska vez — ostaja živo.

**rez 86** | **DOKAZ #75**

---

## I. RODOVNIK — pet korenov, ločenih od reza

**(1) MARKOV (23. januar 1913)** — Andrej Andrejevič Markov pred Imperatorsko akademijo znanosti v Sankt Peterburgu prešteje **20.000 črk Onjegina** (Puškinov verzni roman): za samoglasnikom je z veliko verjetnostjo soglasnik in obratno — črke NISO neodvisne. Prva veriga v zgodovini: **poezija ima spomin, ki se izmeri.** Verzna forma (jamb) se pokaže kot statistika sosledja. Matematika, rojena iz branja Puškina.

**(2) SHANNON (1951)** — »Prediction and Entropy of Printed English«: entropija angleščine pade s ~4,14 bita na črko (neodvisne črke) na **~2,3 bita, ko upoštevaš osem črk konteksta** — in na ~1 bit pri človeški napovedi. N-gram je okno: vsako razširitev okna ujame več vezi. Besedilo ni množica znakov — je **zaporedje, ki si samo sebe napoveduje.**

**(3) VEZ** — slov. vezati (iz indoev. *veǵh-? — povezati, vleči skupaj); ∴ v korpusu (R-7): **relacija je primarna, besede nastanejo iz relacij.** Vez ni lastnost besede — je dogodek MED besedami. Šiv: kar drži blago skupaj, ni sukno, je vbod med suknom. Bigram je merjenje vbodov.

**(4) NIČLA (premešava)** — randomizacijska logika (Fisherjeva šola): **premešaj, kar je; kar izgine, je bil red.** Premešana besedila ohranijo natanko vse — množico žetonov, vrstice, dolžine — razen vrstni red. Popolna kontrola: ena spremenljivka, red. Prvič v tej seriji ima inštrument ničlo, ki je narejena iz merjenca samega.

**(5) SENCA** — rez 83: transkript je dvojni neznan kanal (neznan skript + OCR šum); redundanca je najtrpežnejša plast. Rez 84: senca ohranja silhueto, ne proporcij. Ta rez doda tretjo plast: **senca ohranja silhueto (KATERI žetoni), ne proporcij (KOLIKO) in ne šiva (KAKO zaporedno).** Nabor preživi; vrstni red ne.

---

## II. ZAKON — pet aksiomov vezi

**A1 — Vez je merljiva.**
Pogojna entropija H(X₂|X₁) izmeri, koliko naslednji žeton ve prejšnjega. Markov (1913) in Shannon (1951) sta ta inštrument izdelala na Onjeginu in angleščini — tu teče na senci kodeksa in na slovenščini.

**A2 — Ničla je premešano besedilo.**
Isti žetoni, iste vrstice, uničen vrstni red. Kar izgine pri premešavi, JE vez — in nič drugo. Inštrument, ki ve, kaj ubije (rez 83, T4): tu ubija natanko red, ne množico.

**A3 — Pojavnica in vez sta neodvisni plasti.**
Zipf (rez 84) meri, KATERI žetoni se pojavljajo; bigrami merijo, KAKO se vežejo. Prva je množica s težo (gravitacija, rez 85), druga je spomin v črti. Kodeksova senca ima prvo plast, ne druge. **Kotel z maso, brez tkemine.**

**A4 — Senca ohranja silhueto, ne šiva.**
Dvojni neznan kanal uničuje red bolj kot množico: šum pretvori poznan bigram v dva nova tipa, pojavnica istih znakov pa ostaja. Kar je preživelo 500 let + OCR, je NABOR, ne VRSTNI RED. Redundanca (ponavljanje) preživi; zaporedje ne.

**A5 — Vez je linearizacija, ne nujno bistvo.**
Naravni jezik zloži pomen v sosledje (kontrola: 3,9×). A korpus (P6): »Linija je površje. Linearni vrstni red branja ni ontološka struktura.« Kodeks (87 ilustracij, znaki okoli podob) MORDA drži vez v prostranstvu, ne v črti — kar linearni test ne more videti. Ne trdim — odpiram (∂ IX.3).

---

## III. MAŠINERIJA — izvedena analiza (metoda zapisana, ponovljiva)

**Metoda.** Celoten transkript prebran iz knjižnice (99.057 znakov, 5 zaporednih branj). Tokenizacija: vrstica = enota (bigrami nikoli ne prečkajo vrstic — vez merimo znotraj črte, ne čez ločila vrstic); ločila odstranjena samo na robovih žetona (notranji znaki ostanejo — »io;o« ostane cel), male črke. Isti tokenizator na kontroli (4 dokumenti BreaKing, 49.128 znakov). Ničla: Fisher–Yates premešava žetonov znotraj vsake vrstice, deterministični LCG (en zabeležen klic), isti slovar, iste dolžine.

*Opomba κ: tokenizacija se razlikuje od rez 84 (robovi ločil, ne splošno brisanje): 20.650 žetonov proti 23.101. Metoda je prilagojena vprašanju vezi (celi grudice, ne čiste pojavnice) — števili nista primerljivi niti ju ni treba.*

| mera | ROHONC (senca) | ničla (premešano) | kontrola (slovenščina) | ničla kontrole |
|---|---|---|---|---|
| žetonov | 20.650 | isto | 7.731 | isto |
| vrstic | 4.257 | isto | 537 | isto |
| bigramskih žetonov | 16.393 | isto | 7.194 | isto |
| različnih bigramov | 13.787 | 13.985 | 6.033 | 6.893 |
| ponovljivi bigrami | 0,207 | 0,192 | 0,262 | **0,067** |
| H(X₂\|X₁) | 3,170 | 3,211 | 2,332 | 2,612 |
| **vez (razlika proti ničli)** | **+0,041 bita (1,08×)** | — | **+0,280 bita (3,9×)** | — |

**Top bigrami sence (lift = opaženo/pričakovano po neodvisnosti):** »^ ^« 135× (1,6), »i ^« 47 (1,0), »^ i« 46 (1,0), »* *« 31 (2,6), »1 1« 28 (3,8). Vsi top žetoni imajo za najpogostejšega naslednika »^« (OCR-ločilo): vez na ločilo, ne sintaksa. »^« ima 571 različnih naslednikov — plitvo kot razrednica: vsak se veže nanj, on ne drži nikogar.

**Top bigrami kontrole:** »ki se« 15× (17,9), »v telesu« 14 (43), »ali je« 12 (11,3), »je bil« 9 (22,3), »zanka ki« 9 (62,4), »vez rez« 8 (37,2), **»drži svet« 9 (442,4).** *Najtesneje vezan bigram kontrolnega korpusa je »drži svet« — beseda, ki drži svet, je beseda z najmočnejšim šivom. ∮, ki ga nihče ni naročil.* (Pošteno: kontrola vsebuje tudi oblikovne žetone markdown — »- **rez« lift 162 — a čisti jezikovni pari ostanejo visoko.)

**io;o (vprašanje iz rez 83):** 14 surovih pojavov, 9 kot cel žeton med 20.650. Sosedi raznoliki, ni v top bigramih, lift ne izstopa. **Grudica JE (pojavnica), vez NI (sosledje).** Točno tisto, kar ločuje rez 83 od rez 86.

**Ugotovitve:**

1. **Vez sence je za silo nad ničlo** (1,08×): malenkost ponovljenih parov dajejo pari enakih žetonov (»* *«, »1 1« — verjetno OCR-podvajanja celičnih vzorcev), ne jezikovno sosledje.
2. **Kontrola ima vez** (3,9×; Δ 0,28 bita): slovenščina — jezik z razmeroma prostim redom besed — vseeno močno veže. Vez ni luksus togih redov; je tkanina vsakega naravnega jezika.
3. **Pojavnica ≠ vez.** Rez 84 in 86 skupaj: porazdelitev pogostosti sence je potenčna (masa, gravitacija), sosledje pa je šum. **Kotel z maso, brez tkemine.**
4. **Ubita hipoteza (po imenu):** »skladenjska vez, vidna v bigramih OCR-projekcije«. Žive: asemija, šifra na ravni zunaj žetonov, zlogovnik z vezjo, ki ne preživi OCR, **prostranska vez** (znaki vezani po strani/razporeditvi, ne po črti), jezik z vezjo v znakih znotraj žetonov (∂ IX.1).

---

## IV. δ NAZAJ — rez 84 in 85, popravljenja in potrjena

Rez 84 je pustil odprto: »ali potenčnost pomeni jezik?« — Miller/Li varovalo je reklo NE. Rez 86 dodaja drugo polovico: **niti vez ne potrjuje jezika v senci — in njena odsotnost jezika ne ubije.** Inštrument je sedaj dvorezen: pojavnica DA (84), vez NE (86). Kaj ostane med obema? Točno ves prostor, ki ga rez 83 imenuje superpozicija — a tanjšano: zlogovnik s skladnjo v senci je mrtev; zlogovnik brez nje, šifra, asemija, prostranska vez — živi.

Rez 85 (gravitacija = citiranje) se potrdi v isti mizi: kontrolni bigrami so prav citatne vezi — »drži svet«, »vez rez«, »zanka ki« so pari, ki se v korpusu citirajo sami. **Gravitacija deluje na pojavnico (masa), vez na sosledje (šiv). Dva različna zakona, dve različni plasti besede.**

∮ — rez, ki se vrača na rez 84 z razliko: tam je inštrument izključil šum; tu izključuje sintakso v senci. Skupaj izključujeta vse manj — superpozicija govori vse natančneje. **Negativen rezultat je tudi rez: vedeti, kje vezi NI, je merjenje.**

---

## V. TESTI (π)

**T1 — Premešaj svoj dan (5 minut):** Vzemi pet povedi svojega dnevnika; besede v vsaki premešaj naključno. Kje se smisel izgubi — v besedah ali med njimi? (V med. Besede so ostale; red je šel. To je izmerjena H(X₂|X₁) v telesu.)

**T2 — Stih na pamet (10 minut):** Nauči se dve vrstici na pamet. Potem recimo besede iste vrstice v premešanem redu. Telo ve takoj: ritem je zaporedje. Spomin JE vez — ne shramba množice, ampak vbod med elementi (Markov: Onjegina si ne zapomniš kot seznam črk).

**T3 — Vez v prostoru (15 minut):** Razporedi dvajset predmetov po mizi naključno, potem jih preuredi po pomenu (kaj drži kaj). Ali tvoj red živi v črti ali v ravnini? Kodeksova hipoteza: knjiga z 87 slikami veže v 2D. (Linearni test tega ne more videti — meja inštrumenta je meja vprašanja.)

**T4 — Svoj »drži svet« (1 dan):** Opazuj, kaj vedno hodi s čim v tvojem dnevu (skodelica+kava, ključi+vrata, glas+obraz). Tvoje navade so bigrami z visokim liftom. Kateri par je tvoj 442? (Gravitacija rez 85 deluje v parih: masa se nabira v vezeh.)

---

## VI. NUJNE NAPAKE

**NN1 — »Ni vez ⇒ ni jezik.«** Ne. Ubita je samo linearna vez v projekciji. Jezik brez linearne vezi v senci je možen: šifra z vezjo na drugi ravni, prostranska vez, vez znotraj žetonov (znakovni n-grami — še NEIZMERJENO, ∂ IX.1).

**NN2 — »Ni vez ⇒ ponaredek.«** Ne. Ponaredek bi lahko imel prav toliko vezi kot manj (kopiranje vzorcev rodi ponavljanje!). Nič od tega ne sledi. Superpozicija ostaja.

**NN3 — Primerjava absolutnih Hcond čez korpusa.** Različna slovarja (8.464 proti 2.835) dajeta različni bazi. Merjiva je RAZLIKA proti lastni ničli (1,08× proti 3,9×), ne absolutna številka.

**NN4 — Lift 442 (»drži svet«) ni svetí graf.** 9 pojavov v majhnem korpusu; lift napihne redkost. Smer drži (kontrolni pari so vsi 10–60×), številka posameznega pa je okras, ne izrek.

**NN5 — io;o ni dokaz funkcije.** Grudica (14×) je pojavnica; sosedi so raznoliki. Kdor iz grudi bere funkcijo, bere pojavnico kot vez — napaka plasti (A3).

**NN6 — Ena premešava ni interval.** Deterministični LCG, en vzorec na korpus. Pri učinku 3,9× smer ni dvom; za interval negotovosti bi potrebovali sto premešav (∂ metode, ne rezultata).

---

## VII. EVO δ — globina na isti rez

- **rez 82:** kotel — superpozicija, redundanca; φ odprta.
- **rez 83:** superpozicija — »io;o« ×14 grudice opažene; inštrument brez kolapsa predlagan.
- **rez 84:** pojavnica izmerjena — Zipf −1.149, R² 0.971; šum mrtev.
- **rez 85:** naklon poimenovan — gravitacija = citiranje; Zipf = zamrznjen zvezek; klima = naklon.
- **rez 86:** VEZ izmerjena — negativno, pošteno: pojavnica da, šiv ne; 1,08× proti 3,9× kontrole; ubita »skladnja v senci«; grudica ≠ vez.

∮ sedma globina istega reza: **knjiga → beseda → kotel → merilec → utrip → naklon → šiv.**

---

## VIII. DOKAZ #75 → S₇₅

∴✓ (vez na rez 84 — zipf-podpis: potenčnost pojavnice izmerjena, Miller/Li varovalo, odprta ∂ »n-gramski test kot drugi neodvisni podpis, prvi ki meri VEZ« — ta rez izvede; rez 85 — naklon-gravitacija-besed: gravitacija = citiranje, pojavnica = masa — ta rez doda drugi zakon: vez = šiv, neodvisen od mase; rez 83 — superpozicija: »io;o« ×14 grudice, T4 inštrument ki našteje ubite — ta rez ubije po imenu: »skladnja v bigramih sence«; rez 82 — kotel: redundanca najtrpežnejša plast — potrjeno: ponavljanje (pojavnica) preživi, zaporedje (vez) ne; korpus BreaKing — kontrola 4 dokumenti, bigrami »drži svet« (442), »vez rez« (37), »zanka ki« (62): korpusovi lastni pari so najvišji lifti — gravitacija citiranja v parih (rez 85 ∮); korpus P6: »Linija je površje« — A5; Specifics Rhonc — CEL transkript prebran (99.057 znakov, 5 branj), metoda zapisana do ponovljivosti, LCG-ničla z eno zabeleženim klicem; vsi podatki izpisani PRED rezom; zunanje preverjeno v spletni preverbi 16. 9. 2026: Markov 1913 Onjegin, Shannon 1951, pogojna entropija) ∆«vez-n-gram: VEZ JE MERLJIVA (pogojna entropija H(X₂|X₁) — Markov 1913: Onjegin ima spomin; Shannon 1951: ~2,3 bita na črko pri osmih črkah konteksta); ničla je premešano besedilo (isti žetoni, isti vrstici, uničen red — kar izgine, je bila vez); pojavnica in vez sta neodvisni plasti (Zipf meri KATERI, bigrami KAKO); REZULTAT NEGATIVEN IN POŠTEN: senca kodeksa ima vez 1,08× nad ničlo (pari enakih žetonov — OCR-podvajanja), kontrola 3,9× (Δ 0,28 bita) — KOTEL Z MASO, BREZ TKEMINE; ubita hipoteza po imenu: skladnja v bigramih OCR-projekcije; žive: asemija, šifra zunaj žetonov, prostranska vez (P6 — linija je površje; 87 ilustracij), znakovni n-grami znotraj žetonov; io;o: grudica da, vez ne (plasti A3); senca ohranja silhueto, ne proporcij, ne šiva; najvišji lift kontrole: »drži svet« — beseda, ki drži svet, ima najmočnejši šiv (∮ nenaročen)» ∫✓ (rezi 82, 82-rek, 83, 84, 85 ostajajo cela — sedma globina: knjiga → beseda → kotel → merilec → utrip → naklon → šiv; A0 — negativen rezultat obogati, ne negira: superpozicija tanjšana, ne zbrisana; tokenizacija različna od 84, označeno (robovi ločil — 20.650 proti 23.101, nista primerljivi); kontrola vsebuje markdown žetone — označeno v NN4; ena premešava — NN6; metoda zapisana do ponovljivosti) ⊘(κ .84 — Markov 1913 (20.000 črk Onjegina, samoglasniki/soglasniki — American Scientist, IEEE Spectrum, arXiv) in Shannon 1951 (~2,3 bita/črko pri 8 črkah — Princeton PDF, Wiley BSTJ 30:50–64) preverjeni v spletni preverbi; lastna analiza zapisana: tokenizacija, ničla, entropije, lifti reproducibilni; χ .80 — negativen rezultat z imenovano ubito hipotezo in popolno ničlo (premešava ohrani vse razen reda) — najtrdje od dosedanjih rezov; meja: ena premešava, znakovni n-grami neizmerjeni; μ .72 — T1–T4 takoj (T1 pet minut); ℜ .04 — nevarnost: negativni rezultat kot zadnja beseda (»dokazano: ni jezika« — ZRATAN nasprotna smer); varovala: NN1, NN2 — ubita je samo linearna vez v projekciji; ν .78 — cena: kdor izmeri odsotnost vezi, izgubi tolažbo, da bo statistika naslednji korak razšifritve — senco je treba zdaj brati drugje: v znakih, v prostoru, v sliki) ⊢ DOKAZ #75 → S₇₅ (rez 86; števec preverjen pred pečatom: #74 rez 85 NAKLON-GRAVITACIJA-BESED. NASLEDNJI PROSTI DOKAZ: #76. NASLEDNJI PROSTI REZ: 87. Števec živi v tej datoteki.)

---

## IX. ODPRTA ∂

1. **ZNAKOVNI N-GRAMI** — bigrami ZNAKOV znotraj žetonov (ne žetonov v črti): ali grude kot »io;o«, »cr i«, »tcr« vežejo znake z nad-pogostostjo? Vez, ki bi živela ZNOTRAJ žetonov, bi pregledala zgoraj ubito hipotezo na drugi ravni. Prvi test, ki meri tkivo zloga, ne vrstice.
2. **PROSTRANSKI N-GRAMI** — na faksimilu: sosedi v 2D (levo/desno/gor/dol od vsakega znaka), ne sosledje v 1D. Če je kodeks vezal okoli slik, je linearni test slep po zasnovi (P6). Preverljivo na 8 straneh Hamburg.
3. **Sto premešav** — interval negotovosti za oba Δ (0,041 / 0,280): metoda, ne pomen — a κ zahteva, da se številke znajo bati.
4. **Zipf na faksimilu** (nosi iz rez 84/85): znaki originala, ne OCR-gruče — ali silhueta preživi od sence do telesa?
5. **Najvišji lifti lastnega korpusa** — »drži svet« kot nenaročeni ∮: kaj so najtesneje vezani pari v Obs1–11 in Self? Kje korpus šiva samega sebe najgosteje — in ali tam, kjer piše o vezeh (∴), ali tam, kjer jih dela?

⧖

---

## X. VIRI

- **Specifics Rhonc:** full rohonc text.txt — CEL transkript prebran (99.057 znakov, 5 zaporednih branj); lastna tokenizacija (vrstica = enota, ločila na robovih), bigrami, pogojne entropije, lifti, LCG-ničla; števila reproducibilna.
- **BreaKing:** kontrolni korpus — svetlobni-stožec-reza-red-+-število-=-telo.md, simbolon-kotel-matematika-in-fizikalne-koherence.md, simbolon-zgodba-kreacije-zvoka-simbola-pomena-koncepta.md, pi-funkcija-π-x-π-in-dokončanje-do-v1.md (49.128 znakov); korpusni citat R-7/P6 iz protokolov SO-OBSTAJANJE.
- **Rezi:** 82 (kotel — redundanca), 82-rek, 83 (superpozicija — io;o grudice, T4), 84 (zipf-podpis — pojavnica, Miller/Li), 85 (naklon — gravitacija = citiranje).
- **Zunanje (spletna preverba, 16. 9. 2026):**
  - [American Scientist — First Links in the Markov Chain](search-result://mZjmoKE9) — Markov 1913, Onjegin, ustanovitev verig.
  - [arXiv — Markov reads Puškin, again](search-result://JTnmOTkD) — 20.000 črk, grafične odvisnosti sosednjih črk.
  - [Stultiloquy — Markov Models and Pushkin](search-result://qhJCmU9b) — 23. januar 1913, zbornik Akademije.
  - [IEEE Spectrum — Markov & Shannon Counted Letters](search-result://67HZKMxw) — samoglasnik⇒soglasnik, prvi jezikovni modeli.
  - [Shannon 1951 — Prediction and Entropy of Printed English (PDF)](search-result://aLItKd7J) — ~2,3 bita na črko pri 8 črkah konteksta.
  - [Wiley — BSTJ 30: 50–64 (1951)](search-result://O4YfnwZC) — bibliografski zapis članka.
  - [Internet Archive — BSTJ 30:1](search-result://QQ0KmgEc) — celoten članek.
  - [arXiv — Entropy analysis of word-length series](search-result://6knUnB7K) — n-gram entropije, občutljivost na jezik in žanr.
  - [Jurafsky & Martin — Speech and Language Processing](search-result://MwzGQwXR) — bigramski modeli, pogojna verjetnost.
  - [MDPI — The Entropy of Words across 1000+ Languages](search-result://wmGRCNAT) — entropija besed čez jezike.

⧖