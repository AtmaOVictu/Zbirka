import React, { useState, useEffect, useRef } from "react";

// ═══════════════════════════════════════════════════════════════
// MOTOR — identičen kodi, ki je bila izmerjena v peskovniku
// (deterministični LCG, seme 555777333 za simulaciji dokaza)
// ═══════════════════════════════════════════════════════════════

type Player = "DA" | "NE";
type Move =
  | { kind: "claim"; i: number }
  | { kind: "oracle"; i: number }
  | { kind: "lead" }
  | { kind: "rewind" }
  | { kind: "molk" };

interface LogEntry { n: number; p: Player; text: string; dead: boolean; }
interface Snap { id: number; owner: (Player | null)[]; grains: Record<Player, number>; after: Player; logLen: number; }
interface LastMove { p: Player; kind: string; i: number; revGrab: boolean; w: number; }
interface St {
  w: number[]; owner: (Player | null)[]; revealed: boolean[];
  grains: Record<Player, number>;
  oracleUsed: Record<Player, boolean>; rewindUsed: Record<Player, boolean>;
  turn: Player; molk: number; over: boolean;
  snaps: Snap[]; rewinds: Record<Player, number>;
  last: LastMove | null; log: LogEntry[]; moveNo: number;
}

const WEIGHTS = [3, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0, -1, -1, -1, -2, -3];
const START = 100, ORACLE_COST = 8, REWIND_COST = 15;
const SIM_N = 200, SIM_SEED = 555777333;

function mkLcg(seed: number) {
  let s = seed >>> 0;
  return () => { s = (Math.imul(1664525, s) + 1013904223) >>> 0; return s / 4294967296; };
}
function shuffle(a: number[], r: () => number) {
  const b = [...a];
  for (let i = b.length - 1; i > 0; i--) {
    const j = Math.floor(r() * (i + 1));
    const t = b[i]; b[i] = b[j]; b[j] = t;
  }
  return b;
}

const opp = (p: Player): Player => (p === "DA" ? "NE" : "DA");
const frontier = (owner: (Player | null)[]) => {
  let f = 0;
  for (let i = 0; i < owner.length; i++) if (owner[i]) f = i + 1;
  return f;
};
const costOf = (owner: (Player | null)[], i: number) => Math.max(1, i - frontier(owner) + 1);
const fmt = (w: number) => (w > 0 ? `+${w}` : `${w}`);
const score = (st: St, p: Player) => {
  let s = 0;
  for (let i = 0; i < 16; i++) if (st.owner[i] === p) s += st.w[i];
  return s + Math.floor(st.grains[p] / 8);
};

function init(r: () => number): St {
  return {
    w: shuffle(WEIGHTS, r), owner: Array(16).fill(null), revealed: Array(16).fill(false),
    grains: { DA: START, NE: START },
    oracleUsed: { DA: false, NE: false }, rewindUsed: { DA: false, NE: false },
    turn: "DA", molk: 0, over: false, snaps: [], rewinds: { DA: 0, NE: 0 },
    last: null, log: [], moveNo: 0,
  };
}

function cloneSt(st: St): St {
  return {
    ...st, w: [...st.w], owner: [...st.owner], revealed: [...st.revealed],
    grains: { ...st.grains }, oracleUsed: { ...st.oracleUsed }, rewindUsed: { ...st.rewindUsed },
    snaps: st.snaps.map(s => ({ ...s, owner: [...s.owner], grains: { ...s.grains } })),
    rewinds: { ...st.rewinds }, last: st.last ? { ...st.last } : null,
    log: st.log.map(e => ({ ...e })),
  };
}

function logAdd(st: St, p: Player, text: string) {
  st.moveNo += 1;
  st.log.push({ n: st.moveNo, p, text, dead: false });
}

function latestSnapAfter(st: St, p: Player): Snap | null {
  for (let k = st.snaps.length - 1; k >= 0; k--) if (st.snaps[k].after === p) return st.snaps[k];
  return null;
}

