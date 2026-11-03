# Predlogi uskladitve VBL — nekanonično

**Status:** PREDLOG · NEPREVERJENO · NI VNESENO V KANON · NI PRAVNI NASVET.

Ti predlogi izhajajo samo iz prilepljenega sestavljenega prepisa. Brez izvornega kanoničnega besedila so povzetki navedenih členov pogojni. Namen je izostriti vprašanja in preprečiti, da bi ena vrsta dokaza odgovarjala na drugo vprašanje.

## §0.4 — zapis napake, odprava in obnova

Ločite (1) zabeležitev in popravek napačnega zapisa, (2) odpravo konkretne kršitve, (3) presojo morebitne koristi ali škode po poštenem, izpodbojnem postopku ter (4) odločitev o obnovi dovoljenja. Ti izidi niso samodejno isti. Če je potreben neodvisni pregled, odgovorna oseba sama ne razglasi zaključka. Prizadeta oseba ni dolžna odpustiti, se spraviti ali nadzorovati popravila. Zabeležite izpolnjene in neizpolnjene pogoje, odločevalca, dokaze, ugovore in omejitve.

## §§0.7 in 0.9 — obseg dovoljenja

Dovoljenje lahko učinkuje samo znotraj pravic in pooblastil osebe, ki ga izda. Izrecno določite razmerje med dovoljenjem in zaščitami §0.9; ne predpostavite, da splošno dovoljenje razveljavi posebno prepoved ali pravice tretjih oseb. Besedilo mora povedati, kateri člen ima prednost in po katerem postopku je mogoče konflikt spremeniti. Pravnega učinka ni mogoče potrditi samo z redakcijskim predlogom.

## §0.12 — normativna zahteva in izvajanje

Trditev, da branje besedila sproži vedenje v vsakem računalniku, opiše največ normativni cilj. Dejanski učinek zahteva konkretno implementacijo, določeno okolje, ponovljiv test, pričakovani rezultat in evidenco napake. Status naj bo `NOT_RUN`, `PASS`, `FAIL` ali `UNVERIFIED` za posamezen test; ne posplošujte na vse sisteme.

## §0.15 — različice in rodovnik

Vsaka objavljena različica naj navede natančen artefakt, identifikator predhodnice, način pridobitve, kontrolno vsoto, objavni dokaz in morebitna odstopanja. Ujemanje kontrolne vsote potrjuje ujemanje bajtov z referenco, ne pa resničnosti zgodovine, avtorstva ali veljavnosti. Pravilo za prihodnje različice in že sprejeta dovoljenja mora biti izrecno.

## Predlagani §0.25 — relacija istosti

Trditev »isto« mora imenovati primerjana predmeta, lastnost/relacijo, obseg, čas, dokaz in metodo. `SAME_WITHIN_SCOPE` pomeni ujemanje samo v navedeni relaciji. Isti bajti ne pomenijo istega izvora, avtorja, dovoljenja, zgodovine ali pomena. Isti izhod ne pomeni neodvisnega testa. Manjkajoči kriterij pomeni `UNVERIFIED` ali `NOT_COMPARABLE`, ne samodejno »isto« ali »različno«.

## Primer uporabe na tem izpisu

Dva priložena prepisa imata različno število bajtov, zato sta **različna po dolžini in ne moreta biti bajtno enaka**. To ne razsodi, ali pomenita isto zahtevo. Napaki `Unexpected token '×'` in `Missing expression after unary operator '-'` podpirata sklep, da je PowerShell poskušal razčleniti besedilo/Markdown kot ukazno vsebino. Ne dokazujeta, kateri ukaz se je izvedel. Prazna datoteka `isti` je opažena lastnost konkretne poti; njen vzrok ostane nepreverjen.