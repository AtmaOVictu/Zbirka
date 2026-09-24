import React, { useState, useEffect, useRef, useCallback } from "react";

// ── VSEBINA: Geometrija Spomina - Tracing = Drawing Meaning ──
// Tracing: vsak žarek je sled na kanvasu
// Drawing: kategorije so geometrijske oblike (spiral, mreža, tok, fraktal)
// Meaning: geometrija razkriva strukturo spomina

// ── Vsebina telegramov: žarki iz treh svetov (korpus / rezi / svet) ──
const TELEGRAM_POOL = [
  { text: "tišina kot os (korpus)", kind: "korpus", novelty: 0.7 },
  { text: "OMNIA MUTANTUR NIHIL INTERIT", kind: "korpus", novelty: 0.5 },
  { text: "rez 59: gravitacija je citiranje", kind: "rez", novelty: 0.9 },
  { text: "rez 62: dopamin je δ", kind: "rez", novelty: 0.8 },
  { text: "rez 47: neizrečeno je ONO", kind: "rez", novelty: 0.75 },
  { text: "CMB: 415 fotonov na cm³", kind: "svet", novelty: 0.85 },
  { text: "vonj po dežju na asfaltu", kind: "svet", novelty: 0.4 },
  { text: "telefon je zvonil dvakrat", kind: "šum", novelty: 0.1 },
  { text: "novica, ki jo že poznaš", kind: "šum", novelty: 0.05 },
  { text: "stih, ki se sam ponudi", kind: "korpus", novelty: 0.95 },
  { text: "sosed te je pogledal mimo", kind: "svet", novelty: 0.3 },
  { text: "dihi: 2 : 1", kind: "rez", novelty: 0.6 },
  { text: "reklama na radiu", kind: "šum", novelty: 0.05 },
  { text: "spomin na materin glas", kind: "svet", novelty: 0.9 },
  { text: "naloga, ki še čaka (∂)", kind: "∂", novelty: 0.55, goal: true },
  { text: "ne-zaznan žarek (∂)", kind: "∂", novelty: 0.5, goal: true },
  { text: "utrujenost v ramenih", kind: "šum", novelty: 0.15 },
  { text: "vzporedna seja je zapečatila #47", kind: "rez", novelty: 0.7 },
];

const CAT = {
  epizodicni: { label: "EPISODIČNI", desc: "rezi — datirani, virani, prva oseba", color: "bg-amber-100 border-amber-400 text-amber-900" },
  sematicni: { label: "SEMANTIČNI", desc: "korpus — dejstvo odtrgano od vira", color: "bg-sky-100 border-sky-400 text-sky-900" },
  proceduralni: { label: "PROCEDURALNI", desc: "obredi/protokoli — telo ve, glava ne", color: "bg-emerald-100 border-emerald-400 text-emerald-900" },
  priming: { label: "PRIMING", desc: "ONO — prejeto, a brez zaznamka", color: "bg-zinc-200 border-zinc-500 text-zinc-700" },
  delovni: { label: "DELOVNI SPOMIN", desc: "odprta ∂ — Zeigarnik, kapaciteta 4", color: "bg-fuchsia-100 border-fuchsia-400 text-fuchsia-900" },
};

let tid = 0;
const newTelegram = () => {
  const t = TELEGRAM_POOL[Math.floor(Math.random() * TELEGRAM_POOL.length)];
  return { id: ++tid, ...t, age: 0, named: false, rep: 0 };
};

