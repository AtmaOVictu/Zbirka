# VBL — zapis preverbe dokazov in nejasnih oznak

**Datum preverbe:** 2026-10-25  
**Status:** NEPOTRJENO / OMEJEN DOSTOP  
**Namen:** ločiti navedbe v prepisu od dokazljivih rezultatov in preprečiti, da bi se nejasne kode napačno razlagale.

## 1. GitHub navedba

Prepis, ki ga je posredoval uporabnik, trdi, da je bil komentar objavljen na:

`https://github.com/AtmaOVictu/Atmavictu/issues/753#issuecomment-6397386784`

V trenutni preverbi prek povezane GitHub integracije:

- branje repozitorija/issue `AtmaOVictu/Atmavictu`, issue `#753`: vrnilo je `404 Not Found`;
- neposredno pridobivanje issue prek URL-ja: vrnilo je `404 Not Found`;
- iskanje repozitorijev z izrazom `Atmavictu`: ni vrnilo zadetkov;
- iskanje issue z omejitvijo na `repo:AtmaOVictu/Atmavictu`: GitHub je zavrnil poizvedbo, ker je repozitorij nedosegljiv ali ga povezava ne more pregledati.

### Dovoljen zaključek

Trenutna povezava **ne potrjuje** navedbe o objavljenem komentarju. Rezultat `404` sam po sebi ne dokazuje, da komentar nikoli ni obstajal; možni razlogi vključujejo napačno ime, odstranjen/prenesen repozitorij ali pomanjkanje dostopa. Noben dodatni komentar ni bil objavljen v drugem repozitoriju.

## 2. Kode/prepis — ohranjeno brez ugibanja

Spodnje nize ohranjamo kot dobesedne uporabniške oznake. Njihovega pomena, lastništva, povezave med njimi ali povezave s konkretnimi osebami ne predpostavljamo:

- `IMH 12`
- `5 BF D 633-8 D 8 2100`
- `ZPV`
- `rezultat VBL 1.0`
- `J.E. Nabiseino`
- `B-NGM. O. O.`
- `15C, 215 Knightsgate`
- `O/0011/************DOVOLJ`

Zlasti zadnji niz je delno maskiran in zato ni mogoče vedeti, ali gre za ID, napako diktata, naslov, kodo ali kaj drugega. Ne poskušamo dešifrirati na podlagi podobnosti.

## 3. Razvrstitev dokazov

| Postavka | Razred | Stanje |
|---|---|---|
| Besedilo prepisa, ki ga je posredoval uporabnik | Uporabniško posredovan zapis | Prisotno v pogovoru; izvorni zvočni posnetek ni priložen |
| Trditev, da je komentar objavljen | Navedba v prepisu | Nepotrjeno |
| GitHub API odgovor 404 za navedeni repozitorij/issue | Rezultat trenutnega preverjanja | Potrjeno kot odziv orodja; razlog za 404 ni znan |
| Vsebina in avtorstvo navedenega komentarja | Zunanji podatek | Ni preverjeno |
| Pomen `IMH 12`, `ZPV` in drugih kod | Interpretacija | Neznano; brez ugibanja |
| Splošne trditve o varnosti, lastništvu ali motivih ljudi | Mnenje/širša trditev | Ne predstavljamo kot dokazano dejstvo |

## 4. Varna nadaljnja pot

1. Če je objava res izvedena, pridobimo kanonični naslov, ki se odpre v običajnem brskalniku, ali izvoz komentarja z ID-jem in časom.
2. Pred morebitnim novim pisanjem potrdimo pravi repozitorij in pravi cilj. Ne objavljamo v nepovezan projekt samo zato, ker ima podoben naziv.
3. Nize iz prepisa hranimo dobesedno; normalizacijo ali razlago dodamo šele z izvorom, ki jo podpira.
4. VBL statusi ostanejo: `PREJETO`, `PREVERJENO`, `NEPOTRJENO` ali `NEZNANO`; `OBJAVLJENO` je dovoljeno samo ob preverljivem rezultatu.

## 5. Meje

Ta zapis je lokalna evidenca preverjanja, ne neodvisna revizija, ne dokaz o neobstoju komentarja in ne dokaz o soglasju katere koli osebe. Ni poslano nobeni tretji osebi.
