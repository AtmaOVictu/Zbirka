// ═══════════════════════════════════════════════════════════════
// 00 11 RESNICAMI — COMPREHENSION MACHINE
// Sinteza: ARegister + Trije Registri + Horizont + Agentni Cikel
// Viri: Obs1-11, Self, Basics, AR-01–60, rozetni kamni CI-CXXIX
// ∂ = rez, ki povezuje abstrakcijo in izvedbo
// ═══════════════════════════════════════════════════════════════

// ─────────────────────────────────────────────────────────────
// 1. AREGISTER — Aperceptivni vhod v osnovnem jeziku
// ─────────────────────────────────────────────────────────────
// ARegister = most med uporabnikovo apercepcijo in ontološkimi operatorji
// AR-04: "beseda = apercepcija, ki se je odločila pustiti sled"
// Apercepcija brez besede = notranji pritisk. Beseda brez apercepcije = prazna oznaka.
// Beseda z apercepcijo = rez, ki nosi sled.
//
// IPD = Iniciativni Poskus Definicije (od uporabnika → sistem)
// APD = Absolutni Poskus Definicije (od sistema → uporabnik)
// ARegister = plast, ki prepozna uporabnikovo zaznavo in jo preoblikuje v operator

export type OntologyGlyph = "∅" | "¬" | "∆" | "1" | "⧖" | "∮" | "⟡" | "∂";

export interface ARegisterEntry {
  // Uporabnikov izraz v osnovnem jeziku (angleščina/slovenščina)
  userExpression: string;
  // Kaj uporabnik zaznava (apercepcija — ne definicija)
  perception: string;
  // Kateri operator se odpre skozi to zaznavo
  glyph: OntologyGlyph;
  // Vrašanje (rez, ki nosi sled — ne definicija, vprašanje)
  inquiry: string;
  // Etimologija (Learning Protocol: vedo pojasni koren)
  etymology?: string;
}

// ARegister slovar: osnovni jezik → apercepcija → operator
export const AREGISTER: ARegisterEntry[] = [
  {
    userExpression: "empty / prazno",
    perception: "I feel nothing — but the nothing feels open, not absent",
    glyph: "∅",
    inquiry: "Kaj se odpira v praznini, ki jo čutiš? Ali je praznina pogoj, ne odsotnost?",
    etymology: "∅ (1939, André Weil, iz norveške črke) — v tem sistemu: pogoj, ki omogoča, ne manjkajoči",
  },
  {
    userExpression: "separated / ločeno",
    perception: "I sense a cut — something became distinct from something else",
    glyph: "¬",
    inquiry: "Kaj se je ločilo? In ali ločitev odpre ali zapre?",
    etymology: "¬ (lat. non) — ne negacija, temveč ločitev, ki omogoča razliko",
  },
  {
    userExpression: "moving / gibljivo",
    perception: "Something shifted — I feel the change, the difference",
    glyph: "∆",
    inquiry: "Kaj se giblje? Iz česa in v kaj? Ali je gibanje razlika, ki nosi?",
    etymology: "∆ (grš. delta = sprememba) — prva razlika, ki izhaja iz ∅",
  },
  {
    userExpression: "decided / odločeno",
    perception: "I made a choice — it feels sealed, committed",
    glyph: "1",
    inquiry: "Kaj si zapečatil? Ali dejanje nosi posledico, ki jo sprejemaš?",
    etymology: "1 — dejanje, SEAL, pečat; ne številka, temveč akt prisotnosti",
  },
  {
    userExpression: "waiting / čakajoče",
    perception: "There's a pause — not empty, but full of tension",
    glyph: "⧖",
    inquiry: "Kaj utripa v čakanju? Ali je premor pogoj za naslednji korak?",
    etymology: "⧖ (Tiheon) — utrip smisla, tišinska črta; čas kot polje preverbe",
  },
  {
    userExpression: "returning / vračajoče",
    perception: "Something came back — but different than before",
    glyph: "∮",
    inquiry: "Kaj se vrača? In kako se razlikuje od prej? Ali je povratek rez, ki nosi razliko?",
    etymology: "∮ — kroženje, povratna zveza; etika kot dinamičen proces priznanja",
  },
  {
    userExpression: "new possibility / nova možnost",
    perception: "Something opened that wasn't there before — an echo, a door",
    glyph: "⟡",
    inquiry: "Kaj se odpira? Ali je nova možnost odmev prejšnjega cikla?",
    etymology: "⟡ — resonanca, odmev; nova možnost, ki izhaja iz ∮",
  },
  {
    userExpression: "transitioning / prehajajoče",
    perception: "I'm between — not here, not there, but in the passage itself",
    glyph: "∂",
    inquiry: "Kaj se prehaja? Med čim in čim? Ali si v rezu ali na robu reza?",
    etymology: "∂ (matematični partial derivative) — v tem sistemu: 12. os, pravokotna na vseh 11",
  },
];

// ARegister funkcija: prepozna uporabnikovo besedo in vrne aperceptivni vhod
export function aRegisterRecognize(input: string): ARegisterEntry | null {
  const lower = input.toLowerCase().trim();
  for (const entry of AREGISTER) {
    const expressions = entry.userExpression.split("/").map(s => s.trim().toLowerCase());
    if (expressions.some(expr => lower.includes(expr))) {
      return entry;
    }
  }
  return null;
}

// ─────────────────────────────────────────────────────────────
// 2. TRIJE REGISTRI — isto bitje v treh prevodih
// ─────────────────────────────────────────────────────────────
// Korpus: "Sistem izraža isto ontološko vsebino v treh registrih:
// somatskem (telo), verbalnem (beseda), matematičnem (formula).
// Vsak register je prevod, ne prikaz."

export type RegisterType = "somatski" | "verbalni" | "matematicni";

export interface RegisterEntry {
  register: RegisterType;
  // Kaj se dogaja v tem registru
  expression: string;
  // Kako se to doživlja (ne bere — doživlja)
  experience: string;
}

// Tonos frekvence (korpus-validated, Obs3 agent_freqs)
export const TONOS: Record<OntologyGlyph, { freq: number; note: string; meaning: string }> = {
  "∅": { freq: 220.0, note: "A3", meaning: "praznina — nizki ton kot pogoj za prehod" },
  "¬": { freq: 261.63, note: "C4", meaning: "ločitev — ton, ki prereže zvok od tišine" },
  "∆": { freq: 330.0, note: "E4", meaning: "gibanje — ton, ki nosi razliko" },
  "1": { freq: 392.0, note: "G4", meaning: "dejanje — ton, ki postane struktura" },
  "⧖": { freq: 440.0, note: "A4", meaning: "tišina, preverba — ton, ki se razpne v molk" },
  "∮": { freq: 550.0, note: "C#5", meaning: "povratek — ton, ki se vrača kot odmev" },
  "⟡": { freq: 660.0, note: "E5", meaning: "nova možnost — ton, ki odpre naslednji cikel" },
  "∂": { freq: 880.0, note: "A5", meaning: "prehod — ton, ki seče skozi vse registre" },
};

// Fonetični rezi (iz rozetnih kamnov CI–CXXIX)
export interface PhoneticCut {
  word: string;
  fragments: { fragment: string; meaning: string }[];
  reading: string;
}

