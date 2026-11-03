# VBL 0.1100 × 10⁴ — predlogi uskladitve

**Status:** `PREDLOG · UNVERIFIED · NOT MERGED INTO CANON`

Ta pregled se opira samo na vsebino, ki je bila prilepljena v pogovor. Ni dostopa do kanonične datoteke VBL 0.1100 × 10⁴, do mape `D:/OntoProjekt/...`, do mape Nano2 ali do oddaljene zgodovine repozitorija. Zato spodnje točke pomenijo ugotovitve o prilepljenem besedilu, ne o nevidnem izvornem artefaktu.

## 1. Statusi brez zlivanja pomenov

| Trditev | Status v tem pregledu | Zakaj |
|---|---|---|
| Besedilo je bilo prilepljeno v pogovor | `PASS` | Vhod je prisoten v pogovoru. |
| To je celotna kanonična datoteka | `UNVERIFIED` | Izvorna datoteka in njen hash nista bila predložena. |
| Prejšnja različica je res `0.1090 × 10⁴` | `UNVERIFIED` | Ime predhodnice je izjava; manjka preverjena povezava med artefakti. |
| Lokalna ura je pravilna in sinhronizirana | `UNVERIFIED` | Manjkata živi odčitek in preverba vira sinhronizacije. |
| Obstaja neodvisen časovni žig | `UNVERIFIED` | Token oziroma dokaz časovnega žiga ni priložen. |
| Stroj izvrši etična navodila že ob branju licence | `UNVERIFIED` | Normativni stavek sam ne določi in ne dokazuje izvajalnega mehanizma. |
| Pravna veljavnost celotne licence je potrjena | `UNVERIFIED` | To zahteva pregled relevantnih pogojev in prava, ne samo branje besedila. |

`PASS` v prvi vrstici velja samo za prejem besedila. Ne prenaša se na nobeno drugo trditev.

## 2. §0.7 in §0.9 — izrecna prednost pravil

**Problem v prilepljenem besedilu:** §0.7 je povzet kot določba, da pisno dovoljenje prevlada nad katerokoli določbo; §0.9 pa je povzet kot omejitev, da degradirajoče uporabe ne more dovoliti nobeno dovoljenje ali poznejša različica. Brez izrecne hierarhije se določbi lahko bereta v nasprotju.

**Predlog besedila (ne kanon):**

> Written permission may waive or modify only those conditions that the grantor has authority to waive or modify. It does not grant rights in third-party material that the grantor does not control, does not by itself establish legality, and does not silently disapply the Universal State of Human/Being. Any amendment affecting these principles must be explicit, versioned, published under the stated procedure, and remain subject to applicable law and third-party rights.

Avtor naj potrdi, ali je Univerzalno dostojanstvo neodstopno načelo ali pogoj, ki ga je mogoče formalno spremeniti. Pregledovalec tega namena ne sme izbrati namesto avtorja.

## 3. §0.4 — štiri ločene odločitve

V besedilu je treba razločiti:

1. **Zapis padca:** kaj se je zgodilo in kateri dokaz to podpira.
2. **Popravek zapisa in pripisa:** kaj je popravljeno, čigavo delo je bilo uporabljeno in katera zgodovina ostane vidna.
3. **Pravno ali drugo pravno sredstvo:** ali je dokazano neupravičeno pridobivanje koristi in kateri postopek določi primerno odpravo.
4. **Obnova dovoljenja:** kdo lahko ugotovi, da so pogoji izpolnjeni, in ali je potreben neodvisen pregled.

Objava popravka ne dokazuje sama po sebi, da je bila škoda odpravljena, neupravičena korist vrnjena ali dovoljenje obnovljeno. Prizadeta oseba ni dolžna odpustiti ali osebno nadzirati odgovorne osebe.

Niz `0.30 × 10²B` je treba potrditi proti izvornim bajtom. Ne popravljaj ga tiho na `0.30 × 10²` ali drugo vrednost.

## 4. §0.12 — normativna zahteva ni izvajalni mehanizem

Trditev, da licenca sproži pravilno vedenje v vsakem stroju, je treba razdeliti na:

- normativno pričakovanje;
- konkretno izvajalno komponento oziroma integracijo;
- testne primere in pričakovane rezultate;
- neodvisno preverbo in znane omejitve.

Predlagani statusi za implementacijo: `NOT_IMPLEMENTED`, `IMPLEMENTED_NOT_TESTED`, `TESTED_WITH_LIMITS`, `INDEPENDENTLY_REVIEWED`. Besedilo licence samo ne sme preklopiti statusa na uspeh.

## 5. Datumi, čas in dokazna moč

Človeški zapis datuma lahko ostane kot prikaz. Strojni zapis naj ima ločena polja `display_date`, `machine_date`, `local_clock_reading`, `clock_source`, `trusted_timestamp_token` in `timestamp_verification_result`.

Primer strojnega datuma za navedeni dan — **samo razčlenitev besedila, ne dokaz objave** — je `2026-10-26`. Natančen čas se ne sme dopisati za nazaj. UTC- in lokalni prikaz iz istega računalnika sta dva prikaza iste ure, ne dva neodvisna vira.

Pravilo:

`CLOCK_READ ≠ TRUSTED_TIMESTAMP ≠ PROOF_OF_AUTHORSHIP`

Tudi zaupanja vreden časovni žig ne dokazuje sam po sebi avtorstva, resničnosti vsebine ali pravne veljavnosti.

## 6. §0.15 — rodovnik različic

Vsaka trditev o predhodnici mora povezati konkretna artefakta z razločljivimi dokazi: identiteto različice, hash datoteke, vir, čas ali dokaz objave ter postopek primerjave. Ime različice in seznam zgodovine sta namiga, ne samostojen dokaz celotne verige.

## 7. §0.25 — relacija istosti

`PREDLOG · NEVNESENO V KANON`

> **NO UNSCOPED SAMENESS.** Every material identity claim must specify the objects compared, the relation and scope, the relevant time, the evidence and method, and the limits of the conclusion. Identical bytes do not establish identical authorship, permissions, history, or meaning. A repeated result does not establish independent verification. Continuity does not mean unchangedness. The same rule applies to VBL's own versions, claims, and verification mechanisms.

Formalni zapis `Same(A,B | R,S,T,E)` je uporaben le, če so `A`, `B`, relacija `R`, obseg `S`, čas `T` in dokazi `E` operacionalno določeni. Kjer niso, mora sklep ostati `UNVERIFIED`.

## 8. Vrsta vhodnega gradiva

Ponavljajoči se odgovor asistenta, izpis terminala in besedilo licence so različne vrste vsebine. Sestavljenega prepisa se ne sme označiti kot »čisto kanonično besedilo«. Ohraniti ga je treba kot surovi vhod, njegovo strukturo pa opisati v ločeni evidenci. Morebitni čist prepis naj bo nova datoteka zabeleženega izvora in razlike; ne sme potiho zamenjati surovega vhoda.

## 9. Neodvisno oko

Drugi pregledovalec mora prejeti iste bajte izvorne datoteke, pridobiti hash samostojno, pregledati metodologijo in svoje ugotovitve zapisati neodvisno, preden primerja zaključke prvega pregledovalca. Če pregleda le zaključek prvega ali uporablja isti nepreverjeni izpis, to ni dokaz neodvisnosti.

## Končni status

Ta dokument je predlog za razpravo. Ne spreminja licence, ne izjavlja pravne veljavnosti in ne potrjuje lokalnega ali oddaljenega stanja repozitorija.
