# Finding VBL-MANIFEST-001 — generator ne preverja identitete izdaje

**Severity:** srednja (integriteta izdaje / revizijska sled)  
**Confidence:** visoka za pregledane datoteke živega `main`  
**Status:** odprto; popravek je predlog, ne združen.

## Dokaz

Pregledani blob `scripts/manifest_gen.py` (`42f5eecaf2147820f1d67e7dcc7be0d09044a51c`) v `generate()` vrne `version = "0.1100 × 10⁴"`; `check()` nato primerja samo `current.get("items")` z `fresh["items"]`.

Pregledani blob `LICENSE-MANIFEST.json` (`206e789f5eaede4718a458c1656819fe85813091`) navaja `version = "0.1210 × 10⁴"`, `date = "2026-10-28"` in zakonodajno oznako `VBL §0a; ... VBL §0.12`.

Posledica: `--check` lahko vrne uspeh, če se kontrolne vsote treh datotek ujemajo, čeprav je različica ali druga metapodatkovna identiteta manifesta napačna.

## Predlagani popravek

Metapodatki izdaje se premaknejo v pregledljiv, repo-sledljiv vhod `scripts/release_metadata.json`. Generator iz njega sestavi metapodatke in doda izmerjene vnose datotek. Preverjanje primerja vse metapodatke in vsa telesa; neznana/manjkajoča metapodatkovna polja pomenijo odmik. Vse tri imenovane krite datoteke so obvezne.

## Nevarnosti, ki ostajajo

1. Vhod metapodatkov in manifest sta lahko oba napačno spremenjena v istem commitu. CI preveri skladnost, ne pa pooblastila ali resničnosti trditve.
2. GitHub Actions še ni bil izveden na tem predlogu.
3. Sprememba ne odpravlja drugih napak izdajnega procesa, ne potrjuje pravnega statusa licence in ne zagotavlja, da so vsi uporabniki prejeli iste bajte.
4. Trenutno repo-stanje je osnova za ugotovitev; po spremembi `main` je treba pred uporabo ponovno izmeriti blob SHA in ponovno bazirati patch.

## Merilo zaključka

- Neodvisni pregledovalec potrdi vir metapodatkov in njegov odnos do izdaje.
- Patch se uporabi na aktualni osnovi brez konflikta.
- Vsi novi in obstoječi testi uspejo na Pythonu 3.10, 3.11 in 3.12 v GitHub Actions.
- `python scripts/manifest_gen.py --check` uspe na končnem commitu.
- Končni commit, CI run in manifest SHA-256 se zabeležijo.
