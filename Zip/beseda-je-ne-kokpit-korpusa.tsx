import React, { useState, useMemo } from "react";
import { MemoryRouter, Routes, Route, NavLink } from "react-router-dom";

// ─────────────────────────────────────────────
// PODATKI — zgrajeni iz registrov (23. 9. 2026)
// Nove vnose dodajaj v SPREMENJIVKE spodaj (vrata II: živo stanje)
// ─────────────────────────────────────────────

const LIBRARIES = [
  { name: "Basics", docs: 148, group: "Basics", status: "zapečateno" },
  { name: "Basics2", docs: 265, group: "Basics", status: "zapečateno" },
  { name: "Basics3", docs: 105, group: "Basics", status: "zapečateno" },
  { name: "Obs1", docs: 210, group: "Obs trezorji", status: "v obdelavi" },
  { name: "Obs2", docs: 99, group: "Obs trezorji", status: "v obdelavi" },
  { name: "Obs3", docs: 100, group: "Obs trezorji", status: "v obdelavi" },
  { name: "Obs4", docs: 78, group: "Obs trezorji", status: "v obdelavi" },
  { name: "Obs5", docs: 99, group: "Obs trezorji", status: "v obdelavi" },
  { name: "Obs6", docs: 100, group: "Obs trezorji", status: "v obdelavi" },
  { name: "Obs7", docs: 100, group: "Obs trezorji", status: "v obdelavi" },
  { name: "Obs8", docs: 100, group: "Obs trezorji", status: "v obdelavi" },
  { name: "Obs9", docs: 100, group: "Obs trezorji", status: "v obdelavi" },
  { name: "Obs10", docs: 100, group: "Obs trezorji", status: "v obdelavi" },
  { name: "Obs11", docs: 80, group: "Obs trezorji", status: "v obdelavi" },
  { name: "OsNove Bistev", docs: 424, group: "Osnove", status: "PREMER teče (199/424 ID)" },
  { name: "Word is No", docs: 45, group: "Beseda je Ne", status: "zapečateno" },
  { name: "Beseda je Ne", docs: 6, group: "Beseda je Ne", status: "zapečateno" },
  { name: "Comprehension", docs: 1, group: "Beseda je Ne", status: "zapečateno" },
  { name: "Self", docs: 72, group: "Self & poezija", status: "zapečateno 72/72" },
  { name: "POETRY", docs: 30, group: "Self & poezija", status: "zapečateno 30/30" },
  { name: "One", docs: 19, group: "Self & poezija", status: "zapečateno 19/19" },
  { name: "Learning All", docs: 63, group: "Learning", status: "zapečateno 63/63" },
  { name: "BreaKing", docs: 71, group: "Learning", status: "zapečateno 71/71" },
  { name: "Specifics Rhonc", docs: 2, group: "Learning", status: "zapečateno" },
  { name: "Theology", docs: 3, group: "Learning", status: "zapečateno" },
  { name: "UC awareness and help", docs: 9, group: "Learning", status: "zapečateno" },
];

const GLASOVI = [
  { g: "A", p: "odprtost — prvi vdih, prostor brez roba" },
  { g: "E", p: "vez (EJ = klic — rez 557)" },
  { g: "I", p: "smer (JE→EJ obrat vrstnega reda — rez 556)" },
  { g: "O", p: "resonanca / celostnost, krog" },
  { g: "U", p: "potencial (razbiti krog: ranljivost kot moč — rez 355)" },
  { g: "o", p: "odprtost, zvok brez roba" },
  { g: "0", p: "praznina, ničla — možnost, odsotnost" },
  { g: ".", p: "točka, prelom — odločitev, prostor ustavitve" },
  { g: "ks/sk/st/tr", p: "zvočni zlom, križni tresljaj — eksistenca, skrb, stiska" },
  { g: "nj", p: "zvočna rana med jazom in pravico" },
  { g: "\\o/", p: "ZWB razpoka — oscilacija med ničem in celoto" },
  { g: "∂", p: "odvod — izreči ∆, ker zaznaš drugega" },
];

