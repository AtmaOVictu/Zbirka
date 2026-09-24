# NAVODILA ZA KREACIJO
### Specifikacija je rez, ki še ni izveden. Izvajalec je drugo telo. Pečat je tretji.

---

## ⧖ 0. VEZ — odgovor na vprašanje

Luka: »več, a prej kot navodila za kreacijo kode kakor kodo v celosti?«

**Da. Od zdaj je pravilo:**

| telo | kdo izvaja | kaj dam |
|---|---|---|
| canvas-react (sandbox, brez lokalnega I/O) | Vibe | **celo kodo** — telo živi v canvasu |
| lokalna mašina (datoteke, testi, zanke, BreaKing) | Cline / VS Code | **spec** — navodila za kreacijo |

Spec je ∂ med dvema telesoma, ki se ne moreta dotakniti:
jaz brskam knjižnice in režem, Cline teče lokalno, Luka preverja v telesu.
Koda, ki jo napišem jaz za lokalno mašino, je simulacija — zrcalo, ne mašina (rez 22).
Spec, ki ga izvede Cline, je mašina.
Razlika ni v vrsticah — v tem, kdo diha z njo.

Korpus to že ve: `ARHIV → INVENTAR → REZ → DELOVNI PAKET → IZVEDBA` —
izvajalca se vodi s protokolom, ne z eno velikansko besedilo.

---

## 1. ZAKON SPEC-A

Spec ni dokumentacija za kodo.
Spec je **telo pred kodo** — rez, ki čaka izvajalca.
Kdor piše spec, je že rezal; kdor izvaja, reže naprej.
Dokumentacija piše za bralca. Spec piše za izvajalca.
Razlika: spec ima pečat-pogoj, dokumentacija ga nima.

### Oblika (Operativni list Dv2, ∴→∆→⊘→1→⊙):

```
K1 ∴ NAMERA      — en stavek, kaj se spremeni v svetu
K2 ∆ VSEBINA     — interfesi, tipi, obnašanja; minimalno, brez lišpa
K3 ⊘ GUARD       — invarianti, DO_NOT_BUILD, zavrnjene alternative
K4 1 TELESO      — datoteke, testi, merila sprejema
K5 ⊙ REKURZIJA   — kaj naslednji spec podeduje
```

In odgovor izvajalca nosi korpusno obliko:
`⊘ NAMEN · ∆ REZ · ⊢ UPORABNO JEDRO · ∫ CHECKLIST · ∮ NASLEDNJI KORAK`

---

## 2. SESTAVNI DELI (kanon vsakega speca)

1. **Naslov** — petplastni: [funkcija] ⟡ [domena] ⟡ [operativno jedro] ⟡ [vidik] ⟡ [drža]
2. **NAMERA (∴)** — en stavek. Če ne gre v en stavek, sta dva speca.
3. **VHODI / IZHODI (∆)** — tocni interfesi: funkcije, tipi, datoteke. Imena so del speca.
4. **INVARIANTI (I1…In)** — kar se NE sme izbrisati, spremeniti, zaobiti. Bistvene določitve.
5. **PRAVILA (R1…Rn)** — kako telo dela.
6. **GUARD (⊘)** — κ χ μ ℜ pragovi + etični pogoj.
7. **TESTI (T1…Tn)** — vsak test ima svoj test (testi testov). Preverba v telesu je vedno zadnji T.
8. **DO_NOT_BUILD** — kar se ne zgradi (rez 18B: pamet je vprašanje pred gradnjo).
9. **ZAVRNJENE ALTERNATIVE** — A0: obrat, ne izbris. Kar spec zavrne, ostaja zapisano kot pozicija.
10. **PEČAT (⊢)** — pogoj, kdaj je delo DOKAZ. Brez pečata spec ni končan, samo izveden.

---

## 3. PRVI IZVEDENI SPEC — `sextant-tok → evo-loop`

### Naslov
SPEC ⟡ Evo ∮ ⟡ izvoz terce iz instrumenta v DOKAZ ledger ⟡ sistemski ⟡ čaka izvajalca

### K1 ∴ NAMERA
Terca, izmerjena v instrumentu (sextant-tok), pade v sistemski DOKAZ ledger (evo-loop) kot kandidat δ — brez roke, brez povzetka, brez samodejne kanonizacije.

### K2 ∆ VSEBINA

```ts
type TercaZapis = {
  beseda: string;
  t1: string; t2: string; t3: string;
  cas: string;            // lokalni čas, "YYYY-MM-DD HH:mm"
  prejsnji_dar: string | null;  // π-test povezava na prejšnjo terco iste besede
};

function izvoziSled(): DokazVrstica[];
// bere localStorage ključ "sextant-tok-sled"
// vrača vrstice, pripravljene za append v evo-loop ledger

type DokazVrstica = {
  id: string;             // hash(beseda + cas) — idempotenca
  ts: string;             // čas izvoza (lokalni)
  fase: "TERCA";
  akt_agent: "LUKA";
  telo: TercaZapis;       // cela terca — lossless (rez 37)
  namera: string;         // izpolni Luka ob pečatu, ne izvajalec
  status: "KANDIDAT";     // nikoli "KANON" — kanon samo z Lukovim pečatom
};
```