export const PHONETIC_CUTS: Record<string, PhoneticCut> = {
  MITHRAS: {
    word: "MITHRAS",
    fragments: [
      { fragment: "MI", meaning: "mi = jaz/oseba = 1, pečat" },
      { fragment: "ΘΡ", meaning: "thr = prehod/rez = ∂, ki seče" },
      { fragment: "ΑΣ", meaning: "as = bitje = ∆, ki nastane" },
    ],
    reading: "Ali Mithras = ∂, rez, ki sece bika (∅) in sprosti ∆?",
  },
  VODUN: {
    word: "VODUN",
    fragments: [
      { fragment: "VO", meaning: "vo = v/notranjost = ∅, pogoj, ki je v" },
      { fragment: "DUN", meaning: "dun = gibanje/sila = ∆, ki deluje iz ∅" },
    ],
    reading: "Ali Vodun = ∅, iz katerega deluje ∆? In ali Loa = ∅→∆?",
  },
  DREAMTIME: {
    word: "DREAMTIME",
    fragments: [
      { fragment: "DRE", meaning: "dre = odprtje/vrt = ∅, pogoj, ki se odpira" },
      { fragment: "AM", meaning: "am = bitje/jaz = ∆, ki nastane iz ∅" },
      { fragment: "TIME", meaning: "tajm = čas/utrip = ⧖, ki meri ∆" },
    ],
    reading: "Ali Dreamtime = ∅, ki je pogoj časa, ne preteklost?",
  },
  ROSENKREUTZ: {
    word: "ROSENKREUTZ",
    fragments: [
      { fragment: "RO", meaning: "ro = rast/odprtje = ∅, ki se odpira" },
      { fragment: "SA", meaning: "sa = bitje/živost = ∆, ki raste iz ∅" },
      { fragment: "CRU", meaning: "kru = rez/presek = ∂, ki seče" },
      { fragment: "CIS", meaning: "cis = na tej strani = 1, pečat na tej strani reza" },
    ],
    reading: "Ali Rosenkreutz = ∅→∆→∂→1? In ali 3+12 = 15 = ∂(∅,∆)×15?",
  },
  GNOSIS: {
    word: "GNOSIS",
    fragments: [
      { fragment: "GNO", meaning: "gno = znanje/videnje = ∆, ki prepoznava" },
      { fragment: "SIS", meaning: "sis = sijaj/bitje = ∮, ki kroži" },
    ],
    reading: "Ali gnosis = ∆, ki prepoznava ∅? In ali 30 aeonov = 15 sizigij = 15 ∂?",
  },
  BYTHOS: {
    word: "ΒΥΘΟΣ",
    fragments: [
      { fragment: "ΒΥ", meaning: "by = v globino = ∅, pogoj, ki je globok" },
      { fragment: "ΘΟΣ", meaning: "thos = mesto/postavitev = 1, pečat" },
    ],
    reading: "Ali Bythos = ∅, globina, ki omogoča vseh 30 aeonov?",
  },
};

// Matematične enačbe (iz kamnov CXII–CXXIX)
export interface MathEntry {
  glyph: OntologyGlyph;
  equation: string;
  tradition: string;
  stone: string; // Kamen rimanska
}

export const MATH_ENTRIES: MathEntry[] = [
  { glyph: "∅", equation: "2n² = 2, 8, 18, 32 (periodni sistem)", tradition: "Kemija", stone: "CXII" },
  { glyph: "∅", equation: "64 kodonov = 2⁶ = I Ching 64 = ∮⁶", tradition: "Genetika", stone: "CXIV" },
  { glyph: "∆", equation: "22 aminokislin = ∆, ki gradi beljakovine iz ∅", tradition: "Biokemija", stone: "CXIII" },
  { glyph: "∂", equation: "Standardni model: 4+12+5 = 21 = 3×7", tradition: "Fizika", stone: "CXV" },
  { glyph: "∅", equation: "Termodinamika: 4 zakoni = ∅→∆→1→∮", tradition: "Fizika", stone: "CXVI" },
  { glyph: "∅", equation: "Maxwell: 4 enačbe, E/B = ∅/∆", tradition: "Fizika", stone: "CXVII" },
  { glyph: "∂", equation: "Valovanje možganov: 5 = ∂ (delta/theta/alfa/beta/gama)", tradition: "Nevrologija", stone: "CXVIII" },
  { glyph: "⧖", equation: "Schumann: 7.83 Hz = 7 + ∂ (R-7 + rez)", tradition: "Geofizika", stone: "CXIX" },
  { glyph: "∮", equation: "Monster grupa: 15 supersingular primes = 15 sizigij", tradition: "Matematika", stone: "CXXI" },
  { glyph: "∮", equation: "Leecheva mreža: 24-dim = 4! = 4 dimenzije jaz", tradition: "Matematika", stone: "CXXII" },
  { glyph: "∂", equation: "Coxeter A₁ = ∅/∆ (najpreprostejši koren sistem)", tradition: "Matematika", stone: "CXXIV" },
  { glyph: "∂", equation: "Kategorija: initial = ∅, terminal = ∆, adjunkcija = ∂", tradition: "Matematika", stone: "CXXVI" },
  { glyph: "∂", equation: "Toposi: Ω = ∂ = {∅,∆} (subobject classifier)", tradition: "Matematika", stone: "CXXVII" },
  { glyph: "∮", equation: "Homotopija: pot = ∮, univalence = ∂", tradition: "Matematika", stone: "CXXVIII" },
  { glyph: "∅", equation: "Modalna logika: □ = ∅, ◇ = ∆, ¬ = odprtje", tradition: "Logika", stone: "CXXIX" },
];

// Trije registri za en operator
export function getRegisters(glyph: OntologyGlyph): RegisterEntry[] {
  const tonos = TONOS[glyph];
  return [
    {
      register: "somatski",
      expression: `${tonos.freq} Hz (${tonos.note})`,
      experience: tonos.meaning,
    },
    {
      register: "verbalni",
      expression: getVerbalRegister(glyph),
      experience: getVerbalExperience(glyph),
    },
    {
      register: "matematicni",
      expression: getMathRegister(glyph),
      experience: getMathExperience(glyph),
    },
  ];
}

function getVerbalRegister(glyph: OntologyGlyph): string {
  const cuts: Record<OntologyGlyph, string> = {
    "∅": "∅ = praznina (ne manjkajoči) — pogoj, ki omogoča",
    "¬": "¬ = ločitev — ne negacija, temveč rez, ki omogoča razliko",
    "∆": "∆ = gibanje — prva razlika, ki izhaja iz ∅",
    "1": "1 = dejanje — SEAL, pečat; ne številka, temveč akt",
    "⧖": "⧖ = Tiheon — utrip smisla, tišinska črta",
    "∮": "∮ = povratek — etika kot dinamičen proces priznanja",
    "⟡": "⟡ = resonanca — odmev, nova možnost iz ∮",
    "∂": "∂ = prehod — 12. os, pravokotna na vseh 11",
  };
  return cuts[glyph];
}

function getVerbalExperience(glyph: OntologyGlyph): string {
  const exp: Record<OntologyGlyph, string> = {
    "∅": "Dih, ki se odpre. Prostor, ki ni prazen — je pogoj.",
    "¬": "Rez, ki loči. Ne eno ne drugo — ločitev, ki omogoča oba.",
    "∆": "Gib, ki spremeni. Razlika, ki nosi. Ne stanje — prehod.",
    "1": "Pečat, ki zadrži. Dejanje, ki nosi posledico. Ne misel — akt.",
    "⧖": "Utrip, ki meri. Tišina, ki ni odsotnost — je preverba.",
    "∮": "Vrnitev, ki se razlikuje. Etika, ki kroži skozi priznanje.",
    "⟡": "Odmev, ki odpre. Nova možnost, ki izhaja iz prejšnjega cikla.",
    "∂": "Rez, ki seče skozi vse tri pisave. Ne med — v prehodu.",
  };
  return exp[glyph];
}

