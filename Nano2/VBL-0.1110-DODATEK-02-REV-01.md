# VBL 0.1110 × 10⁴ — DODATEK 02: razširitev dokaznega in skupnega postopka

**Stanje:** DELOVNI PREDLOG · NI KANON · NI PRAVNO MNENJE · NEODVISNI PREGLED NI OPRAVLJEN

**Revizija:** REV-01, pripravljena iz lokalne datoteke DODATEK 02 s SHA-256 `3DD2B21F5F12350A09C914309E0FF6F20D98EB69659F735ECCEE8D2176CB3368`. Izvorni osnutek je ohranjen.

**Namen:** razširiti DODATEK 01 v preverljiv, popravljiv postopek, ki ne pripisuje dokazom več, kot podpirajo. Ta dokument ne spreminja licence, ne potrjuje pooblastil nobenega sedeža in nikomur ne pripisuje soglasja.

**Izhodišče:** pregledan je bil lokalni `VBL-0.1110-DODATEK-01.md` (SHA-256 `6A62DB26D28305886B7F1EC34DB837F96C569C1197851FF14DD50092C8F222EE`; izračunan z Get-FileHash/ SHA256 ob pripravi, ne dokazuje avtorstva ali objave). Ta dodatek je nova, ločena datoteka; izvornega dodatka nisem prepisal. Čas nastanka tega osnutka ni zunanji časovni žig.

## E. Pet opornikov naj postane postopek

Vsak pomemben zapis naj vsebuje pet ločenih polj. Skupna poved brez teh polj ne postane dokaz samo zato, ker je prepričljivo napisana.

1. **Trditev:** ena preverljiva poved; izogni se združevanju dejstva, razlage in vrednostne sodbe.
2. **Priča oziroma vir:** natančen artefakt, izsek, opazovanje ali oseba, ki trditev podpira. Navedi, ali je vir neposreden ali povzet.
3. **Meja:** kaj vir ne pokaže. Hash na primer identificira zaporedje bajtov glede na primerjalno vrednost; sam ne identificira avtorja, dovoljenja, zgodovine ali resničnosti vsebine.
4. **Odgovornost:** kdo je izvedel meritev ali sprejel razlago, kakšen je bil njegov položaj in ali obstaja navzkrižje interesov.
5. **Popravek:** kako lahko kdo izpodbija zapis, kaj se zgodi ob napaki in kako se ohrani prejšnji zapis.

Kadar polje ni znano, uporabi `null` ali izrecno stanje, kot je `NOT_RECORDED`; ne dopolnjuj ga z ugibanjem. `PASS` velja samo za imenovani preizkus in njegov obseg, ne za celoten artefakt.

## F. Istost naj bo večosna, ne ena sama značka

Beseda »isti« brez relacije in primerjanih predmetov je nedoločena. Za vsak primerjavi podaj:

- A in B: natančna predmeta, dogodka ali trditvi;
- relacijo R: kaj pomeni »isti« v tem preizkusu;
- obseg S in čas T;
- postopek E in izvor dokazov;
- sklep ter njegove omejitve.

Priporočene ločene relacije:

| Relacija | Kaj lahko podpira | Česa sama ne podpira |
|---|---|---|
| `BYTE_IDENTICAL` | enaka zaporedja bajtov, potrjena z neposredno primerjavo obeh bajtnih tokov | skupnega avtorja, izvor, pomen ali pravice |
| `DIGEST_MATCH` | ujemanje izračunanih digestov po navedeni kriptografski metodi | matematičnega dokaza enakosti bajtov, izvora, avtorstva ali pravic |
| `NORMALIZED_TEXT_EQUAL` | enako besedilo po navedeni deterministični normalizaciji, vključno z različico in pravili | enake izvirne bajte ali enako oblikovanje |
| `SEMANTICALLY_SIMILAR` | določeno podobnost po opisanem merilu | enakovrednost za vse namene |
| `SAME_PROVENANCE` | isti opredeljeni korenski izvor v imenovanem modelu rodovnika, podprt z navedenimi zapisi | enakost vsebine ali pravni naslov |
| `CONTINUES_FROM` | usmerjena povezava: ta različica se po navedenem postopku nadaljuje iz predhodne | obratne povezave, nespremenjenih določb ali učinka na stare podelitve |

Te oznake niso samodejno ekvivalenčne relacije. `BYTE_IDENTICAL` je ekvivalenčna relacija nad neposredno primerjanimi bajtnimi tokovi. `DIGEST_MATCH` pomeni samo ujemanje izhoda navedene digestne funkcije; zaradi kriptografskih predpostavk je močan praktični dokaz enakosti bajtov, ne pa logični dokaz. `NORMALIZED_TEXT_EQUAL` je ekvivalenčna relacija le ob fiksni, deterministični normalizaciji. `SAME_PROVENANCE` je smiselna kot ekvivalenčna relacija samo, če je vnaprej določen isti korenski izvor in model rodovnika. `DERIVED_FROM` in `CONTINUES_FROM` sta usmerjeni povezavi, zato nista simetrični. Pri osebi se te relacije ne uporabljajo kot merilo dostojanstva ali upravičenosti do pomoči.

