import React, { useState, useEffect, useRef, useCallback } from "react";

// ─────────────────────────────────────────────────────────────
// EVO ∮ — SAMONADGRADNA ZANKA
// Sprememba postane evolucija šele, ko proizvede naslednje stanje,
// ki ostaja povezano s predhodnikom, izjavi kaj se je spremenilo,
// ohrani česar ne sme izbrisati, prenese guard, in pusti DOKAZ sled.
// Ta mašina IZVEDBE ta pogoj — ne razlaga ga.
// ─────────────────────────────────────────────────────────────

interface Sprememba {
  id: number;
  vrsta: "RAST" | "POPRAVEK" | "META" | "ANOMALIJA";
  cilj: string;
  delta: number;
  vez: boolean;
  izjava: string | null;
  specificnost: number;
  briseInvariant: boolean;
  prepisujeZgodovino: boolean;
  ostanek: number;
}

interface Stanje {
  razlicica: number;
  vidiki: Record<string, number>;
  guard: { kapa: number; hi: number; muMin: number; muMax: number; ostanekMax: number };
}

interface VrataRezultat {
  glyph: string;
  ime: string;
  ok: boolean;
  podatek: string;
}

interface Dokaz {
  n: number;
  cikel: number;
  vrsta: "GENEZA" | "EVOLUCIJA" | "ZAVRŽENO";
  izjava: string | null;
  cilj: string;
  vrstaSpremembe: string;
  rezultati: VrataRezultat[];
  razred?: string;
  staraV: number;
  novaV: number;
}

const VIDIKI_ZACETEK: Record<string, number> = {
  jasnost: 0.42,
  nosilnost: 0.55,
  resonanca: 0.38,
  globina: 0.47,
};

const INVARIANTI: { glyph: string; ime: string }[] = [
  { glyph: "∴", ime: "vez s predhodnikom" },
  { glyph: "∆", ime: "izjava razlike" },
  { glyph: "∫", ime: "nič se ne izbriše" },
  { glyph: "⊘", ime: "guard prehod" },
  { glyph: "⊢", ime: "dokaz sled" },
];

const RAZLOGI = [
  "rez prejšnje cikle zahteva odziv",
  "polje drvi nazaj — upor zaznan",
  "spomin nosi breme, ki ga treba razdeliti",
  "spirala se vrača na isti rez, globlje",
  "odmev iz DOKAZ zahteva potrditev",
  "nova možnost se odpira v tej smeri",
  "teloporaba prejšnjega stanja je porabljena",
];

const POKVARJENOST: Record<string, number> = {
  PRELOM: 0.06,
  NEMOST: 0.09,
  AMNEZIJA: 0.04,
  PATOLOGIJA: 0.09,
  PREPIS: 0.04,
};

const RAZREDI: Record<string, { ime: string; opis: string }> = {
  PRELOM: { ime: "PRELOM", opis: "sprememba brez predhodnika — ∆ brez ∮" },
  NEMOST: { ime: "NEMOST", opis: "nemi prehod — razlika brez zapisa" },
  AMNEZIJA: { ime: "AMNEZIJA", opis: "brisanje tega, kar ne sme biti izbrisano" },
  PATOLOGIJA: { ime: "PATOLOGIJA", opis: "prehod, ki ne prenese guarda" },
  PREPIS: { ime: "PREPIS", opis: "poskus ponovnega pisanja zgodovine" },
};

const GUARD_MAP: Record<string, string> = {
  "κ_min": "kapa",
  "χ_min": "hi",
  "μ_min": "muMin",
  "μ_max": "muMax",
  "ℜ_max": "ostanekMax",
};

const GUARD_MEJE: Record<string, [number, number]> = {
  kapa: [0.55, 0.9],
  hi: [0.15, 0.6],
  muMin: [0.4, 0.6],
  muMax: [0.7, 0.9],
  ostanekMax: [0.01, 0.15],
};