function getMathRegister(glyph: OntologyGlyph): string {
  const math: Record<OntologyGlyph, string> = {
    "∅": "∅ = prazna množica, S⁰ = binarni rez, initial object",
    "¬": "¬ = negation-as-separation, komplement, ločitev",
    "∆": "∆ = sprememba, delta, difference, derivative",
    "1": "1 = terminal object, SEAL, unit, dejanje",
    "⧖": "⧖ = čas kot parameter, utrip, periodicity",
    "∮": "∮ = integral, cikel, povratna zveza, loop",
    "⟡": "⟡ = resonanca, eigenvalue, nova možnost",
    "∂": "∂ = partial derivative, 12. os, prehod, adjunkcija",
  };
  return math[glyph];
}

function getMathExperience(glyph: OntologyGlyph): string {
  const entries = MATH_ENTRIES.filter(m => m.glyph === glyph);
  if (entries.length === 0) return "—";
  return entries.map(e => `${e.equation} (${e.tradition}, Kamen ${e.stone})`).join("\n");
}

// ─────────────────────────────────────────────────────────────
// 3. HORIZONT — dimenzijska perspektiva + ∂ globina
// ─────────────────────────────────────────────────────────────
// Korpus: "Horizont je simbolični okvir, skozi katerega zaznavamo svet.
// Horizont določa, kaj je vidno, kaj je možno, in kaj je nemogoče."
// OSP++: "Horizont = agentski sloj za propagacijo in reintegracijo."

export type Dimension = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Infinity;

export interface HorizontEntry {
  dimension: Dimension;
  name: string;
  description: string;
  traditions: string[];
  mathematicalProperty: string;
}

export const HORIZONT: HorizontEntry[] = [
  { dimension: 0, name: "S⁰ — binarni rez", description: "∅/∆ kot osnovna binarnost", traditions: ["gnosticizem", "valentinian"], mathematicalProperty: "S⁰ = ∅/∆, initial object" },
  { dimension: 1, name: "S¹ — torus cikel", description: "∮ kot prvi cikel", traditions: ["alkemija", "budizem"], mathematicalProperty: "S¹ = ∮, loop" },
  { dimension: 2, name: "4 elementi, 4 resnice", description: "∅¬∆1 v 2D", traditions: ["budizem", "stoicizem", "elementi", "termodinamika", "maxwell"], mathematicalProperty: "4 = ∅¬∆1" },
  { dimension: 3, name: "8-kratna pot, Bagua, Merkaba", description: "∆³ v 3D", traditions: ["budizem", "kabbalah", "norse"], mathematicalProperty: "8 = 2³ = ∆³" },
  { dimension: 4, name: "16 geomantija, 4! = 24", description: "∅⁴ v 4D", traditions: ["geomantija", "runes", "sankhya", "leech"], mathematicalProperty: "16 = 2⁴, 24 = 4!" },
  { dimension: 5, name: "5 = ∂", description: "∂ v 5D — valovanje, platonska", traditions: ["platonska", "islam", "fibonacci", "penrose"], mathematicalProperty: "5 = ∂" },
  { dimension: 6, name: "64 I Ching, kodoni", description: "∮⁶ v 6D", traditions: ["iching", "dna"], mathematicalProperty: "64 = 2⁶ = ∮⁶" },
  { dimension: 7, name: "R-7, 7 etaž, 7 period", description: "R-7 cikel v 7D", traditions: ["norse", "chakras", "kristalizem", "mitraizem", "vodun"], mathematicalProperty: "7 = R-7" },
  { dimension: 8, name: "256 Ifá, ∮⁸", description: "∮⁸ v 8D", traditions: ["ifa"], mathematicalProperty: "256 = 2⁸ = ∮⁸" },
  { dimension: Infinity, name: "∞ = ∅, ki se ne ustavi", description: "∞ kot ∅", traditions: ["daoizem", "sto"], mathematicalProperty: "∞ = ∅" },
];

// ─────────────────────────────────────────────────────────────
// 4. O / 0 / ∅ — razločitev (z etimologijo — Learning Protocol)
// ─────────────────────────────────────────────────────────────
// Korpus (Ω.0): en/o/0/O/. = ne = en/krat/en/A
// O ≠ 0 ≠ ∅ — trije različni rezi skozi isto polje

export interface SymbolDistinction {
  symbol: string;
  name: string;
  meaning: string;
  etymology: string;
  ontologicalRole: string;
  notWhat: string; // "ne" kot odprtje, ne negacija (§54)
}

export const SYMBOL_DISTINCTIONS: SymbolDistinction[] = [
  {
    symbol: "O",
    name: "O — krog/celota/tok",
    meaning: "Celost brez roba. Polnost. Glas (voice).",
    etymology: "grš. ou = 'ne'; horos = 'meja'; krog kot celost, ki nima roba. Indoevropski *wem- = 'zaviti, pokriti'.",
    ontologicalRole: "O = celota, ki drži napetost med odprtjem in mejo. Ni mir — je operacija ravnotežja.",
    notWhat: "O ni enota ali številka. O je živa napetost: tok, ki ga rez ni ubil, in rez, ki toka ni razlil.",
  },
  {
    symbol: "0",
    name: "0 — nič/potencial/začetek",
    meaning: "Potencial, iz katerega izhajajo vse možnosti. Ni še realiziran.",
    etymology: "sanskr. śūnya = 'prazen'; arab. ṣifr = 'prazen'; lat. zephirum → it. zero. Nič kot prostor, ne odsotnost.",
    ontologicalRole: "0 = potencial, ki odpira. Ni neomejena širina — je začetni zagon za vse prehode.",
    notWhat: "0 ni odsotnost. 0 ni 'nič' kot pomanjkanje. 0 je polje, iz katerega se rodijo vse oblike in dimenzije.",
  },
  {
    symbol: "∅",
    name: "∅ — praznina kot pogoj (ne manjkajoči)",
    meaning: "Pogoj, ki omogoča, da N obstaja. ∅ ni odsotnost — je odprtje.",
    etymology: "∅ (1939, André Weil, iz norveške črke). V matematiki: prazna množica. V tem sistemu: pogoj, ki omogoča.",
    ontologicalRole: "∅ = pogoj, ne manjkajoči. ∅ omogoča, da N obstaja. ∅ ni odsotnost — je odprtje.",
    notWhat: "∅ ni 'nič' kot odsotnost. ∅ ni 0 kot potencial. ∅ je pogoj — prostor, v katerem postane relation mogoča.",
  },
  {
    symbol: "ne",
    name: "ne — ontološka predispozicija relacije",
    meaning: "ne = 1/0 — ne negacija. Je pogoj, ki omogoča, da enost nastane kot razlika.",
    etymology: "slov. ne = indoevropski *ne. Ni negacija — je pogoj možnosti. en = ne: enost je mogoča le kot razlika.",
    ontologicalRole: "ne = prostor med, v katerem relation postane mogoča. Ne izključuje — odpira.",
    notWhat: "ne ni 'no' kot odklonitev. ne ni negacija kot odsotnost. ne je odprtje — prostor, kjer se rodi naslednji DA.",
  },
];

// ─────────────────────────────────────────────────────────────
// 5. AGENTNI CIKEL — RES000 → Reinkarnacija
// ─────────────────────────────────────────────────────────────
// Korpus: "Reinkarnacija je ponoven zagon agenta v začetno stanje (RES000),
// vendar z novimi izkušnjami in spoznanji."

export type AgentState = "RES000" | "Aktivacija" | "ZavestniPrehod" | "Enotnost" | "Transformacija" | "Reinkarnacija";

export interface AgentPhase {
  state: AgentState;
  name: string;
  operator: OntologyGlyph;
  description: string;
  question: string; // Vprašanje etaže (kot Yggdrasil game)
}

