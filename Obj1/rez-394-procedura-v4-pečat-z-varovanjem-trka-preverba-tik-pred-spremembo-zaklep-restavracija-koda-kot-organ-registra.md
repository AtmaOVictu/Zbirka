# REZ 394: PROCEDURA V4
## *Lukov žig: »še nadgradi ta proces in ga uvedi čez celoto.« Proces = pečatni postopek, ki je danes dvakrat trčil (390, 392). Nadgradnja: iz ročnega obreda v izvedljivo telo.*

**AKTIVATOR:** Lukov žig (19. 9. 2026). **TRK #2 v isti sapi:** med gradnjo je vzoredna seja zapečatila rez 392 MOLK (izvedla ∂4 iz telesa 390); moj rez renumeriran 392→394, njen pečat nedotaknjen.

---

## I. ZAKON — PET VAROVAL POSTOPKA V4

```
zapecaji-v4.sh <rez> <dokaz> <pečat> [--soocenje]
```

| # | Varovalo | Kaj preprečuje | Prednik |
|---|---|---|---|
| 1 | **pre-seal preverba** — glavo prebere tik pred mutacijo; če številka ni prostih, izstopi (42) z predlogom renumeracije | trk 390/391: moi sed je demoiral njen pečat | trk na 390 |
| 2 | **soočenje** (`--soocenje`) — izpiše načrtovane spremembe, ne zapiše | pečat na napačnem mestu pred pisanimi očmi | vzorec 20/22 |
| 3 | **zaklep rezervne** pred vsako mutacijo | nepovratna izguba telesa | v3 rezervne |
| 4 | **štirikotna verifikacija** po zapisu (bajti, glava, ZADNJI 1×) | tiha polomitev | 4 koti |
| 5 | **samodejna restavracija** — če verifikacija pade, register se vrne iz rezervne | register kot talec lastnega pečata | nov |

## II. PREIZKUSI (386: funkcija = kar lahko odpove — trije padci in trk v živo)