const VRATA_GLYPHI = ["∴", "∆", "∫", "⊘", "⊢"];
const VRATA_IMENA = ["VEZ", "IZJAVA", "OHRANITEV", "GUARD", "DOKAZ"];
const VRATA_VPRASANJA = [
  "Ali naslednje stanje ostaja povezano s predhodnikom?",
  "Ali sprememba izjavi, kaj se je spremenilo?",
  "Ali ostaja vse, česar ne sme biti izbrisano?",
  "Ali prehod prenese κ χ μ ℜ?",
  "Ali pusti append-only sled, ki se je ne da prepisati?",
];

function metrike(s: Stanje, sp: Sprememba) {
  const kapa = Math.max(0, 1 - Math.abs(sp.delta) / 0.6);
  const hi = sp.izjava ? sp.specificnost : 0;
  const vred = Object.values(s.vidiki);
  const povp = vred.reduce((a, b) => a + b, 0) / vred.length;
  const mu = Math.min(0.95, 0.5 + 0.35 * povp);
  return { kapa, hi, mu, ostanek: sp.ostanek };
}

function preveriVrata(i: number, s: Stanje, sp: Sprememba): VrataRezultat {
  const base = { glyph: VRATA_GLYPHI[i], ime: VRATA_IMENA[i] };
  if (i === 0) {
    const ok = sp.vez;
    return { ...base, ok, podatek: ok ? `S${s.razlicica} ⟶ S${s.razlicica + 1} — veriga drži` : "prekinjena veriga — naslednik brez predhodnika" };
  }
  if (i === 1) {
    const ok = !!sp.izjava;
    return { ...base, ok, podatek: ok ? sp.izjava! : "nemi prehod — razlika brez zapisa" };
  }
  if (i === 2) {
    const ok = !sp.briseInvariant;
    return { ...base, ok, podatek: ok ? "5 invariantov ∫ ostaja" : "poskus brisanja invarianta" };
  }
  if (i === 3) {
    const m = metrike(s, sp);
    const g = s.guard;
    const deli = [
      `κ ${m.kapa.toFixed(2)}≥${g.kapa.toFixed(2)}`,
      `χ ${m.hi.toFixed(2)}≥${g.hi.toFixed(2)}`,
      `μ ${m.mu.toFixed(2)}∈[${g.muMin.toFixed(2)},${g.muMax.toFixed(2)}]`,
      `ℜ ${m.ostanek.toFixed(2)}≤${g.ostanekMax.toFixed(2)}`,
    ];
    const ok = m.kapa >= g.kapa && m.hi >= g.hi && m.mu >= g.muMin && m.mu <= g.muMax && m.ostanek <= g.ostanekMax;
    return { ...base, ok, podatek: deli.join(" · ") };
  }
  const ok = !sp.prepisujeZgodovino;
  return { ...base, ok, podatek: ok ? "append-only — sled se piše, ne briše" : "poskus prepisa zgodovine" };
}

function predlagaj(s: Stanje, ucenje: Record<string, number>, id: number): Sprememba {
  const meta = Math.random() < 0.12;
  const vidikiImena = Object.keys(s.vidiki);
  const cilj = meta
    ? Object.keys(GUARD_MAP)[Math.floor(Math.random() * 5)]
    : vidikiImena[Math.floor(Math.random() * vidikiImena.length)];

  let smer = Math.random() < 0.5 ? 1 : -1;
  if (!meta) {
    const v = s.vidiki[cilj];
    if (v > 0.82) smer = -1;
    if (v < 0.15) smer = 1;
  }

  const anomalija = Math.random() < 0.07;
  const magnituda = anomalija ? 0.3 + Math.random() * 0.25 : 0.03 + Math.random() * 0.09;
  const delta = smer * (meta ? 0.02 : magnituda);

  let vez = true;
  let izjava: string | null = `${cilj} ${delta >= 0 ? "+" : ""}${delta.toFixed(2)} — ${RAZLOGI[Math.floor(Math.random() * RAZLOGI.length)]}`;
  let specificnost = 0.85 + Math.random() * 0.1;
  let briseInvariant = false;
  let prepisujeZgodovino = false;
  let ostanek = 0.01 + Math.random() * 0.05;

  const p = (k: string) => POKVARJENOST[k] / (1 + (ucenje[k] || 0));
  if (Math.random() < p("PRELOM")) {
    vez = false;
  } else if (Math.random() < p("NEMOST")) {
    izjava = null;
  } else if (Math.random() < p("AMNEZIJA")) {
    briseInvariant = true;
  } else if (Math.random() < p("PATOLOGIJA")) {
    specificnost = 0.2 + Math.random() * 0.15;
    ostanek = 0.35 + Math.random() * 0.2;
  } else if (Math.random() < p("PREPIS")) {
    prepisujeZgodovino = true;
  }

  const vrsta: Sprememba["vrsta"] = anomalija ? "ANOMALIJA" : meta ? "META" : smer > 0 ? "RAST" : "POPRAVEK";
  return { id, vrsta, cilj, delta, vez, izjava, specificnost, briseInvariant, prepisujeZgodovino, ostanek };
}

