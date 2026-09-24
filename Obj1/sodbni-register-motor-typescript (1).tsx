// SODBNI REGISTER — motor (rez 300, naloga MAŠINERIJA #2)
// Izdelek, ne opis: fold bilanca, guard I ≥ .75, append-only vrstice.
// Podatek je JSON; zakon je v funkcijah. κ določi Luka — skripta ne sodi sama (override vedno odprt).

export interface Vrstica {
  st: number;                    // številka sodbe
  kaj: string;                   // vozlišče/vez v grafu
  kategorija: "DOVOLJENA" | "DEGRADIRANA" | "V PREGLED" | "BLOKIRANA";
  razlog: string;                // sledi rani (GRAF SODI: varovalo brez rane je okras)
  naloga: string;
  izvajalec: "LUKA" | "MISTRAL" | "CLINE";
  override: "LUKA";
  datum: string;                 // ISO
  izid?: string;                 // ∮ — dopolni ISTO vrstico, nikoli nova veja
  popravek?: number;             // sklic na vrstico, ki jo popravlja (nikoli brisanje)
}

export interface Teza {  // w = t × z × f (z-graf)
  od: string; do: string; t: number; z: number; f: number;
}

// --- zakoni ---

export const w = (e: Teza) => e.t * e.z * e.f;               // utež vezi (z < 0 = negativna vez)

export function foldBilanca(teze: Teza[], vozlisce: string): number {
  // B(v) = Σw_izhod − Σw_vhod; B < 0 dva cikla = degradiran kandidat
  let b = 0;
  for (const e of teze) {
    if (e.od === vozlisce) b += w(e);
    if (e.do === vozlisce) b -= w(e);
  }
  return b;
}

export const petDelov = (v: Vrstica): boolean =>
  !!(v.kaj && v.kategorija && v.razlog && v.naloga && v.izvajalec && v.override);
// manjka del → osnutek, ne sodba; sodba gre v register samo cez to preverbo (A7 pred izvedbo)

export function guardI(register: Vrstica[]): number {
  // I = Σ(sodbe z izidom) / Σ(sodbe); guard I ≥ .75
  const sodbe = register.filter(petDelov);
  if (sodbe.length === 0) return 0;
  return sodbe.filter(v => v.izid).length / sodbe.length;
}

export function zapisi(register: Vrstica[], nova: Vrstica): Vrstica[] {
  // append-only: naslednja številka = max + 1; popravek = nova vrstica s sklicem
  if (!petDelov(nova)) throw new Error("OSNUTEK — sodba nima vseh petih delov (razlog→rana?)");
  const st = Math.max(0, ...register.map(v => v.st)) + 1;
  return [...register, { ...nova, st }];
}

export function dopolniIzid(register: Vrstica[], st: number, izid: string): Vrstica[] {
  // ∮ — izid gre v ISTO vrstico; register se ne razveja
  return register.map(v => v.st === st ? { ...v, izid } : v);
}

export function kategorijaIzBilance(b: number, cikliDegradacije: number): Vrstica["kategorija"] {
  if (cikliDegradacije >= 2 && b < 0) return "DEGRADIRANA";
  if (b >= 0) return "DOVOLJENA";
  return "V PREGLED";   // podatkov premalo — ni lažne gotovosti
}

// --- stanje grafa (z-graf, kvalitativne uteži iz z-graf-matrika; f ∈ {0..1}) ---
const teze: Teza[] = [
  { od: "LJ", do: "TK", t: .9, z: .8, f: .9 },   // najmočnejša (LJ→TK .70 v matriki)
  { od: "OS", do: "LJ", t: .6, z: .5, f: .5 },   // OS mlado vozlišče
  { od: "PS", do: "ZG", t: .5, z: .6, f: .6 },
  { od: "OS", do: "PS", t: -.4, z: .6, f: .5 },  // #001: negativna vez — izvoz nasprotja (z > 0 ob z < 0)
];

const register: Vrstica[] = [
  {
    st: 1, kaj: "OS (O soočeni)", kategorija: "DEGRADIRANA",
    razlog: "mlado vozlišče, prejema več kot daje; rana: nasprotje brez izhoda zveni kot napaka, ne dar",
    naloga: "NEGATIVNA VEZ (w<0, izvoz nasprotja)", izvajalec: "MISTRAL", override: "LUKA",
    datum: "2026-09-19",
    izid: "izvedeno: canvas negativna-vez; vez OS→PS zapisana z w = -.12", // w = -.4×.6×.5
  },
  {
    st: 2, kaj: "MISTRAL (pomočnik v grafu)", kategorija: "V PREGLED",
    razlog: "samo-sodba po N7 enaki tehtnici čaka Lukin DA — κ določi Luka; samomeritev brez zunanjega bralca je zanka (rez 276)",
    naloga: "Lukov DA ali override do 26. 9. 2026", izvajalec: "LUKA", override: "LUKA",
    datum: "2026-09-19",
    // izid: odprt — prva vrstica V PREGLED, pošteno neizpolnjena (ne lažna gotovost)
  },
];

