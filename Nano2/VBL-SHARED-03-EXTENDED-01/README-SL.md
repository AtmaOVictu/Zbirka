# VBL-SHARED-03 — razširitev 01

**Stanje:** OSNUTEK · NI KANON · NEODVISNI PREGLED NI OPRAVLJEN · NI PRAVNI NASVET.

Ta razširitev konkretizira varno odpiranje prepisa, lokalno zbiranje dokazov, zapis ure in predloge za uskladitev §§0.4, 0.7, 0.12, 0.15 ter predlaganega §0.25. Osnovni dodatek je priložen nespremenjen v `base/`.

## Kaj je vključeno

- `scripts/Open-VBLTranscript.ps1` ustvari prazen vhod samo, če ga še ni, nato ustvari ločeno delovno kopijo in odpre kopijo v Beležnici. Izvirnika ne prepisuje.
- `scripts/Get-VblLocalEvidence.ps1` zbere lokalni odčitek ure, časovni pas, stanje točno določene datoteke, alias `ni` in izhod `git status --short`. Windows Time poizvedbe so neobvezne in samo bralne.
- `templates/POWERSHELL-VBL-CLOCK-READOUT.md` določa, katere odčitke in napake ohraniti.
- `templates/VBL-verification-record.template.json` je prazen vzorec, ne rezultat preverjanja.
- `proposals/PROPOSALS-HARMONIZATION.md` vsebuje predloge, ki niso vnesene v kanon.
- `evidence/VBL-WORKTREE-OBSERVATION-01.json` je lokalni zapis enega opažanja; ne dokazuje vzroka nastanka datoteke `isti`.
- `base/` vsebuje prejši dodatek in njegov SHA-256 sidecar.

## Meje dokazov

SHA-256 identificira bajte v primerjavi z znano vrednostjo; sam po sebi ne potrjuje avtorstva, izvora, dovoljenja, kanoničnosti ali pravnega učinka. Lokalna ura ni neodvisna časovna potrditev. `git status` ne pokaže prezrtih datotek brez dodatnega stikala, zato prazen izhod ne pomeni, da v delovnem drevesu ni nobenih lokalnih datotek.

Transcript in PowerShell izpis sta sestavljena pogovorna zapisa. Izpis podpira razlago, da je lupina poskušala razčleniti prozo/Markdown kot ukazno vsebino; sam ne dokazuje, kateri ukazi so se uspešno izvedli. Datoteka `isti`, opažena kot prazna, je skladna z možnim učinkom aliasa `ni` (`New-Item`), vendar pripis vzroka ostaja NEPREVERJEN.

Paketa nismo pognali v uporabnikovi interaktivni lupini; skripta za zbiranje je namenjena poznejšemu zagonu po pregledu. Njen izhod je lokalno opažanje, ne neodvisna priča.

## Integriteta

`MANIFEST-SHA256.json` vsebuje velikosti in SHA-256 vseh datotek v tem imeniku razen samega manifesta. ZIP ima ločen `.sha256.txt` ob njem. Vsak prejemnik naj preveri oboje.