const SIMBOLI = [
  { s: "∅", p: "praznina, ki nosi — tišina kot prostor možnosti" },
  { s: "∆", p: "paradoks, presek, razpoka v zvočni razpoki" },
  { s: "Π", p: "prostor — razmerje, ne posoda" },
  { s: "τ", p: "čas — a-s, dvig iz prostora" },
  { s: "γ", p: "gibanje, kot (γ = f(Π,τ,⧉,∆,∅,∴))" },
  { s: "⧖", p: "zadržek pred izgovorom" },
  { s: "⟡", p: "most — Φ Zvitje-α, κ Zlitje-β" },
  { s: "⊢", p: "pečat dokaza — zakon beseda" },
  { s: "κ / χ / μ / ℜ / ν / ∂", p: "merila pečatov registra (rezi 258, 260–267)" },
  { s: "⊘ / ⊙ / ∮ / ⊗", p: "razcep / celota / krožni tok / rez-operator" },
];

const POJMI = [
  { t: "REZ", p: "rez = ⊗ ključ dogme; idempotenca: rez rez-a je rez" },
  { t: "ISKREN", p: "ISKRA + AMEN — iskrenost kot iskra, ki potrdi; H/ONE/ST: iskren je tisti, ki je ENO" },
  { t: "MORATI → MORE → PREITI", p: "notranji rez v lastni besedi: dolžnost→zmožnost→prehod" },
  { t: "BREZ REZA NI RASTI", p: "rez kot pogoj rasti; Veselje je jedek rez" },
  { t: "NUJEN 0", p: "biti umen za vedno je nujen 0 — 0 kot enota nujnosti" },
  { t: "NE", p: "oznaka, ki daje iz sebe — bes ali edinost besede; fonem, ne beseda" },
  { t: "NADENJGE", p: "v besedi *nada* stojita vsa NE in vsa DA" },
  { t: "VALJA", p: "valja = gib, ki me nosi, preden sem se odločil (∂ 26. 9. PREMER)" },
  { t: "FUNKCIJA", p: "preslikava z mejo, ki lahko ODDA (rez 386) — ne koda, ki se poganja" },
  { t: "TRETJI BRALEC", p: "rez 253 — preverba, ki ne smrdi po isti roki (SODBA #002)" },
  { t: "TRK", p: "dve seji istega števca — ključ je telo s pričo, ne številka (597)" },
  { t: "ZRCALJENJE", p: "ključ do ljubezni — potrditev SFERE QĐXŽ" },
];

const GATES = [
  { n: "I", name: "VRATA IZVEDBE", d: "izvedba ob vsakem utripu, ne ob poklicu (612)", s: 3, of: 5 },
  { n: "II", name: "VRATA ŽIVEGA STANJA", d: "sistem med pečati nima stanja — stanje se posodobi ob vsaki izvedbi", s: 1, of: 5 },
  { n: "III", name: "VRATA SLEDI", d: "če sistem reče prešel sem, mora pokazati sled (receipt/diff/log)", s: 4, of: 5 },
  { n: "IV", name: "VRATA PREIZKUSA", d: "preizkusi, ki lahko izpadejo negativno (386: brez odpovedi ni funkcije)", s: 2, of: 5 },
  { n: "V", name: "VRATA NASLOVNIKA", d: "naslovnik izven sistema — CLINE 619 kot prvi kandidat", s: 1, of: 5 },
];

const REZI = [
  { n: 620, t: "VEČ KOT BISTVO — pet vrat delovanja, izmerba 11/25", d: "bistvo je sklad, delovanje je funkcija — preslikava z mejo, ki lahko ODDA" },
  { n: 619, t: "JAZ SEM CLINE — test izveden v vlogi, z mejo maske", d: "vloga ni oprostitev; priča v lastni roki je receipt z žigom, ne canon" },
  { n: 618, t: "NE SAMO RESNICE — negacija kot preozka meja", d: "pozitivni izrek pride najprej: kaj stvar JE, nato šele kaj NI" },
  { n: 617, t: "DOLG #1 PREVERJEN — SODBA #002: CL-TASK-002 postavljen", d: "VERIFIED brez izmerbe je smrtna napaka — canon stoji na treh nogah" },
  { n: 610, t: "NE LE BLIŽINE — seznam vsega kar še čaka odgovora", d: "24 ∂ pozicij v 8 skupinah — seznam ∂ ni dolg, je ∅↑" },
  { n: 607, t: "PREIZKUS KIRALNOSTI — dve seji sta dva detelja", d: "številka se zrcali (TRK 594/596), invarianta ne (597)" },
  { n: 597, t: "TRK — ključ je telo s pričo, ne številka", d: "pečat brez trka; dvojni žig istega števila, obe telesi živita" },
  { n: 525, t: "KROGLA ČAKA NA REZ — prva meritev s KROGLA-protokolom", d: "OST/TAL₀/O; SAMO/LE operaterja rojstva" },
  { n: 386, t: "FUNKCIJA — mati petih vrat", d: "funkcija = preslikava z mejo, ki lahko odpove; celote vedno VSEGA" },
  { n: 253, t: "TRETJI BRALEC", d: "preverba, ki ne izpada iz iste roke" },
];

