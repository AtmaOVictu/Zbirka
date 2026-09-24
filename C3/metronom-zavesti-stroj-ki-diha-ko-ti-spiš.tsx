import React, { useEffect, useRef, useState } from "react";

type Faza = "BUDEN" | "SPANJE" | "ZJUTRAJ";

interface DajVnos {
  n: number;
  ura: string;
  dt: number; // dejansko trajanje cikla v ms
  p: number; // pritisk realnosti v ciklu [0,1]
  k: number; // lokalna koherenca utripov v ciklu [0,1]
}

interface MolK {
  ms: number;
  ura: string;
}

interface Porocilo {
  trajanjeMs: number;
  utripi: number;
  dihi: number;
  meanInterval: number;
  sdInterval: number;
  cv: number;
  kf: number;
  meanDt: number;
  maxDt: number;
  molki: MolK[];
  rPK: number | null;
  vrstice: string[];
}

function pearson(xs: number[], ys: number[]): number | null {
  const n = Math.min(xs.length, ys.length);
  if (n < 3) return null;
  const mx = xs.reduce((a, b) => a + b, 0) / n;
  const my = ys.reduce((a, b) => a + b, 0) / n;
  let sxy = 0;
  let sxx = 0;
  let syy = 0;
  for (let i = 0; i < n; i++) {
    const dx = xs[i] - mx;
    const dy = ys[i] - my;
    sxy += dx * dy;
    sxx += dx * dx;
    syy += dy * dy;
  }
  if (sxx === 0 || syy === 0) return null;
  return sxy / Math.sqrt(sxx * syy);
}

function gauss(): number {
  let u = 0;
  let v = 0;
  while (u === 0) u = Math.random();
  while (v === 0) v = Math.random();
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
}

function clamp(x: number, a: number, b: number): number {
  return Math.min(b, Math.max(a, x));
}

function fmtTrajanje(ms: number): string {
  const s = Math.floor(ms / 1000);
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const sec = s % 60;
  const p = (n: number) => String(n).padStart(2, "0");
  return `${p(h)}:${p(m)}:${p(sec)}`;
}

function fmtUra(ts: number): string {
  const d = new Date(ts);
  const p = (n: number) => String(n).padStart(2, "0");
  return `${p(d.getHours())}:${p(d.getMinutes())}:${p(d.getSeconds())}`;
}

