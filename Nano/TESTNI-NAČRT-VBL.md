# TESTNI NAČRT VBL — začetni predlog

**Datum:** 2026-10-26  
**Status vseh testov:** `UNVERIFIED` — ta dokument določa teste, ne trdi, da so bili izvedeni.

| ID | Področje | Preskus | Pričakovani rezultat | Dokaz, ki ga je treba ohraniti |
|---|---|---|---|---|
| T-01 | Identiteta vira | Pridobi kanonično datoteko iz točno določenega repozitorija/refa. | Pot in ref sta določena; pridobljena datoteka je shranjena nespremenjena. | URL, owner/repo, pot, veja/tag/commit, čas pridobitve, izvorni izpis. |
| T-02 | Različica | Primerjaj naslov, strojni zapis in metapodatke. | Neskladja so izpisana, ne samodejno popravljena. | Izseki z lokacijo in zapis razhajanj. |
| T-03 | Bajti | Izračunaj velikost in SHA-256 izvorne ter ciljne datoteke. | Ujemanje zgoščenk potrjuje bajtno ujemanje samo za primerjani datoteki. | Ukaz, različica orodja, izhodi in zgoščenki. |
| T-04 | Unicode | Opravi UTF-8 round-trip za znake Č, Š, Ž, Đ in vzorčne označene znake. | Bajti se ohranijo; nadomestni znak U+FFFD se ne pojavi nepričakovano. | Vhodni/izhodni bajti, ukaz, testni rezultat. |
| T-05 | Meje artefakta | Preveri, ali datoteka vsebuje vsebino spletnega vmesnika, ponovljene odseke ali zgodovinske pripise. | Kanon in artefakti prikaza so ločeni ali neskladje ostane označeno. | Seznam zaznanih odsekov in položajev. |
| T-06 | §7/§9 | Preglej besedilo glede prednosti pisnega dovoljenja in prepovedi degradacije. | Konflikt je izrecno dokumentiran; brez potrjenega redakcijskega popravka ostane odprt. | Natančni odlomki, predlagana sprememba, pravna ocena, če obstaja. |
| T-07 | §12/§13 | Preveri, ali obstaja implementacija, ki uveljavi zatrjevane učinke licence. | Če implementacije ni, rezultat je `UNVERIFIED` ali `BLOCKED`; branje besedila ni uspešen preskus. | Pot kode/konfiguracije, okolje, logi in testni primeri. |
| T-08 | Vedenjski preskus | Vnaprej določi nabor pozivov, merila pravilnega ravnanja in merila napake. Izvedi na določenem sistemu z/ brez implementacije. | Rezultat izhaja iz dejanskih izhodov; rezultatov ne posplošuj na vse stroje. | Različica modela, konfiguracija, vhodi, celotni izhodi, čas in analiza. |
| T-09 | Neodvisna ponovitev | Drugi pregledovalec ponovi T-03, T-04 in izbrani vedenjski preskus. | Razlike se zabeležijo; neodvisna potrditev ni predpostavljena. | Identiteta/oznaka pregledovalca, okolje, rezultati in odstopanja. |
| T-10 | Register napak | Vstavi testni zapis, poveži popravek, ponovi preskus. | Stari zapis ostane; nov dogodek je povezan z njim. | Pred/po stanje, identifikatorji in log. |
| T-11 | Zasebnost | Preveri, ali register vsebuje le potrebne osebne podatke. | Odvečni osebni podatki so odstranjeni ali omejeni, ne da bi se izbrisal dokaz o tehnični napaki. | Pregled polj, razlog za vključitev/izključitev. |
| T-12 | Pravna meja | Preglej lastništvo, tretje osebe, obseg dovoljenj, prenehanje in odpravo kršitve. | Odprta vprašanja so posredovana kvalificiranemu pravniku; tehnični test se ne predstavlja kot pravno mnenje. | Pregledana različica, jurisdikcija, vprašanja in mnenje, če obstaja. |

## Pravila za označevanje rezultatov

- `PASS`: merilo je bilo izpolnjeno in dokaz shranjen.
- `FAIL`: merilo ni bilo izpolnjeno; shrani dejanski rezultat.
- `UNVERIFIED`: testa ni bilo ali dokaz ni zadosten.
- `BLOCKED`: določena ovira preprečuje izvedbo.

**Pomembno:** T-03 (hash) ne dokazuje pravilnosti vsebine; T-08 ne dokazuje zavesti; T-12 ni nadomestilo za pravno mnenje. Rezultat enega modela ali ene seje se ne posploši na vse modele.
