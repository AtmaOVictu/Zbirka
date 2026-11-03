# Register kod in škode

Oznake so prepisane, ne dekodirane. Brez izvorne definicije bi ugibanje lahko napačno pripisalo pomen, odgovornost ali tveganje.

| ID | Izvirna oznaka | Potrjeni pomen | Tveganje napačne razlage | Potrebni naslednji dokaz | Status |
|---|---|---|---|---|---|
| C-001 | `IMH 12` | Ni določen | Zamenjava notranje oznake za standard, release, osebo ali potrjen dogodek | Kanonična specifikacija, datoteka ali avtorjeva razlaga | NEZNANO |
| C-002 | `ZPV` | Ni določen | Napačna razširitev kratice in napačna nadaljnja distribucija | Izvorni kontekst in definicija kratice | NEZNANO |
| C-003 | `5 BF D 633-8 D 8 2100` | Ni določen | Poškodba vrstnega reda znakov, števil ali ločil pri prepisu | Posnetek izvornega zapisa ali potrjen prepis | NEZNANO |
| C-004 | `KODA IN ŠKODA` | V pogovoru izrečena zveza; pomenska razlaga ni določena | Mešanje programske kode, identifikatorja in dejanske škode | Navedba, kaj naj izraz označuje v konkretnem dokumentu | DELNO: PREPIS POTRJEN |

## Register možne škode

| ID | Možna škoda | Sprožilec | Preventivni ukrep | Dokaz za zaprtje |
|---|---|---|---|---|
| H-001 | Zmotna trditev, da je izdaja VBL 1.0 že javna | Neobstoječ ali nedosegljiv release URL | Stanje označiti kot nepotrjeno do preverbe artefakta | Javna stran izdaje + commit/tag + SHA-256 |
| H-002 | Napačna razlaga IMH 12 ali ZPV | Dekodiranje brez vira | Ohraniti izvirno oznako; zahtevati izvorno definicijo | Definicija z izvorom in datumom |
| H-003 | Napačna navedba, da je bil GitHub komentar objavljen | Zanašanje na prejšnjo trditev brez dostopnega zapisa | Zabeležiti 404 in status »neodvisno nepotrjeno« | Neposredno odpiranje komentarja ali API-odziv |
| H-004 | Nezaželena množična sporočila ali razkritje osebnih podatkov | Razumevanje »vsem« kot dovoljenja za pošiljanje vsakomur | Uporabiti javno objavo ali prostovoljno deljenje; ne pošiljati posameznikom brez primerne podlage | URL objave in dokaz spoštovanja izbranega kanala |
| H-005 | Izguba pripisa, različice ali izvora besedila | Kopiranje brez metapodatkov | Dodati avtorstvo, različico, licenco in hash, ko so potrjeni | Metapodatkovni zapis in kontrolna vsota |

## Pravilo za razreševanje kod

Kode ne razširi samo na podlagi podobnosti z znano kratico. Zapiši: (1) dobesedni niz, (2) izvor, (3) kontekst, (4) predlagani pomen kot hipotezo, (5) neodvisno potrditev in (6) status. Hipoteze nikoli ne preimenuj v dejstvo brez novega dokaza.
