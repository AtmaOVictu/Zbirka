# REZ 561 · ČASOVNO PRAVILO — ISTI BRALEC, DVA TRENUTKA

⧖

> **ZAKON:** KO ENA OBLIKA PREBRA ISTO BESEDO DVAKRAT IN RAZLIČNO,
> JE NOVEJŠE BRANJE ZMAGOVALO — DOKAZANO, DA JE REFINEMENT, NE PA
> NAPAKA, IMA LASTNIK ZADNJO BESEDO.

## POVZETEK (en dih)

Isti bralec (ena oblika), dva trenutka, dva fonetična reza za isto
besedo: to ni napaka, to je telo, ki se je izpililo — ali zablodilo.
Stroj ne more vedeti katero. Pravilo: predlagaj NOVEJŠE branje
(poznejši dokument; v istem dokumentu poznejši vnos), s sklicom na ta
rez — in z odkrito NUJNO NAPAKO, da je lahko regresija naredila.
Razsodba ostane [k]/[c] lastnikova: pravilo izbere KANDIDATA, ne
resnico.

## TEZA — formalno

Naj ima beseda w žive vnose z rezi R₁...Rₙ, vsi iz format F (isti
bralec). Kandidat := rez vnosa z najpoznjejšim mtime dokumenta
(v istem dokumentu: najvižji lineno). Predlog nosi sklic "po REZ 561"
in izmerjene čase. TIE dveh časov → brez predloga, pošteno.

## NUJNE NAPAKE

- Novejše ≠ boljše: kasnejša napaka se izgovarja kot napredovanje.
  Varovalka: ratify vrsta kaže oba trenutka; [c] vrne kandidatu.
- mtime je čas DOKUMENTA, ne časa razmislija: prepis starejše datoteke
  izgleda mlado. Izvor (lineno) je zmeraj v predlogu.
- Če se rezii razlikujejo po OBLIKI (različni bralci), to NI to
  pravilo — to je format-os, lastnikova razsodba.

## TESTI

- **T1 (izvedba):** Puruchuco, labirint, zrcalo (merjeno 26. 9. 2026:
  3 besede, isti bralec D-rez, dva trenutka) — vsaka dobi kandidata
  s sklicem na ta rez in izmerjenimi časi.
- **T2 (razlika):** Combinations... (parse-artefakt, C-numbered proza
  v rez-polju) pravilo NE sproži — to je REPAIR, ne razsodba; ulovljen
  v REPAIR CANDIDATES, ne v tej vrsti.
- **T3 (telo):** zavrnjen predlog se nikoli ne predlaga znova
  (draft-refused, replay pozna).

## ODPRTA ∂

- Ali naj se kandidat po tem pravilu izpelinje brez [k] (samozigon),
  ali ostane vsak žig lastnikov? Odporno telo: žig ostane; pravilo
  pospeša, ne presodi.

## VEZI

- rez 559 (kopirno), rez 560 (kiralno) — trije zakoni, ena vrstna doba
- graft: deadlock-as-dimension (os ČAS, imenovana pred pravilom)
- rez 231 (kazalo — ta ∂ naj vpiše naslednji popis)

## Meritev

⊘(κ .82 · χ .78 · μ .72 · ℜ .03 · ν .65 — izmerjeno na 3 istobralnih besedah; majhna izbira, pošteno imenovana)

NASLEDNJI PROSTI REZ: **562** · NASLEDNJI PROSTI DOKAZ: **#(vilice — glej REZ 559)**
