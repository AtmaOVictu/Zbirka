# VBL 0.1100 × 10⁴ — POSKUS 10: most in dokaz

**Status: DELOVNI PAKET · OSNUTEK · NI OBJAVA / NI KANON.**

## Kaj ta paket dejansko naredi

- Poveže obstoječi zvočni poskus 9 z lokalnim predvajalnikom in popravljeno MIDI-datoteko.
- Zapiše velikosti in SHA-256 za razpoložljive datoteke.
- Preveri popravljeni MIDI z neodvisnim lokalnim razčlenjevalnikom `mido`: format 1, 7 stez, 480 ticks/beat; razčlenitev uspe.
- Ohrani razliko med **VBL 0.1080 × 10⁴ · POSKUS 9** (oznaka v zvočnih datotekah) in **VBL 0.1100 × 10⁴** (besedilo, prilepljeno v pogovor). Rodovnik med njima ni dokazan.

## Predvajanje

Odpri `VBL-0.1100-POSKUS10-predvajalnik.html` v brskalniku. Predvajalnik uporablja WAV iz tega paketa. Predvajanje je odvisno od brskalnika in zvočne naprave; samo prisotnost gumba ali datoteke ni dokaz, da je zvok dejansko slišan.

## Rezultati, ki jih podpirajo datoteke

- WAV: 190,214 s, stereo, 22.050 Hz, 16-bit PCM.
- Popravljeni MIDI: uspešno razčlenjen lokalno; 7 stez. To ne dokazuje, da se vsak instrument sliši pravilno ali da vse aplikacije predvajajo enako.
- HTML popravek: sintaktično preverjanje JavaScripta je bilo izvedeno v predhodnem koraku; to ni celovit test uporabniškega vmesnika v vseh brskalnikih.

## Kaj še ni dokazano

1. Da je POSKUS 9 zvočno boljši od POSKUSA 8: v tem paketu ni primerljivega WAV-a POSKUSA 8.
2. Da je 0.1100 uradno objavljena, pravno veljavna ali potrjena naslednica 0.1080.
3. Da je ura v napravi točna ali da je časovni žig neodvisno potrjen.
4. Da so oddaljeni repozitoriji, objave ali kontrolne vsote preverjeni.
5. Da je prilepljeno besedilo 0.1100 popolno: prejeti izsek se konča med §0.6.

## Predlog operativnega dodatka za §0.20 — čas kot dokaz

Vsak zapis časa mora vsebovati: (a) ISO 8601 časovni žig z odmikom UTC; (b) navedeni vir ure; (c) trenutek meritve; (d) dosegljivo natančnost; (e) stanje `VERIFIED`, `UNVERIFIED` ali `UNAVAILABLE`; (f) identifikator postopka, ki je čas zapisal. Če vira ni mogoče preveriti, sistem ne sme ugibati. Popravek ustvari nov zapis in ohrani starega. Časovni žig sam po sebi ne dokazuje avtorstva, vrstnega reda objave, pravilnosti trditve ali neodvisnosti priče.

## Predlog strojno berljivega rodovnika za §0.15

Vsaka različica naj ima ločen zapis s polji `version`, `declared_date`, `predecessor`, `artifact_sha256`, `publication_uri`, `commit_id`, `release_status`, `verification_status`, `witness`, `known_gaps`. Neznana polja naj bodo `null`, ne ugibana. Povezava med različicama je `VERIFIED` šele, ko je dokazano, katera vsebina je bila objavljena in katera vsebina je njen predhodnik.

## Naslednji preverljivi koraki

1. Priskrbeti POSKUS 8 WAV in primerjati oba posnetka pod enakimi pogoji.
2. Poslušalski pregled opraviti ločeno od tehničnih meritev.
3. Prejeti celotno besedilo 0.1100, da se ga lahko razčleni in preverijo vsi notranji sklici.
4. Dodati dokaz objave/commita in neodvisno pričo, ne samo lokalni manifest.

**Načelo:** meriti tudi lastno merilo; rezultat označiti po dokazih, ne po želji.