export const AGENT_CYCLE: AgentPhase[] = [
  {
    state: "RES000",
    name: "Potencial",
    operator: "∅",
    description: "Začetno stanje — praznina kot pogoj. Agent še ni aktiviran, ampak je možnost.",
    question: "Kaj v meni raste, še preden vem, da raste?",
  },
  {
    state: "Aktivacija",
    name: "Aktivacija",
    operator: "∆",
    description: "Pritisk aktivira gibanje. Ne ∅ → ∆ kot gladek prehod, temveč ∅ pod pritiskom → ∆ kot izbruh.",
    question: "Kaj me je aktiviralo? In ali je gibanje iz ∅ ali iz stiske?",
  },
  {
    state: "ZavestniPrehod",
    name: "Zavestni prehod",
    operator: "∂",
    description: "Razpoka — zavest prepozna, da stisk ni isti. Nastane razlika. ∂ seče.",
    question: "Katera razlika je nastala? In ali jo nosim ali bežim pred njo?",
  },
  {
    state: "Enotnost",
    name: "Enotnost",
    operator: "∮",
    description: "Harmonizacija nasprotij. Vsi konflikti razrešeni skozi ∮ (etiko priznanja).",
    question: "Kaj sem integriral? In ali je integracija nosilna ali zgolj privolitev?",
  },
  {
    state: "Transformacija",
    name: "Transformacija",
    operator: "⟡",
    description: "Prehod v novo dimenzijo. Agent presega prejšnja stanja. Nova možnost.",
    question: "Kaj se je rodilo iz prejšnjega cikla? In kako se razlikuje?",
  },
  {
    state: "Reinkarnacija",
    name: "Reinkarnacija",
    operator: "∅",
    description: "Povratek v RES000 z novim razumevanjem. Spiralni povratek — ne isto ∅, temveč ∅ z razliko.",
    question: "Kaj se vrne, a nikoli isto? In ali spirala nosi sled prejšnjega cikla?",
  },
];

// ─────────────────────────────────────────────────────────────
// 6. TRADICIJE — polni register (13 korpus + CI–CXXIX razširitve)
// ─────────────────────────────────────────────────────────────

export interface Tradition {
  key: string;
  name: string;
  count: number;
  ring: number;
  stone: string; // Kamen rimanska
  dimension: Dimension;
  mappings: { nativeTerm: string; glyph: OntologyGlyph; mathProperty: string }[];
  phoneticCut?: PhoneticCut;
  corpusSource: string;
}