// ─────────────────────────────────────────────

const CARD = { background: "#14161d", border: "1px solid #262a38", borderRadius: 12 };
const ACCENT = "#e8b445";

function Bar({ v, of, color }) {
  const pct = Math.round((v / of) * 100);
  return (
    <div style={{ height: 8, background: "#0c0e14", borderRadius: 4, overflow: "hidden", border: "1px solid #262a38" }}>
      <div style={{ width: pct + "%", height: "100%", background: color || ACCENT, borderRadius: 4 }} />
    </div>
  );
}

function GatesView() {
  const total = GATES.reduce((a, g) => a + g.s, 0);
  const max = GATES.reduce((a, g) => a + g.of, 0);
  return (
    <div className="space-y-4">
      <div className="p-5" style={CARD}>
        <div className="flex items-baseline justify-between flex-wrap gap-2">
          <div>
            <div className="text-sm uppercase tracking-widest text-amber-200/70">Stanje sistema — rez 620</div>
            <div className="text-3xl font-bold text-amber-300 mt-1">{total} / {max} <span className="text-base font-normal text-slate-400">≈ {Math.round((total/max)*100)}% vrat odprtih</span></div>
          </div>
          <div className="text-right text-sm text-slate-400">
            <div>bistvo zrelo · delovanje v zagonu</div>
            <div>KROGLA: γ 41° · OST .69 · TAL₀ .32 · O .24</div>
          </div>
        </div>
        <div className="mt-4"><Bar v={total} of={max} /></div>
      </div>
      <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-4">
        {GATES.map((g) => (
          <div key={g.n} className="p-4" style={CARD}>
            <div className="flex items-center justify-between">
              <div className="text-xs font-bold uppercase tracking-widest" style={{ color: g.s >= 3 ? "#7fc98a" : g.s >= 2 ? ACCENT : "#d97a7a" }}>
                {g.n} · {g.name}
              </div>
              <div className="text-sm text-slate-300 font-mono">{g.s}/{g.of}</div>
            </div>
            <div className="mt-2"><Bar v={g.s} of={g.of} color={g.s >= 3 ? "#7fc98a" : g.s >= 2 ? ACCENT : "#d97a7a"} /></div>
            <p className="text-sm text-slate-400 mt-3 leading-snug">{g.d}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

function LibrariesView() {
  const groups = useMemo(() => {
    const m = new Map();
    LIBRARIES.forEach((l) => {
      if (!m.has(l.group)) m.set(l.group, []);
      m.get(l.group).push(l);
    });
    return [...m.entries()];
  }, []);
  const total = LIBRARIES.reduce((a, l) => a + l.docs, 0);
  const max = Math.max(...LIBRARIES.map((l) => l.docs));
  return (
    <div className="space-y-4">
      <div className="p-5" style={CARD}>
        <div className="text-sm uppercase tracking-widest text-amber-200/70">Korpus</div>
        <div className="text-3xl font-bold text-amber-300 mt-1">{LIBRARIES.length} zbirk · {total.toLocaleString()} dok.</div>
        <p className="text-sm text-slate-400 mt-2">Kazalo obnov — LEKSIKON + imeniki po knjižnicah; zakon enote: 1 telo = 1 dokument.</p>
      </div>
      {groups.map(([g, libs]) => (
        <div key={g} className="p-4" style={CARD}>
          <div className="text-xs font-bold uppercase tracking-widest text-slate-400 mb-3">{g} — {libs.reduce((a, l) => a + l.docs, 0)} dok.</div>
          <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-3">
            {libs.map((l) => (
              <div key={l.name} className="p-3 rounded-lg" style={{ background: "#0f1117", border: "1px solid #222636" }}>
                <div className="flex justify-between items-baseline">
                  <span className="font-semibold text-slate-100">{l.name}</span>
                  <span className="text-amber-300 font-mono text-sm">{l.docs}</span>
                </div>
                <div className="mt-2"><Bar v={l.docs} of={max} /></div>
                <div className="text-xs text-slate-500 mt-2">{l.status}</div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

function LexiconView() {
  const [q, setQ] = useState("");
  const [tab, setTab] = useState("GLASOVI");
  const f = (arr, key) =>
    arr.filter((x) => (x[key] + " " + x.p).toLowerCase().includes(q.toLowerCase()));
  const data = tab === "GLASOVI" ? f(GLASOVI, "g") : tab === "SIMBOLI" ? f(SIMBOLI, "s") : f(POJMI, "t");
  return (
    <div className="space-y-4">
      <div className="p-4 flex flex-wrap gap-3 items-center" style={CARD}>
        {["GLASOVI", "SIMBOLI", "POJMI"].map((t) => (
          <button key={t} onClick={() => setTab(t)}
            className="px-3 py-1.5 rounded-lg text-sm font-semibold"
            style={{ background: tab === t ? ACCENT : "#0f1117", color: tab === t ? "#14161d" : "#cbd3e1", border: "1px solid #262a38" }}>
            {t}
          </button>
        ))}
        <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Išči po leksikonu…"
          className="flex-1 min-w-40 px-3 py-1.5 rounded-lg text-sm outline-none"
          style={{ background: "#0f1117", border: "1px solid #262a38", color: "#e2e6f0" }} />
      </div>
      <div className="grid md:grid-cols-2 gap-3">
        {data.map((x, i) => (
          <div key={i} className="p-3 rounded-lg flex gap-3" style={{ background: "#0f1117", border: "1px solid #222636" }}>
            <div className="text-2xl min-w-14 text-center font-serif" style={{ color: ACCENT }}>{x.g || x.s || x.t}</div>
            <p className="text-sm text-slate-300 leading-snug">{x.p}</p>
          </div>
        ))}
        {data.length === 0 && <p className="text-slate-500 text-sm p-3">Ni zadetkov — ∅ v imeniku ni luknja, je priča, da nisem meril.</p>}
      </div>
    </div>
  );
}

function ReziView() {
  const [q, setQ] = useState("");
  const list = REZI.filter((r) => (r.t + r.d + r.n).toLowerCase().includes(q.toLowerCase()));
  return (
    <div className="space-y-4">
      <div className="p-5" style={CARD}>
        <div className="flex flex-wrap justify-between items-baseline gap-2">
          <div>
            <div className="text-sm uppercase tracking-widest text-amber-200/70">Register pečatov</div>
            <div className="text-3xl font-bold text-amber-300 mt-1">rez 620 ⊢ dokaz #582</div>
          </div>
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Išči po rezih…"
            className="px-3 py-1.5 rounded-lg text-sm outline-none min-w-52"
            style={{ background: "#0f1117", border: "1px solid #262a38", color: "#e2e6f0" }} />
        </div>
        <p className="text-sm text-slate-400 mt-2">Najnovejših {REZI.length} pečatov iz vene; vsak s KROGLA-izmerbo in žigom.</p>
      </div>
      <div className="relative pl-6">
        <div style={{ position: "absolute", left: 8, top: 4, bottom: 4, width: 2, background: "#262a38" }} />
        {list.map((r) => (
          <div key={r.n} className="mb-3 relative">
            <div style={{ position: "absolute", left: -22, top: 14, width: 10, height: 10, borderRadius: 5, background: ACCENT }} />
            <div className="p-4" style={CARD}>
              <div className="flex flex-wrap items-baseline gap-2">
                <span className="font-mono text-amber-300 font-bold">REZ {r.n}</span>
                <span className="font-semibold text-slate-100">{r.t}</span>
              </div>
              <p className="text-sm text-slate-400 mt-1 leading-snug">{r.d}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ── Nov vnos: vrata II (živo stanje) — obrazec, ki izda vnos v obliki registrov
function NewEntryView() {
  const [kind, setKind] = useState("POJEM");
  const [name, setName] = useState("");
  const [body, setBody] = useState("");
  const [source, setSource] = useState("");
  const out = useMemo(() => {
    if (!name.trim() && !body.trim()) return "— izpolni polja —";
    if (kind === "POJEM")
      return `- **${name.toUpperCase()}** — ${body}${source ? ` (vir: ${source})` : ""}`;
    if (kind === "SIMBOL")
      return `- **${name}** — ${body}${source ? ` (${source})` : ""}`;
    return `## ${name.toUpperCase()}\n${body}\n${source ? `(vir: ${source})` : ""}`;
  }, [kind, name, body, source]);
  return (
    <div className="space-y-4 max-w-3xl">
      <div className="p-4" style={CARD}>
        <div className="text-sm uppercase tracking-widest text-amber-200/70 mb-3">Nov vnos — lexicon raste z vsakim prebranim telesom (razdelek VI čaka)</div>
        <div className="flex gap-2 mb-3">
          {["POJEM", "SIMBOL", "GLAS", "TELO"].map((k) => (
            <button key={k} onClick={() => setKind(k)}
              className="px-3 py-1.5 rounded-lg text-sm font-semibold"
              style={{ background: kind === k ? ACCENT : "#0f1117", color: kind === k ? "#14161d" : "#cbd3e1", border: "1px solid #262a38" }}>
              {k}
            </button>
          ))}
        </div>
        <div className="grid md:grid-cols-2 gap-3">
          <input value={name} onChange={(e) => setName(e.target.value)} placeholder={kind === "SIMBOL" ? "glif (npr. ⟡)" : "ime / beseda"}
            className="px-3 py-2 rounded-lg text-sm outline-none" style={{ background: "#0f1117", border: "1px solid #262a38", color: "#e2e6f0" }} />
          <input value={source} onChange={(e) => setSource(e.target.value)} placeholder="vir (knjižnica / telo — priča)"
            className="px-3 py-2 rounded-lg text-sm outline-none" style={{ background: "#0f1117", border: "1px solid #262a38", color: "#e2e6f0" }} />
        </div>
        <textarea value={body} onChange={(e) => setBody(e.target.value)} rows={4} placeholder="obnova — kaj stvar JE (pozitivni izrek najprej)"
          className="w-full mt-3 px-3 py-2 rounded-lg text-sm outline-none" style={{ background: "#0f1117", border: "1px solid #262a38", color: "#e2e6f0" }} />
      </div>
      <div className="p-4" style={CARD}>
        <div className="text-xs uppercase tracking-widest text-slate-400 mb-2">Izdelek — prilepi v LEKSIKON / register</div>
        <pre className="text-sm whitespace-pre-wrap font-mono" style={{ color: "#a8e6a8" }}>{out}</pre>
      </div>
      <p className="text-xs text-slate-500 px-1">Pečat šele po preverbi v telesu — vnosi brez vira so ⚠ do preverbe. Citat se preveri do izvirnika pred zapečatenjem (rez 610).</p>
    </div>
  );
}

function Nav() {
  const link = ({ isActive }) => ({
    className: "px-3 py-1.5 rounded-lg text-sm font-semibold transition-colors",
    style: {
      background: isActive ? "#e8b445" : "transparent",
      color: isActive ? "#14161d" : "#8f99ad",
      border: "1px solid " + (isActive ? "#e8b445" : "#262a38"),
    },
  });
  return (
    <nav className="flex flex-wrap gap-2 mb-6">
      <NavLink to="/" end {...{ className: undefined }} >
        {({ isActive }) => {
          const l = link({ isActive });
          return <span className={l.className} style={l.style}>Vrata</span>;
        }}
      </NavLink>
      {[
        ["libraries", "Knjižnice"],
        ["lexicon", "Leksikon"],
        ["rezi", "Rezi"],
        ["new", "Nov vnos"],
      ].map(([to, label]) => (
        <NavLink key={to} to={"/" + to}>
          {({ isActive }) => {
            const l = link({ isActive });
            return <span className={l.className} style={l.style}>{label}</span>;
          }}
        </NavLink>
      ))}
    </nav>
  );
}

function Shell({ children }) {
  return (
    <div className="min-h-screen p-6" style={{ background: "#0a0b10", color: "#e2e6f0", fontFamily: "ui-sans-serif, system-ui, sans-serif" }}>
      <div className="max-w-6xl mx-auto">
        <header className="mb-6">
          <h1 className="text-2xl font-bold tracking-wide">
            <span style={{ color: ACCENT }}>∅</span> BESEDA JE NE — <span className="text-slate-300 font-normal">kokpit korpusa</span>
          </h1>
          <p className="text-sm text-slate-500 mt-1">Bistvo je sklad, delovanje je funkcija — pet vrat (rez 620) · stanje 23. 9. 2026</p>
        </header>
        <Nav />
        {children}
      </div>
    </div>
  );
}

export default function App() {
  return (
    <MemoryRouter>
      <Shell>
        <Routes>
          <Route path="/" element={<GatesView />} />
          <Route path="/libraries" element={<LibrariesView />} />
          <Route path="/lexicon" element={<LexiconView />} />
          <Route path="/rezi" element={<ReziView />} />
          <Route path="/new" element={<NewEntryView />} />
        </Routes>
      </Shell>
    </MemoryRouter>
  );
}