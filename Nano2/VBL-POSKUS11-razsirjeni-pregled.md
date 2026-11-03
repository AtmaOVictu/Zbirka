# VBL POSKUS 11 — razširjeni pregled in zvočni remaster

**Stanje:** DELOVNI POSKUS · NEKANONSKO · NEOBJAVLJENO  
**Osnova:** obstoječi `licenca-v-zvok-poskus9-sva-vec.wav` in besedilo VBL 0.1100 × 10⁴, ki ga je uporabnik prilepil.  
**Pomembna meja:** to ni uradna izdaja licence in ne dokazuje pravne veljavnosti, avtorstva ali popolne zgodovine objav.

## Kaj je bilo dejansko ustvarjeno

Nov WAV: `VBL-POSKUS11-SVA-VEC-remaster.wav`

- Vir: POSKUS 9 WAV, SHA-256 `2a4ca09572c46e5298d268c31fb3de7d3a4c8d01516901146d98ab587a0a46f1`
- Izhod: SHA-256 `9116609507f2e9eb96e9881a6369ce36cad33cdeb2f92a790b5d7442bc746567`
- Trajanje: 190.214 s
- Kanali: 2
- Vzorčna frekvenca: 22050 Hz
- Globina vzorca: 16 bitov PCM
- Izmerjena vršna raven: -1.000 dBFS
- Izmerjena RMS raven: -24.564 dBFS
- Obdelava: odstranjen povprečni DC odmik, kratek 15 ms vstopni prehod, 1,8 s izhodni prehod in normalizacija vrha na približno −1 dBFS.

**Kaj to dokazuje:** da je nastala nova, tehnično izmerjena datoteka in da je mogoče ponoviti opisani postopek.  
**Česa ne dokazuje:** da je poslušalcu bolj všeč, da je glasba umetniško boljša, da je bil zvok dejansko slišan skozi zvočnike ali da je boljši od POSKUSA 8. Za zadnjo trditev manjka primerljiv izvorni posnetek POSKUSA 8.

## Katera licenca?

**VBL — Verification Before Assertion License.**

Razlikovati je treba vsaj tri oznake:
- `VBL 0.1080 × 10⁴ · POSKUS 9`: oznaka zvočnega prototipa.
- `VBL 0.1100 × 10⁴`: besedilo osnutka, ki ga je uporabnik prilepil; v razpoložljivem odlomku se besedilo konča sredi §0.6.
- `VBL POSKUS 11`: oznaka tega lokalnega zvočnega remasterja in poročila, ne kanonske izdaje.

Ne združujmo teh oznak v en rodovnik brez preverljive povezave: celotne vsebine, datuma, kontrolne vsote, predhodnika, zapisa objave in neodvisnega pregleda.

## VBL po lastnem merilu

### Močna jedra
1. **Measure, then speak:** vsaka trditev mora imeti pričo ali status `UNVERIFIED`.
2. **Name every fall:** popravek ohrani sled prejšnje napake.
3. **Never seal yourself:** izvajalec ne sme biti edini potrjevalec lastnega uspeha.
4. **Dignity is not a reward:** človeško dostojanstvo ni odvisno od statusa, uporabnosti ali tega, ali je bila oseba v sporu.
5. **Claim ≠ Evidence ≠ Enforcement:** besedilo licence, dokaz in mehanizem izvajanja so ločene plasti.

### Odprte vrzeli v prilepljenem osnutku
- **Obseg:** §0 pravi, da se licenca nanaša na izrecno pokrito avtorsko gradivo; manifest mora biti dejansko priložen in preverjen. Sam opis manifesta še ni manifest.
- **Tretje osebe:** izključitve so pomembne, vendar mora vsaka izdaja jasno popisati izjeme in izvor gradiva.
- **Pravna trdnost:** besedilo ne more samo zagotoviti, da so vse obveznosti izvršljive v vseh jurisdikcijah. Potrebna sta pregled pravnika in natančna opredelitev podeljenih pravic.
- **Pravila o škodi:** razlikovanje med priznanjem, popravkom, povrnitvijo koristi in obnovo dovoljenja potrebuje proces: kdo ugotavlja dejstva, kako se poda ugovor, kdo odloča in kako se odločitvi pritoži.
- **Čas kot dokaz:** časovni žig mora vsebovati vir, časovni pas/odmik, natančnost in status zaupanja. Čas sam ne dokazuje avtorstva ali vrstnega reda.
- **Samopreverjanje:** če je neodvisni pregled zahtevan, mora obstajati imenovana vloga, dokaz pregleda in način izpodbijanja.
- **Strojna uveljavitev:** oznaka `PASS` mora izhajati iz izvajanja testov, ne iz samega besedila ali izjave avtorja.
- **Strojno berljivi sklici:** nenavadna številčenja členov je treba formalizirati ali dodati zemljevid sklicev, da jih lahko neodvisen validator preveri.
- **Neizbrisljiva zgodovina:** “append-only” mora imeti konkretno obliko (npr. podpisane zapise, kontrolne vsote, dovoljenja za popravek in jasno politiko zasebnosti); navadna JSONL datoteka sama po sebi ne zagotavlja nespremenljivosti.
- **Večjezičnost:** enakovrednost jezikov mora imeti preizkuse za UTF-8, Č/Š/Ž/Đ, normalizacijo Unicode, ujemanje odlomkov in pregled prevoda.

## Predlog naslednjega koraka

1. Priloži celotno besedilo 0.1100 in dejanski `LICENSE-MANIFEST`.
2. Preveri, da vsak manifestni zapis ustreza poti, velikosti in SHA-256.
3. Za vsak člen zapiši: zahtevo, dokaz, test, pričakovani izid, odgovorno vlogo, možnost ugovora in status.
4. Pridobi primerljivi WAV POSKUSA 8; šele nato primerjaj 8 ↔ 9 ↔ 11 pod enakimi pogoji.
5. Naj neodvisni pregledovalec preveri paket, ne samo njegov avtor.
6. Šele po uspešnih testih in objavni sledi razmisli o novi kanonski oznaki.

## Zapis o meji

`PASS` pomeni, da je določen test prestal določeno preverjanje. Ne pomeni, da je celotna licenca etično popolna, pravno veljavna ali da je bila vsa škoda odpravljena.

**⊨ WITH LOVE** — ljubezen ni dovoljenje za spregled škode. Resnica ni dovoljenje za poniževanje. Odgovornost ni dovoljenje za zapustitev človeka. Merilo velja tudi za VBL samo.