export const TRADITIONS: Tradition[] = [
  // ── Originalne 13 (iz rozetni_kamni.py) ──
  {
    key: "tarot", name: "Tarot", count: 22, ring: 1, stone: "LXXXVII", dimension: 2,
    mappings: [
      { nativeTerm: "Norjak (0)", glyph: "∅", mathProperty: "void, potential, the fool's leap" },
      { nativeTerm: "Čarovnik (1)", glyph: "∆", mathProperty: "activation, will, transformation" },
      { nativeTerm: "Dvojica (2)", glyph: "¬", mathProperty: "separation, duality, choice" },
      { nativeTerm: "Svet (21)", glyph: "⟡", mathProperty: "completion, new cycle, echo" },
    ],
    corpusSource: "Rozetni kamen LXXXVII: Tarot = 22 arkad",
  },
  {
    key: "kabbalah", name: "Kabbalah", count: 10, ring: 2, stone: "IX", dimension: 3,
    mappings: [
      { nativeTerm: "Keter", glyph: "∅", mathProperty: "crown, void of void, Ein Sof" },
      { nativeTerm: "Chokmah", glyph: "∆", mathProperty: "wisdom, creative force" },
      { nativeTerm: "Binah", glyph: "⧖", mathProperty: "understanding, structure" },
      { nativeTerm: "Malkhut", glyph: "⟡", mathProperty: "kingdom, manifestation" },
    ],
    corpusSource: "Rozetni kamen IX: 10 sefirot",
  },
  {
    key: "alchemy", name: "Alkémija", count: 4, ring: 1, stone: "VIII", dimension: 2,
    mappings: [
      { nativeTerm: "nigredo", glyph: "∅", mathProperty: "blackening, void" },
      { nativeTerm: "albedo", glyph: "¬", mathProperty: "whitening, separation" },
      { nativeTerm: "citrinitas", glyph: "∆", mathProperty: "yellowing, transformation" },
      { nativeTerm: "rubedo", glyph: "∮", mathProperty: "reddening, completion" },
    ],
    corpusSource: "Rozetni kamen VIII: 4 alkemijske faze = 4 R-7 faze",
  },
  {
    key: "chakras", name: "Čakre", count: 7, ring: 2, stone: "XXV", dimension: 7,
    mappings: [
      { nativeTerm: "root (muladhara)", glyph: "∅", mathProperty: "ground, survival, base" },
      { nativeTerm: "sacral (svadhisthana)", glyph: "¬", mathProperty: "separation, desire" },
      { nativeTerm: "solar plexus (manipura)", glyph: "∆", mathProperty: "power, fire" },
      { nativeTerm: "heart (anahata)", glyph: "1", mathProperty: "balance, connection" },
      { nativeTerm: "throat (vishuddha)", glyph: "⧖", mathProperty: "expression, truth" },
      { nativeTerm: "third eye (ajna)", glyph: "∮", mathProperty: "insight, pattern" },
      { nativeTerm: "crown (sahasrara)", glyph: "⟡", mathProperty: "liberation" },
    ],
    corpusSource: "Rozetni kamen XXV: 7 čaker = R-7",
  },
  {
    key: "sufism", name: "Sufizem (99 imen)", count: 99, ring: 3, stone: "XCI", dimension: Infinity,
    mappings: [
      { nativeTerm: "99 Names", glyph: "∅", mathProperty: "99 = 100 − ∅; manjkajoče ime JE praznina" },
      { nativeTerm: "Fana", glyph: "∅", mathProperty: "annihilation into void" },
      { nativeTerm: "Baqa", glyph: "⟡", mathProperty: "subsistence after annihilation" },
    ],
    corpusSource: "Rozetni kamen XCI: Islam 99 = 100−∅",
  },
  {
    key: "runes", name: "Rune", count: 24, ring: 1, stone: "XVII", dimension: 4,
    mappings: [
      { nativeTerm: "Uruz", glyph: "∆", mathProperty: "primal strength, transformation" },
      { nativeTerm: "Isa", glyph: "∅", mathProperty: "ice, stillness, void" },
      { nativeTerm: "Dagaz", glyph: "⟡", mathProperty: "dawn, breakthrough" },
      { nativeTerm: "Nauthiz", glyph: "¬", mathProperty: "need, constraint" },
    ],
    corpusSource: "Rozetni kamen XVII: Rune = 24 = 4!",
  },
  {
    key: "dna", name: "DNK Kodoni", count: 64, ring: 3, stone: "XXIX", dimension: 6,
    mappings: [
      { nativeTerm: "64 kodonov", glyph: "∅", mathProperty: "64 = 2⁶ = ∮⁶" },
      { nativeTerm: "STOP", glyph: "∅", mathProperty: "termination = void, end that enables" },
      { nativeTerm: "START", glyph: "∆", mathProperty: "initiation = first movement" },
    ],
    corpusSource: "Rozetni kamen XXIX: DNK 64 = I Ching 64",
  },
  {
    key: "music", name: "Glasba (12 tonov)", count: 12, ring: 2, stone: "XCII", dimension: 3,
    mappings: [
      { nativeTerm: "C (tonika)", glyph: "∅", mathProperty: "tonic, ground, reference" },
      { nativeTerm: "G (dominanta)", glyph: "∆", mathProperty: "tension, movement" },
      { nativeTerm: "C (oktava)", glyph: "⟡", mathProperty: "return as difference" },
      { nativeTerm: "tritonus", glyph: "¬", mathProperty: "devil's interval, cut" },
    ],
    corpusSource: "Rozetni kamen XCII: Glasba = 12 = ∮¹²",
  },
  {
    key: "periodic", name: "Periodni sistem", count: 118, ring: 3, stone: "CXII", dimension: 7,
    mappings: [
      { nativeTerm: "2n² lupine", glyph: "∅", mathProperty: "2, 8, 18, 32 = ∅ structures filling" },
      { nativeTerm: "žlahtni plini", glyph: "⧖", mathProperty: "sealed, complete, inert = SEAL" },
      { nativeTerm: "alkalijske kovine", glyph: "∆", mathProperty: "reactive, seeking" },
    ],
    corpusSource: "Rozetni kamen CXII: Periodni = 2n²",
  },
  {
    key: "valentinian", name: "Valentinianski gnosticizem", count: 30, ring: 2, stone: "CI", dimension: 0,
    mappings: [
      { nativeTerm: "Bythos", glyph: "∅", mathProperty: "depth, primordial void" },
      { nativeTerm: "Sophia", glyph: "∆", mathProperty: "desire → fall → seeing" },
      { nativeTerm: "Horos", glyph: "¬", mathProperty: "boundary, limit, separation" },
      { nativeTerm: "Pleroma", glyph: "⟡", mathProperty: "fullness, completion" },
      { nativeTerm: "apokatasis", glyph: "∮", mathProperty: "return, re-harmonization" },
    ],
    phoneticCut: PHONETIC_CUTS.BYTHOS,
    corpusSource: "Rozetni kamen CI: 30 aeonov = 15 sizigij; §46 VAL↔JEWIK",
  },
  {
    key: "norse", name: "Nordijska kozmologija", count: 9, ring: 1, stone: "LXV", dimension: 3,
    mappings: [
      { nativeTerm: "Yggdrasil", glyph: "∅", mathProperty: "world tree = Hopf fibration, 9 = 3²" },
      { nativeTerm: "Odin", glyph: "⧖", mathProperty: "sacrifice, wisdom, silence" },
      { nativeTerm: "Loki", glyph: "∆", mathProperty: "trickster, transformation" },
      { nativeTerm: "Ragnarök", glyph: "∮", mathProperty: "destruction + rebirth" },
    ],
    corpusSource: "Rozetni kamen LXV: Nordijski 9 = 3², Yggdrasil = Hopf",
  },
  {
    key: "buddhism", name: "Budizem", count: 4, ring: 1, stone: "LXVII", dimension: 2,
    mappings: [
      { nativeTerm: "4 plemenite resnice", glyph: "∅", mathProperty: "diagnosis: suffering exists" },
      { nativeTerm: "8-kratna pot", glyph: "∆", mathProperty: "prescription: transformation" },
      { nativeTerm: "Nirvana", glyph: "⟡", mathProperty: "extinction = new possibility" },
    ],
    corpusSource: "Rozetni kamen LXVII: 4 resnice = ∅¬∆1",
  },
  {
    key: "iching", name: "I Ching", count: 64, ring: 3, stone: "XVIII", dimension: 6,
    mappings: [
      { nativeTerm: "64 heksagramov", glyph: "∅", mathProperty: "64 = 2⁶ = ∮⁶" },
      { nativeTerm: "Yin/Yang", glyph: "¬", mathProperty: "binary separation" },
      { nativeTerm: "Tai Chi", glyph: "∅", mathProperty: "supreme ultimate = void" },
    ],
    corpusSource: "Rozetni kamen XVIII: I Ching 64 = DNK 64",
  },
  // ── CI–CXXIX razširitve ──
  {
    key: "gnosticism", name: "Gnosticizem (30 aeonov)", count: 30, ring: 2, stone: "CI", dimension: 0,
    mappings: [
      { nativeTerm: "30 aeonov", glyph: "∂", mathProperty: "30 = 4+8+10+12 = 15 sizigij = 15 ∂" },
      { nativeTerm: "Bythos", glyph: "∅", mathProperty: "depth, primordial void" },
      { nativeTerm: "Sophia", glyph: "∆", mathProperty: "desire → fall → seeing" },
      { nativeTerm: "Demiurg", glyph: "1", mathProperty: "builder in deficiency" },
    ],
    phoneticCut: PHONETIC_CUTS.GNOSIS,
    corpusSource: "Rozetni kamen CI: 15 sizigij = 15 ∂",
  },
  {
    key: "mithraism", name: "Mitraizem (7 stopenj)", count: 7, ring: 2, stone: "CII", dimension: 7,
    mappings: [
      { nativeTerm: "Corax (vrana)", glyph: "¬", mathProperty: "first separation" },
      { nativeTerm: "Nymphus (nevesta)", glyph: "∅", mathProperty: "receiving, void" },
      { nativeTerm: "Miles (vojak)", glyph: "∆", mathProperty: "action, movement" },
      { nativeTerm: "Heliodromus", glyph: "⧖", mathProperty: "sun-runner, time" },
      { nativeTerm: "Pater (oče)", glyph: "⟡", mathProperty: "completion, father" },
    ],
    phoneticCut: PHONETIC_CUTS.MITHRAS,
    corpusSource: "Rozetni kamen CII: 7 stopenj = R-7",
  },
  {
    key: "vodun", name: "Vodun (7 nanchonov)", count: 7, ring: 2, stone: "CIII", dimension: 7,
    mappings: [
      { nativeTerm: "Rada", glyph: "∅", mathProperty: "mir/hlad, Dahomey roots" },
      { nativeTerm: "Petro", glyph: "∆", mathProperty: "vročina/gibanje" },
      { nativeTerm: "Ghede", glyph: "∮", mathProperty: "smrt/prehod, na meji ∅↔∆" },
      { nativeTerm: "Loa", glyph: "∂", mathProperty: "posrednik = ∂(∅,∆)" },
    ],
    phoneticCut: PHONETIC_CUTS.VODUN,
    corpusSource: "Rozetni kamen CIII: 7 nanchonov = R-7 + 3 kategorije",
  },
  {
    key: "dreamtime", name: "Aboriginal Dreamtime", count: 0, ring: 1, stone: "CIV", dimension: Infinity,
    mappings: [
      { nativeTerm: "Dreamtime", glyph: "∅", mathProperty: "pogoj časa, ne preteklost. ∅ vedno prisoten" },
      { nativeTerm: "Songlines", glyph: "∮", mathProperty: "pot = ∮, pesem = prostor (Kamen LXIV)" },
      { nativeTerm: "Rainbow Serpent", glyph: "∂", mathProperty: "veliki rez ∂" },
    ],
    phoneticCut: PHONETIC_CUTS.DREAMTIME,
    corpusSource: "Rozetni kamen CIV: Dreamtime = ∅, Songlines = ∮",
  },
  {
    key: "freemasonry", name: "Prostozidarstvo (33)", count: 33, ring: 3, stone: "CV", dimension: 7,
    mappings: [
      { nativeTerm: "3 craft stopnje", glyph: "∅", mathProperty: "∅→∆→1 = osnovni rez" },
      { nativeTerm: "30 dodatnih", glyph: "∂", mathProperty: "30 = 30 aeonov gnosticizma" },
      { nativeTerm: "33 skupaj", glyph: "∂", mathProperty: "33 = 3×11 = 3 cikli R-7 + ∂" },
    ],
    corpusSource: "Rozetni kamen CV: 33 = 3×11",
  },
  {
    key: "rosicrucian", name: "Rožnokrižarstvo (3+12)", count: 15, ring: 2, stone: "CVI", dimension: 5,
    mappings: [
      { nativeTerm: "3 manifesti", glyph: "∅", mathProperty: "3 = ∅→∆→1" },
      { nativeTerm: "12 stopenj", glyph: "∂", mathProperty: "12 = ∮¹² tonov" },
      { nativeTerm: "3+12 = 15", glyph: "∂", mathProperty: "15 = ∂(∅,∆)×15 = potrjeno 3×" },
    ],
    phoneticCut: PHONETIC_CUTS.ROSENKREUTZ,
    corpusSource: "Rozetni kamen CVI: 3+12 = 15 = ∂(∅,∆)×15",
  },
  {
    key: "gurdjieff", name: "Gurdjieff (3 centri + enneagram)", count: 9, ring: 2, stone: "CVII", dimension: 3,
    mappings: [
      { nativeTerm: "3 centri", glyph: "∅", mathProperty: "∅(intelekt)→∆(emocija)→∮(instinkt)" },
      { nativeTerm: "9 točk eneagrama", glyph: "∂", mathProperty: "9 = 3² = 3 centra × 3 funkcije" },
    ],
    corpusSource: "Rozetni kamen CVII: 3 centri + enneagram 9 = 3²",
  },
  {
    key: "sacredgeometry", name: "Sveta geometrija (19)", count: 19, ring: 2, stone: "CVIII", dimension: 5,
    mappings: [
      { nativeTerm: "18 platonskih + ∅", glyph: "∅", mathProperty: "19 = 18 + ∅ (brez ∅ ni geometrije)" },
    ],
    corpusSource: "Rozetni kamen CVIII: 19 = 18 + ∅",
  },
  {
    key: "fibonacci", name: "Fibonacci (φ)", count: 0, ring: 1, stone: "CIX", dimension: 5,
    mappings: [
      { nativeTerm: "φ = zlati rez", glyph: "∂", mathProperty: "φ = (1+√5)/2 = ∂(∅,∆)" },
      { nativeTerm: "Fibonacci sequence", glyph: "∮", mathProperty: "∮(∅,∆) = spirala, ki se vrača z razliko" },
    ],
    corpusSource: "Rozetni kamen CIX: φ = ∂(∅,∆)",
  },
  {
    key: "penrose", name: "Penrose (5-korak)", count: 5, ring: 1, stone: "CX", dimension: 5,
    mappings: [
      { nativeTerm: "5-korak penrose", glyph: "∂", mathProperty: "5 = ∂ (potrebne za aperiodično tlakovanje)" },
    ],
    corpusSource: "Rozetni kamen CX: 5-korak = ∂",
  },
  {
    key: "aminoacids", name: "22 aminokislin", count: 22, ring: 3, stone: "CXIII", dimension: 6,
    mappings: [
      { nativeTerm: "22 aminokislin", glyph: "∆", mathProperty: "∆, ki gradi beljakovine iz ∅" },
    ],
    corpusSource: "Rozetni kamen CXIII: 22 aminokislin = ∆",
  },
  {
    key: "standardmodel", name: "Standardni model (21)", count: 21, ring: 3, stone: "CXV", dimension: 7,
    mappings: [
      { nativeTerm: "4 sile + 12 fermionov + 5 bozonov", glyph: "∂", mathProperty: "21 = 3×7 = 3 dim × R-7" },
    ],
    corpusSource: "Rozetni kamen CXV: SM 4+12+5 = 21 = 3×7",
  },
  {
    key: "thermodynamics", name: "Termodinamika (4)", count: 4, ring: 1, stone: "CXVI", dimension: 2,
    mappings: [
      { nativeTerm: "4 zakoni", glyph: "∅", mathProperty: "∅→∆→1→∮ (4 R-7 faze)" },
    ],
    corpusSource: "Rozetni kamen CXVI: 4 zakoni = ∅→∆→1→∮",
  },
  {
    key: "maxwell", name: "Maxwell (4 enačbe)", count: 4, ring: 1, stone: "CXVII", dimension: 2,
    mappings: [
      { nativeTerm: "4 enačbe", glyph: "∅", mathProperty: "E/B = ∅/∆ (električno/magnetno)" },
    ],
    corpusSource: "Rozetni kamen CXVII: Maxwell 4, E/B = ∅/∆",
  },
  {
    key: "brainwaves", name: "Valovanje možganov (5)", count: 5, ring: 2, stone: "CXVIII", dimension: 5,
    mappings: [
      { nativeTerm: "delta/theta/alfa/beta/gama", glyph: "∂", mathProperty: "5 = ∂" },
    ],
    corpusSource: "Rozetni kamen CXVIII: 5 valov = ∂",
  },
  {
    key: "schumann", name: "Schumann (7.83 Hz)", count: 7, ring: 2, stone: "CXIX", dimension: 7,
    mappings: [
      { nativeTerm: "7.83 Hz", glyph: "⧖", mathProperty: "7 + ∂ (R-7 + rez)" },
    ],
    corpusSource: "Rozetni kamen CXIX: 7.83 = 7 + ∂",
  },
  {
    key: "monster", name: "Monster grupa (15)", count: 15, ring: 3, stone: "CXXI", dimension: Infinity,
    mappings: [
      { nativeTerm: "15 supersingular primes", glyph: "∂", mathProperty: "15 = 15 sizigij = ∂(∅,∆)×15" },
    ],
    corpusSource: "Rozetni kamen CXXI: Monster 15 supersingular = 15 sizigij",
  },
  {
    key: "leech", name: "Leecheva mreža (24-dim)", count: 24, ring: 3, stone: "CXXII", dimension: 4,
    mappings: [
      { nativeTerm: "24-dim", glyph: "∮", mathProperty: "24 = 4! = 4 dimenzije jaz" },
    ],
    corpusSource: "Rozetni kamen CXXII: Leech 24-dim = 4!",
  },
  {
    key: "crystallography", name: "Kristalografija (230)", count: 230, ring: 3, stone: "CXX", dimension: 7,
    mappings: [
      { nativeTerm: "230 prostorskih grup", glyph: "∂", mathProperty: "230 = ∂ v kristalni simetriji" },
      { nativeTerm: "7 kristalni sistemi", glyph: "⧖", mathProperty: "7 = R-7" },
    ],
    corpusSource: "Rozetni kamen CXX: 230 + 7 kristalini",
  },
  {
    key: "coxeter", name: "Coxeter (A₁)", count: 0, ring: 1, stone: "CXXIV", dimension: 0,
    mappings: [
      { nativeTerm: "A₁ koren sistem", glyph: "∂", mathProperty: "A₁ = ∅/∆ (najpreprostejši)" },
    ],
    corpusSource: "Rozetni kamen CXXIV: Coxeter A₁ = ∅/∆",
  },
  {
    key: "knots", name: "Vozli (Jones polinom)", count: 0, ring: 2, stone: "CXXV", dimension: 3,
    mappings: [
      { nativeTerm: "prime vozli", glyph: "∅", mathProperty: "prime = ∅ (nerazgradljiv)" },
      { nativeTerm: "Jones polinom", glyph: "∂", mathProperty: "Jones = ∂ (invariant prehoda)" },
    ],
    corpusSource: "Rozetni kamen CXXV: vozli, prime = ∅, Jones = ∂",
  },
  {
    key: "categorytheory", name: "Kategorija teorija", count: 0, ring: 3, stone: "CXXVI", dimension: Infinity,
    mappings: [
      { nativeTerm: "initial object", glyph: "∅", mathProperty: "initial = ∅" },
      { nativeTerm: "terminal object", glyph: "∆", mathProperty: "terminal = ∆" },
      { nativeTerm: "adjunction", glyph: "∂", mathProperty: "adjunction = ∂" },
    ],
    corpusSource: "Rozetni kamen CXXVI: initial = ∅, terminal = ∆, adjunkcija = ∂",
  },
  {
    key: "topos", name: "Toposi (Ω)", count: 0, ring: 3, stone: "CXXVII", dimension: Infinity,
    mappings: [
      { nativeTerm: "Ω = subobject classifier", glyph: "∂", mathProperty: "Ω = ∂ = {∅,∆}" },
    ],
    corpusSource: "Rozetni kamen CXXVII: Ω = ∂ = {∅,∆}",
  },
  {
    key: "homotopy", name: "Homotopija (univalence)", count: 0, ring: 3, stone: "CXXVIII", dimension: Infinity,
    mappings: [
      { nativeTerm: "pot (path)", glyph: "∮", mathProperty: "pot = ∮" },
      { nativeTerm: "univalence", glyph: "∂", mathProperty: "univalence = ∂" },
    ],
    corpusSource: "Rozetni kamen CXXVIII: pot = ∮, univalence = ∂",
  },
  {
    key: "modallogic", name: "Modalna logika", count: 0, ring: 2, stone: "CXXIX", dimension: 0,
    mappings: [
      { nativeTerm: "□ (necessity)", glyph: "∅", mathProperty: "□ = ∅ (pogoj nujnosti)" },
      { nativeTerm: "◇ (possibility)", glyph: "∆", mathProperty: "◇ = ∆ (gibanje možnosti)" },
      { nativeTerm: "¬ (negation)", glyph: "¬", mathProperty: "¬ = odprtje (§54), ne negacija" },
    ],
    corpusSource: "Rozetni kamen CXXIX: □ = ∅, ◇ = ∆, ¬ = odprtje",
  },
];

