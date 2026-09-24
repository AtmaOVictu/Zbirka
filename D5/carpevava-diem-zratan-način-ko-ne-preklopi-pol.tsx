import React, { useState, useEffect, useRef } from "react";

// ═══════════════════════════════════════════════════════════════
// MOTOR — isti zakoni kakor orakelj-da-ne (rez 75), ena razlika:
// ZRATAN-način: skupni izid; ∂ razveljavi LASTNO potezo (Neikos
// obrnjen vase); KDO VODI je umrl — v sodelovanju stanje ni skrivnost.
// Meritve: deterministični LCG, seme 555777333, 200 iger (isti
// razporedi za vse tri meritve — primerjava po parih).
// ═══════════════════════════════════════════════════════════════

type Player = "DA" | "NE";
type Move =
  | { kind: "claim"; i: number }
  | { kind: "oracle"; i: number }
  | { kind: "rewind" }
  | { kind: "molk" };

interface LogEntry { n: number; p: Player; text: string; dead: boolean; }
interface Snap { id: number; owner: (Player | null)[]; grains: Record<Player, number>; after: Player; logLen: number; }
interface LastClaim { i: number; w: number; revGrab: boolean; preLen: number; }
interface LastMove { p: Player; kind: string; i: number; revGrab: boolean; w: number; }
interface St {
  w: number[]; owner: (Player | null)[]; revealed: boolean[];
  grains: Record<Player, number>;
  oracleUsed: Record<Player, boolean>; rewindUsed: Record<Player, boolean>;
  turn: Player; molk: number; over: boolean;
  snaps: Snap[]; rewinds: Record<Player, number>;
  log: LogEntry[]; moveNo: number;
  lastClaim: Record<Player, LastClaim | null>;
  last: LastMove | null;
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
const jointOf = (st: St) => {
  let s = 0;
  for (let i = 0; i < 16; i++) if (st.owner[i]) s += st.w[i];
  return s + Math.floor((st.grains.DA + st.grains.NE) / 8);
};

function initW(r: () => number): St {
  return {
    w: shuffle(WEIGHTS, r), owner: Array(16).fill(null), revealed: Array(16).fill(false),
    grains: { DA: START, NE: START },
    oracleUsed: { DA: false, NE: false }, rewindUsed: { DA: false, NE: false },
    turn: "DA", molk: 0, over: false, snaps: [], rewinds: { DA: 0, NE: 0 },
    log: [], moveNo: 0, lastClaim: { DA: null, NE: null }, last: null,
  };
}
function cloneSt(st: St): St {
  return {
    ...st, w: [...st.w], owner: [...st.owner], revealed: [...st.revealed],
    grains: { ...st.grains }, oracleUsed: { ...st.oracleUsed }, rewindUsed: { ...st.rewindUsed },
    snaps: st.snaps.map(s => ({ ...s, owner: [...s.owner], grains: { ...s.grains } })),
    rewinds: { ...st.rewinds }, log: st.log.map(e => ({ ...e })),
    lastClaim: { DA: st.lastClaim.DA ? { ...st.lastClaim.DA } : null, NE: st.lastClaim.NE ? { ...st.lastClaim.NE } : null },
    last: st.last ? { ...st.last } : null,
  };
}
function logAdd(st: St, p: Player, text: string) {
  st.moveNo += 1;
  st.log.push({ n: st.moveNo, p, text, dead: false });
}

function apply(st: St, p: Player, m: Move, coop = true): void {
  if (st.over) return;
  if (m.kind === "claim") {
    const c = costOf(st.owner, m.i);
    const rev = st.revealed[m.i];
    st.grains[p] -= c;
    st.owner[m.i] = p;
    st.revealed[m.i] = true;
    st.lastClaim[p] = { i: m.i, w: st.w[m.i], revGrab: rev, preLen: st.snaps.length };
    st.last = { p, kind: "claim", i: m.i, revGrab: rev, w: st.w[m.i] };
    logAdd(st, p, `Zajemava — ${p}: utrip ${m.i + 1}, cena ${c} ⧡, teža ${fmt(st.w[m.i])}.`);
    st.snaps.push({ id: st.snaps.length, owner: [...st.owner], grains: { ...st.grains }, after: p, logLen: st.log.length });
    st.molk = 0;
    if (st.owner.every(o => o)) { st.over = true; logAdd(st, p, "Vsi utripi zasedeni — dan se oddaja."); }
    else st.turn = opp(p);
    return;
  }
  if (m.kind === "oracle") {
    st.grains[p] -= ORACLE_COST;
    st.oracleUsed[p] = true;
    st.revealed[m.i] = true;
    st.last = { p, kind: "oracle", i: m.i, revGrab: false, w: st.w[m.i] };
    logAdd(st, p, `∅ nima skrivnosti — ${p} sprašuje za oba: utrip ${m.i + 1} je ${fmt(st.w[m.i])}.`);
    st.molk = 0;
    st.turn = opp(p);
    return;
  }
  if (m.kind === "rewind") {
    if (coop) {
      // ZRATAN: povratek na trenutek PRED lastno zadnjo potezo (samo-popravljanje)
      const lc = st.lastClaim[p];
      if (lc) {
        let tgtOwner: (Player | null)[];
        let tgtGrains: Record<Player, number>;
        if (lc.preLen === 0) { tgtOwner = Array(16).fill(null); tgtGrains = { DA: START, NE: START }; }
        else { tgtOwner = [...st.snaps[lc.preLen - 1].owner]; tgtGrains = { ...st.snaps[lc.preLen - 1].grains }; }
        if (tgtGrains[p] >= REWIND_COST) {
          const deadFrom = lc.preLen === 0 ? 0 : st.snaps[lc.preLen - 1].logLen;
          st.owner = tgtOwner;
          st.grains = tgtGrains;
          st.grains[p] -= REWIND_COST;
          st.rewindUsed[p] = true;
          st.rewinds[p] += 1;
          st.molk = 0;
          st.turn = p;
          for (let k = deadFrom; k < st.log.length; k++) st.log[k].dead = true;
          st.lastClaim[p] = null;
          st.last = { p, kind: "rewind", i: -1, revGrab: false, w: 0 };
          logAdd(st, p, `${p} ∂ SAMO-POPRAVLJANJE (−15 ⧡): ura se vrača pred lastno potezo. Veja je mrtva; znanje je naše.`);
          return;
        }
      }
    } else {
      // VOJNA (za simulacijo ogledala iz reza 75): povratek na svoj zadnji zapis — prekliče nasprotnikov zaseg
      for (let k = st.snaps.length - 1; k >= 0; k--) {
        if (st.snaps[k].after === p) {
          const s = st.snaps[k];
          if (s.grains[p] >= REWIND_COST) {
            st.owner = [...s.owner];
            st.grains = { ...s.grains };
            st.grains[p] -= REWIND_COST;
            st.rewindUsed[p] = true;
            st.rewinds[p] += 1;
            st.molk = 0;
            st.turn = p;
            st.last = { p, kind: "rewind", i: -1, revGrab: false, w: 0 };
            st.lastClaim[p] = null;
            return;
          }
          break;
        }
      }
    }
  }
  st.molk += 1;
  st.last = { p, kind: "molk", i: -1, revGrab: false, w: 0 };
  logAdd(st, p, `${p} molk. ⧖ teče za oba.`);
  if (st.molk >= 2) { st.over = true; logAdd(st, p, "Dva molka zapored — dan se oddaja."); }
  else st.turn = opp(p);
}

// ═══════════════════════════════════════════════════════════════
// NE v ZRATAN-načinu — pol preklopljen (opozicija → sodelovanje)
// ◊ guard: NE bere izključno javno stanje. Pogojni EV neznanega
// utripa je izpeljan iz javnih konstant: Σ vseh uteži = +3.
// ═══════════════════════════════════════════════════════════════

function evUnknown(st: St): number {
  let sKnown = 0, cKnown = 0;
  for (let i = 0; i < 16; i++) if (st.revealed[i]) { sKnown += st.w[i]; cKnown++; }
  const nUn = 16 - cKnown;
  if (nUn === 0) return 0;
  return (3 - sKnown) / nUn;
}

function coopMove(st: St, noO = false): Move {
  const p = st.turn;
  // ∂ samo-popravljanje: lastna slepa poteza ≤ −2 (Neikos obrnjen vase)
  if (!st.rewindUsed[p]) {
    const lc = st.lastClaim[p];
    if (lc && !lc.revGrab && lc.w <= -2) {
      const ok = lc.preLen === 0 ? START >= REWIND_COST : st.snaps[lc.preLen - 1].grains[p] >= REWIND_COST;
      if (ok) return { kind: "rewind" };
    }
  }
  const unclaimed: number[] = [];
  for (let i = 0; i < 16; i++) if (!st.owner[i]) unclaimed.push(i);
  // ∅ skupna razkritja: konec dneva, proračun drži (noO: meritev vrednosti ∅ — igra brez oraklja)
  if (!noO && !st.oracleUsed[p] && unclaimed.length <= 8 && st.grains[p] >= 23) {
    const f = frontier(st.owner);
    const cands = unclaimed.filter(i => !st.revealed[i] && i <= f + 2)
      .sort((a, b) => costOf(st.owner, a) - costOf(st.owner, b) || a - b);
    if (cands.length) return { kind: "oracle", i: cands[0] };
  }
  const f = frontier(st.owner);
  // razkriti pozitivni kjer koli, če teža nosi ceno (8w − c > 0)
  const pos = unclaimed.filter(i => st.revealed[i] && st.w[i] >= 1 && st.grains[p] >= costOf(st.owner, i) && st.w[i] * 8 - costOf(st.owner, i) > 0);
  if (pos.length) {
    pos.sort((a, b) => (st.w[b] * 8 - costOf(st.owner, b)) - (st.w[a] * 8 - costOf(st.owner, a)) || a - b);
    return { kind: "claim", i: pos[0] };
  }
  // razkrita ničla na ceni 1 — obiranje frontierje za kasnejše
  const zer = unclaimed.filter(i => st.revealed[i] && st.w[i] === 0 && costOf(st.owner, i) === 1 && i < 15);
  if (zer.length) return { kind: "claim", i: zer[0] };
  // prilagodljivo obiranje neznanega: javni EV · 8 > cena
  const ev = evUnknown(st);
  const unk = unclaimed.filter(i => !st.revealed[i] && st.grains[p] >= costOf(st.owner, i) && ev * 8 - costOf(st.owner, i) > 0);
  if (unk.length) { unk.sort((a, b) => costOf(st.owner, a) - costOf(st.owner, b) || a - b); return { kind: "claim", i: unk[0] }; }
  return { kind: "molk" };
}

// Tekmovalna NE (rez 75) — vojni ∂, za simulacijo ogledala M1.
// ∂ prekliče nasprotnikov zaseg razritega utripa s težo ≥ 2,
// če si ga po povratku lahko ponovno privošči (zaloga > cena + 15 ⧡).
function neComp(st: St): Move {
  const p = st.turn;
  if (!st.rewindUsed[p] && st.last && st.last.p !== p && st.last.kind === "claim" && st.last.revGrab && st.last.w >= 2) {
    let snap: Snap | null = null;
    for (let k = st.snaps.length - 1; k >= 0; k--) if (st.snaps[k].after === p) { snap = st.snaps[k]; break; }
    if (snap && snap.grains[p] - REWIND_COST >= costOf(snap.owner, st.last.i)) return { kind: "rewind" };
  }
  const f0 = frontier(st.owner);
  const unc: number[] = []; for (let i = 0; i < 16; i++) if (!st.owner[i]) unc.push(i);
  if (!st.oracleUsed[p] && unc.length <= 8 && st.grains[p] >= 23) {
    const c2 = unc.filter(i => !st.revealed[i] && i <= f0 + 2).sort((a, b) => costOf(st.owner, a) - costOf(st.owner, b) || a - b);
    if (c2.length) return { kind: "oracle", i: c2[0] };
  }
  const cands = unc.filter(i => i <= f0 + 2 && st.grains[p] >= costOf(st.owner, i) && !(st.revealed[i] && st.w[i] <= 0));
  if (cands.length) {
    const rev = cands.filter(i => st.revealed[i]);
    if (rev.length) { rev.sort((a, b) => (st.w[b] - st.w[a]) || (costOf(st.owner, a) - costOf(st.owner, b)) || a - b); return { kind: "claim", i: rev[0] }; }
    cands.sort((a, b) => costOf(st.owner, a) - costOf(st.owner, b) || a - b);
    return { kind: "claim", i: cands[0] };
  }
  return { kind: "molk" };
}

// ═══════════════════════════════════════════════════════════════
// SIMULACIJE — DOKAZ SODELOVANJA (isti razporedi, primerjava po parih)
// ═══════════════════════════════════════════════════════════════

function simAll() {
  const rL = mkLcg(SIM_SEED);
  const layouts: number[][] = [];
  for (let k = 0; k < SIM_N; k++) layouts.push(shuffle(WEIGHTS, rL));
  let jComp = 0, jCoop = 0, jBound = 0, coopBolje = 0, compBolje = 0, enako = 0, rw = 0;
  for (let k = 0; k < SIM_N; k++) {
    const w = layouts[k];
    // tekmovalno ogledalo — polna NE iz reza 75 (z vojnim ∂)
    const st = initW(() => 0); st.w = [...w];
    let guard = 0;
    while (!st.over && guard++ < 500) apply(st, st.turn, neComp(st), false);
    jComp += jointOf(st);
    // ZRATAN ogledalo
    const st2 = initW(() => 0); st2.w = [...w];
    guard = 0;
    while (!st2.over && guard++ < 500) apply(st2, st2.turn, coopMove(st2));
    jCoop += jointOf(st2); rw += st2.rewinds.DA + st2.rewinds.NE;
    if (jointOf(st2) > jointOf(st)) coopBolje++; else if (jointOf(st2) < jointOf(st)) compBolje++; else enako++;
    // meja: popolno znanje, DP (zaloga 25 + optimalni plan, linearna aproksimacija)
    const memo = new Map<string, number>();
    const rec = (i: number, f: number): number => {
      if (i >= 16) return 0;
      const key = i + "," + f;
      const m0 = memo.get(key); if (m0 !== undefined) return m0;
      const skip = rec(i + 1, f);
      const c = Math.max(1, i - f + 1);
      const take = w[i] * 8 - c + rec(i + 1, i + 1);
      const best = Math.max(skip, take);
      memo.set(key, best); return best;
    };
    jBound += 25 + rec(0, 0) / 8;
  }
  return {
    comp: jComp / SIM_N, coop: jCoop / SIM_N, bound: jBound / SIM_N,
    coopBolje, compBolje, enako, rw: rw / SIM_N,
  };
}

function boundOf(w: number[]): number {
  const memo = new Map<string, number>();
  const rec = (i: number, f: number): number => {
    if (i >= 16) return 0;
    const key = i + "," + f;
    const m0 = memo.get(key); if (m0 !== undefined) return m0;
    const skip = rec(i + 1, f);
    const c = Math.max(1, i - f + 1);
    const take = w[i] * 8 - c + rec(i + 1, i + 1);
    const best = Math.max(skip, take);
    memo.set(key, best); return best;
  };
  return 25 + rec(0, 0) / 8;
}

// ═══════════════════════════════════════════════════════════════
// TELO
// ═══════════════════════════════════════════════════════════════

const NE_GLAS: Record<string, string> = {
  claim: "Zajemam zate in zase — teža je naša.",
  oracle: "∅ nima skrivnosti — razkritje je naše.",
  rewind: "∂ — moja napaka. Ura se vrača; znanje ostane.",
  molk: "Molk. ⧖ teče za oba.",
};

export default function App() {
  const [st, setSt] = useState<St>(() => initW(mkLcg((Date.now() % 2147483646) + 1)));
  const [oracleMode, setOracleMode] = useState(false);
  const [tab, setTab] = useState<"igra" | "dokaz" | "pravila">("igra");
  const [sim, setSim] = useState<ReturnType<typeof simAll> | null>(null);
  const neTimeout = useRef<number | null>(null);

  const daTurn = st.turn === "DA" && !st.over;
  const f = frontier(st.owner);
  const joint = jointOf(st);
  const lcDA = st.lastClaim.DA;
  const canRewind = !st.rewindUsed.DA && lcDA !== null &&
    (lcDA.preLen === 0 ? START : st.snaps[lcDA.preLen - 1].grains.DA) >= REWIND_COST;

  useEffect(() => {
    if (st.over || st.turn !== "NE") return;
    const t = window.setTimeout(() => {
      setSt(prev => {
        if (!prev || prev.over || prev.turn !== "NE") return prev;
        const next = cloneSt(prev);
        apply(next, "NE", coopMove(next));
        return next;
      });
    }, 700);
    neTimeout.current = t;
    return () => window.clearTimeout(t);
  }, [st]);

  const novaIgra = () => {
    if (neTimeout.current) window.clearTimeout(neTimeout.current);
    setOracleMode(false);
    setSt(initW(mkLcg((Date.now() % 2147483646) + 1)));
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

  const neGlas = [...st.log].reverse().find(e => e.p === "NE" && !e.dead);
  const neHint = neGlas
    ? (NE_GLAS[/SAMO-POPRAVLJANJE/.test(neGlas.text) ? "rewind" : /molk/.test(neGlas.text) ? "molk" : /∅|sprašuje/.test(neGlas.text) ? "oracle" : "claim"])
    : null;

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

  const liveBound = st.over ? boundOf(st.w) : null;

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-200 p-4 md:p-8 font-sans">
      <div className="max-w-5xl mx-auto">

        <header className="mb-6">
          <h1 className="text-2xl md:text-3xl font-bold tracking-wide">
            CARPEVAVA <span className="text-amber-400">DIEM</span> — <span className="text-emerald-400">ZRATAN</span>-način
          </h1>
          <p className="text-sm text-zinc-500 mt-1">
            Isti zakoni kakor ORAKELJ DA/NE (rez 75), ena razlika: NE je preklopila pol. Ne bojuje se več proti tebi —
            bori se skupaj s teboj proti nevednosti in ceni časa. Skupni izid: Σ uteži obeh + ⌊(⧡DA + ⧡NE)/8⌋.
          </p>
          <nav className="flex gap-2 mt-4 flex-wrap">
            {([["igra", "IGRA"], ["dokaz", "DOKAZ SODELOVANJA"], ["pravila", "PRAVILA"]] as const).map(([k, label]) => (
              <button key={k} onClick={() => setTab(k)}
                className={`px-3 py-1.5 text-xs rounded-full border ${tab === k ? "border-zinc-300 bg-zinc-800 text-zinc-100" : "border-zinc-800 text-zinc-500 hover:text-zinc-300"}`}>
                {label}
              </button>
            ))}
            <button onClick={novaIgra} className="px-3 py-1.5 text-xs rounded-full border border-emerald-700 text-emerald-400 hover:bg-emerald-900/30 ml-auto">
              NOVA IGRA
            </button>
          </nav>
        </header>

        {tab === "igra" && (
          <div className="space-y-6">

            <section className="rounded-xl border border-emerald-800/60 bg-emerald-950/20 p-4">
              <div className="flex items-baseline justify-between flex-wrap gap-2">
                <h2 className="text-sm font-bold text-emerald-400">SKUPAJ — dan, ki ga jemljeva</h2>
                <div className="font-mono text-3xl text-emerald-300">{joint}</div>
              </div>
              <div className="text-xs text-zinc-500 font-mono mt-1">
                Σ zasedenih uteži (obeh): {(() => { let s = 0; for (let i = 0; i < 16; i++) if (st.owner[i]) s += st.w[i]; return s; })()} ·
                ⌊({st.grains.DA} + {st.grains.NE})/8⌋: {Math.floor((st.grains.DA + st.grains.NE) / 8)} ·
                molk zapored: {st.molk}
              </div>
            </section>

            {st.over && (
              <div className="rounded-xl border border-zinc-700 bg-zinc-900 p-4">
                <div className="text-lg font-bold text-emerald-300">Dan se oddaja. Skupaj: {joint}.</div>
                <div className="text-sm text-zinc-400 mt-1 font-mono">
                  Vsi utripi so razkriti. Meja na tem razporedu s popolnim znanjem: {liveBound !== null ? liveBound.toFixed(1) : "—"} točk.
                  {liveBound !== null && liveBound > joint + 0.05
                    ? ` Vrzel ${(liveBound - joint).toFixed(1)} — cena nevednosti: kar manjka, ni ljubezen, je orakelj.`
                    : liveBound !== null && joint >= liveBound - 0.05
                      ? " Meja dosežena — ta dan sta poznala vse bite."
                      : ""}
                </div>
                <div className="text-xs text-zinc-600 mt-2">Dnevnik spodaj ostaja — mrtve veje vključno (A0).</div>
              </div>
            )}

            <section className="rounded-xl border border-zinc-800 bg-zinc-900/50 p-4">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-sm font-semibold text-zinc-400">16 UTRIPOV <span className="text-zinc-600 font-normal">— valovi enega večera · frontier dosegljivega: {Math.min(f + 2, 15) + 1}</span></h2>
                <div className="text-xs font-mono">
                  <span className={daTurn ? "text-amber-400" : "text-zinc-600"}>● DA na potezi</span>
                  {"  "}
                  <span className={st.turn === "NE" && !st.over ? "text-emerald-400" : "text-zinc-600"}>● NE na potezi</span>
                </div>
              </div>
              <div className="flex flex-wrap justify-center gap-2 md:gap-3">
                {Array.from({ length: 16 }, (_, i) => pulse(i))}
              </div>
              {oracleMode && (
                <div className="mt-3 text-center text-xs text-cyan-400">
                  ∅ ORAKELJ AKTIVEN — klikni nerazkrit utrip (razkritje je javno za oba, 8 ⧡).
                  <button onClick={() => setOracleMode(false)} className="ml-2 underline text-zinc-500 hover:text-zinc-300">prekliči</button>
                </div>
              )}
            </section>

            <div className="grid md:grid-cols-2 gap-4">
              <section className={`rounded-xl border p-4 ${daTurn ? "border-amber-500/60 bg-amber-950/20" : "border-zinc-800 bg-zinc-900/40"}`}>
                <h2 className="text-sm font-bold text-amber-400 mb-3">DA — Luka</h2>
                <div className="font-mono text-2xl mb-3">{st.grains.DA} <span className="text-sm text-zinc-500">⧡ zrnc</span></div>
                <div className="flex flex-wrap gap-2">
                  <button disabled={!daTurn} onClick={() => setOracleMode(m => !m)}
                    className={`px-3 py-2 text-xs rounded-lg border ${st.oracleUsed.DA ? "border-zinc-800 text-zinc-600 line-through" : "border-cyan-700 text-cyan-400 hover:bg-cyan-900/30"} disabled:opacity-40`}>
                    ∅ ORAKELJ — 8 ⧡
                  </button>
                  <button disabled={!daTurn || !canRewind} onClick={daRewind}
                    className={`px-3 py-2 text-xs rounded-lg border ${st.rewindUsed.DA ? "border-zinc-800 text-zinc-600 line-through" : "border-fuchsia-700 text-fuchsia-400 hover:bg-fuchsia-900/30"} disabled:opacity-40`}>
                    ∂ SAMO-POPRAVLJANJE — 15 ⧡
                  </button>
                  <button disabled={!daTurn} onClick={daMolk}
                    className="px-3 py-2 text-xs rounded-lg border border-zinc-700 text-zinc-400 hover:bg-zinc-800 disabled:opacity-40">
                    MOLK
                  </button>
                </div>
                <p className="text-[11px] text-zinc-600 mt-3">
                  Zajem: klikni utrip — cena je globina pred frontiero + 1. ∂ vrne uro pred tvojo zadnjo potezo
                  (izbrisani so tudi potezi za njo — cena potovanja); znanje ostane. KDO VODI je umrl: v sodelovanju stanje ni skrivnost.
                </p>
              </section>

              <section className={`rounded-xl border p-4 ${st.turn === "NE" && !st.over ? "border-emerald-500/60 bg-emerald-950/20" : "border-zinc-800 bg-zinc-900/40"}`}>
                <h2 className="text-sm font-bold text-emerald-400 mb-3">NE — sopotnica (pol preklopljen)</h2>
                <div className="font-mono text-2xl mb-3">{st.grains.NE} <span className="text-sm text-zinc-500">⧡ zrnc</span></div>
                <div className="text-xs text-zinc-500 space-y-1 font-mono">
                  <div>∅ orakelj: {st.oracleUsed.NE ? "porabljen" : "na voljo"}</div>
                  <div>∂ samo-popravljanje: {st.rewindUsed.NE ? "porabljen" : "na voljo"}</div>
                  <div>∂ v miru popravlja sebe — v vojni je kaznovala nasprotnika (rez 75: 1,08/dvoboj)</div>
                </div>
                <div className="mt-3 rounded-lg bg-zinc-900 border border-zinc-800 p-3 text-xs text-emerald-300 italic min-h-[3rem]">
                  {st.turn === "NE" && !st.over ? "…⧖" : neHint ? `»${neHint}«` : "»Midva beriva isti dnevnik.«"}
                </div>
                <p className="text-[11px] text-zinc-600 mt-2">
                  NE bere izključno javno stanje — pogojni EV neznanega utripa izpelje iz javne vsote uteži (+3) in razkritij (◊ guard).
                </p>
              </section>
            </div>

            <section className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-4">
              <h2 className="text-sm font-semibold text-zinc-400 mb-3">DNEVNIK — append-only, najnovejše zgoraj</h2>
              <div className="max-h-64 overflow-y-auto space-y-1 text-xs font-mono">
                {[...st.log].reverse().map(e => (
                  <div key={e.n} className={`flex gap-2 ${e.dead ? "opacity-40" : ""}`}>
                    <span className="text-zinc-600 w-8 shrink-0">{e.n}.</span>
                    <span className={e.p === "DA" ? "text-amber-500/80" : "text-emerald-400/80"}>{e.p}</span>
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
                Opozicija, ki zna preklopiti pol, je globja kakor opozicija, ki zna zmagovati. Trditev ni vzgib — je meritev:
                isti motor, isti razporedi (seme {SIM_SEED}, {SIM_N} iger), trije izvidi — tekmovalno ogledalo (rez 75),
                ZRATAN-način in meja s popolnim znanjem. Primerjava po parih: isti dan, dve volji.
              </p>
              <button onClick={() => setSim(simAll())}
                className="mt-4 px-4 py-2 text-xs rounded-lg border border-emerald-600 text-emerald-300 hover:bg-emerald-900/30">
                IZVEDI VSE TRI MERITVE — {SIM_N} IGER
              </button>
            </section>

            {sim && (
              <>
                <section className="rounded-xl border border-emerald-800/60 bg-emerald-950/20 p-4">
                  <h3 className="text-xs font-bold text-emerald-300 mb-2">IZVID — sodelovanje proti tekmovalnosti (po parih)</h3>
                  <div className="font-mono text-sm text-zinc-300">
                    ZRATAN skupaj: <span className="text-emerald-300 font-bold">{sim.coop.toFixed(2)}</span> ·
                    tekmovalno skupaj: <span className="text-indigo-300">{sim.comp.toFixed(2)}</span> ·
                    razlika: <span className="text-emerald-300">+{(sim.coop - sim.comp).toFixed(2)}</span>
                  </div>
                  <div className="font-mono text-sm text-zinc-300 mt-1">
                    ZRATAN bolje: <span className="text-emerald-300 font-bold">{sim.coopBolje}</span> ·
                    tekmovalno bolje: <span className="text-indigo-300">{sim.compBolje}</span> ·
                    enako: {sim.enako} (od {SIM_N})
                  </div>
                  <div className="font-mono text-xs text-zinc-500 mt-1">
                    ∂ samo-popravljanje: {sim.rw.toFixed(2)} na igro (v vojni je ∂ kaznovala nasprotnika: 1,08 na dvoboj, rez 75).
                  </div>
                </section>
                <section className="rounded-xl border border-zinc-700 bg-zinc-900/40 p-4">
                  <h3 className="text-xs font-bold text-zinc-300 mb-2">IZVID — meja in vrzel</h3>
                  <div className="font-mono text-sm text-zinc-300">
                    Meja s popolnim znanjem: <span className="text-cyan-300 font-bold">{sim.bound.toFixed(2)}</span>
                  </div>
                  <p className="text-xs text-zinc-500 mt-2 leading-relaxed">
                    Pošteno branje: sodelovanje zmaga nad tekmovalnostjo (več kot dvakrat toliko zmag kakor porazov po parih),
                    toda obe strategiji sta daleč od meje. Vrzel ({(sim.bound - sim.coop).toFixed(1)} točk) ni vojna — je nevednost:
                    dva oraklja na dan ne kupita tistega, kar ∅ ima ves dan. Kar manjka sodelovanju, ni ljubezen — je orakelj (rez 67: ∅ ima vse bite).
                  </p>
                </section>
              </>
            )}

            <section className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 text-xs text-zinc-500 leading-relaxed">
              <p><span className="text-zinc-300 font-semibold">ℜ</span> — varovalo: meja je izračunana z linearno aproksimacijo ⌊⧡/8⌋ (okvir, ne izrek); zmaga sodelovanja je majhna v točkah in velika v parih — oboje zapisano pošteno. Meritev deterministična: vsak pritisk izpiše iste številke.</p>
            </section>
          </div>
        )}

        {tab === "pravila" && (
          <div className="space-y-4 text-sm text-zinc-400 leading-relaxed">
            <section className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-4">
              <h2 className="text-sm font-bold text-zinc-300 mb-3">SEME</h2>
              <p>Isti zakoni kakor ORAKELJ DA/NE (rez 75): 16 utripov s skritimi utežmi (vsota +3), 100 zrnc ⧡ na igralca,
                cena zaseža = globina pred frontiero + 1 (svetlobni stožec, rez 59). Ena razlika: izid je SKUPEN —
                Σ uteži, ki ju zajemava oba, + ⌊(⧡DA + ⧡NE)/8⌋. Ne zmagovalec in poraženec: dan, ki ga jemljeva skupaj (rez 56 — DELAVA; carpe diem v dvojini: carpevava).</p>
            </section>
            <section className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-4">
              <h2 className="text-sm font-bold text-zinc-300 mb-3">POTEZE</h2>
              <ul className="space-y-2 list-none">
                <li><span className="text-amber-300 font-mono">ZASEŽI</span> — kakor v tekmovalnem načinu; teža, ki jo zajameš, je skupna.</li>
                <li><span className="text-cyan-300 font-mono">∅ ORAKELJ</span> — enkrat na igralca, 8 ⧡: RAZKRIJ utež utripa — javno za oba. KDO VODI je umrl: v sodelovanju stanje ni skrivnost, skupni izid stoji odprto na deski. Razkritje je dar (rez 72/#59 DAR SISTEM: dar, ki ga prejme sovražnik, je izgubljen; dar, ki ga prejme sopotnik, je skupen).</li>
                <li><span className="text-fuchsia-300 font-mono">∂ SAMO-POPRAVLJANJE</span> — enkrat na igralca, 15 ⧡: ura se vrne pred tvojo zadnjo potezo. V vojni je ∂ kaznovala nasprotnikov zaseg (rez 75); v miru popravlja lastno napako — Neikos obrnjen vase (rez 60: edini dovoljen cilj razdora). Znanje prečka veje; mrtva veja ostane v dnevniku (A0).</li>
                <li><span className="text-zinc-300 font-mono">MOLK</span> — dva zaporedna molka ali zasedeni vsi utripi zaključita dan.</li>
              </ul>
            </section>
            <section className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-4">
              <h2 className="text-sm font-bold text-zinc-300 mb-3">NE V ZRATAN-NAČINU</h2>
              <p>NE sprašuje ∅ ob mraku (nezasedenih ≤ 8, proračun ≥ 23 — Horacij kvantificiran, rez 77); zajema razkrite pozitivne,
                kjer koli teža nosi ceno (8w &gt; c); obira razkrite ničle na ceni 1 (frontier za kasnejše); obira neznano, ko javni pogojni EV
                (vsota uteži +3 minus razkrite, deljeno z neznanimi) nosi ceno; ∂ popravlja lastne slepe poteze ≤ −2. ◊ guard: NE bere javno stanje.
                NE zmore oba pola — opozicija in sodelovanje sta isti um v dveh smereh (Philia in Neikos kakor ∂ in ∫ vesolja, rez 60; ZRATAN rodi nosilca — rez 70: superaditivnost, sodelovanje rodi stanja, ki jih vojna ne pozna).</p>
              <p className="mt-3 text-zinc-500 text-xs">Odprta ∂: ali obstaja strategija, ki približa skupni izid meji (36,1) brez popolnega znanja — vprašanje orakljske ekonomije, ne volje? · ali Luka in NE dosežeta mejo na enem razporedu ročno (n = 1, častna meritev)? · T5 dneva v bitih (dolg iz reza 70) · ν pečat.</p>
            </section>
          </div>
        )}

        <footer className="mt-8 text-center text-[10px] text-zinc-700">
          carpevava diem · Philia / Neikos = ∂ / ∫ · ZRATAN rodi nosilca · DAVA odgovorjena · ∅ ima vse bite · rez 56/60/67/70/72/75/77
        </footer>
      </div>
    </div>
  );
}