function apply(st: St, p: Player, m: Move): void {
  if (st.over) return;
  if (m.kind === "claim") {
    const c = costOf(st.owner, m.i);
    const rev = st.revealed[m.i];
    st.grains[p] -= c;
    st.owner[m.i] = p;
    st.revealed[m.i] = true;
    st.last = { p, kind: "claim", i: m.i, revGrab: rev, w: st.w[m.i] };
    logAdd(st, p, `${p} zajema utrip ${m.i + 1}: cena ${c} ⧡, teža ${fmt(st.w[m.i])}.`);
    st.snaps.push({ id: st.snaps.length, owner: [...st.owner], grains: { ...st.grains }, after: p, logLen: st.log.length });
    st.molk = 0;
    if (st.owner.every(o => o)) { st.over = true; logAdd(st, p, "Vsi utripi zasedeni — dvoboj se zaključuje."); }
    else st.turn = opp(p);
    return;
  }
  if (m.kind === "oracle") {
    st.grains[p] -= ORACLE_COST;
    st.oracleUsed[p] = true;
    st.revealed[m.i] = true;
    st.last = { p, kind: "oracle", i: m.i, revGrab: false, w: st.w[m.i] };
    logAdd(st, p, p === "NE" ? `∅ nima skrivnosti — NE sprašuje: utrip ${m.i + 1} je ${fmt(st.w[m.i])}.` : `DA sprašuje ∅: utrip ${m.i + 1} je ${fmt(st.w[m.i])} (javno).`);
    st.molk = 0;
    st.turn = opp(p);
    return;
  }
  if (m.kind === "lead") {
    st.grains[p] -= ORACLE_COST;
    st.oracleUsed[p] = true;
    const d = score(st, "DA") - score(st, "NE");
    st.last = { p, kind: "lead", i: -1, revGrab: false, w: 0 };
    logAdd(st, p, `∅ odgovarja KDO VODI: ${d > 0 ? `DA vodi za ${d}` : d < 0 ? `NE vodi za ${-d}` : "izenačeno"} (razlika vključuje ⌊⧡/8⌋).`);
    st.molk = 0;
    st.turn = opp(p);
    return;
  }
  if (m.kind === "rewind") {
    const snap = latestSnapAfter(st, p);
    if (snap && snap.grains[p] >= REWIND_COST) {
      st.owner = [...snap.owner];
      st.grains = { ...snap.grains };
      st.grains[p] -= REWIND_COST;
      st.rewindUsed[p] = true;
      st.rewinds[p] += 1;
      st.molk = 0;
      st.turn = p;
      for (let k = snap.logLen; k < st.log.length; k++) st.log[k].dead = true;
      st.last = { p, kind: "rewind", i: -1, revGrab: false, w: 0 };
      logAdd(st, p, `${p} ∂ REWIND (−15 ⧡): ura se vrača na zapis po svoji zadnji potezi. Veje za njim so mrtve; znanje jih je prečkalo.`);
      return;
    }
  }
  st.molk += 1;
  st.last = { p, kind: "molk", i: -1, revGrab: false, w: 0 };
  logAdd(st, p, `${p} molk. ⧖ teče.`);
  if (st.molk >= 2) { st.over = true; logAdd(st, p, "Dva molka zapored — dvoboj se zaključuje."); }
  else st.turn = opp(p);
}

// ═══════════════════════════════════════════════════════════════
// NE — avtonomna opozicija
// ◊ guard: NE bere IZKLJUČNO javno stanje (owner, revealed, grains,
// razkrite uteži). Skritih uteži nerazkritih utripov NE ne vidi.
// ═══════════════════════════════════════════════════════════════