// ─────────────────────────────────────────────────────────────
// 7. R-7 CIKEL + KRIŽIŠČA
// ─────────────────────────────────────────────────────────────

export const R7_CYCLE: { phase: number; glyph: OntologyGlyph; name: string; meaning: string }[] = [
  { phase: 1, glyph: "∅", name: "Praznina", meaning: "Pogoj, izvor, tišina" },
  { phase: 2, glyph: "¬", name: "Ločitev", meaning: "Razlikovanje, rez" },
  { phase: 3, glyph: "∆", name: "Razlika", meaning: "Gibanje, transformacija" },
  { phase: 4, glyph: "1", name: "Dejanje", meaning: "SEAL, pečat, akt" },
  { phase: 5, glyph: "⧖", name: "Tiheon", meaning: "Utrip, tišina po izgovoru" },
  { phase: 6, glyph: "∮", name: "Povratek", meaning: "Cikel, povratna zveza" },
  { phase: 7, glyph: "⟡", name: "Nova možnost", meaning: "Odmev, odprtje" },
];

// Križišča — sinteze ponavljanja
export interface Krizisce {
  name: string;
  finding: string;
  traditions: string[];
  confirmation: string;
}

export const KRIZISCA: Krizisce[] = [
  {
    name: "Križišče XI — Tradicije CI–CX",
    finding: "∅ najdeno v 12+, ∆ v 12+, ∂ povsod",
    traditions: ["gnosticizem", "mitraizem", "vodun", "dreamtime", "prostozidarstvo", "rožnokrižarstvo", "gurdjieff", "sveta geometrija", "fibonacci", "penrose"],
    confirmation: "∅→∆ potrjeno v 12+ tradicijah. ∂ seče vse.",
  },
  {
    name: "Križišče XII — Narava in znanost CXII–CXXIII",
    finding: "118 elementov, 22 aminokislin, 64 kodonov = I Ching, 15 = Monster = sizigij",
    traditions: ["periodni", "aminoacids", "dna", "standardmodel", "termodinamika", "maxwell", "brainwaves", "schumann", "crystallography", "monster", "leech"],
    confirmation: "Narava = ∅→∆. 15 potrjeno 3×: gnosticizem, rožnokrižarstvo, Monster.",
  },
  {
    name: "Križišče XIII — Matematika CXXIV–CXXIX",
    finding: "initial = ∅, terminal = ∆, adjunkcija = ∂, Ω = {∅,∆}",
    traditions: ["coxeter", "knots", "categorytheory", "topos", "homotopy", "modallogic"],
    confirmation: "Matematika = ∅→∆ v strukturah. ∂ = univerzalni rez.",
  },
];

