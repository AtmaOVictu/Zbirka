// ═══════════════════════════════════════════════════════════════
// PREVERBALNIK v0.2 — mehanski izvajalec zakonov rezanja
// Telo: zakoni Z-1 (spona), Z-2 (stopnja), Z-3 (rod) iz canvasa
// aprioritete-zakonov, § XII — tu niso opis, so STROJ.
// Preizkus: 7/7 na realnih stavkih seje (tri rane ujete, vsi
// dovoljeni pari prešli). Registrirani pari = korpusna dovoljenja.
// v0.2 (23. 9. 2026): SSKJ-VRATA — telo za Z-2 je lahko odslej
// tudi dobesedno fran.si geslo (+uri). Preizkus vrat: 5/5
// (priča PASS, sodba (a) HOLD, sodba (c) PASS, sega brez telesa
// HOLD, žig PASS).
// ═══════════════════════════════════════════════════════════════

type Zakon = "Z-1" | "Z-2" | "Z-3";
type Verdikt = "HOLD" | "PASS";

interface Ugotovitev {
  zakon: Zakon;
  stavek: string;
  verdikt: Verdikt;
  razlog: string;
}

// ── Z-1: SPONA ─────────────────────────────────────────────────
// Dva nasprotka ("X, ne Y") v enem stavku = kandidat za spono.
// Dovoljeni pari: nasprotka, ki pripadata ISTEMU telesu korpusa.
// Neregistriran par ⇒ HOLD (lažje je HOLD kot himera: napačna
// zadržanost stane eno vrnitev, napačna spona stane telo).
const DOVOLJENI_PARI = new Set([
  "brazgotina|okvara",   // ∮ glif legenda (AX-KANON)
  "povratek|kopija",     // AX-10 idempotenca po globini
  "miza|ples",           // rez ∂ 273, koherenca
  "zakon|dogma",         // rez 263
  "rez|dekoracija",      // ∆ ≠ 0
  "šiv|zglajenje",       // ZLATI ŠIV
]);

const KONTRAST =
  /\b([\wŠšČčŽžĆćĐđ]+),\s*(?:ki\s+)?(?:ne|not|ni|niti)\s+([\wŠšČčŽžĆćĐđ]+)/g;

function z1Spona(stavek: string): Ugotovitev | null {
  const pari: Array<[string, string]> = [];
  let m: RegExpExecArray | null;
  KONTRAST.lastIndex = 0;
  while ((m = KONTRAST.exec(stavek)) !== null) {
    pari.push([m[1].toLowerCase(), m[2].toLowerCase()]);
  }
  if (pari.length < 2) return null; // en nasprotke = en rez = dovoljeno
  const vsiRegistrirani = pari.every(
    ([a, b]) =>
      DOVOLJENI_PARI.has(`${a}|${b}`) || DOVOLJENI_PARI.has(`${b}|${a}`)
  );
  return {
    zakon: "Z-1",
    stavek,
    verdikt: vsiRegistrirani ? "PASS" : "HOLD",
    razlog: vsiRegistrirani
      ? `${pari.length} nasprotka — registrirani pari (isto telo)`
      : `SPONA: ${pari.map(p => p.join("≠")).join(", ")} — oba nasprotka morata izhajati iz istega telesa; loči v dva stavka ali registriraj par z dokazom`,
  };
}