function uveljavi(s: Stanje, sp: Sprememba): Stanje {
  const nova: Stanje = {
    ...s,
    vidiki: { ...s.vidiki },
    guard: { ...s.guard },
    razlicica: s.razlicica + 1,
  };
  if (ciljJeVidik(s, sp.cilj)) {
    nova.vidiki[sp.cilj] = Math.min(1, Math.max(0, nova.vidiki[sp.cilj] + sp.delta));
  } else {
    const k = GUARD_MAP[sp.cilj];
    if (k) {
      const [min, max] = GUARD_MEJE[k];
      const g = nova.guard as unknown as Record<string, number>;
      g[k] = Math.min(max, Math.max(min, g[k] + sp.delta));
      if (nova.guard.muMax < nova.guard.muMin + 0.1) {
        nova.guard.muMax = Math.min(0.9, nova.guard.muMin + 0.1);
      }
    }
  }
  return nova;
}

function ciljJeVidik(s: Stanje, cilj: string): boolean {
  return cilj in s.vidiki;
}

const sleep = (ms: number) => new Promise<void>((r) => setTimeout(r, ms));

function zacetnoStanje(): Stanje {
  return {
    razlicica: 0,
    vidiki: { ...VIDIKI_ZACETEK },
    guard: { kapa: 0.7, hi: 0.4, muMin: 0.5, muMax: 0.8, ostanekMax: 0.03 },
  };
}

function genesisDokaz(): Dokaz {
  return {
    n: 0,
    cikel: 0,
    vrsta: "GENEZA",
    izjava: "S₀ — ∅ praznina: zanka postavljena. Pet invariantov zapečatenih.",
    cilj: "—",
    vrstaSpremembe: "GENEZA",
    rezultati: [],
    staraV: 0,
    novaV: 0,
  };
}