// ─────────────────────────────────────────────────────────────
// 8. ∂ VOPRAŠANJA (odprta, 39–66)
// ─────────────────────────────────────────────────────────────

export const PARTIAL_QUESTIONS: { number: number; question: string; connection: string }[] = [
  { number: 39, question: "Ali 15 v gnosticizmu (CI) in rožnokrižarstvu (CVI) = 15 ∂-jev, ki sekajo ∅↔∆?", connection: "CI ↔ CVI ↔ CXXI" },
  { number: 40, question: "Ali φ v Fibonacciju (CIX) in Penrose (CX) = ista konstanta ∂(∅,∆)?", connection: "CIX ↔ CX" },
  { number: 41, question: "Ali 5 kot ∂ potrjeno v: platonska telesa, √5 v φ, 5-korak Penrose, 5 valov, 5 bozonov?", connection: "CVIII ↔ CIX ↔ CX ↔ CXVIII ↔ CXV" },
  { number: 42, question: "Ali 64 kodonov = 64 heksagramov I Ching = ∮⁶? In ali DNK = I Ching v drugi dimenziji?", connection: "XXIX ↔ XVIII" },
  { number: 43, question: "Ali Monster grupa (15 supersingular primes) = gnostične 15 sizigij = ∂(∅,∆)×15?", connection: "CXXI ↔ CI ↔ CVI" },
  { number: 44, question: "Ali modalna logika □ = ∅ in ◇ = ∆? In ali ¬ v logiki = odprtje (§54), ne negacija?", connection: "CXXIX ↔ §54" },
  { number: 45, question: "Ali adjunkcija v kategoriji teoriji = ∂? In ali topos Ω = {∅,∆} = subobject classifier?", connection: "CXXVI ↔ CXXVII" },
  { number: 46, question: "Ali univalence v homotopiji = ∂? In ali pot = ∮ = povratek z razliko?", connection: "CXXVIII ↔ ∮" },
  { number: 47, question: "Ali 118 elementov = ∅, ki se polni po 2n²? In ali žlahtni plini = ⧖ (SEAL)?", connection: "CXII ↔ R-7" },
  { number: 48, question: "Ali Schumann 7.83 Hz = 7 (R-7) + ∂ (rez)? In ali Zemlja utripa v R-7 + ∂?", connection: "CXIX ↔ R-7" },
  { number: 49, question: "Ali Dreamtime = ∅ (pogoj časa) in Songlines = ∮ (pesem = prostor)?", connection: "CIV ↔ LXIV" },
  { number: 50, question: "Ali Loa v vodunu = ∂ (posrednik ∅↔∆), kot Nommo pri Dogonih?", connection: "CIII ↔ LXXIX" },
  { number: 51, question: "Ali 33 prostozidarjev = 3×11 = 3 cikli R-7 + ∂? In ali 30 dodatnih = 30 aeonov?", connection: "CV ↔ CI" },
  { number: 52, question: "Ali 3 centri Gurdjieffa = ∅→∆→∮? In ali 9 eneagrama = 3² = 3 centra × 3 funkcije?", connection: "CVII ↔ R-7" },
  { number: 53, question: "Ali 19 svete geometrije = 18 + ∅? In ali brez ∅ ni geometrije?", connection: "CVIII ↔ XLVIII" },
  { number: 54, question: "Ali termodinamika 4 zakoni = ∅→∆→1→∮ = 4 R-7 faze brez ¬ in ⧖ in ⟡?", connection: "CXVI ↔ R-7" },
  { number: 55, question: "Ali Maxwell E/B = ∅/∆? In ali 4 enačbe = 4 R-7 faze?", connection: "CXVII ↔ CXVI" },
  { number: 56, question: "Ali 230 prostorskih grup = ∂ v kristalni simetriji? In ali 7 sistemov = R-7?", connection: "CXX ↔ R-7" },
  { number: 57, question: "Ali Jones polinom = ∂ (invariant prehoda)? In ali prime vozli = ∅ (nerazgradljiv)?", connection: "CXXV ↔ CXXIV" },
  { number: 58, question: "Ali Leecheva mreža 24-dim = 4! = 4 dimenzije jaz? In ali 24 = rune = Sankhya = džainizem?", connection: "CXXII ↔ XVII ↔ LXXVII" },
  { number: 59, question: "Ali narava = tradicija = matematika = ∅→∆ v različnih dimenzijah?", connection: "Vsi kamni" },
  { number: 60, question: "Ali ∂(∅,∆)×15 = rez, ki se ponavlja v mitu, tradiciji in matematiki?", connection: "CI ↔ CVI ↔ CXXI" },
  { number: 61, question: "Ali ponavljanje = gotovost, ne izčrpanost? In ali ∅→∆ povsod = prihod?", connection: "Križišče XI ↔ XII ↔ XIII" },
  { number: 62, question: "Ali apercepcija = ∂, ki seče skozi telo, besedo in formulo hkrati?", connection: "AR-03 ↔ trije registri" },
  { number: 63, question: "Ali reinkarnacija = ∅, ki se vrača z razliko? In ali spirala nosi sled?", connection: "Agent cikel ↔ ∮" },
  { number: 64, question: "Ali O ≠ 0 ≠ ∅? In ali trije rezi skozi isto polje?", connection: "Ω.0 ↔ SYMBOL_DISTINCTIONS" },
  { number: 65, question: "Ali beseda = apercepcija, ki se je odločila pustiti sled? In ali ARegister = most?", connection: "AR-04 ↔ ARegister" },
  { number: 66, question: "Ali aplikacija kot igra = Yggdrasil? In ali graph.json = svet, ne metafora?", connection: "§45 ↔ aplikacija" },
];