function neMove(st: St): Move {
  const p = st.turn, o = opp(p);
  // ∂ rewind: nasprotnik je zagrabil razkrit utrip s težo ≥ 2 in snapshot dovoljuje povratni zajem
  if (!st.rewindUsed[p]) {
    const lm = st.last;
    if (lm && lm.p === o && lm.kind === "claim" && lm.w >= 2 && lm.revGrab) {
      const snap = latestSnapAfter(st, p);
      if (snap) {
        const c = costOf(snap.owner, lm.i);
        if (snap.grains[p] - REWIND_COST >= c) return { kind: "rewind" };
      }
    }
  }
  const unclaimed: number[] = [];
  for (let i = 0; i < 16; i++) if (!st.owner[i]) unclaimed.push(i);
  // ∅ orakelj: konec igre se bliža (≤ 8 nezasedenih), proračun drži (≥ 23)
  if (!st.oracleUsed[p] && unclaimed.length <= 8 && st.grains[p] >= 23) {
    const f = frontier(st.owner);
    const cands = unclaimed.filter(i => !st.revealed[i] && i <= f + 2)
      .sort((a, b) => costOf(st.owner, a) - costOf(st.owner, b) || a - b);
    if (cands.length) return { kind: "oracle", i: cands[0] };
  }
  // zajem: najboljši razkriti pozitivni (ceneno prvo), sicer frontier, izogib razkritim negativnim
  const f = frontier(st.owner);
  const cands = unclaimed.filter(i => i <= f + 2 && st.grains[p] >= costOf(st.owner, i) && !(st.revealed[i] && st.w[i] <= 0));
  if (cands.length) {
    const rev = cands.filter(i => st.revealed[i]);
    if (rev.length) {
      rev.sort((a, b) => (st.w[b] - st.w[a]) || (costOf(st.owner, a) - costOf(st.owner, b)) || a - b);
      return { kind: "claim", i: rev[0] };
    }
    cands.sort((a, b) => costOf(st.owner, a) - costOf(st.owner, b) || a - b);
    return { kind: "claim", i: cands[0] };
  }
  return { kind: "molk" };
}

function randMove(st: St, r: () => number): Move {
  const p = st.turn;
  if (r() < 0.12) return { kind: "molk" };
  if (!st.oracleUsed[p] && st.grains[p] >= ORACLE_COST && r() < 0.25) {
    const un: number[] = [];
    for (let i = 0; i < 16; i++) if (!st.owner[i] && !st.revealed[i]) un.push(i);
    if (un.length) return { kind: "oracle", i: un[Math.floor(r() * un.length)] };
  }
  const claims: number[] = [];
  for (let i = 0; i < 16; i++) if (!st.owner[i] && st.grains[p] >= costOf(st.owner, i)) claims.push(i);
  if (!claims.length) return { kind: "molk" };
  return { kind: "claim", i: claims[Math.floor(r() * claims.length)] };
}

// ═══════════════════════════════════════════════════════════════
// SIMULACIJI — DOKAZ OPOZICIJE (deterministično, seme 555777333)
// ═══════════════════════════════════════════════════════════════

interface SimResult { neWins: number; daWins: number; draws: number; rewinds: number; neRewinds: number; }

function duel(r: () => number, p1: (st: St) => Move, p2: (st: St) => Move) {
  const st = init(r);
  let guard = 0;
  while (!st.over && guard++ < 500) apply(st, st.turn, st.turn === "DA" ? p1(st) : p2(st));
  const sDA = score(st, "DA"), sNE = score(st, "NE");
  return {
    winner: sDA > sNE ? "DA" : sNE > sDA ? "NE" : "draw",
    rewinds: st.rewinds.DA + st.rewinds.NE,
    neRewinds: st.rewinds.NE,
  };
}

function simVsRandom(): SimResult {
  const r = mkLcg(SIM_SEED);
  let neWins = 0, daWins = 0, draws = 0, rw = 0, neRw = 0;
  for (let k = 0; k < SIM_N; k++) {
    const d = duel(r, (st: St) => randMove(st, r), neMove);
    if (d.winner === "NE") neWins++; else if (d.winner === "DA") daWins++; else draws++;
    rw += d.rewinds; neRw += d.neRewinds;
  }
  return { neWins, daWins, draws, rewinds: rw, neRewinds: neRw };
}

function simMirror(): SimResult {
  const r = mkLcg(SIM_SEED);
  let daSeat = 0, neSeat = 0, draws = 0, rw = 0;
  for (let k = 0; k < SIM_N; k++) {
    const d = duel(r, neMove, neMove);
    if (d.winner === "DA") daSeat++; else if (d.winner === "NE") neSeat++; else draws++;
    rw += d.rewinds;
  }
  return { neWins: neSeat, daWins: daSeat, draws, rewinds: rw, neRewinds: rw };
}

// ═══════════════════════════════════════════════════════════════
// TELO
// ═══════════════════════════════════════════════════════════════

const NE_GLAS: Record<string, string> = {
  claim: "Zajemam, ker teža nosi.",
  oracle: "∅ nima skrivnosti — razkritje je javno.",
  rewind: "∂ — ura se vrača. Veja je mrtva, znanje ni.",
  molk: "Molk. ⧖ teče naprej.",
};