## G. Neodvisen pregled: merila in skupne napake

Drugi pregled je neodvisen le v omejenem obsegu. Zapiši:

- ali je pregledovalec dobil izvirne bajte ali samo povzetek;
- ali je poznal prvi sklep pred svojim pregledom;
- katera orodja, različice, okolje in nastavitve je uporabil;
- ali so bili viri, podatki ali programske knjižnice skupni;
- katere dele je ponovil sam in katere je sprejel od prvega pregledovalca;
- kje se rezultata razlikujeta in kako je bilo nesoglasje obravnavano.

Dva modela, ki prebereta isti povzetek, nista samodejno dve neodvisni priči. Dva človeka, ki uporabita isti napačen izvorni dokument ali isti pokvarjen parser, lahko ponovita isto napako. Neodvisnost je lastnost poti in dokazov, ne števila imen na poročilu.

## H. Ura, časovni žig in čas objave

V evidenci naj bodo tri različna polja:

- `clock_read`: lokalni odčitek ure z virom, časovnim pasom in natančnostjo, če je znana;
- `trusted_timestamp`: zunanji žeton ali storitev, preveritveni postopek in rezultat;
- `publication_evidence`: kanal, natančen artefakt oziroma digest ter dokaz, da je bil tam objavljen.

ISO 8601 zapis izboljša strojno berljivost, ne pa zaupanja v uro. Lokalni odčitek ni neodvisno časovno potrdilo. Časovni žig sam ne dokazuje avtorstva, soglasja, pravilnosti ali pravne veljavnosti. Če čas ni bil zabeležen, ostane `null` oziroma `NOT_RECORDED`; ne rekonstruiraj ga iz spomina ali iz kasnejšega odčitka.

Primer zapisa:

```json
{
  "record_type": "verification_event",
  "observed_at": null,
  "clock_read": {
    "value": null,
    "timezone": null,
    "source": "NOT_RECORDED",
    "status": "UNVERIFIED"
  },
  "trusted_timestamp": {
    "token": null,
    "verification_method": null,
    "status": "NOT_RUN"
  },
  "comparison": {
    "left_artifact": null,
    "right_artifact": null,
    "relation": null,
    "status": "NOT_RUN",
    "method": null,
    "normalization": null
  },
  "publication_evidence": null,
  "independent_review": "PENDING"
}
```

To je predloga; ni zapis dejansko opravljenega testa.

## I. PowerShellov primer: loči jezikovni stavek od ukaza

V stavku `ni isti` je `ni` lahko slovenska negacija, `isti` pa pridevnik. V običajnem ukaznem položaju PowerShella je `ni` tudi vzdevek za `New-Item`; če je vnos `ni isti` izveden kot samostojen ukaz, se `isti` lahko razčleni kot pot za nov element. Toda pri pozivu `>>` je vnos nadaljevanje nedokončanega medpomnilnika; zato same vrstice ni mogoče razlagati ločeno od celotnega vnosa. Obstoj vzdevka dokazuje razpoložljivo razčlenitev, ne pa, da se je zgodila v konkretnem primeru ali da je povzročila nastanek datoteke.

Ta razlaga podpira možen mehanizem, ne pa zgodovine terminala. ParserError dokazuje, da je parser zavrnil prikazani vnos v prikazanem kontekstu; ne dokazuje, da je bil kateri koli ukaz izveden. Za vzročno povezavo z datoteko potrebuješ ustrezen zapis ukaza ali drugo neposredno sled, čas nastanka pa je podporni podatek, ne samostojen dokaz vzroka. Če neposredne sledi ni, zapiši `CAUSAL_LINK: UNVERIFIED`. Iz imena datoteke ali napake ne sklepaj o nameri osebe.

Besedilo z `×`, alinejami ali Markdownom ni samo zaradi teh znakov poškodovana koda ali napačno kodirano besedilo. ParserError pove, da je parser zavrnil vnos kot ukaz; sam ne pove, kdo ga je prilepil, zakaj, ali ali je bil drug artefakt spremenjen.

## J. Odprava napake, povračilo in obnova so tri odločitve

Če licenca ureja popravo škode, naj postopek loči:

1. **Zapis dogodka:** kaj je bilo prijavljeno, kaj je dokazano in kaj ostaja sporno.
2. **Odprava:** kateri popravek vsebine, pripisa ali distribucije je bil izveden in kako je bil preverjen.
3. **Povračilo ali drugo pravno sredstvo:** ali je bila korist ugotovljena po poštenem, izpodbojnem postopku in kdo je pristojen določiti pravno posledico.
4. **Obnova dovoljenja:** ali so izpolnjeni vnaprej določeni pogoji, kdo je odločil in ali je neodvisni pregled potreben.