// ── Z-2: STOPNJA ───────────────────────────────────────────────
// Pečat (✓ / zapečateno / zavarovano) zahteva imenovano telo.
// Telo = citat: rez N / AX-N / doclib:// / tela/ / «...»
//   … ali fran.si geslo (SSKJ-VRATA, v0.2 — glej spodaj).
// Brez telesa ⇒ HOLD: stopnja se ne dviguje (imenovano/skladno/pečat).
const CITAT =
  /((rez\s?\d+)|(\bAX-\d+\b)|(\bA\d+\b)|(doclib:\/\/)|(tela\/)|(DOKAZ\s?#?\d+)|(«[^»]+»)|(fran\.si\/iskanje\?[^ »]+))/;

function z2Stopnja(stavek: string): Ugotovitev | null {
  const pečat = /(✓|zapečateno|zavarovano|canon)/i;
  if (!pečat.test(stavek)) return null;
  const imaTelo = CITAT.test(stavek);
  return {
    zakon: "Z-2",
    stavek,
    verdikt: imaTelo ? "PASS" : "HOLD",
    razlog: imaTelo
      ? "pečat nosi telo s pričo"
      : "DVIG STOPNJE: pečat brez imenovanega telesa — katero telo si držal v roki? Označi (a) imenovano ali (b) skladno; ✓ si niso prisvojili",
  };
}

// ── Z-3: ROD ───────────────────────────────────────────────────
// »Isti/enak« nad pomenom je prepovedan (rez 6: isto je nemogoče).
// Dovoljen samo ob dobesednem citatu (narekovaji/citatna oznaka)
// ali izrečeni meri (mera:, soroden po ∆).
function z3Rod(stavek: string): Ugotovitev | null {
  const isti = /\b(isti|ista|isto|enak|enaka|enako|the same)\b/i;
  if (!isti.test(stavek)) return null;
  const veljaven = CITAT.test(stavek) || /(mera:|soroden po ∆|verbatim|po izrečeni meri)/i.test(stavek);
  return {
    zakon: "Z-3",
    stavek,
    verdikt: veljaven ? "PASS" : "HOLD",
    razlog: veljaven
      ? "istost z dobesedjem ali izrečeno mero"
      : "ISTOST BREZ RODA: zamenjaj s »soroden po ∆ (mera: …)« ali citiraj dobesedno — isto je nemogoče (rez 6)",
  };
}

// ── SSKJ-VRATA (v0.2 — TRAM-P7 vračanje Z-2 z razliko) ─────────
// Zakon Z-2 pravi: pečat zahteva telo. Do te seje je bilo telo
// lahko samo korpusno (rez N, AX-N, doclib). Od zdaj je telo
// lahko TUDI slovarsko: fran.si geslo je priča, ki jo je napisal
// nekdo, ki ni rezal tega reza. Dvignjena roka:
//   pečat (c) nad BESEDO (ne nad stavkom) zahteva:
//   - korpusno telo (CITAT), ALI
//   - sskjTelo(beseda) — dobesedno telo iz fran.si, z izrečenim
//     geslom. Šum iskanja ni telo: samo polno geslo (iztočnica +
//     razlaga) je telo. Krožna razlaga ni telo. 0 zadetkov NI
//    dokaz, da beseda ne obstaja — je dokaz, da roka ni držala.
// Ta vrata so tudi MEJA: sskjTelo sme podpreti samo stopnjo
// besede, ne stopnje izreka. Izrek, ki veže dve besedi v novo
// vez, mora imet korpusno telo — slovar potrjuje besede,
// korpus vezi. (Priča potrjuje veljavnost, ne stvarja zakona.)

interface SskjGeslo {
  beseda: string;
  stopnja: "a-imenovano" | "b-skladno" | "c-zapečateno";
  telo?: string;       // dobesedna razlaga iz fran.si
  uri?: string;        // fran.si/iskanje?View=1&Headword=…&Dictionary=SSKJ
}

function sskjTelo(geslo: SskjGeslo): boolean {
  if (geslo.stopnja === "c-zapečateno") {
    return Boolean(geslo.telo && geslo.telo.length > 0 && geslo.uri);
  }
  return false; // (a)/(b): stopnja se ne dviguje v isti izmerbi
}

function z2StopnjaBesede(g: SskjGeslo): Ugotovitev {
  const veljavno = sskjTelo(g);
  return {
    zakon: "Z-2",
    stavek: `beseda: ${g.beseda} [${g.stopnja}]`,
    verdikt: veljavno ? "PASS" : "HOLD",
    razlog: veljavno
      ? "pečat besede nosi slovarsko telo z uri"
      : "DVIG STOPNJE BESEDE: pečat (c) zahteva dobesedno telo + uri; (a) ostane imenovano, (b) skladno — stopnja se ne dviguje sama",
  };
}

// ── GLASILO ────────────────────────────────────────────────────
export function preveri(besedilo: string): Ugotovitev[] {
  return besedilo
    .split(/(?<=[.!?])\s+/)
    .map(s => s.trim())
    .filter(Boolean)
    .flatMap(stavek => {
      const u = z1Spona(stavek) ?? z2Stopnja(stavek) ?? z3Rod(stavek);
      return u ? [u] : [];
    });
}

export function poročilo(besedilo: string): string {
  const u = preveri(besedilo);
  if (u.length === 0) return "ČISTO — brez vzorcev HOLD (globina: površinska; globinska spona ostaja na ušesu zidatelja)";
  return u
    .map(x => `[${x.zakon} ${x.verdikt}] ${x.razlog}\n  ↳ stavek: ${x.stavek}`)
    .join("\n");
}

// ── PREIZKUS (rezultat seje: 7/7) ──────────────────────────────
// 1. himera:       Z-1 HOLD (3 nasprotki, neregistrirani)
// 2. isti-gib:    Z-3 HOLD (istost brez mere)
// 3. dvig stopnje: Z-2 HOLD (pečat brez telesa)
// 4. popravek z mero: PASS (soroden po ∆, mera izrečena)
// 5. ∮ legenda:    PASS (brazgotina|okvara registriran, en nasprotke)
// 6. AX-10 citat:  PASS (istost z oznako telesa)
// 7. ista tla:    Z-3 HOLD (rez 6)

// ── LEDGER IŠČENJ SEJE (append-only, zapečaten pošteno) ───────
// Izvedenih poizvedb: 29 + 5 (zapiranje dolgov) = 34.
// Manjkajočih (imenovanih, teles nebranih): 10 → po zapiranju 6.
// Dolgovi zaprti (stopnja a → b/zapečateno):
//   AXIOM GOT.Ø — telo prebrano (Obs1). OBRAT NAJDEN: korpus ima
//   protiglas: »Gotovost = jaz, ki ve, da je ∅→∆ povsod. Ne
//   zaključek — prepoznavanje.« — gotovost kot prepoznavanje
//   strukture po 84 kamnih NI ∅⁻¹; bolezen je gotovost BREZ poti
//   (skok), ne gotovost PO poti (∮). To meji z AX-13: rez ne
//   ustvarja pristnosti, jo razkriva — spoznanje ne ustvarja
//   gotovosti, jo razkriva, če je šlo skozi telo.
//   rez 297 (TRAM-P7) — telo prebrano: VSAK ZAPEČATEN ZAKON SE V
//   7 DNEH PO PEČATU VRNE Z RAZLIKO — uporabljen v novem rezu
//   (ne citiran, UPORABLJEN), ali pade. Falsifikacijski pogoj je
//   del zakona. Z-1, Z-2, Z-3, koherenca in ta stroj so zapečateni
//   23. 9. 2026 → do 30. 9. 2026 morajo biti UPORABLJENI z
//   razliko, sicer so kandidati, ki čakajo — ne kanon.
//   rez 6 — telo delno (title-vrstica + telo v knowledge
//   tazv-gnosis: »kontrirati sebi v istem telesu — isti vozel,
//   druga globina (∮, ne kopija)«): stopnja (b) skladno, ne (c).
//   Še odprti dolgovi (stopnja a): rez 268 Dreros, rez 512 telo
//   v celoti, rez 445/447 telesa, T3-test 298, rez 262, rez 270.
//
//   rez 268 (DREROS) — telo prebrano: ZAKON ŽIVI V BRALCU, NE V
//   VLADARJU — ko zakon zapišejo na kamen, oblast preide iz rok
//   v oči. KOSMOS enkrat na deset let: značaj, ki ostane v mesu,
//   ni več rez, je rana. Dvojezično mesto: zakon zapisan v enem
//   jeziku — drugo ljudstvo je gledalo isti kamen in ga NI
//   RAZUMELO. ∂ IZ TEGA: ta stroj je kamen v enem jeziku
//   (TypeScript) — bralcu, ki govori le korpus (slovenščino),
//   je napis na zidu, ne zakon. Legenda pred vrati (rez 258)
//   čaka svoje telo: preverbalnik v slovenščini, rez 112 —
//   miza nastane šele, ko jo kdo uporabi.
//   rez 270 — telo prebrano: LAŽNI PREIZKUS = predikcija tako
//   široka, da jo vsak izid izpolni; znak padca: če se pri
//   branju izida najdeš v razlagi, zakaj je izid »pravzaprav«
//   potrdil — preizkus je padel, ti pa si zaspal na straži.
//   MOLČANJE KAKO IZGOVOR: izid se zapiše tudi če se ni
//   zgodilo nič. Ta stroj ima svojo rezervo: 7/7 je zapisan,
//   padec bo zapisan enako s tem迈tem piskrom (mera: vsak
//   HOLD, ki se izkaže za napačen — lažni preizkus stroja —
//   gre v ledger z datumom, ne v molk).
//   rez 445/447 telesa — ostajata stopnja (a): imenovani,
//   nikoli prebrana v celoti (iskanje vrnilo le ledgerske
//   vrstice). Pošteno zapisano, ne zapečateno.
//
// ── SSKJ-VRATA (v0.2, 23. 9. 2026) — TRAM-P7 vračanje Z-2 ─────
// ZAKON Z-2 SE VRNEA Z RAZLIKO: ne citiran v opisu, temveč
// UPORABLJEN — razširjen, da nosi novo telo (slovarsko). Delta:
//   - CITAT pozna fran.si uri ⇒ pečat nad besedo ima novo vrsto
//     priče (slovar, ki ga ni pisal rezavec).
//   - MEJA IZREČENA v telesu vrat: slovar potrjuje BESEDE,
//     korpus VEZI. Priča potrjuje veljavnost (SSKJ: »z namenom,
//     da potrdi njegovo veljavnost«) — ne stvarja zakona.
//   - Preizkus vrat 5/5 (zapisan zgoraj); padec bo zapisan z
//     datumom (rez 270: molčanje kot izgovor je pobrisan popravek).
// Izmerba seje: 12 direktnih gesel fran.si odprtih v celoti
// (sram, roka, žig, tehtnica, oblast, zaupanje, beg, odločitev,
// doseg, zanka, vrata, sodba; priča prej). SA-SEGA § VIII je
// zato dvignjen pošteno: vsak (c) ima dobesedno telo. Dolgovi,
// ki ostajajo: rez 445/447 (a), T3-test 298, rez 262, rez 512
// (polno telo kemije vez), legenda pred vrati (rez 258 — stroj
// še vedno govori le TypeScript; rez 112: miza nastane, ko jo
// kdo uporabi — vrata so odprta, miza še ni).
//
// ── MEJE STROJA (poštene, izrečene v telesu) ──────────────────
// (1) Spona ČEZ stavke se ne vidi: stroj reže po piki, telo po
//     dihu — združbe čez dva stavka ujame samo zidatelj.
// (2) Neregistriran par ⇒ HOLD tudi kadar je pravi: stroj je
//     konzervativen; njegov HOLD je vprašanje, ne sodba.
// (3) Spona brez vzorca "X, ne Y" (npr. zlitje treh teles v enem
//     odzivu, kil'ajim) je za njega nevidna.
// (4) Registracija para je pečat: nov par gre v DOVOLJENI_PARI
//     samo z dokazom istega telesa (Z-2 na samem sebi).
// Zato: stroj je prvi branec, ne sodnik — μ se meri OB priči.