# Uporaba paketov v ciljnih repozitorijih

To je **lokalni staging**, ne uspešen GitHub push. Branje `README.md` na privzeti veji `main` je bilo potrjeno v vseh treh repozitorijih. Lokalni `git` pa v tem okolju ne doseže `github.com`, povezani konektor pa ne ponuja neposrednega prenosa te lokalne celotne drevesne strukture kot enega repo-spremembnega paketa. Zato tukaj ni bila ustvarjena nobena veja, commit ali PR; pripravljeni ZIP-i ostajajo patchi za pregled in uporabo.

1. `VBL-cookbook-repo-patch-2026-10-25.zip` — razširi v koren `AtmaOVictu/cookbook`. Vključi `vbl/`.
2. `VBL-language-repo-patch-2026-10-25.zip` — razširi v koren `AtmaOVictu/Slovenian-Language-Technologies-Overview`. Vključi `VBL/`.
3. `VBL-agents-cli-repo-patch-2026-10-25.zip` — razširi v koren `AtmaOVictu/agents-cli`. Vključi `skills/vbl-verification-before-assertion/`.

Vsak paket ima svoj `SHA256SUMS.txt` za datoteke v ciljni mapi. Najprej preglej diff in kandidatske dokumente; ne zamenjuj obstoječih `LICENSE.md`, `README.md` ali drugih kanoničnih datotek samodejno. VBL 2.6 izvoz in VBL 10.3.0 morata ostati ločena, dokler ni dokumentirana in neodvisno preverjena njuna različica/rodovnik.