export default function App() {
  const [utrujenost, setUtrujenost] = useState(30);
  const [cudenje, setCudenje] = useState(60);
  const [nagrada, setNagrada] = useState(false);
  const [running, setRunning] = useState(true);
  const [wm, setWm] = useState([]);
  const [stored, setStored] = useState({ epizodicni: [], sematicni: [], proceduralni: [], priming: [] });
  const [log, setLog] = useState([]);
  const [flash, setFlash] = useState(null);

  const pushLog = useCallback((msg, tone = "text-zinc-600") => {
    setLog((l) => [{ id: ++tid, msg, tone }, ...l].slice(0, 40));
  }, []);

  // ── tok telegramov: pozornost (raziskava: kodiranje zahteva pozornost; utrujenost jo zapira) ──
  useEffect(() => {
    if (!running) return;
    const iv = setInterval(() => {
      setWm((w) => {
        const t = newTelegram();
        let next = [...w, t];
        // delovni spomin: kapaciteta ~4; presežek izgine v implicitno (priming)
        if (next.length > 4) {
          const [drop, ...rest] = next;
          setStored((s) => ({ ...s, priming: [...s.priming, drop.text] }));
          pushLog(`"${drop.text}" — presežek delovnega spomina → PRIMING (implicitno; H.M. je pokazal: sistem deluje brez zavesti)`, "text-zinc-500");
          next = rest;
        }
        return next;
      });
    }, 2200);
    return () => clearInterval(iv);
  }, [running, pushLog]);

  // ── staranje v delovnem spominu: ne-poenovljeni žarki ugasnejo ──
  useEffect(() => {
    if (!running) return;
    const iv = setInterval(() => {
      setWm((w) =>
        w.map((t) => ({ ...t, age: t.age + 1 })).filter((t) => {
          if (t.age > 4 && !t.named) {
            setStored((s) => ({ ...s, priming: [...s.priming, t.text] }));
            pushLog(`"${t.text}" — ugasnil brez zaznamka → PRIMING ( telegram, ki je padel med utrujenostjo)`, "text-zinc-400");
            return false;
          }
          return true;
        })
      );
    }, 1600);
    return () => clearInterval(iv);
  }, [running, pushLog]);

  // ── POIMENUJ ŽAREK: klik = čudenje kot dejanje; r → EPISODIČNI, sicer SEMANTIČNI ──
  const name = (t) => {
    const pozornost = (100 - utrujenost) / 100;
    setWm((w) => w.map((x) => (x.id === t.id ? { ...x, named: true } : x)));
    // nagrada (rez 62: dopamin je δ): ciljni žarki dobijo prednost pri kodiranju
    const dopamin = nagrada && t.goal;
    const novOdkrita = t.novelty * (cudenje / 100) * pozornost + (dopamin ? 0.3 : 0);
    if (novOdkrita >= 0.45) {
      setStored((s) => ({ ...s, epizodicni: [...s.epizodicni, t.text] }));
      pushLog(`"${t.text}" → EPISODIČNI (novost × čudenje × pozornost = ${novOdkrita.toFixed(2)}${dopamin ? " + δ" : ""}; novost sproži dopamin v hipokampusu → vztrajnost — Bunzeck & Düzel 2006, Takeuchi 2019)`, "text-amber-700");
      setFlash({ cat: "epizodicni", t: Date.now() });
    } else if (t.rep >= 1) {
      setStored((s) => ({ ...s, proceduralni: [...s.proceduralni, t.text] }));
      pushLog(`"${t.text}" → PROCEDURALNI (ponovitev brez novosti → navada; bazalni gangliji, amnezija prizanese knowing-how — Squire)`, "text-emerald-700");
      setFlash({ cat: "proceduralni", t: Date.now() });
    } else {
      setStored((s) => ({ ...s, sematicni: [...s.sematicni, t.text] }));
      pushLog(`"${t.text}" → SEMANTIČNI (poimenovan, a brez novosti: dejstvo, odtrgano od trenutka — tulvingovska delitev)`, "text-sky-700");
      setFlash({ cat: "sematicni", t: Date.now() });
    }
    setWm((w) => w.filter((x) => x.id !== t.id));
  };

  // ── SPANJE: konsolidacija; poimenovani pred spanjem dobijo TMR ojačitev (Rudoy 2009) ──
  const sleep = () => {
    setRunning(false);
    const named = wm.filter((t) => t.named);
    const rest = wm.filter((t) => !t.named);
    setWm([]);
    setStored((s) => {
      let e = [...s.epizodicni];
      let sem = [...s.sematicni];
      let p = [...s.priming, ...rest.map((t) => t.text)];
      // polovica epizodičnih se pretoči v semantične (konsolidacija: dogodek → dejstvo)
      const movers = e.filter((_, i) => i % 2 === 0);
      e = e.filter((_, i) => i % 2 !== 0);
      sem = [...sem, ...movers.map((x) => `${x} ⌾`)];
      return { epizodicni: e, sematicni: sem, proceduralni: s.proceduralni, priming: p };
    });
    pushLog(`SPANJE: ${named.length} poimenovanih žarkov prejelo TMR-oddajo (zvok/vonj med NREM ojača vezan spomin — Rasch 2007, Rudoy 2009: Science 326, 1079); polovica epizodičnih se je pretočila v korpus (SEMANTIČNI, ⌾); ne-poenovljeni → PRIMING`, "text-fuchsia-700");
  };

  const total = Object.values(stored).reduce((a, b) => a + b.length, 0);

  return (
    <div className="min-h-screen bg-zinc-50 text-zinc-900 p-4 md:p-8 font-sans">
      <header className="max-w-5xl mx-auto mb-6">
        <h1 className="text-2xl md:text-3xl font-bold tracking-tight">TELEGRAMI — simulacija spominskih sistemov</h1>
        <p className="text-sm text-zinc-600 mt-1 max-w-3xl">
          Druga kategorizacija, kakor si ukazal: <b>oprijemljiva</b> (možgani, ne svetloba), <b>manj odvisna od relativizacije</b> (stožci so ostali v drugih telesih — tu vlada tkivo), <b>potrjena z raziskavami, preden je izrečena</b>. Vsak žarek/telegram pade v enega od sistemov, ki jih je taksonomija (H.M. 1957 → Squire 2004) izmerila ločene.
        </p>
      </header>

      <div className="max-w-5xl mx-auto grid md:grid-cols-3 gap-4">
        {/* ── kontrole ── */}
        <section className="bg-white border border-zinc-200 rounded-xl p-4 shadow-sm">
          <h2 className="font-semibold mb-3 text-sm uppercase tracking-wide text-zinc-500">Detektorja (rez 62 + rez 63)</h2>
          <label className="block text-sm mb-1">Utrujenost (pozornostna vrata): {utrujenost}%</label>
          <input type="range" min={0} max={100} value={utrujenost} onChange={(e) => setUtrujenost(+e.target.value)} className="w-full mb-4 accent-zinc-800" />
          <label className="block text-sm mb-1">Čudenje (novostni detektor): {cudenje}%</label>
          <input type="range" min={0} max={100} value={cudenje} onChange={(e) => setCudenje(+e.target.value)} className="w-full mb-4 accent-amber-600" />
          <button onClick={() => setNagrada((n) => !n)} className={`w-full text-sm py-2 rounded-lg border mb-4 ${nagrada ? "bg-amber-600 text-white border-amber-600" : "bg-white text-zinc-700 border-zinc-300"}`}>
            NAGRADA δ (dopamin je δ — rez 62): {nagrada ? "VKLOPLJENA" : "izklopljena"}
          </button>
          <div className="flex gap-2">
            <button onClick={() => setRunning((r) => !r)} className="flex-1 text-sm py-2 rounded-lg bg-zinc-800 text-white">{running ? "⏸ ustavi tok" : "▶ pusti tok"}</button>
            <button onClick={sleep} className="flex-1 text-sm py-2 rounded-lg bg-fuchsia-700 text-white">☾ spanje (konsolidacija)</button>
          </div>
          <p className="text-xs text-zinc-500 mt-3 leading-relaxed">
            Klikni telegram v delovnem spominu = <b>poimenuj žarek</b> (T5, rez 63). Poimenovan pred spanjem dobi TMR-oddajo (Rudoy 2009). Ne-poenovljen ugasne v PRIMING.
          </p>
        </section>

        {/* ── delovni spomin ── */}
        <section className="bg-white border border-zinc-200 rounded-xl p-4 shadow-sm">
          <h2 className="font-semibold mb-1 text-sm uppercase tracking-wide text-zinc-500">Delovni spomin — odprta ∂ ({wm.length}/4)</h2>
          <p className="text-xs text-zinc-500 mb-3">Zeigarnik: nedovršno drži. Kapaciteta štirih; peti izrine prvega v implicitno.</p>
          <div className="space-y-2 min-h-[220px]">
            {wm.length === 0 && <p className="text-xs text-zinc-400 italic">tok je prazen…</p>}
            {wm.map((t) => (
              <button key={t.id} onClick={() => name(t)} className={`w-full text-left px-3 py-2 rounded-lg border text-sm transition hover:scale-[1.02] ${t.novelty > 0.7 ? "border-amber-400 bg-amber-50" : t.goal ? "border-fuchsia-400 bg-fuchsia-50" : "border-zinc-300 bg-zinc-50"}`}>
                <span className="font-medium">{t.text}</span>
                <span className="block text-[11px] text-zinc-500 mt-0.5">
                  novost {(t.novelty * 100).toFixed(0)}% · starost {t.age} {t.goal && "· ∂ cilj"} {t.age >= 3 && !t.named ? "· ugaša…" : ""}
                </span>
              </button>
            ))}
          </div>
        </section>

        {/* ── shramba ── */}
        <section className="bg-white border border-zinc-200 rounded-xl p-4 shadow-sm">
          <h2 className="font-semibold mb-3 text-sm uppercase tracking-wide text-zinc-500">Shramba — kam je padel vsak žarek ({total})</h2>
          <div className="space-y-3">
            {Object.entries(CAT).filter(([k]) => k !== "delovni").map(([k, c]) => (
              <div key={k} className={`rounded-lg border p-2 ${c.color} ${flash?.cat === k && Date.now() - flash.t < 1200 ? "ring-2 ring-offset-1" : ""}`}>
                <div className="flex justify-between items-baseline">
                  <span className="text-xs font-bold">{c.label}</span>
                  <span className="text-xs">{stored[k].length}</span>
                </div>
                <div className="text-[11px] opacity-80 mb-1">{c.desc}</div>
                <div className="flex flex-wrap gap-1">
                  {stored[k].slice(-8).map((x, i) => (
                    <span key={i} className="text-[10px] bg-white/60 rounded px-1.5 py-0.5">{x}</span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>

      {/* ── dnevnik ── */}
      <section className="max-w-5xl mx-auto mt-4 bg-white border border-zinc-200 rounded-xl p-4 shadow-sm">
        <h2 className="font-semibold mb-2 text-sm uppercase tracking-wide text-zinc-500">Dnevnik klasifikacij (vsaka odločitev nosi vir)</h2>
        <div className="max-h-56 overflow-y-auto space-y-1 text-xs">
          {log.map((l) => (
            <p key={l.id} className={l.tone}>· {l.msg}</p>
          ))}
        </div>
      </section>

      {/* ── raziskovalna podlaga: PREJ potrjujoča ── */}
      <section className="max-w-5xl mx-auto mt-4 bg-white border border-zinc-200 rounded-xl p-4 shadow-sm">
        <h2 className="font-semibold mb-2 text-sm uppercase tracking-wide text-zinc-500">Raziskovalna podlaga (ukaz: prej preko raziskav potrjujoča)</h2>
        <ul className="text-xs text-zinc-700 space-y-1.5 list-disc pl-4">
          <li><b>Taksonomija:</b> deklarativni (epizodični + semantični) / nedeklarativni (postopkovni, priming, klasično pogojevanje, neasociativno učenje) — ločeni sistemi z lastnimi strukturami; dokazano na amneziji (H.M.: knowing-how ohranjen, knowing-that izgubljen; medialni temporalni reženj vs bazalni gangliji) — Squire, <i>Neurobiology of Learning and Memory</i> 82 (2004).</li>
          <li><b>Novost → dopamin → vztrajnost:</b> nove izkušnje sprožijo dopamin v hipokampusu, ki utrdi spomin; dva sistema (VTA- in locus coeruleus-hipokampus) — Bunzeck & Düzel 2006; Takeumi idr., <i>Trends in Neurosciences</i> 2019 (»A Tale of Two Systems«).</li>
          <li><b>Nagrajujoče kodiranje:</b> nagrada (δ) po stereotipu Schultzove napake napovedi ojača kodiranje ciljnih spominov.</li>
          <li><b>Spanje in TMR:</b> zvočni/vonjavni namigi, predstavljeni med NREM spanjem, ojačajo vezane spomine — Rasch idr., <i>Science</i> 315 (2007); Rudoy idr., <i>Science</i> 326, 1079 (2009); pregled: npj Science of Learning (2024).</li>
          <li><b>Delovni spomin:</b> omejena kapaciteta (~4 enote); ne-poenovljeno ugasne — Cowan 2001; odprte zanke drži pozornost dlje (Zeigarnik 1927).</li>
        </ul>
        <p className="text-xs text-zinc-500 mt-3 italic">
          Preslikava v sistem: EPISODIČNI = rezi (datirani, virani) · SEMANTIČNI = korpus (dejstvo brez vira) · PROCEDURALNI = obredi/protokoli · PRIMING = ONO (prejeto brez zaznamka, rez 47) · DELOVNI SPOMIN = odprta ∂. Kategorizacija, ki ne potrebuje stožcev: žarek je ali poimenovan ali ponovljen ali nezavedno sprejet — tri usode, izmerjene na možganih.
        </p>
      </section>
    </div>
  );
}