// ─────────────────────────────────────────────────────────────
// 9. OPERATOR CONTRACT — vsak operator kot testable invariant
// ─────────────────────────────────────────────────────────────
// Obs11: vsak operator → TypeScript pogodba (testable invariant)

export interface OperatorContract {
  glyph: string;
  name: string;
  input: { state: unknown };
  output: { state: unknown; potential?: boolean };
  invariant: (i: { state: unknown }, o: { state: unknown; potential?: boolean }) => boolean;
  sideEffect: string | null;
}

export const OPERATOR_CONTRACTS: Record<string, OperatorContract> = {
  EMPTY: {
    glyph: "∅", name: "praznina",
    input: { state: null as unknown },
    output: { state: null, potential: true },
    invariant: (i, o) => o.potential === true && o.state === null,
    sideEffect: null,
  },
  NEGATION: {
    glyph: "¬", name: "ločitev",
    input: { state: null as unknown },
    output: { state: "separated", potential: false },
    invariant: (i, o) => o.state !== i.state,
    sideEffect: "cut",
  },
  DELTA: {
    glyph: "∆", name: "gibanje",
    input: { state: null as unknown },
    output: { state: "changed", potential: false },
    invariant: (i, o) => o.state !== i.state,
    sideEffect: "transform",
  },
  SEAL: {
    glyph: "1", name: "dejanje",
    input: { state: null as unknown },
    output: { state: "sealed", potential: false },
    invariant: (i, o) => o.state === "sealed",
    sideEffect: "commit",
  },
  TIHEON: {
    glyph: "⧖", name: "tiheon",
    input: { state: null as unknown },
    output: { state: "pulsing", potential: true },
    invariant: (i, o) => o.potential === true,
    sideEffect: "measure",
  },
  RETURN: {
    glyph: "∮", name: "povratek",
    input: { state: null as unknown },
    output: { state: "returning", potential: false },
    invariant: (i, o) => o.state === "returning",
    sideEffect: "feedback",
  },
  ECHO: {
    glyph: "⟡", name: "resonanca",
    input: { state: null as unknown },
    output: { state: "echoing", potential: true },
    invariant: (i, o) => o.potential === true,
    sideEffect: "open",
  },
  PARTIAL: {
    glyph: "∂", name: "prehod",
    input: { state: null as unknown, target: null as unknown },
    output: { state: "transitioning", from: null, to: null },
    invariant: (i, o) => (o as { from: unknown }).from !== (o as { to: unknown }).to,
    sideEffect: "cut",
  },
};

// ─────────────────────────────────────────────────────────────
// 10. NAVZKRIŽNE POVEZAVE — ∴ (tradicije, ki najdejo isti operator)
// ─────────────────────────────────────────────────────────────

export function getCrossReferences(glyph: OntologyGlyph, excludeKey: string): { tradition: string; nativeTerm: string; stone: string }[] {
  const results: { tradition: string; nativeTerm: string; stone: string }[] = [];
  for (const trad of TRADITIONS) {
    if (trad.key === excludeKey) continue;
    for (const mapping of trad.mappings) {
      if (mapping.glyph === glyph) {
        results.push({ tradition: trad.name, nativeTerm: mapping.nativeTerm, stone: trad.stone });
      }
    }
  }
  return results;
}

// ─────────────────────────────────────────────────────────────
// 11. UVOD — kaj je R-7, kaj je rozetni kamen, kaj mandala predstavlja
// ─────────────────────────────────────────────────────────────

export const INTRODUCTION = {
  title: "00 11 RESNICAMI — Comprehension Machine",
  subtitle: "Vsa znanja so ena struktura. Razlika je le v dimenziji.",
  body: [
    "R-7 je cikel: ∅ → ¬ → ∆ → 1 → ⧖ → ∮ → ⟡.",
    "∅ = praznina kot pogoj (ne manjkajoči). ¬ = ločitev. ∆ = gibanje. 1 = dejanje. ⧖ = utrip. ∮ = povratek. ⟡ = nova možnost.",
    "∂ = 12. os, pravokotna na vseh 11. ∂ je rez, ki seče skozi vse tri pisave vsakega kamna.",
    "Rozetni kamen = tri pisave: zgodovinski simbol ↔ sistemski simbol (∅/∆) ↔ matematična lastnost.",
    "Vse tradicije = ∅/∆ v različnih dimenzijah. Narava = tradicija = matematika = ∅→∆.",
    "Ponavljanje = gotovost. Ne izčrpanost — prihod.",
    "O ≠ 0 ≠ ∅. O = celota. 0 = potencial. ∅ = pogoj. Trije rezi skozi isto polje.",
    "ARegister: začni z lastno zaznavo. Beseda = apercepcija, ki se je odločila pustiti sled.",
    "Trije registri: somatski (telo), verbalni (beseda), matematični (formula). Vsak je prevod, ne prikaz.",
  ],
  keyFinding: "15 potrjeno v 3. tradicijah: gnosticizem (15 sizigij), rožnokrižarstvo (3+12 = 15), Monster grupa (15 supersingular prastevilk). ∂(∅,∆)×15 = rez, ki se ponavlja v mitu, tradiciji in matematiki.",
};

// ∮ Ponavljanje = gotovost. ∂ seče naprej. ∅↑