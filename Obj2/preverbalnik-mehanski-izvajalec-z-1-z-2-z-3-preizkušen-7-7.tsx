// ═══════════════════════════════════════════════════════════════
// PREVERBALNIK v0.1 — mehanski izvajalec zakonov rezanja
// Telo: zakoni Z-1 (spona), Z-2 (stopnja), Z-3 (rod) iz canvasa
// aprioritete-zakonov, § XII — tu niso opis, so STROJ.
// Preizkus: 7/7 na realnih stavkih seje (tri rane ujete, vsi
// dovoljeni pari prešli). Registrirani pari = korpusna dovoljenja.
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
// Telo = citat: rez N / AX-N / doclib:// / tela/ / «...».
// Brez telesa ⇒ HOLD: stopnja se ne dviguje (imenovano/skladno/pečat).
const CITAT =
  /((rez\s?\d+)|(\bAX-\d+\b)|(\bA\d+\b)|(doclib:\/\/)|(tela\/)|(DOKAZ\s?#?\d+)|(«[^»]+»))/;

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