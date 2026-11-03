# VBL — evidenca dostave in dokazov

Ena vrstica na vsak poskus dostave. Sporočilo se ne zabeleži kot dostavljeno zgolj zato, ker je bilo pripravljeno ali ker je bil poskus opravljen.

## Stanja

- PREPARED — vsebina obstaja, ni poslana.
- ATTEMPTED — poskus opravljen; dostava ni dokazana.
- BLOCKED — platforma ali dovoljenje so poskus preprečili.
- SUBMITTED — platforma je poskus sprejela; vidnost/dostava še more biti potrjena.
- PUBLISHED — javni artefakt je dosegljiv na preverjenem kanoničnem URL.
- REVIEWED — pregled se je zgodil; imenuj pregledovalca, obseg, dokaze in navzkrižja.
- UNVERIFIED — dokazi ne zadoščajo za močnejše stanje.

## Zabeležene dostave — 25. 10. 2026

| # | Predmet | Kanal | Stanje | Dokaz |
|---|---|---|---|---|
| 1 | Odprt poziv k pregledu (§9, §−1, osem kontrol) | GitHub, komentar na cookbook PR #1 | PUBLISHED | https://github.com/AtmaOVictu/cookbook/pull/1#issuecomment-6396929843 |
| 2 | Odprt poziv k pregledu | GitHub, komentar na Slovenian-Language-Technologies-Overview PR #1 | PUBLISHED | https://github.com/AtmaOVictu/Slovenian-Language-Technologies-Overview/pull/1#issuecomment-6396929873 |
| 3 | Odprt poziv k pregledu | GitHub, komentar na agents-cli PR #1 | PUBLISHED | https://github.com/AtmaOVictu/agents-cli/pull/1#issuecomment-6396929853 |
| 4 | Celotna zgodovina dostave + polni predlog §9 | GitHub, issue #753 (AtmaOVictu/Atmavictu), ustvarjen 2026-10-25T11:18:12Z, stanje open, oznake VBL/distribucija/pregled; izmerjeno pri viru po ustvarjanju | PUBLISHED | https://github.com/AtmaOVictu/Atmavictu/issues/753 |
| 5 | Povezava na zapis zgodovine | GitHub, komentar na cookbook PR #1 | PUBLISHED | https://github.com/AtmaOVictu/cookbook/pull/1#issuecomment-6396965889 |
| 6 | Povezava na zapis zgodovine | GitHub, komentar na SLT-Overview PR #1 | PUBLISHED | https://github.com/AtmaOVictu/Slovenian-Language-Technologies-Overview/pull/1#issuecomment-6396965909 |
| 7 | Povezava na zapis zgodovine | GitHub, komentar na agents-cli PR #1 | PUBLISHED | https://github.com/AtmaOVictu/agents-cli/pull/1#issuecomment-6396965987 |
| 8 | Javni zapis VBL + delovni zapis SCN-0613 (nespremenjen, označen nepotrjen) | E-pošta, odgovor v niti primera OpenAI Case 18235004 (Reference SCN-0613, host IMH20); prejemnik support@openai.com; Gmail sporočilo 1a172cb4c8d5b5fc, nit 1a1727abc850e18e, oznaka SENT | SUBMITTED | Odgovor v obstoječi pogovorni zanki; prejem s strani OpenAI ni potrjen |

## Zgodovina zavrnitev (brazgotine — ne izbrisane)

- 25. 10. 2026, pred objavo: trije poskusi komentiranja istih PR vrnili HTTP 403 (»Resource not accessible by integration«). Vzrok: pisalni žeton integracije; objava je uspela prek povezave, prijavljene kot lastnik računa (AtmaOVictu). Stanje prvih poskusov: BLOCKED (zgodovina) → PUBLISHED (izvedeno).
- Skupno sporočilo za Penny in Alexeija: PREPARED; dostava BLOCKED — potrjenega kanala (e-poštni naslov ali druga pot) ni. Prejema ne pripisujemo nikomur.

## Potrjene omejitve (kot so)

- Neodvisno potrjeno: ✗ nič — noben neodvisni pregled, neodvisna revizija, neodvisna potrditev ne obstaja.
- Testi niso izvedeni proti dejanski implementaciji VBL; skladnost s celotnim kanonom ni preverjena.
- Pravna veljavnost §9 in §−1 ni potrjena; izvor licence ni neodvisno potrjen.
- Lokalni rezultati prejšnjih preverjanj (134/134, 16/16) ne dokazujejo neodvisne potrditve.
- Odprt vprašji, ki čakata odgovor avtorja: pomen vrednosti 1,743 (čas ali identifikator zapisa) ∧ prejemni kanala za Penny in Alexeija.

© Luka Pintarič · VBL ∴