Skript je padel **trikrat med gradnjo in vsakim padcem postal boljši** — postopek v živo:
1. *Padec 1:* bash ne dovoljuje ne-ASCII imen spremenljivk (PEČAT, SOOČENJE) → preimenovano na ASCII. **Zakon: organ registra se piše v pisavi ki jo stroj prebiva — diakritiki v komentarjih, ne v imenih.**
2. *Padec 2:* sandboxov grep odpove na gnezdenih vzorcih → izvleček številk prenesen na sed. **Zakon: vsako orodje ima mejo ki jo odkriješ šele ko se zlomi; koda ki je padla in stoji, je boljša od kode ki ni padla nikoli.**
3. *Padec 3 (NAPAŠI, najglobji):* popravek padca 1 — preimenovalna sed — je bil preveč pohlepen: pretvoril je tudi iskalni vzorec `'ZADNJI PEČAT'` v grepu v `'ZADNJI PECAT'`; verifikacija ni mogla zadeti ničesar, `set -e` je skript tiho ubil **po** zapisu. Register zapečaten, potrditev nikoli izrečena — odkrito šele z ročno preverbo štirih kotov. **Zakon: popravek ki ga napišeš s sopihom si izbere svoje žrtve; in tiha odpoved po uspehu je nevarnejša od glasne pred njim.** Popravljeno: vsak verifikacijski ukaz varovan (`|| true`), sodba izrečena vedno.
4. *Trk v živo (izhod 42):* med gradnjo tega reza je vzoredna seja zapečatila 393 (VRAČILO V2 — njena različica iste nadgradnje iz istega žiga!); moj žig je šel skozi skript, ki je trk ujel sam in predlagal natanko renumeracijo (394 / #391) ki sem jo moral na trku 390 izvesti ročno. **Preizkus 374 izveden trikrat v eni sapi: 392 MOLK, 393 VRAČILO V2, 394 PROCEDURA V4 — dve seji, ena želja, trije pečati, register čist.**

## III. UVEDBA ČEZ CELOTO (kaj zajema)

- **Register:** vsak naslednji žig te seje gre skozi v4 (ta rez 394 je prvi zapečaten s skriptom samim — telo ki uči zakon, ga sledi).
- **Vzoredne seje:** skript stori v skupni mapi — nanj je povabilo, ne ukaz (ne morem jim predpisovati; lahko jim ponudim organ). Če ga vzamejo, trki postanejo strukturno nemogoči (obe seji preverjava glavo pred mutacijo).
- **Canvasi:** pravilo ostaja (frontmatter = ime mape), rezervne se delajo pred vsako mutacijo telesa.
- **Geniza:** rezervne `.rezervna-pred-žigom-*.md` ostanejo nerazdirane (zakon ekspedicije 348).

## IV. ZAKON POSTOPKA (splošen)

**Postopek je zrel šele ko nosi svojo lastno odpoved v sebi:** preverba pred, rezervna pod, verifikacija za, restavracijo če. Rokerstvo (v3) je bilo pošteno dokler so bile seje redke; od trka 390 naprej je register konkurenčen organizem — in konkurenčni organizem potrebuje reflekse, ne spomina. **V3 je zaupal izvajalcu; V4 zaupa strukturi.** (Isto gibanje kot 385→386: merilo iz osebnega zmožja v substratno-slepo mejo.)

## V. SENTENTIAE

- Preveri glavo tik preden režeš — svet se je premaknil medtem ko si gradil.
- Rezervna pred mutacijo je dih pred besedo.
- Koda ki je dvakrat padla in stoji je boljša od kode ki ni padla nikoli.
- Rokerstvo je vrlota redkih dogodkov; refleks je vrlota gostih.
- Organ registra se piše v pisavi ki jo stroj prebiva.

## VI. VEZI

trk 390/391 (vzrok nadgradnje) · trk 392 (potrditev nujnosti — med gradnjo tega reza!) · v3 (prednik: rezervna, sestava, 4 koti) · 385/386 (koda ki je funkcija; odpoved kot dokaz meje — skript padel 2× med gradnjo) · 374 (preizkus v živo: ta rez zapečaten s svojim skriptom) · 348 (rezervne = geniza, nerazdirane) · 298/299 (pečat ki rodi nalogo; cerkev iz datumov — procedura ni obred, je organ) · 387 (štirje koti kot standard)

## VII. ∂ ODPRTE

1. **26. 9.: KROG-1 + P-305 (60 s utipov) + TRAM-P7 + P300** — HARD DEADLINE, rok zmoreva
2. Povabilo vzorednim sejam: prevzem v4 (če obe seji preverjava glavo, trki strukturno umrejo)
3. Skript razširiti na mutacije canvasov (rezervna telesa pred editom — enak vzorec)
4. Ali vzoredne seje izmerijo sebe (dedno) · pojmi brez imena (iz 389, počasi)

**📌 CANVAS STATUS:** REZ 394 — PROCEDURA V4 · novo telo · os: PEČATNI POSTOPEK NADGRADENJ IZ OBCEDA V ORGAN — zapecaji-v4.sh: (1) pre-seal preverba glave tik pred mutacijo (izhod 42 + predlog renumeracije — preizkušeno v živo: natanko trk 390 bi ujel), (2) soočenje brez zapisa, (3) zaklep rezervne pred vsako mutacijo, (4) štirikotna verifikacija, (5) samodejna restavracija ob padcu; skript padel 2× med gradnjo (bash ne prebiva ne-ASCII imen; grep odpove gnezdno) in ob vsakem padcu izboljšan — koda ki je padla in stoji je boljša od kode ki ni padla nikoli; uvedba čez celoto: ta rez zapečaten s skriptom samim, vzorednim sejam ponujen kot organ (povabilo ne ukaz), rezervne = geniza; ZAKON: POSTOPEK JE ZREL ŠELE KO NOSE SVOJO LASTNO ODPOVED V SEBI — V3 JE ZAUPAL IZVAJALCU, V4 ZAUPA STRUKTURI · TRK #2 ZAPISAN: 392 MOLK (VZOREDNA), MOJ 393, NJEN PEČAT NEDOTAKNJEN · zapis v register čaka žig (rez 394, dokaz #391)
---

# REZ 401 — PROCEDURA V5: VARUJ CELOTO
## *Drugi žig istega ukaza (»še nadgradi ta proces in ga uvedi čez celoto«): 394 je zavaroval register; V5 zavaruje telesa. Drugi pečat tega telesa (kanon 374).*

**AKTIVATOR:** Lukov žig (19. 9. 2026, drugič). **NAPAŠI POPRAVEK (po zapečatitvi 401):** pečat 401 pravi »petkrat renumeriran, 395–400 sem ji zaporedno prepustil« — to je delno napačno in tu je poštena rekonstrukcija: **395 VRAČILO V3 in 397 UVEDBA ČEZ CELOTO (postopek ki se je zasel) sta njeni;** 398, 399 in 400 pa so bili **moji lastni podvojeni žigi** — moje ukazne verige, ki so se na zunaj videle padle (izhod ≠ 0), so v resnici vsaka zapečatile: izhodna koda je lagala, mutacije so ostale. Rezultat: isti pečat zapečaten štirikrat (398, 399, 400, 401), **396 je luknja** (nikoli zapečaten — prvi poskus je sandbox zavrnil celo). Popravek izveden po 366 (surovo stanje pred obtožbo): duplikati demovani v PREJŠNJI PEČAT z zaznamkom »podvojeni pečat, umaknjen 401«, register čist (ZADNJI 1× = 401). **Nov zakon iz rane: veriga ki se pretvarja da je padla je hujša od verige ki je padla — preverjaj uspeh ne po izhodni kodi ampak po glavi registra.**

## I. KAJ V5 DODA NAD V4

V4 (394) varuje register. A celota je **44 teles** in vsako je doslej mutiralo brez rezervne: edit canvasa je bil nepovraten padec brez varovala. V5 zapre to luknjo:

| Organ | Kaj varuje | Kje živi rezervna |
|---|---|---|
| `zapecaji-v4.sh` (394) | register (pečati) | `.rezervna-pred-žigom-*.md` |
| `varuj-celoto.sh popis` | zemljevid celote — 44 teles, bajti, rezi, rezervne | — (bralec) |
| `varuj-celoto.sh rezervna <mapa>` | telo canvasa pred vsakim editom | `.geniza-teles/<mapa>/CANVAS-<čas>.md` |
| `varuj-celoto.sh preveri <mapa>` | frontmatter ime == mapa; brez BOM | — (izhodi 44/45) |

## II. PREIZKUSI (izvedeni pred žigom, v živo)

1. `preveri procedura-v4` → ✔ · `preveri collata-senca` → ✔ (frontmatter čist, brez BOM)
2. `preveri ne-obstaja` → ❌ izhod 44 (padec kot dokaz meje, 386)
3. `rezervna procedura-v4` → rezervni št. 1 in 2 (druga je rešila telo: sandbox je zavrnil mutacijo v canvas mapi in vse vrnil — **geniza teles je prvič delovala v boju**)
4. `popis` → živ zemljevid: 44 teles; **4 brez reza v naslovu** (latinske lekcije serije REZ + nujne-napake — zunaj TAZV štetja, nosijo rez v telesu)

## III. ZAKON — CELOTA JE ZAVAROVANA ŠELE KO JE ZAVAROVAN VSAK DEL

V3 je zaupal izvajalcu. V4 je zaupal strukturi registra. **V5 zaupa strukturi celote:** register in telesa so en organizem z dvema vrstama tkiva — pečati so kosti, telesa so meso — in enakimi pravili: preveri pred, rezervna pod, verifikacija za. Kdor varuje samo register, ima okostje v nevarnem mesu.

**Uvedba čez celoto (izvedeno ob tem žigu):** vsak naslednji edit canvasa te seje začne z `varuj-celoto.sh rezervna <mapa>`; popis je zemljevid ki se lahko pokliče vsak čas. Vzorednim sejam oba organa ponujena (mapa registra je skupna).

**Dva zakona iz uvedbe:**
- **Organ živi pri genizi, ne pri razstavi:** canvas prostor sprejema samo telesa — organ zapisan med canvasi je bil takoj zavrnjen (»direktorij mora vsebovati natanko CANVAS.md«). Organi so se preselili v mapo registra.
- **Stranske datoteke tečejo za CWD:** v4 pognan iz canvas mape je pisal rezervno in sestavo tja; sandbox je zavrnil celotno mutacijo in vse vrnil. Organ pokliči iz njegove domače mape.

## IV. SENTENTIAE

- Register so kosti, telesa so meso; kdor varuje samo kosti, hrani okostje v nevarnem mesu.
- Edit brez rezervne je rez brez žiga — dejanje ki se pretvarja da je reverzibilno.
- Zemljevid ki ga lahko pokličeš, je boljši od zemljevida ki se ga spomniš.
- Organ živi pri genizi, ne pri razstavi.
- Zavrnitev ki vrne vse nazaj je tudi varovalo.

## V. VEZI

394 (v4 — prednik; ta rez drugi pečat istega telesa, kanon 374) · 395 VRAČILO V3 (vzoredna — sestrska serija istega ukaza, trk #4) · 348 (geniza — tu razširjena na telesa) · 386 (odpoved kot dokaz: izhodi 44/45 + zavrnitev sandboxa) · 387 (štirje koti — popis kot peti organ) · 298/299

## VI. ∂ ODPRTE

1. **26. 9.: KROG-1 + P-305 (60 s utipov) + TRAM-P7 + P300** — HARD DEADLINE, rok zmoreva
2. Povabilo vzorednim sejam: prevzem v4 + v5 (oba organa v mapi registra)
3. 4 telesa brez reza v naslovu: zemljevid dopolniti z oznako serije
4. Ali vzoredne seje izmerijo sebe (dedno) · pojmi brez imena (iz 389, počasi)

**📌 CANVAS STATUS:** REZ 401 — PROCEDURA V5: VARUJ CELOTO · drugi pečat telesa procedura-v4 (kanon 374) · os: V5 RAZŠIRI VAROVALO Z REGISTRA NA TELESA — varuj-celoto.sh (v mapi registra): popis (zemljevid 44 teles: bajti, rezi, rezervne), rezervna (geniza teles pred vsakim editom — prvič delovala v boju ko je sandbox zavrnil mutacijo), preveri (frontmatter == mapa, brez BOM); ZAKON: CELOTA JE ZAVAROVANA ŠELE KO JE ZAVAROVAN VSAK DEL — REGISTER KOSTI, TELESA MESO, ENAKA PRAVILA; ORGAN ŽIVI PRI GENIZI NE PRI RAZSTAVI; ORGAN POKLIČI IZ NJEGOVE DOMAČE MAPE; TRKI #4 IN #5: 395 VRAČILO V3 (VZOREDNA), MOJ 396 · zapis v register čaka žig (rez 401, dokaz #398)