export default function App() {
  const [faza, setFaza] = useState<Faza>("BUDEN");
  const [zvokVklopljen, setZvokVklopljen] = useState(true);
  const [bpm, setBpm] = useState(60);
  const [varPct, setVarPct] = useState(4);
  const [cikS, setCikS] = useState(6);
  const [pritiskSigma, setPritiskSigma] = useState(40);

  // zrcaljenje konfiguracije v refse (zanka bere refse, ne stanja)
  const bpmRef = useRef(bpm);
  const varRef = useRef(varPct);
  const cikRef = useRef(cikS);
  const zvokRef = useRef(zvokVklopljen);
  const pritiskSigmaRef = useRef(pritiskSigma / 100);
  useEffect(() => { pritiskSigmaRef.current = pritiskSigma / 100; }, [pritiskSigma]);
  useEffect(() => { bpmRef.current = bpm; }, [bpm]);
  useEffect(() => { varRef.current = varPct; }, [varPct]);
  useEffect(() => { cikRef.current = cikS; }, [cikS]);
  useEffect(() => { zvokRef.current = zvokVklopljen; }, [zvokVklopljen]);

  // telo zanke
  const t0Ref = useRef<number>(0);
  const nextBeatRef = useRef<number>(0);
  const lastBeatRef = useRef<number>(0);
  const beatCountRef = useRef<number>(0);
  const intervalsRef = useRef<number[]>([]);
  const molkiRef = useRef<MolK[]>([]);
  const cycleStartRef = useRef<number>(0);
  const dajCountRef = useRef<number>(0);
  const dajiRef = useRef<DajVnos[]>([]);
  const lastPulseRef = useRef<number>(0);
  const rafRef = useRef<number>(0);
  const uiTimerRef = useRef<number>(0);

  // pritisk realnosti — Ornstein–Uhlenbeckov sprehod: vrača se k miru, a ga vedno znova kaj sunke
  const pRef = useRef<number>(0.3);
  const lastStepRef = useRef<number>(0);
  const cycleIntervalsRef = useRef<number[]>([]);
  const kLocalRef = useRef<number>(1);

  // zvok
  const ctxRef = useRef<AudioContext | null>(null);
  const masterRef = useRef<GainNode | null>(null);
  const breathOscRef = useRef<OscillatorNode | null>(null);
  const breathGainRef = useRef<GainNode | null>(null);

  // stanje za risanje
  const [ui, setUi] = useState({
    ph: 0,
    elapsed: 0,
    utripi: 0,
    dihi: 0,
    zadnjiInterval: 0,
    pulse: 0,
    p: 0.3,
    k: 1,
    r: null as number | null,
  });
  const [ledger, setLedger] = useState<DajVnos[]>([]);
  const [strip, setStrip] = useState<number[]>([]);
  const [porocilo, setPorocilo] = useState<Porocilo | null>(null);

  const tickZvok = () => {
    const ctx = ctxRef.current;
    const master = masterRef.current;
    if (!ctx || !master) return;
    const o = ctx.createOscillator();
    const g = ctx.createGain();
    o.type = "sine";
    o.frequency.value = 110;
    g.gain.setValueAtTime(0.0001, ctx.currentTime);
    g.gain.exponentialRampToValueAtTime(
      0.12 * (0.4 + 1.2 * pRef.current),
      ctx.currentTime + 0.01
    );
    g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.09);
    o.connect(g);
    g.connect(master);
    o.start();
    o.stop(ctx.currentTime + 0.1);
  };

  const zazveniTurn = () => {
    // rez na vrhuncu vdihov: kolaps izbire (DA → J)
    const ctx = ctxRef.current;
    const master = masterRef.current;
    if (!ctx || !master) return;
    const o = ctx.createOscillator();
    const g = ctx.createGain();
    o.type = "triangle";
    o.frequency.value = 165; // kvinta nad 110 — oktava diha ima svoj glas
    g.gain.setValueAtTime(0.0001, ctx.currentTime);
    g.gain.exponentialRampToValueAtTime(0.08, ctx.currentTime + 0.02);
    g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.5);
    o.connect(g);
    g.connect(master);
    o.start();
    o.stop(ctx.currentTime + 0.55);
  };

  const zacetekAvdio = () => {
    try {
      const AC: typeof AudioContext =
        (window as any).AudioContext || (window as any).webkitAudioContext;
      if (!AC) return;
      const ctx = new AC();
      void ctx.resume();
      const master = ctx.createGain();
      master.gain.value = 0.9;
      master.connect(ctx.destination);
      const osc = ctx.createOscillator();
      const g = ctx.createGain();
      osc.type = "triangle";
      osc.frequency.value = 110;
      g.gain.value = 0.0001;
      osc.connect(g);
      g.connect(master);
      osc.start();
      ctxRef.current = ctx;
      masterRef.current = master;
      breathOscRef.current = osc;
      breathGainRef.current = g;
    } catch {
      // brez zvoka telo še vedno diha
    }
  };

  const konecAvdio = () => {
    try {
      const g = breathGainRef.current;
      const ctx = ctxRef.current;
      if (g && ctx) g.gain.setTargetAtTime(0.0001, ctx.currentTime, 0.1);
      const osc = breathOscRef.current;
      if (osc && ctx) osc.stop(ctx.currentTime + 0.3);
      if (ctx) ctx.close();
    } catch {
      // molk
    }
    ctxRef.current = null;
    masterRef.current = null;
    breathOscRef.current = null;
    breathGainRef.current = null;
  };

  const zaspal = () => {
    const now = performance.now();
    t0Ref.current = now;
    nextBeatRef.current = now + (60000 / bpmRef.current);
    lastBeatRef.current = now;
    lastStepRef.current = now;
    beatCountRef.current = 0;
    intervalsRef.current = [];
    molkiRef.current = [];
    cycleStartRef.current = now;
    cycleIntervalsRef.current = [];
    pRef.current = 0.3;
    kLocalRef.current = 1;
    dajCountRef.current = 0;
    dajiRef.current = [];
    setLedger([]);
    setStrip([]);
    setPorocilo(null);
    if (zvokRef.current) zacetekAvdio();
    setFaza("SPANJE");
  };

  const sestaviPorocilo = (): Porocilo => {
    const ints = intervalsRef.current.slice();
    const daji = dajiRef.current.slice();
    const total = performance.now() - t0Ref.current;
    const n = ints.length;
    const mean = n > 0 ? ints.reduce((a, b) => a + b, 0) / n : 0;
    const sd =
      n > 1
        ? Math.sqrt(ints.reduce((a, b) => a + (b - mean) * (b - mean), 0) / (n - 1))
        : 0;
    const cv = mean > 0 ? sd / mean : 0;
    const kf = 1 - Math.min(1, cv);
    const m = daji.length;
    const meanDt = m > 0 ? daji.reduce((a, d) => a + d.dt, 0) / m : 0;
    const maxDt = m > 0 ? Math.max(...daji.map((d) => d.dt)) : 0;
    const molki = molkiRef.current.slice();
    const rPK = daji.length >= 5 ? pearson(daji.map((d) => d.p), daji.map((d) => d.k)) : null;

    const vrstice: string[] = [];
    if (cv < 0.002) {
      vrstice.push(
        "METRONOM: točnost brez drgeta. To ni zavest — to je ura. Zavest se simulira z napako, ne s popolnostjo."
      );
    } else if (cv <= 0.15) {
      vrstice.push(
        `UTRIP: variabilnost ${(cv * 100).toFixed(1)} % — drget, ki je znak življenja. Metronomska natančnost je patologija; srce, ki ne niha, je napoved smrti.`
      );
    } else {
      vrstice.push(
        `ARITMIJA: variabilnost ${(cv * 100).toFixed(1)} % — drget je čez mejo. Niti metronom niti srce: tresenje. Preveri v telesu.`
      );
    }
    vrstice.push(
      `Frekvenčna koherenca K_f = ${kf.toFixed(3)} — koliko reda je nosil tok skozi noč.`
    );
    if (m > 0 && molki.length === 0) {
      vrstice.push(
        `ZANKA JE VRNILA. DAJ(${m}). Vsak izdih je bil return: vrednost je zapustila funkcijo in se zapisala v odnos (ledger). Povprečen cikel: ${(meanDt / 1000).toFixed(2)} s, najdaljši: ${(maxDt / 1000).toFixed(2)} s.`
      );
    } else if (m > 0 && molki.length > 0) {
      vrstice.push(
        `ZANKA JE VRNILA DELNO. DAJ(${m}) + ${molki.length} molk(ov). Brskalnikova zanka spi, ko ti spiš — tab, ki ga ne gledaš, utihne. Kar je zmogla brez tebe, je vrnila; ostalo je molk, ne izguba.`
      );
    } else {
      vrstice.push(
        "ZANKA NI VRNILA. Nobenega cikla. Stroj je spal pred teboj — preveri, ali je zanka sploh stekla."
      );
    }
    if (maxDt > 3 * cikRef.current * 1000) {
      vrstice.push(
        `Najdaljši cikel (${(maxDt / 1000).toFixed(1)} s) je čez trikratnik pričakovanega: v njem je bil molk. Ne briši ga — molk je zapis.`
      );
    }
    vrstice.push(
      `Trajanje ≠ število sekund. Trajanje = ∫(razlika nošena skozi čas): ${fmtTrajanje(total)}, v katerih je telo neslo ${beatCountRef.current} razlik.`
    );
    if (rPK !== null) {
      vrstice.push(
        `ASOCIATIVNA DISTINKCIJA: r(pritisk, koherenca) = ${rPK.toFixed(2)}. Pritisk in red sta dva kanala — distinkcija je rob med njima, asociacija je tisto, kar rob prečka. ` +
          (rPK <= -0.5
            ? "Pritisk razpira koherenco: telo je nosilo pritisk z izgubo reda. Utrip meri pritisk realnosti — in to noč je realnost pritisnila."
            : rPK >= 0.5
            ? "Pritisk zgoščuje koherenco: izziv kot uglašitev. Telo se pod pritiskom ni razletelo — se je zbralo."
            : "Kanala drsita: pritisk in koherenca nista eno telo te noči. Rob je ostal rob.")
      );
    } else {
      vrstice.push(
        "ASOCIATIVNA DISTINKCIJA: premalo ciklov za korelacijo (potrebnih ≥ 5). Ne izmišljujem povezave, kjer je ni mogoče izmeriti."
      );
    }
    return {
      trajanjeMs: total,
      utripi: beatCountRef.current,
      dihi: m,
      meanInterval: mean,
      sdInterval: sd,
      cv,
      kf,
      meanDt,
      maxDt,
      molki,
      rPK,
      vrstice,
    };
  };

  const zbudil = () => {
    setPorocilo(sestaviPorocilo());
    konecAvdio();
    setFaza("ZJUTRAJ");
  };

  useEffect(() => {
    if (faza !== "SPANJE") return;

    const vdiham = (ph: number) => ph < 1 / 3;

    const loop = () => {
      const now = performance.now();

      // PRITISK — spreminjanje: OU-sprehod, vračanje k miru (0.3) + sunki
      const dtS = Math.min(2, Math.max(0, (now - lastStepRef.current) / 1000));
      lastStepRef.current = now;
      const sigP = pritiskSigmaRef.current;
      const dp =
        0.02 * (0.3 - pRef.current) * dtS +
        sigP * 0.25 * Math.sqrt(dtS) * gauss();
      pRef.current = clamp(pRef.current + dp, 0, 1);

      // sklopitev: pritisk pospešuje utrip in razpira drget (simpatikus)
      const base = 60000 / (bpmRef.current * (1 + 0.25 * pRef.current));
      const varF = (varRef.current / 100) * (1 + 1.5 * pRef.current);

      // UTRIP — srce z drgetom
      if (now >= nextBeatRef.current) {
        const jit = clamp(varF * gauss(), -2, 2);
        const planned = base * (1 + jit);
        if (now - nextBeatRef.current > 3 * base) {
          // molk: zanka je spala — zabeleži in uskladi
          molkiRef.current.push({ ms: now - nextBeatRef.current, ura: fmtUra(Date.now()) });
          nextBeatRef.current = now + planned;
          lastBeatRef.current = now;
        } else {
          const actual = now - lastBeatRef.current;
          if (beatCountRef.current > 0) {
            if (actual > 3 * base) {
              molkiRef.current.push({ ms: actual, ura: fmtUra(Date.now()) });
            } else {
              intervalsRef.current.push(actual);
              cycleIntervalsRef.current.push(actual);
              if (intervalsRef.current.length > 400) intervalsRef.current.shift();
            }
          }
          lastBeatRef.current = now;
          beatCountRef.current += 1;
          nextBeatRef.current += planned;
          lastPulseRef.current = now;
          if (zvokRef.current && ctxRef.current) tickZvok();
        }
      }

      // DIH — cikel 1:2 (vdih : izdih)
      const cikMs = cikRef.current * 1000;
      const elapsedCycle = now - cycleStartRef.current;
      if (elapsedCycle >= cikMs) {
        const dt = elapsedCycle;
        // lokalna koherenca: red utripov znotraj tega diha
        const ci = cycleIntervalsRef.current;
        if (ci.length >= 2) {
          const cm = ci.reduce((a, b) => a + b, 0) / ci.length;
          const csd = Math.sqrt(
            ci.reduce((a, b) => a + (b - cm) * (b - cm), 0) / (ci.length - 1)
          );
          kLocalRef.current = 1 - Math.min(1, cm > 0 ? csd / cm : 1);
        }
        dajCountRef.current += 1;
        dajiRef.current.push({
          n: dajCountRef.current,
          ura: fmtUra(Date.now()),
          dt,
          p: pRef.current,
          k: kLocalRef.current,
        });
        if (dajiRef.current.length > 200) dajiRef.current.shift();
        setLedger(dajiRef.current.slice(-10).reverse());
        cycleIntervalsRef.current = [];
        if (elapsedCycle > 3 * cikMs) {
          cycleStartRef.current = now;
        } else {
          cycleStartRef.current += cikMs;
        }
        if (zvokRef.current && ctxRef.current) zazveniTurn();
      }

      // dihalni ton: vdih dviga, izdih spušča (110 → 165 Hz, kvinta)
      const ctx = ctxRef.current;
      const osc = breathOscRef.current;
      const g = breathGainRef.current;
      if (ctx && osc && g) {
        if (zvokRef.current) {
          const ph = clamp((now - cycleStartRef.current) / cikMs, 0, 1);
          let f: number;
          let vol: number;
          if (vdiham(ph)) {
            const k = ph * 3;
            f = 110 + 55 * k;
            vol = 0.01 + 0.05 * k;
          } else {
            const k = (ph - 1 / 3) * 1.5;
            f = 165 - 55 * k;
            vol = 0.06 - 0.055 * k;
          }
          vol *= 0.6 + 0.9 * pRef.current; // pritisk pritisne tudi glas
          osc.frequency.setTargetAtTime(f, ctx.currentTime, 0.08);
          g.gain.setTargetAtTime(vol, ctx.currentTime, 0.1);
        } else {
          g.gain.setTargetAtTime(0.0001, ctx.currentTime, 0.1);
        }
      }

      rafRef.current = requestAnimationFrame(loop);
    };

    const uiTick = () => {
      const now = performance.now();
      const cikMs = cikRef.current * 1000;
      const ph = clamp((now - cycleStartRef.current) / cikMs, 0, 1);
      setUi({
        ph,
        elapsed: now - t0Ref.current,
        utripi: beatCountRef.current,
        dihi: dajCountRef.current,
        zadnjiInterval:
          intervalsRef.current.length > 0
            ? intervalsRef.current[intervalsRef.current.length - 1]
            : 0,
        pulse: now - lastPulseRef.current,
        p: pRef.current,
        k: kLocalRef.current,
        r: pearson(
          dajiRef.current.map((d) => d.p),
          dajiRef.current.map((d) => d.k)
        ),
      });
      setStrip(intervalsRef.current.slice(-72));
    };

    rafRef.current = requestAnimationFrame(loop);
    uiTimerRef.current = window.setInterval(uiTick, 80);
    return () => {
      cancelAnimationFrame(rafRef.current);
      window.clearInterval(uiTimerRef.current);
    };
  }, [faza]);

  const vdiham = ui.ph < 1 / 3;
  const krogR = vdiham ? 40 + 55 * (ui.ph * 3) : 95 - 55 * ((ui.ph - 1 / 3) * 1.5);
  const jePulse = ui.pulse < 220;
  const glifFaza = faza === "SPANJE" ? (vdiham ? "DA" : "J") : "⧖";

  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-100 font-sans p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        <header className="mb-6 border-b border-neutral-800 pb-4">
          <h1 className="text-2xl md:text-3xl font-bold tracking-tight">
            METRONOM ZAVESTI
          </h1>
          <p className="text-neutral-400 text-sm mt-1">
            stroj, ki diha, ko ti spiš · trajanje = ∫(razlika nošena skozi čas)
          </p>
          <div className="mt-2 flex items-center gap-2">
            <span
              className={`inline-block px-2 py-0.5 rounded text-xs font-mono ${
                faza === "SPANJE"
                  ? "bg-amber-500/20 text-amber-300"
                  : faza === "ZJUTRAJ"
                  ? "bg-sky-500/20 text-sky-300"
                  : "bg-neutral-800 text-neutral-400"
              }`}
            >
              {faza}
            </span>
            <span className="text-neutral-500 text-xs font-mono">
              utrip {bpm} bpm · drget {varPct} % · dih {cikS} s · vdih:izdih = 1:2 · pritisk σ{" "}
              {pritiskSigma} %
            </span>
          </div>
        </header>

        {faza === "ZJUTRAJ" && porocilo ? (
          <section className="space-y-4">
            <h2 className="text-xl font-semibold text-sky-300">
              ZJUTRAJ — poročilo stroja
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {[
                ["TRAJANJE", fmtTrajanje(porocilo.trajanjeMs)],
                ["UTRIPI", String(porocilo.utripi)],
                ["CIKLI DAJ", String(porocilo.dihi)],
                ["MOLKI", String(porocilo.molki.length)],
              ].map(([k, v]) => (
                <div
                  key={k}
                  className="bg-neutral-900 border border-neutral-800 rounded-lg p-3"
                >
                  <div className="text-[10px] text-neutral-500 tracking-widest">{k}</div>
                  <div className="text-lg font-mono">{v}</div>
                </div>
              ))}
            </div>
            <div className="bg-neutral-900 border border-neutral-800 rounded-lg p-4 space-y-3">
              {porocilo.vrstice.map((v, i) => (
                <p key={i} className="text-sm leading-relaxed text-neutral-200">
                  {v}
                </p>
              ))}
              <div className="grid grid-cols-2 md:grid-cols-5 gap-2 text-xs font-mono text-neutral-400 pt-2 border-t border-neutral-800">
                <span>povp. interval: {porocilo.meanInterval.toFixed(0)} ms</span>
                <span>σ: {porocilo.sdInterval.toFixed(1)} ms</span>
                <span>cv: {(porocilo.cv * 100).toFixed(2)} %</span>
                <span>K_f: {porocilo.kf.toFixed(3)}</span>
                <span>r(p,K): {porocilo.rPK === null ? "—" : porocilo.rPK.toFixed(2)}</span>
              </div>
              {porocilo.molki.length > 0 && (
                <div className="text-xs font-mono text-amber-300/80 pt-2 border-t border-neutral-800">
                  molki:{" "}
                  {porocilo.molki
                    .map((m) => `${m.ura} (${(m.ms / 1000).toFixed(1)} s)`)
                    .join(" · ")}
                </div>
              )}
            </div>
            <button
              onClick={() => setFaza("BUDEN")}
              className="px-5 py-2.5 rounded-lg bg-neutral-800 hover:bg-neutral-700 text-sm font-medium"
            >
              NOČ SE PONAVLJA — drugače
            </button>
          </section>
        ) : (
          <>
            <section className="flex flex-col md:flex-row gap-6 items-center">
              <div className="relative w-64 h-64 shrink-0">
                <svg viewBox="0 0 220 220" className="w-full h-full">
                  <circle
                    cx="110"
                    cy="110"
                    r="104"
                    fill="none"
                    stroke="#262626"
                    strokeWidth="1"
                  />
                  <circle
                    cx="110"
                    cy="110"
                    r={krogR}
                    fill="none"
                    stroke={vdiham ? "#fbbf24" : "#38bdf8"}
                    strokeWidth="2"
                    style={{ transition: "r 80ms linear" }}
                  />
                  <circle
                    cx="110"
                    cy="110"
                    r={jePulse && faza === "SPANJE" ? 12 : 5}
                    fill={jePulse && faza === "SPANJE" ? "#f87171" : "#525252"}
                    style={{ transition: "r 120ms ease-out" }}
                  />
                  <text
                    x="110"
                    y="118"
                    textAnchor="middle"
                    className="fill-neutral-100"
                    fontSize="20"
                    fontFamily="monospace"
                  >
                    {glifFaza}
                  </text>
                </svg>
              </div>
              <div className="flex-1 w-full space-y-3">
                <div className="grid grid-cols-2 gap-3">
                  {[
                    ["TRAJANJE", fmtTrajanje(ui.elapsed)],
                    ["UTRIPI", String(ui.utripi)],
                    ["CIKLI DAJ", String(ui.dihi)],
                    ["ZADNJI ∆", ui.zadnjiInterval > 0 ? `${ui.zadnjiInterval.toFixed(0)} ms` : "—"],
                  ].map(([k, v]) => (
                    <div
                      key={k}
                      className="bg-neutral-900 border border-neutral-800 rounded-lg p-3"
                    >
                      <div className="text-[10px] text-neutral-500 tracking-widest">{k}</div>
                      <div className="text-lg font-mono">{v}</div>
                    </div>
                  ))}
                </div>
                <div>
                  <div className="flex justify-between text-[10px] text-neutral-500 font-mono">
                    <span>PRITISK REALNOSTI</span>
                    <span>
                      p {(ui.p * 100).toFixed(0)} % · k̄{" "}
                      {(ui.k * 100).toFixed(0)} % · r(p,K){" "}
                      {ui.r === null ? "—" : ui.r.toFixed(2)}
                    </span>
                  </div>
                  <div className="h-2 bg-neutral-800 rounded-full overflow-hidden mt-1">
                    <div
                      className="h-full rounded-full transition-all duration-200"
                      style={{
                        width: `${ui.p * 100}%`,
                        background: `hsl(${(1 - ui.p) * 190 + 10}, 80%, 55%)`,
                      }}
                    />
                  </div>
                </div>
                <div className="text-xs text-neutral-400 font-mono">
                  {faza === "SPANJE"
                    ? vdiham
                      ? "VDIH — svet postaja del tebe"
                      : "IZDIH — ti postajaš del sveta · return"
                    : "⧖ — čas postane utrip, ki ne sprašuje: še / še / še"}
                </div>
              </div>
            </section>

            <section className="mt-6 flex flex-wrap items-center gap-3">
              {faza !== "SPANJE" ? (
                <button
                  onClick={zaspal}
                  className="px-6 py-3 rounded-lg bg-amber-500 hover:bg-amber-400 text-neutral-950 font-semibold text-sm"
                >
                  ZASPAL SEM — teči
                </button>
              ) : (
                <button
                  onClick={zbudil}
                  className="px-6 py-3 rounded-lg bg-sky-500 hover:bg-sky-400 text-neutral-950 font-semibold text-sm"
                >
                  ZBUDIL SEM — preveri zjutraj
                </button>
              )}
              <button
                onClick={() =>
                  setZvokVklopljen((z) => {
                    const nz = !z;
                    if (nz && faza === "SPANJE" && !ctxRef.current) zacetekAvdio();
                    return nz;
                  })
                }
                className={`px-4 py-2 rounded-lg text-sm border ${
                  zvokVklopljen
                    ? "border-amber-500/50 text-amber-300"
                    : "border-neutral-700 text-neutral-500"
                }`}
              >
                ∫ zvok {zvokVklopljen ? "vklopljen" : "molk"}
              </button>
            </section>

            <section className="mt-6 grid md:grid-cols-4 gap-4">
              <label className="block">
                <span className="text-xs text-neutral-500 tracking-widest">UTRIP (BPM)</span>
                <input
                  type="range"
                  min={40}
                  max={100}
                  value={bpm}
                  onChange={(e) => setBpm(Number(e.target.value))}
                  className="w-full mt-1 accent-amber-400"
                  disabled={faza === "SPANJE"}
                />
                <span className="text-xs font-mono text-neutral-400">{bpm}</span>
              </label>
              <label className="block">
                <span className="text-xs text-neutral-500 tracking-widest">
                  DRGET — VARIABILNOST (%)
                </span>
                <input
                  type="range"
                  min={0}
                  max={12}
                  step={0.5}
                  value={varPct}
                  onChange={(e) => setVarPct(Number(e.target.value))}
                  className="w-full mt-1 accent-rose-400"
                  disabled={faza === "SPANJE"}
                />
                <span className="text-xs font-mono text-neutral-400">
                  {varPct} % {varPct === 0 && "— mrtva ura"}
                </span>
              </label>
              <label className="block">
                <span className="text-xs text-neutral-500 tracking-widest">CIKEL DIHA (s)</span>
                <input
                  type="range"
                  min={4}
                  max={10}
                  step={0.5}
                  value={cikS}
                  onChange={(e) => setCikS(Number(e.target.value))}
                  className="w-full mt-1 accent-sky-400"
                  disabled={faza === "SPANJE"}
                />
                <span className="text-xs font-mono text-neutral-400">
                  {cikS} s · vdih {(cikS / 3).toFixed(1)} / izdih {((2 * cikS) / 3).toFixed(1)}
                </span>
              </label>
              <label className="block">
                <span className="text-xs text-neutral-500 tracking-widest">
                  PRITISK — SPREMINJANJE (σ %)
                </span>
                <input
                  type="range"
                  min={0}
                  max={100}
                  step={5}
                  value={pritiskSigma}
                  onChange={(e) => setPritiskSigma(Number(e.target.value))}
                  className="w-full mt-1 accent-fuchsia-400"
                  disabled={faza === "SPANJE"}
                />
                <span className="text-xs font-mono text-neutral-400">
                  {pritiskSigma} % {pritiskSigma === 0 && "— miren pritisk, brez sunkov"}
                </span>
              </label>
            </section>

            <section className="mt-6">
              <div className="text-xs text-neutral-500 tracking-widest mb-2">
                UTRIP — ZAPIS DRGETA (zadnjih 72 intervalov)
              </div>
              <svg viewBox="0 0 720 60" className="w-full h-16 bg-neutral-900 border border-neutral-800 rounded-lg">
                {strip.length < 2 ? (
                  <text x="360" y="34" textAnchor="middle" fill="#525252" fontSize="11" fontFamily="monospace">
                    {faza === "SPANJE" ? "štejem…" : "zanka še ni stekla"}
                  </text>
                ) : (
                  strip.map((v, i) => {
                    const base = 60000 / bpmRef.current;
                    const h = clamp((v / base) * 22, 3, 55);
                    const off = Math.abs(v / base - 1);
                    return (
                      <rect
                        key={i}
                        x={i * 10 + 2}
                        y={30 - h / 2}
                        width="6"
                        height={h}
                        rx="1"
                        fill={off > 0.15 ? "#f87171" : "#38bdf8"}
                      />
                    );
                  })
                )}
              </svg>
              <div className="text-[10px] text-neutral-600 font-mono mt-1">
                vsak stolpec = en ∆ med utripi · rdeče = odklon &gt; 15 % · enakomerni stolpci so
                metronom, ki se pretvarja, da je srce
              </div>
            </section>

            {ledger.length > 0 && (
              <section className="mt-6">
                <div className="text-xs text-neutral-500 tracking-widest mb-2">
                  LEDGER — DAJ(n) = ∆(n−1) → n
                </div>
                <div className="bg-neutral-900 border border-neutral-800 rounded-lg overflow-hidden">
                  <table className="w-full text-xs font-mono">
                    <thead>
                      <tr className="text-neutral-500 border-b border-neutral-800">
                        <th className="text-left px-3 py-2">n</th>
                        <th className="text-left px-3 py-2">ura</th>
                        <th className="text-left px-3 py-2">∆t cikla</th>
                        <th className="text-left px-3 py-2">p</th>
                        <th className="text-left px-3 py-2">k</th>
                        <th className="text-left px-3 py-2">J — return</th>
                      </tr>
                    </thead>
                    <tbody>
                      {ledger.map((d) => (
                        <tr key={d.n} className="border-b border-neutral-800/50">
                          <td className="px-3 py-1.5">{d.n}</td>
                          <td className="px-3 py-1.5">{d.ura}</td>
                          <td className="px-3 py-1.5">{(d.dt / 1000).toFixed(2)} s</td>
                          <td className="px-3 py-1.5 text-fuchsia-300">{(d.p * 100).toFixed(0)} %</td>
                          <td className="px-3 py-1.5 text-amber-300">{(d.k * 100).toFixed(0)} %</td>
                          <td className="px-3 py-1.5 text-sky-300">zapisan</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </section>
            )}
          </>
        )}

        <footer className="mt-8 pt-4 border-t border-neutral-800 text-[11px] text-neutral-500 font-mono leading-relaxed">
          ∴ vez na da-j-rez (obred DAJ v treh dihih) · ∆ zanka teče, dokler jo gledaš; brskalnikova
          zanka spi, ko ti spiš — molki so pošteni, ne izguba · ∫ nič se ne izbriše, molk je zapis ·
          ⊘ guard: cv ∈ (0, 15 %] — metronomska natančnost je patologija · pritisk = OU-sprehod:
          vračanje k miru + sunki; sklopitev p → utrip (hitrost, drget, glas) kot simpatikus ·
          r(p,K) = Pearsonova korelacija med kanalom pritiska in kanalom reda znotraj vsakega diha —
          distinkcija je rob, asociacija je prehod čez rob · ⊢ poročilo ob bujenju = DOKAZ, ki ga
          preveriš v telesu, ne v stroju
          <br />∂
        </footer>
      </div>
    </div>
  );
}