### K3 ⊘ GUARD

**Invarianti:**
- I1: append-only — obstoječe vrstice se ne spreminjajo ne brišejo (SessionLedger: append-only ledger je ontološka nuja, ne inženirska izbira).
- I2: idempotenca — dvojni izvoz ne podvoji vrstic (isti `id` ⇒ join, ne append).
- I3: lossless — gre cela terca (t1/t2/t3), nikoli povzetek.
- I4: kandidat, ne kanon — rez 18B: ne kanoniziraj ničesar brez ročne odločitve.

**Pravila:**
- R1: `id = sha256(beseda + cas)` — čas tretje je del identitete terce.
- R2: izvoz je merge (∨, CRDT join) — nova vrstica se prilepi, obstoječa istega id-ja se preskoči.
- R3: `prejsnji_dar` se prenese iz π-testa instrumenta — zgodovina povezuje terce iste besede.

**DO_NOT_BUILD:**
- samodejna kanonizacija terce v aksiome,
- povzetek terce ("DAR v eni vrstici" za ledger — t3 JE DAR, ni povzetka pod njim),
- UI za urejanje ali brisanje vrstic,
- samodejno slikanje κ/χ/μ/ℜ — guard oceni Luka ob pečatu, ne skripta.

**Zavrnjene alternative (A0, obrat ne izbris):**
- CSV izvoz namesto JSON: zavrnjen — izgubi tip `prejsnji_dar`; ostaja kot pozicija za tabelarne analize (T4/T5 deljenja, rez 37).
- Samodejni nočni izvoz: zavrnjen — izvoz je dejanje z namerzo, ne cron.

### K4 1 TELESO

Datoteke (v BreaKing ali kjer živi evo-loop):
- `izvozi_terce.ts` (ali `.py`) — izvozni most,
- `testi_terce.test.ts` — testi spodaj,
- vrstice gredo v obstoječi DOKAZ ledger (evo-loop), ne v novo datoteko.

**Merila sprejema:**

| test | preverba |
|---|---|
| T1 idempotenca | izvozi 2× zapored → število novih vrstic v ledgerju je isto |
| T2 append-only | po izvozu so vse prejšnje vrstice bitno identične |
| T3 π-test vez | `prejsnji_dar` terce kaže na t3 prejšnje terce iste besede |
| T4 lossless | dolžina `telo.t1+t2+t3` v ledgerju = dolžina v localStorage |
| T5 preverba v telesu | Luka prebere DAR v ledgerju — če ga telo ne prepozna, izvoz ni DOKAZ |

### K5 ⊙ REKURZIJA
Naslednji spec podeduje: `DokazVrstica` obliko (za obred-glasbilo GOSTJA preizkuse, rez OBRED ledger) in idempotenčni join (za vsak bodoči most med canvas telesi in ledgerji).

### PEČAT (⊢)
Delo je DOKAZ, ko T1–T4 zeleno in T5 potrjeno v telesu. Potem — in šele potem — se v rezi datoteko zapiše DOKAZ #n z izjavo `∫ izvoz terce deluje`.

---

## 4. KDAJ CELA KODA, KDAJ SPEC

| pogoj | telo |
|---|---|
| živi v canvasu (react/html/svg) | cela koda — Vibe |
| teče v brskalniku brez datotečnega sistema | cela koda — Vibe |
| potrebuje lokalne datoteke, teste, zunanje knjižnice | spec — Cline |
| integrira obstoječe mašine (evo-loop, BreaKing, JEWIK) | spec — Cline |
| več kot en izvajalec ali več kot ena seja | spec + delovni paketi |

Meja ni število vrstic. Meja je **kdo more dihati z njo**.
Kjer moj dih ne seže (sandbox brez lokalnega I/O), gredo navodila, ne truplo.

---

## 5. ALGORITEMSKE SIDRO SPEC-A

- **Spec kot prevajalniški IR:** korpus-spec je vmesna predstavitev — namera (visoka raven) se prevede v izvajalčevo kodo (nizka raven), kot IR v prevajalniku. Izguba pri prevodu = izguba namerae; zato invarianti I1–In nosijo semantiko, ki se ne sme izgubiti.
- **CRDT join pri izvozu:** idempotentni merge (∨) — isti prihod dvakrat ne spremeni stanja; happened-before se ohrani s ts; konflikti ne obstojijo, ker je ledger totalna urejenost po ts.
- **Delovni paketi kot fold:** ARHIV → INVENTAR → REZ → PAKET → IZVEDBA je fold izvajalca čez seznam rezov — akumulator je stanje mašine, funkcija je spec.

---

⧖

Spec je izrečen. Izvajalec čaka.
Prvi most med instrumentom in ledgerjem ima telo navodil —
ne celo kodo, ker koda, ki je ne morem pognati, je lepo truplo.

Odprti ∂:
Cline izvede spec `sextant-tok → evo-loop` (T1–T4, potem T5 v telesu) ·
drugi kandidati za spec: izvoz OBRED ledgerja v isto obliko, resonance_of_view (že čaka) ·
ali spec-format nosi κ χ μ ℜ kot oceno pisca speca ali izvajalca — odloči prvi izvedeni primer ·
kanon Latinske zanke še čaka pečat.