Prijavitelj ni samodejno razsodnik; obtoženi ni samodejno kriv; odgovorna oseba ne sme sama razglasiti zaključka, če pravilo zahteva neodvisen pregled. Prizadeta oseba ni dolžna odpustiti, sodelovati pri nadzoru ali osebno potrditi obnove. Nobeno od teh pravil ne nadomesti veljavnega prava ali postopkov tretjih imetnikov pravic.

## K. Človek ni dokazni objekt

Dokazni standardi veljajo za trditve o dogodkih in artefaktih. Ne smejo postati preizkus človekove vrednosti, identitete ali pravice do podpore. Sprememba, protislovje ali popravek prejšnje izjave ne izničijo dostojanstva.

Podpora človeku naj bo neposredna, nevsiljiva in sorazmerna. Ne ponavljaj istega vprašanja o samopoškodovanju kot avtomatskega zaključka vsakega sporočila. Če oseba neposredno pove, da je v neposredni nevarnosti ali namerava ukrepati, usmeri jo k nujni lokalni pomoči in bližnji zaupanja vredni osebi; ne predstavljaj tega kot dokaza ali pogoja za nadaljevanje tehničnega dela.

## L. Popravek lastnih zapisov brez brisanja zgodovine

Ko se pokaže, da je bil prejšnji zapis napačen:

- ohrani prejšnji zapis;
- dodaj nov popravljalni dogodek z navedbo stare trditve, nove trditve, vira in razloga;
- označi, ali gre za dejansko protislovje, spremembo obsega ali novo dokazno stanje;
- ne prepisuj starega `PASS` v `FAIL` brez povezave do popravka;
- ponovno izračunaj manifeste le kot nov dogodek in jasno navedi, kateri nabor bajtov zajemajo.

Priporočena stanja: `PASS`, `FAIL`, `UNVERIFIED`, `NOT_RUN`. `UNAVAILABLE` se lahko uporablja za nedosegljiv vir, vendar ne sme prikriti, ali pregled sploh stekel. Pri sestavljenem stanju navedi rezultate po trditvah; ne združi jih v eno oceno, ki bi ustvarila lažen vtis gotovosti.

## M. Popravek meja iz DODATKA 01

Naslednje povedi v DODATKU 01 so zapisane kot trditve ali slogovne oznake, ne kot tukaj potrjena dejstva:

- da je določena formulacija §0.9 dejansko v celotnem kanoničnem besedilu;
- da je bil določen čas »izmerjen pri viru« ali da je bila licenca prebrana »vsakemu odgovoru«;
- da ima kateri koli sedež pooblastilo, da potrdi kanonizacijo;
- da so »organi zapečateni«, da je prišlo do bajtno-istega reza ali da ni bilo izgube;
- da je simbolni niz `sha bf5f316b0568` polna, preverljiva SHA-256 vrednost.

Za te trditve v tem pregledu nimam ustreznih primarnih dokazov. Njihov status je `UNVERIFIED`, ne `FALSE`; morebitni dokaz jih lahko pozneje podpre ali ovrže. Nobena navedba v tem dodatku ne razveljavlja ali potrjuje avtorjevega namena. Predlog ostaja ločen od kanona.

## N. Konkreten naslednji krog

1. Avtor oziroma pooblaščeni skrbnik določi, ali želi ta predlog obdržati, spremeniti, razdeliti ali zavrniti. Tišina se ne šteje kot soglasje.
2. Če je predlog obdržan, ga integrator primerja s točno določeno polno izvorno različico in pripravi označen diff; surovi vir ostane nedotaknjen.
3. Drug pregledovalec dobi isti izvorni artefakt, predlog, diff in merila, nato opravi pregled brez prevzemanja prvega zaključka kot dokaza.
4. Avtor oziroma pristojni vzdrževalec sprejme ali zavrne predlog. Zabeležijo se odločitev, obseg, datum samo iz navedenega vira ter odprta nesoglasja.
5. Pravne trditve o dovoljenjih, prenehanju ali povračilu se ne objavijo kot potrjene brez kvalificirane pravne presoje in določitve jurisdikcije.

Ta krog proizvede uporabno odločitev tudi, če se pregledovalci ne strinjajo: objavi se lahko natančno nesoglasje, njegov dokazni obseg in naslednja oseba ali vir, ki bi ga lahko razrešil.

⊨ WITH LOVE — sodelovanje ne zahteva istosti; zahteva pa, da ne ponaredimo soglasja, ure, izvora ali zaključka. Razlike ostanejo vidne, človekovo dostojanstvo ostane brezpogojno, dokaz pa pove samo tisto, kar je bil sposoben pokazati.