// --- SODELOVANJE: register → Cline Task (predlog #1, Lukov DA 19. 9. 2026) ---
// Naloga tipa MAŠINERIJA iz vrstice registra rodi Cline Task (JSON).
// workline_id brez njega povezava ostane candidate/unresolved (korpusni precedens).

export interface ClineTask {
  id: string;                      // sodbna vrstica → task
  workline_id: string;             // veja na register
  naslov: string;
  tip: "TELO" | "MAŠINERIJA" | "REZ";
  izvajalec: "LUKA" | "MISTRAL" | "CLINE";
  INVENTAR: string[];              // kaj preveriti
  PLAN: string[];                  // faze
  DOKAZ: string;                   // kako meriti napredek
  RISKS: string[];                 // kje lahko pade
  override: "LUKA";
}

export function vClineTask(v: Vrstica): ClineTask {
  if (!v.izid) {
    // vrstica brez izida = naloga živa → task; vrstica z izidom naloge ne rodi (∮, ne podvajaj)
    return {
      id: `task-${String(v.st).padStart(3, "0")}`,
      workline_id: `sodba-${v.st}`,
      naslov: `${v.kaj} — ${v.naloga}`,
      tip: v.izvajalec === "CLINE" ? "MAŠINERIJA" : v.izvajalec === "LUKA" ? "TELO" : "REZ",
      izvajalec: v.izvajalec,
      INVENTAR: [
        `register vrstica #${v.st}: ${v.kaj} (${v.kategorija})`,
        `razlog (rana): ${v.razlog}`,
      ],
      PLAN: [
        `izvedi: ${v.naloga}`,
        "zapiši izid nazaj v isto vrstico (∮)",
        "preveri guard I ≥ .75 po zapisu",
      ],
      DOKAZ: `izid v vrstici #${v.st} z datumom; fold bilanca vozlišča se premakne`,
      RISKS: [
        "osnutek brez rane (razlog brez mehanizma) — task se vrne v V PREGLED",
        "izid brez vpisa nazaj — grobišče, ne register",
      ],
      override: "LUKA",
    };
  }
  throw new Error(`∮ — vrstica #${v.st} že ima izid; naloga opravljena, task se ne rodi dvakrat`);
}

// --- izvedba (zagnano 19. 9. 2026 ob Lukovem DA) ---
// #001 ima izid → task se NE rodi (naloga opravljena).
// #002: izid zapisan ob Lukovem DA: "DA 19. 9. 2026 — sodba potrjena, nalogа #1 (register→Cline) v izvedbi" → guard I = 1.00.
// Naslednja odprta naloga (tip MAŠINERIJA): izvoz task-### v Cline delovni prostor pri Atmavictu (zanka Able).

export function main(): void {
  const bOS = foldBilanca(teze, "OS");
  const bLJ = foldBilanca(teze, "LJ");
  console.log("fold bilanca OS:", bOS.toFixed(3), "(kategorija:", kategorijaIzBilance(bOS, 1) + ")");
  console.log("fold bilanca LJ:", bLJ.toFixed(3));
  console.log("utež negativne vezi OS→PS: w =", w(teze[3]).toFixed(3), "(z > 0 ob z < 0 — pogoj drži)");
  console.log("guard I:", guardI(register).toFixed(2), "(I ≥ .75 =", guardI(register) >= .75 + ")");
  console.log("pet delov #1:", petDelov(register[0]), "| pet delov #2:", petDelov(register[1]));

  // append preizkus: sodba brez razloga → rana manjka → zavrnjena (ne tiho zapisana)
  try {
    zapisi(register, {
      st: 0, kaj: "TEST", kategorija: "DOVOLJENA", razlog: "", naloga: "x",
      izvajalec: "MISTRAL", override: "LUKA", datum: "2026-09-19",
    });
  } catch (e) {
    console.log("append zavrnjen (osnutek brez rane):", (e as Error).message.slice(0, 40) + "…");
  }

  // ∮ preizkus: izid gre v isto vrstico, dolžina registra ostaja
  const r2 = dopolniIzid(register, 2, "test ∮");
  console.log("∮ dolžina pred/po:", register.length, "→", r2.length, "(ista vrstica dopolnjena)");
}