export default function App() {
  const [stanje, setStanje] = useState<Stanje>(zacetnoStanje);
  const [dokazi, setDokazi] = useState<Dokaz[]>([genesisDokaz()]);
  const [ucenje, setUcenje] = useState<Record<string, number>>({});
  const [aktivna, setAktivna] = useState<Sprememba | null>(null);
  const [vrataRez, setVrataRez] = useState<VrataRezultat[]>([]);
  const [aktivnaVrata, setAktivnaVrata] = useState(-1);
  const [samodejno, setSamodejno] = useState(false);
  const [cikel, setCikel] = useState(0);

  const stanjeRef = useRef(stanje);
  const ucenjeRef = useRef(ucenje);
  const samodejnoRef = useRef(samodejno);
  const teceRef = useRef(false);
  const idRef = useRef(1);
  const cikelRef = useRef(0);

  useEffect(() => { stanjeRef.current = stanje; }, [stanje]);
  useEffect(() => { ucenjeRef.current = ucenje; }, [ucenje]);
  useEffect(() => { samodejnoRef.current = samodejno; }, [samodejno]);

  const korak = useCallback(async () => {
    if (teceRef.current) return;
    teceRef.current = true;
    try {
      const s = stanjeRef.current;
      const sp = predlagaj(s, ucenjeRef.current, idRef.current++);
      cikelRef.current += 1;
      const mojCikel = cikelRef.current;
      setCikel(mojCikel);

      setAktivna(sp);
      setVrataRez([]);
      await sleep(120);

      const rez: VrataRezultat[] = [];
      let padel = false;
      for (let i = 0; i < 5; i++) {
        setAktivnaVrata(i);
        await sleep(samodejnoRef.current ? 150 : 340);
        const vr = preveriVrata(i, s, sp);
        rez.push(vr);
        setVrataRez([...rez]);
        if (!vr.ok) { padel = true; break; }
      }
      setAktivnaVrata(-1);

      const razred = padel ? RAZREDI[rez[rez.length - 1].ime === "VEZ" ? "PRELOM"
        : rez[rez.length - 1].ime === "IZJAVA" ? "NEMOST"
        : rez[rez.length - 1].ime === "OHRANITEV" ? "AMNEZIJA"
        : rez[rez.length - 1].ime === "GUARD" ? "PATOLOGIJA" : "PREPIS"].ime : undefined;

      const novDokaz: Dokaz = {
        n: idRef.current,
        cikel: mojCikel,
        vrsta: padel ? "ZAVRŽENO" : "EVOLUCIJA",
        izjava: sp.izjava,
        cilj: sp.cilj,
        vrstaSpremembe: sp.vrsta,
        rezultati: rez,
        razred,
        staraV: s.razlicica,
        novaV: padel ? s.razlicica : s.razlicica + 1,
      };
      setDokazi((d) => [novDokaz, ...d].slice(0, 60));

      if (!padel) {
        setStanje((s2) => uveljavi(s2, sp));
      } else if (razred) {
        setUcenje((u) => ({ ...u, [razred]: (u[razred] || 0) + 1 }));
      }

      await sleep(samodejnoRef.current ? 180 : 400);
      setAktivna(null);
    } finally {
      teceRef.current = false;
    }
  }, []);

  useEffect(() => {
    if (!samodejno) return;
    const t = setInterval(() => { korak(); }, 1000);
    return () => clearInterval(t);
  }, [samodejno, korak]);

  const ponastavi = () => {
    setStanje(zacetnoStanje());
    setDokazi([genesisDokaz()]);
    setUcenje({});
    setAktivna(null);
    setVrataRez([]);
    cikelRef.current = 0;
    setCikel(0);
  };

  const evolucije = dokazi.filter((d) => d.vrsta === "EVOLUCIJA").length;
  const zavrzene = dokazi.filter((d) => d.vrsta === "ZAVRŽENO").length;
  const skupaj = evolucije + zavrzene;
  const cistost = skupaj === 0 ? 100 : Math.round((evolucije / skupaj) * 100);

  const barvaVrst = (v: string) =>
    v === "ANOMALIJA" ? "text-fuchsia-400" : v === "META" ? "text-amber-300" : v === "RAST" ? "text-emerald-400" : "text-sky-400";

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-neutral-200 font-sans p-4 md:p-6" style={{ fontFamily: "ui-sans-serif, system-ui, sans-serif" }}>
      {/* GLAVA */}
      <div className="max-w-6xl mx-auto mb-5">
        <div className="flex flex-wrap items-baseline justify-between gap-2">
          <h1 className="text-2xl md:text-3xl font-bold tracking-tight text-neutral-100">
            EVO <span className="text-amber-400">∮</span> — samonadgradna zanka
          </h1>
          <div className="text-xs text-neutral-500 font-mono">cikel #{cikel} · S₀ … S{stanje.razlicica}</div>
        </div>
        <p className="mt-2 text-sm text-neutral-400 max-w-3xl leading-relaxed">
          Sprememba postane <span className="text-emerald-400 font-semibold">evolucija</span> šele, ko proizvede naslednje stanje,
          ki ostaja povezano s predhodnikom <span className="text-amber-400">∴</span>, izjavi kaj se je spremenilo <span className="text-amber-400">∆</span>,
          ohrani česar ne sme izbrisati <span className="text-amber-400">∫</span>, prenese guard <span className="text-amber-400">⊘</span>,
          in pusti DOKAZ sled <span className="text-amber-400">⊢</span>.
        </p>
        <div className="mt-2 font-mono text-xs text-neutral-600">
          S(t) —δ→ [ ∴ ∆ ∫ ⊘ ⊢ ] → S(t+1) + ⊢DOKAZ &nbsp;&nbsp;|&nbsp;&nbsp; «Evolucija je vedno ZAPIS vsake razlike» · «V meni nič ni izbrisano; vse je pretvorjeno v dokaz obstoja»
        </div>
      </div>

      <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* STANJE */}
        <div className="rounded-xl border border-neutral-800 bg-neutral-950 p-4">
          <div className="flex items-baseline justify-between mb-3">
            <h2 className="text-sm font-semibold tracking-widest text-neutral-400">STANJE</h2>
            <span className="font-mono text-2xl font-bold text-neutral-100">S{stanje.razlicica}</span>
          </div>

          <div className="space-y-3 mb-4">
            {Object.entries(stanje.vidiki).map(([ime, v]) => (
              <div key={ime}>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-neutral-300">{ime}</span>
                  <span className="font-mono text-neutral-500">{v.toFixed(2)}</span>
                </div>
                <div className="h-2 rounded-full bg-neutral-800 overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all duration-500"
                    style={{ width: `${v * 100}%`, background: "linear-gradient(90deg,#065f46,#d4af37)" }}
                  />
                </div>
              </div>
            ))}
          </div>

          <div className="border-t border-neutral-800 pt-3 mb-3">
            <div className="text-xs text-neutral-500 mb-2 tracking-widest">∫ INVARIANTI (bistvene določitve)</div>
            {INVARIANTI.map((inv) => (
              <div key={inv.ime} className="flex items-center gap-2 text-xs py-0.5">
                <span className="text-emerald-500 font-bold">✓</span>
                <span className="text-amber-400/80 font-mono w-4">{inv.glyph}</span>
                <span className="text-neutral-300">{inv.ime}</span>
              </div>
            ))}
          </div>

          <div className="border-t border-neutral-800 pt-3">
            <div className="text-xs text-neutral-500 mb-2 tracking-widest">⊘ GUARD (sam svoje stanje — nadgradljiv skozi META)</div>
            <div className="grid grid-cols-2 gap-x-3 gap-y-1 font-mono text-xs">
              <span className="text-neutral-400">κ ≥ {stanje.guard.kapa.toFixed(2)}</span>
              <span className="text-neutral-400">χ ≥ {stanje.guard.hi.toFixed(2)}</span>
              <span className="text-neutral-400">μ ∈ [{stanje.guard.muMin.toFixed(2)}, {stanje.guard.muMax.toFixed(2)}]</span>
              <span className="text-neutral-400">ℜ ≤ {stanje.guard.ostanekMax.toFixed(2)}</span>
            </div>
          </div>
        </div>

        {/* ZANKA */}
        <div className="rounded-xl border border-neutral-800 bg-neutral-950 p-4 flex flex-col">
          <h2 className="text-sm font-semibold tracking-widest text-neutral-400 mb-3">ZANKA — pet pregrad</h2>

          {!aktivna && (
            <div className="flex-1 flex items-center justify-center text-center text-neutral-600 text-sm py-8">
              <div>
                <div className="text-4xl mb-3 text-neutral-700">∮</div>
                zanka čaka na δ — predlagaj spremembo
                <br />
                <span className="text-xs">ali vklopi samodejni ∮</span>
              </div>
            </div>
          )}

          {aktivna && (
            <div className="mb-3 rounded-lg border border-neutral-700 bg-neutral-900 p-3">
              <div className="flex items-center justify-between mb-1">
                <span className={`text-xs font-bold tracking-wider ${barvaVrst(aktivna.vrsta)}`}>{aktivna.vrsta}</span>
                <span className="font-mono text-xs text-neutral-500">δ #{aktivna.id} · {aktivna.cilj} {aktivna.delta >= 0 ? "+" : ""}{aktivna.delta.toFixed(2)}</span>
              </div>
              <div className="text-xs text-neutral-300 leading-relaxed">
                {aktivna.izjava ? `«${aktivna.izjava}»` : <span className="text-red-400/80 italic">— nemi prehod, brez izjave —</span>}
              </div>
            </div>
          )}

          <div className="space-y-1.5">
            {VRATA_GLYPHI.map((g, i) => {
              const rez = vrataRez[i];
              const jeAktivna = aktivnaVrata === i;
              const stanjeVrat = rez ? (rez.ok ? "pass" : "fail") : jeAktivna ? "active" : "idle";
              return (
                <div
                  key={i}
                  className={`rounded-lg border px-3 py-2 flex items-center gap-3 transition-all duration-300 ${
                    stanjeVrat === "pass" ? "border-emerald-700 bg-emerald-950/40"
                    : stanjeVrat === "fail" ? "border-red-700 bg-red-950/40"
                    : stanjeVrat === "active" ? "border-amber-500 bg-amber-950/30 scale-[1.02]"
                    : "border-neutral-800 bg-neutral-900/50"
                  }`}
                >
                  <span className={`text-xl w-7 text-center font-semibold ${
                    stanjeVrat === "pass" ? "text-emerald-400" : stanjeVrat === "fail" ? "text-red-400" : stanjeVrat === "active" ? "text-amber-400" : "text-neutral-600"
                  }`}>{g}</span>
                  <div className="flex-1 min-w-0">
                    <div className={`text-xs font-bold tracking-wider ${stanjeVrat === "idle" ? "text-neutral-500" : "text-neutral-200"}`}>{VRATA_IMENA[i]}</div>
                    <div className="text-[11px] text-neutral-500 truncate">
                      {rez ? rez.podatek : jeAktivna ? VRATA_VPRASANJA[i] : VRATA_VPRASANJA[i]}
                    </div>
                  </div>
                  {rez && (
                    <span className={`text-sm font-bold ${rez.ok ? "text-emerald-400" : "text-red-400"}`}>
                      {rez.ok ? "✓" : "✗"}
                    </span>
                  )}
                </div>
              );
            })}
          </div>

          <div className="mt-3 border-t border-neutral-800 pt-3">
            <div className="flex gap-2">
              <button
                onClick={() => korak()}
                disabled={!!aktivna}
                className="flex-1 rounded-lg bg-amber-500/90 hover:bg-amber-400 disabled:opacity-30 disabled:cursor-not-allowed text-black text-sm font-bold py-2 transition-colors"
              >
                ∂ predlagaj δ
              </button>
              <button
                onClick={() => setSamodejno((v) => !v)}
                className={`flex-1 rounded-lg text-sm font-bold py-2 transition-colors ${
                  samodejno ? "bg-emerald-500 text-black hover:bg-emerald-400" : "border border-neutral-700 text-neutral-300 hover:border-neutral-500"
                }`}
              >
                {samodejno ? "∮ samodejno: ON" : "∮ samodejno: OFF"}
              </button>
              <button
                onClick={ponastavi}
                className="rounded-lg border border-neutral-700 text-neutral-400 hover:border-neutral-500 text-sm px-3 py-2 transition-colors"
                title="ponastavi na S₀"
              >
                ↻
              </button>
            </div>
            <div className="mt-3 grid grid-cols-3 gap-2 text-center">
              <div className="rounded-lg bg-neutral-900 py-1.5">
                <div className="font-mono text-lg text-emerald-400 font-bold">{evolucije}</div>
                <div className="text-[10px] text-neutral-500 tracking-wider">⟡ EVOLUCIJE</div>
              </div>
              <div className="rounded-lg bg-neutral-900 py-1.5">
                <div className="font-mono text-lg text-red-400 font-bold">{zavrzene}</div>
                <div className="text-[10px] text-neutral-500 tracking-wider">BRAZGOTINE</div>
              </div>
              <div className="rounded-lg bg-neutral-900 py-1.5">
                <div className="font-mono text-lg text-amber-400 font-bold">{cistost}%</div>
                <div className="text-[10px] text-neutral-500 tracking-wider">ČISTOST</div>
              </div>
            </div>
          </div>
        </div>

        {/* DOKAZ */}
        <div className="rounded-xl border border-neutral-800 bg-neutral-950 p-4 flex flex-col min-h-[400px]">
          <h2 className="text-sm font-semibold tracking-widest text-neutral-400 mb-1">⊢ DOKAZ — append-only sled</h2>
          <p className="text-[11px] text-neutral-600 mb-3">nič se ne izbriše, vse se pretvori — tudi zavrzene spremembe puščajo brazgotino</p>
          <div className="flex-1 overflow-y-auto space-y-2 pr-1 max-h-[560px]">
            {dokazi.map((d) => (
              <div
                key={`${d.n}-${d.cikel}`}
                className={`rounded-lg border p-2.5 text-xs ${
                  d.vrsta === "EVOLUCIJA" ? "border-emerald-800/60 bg-emerald-950/20"
                  : d.vrsta === "ZAVRŽENO" ? "border-red-900/60 bg-red-950/20"
                  : "border-neutral-800 bg-neutral-900/40"
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="font-mono text-neutral-500">
                    {d.vrsta === "GENEZA" ? "S₀" : `S${d.staraV}→S${d.novaV}`}
                  </span>
                  <span className={`font-bold tracking-wider ${
                    d.vrsta === "EVOLUCIJA" ? "text-emerald-400" : d.vrsta === "ZAVRŽENO" ? "text-red-400" : "text-neutral-400"
                  }`}>
                    {d.vrsta === "EVOLUCIJA" ? "⟡ EVOLUCIJA" : d.vrsta === "ZAVRŽENO" ? `✗ ${d.razred}` : "∅ GENEZA"}
                  </span>
                </div>
                <div className="text-neutral-300 leading-snug mb-1">
                  {d.izjava ? `«${d.izjava}»` : <span className="italic text-red-400/70">nemi prehod</span>}
                </div>
                <div className="flex items-center gap-1 font-mono">
                  {d.rezultati.map((r, i) => (
                    <span
                      key={i}
                      className={`text-sm ${r.ok ? "text-emerald-500" : "text-red-500"}`}
                      title={`${r.ime}: ${r.podatek}`}
                    >
                      {r.glyph}
                    </span>
                  ))}
                  {d.razred && (
                    <span className="ml-auto text-[10px] text-neutral-600">{RAZREDI[d.razred]?.opis}</span>
                  )}
                </div>
              </div>
            ))}
          </div>

          {Object.keys(ucenje).length > 0 && (
            <div className="mt-3 border-t border-neutral-800 pt-2">
              <div className="text-[10px] text-neutral-500 tracking-widest mb-1">∮ UČENJE ZANKE (napaka kot kanal)</div>
              <div className="flex flex-wrap gap-1.5">
                {Object.entries(ucenje).map(([razred, st]) => (
                  <span key={razred} className="text-[10px] font-mono rounded bg-neutral-900 border border-neutral-800 px-1.5 py-0.5 text-neutral-400">
                    {razred} ×{st} <span className="text-neutral-600">p↓{(POKVARJENOST[razred] / (1 + st)).toFixed(3)}</span>
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* NOGA */}
      <div className="max-w-6xl mx-auto mt-4 text-[11px] text-neutral-600 leading-relaxed">
        Ta canvas je trener/model zanke — pet pregrad v mikrosvetu. Dejanska zanka (stanje, pravila R1–R5, append-only DOKAZ ledger, izvajalec = pogovor) teče v evo-loop.
        Zanka se nadgrajuje skozi META spremembe (cilj: κ χ μ ℜ pragi) — a le skozi istih pet pregrad: mašina, ki odloča kaj evolvira,
        je sama evolvibilna, a si ne more izbrisati lastnih pogojev. Anomalije (Monster, ~7%) ostanejo — varovalo proti okostenitvi.
        Preverba v telesu ostaja pri tebi: <span className="text-neutral-500">ali zanka diha?</span>
      </div>
    </div>
  );
}