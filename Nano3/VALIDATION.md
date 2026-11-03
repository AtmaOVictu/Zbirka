# Validacijski zapis

Datum: 2026-10-30  
Okolje: Python 3.13.5, lokalni začasni imenik, brez omrežnih CI izvajanj.

| Preverjanje | Rezultat | Opomba |
|---|---|---|
| `py_compile` na generatorju in testih | PASS | Brez sintaktičnih napak |
| `python test_manifest_gen.py` | PASS | 14/14 testov |
| CLI tok: generator ustvari manifest, nato `--check` | PASS | Izoliran sintetični checkout |
| Primerjava predlaganih metapodatkov s trenutno objavljenim manifestom | PASS | Polja so enaka; verzija/datum nista ugibana |
| Rekonstrukcija SHA Git blob štirih izhodiščnih datotek | PASS | Ujemanje z zajetimi Git SHA; preverjeno še enkrat po delu |
| `git apply --check` | PASS | Sintetični checkout iz preverjene osnove |
| `git apply` v sintetičnem checkoutu | PASS | Patch se uporabi brez konflikta |
| Polni projektni CI | NOT RUN | Ni celotnega lokalnega klona in ni izvedbe GitHub Actions |
| Python 3.10 / 3.11 / 3.12 lokalno | NOT RUN | V tem okolju ni bilo teh izvršljivih datotek |
| GitHub push / PR | NOT DONE | Ni remote veje ali PR |

## Testirana vedenja

1. Ujemajoči se manifest uspe.
2. Napačna različica ne uspe, tudi če so vse kontrolne vsote datotek enake.
3. Napačen datum ne uspe.
4. Napačno pravilo ne uspe.
5. Nepredvideno dodatno polje manifesta ne uspe.
6. Spremenjeni bajti krite datoteke ne uspejo.
7. Manjkajoča krita datoteka ne uspe zaprto.
8. Manjkajoče obvezno polje vira metapodatkov ne uspe.
9. Napačen JSON manifesta vrne razumljivo napako, ne nekontroliran traceback.
10. Manjkajoč manifest ne uspe.
11. Vir metapodatkov ne sme vsebovati `items`.
12. Vir metapodatkov mora biti JSON-objekt.
13. Manjkajoč vir metapodatkov ne uspe.
14. Sprememba opombe v viru povzroči odmik obstoječega manifesta.

`PASS` tukaj pomeni uspeh lokalnega regresijskega testa; ne pomeni GitHub CI, zunanje revizije ali pravne potrditve.
