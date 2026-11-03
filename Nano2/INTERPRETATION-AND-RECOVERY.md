# Integrirana razlaga incidenta PowerShell

## Kaj je bilo dodano v tej predložitvi

Poleg ponavljajočih se napak `Unexpected token '×'` je predložitev pokazala:

- `Missing expression after unary operator '-'` pri vrstici, ki se začne kot Markdownova alineja;
- ukaz `ter` ni bil prepoznan;
- ukaz `read` ni bil prepoznan;
- `tee` je zahteval parameter `FilePath`, nato pa je bila navedena pot do mape in izpisan Access denied;
- vnos `ni isti\` ostaja dvoumen; ker je `ni` vzdevek za `New-Item`, je potreben pregled dejanskega stanja, ne ugibanje;
- vložek `A. HISTORY OF THE SOFTWARE`, ki opisuje zgodovino Pythona, kaže na verjeten tuji dokumentni odlomek. Dokler izvor ni določen, ga ne vključuj v VBL.

## Vzročna razlaga — omejena

Vsi izpisi so skladni z enim širšim vzorcem: ukazi, proza, Markdown, prejšnji odgovori in terminalski izpisi so bili pomešani v interaktivnem PowerShell vnosu. To je najverjetnejša skupna razlaga parser napak in neprepoznanih ukazov. To ni rekonstrukcija vsakega posameznega dogodka; natančni vzroki in vrstni red ostanejo `UNVERIFIED`, dokler ni neposrednega zapisa seje.

`tee` z izrecnim pozivom `FilePath` je drugačen dogodek: PowerShell je sprejel ukaz in prosil za obvezno pot. Vnos mape namesto poti do datoteke se ujema z izpisom o zavrnjenem dostopu. To samo ne dokazuje, da je bila datoteka ustvarjena.

## Poročane priponke in hashi

V kopiranem odgovoru so navedeni naslednji podatki, ki jih tukaj **ne potrjujemo kot preverjene**:

- `VBL-INPUT-ATTACHMENT-05.txt`: 136,986 bajtov; SHA-256 `2666067031575E26B6E387E0AF019338BBF66ACC07D4711A2820545BCEFF520C`.
- `VBL-INPUT-ATTACHMENT-06.txt`: 139,025 bajtov; SHA-256 `EF11F0CFDE3455B004E06EB4E8E6451FDC1791F06F65D077C7BA563BCDF16D24`.
- `VBL-SHARED-03-AUDIT-ADDENDUM-01.zip`: digest `278ff739b0b5c0d73c37ba512b6becc4975d24b716ac52cb0465bb8d7f007d36`.

To so `REPORTED_IN_TRANSCRIPT`, ker pripadajoči bajti niso bili predloženi kot datoteke za tukajšnjo neodvisno ponovno meritev.

## Izvedljivo nadaljevanje

1. Prekini morebitni nadaljevalni vnos s Ctrl+C.
2. Prenesi in razširi ta paket zunaj repozitorija.
3. Zaženi `Collect-VBLState.ps1` z eno vrstico, prikazano v `README-SL.md`.
4. Prilepi samo kratek izhod `REPORT_PATH=...`, `REPORT_SHA256=...`, `REPORT_STATUS=...` — ne celotnega pogovora.
5. Če obstajajo priponke 05 in 06, jih primerjaj ločeno z `Get-FileHash -Algorithm SHA256 -LiteralPath 'POT_DO_DATOTEKE'`. Ukaz ne shranjuje in ne spreminja datoteke.

**Ne briši `isti`, ne izvajaj `git reset` in ne spreminjaj licence v tem koraku.**