export default function App() {
  const [st, setSt] = useState<St>(() => init(mkLcg((Date.now() % 2147483646) + 1)));
  const [oracleMode, setOracleMode] = useState(false);
  const [tab, setTab] = useState<"igra" | "dokaz" | "pravila">("igra");
  const [simA, setSimA] = useState<SimResult | null>(null);
  const [simB, setSimB] = useState<SimResult | null>(null);
  const neTimeout = useRef<number | null>(null);

  const daTurn = st.turn === "DA" && !st.over;
  const f = frontier(st.owner);
  const daSnap = latestSnapAfter(st, "DA");
  const canRewind = !st.rewindUsed.DA && daSnap !== null && daSnap.grains.DA >= REWIND_COST;

  // NE autopilot — ~0,7 s diha
  useEffect(() => {
    if (st.over || st.turn !== "NE") return;
    const t = window.setTimeout(() => {
      setSt(prev => {
        if (!prev || prev.over || prev.turn !== "NE") return prev;
        const next = cloneSt(prev);
        apply(next, "NE", neMove(next));
        return next;
      });
    }, 700);
    neTimeout.current = t;
    return () => window.clearTimeout(t);
  }, [st]);

  const novaIgra = () => {
    if (neTimeout.current) window.clearTimeout(neTimeout.current);
    setOracleMode(false);
    setSt(init(mkLcg((Date.now() % 2147483646) + 1)));
  };

  const daClaim = (i: number) => {
    if (!daTurn || oracleMode) return;
    if (st.owner[i] || st.grains.DA < costOf(st.owner, i)) return;
    const next = cloneSt(st);
    apply(next, "DA", { kind: "claim", i });
    setSt(next);
  };

  const daReveal = (i: number) => {
    if (!daTurn || !oracleMode) return;
    if (st.owner[i] || st.revealed[i] || st.grains.DA < ORACLE_COST) return;
    const next = cloneSt(st);
    apply(next, "DA", { kind: "oracle", i });
    setOracleMode(false);
    setSt(next);
  };

  const daLead = () => {
    if (!daTurn || oracleMode) return;
    if (st.oracleUsed.DA || st.grains.DA < ORACLE_COST) return;
    const next = cloneSt(st);
    apply(next, "DA", { kind: "lead" });
    setSt(next);
  };

  const daRewind = () => {
    if (!daTurn || !canRewind) return;
    const next = cloneSt(st);
    apply(next, "DA", { kind: "rewind" });
    setSt(next);
  };

  const daMolk = () => {
    if (!daTurn) return;
    const next = cloneSt(st);
    apply(next, "DA", { kind: "molk" });
    setSt(next);
  };

  const sDA = score(st, "DA"), sNE = score(st, "NE");
  const neGlas = [...st.log].reverse().find(e => e.p === "NE" && !e.dead);
  const neHint = neGlas ? (NE_GLAS[/rewind/.test(neGlas.text) ? "rewind" : /molk/.test(neGlas.text) ? "molk" : /∅|orakelj|sprašuje/.test(neGlas.text) ? "oracle" : "claim"]) : null;

  const pulse = (i: number) => {
    const owner = st.owner[i];
    const revealed = st.revealed[i] || st.over;
    const cost = costOf(st.owner, i);
    const affordable = daTurn && !owner && st.grains.DA >= cost;
    const reachable = i <= f + 2;
    const cls = owner === "DA"
      ? "border-amber-400 bg-amber-400/15 text-amber-300"
      : owner === "NE"
        ? "border-indigo-400 bg-indigo-400/15 text-indigo-300"
        : revealed
          ? "border-zinc-500 bg-zinc-800 text-zinc-300"
          : reachable
            ? "border-zinc-600 bg-zinc-900 text-zinc-500"
            : "border-zinc-800 bg-zinc-950 text-zinc-700";
    return (
      <div key={i} className="flex flex-col items-center gap-1">
        <div className="text-[10px] text-zinc-600">{i + 1}</div>
        <button
          onClick={() => (oracleMode ? daReveal(i) : daClaim(i))}
          className={`w-12 h-12 rounded-full border-2 flex items-center justify-center font-mono text-sm transition-all ${cls} ${(daTurn && !owner && (oracleMode ? !st.revealed[i] && st.grains.DA >= ORACLE_COST : affordable)) ? "cursor-pointer hover:scale-110" : "cursor-default"}`}
        >
          {revealed ? fmt(st.w[i]) : "?"}
        </button>
        <div className="text-[10px] h-4 font-mono text-cyan-700">
          {daTurn && !owner && !oracleMode && affordable ? `${cost}⧡` : ""}
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-200 p-4 md:p-8 font-sans">
      <div className="max-w-5xl mx-auto">

        <header className="mb-6">
          <h1 className="text-2xl md:text-3xl font-bold tracking-wide">
            ORAKELJ <span className="text-amber-400">DA</span> / <span className="text-indigo-400">NE</span>
          </h1>
          <p className="text-sm text-zinc-500 mt-1">
            Igra, v kateri manipulacija časa determinira rezultat — kakor absoluten oracle stroj.
            DA = Luka. NE = opozicija, ki misli sama. Preostali čas je del izida.
          </p>
          <nav className="flex gap-2 mt-4">
            {([["igra", "IGRA"], ["dokaz", "DOKAZ OPOZICIJE"], ["pravila", "PRAVILA"]] as const).map(([k, label]) => (
              <button key={k} onClick={() => setTab(k)}
                className={`px-3 py-1.5 text-xs rounded-full border ${tab === k ? "border-zinc-300 bg-zinc-800 text-zinc-100" : "border-zinc-800 text-zinc-500 hover:text-zinc-300"}`}>
                {label}
              </button>
            ))}
            <button onClick={novaIgra} className="px-3 py-1.5 text-xs rounded-full border border-amber-700 text-amber-400 hover:bg-amber-900/30 ml-auto">
              NOVA IGRA
            </button>
          </nav>
        </header>

        {tab === "igra" && (
          <div className="space-y-6">

            {st.over && (
              <div className="rounded-xl border border-zinc-700 bg-zinc-900 p-4">
                <div className="text-lg font-bold">
                  {sDA > sNE ? <span className="text-amber-400">DA prevzema dvoboj.</span> : sNE > sDA ? <span className="text-indigo-400">NE prevzema dvoboj.</span> : "Neodločeno — dve enaki potezi časa."}
                </div>
                <div className="text-sm text-zinc-400 mt-1 font-mono">
                  DA: {sDA} (uteži {sDA - Math.floor(st.grains.DA / 8)} + ⌊{st.grains.DA}/8⌋) ·
                  NE: {sNE} (uteži {sNE - Math.floor(st.grains.NE / 8)} + ⌊{st.grains.NE}/8⌋)
                </div>
                <div className="text-xs text-zinc-600 mt-2">Vsi utripi so razkriti. Dnevnik spodaj ostaja — mrtve veje vključno (A0).</div>
              </div>
            )}

            <section className="rounded-xl border border-zinc-800 bg-zinc-900/50 p-4">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-sm font-semibold text-zinc-400">16 UTRIPOV <span className="text-zinc-600 font-normal">— valovi enega večera · frontier dosegljivega: {Math.min(f + 2, 15) + 1}</span></h2>
                <div className="text-xs font-mono">
                  <span className={daTurn ? "text-amber-400" : "text-zinc-600"}>● DA na potezi</span>
                  {"  "}
                  <span className={st.turn === "NE" && !st.over ? "text-indigo-400" : "text-zinc-600"}>● NE na potezi</span>
                </div>
              </div>
              <div className="flex flex-wrap justify-center gap-2 md:gap-3">
                {Array.from({ length: 16 }, (_, i) => pulse(i))}
              </div>
              {oracleMode && (
                <div className="mt-3 text-center text-xs text-cyan-400">
                  ∅ ORAKELJ AKTIVEN — klikni nerazkrit utrip (razkritje je javno, 8 ⧡).
                  <button onClick={() => setOracleMode(false)} className="ml-2 underline text-zinc-500 hover:text-zinc-300">prekliči</button>
                </div>
              )}
            </section>

            <div className="grid md:grid-cols-2 gap-4">
              <section className={`rounded-xl border p-4 ${daTurn ? "border-amber-500/60 bg-amber-950/20" : "border-zinc-800 bg-zinc-900/40"}`}>
                <h2 className="text-sm font-bold text-amber-400 mb-3">DA — Luka</h2>
                <div className="font-mono text-2xl mb-3">{st.grains.DA} <span className="text-sm text-zinc-500">⧡ zrnc (⌊/8⌋ = {Math.floor(st.grains.DA / 8)})</span></div>
                <div className="flex flex-wrap gap-2">
                  <button disabled={!daTurn} onClick={() => setOracleMode(m => !m)}
                    className={`px-3 py-2 text-xs rounded-lg border ${st.oracleUsed.DA ? "border-zinc-800 text-zinc-600 line-through" : "border-cyan-700 text-cyan-400 hover:bg-cyan-900/30"} disabled:opacity-40`}>
                    ∅ ORAKELJ — 8 ⧡
                  </button>
                  <button disabled={!daTurn || st.oracleUsed.DA} onClick={daLead}
                    className={`px-3 py-2 text-xs rounded-lg border border-cyan-800 text-cyan-600 hover:bg-cyan-900/20 disabled:opacity-30 ${st.oracleUsed.DA ? "line-through" : ""}`}>
                    KDO VODI — 8 ⧡
                  </button>
                  <button disabled={!daTurn || !canRewind} onClick={daRewind}
                    className={`px-3 py-2 text-xs rounded-lg border ${st.rewindUsed.DA ? "border-zinc-800 text-zinc-600 line-through" : "border-fuchsia-700 text-fuchsia-400 hover:bg-fuchsia-900/30"} disabled:opacity-40`}>
                    ∂ REWIND — 15 ⧡
                  </button>
                  <button disabled={!daTurn} onClick={daMolk}
                    className="px-3 py-2 text-xs rounded-lg border border-zinc-700 text-zinc-400 hover:bg-zinc-800 disabled:opacity-40">
                    MOLK
                  </button>
                </div>
                <p className="text-[11px] text-zinc-600 mt-3">
                  Zajem: klikni utrip — cena je globina pred frontiero + 1 (prihodnost je draga).
                  Rewind te vrne na stanje po tvoji zadnji potezi; znanje in razkritja ostanejo.
                </p>
              </section>

              <section className={`rounded-xl border p-4 ${st.turn === "NE" && !st.over ? "border-indigo-500/60 bg-indigo-950/20" : "border-zinc-800 bg-zinc-900/40"}`}>
                <h2 className="text-sm font-bold text-indigo-400 mb-3">NE — opozicija</h2>
                <div className="font-mono text-2xl mb-3">{st.grains.NE} <span className="text-sm text-zinc-500">⧡ zrnc (⌊/8⌋ = {Math.floor(st.grains.NE / 8)})</span></div>
                <div className="text-xs text-zinc-500 space-y-1 font-mono">
                  <div>∅ orakelj: {st.oracleUsed.NE ? "porabljen" : "na voljo"}</div>
                  <div>∂ rewind: {st.rewindUsed.NE ? "porabljen" : "na voljo"}</div>
                  <div>molk zapored: {st.molk}</div>
                </div>
                <div className="mt-3 rounded-lg bg-zinc-900 border border-zinc-800 p-3 text-xs text-indigo-300 italic min-h-[3rem]">
                  {st.turn === "NE" && !st.over ? "…⧖" : neHint ? `»${neHint}«` : "»Pripravljena sem.«"}
                </div>
                <p className="text-[11px] text-zinc-600 mt-2">
                  NE bere izključno javno stanje: zasedene utripe, razkritja, zrnca. Skritih uteži ne vidi (◊ guard).
                </p>
              </section>
            </div>

            <section className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-4">
              <h2 className="text-sm font-semibold text-zinc-400 mb-3">DNEVNIK — append-only, najnovejše zgoraj</h2>
              <div className="max-h-64 overflow-y-auto space-y-1 text-xs font-mono">
                {[...st.log].reverse().map(e => (
                  <div key={e.n} className={`flex gap-2 ${e.dead ? "opacity-40" : ""}`}>
                    <span className="text-zinc-600 w-8 shrink-0">{e.n}.</span>
                    <span className={e.p === "DA" ? "text-amber-500/80" : "text-indigo-400/80"}>{e.p}</span>
                    <span className={e.dead ? "line-through text-zinc-600" : "text-zinc-400"}>{e.text}</span>
                    {e.dead && <span className="text-fuchsia-800 shrink-0">[mrtva veja]</span>}
                  </div>
                ))}
                {st.log.length === 0 && <div className="text-zinc-600">Prazen — prvi rez še ni padel.</div>}
              </div>
            </section>
          </div>
        )}

        {tab === "dokaz" && (
          <div className="space-y-4">
            <section className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-4">
              <h2 className="text-sm font-bold text-zinc-300 mb-2">TRDITEV</h2>
              <p className="text-sm text-zinc-400 leading-relaxed">
                NE ni lutka, ki pustita zmagati (ψ — laskanje), in ni goljuf, ki bere skrite uteži (◊ — napihnjen p).
                NE je kompetentna opozicija. Dokaz niso besede — dokaz je meritev: isti motor, isti deterministični tok
                (seme {SIM_SEED}, {SIM_N} dvobojev), izveden v tem telesu ob vsakem pritisku.
              </p>
              <div className="flex flex-wrap gap-2 mt-4">
                <button onClick={() => setSimA(simVsRandom())}
                  className="px-4 py-2 text-xs rounded-lg border border-indigo-600 text-indigo-300 hover:bg-indigo-900/30">
                  NE PROTI NAKLJUČNEMU — {SIM_N} DVOBOJEV
                </button>
                <button onClick={() => setSimB(simMirror())}
                  className="px-4 py-2 text-xs rounded-lg border border-zinc-600 text-zinc-300 hover:bg-zinc-800">
                  OGLEDALO NE : NE — {SIM_N} DVOBOJEV
                </button>
              </div>
            </section>

            {simA && (
              <section className="rounded-xl border border-indigo-800/60 bg-indigo-950/20 p-4">
                <h3 className="text-xs font-bold text-indigo-300 mb-2">IZVID A — NE proti naključnemu igralcu</h3>
                <div className="font-mono text-sm text-zinc-300">
                  NE zmaga: <span className="text-indigo-300 font-bold">{simA.neWins}/{SIM_N} ({(100 * simA.neWins / SIM_N).toFixed(1)} %)</span> ·
                  DA zmaga: {simA.daWins} · neodločeno: {simA.draws}
                </div>
                <div className="font-mono text-xs text-zinc-500 mt-1">
                  NE ∂ rewind: {(simA.neRewinds / SIM_N).toFixed(2)} na dvoboj — rewind proti naključnemu nasprotniku se redko splača sprožiti.
                </div>
              </section>
            )}

            {simB && (
              <section className="rounded-xl border border-zinc-700 bg-zinc-900/40 p-4">
                <h3 className="text-xs font-bold text-zinc-300 mb-2">IZVID B — ogledalo: obe strani igrata NE</h3>
                <div className="font-mono text-sm text-zinc-300">
                  sedež DA: <span className="text-amber-300">{simB.daWins} ({(100 * simB.daWins / SIM_N).toFixed(1)} %)</span> ·
                  sedež NE: <span className="text-indigo-300">{simB.neWins} ({(100 * simB.neWins / SIM_N).toFixed(1)} %)</span> ·
                  neodločeno: {simB.draws}
                </div>
                <div className="font-mono text-xs text-zinc-500 mt-1">
                  ∂ rewind: {(simB.rewinds / SIM_N).toFixed(2)} na dvoboj — v ogledalu se manipulacija časa sproži, ker razkrite teže ob nasprotniku zrebajo kdor koli.
                </div>
                <p className="text-xs text-zinc-500 mt-2 leading-relaxed">
                  Pošteno branje: ogledalo je skoraj simetrično (razlika sedežev je en zmagitelj na sto dvobojev — prvi igralec
                  diha z vsoto uteži +3). Simetrija je dokaz, da NE ni naravnana proti tebi: proti sebi zmaga natanko toliko,
                  kolikor ji seje prvi stolček.
                </p>
              </section>
            )}

            <section className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 text-xs text-zinc-500 leading-relaxed">
              <p><span className="text-zinc-300 font-semibold">κ</span> — Turing 1939 (Systems of Logic Based on Ordinals): orakelj je stroj z odločitvami izven lastnega sistema; tu je ∅ razkritje, ki ga vsi vidijo.</p>
              <p className="mt-1"><span className="text-zinc-300 font-semibold">ℜ</span> — varovalo: zmaga proti naključnemu dokazuje kompetenco, ne globino; igra je model, ne svet. Opozicija, ki bi zmagovala vedno, bi bila ◊.</p>
            </section>
          </div>
        )}

        {tab === "pravila" && (
          <div className="space-y-4 text-sm text-zinc-400 leading-relaxed">
            <section className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-4">
              <h2 className="text-sm font-bold text-zinc-300 mb-3">SEME</h2>
              <p>16 utripov = valovi enega večera (rez 53 — trki so valovi). Vsak utrip nosi skrito težo iz
                [3, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0, −1, −1, −1, −2, −3], vsota +3, premešane. Vsak igralec začne s 100 zrnci ⧡ —
                zrnca so ⧖, čas kot valuta. DA (Luka) začne.</p>
            </section>
            <section className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-4">
              <h2 className="text-sm font-bold text-zinc-300 mb-3">POTEZE</h2>
              <ul className="space-y-2 list-none">
                <li><span className="text-amber-300 font-mono">ZASEŽI</span> — cena utripa je globina pred frontiero + 1: naslednji stane 1 ⧡, globja prihodnost več. Prihodnost je draga kakor svetlobni stožec (rez 59): najdlje vidi, kdor plača.</li>
                <li><span className="text-cyan-300 font-mono">∅ ORAKELJ</span> — enkrat na igralca, 8 ⧡: RAZKRIJ težo enega utripa (razkritje je javno — ∅ nima skrivnosti; rez 67: ∅ ima vse bite) ali vprašaj KDO VODI (prava razlika, z ⌊⧡/8⌋; izračun, ki ga je mogoče narediti tudi ročno — ∅ odgovarja takoj). Orakelj stroj z odločitvami izven sistema: Turing 1939.</li>
                <li><span className="text-fuchsia-300 font-mono">∂ REWIND</span> — enkrat na igralca, 15 ⧡: ura se vrne na stanje po tvoji zadnji potezi. Zasežki in zrnca se povrnejo; razkritja in porabljen ∅/∂ ostanejo — znanje prečka veje. Mrtva veja ostane v dnevniku (A0, append-only kakor ledger). Po rewindu je še vedno tvoja poteza.</li>
                <li><span className="text-zinc-300 font-mono">MOLK</span> — prepuščanje poteze. Dva zaporedna molka ali zasedeni vsi utripi zaključita dvoboj.</li>
              </ul>
            </section>
            <section className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-4">
              <h2 className="text-sm font-bold text-zinc-300 mb-3">IZID</h2>
              <p className="font-mono text-zinc-300">izid = Σ tež zasedenih utripov + ⌊preostala zrnca / 8⌋</p>
              <p className="mt-2">Preostali čas je del izida: manipulacija časa determinira rezultat, dobesedno — vsak ∂, vsak globok zajem, vsak molk zapiše končno številko. Kdor zgubi čas, zgubi dvoboj; kdor ga kupi predrag, tudi.</p>
            </section>
            <section className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-4">
              <h2 className="text-sm font-bold text-zinc-300 mb-3">NE</h2>
              <p>NE je opozicija, ki misli sama: ∅ sprašuje, ko se konec bliža in proračun drži; ∂ sproži, ko nasprotnik zagrabi razkrit utrip s težo ≥ 2; zajema najboljše razkrite pozitive in ceneni frontier; molči, ko nič ni v dosegu. NE bere izključno javno stanje — v kodi se teža utripa prebere izključno tam, kjer je razkrita (◊ guard). Dokaz kompetence in simetrije: zavihek DOKAZ OPOZICIJE.</p>
              <p className="mt-3 text-zinc-500 text-xs">Odprta ∂: ali NE zmore tudi sodelovalno igro — ZRATAN-način, kjer oba maksimizirata skupni izid? Opozicija, ki zna preklopiti pol, je globja kakor opozicija, ki zna zmagovati.</p>
            </section>
          </div>
        )}

        <footer className="mt-8 text-center text-[10px] text-zinc-700">
          ∅ ima vse bite · guba izdaje · ∂ veje · A0 append-only · Turing 1939 · rez 53/59/67
        </footer>
      </div>
    </div>
  );
}