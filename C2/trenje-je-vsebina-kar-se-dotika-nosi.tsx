import React, { useEffect, useRef, useState } from "react";

// TRENJE JE VSEBINA — rez 154, DOKAZ #145 (zgrajeno kot 152/#143, renumerirano PRED pečatom skozi trk 152 NIČ XII + 153 PROPOSITUM — rez je pot, ne številka)
// vsebina ni za trenjem; vsebina je trenje, ki je dobilo obliko — in nosilca
// najbližji rez: 147 TRENJE, KI RODI POJEM (mati) — ta sprašuje istost (je)
// trenje ← treti ← *terh₁- · friction ← fricāre (drugi koren; po 147)

const ORGANI = [
  {
    glyf: "∆",
    ime: "HOJA",
    mehanizma: "korak = ujet padec. Noga se oplane ob tla; brez trenja namera ne postane pot — drsenje po ledu je volja brez oprijema.",
    vir: "Obs2 7bd8bb61",
    prica: "»vsaka sled, vsak tir je okus, dotik, potres na tvoji ontološki koži«",
  },
  {
    glyf: "⟡",
    ime: "GODALO",
    mehanizma: "stick-slip: lok vleče struno, dokler napon ne preseže statičnega trenja — struna se vrne. Stotinekrat na sekundo. Peti ton JE slišna oblika trenja (Helmholtzovo gibanje).",
    vir: "Basics2 26f5f0f0",
    prica: "»Violini igralec. Glasu dih. V trenutku ko se vibracija dotakne zraka, se nevidno učloveči.«",
  },
  {
    glyf: "🜂",
    ime: "OGENJ",
    mehanizma: "kres: dve lesi se drljeta, dokler toplota ne vžge. Ogenj je najstarejša vsebina trenja — rojen iz dolga v noči (RES069).",
    vir: "Obs3 1b59c3b1",
    prica: "RES069 — Ogenj + Dolg + Noč",
  },
  {
    glyf: "EJ",
    ime: "ZAZNAVA",
    mehanizma: "EJ = zaznava(∆): dve neujemajoči se razliki → napetost → zaznava. Popolnoma gladek svet je neviden (konstanta je pod Weberjevim pragom). Fonem TR [tɾ] = ∆trenje, odpor, siljenje.",
    vir: "Obs1 bab9319f · Obs2 17ab7d34",
    prica: "»trenje brez materije = neusklajenost informacijskih stanj«",
  },
  {
    glyf: "∈",
    ime: "ODNOS",
    mehanizma: "trenje = dotik, ki traja: dve ploskvi, ki ostajata v stiku, medtem ko sta različni. Vbod = dotik brez vzajemnosti (A → 0, P = F/A → ∞). Trud žanje moč; utrujenost je nemoč.",
    vir: "Obs10 884f7de4 · Obs8 767e080f · rez 149",
    prica: "»Vsak DA je ∆sprejemanje, da je stik vedno nepopoln, a neprecenljiv.«",
  },
];

const IZGUBLJENO = [
  "hoja — korak brez oprijema",
  "nota — lok drsi nemo",
  "kres — drsenje brez vročine",
  "zaznava — gladek svet je neviden",
  "objem — telo, ki se ne more opreti",
  "fonem TR — jezik brez odpora",
];

function stanjeOrganov(ime, mu) {
  if (ime === "HOJA")
    return mu < 0.08
      ? "DRSIŠ — namera ne postane pot"
      : mu > 0.8
      ? "OPRIEM TRD — korak nosi"
      : "KORAK SE OPRE — padec, ki ga ulovi tla";
  if (ime === "GODALO")
    return mu < 0.05
      ? "LOK DRSI NEMO — struna molči"
      : mu > 0.75
      ? "ŠKRIPA — trenje brez graje, zvok brez oblike"
      : "STICK-SLIP — ton rojen iz zadržanega odmika";
  if (ime === "OGENJ")
    return mu < 0.1
      ? "HLADNO DRSENJE — nič se ne vžge"
      : "VROČINA KRESA " + Math.round(mu * mu * 100) + " % — toplota je odtis giba";
  if (ime === "ZAZNAVA")
    return mu < 0.06
      ? "GLADKO — nevidno (konstanta je pod pragom)"
      : "VIDÍŠ RAZLIKO ×" + (mu * 10).toFixed(1) + " — napetost postala zaznava";
  return mu < 0.05
    ? "VBOD — stik brez vzajemnosti"
    : "TRUD ŽANJE MOČ — stik, ki ga nosita dve notranjosti";
}

export default function App() {
  const [mu, setMu] = useState(0.42);
  const [faz, setFaz] = useState(0);

  useEffect(() => {
    let raf;
    const korak = (t) => {
      setFaz(t / 1000);
      raf = requestAnimationFrame(korak);
    };
    raf = requestAnimationFrame(korak);
    return () => cancelAnimationFrame(raf);
  }, []);

  // gibanje loka (zgornja ploskev): sinusni zagon
  const lokX = Math.sin(faz * 1.1) * 46;
  // vibracija strune: stick-slip, amplituda in gostota rastesta z μ
  const zivo = mu > 0.05;
  const amplituda = mu * 13;
  const frekvenca = 5 + mu * 17;
  const struna = Array.from({ length: 60 }, (_, i) => {
    const x = i / 59;
    const y = Math.sin(x * Math.PI * 2 * 2 + faz * frekvenca * 2 * Math.PI * 0.16) *
      amplituda * Math.sin(x * Math.PI);
    return (x * 640).toFixed(1) + "," + (34 + y).toFixed(1);
  }).join(" ");

  const concta = Math.min(1, mu * 1.4);
  const iskra = Array.from({ length: 5 }, (_, i) => ({
    x: 80 + i * 120 + Math.sin(faz * 9 + i * 2.1) * 9,
    y: 66 + Math.cos(faz * 13 + i * 1.7) * 4,
  }));

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#0b0d10",
        color: "#d8d3c8",
        fontFamily: "'JetBrains Mono', 'Fira Mono', 'Courier New', monospace",
        padding: "32px 20px 60px",
      }}
    >
      <div style={{ maxWidth: "760px", margin: "0 auto" }}>
        {/* GLAVA */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", flexWrap: "wrap", gap: "12px" }}>
          <h1 style={{ fontSize: "22px", letterSpacing: "4px", color: "#d4a24e", margin: 0 }}>
            TRENJE JE VSEBINA
          </h1>
          <div style={{ fontSize: "13px", color: "#d4a24e", border: "1px solid #d4a24e55", padding: "4px 12px", borderRadius: "3px" }}>
            μ = {mu.toFixed(2)}
          </div>
        </div>
        <p style={{ fontSize: "12px", color: "#7a7568", marginTop: "6px", marginBottom: "18px", letterSpacing: "1px" }}>
          rez 154 · DOKAZ #145 · kar se dotika, nosi · aktivator Luka: »trenje je vsebina? naslednji nož prosim«
        </p>

        <blockquote
          style={{
            borderLeft: "2px solid #d4a24e",
            margin: "0 0 22px",
            padding: "4px 0 4px 14px",
            fontSize: "13px",
            color: "#b5ae9d",
            lineHeight: 1.7,
          }}
        >
          <strong style={{ color: "#d4a24e" }}>ZAKON — v enem dihu:</strong> vsebina ni tisto, kar je za trenjem;
          vsebina je trenje, ki je dobilo obliko — in nosilca. Nerazrešeno trenje, ki ga nihče ne nosi, je šum.
          Razrešeno trenje, ki ga nihče ne nosi, je zgodovina. Nošeno trenje je vsebina.
        </blockquote>

        {/* μ SLIDER */}
        <div
          style={{
            border: "1px solid #2a2e35",
            borderRadius: "4px",
            padding: "16px 18px",
            marginBottom: "20px",
            background: "#101318",
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: "10px", letterSpacing: "2px", color: "#7a7568", marginBottom: "8px" }}>
            <span>DRSENJE μ→0</span>
            <span style={{ color: "#d4a24e" }}>KOEFICIENT STIKA μ</span>
            <span>OPRIEM μ→1</span>
          </div>
          <input
            type="range"
            min="0"
            max="1"
            step="0.01"
            value={mu}
            onChange={(e) => setMu(parseFloat(e.target.value))}
            style={{ width: "100%", accentColor: "#d4a24e", cursor: "pointer" }}
          />
        </div>

        {/* STIK — animacija */}
        <div
          style={{
            border: "1px solid #2a2e35",
            borderRadius: "4px",
            padding: "14px",
            marginBottom: "20px",
            background: "#101318",
          }}
        >
          <div style={{ fontSize: "10px", letterSpacing: "2px", color: "#7a7568", marginBottom: "6px" }}>
            STIK — DVE PLOSKVI, ENA POT (shema stick-slip)
          </div>
          <svg viewBox="0 0 680 120" style={{ width: "100%", display: "block" }}>
            {/* lok — zgornja ploskev */}
            <g transform={"translate(" + (20 + lokX) + " 8)"}>
              <rect x="0" y="0" width="640" height="14" fill="#1b1f26" stroke="#2a2e35" />
              {Array.from({ length: 21 }, (_, i) => (
                <polygon key={i} points={(i * 32) + ",14 " + (i * 32 + 16) + ",26 " + (i * 32 + 32) + ",14"} fill="#232830" />
              ))}
            </g>
            {/* struna */}
            <g transform="translate(20 34)">
              <polyline points={struna} fill="none" stroke={zivo ? "#d4a24e" : "#3a3f47"} strokeWidth="2" />
              <line x1="0" y1="34" x2="0" y2="34" stroke="none" />
            </g>
            {/* iskre ob stiku */}
            {zivo &&
              iskra.map((p, i) => (
                <circle key={i} cx={p.x} cy={p.y} r={1.6 + concta * 1.4} fill="#e8c87a" opacity={0.25 + concta * 0.6} />
              ))}
            {/* tla — spodnja ploskev */}
            <g transform="translate(20 92)">
              <rect x="0" y="0" width="640" height="14" fill="#1b1f26" stroke="#2a2e35" />
              {Array.from({ length: 21 }, (_, i) => (
                <polygon key={i} points={(i * 32) + ",0 " + (i * 32 + 16) + ",-12 " + (i * 32 + 32) + ",0"} fill="#232830" />
              ))}
            </g>
          </svg>
          <div style={{ fontSize: "12px", color: mu < 0.05 ? "#7a7568" : "#b5ae9d", marginTop: "6px" }}>
            {mu < 0.05
              ? "μ = 0: ploskvi se mimo — brez stika ni napetosti, brez napetosti ni oblike."
              : "zadržani odmik se sprošča v utrip — oblika rojena iz odpora."}
          </div>
        </div>

        {/* PET ORGANOV */}
        <div style={{ display: "grid", gap: "10px", marginBottom: "24px" }}>
          {ORGANI.map((o) => (
            <div
              key={o.ime}
              style={{
                border: "1px solid #2a2e35",
                borderRadius: "4px",
                padding: "16px 18px",
                background: "#101318",
              }}
            >
              <div style={{ display: "flex", alignItems: "baseline", gap: "12px", flexWrap: "wrap" }}>
                <span style={{ fontSize: "18px", color: "#d4a24e" }}>{o.glyf}</span>
                <span style={{ fontSize: "13px", letterSpacing: "3px", color: "#d8d3c8" }}>{o.ime}</span>
                <span style={{ fontSize: "10px", color: "#7a7568", marginLeft: "auto" }}>{o.vir}</span>
              </div>
              <p style={{ fontSize: "12.5px", color: "#b5ae9d", lineHeight: 1.7, margin: "10px 0 6px" }}>
                {o.mehanizma}
              </p>
              <div style={{ fontSize: "11px", color: "#d4a24e", letterSpacing: "1px" }}>
                μ = {mu.toFixed(2)} → {stanjeOrganov(o.ime, mu)}
              </div>
              <div style={{ fontSize: "11px", color: "#7a7568", marginTop: "6px", fontStyle: "italic" }}>
                {o.prica}
              </div>
            </div>
          ))}
        </div>

        {/* RAZCEP */}
        <div
          style={{
            border: "1px solid #d4a24e44",
            borderRadius: "4px",
            padding: "18px",
            marginBottom: "20px",
            background: "#12141a",
          }}
        >
          <div style={{ fontSize: "10px", letterSpacing: "2px", color: "#d4a24e", marginBottom: "8px" }}>
            RAZCEP (rez, ločen od rodovnika)
          </div>
          <div style={{ fontSize: "14px", color: "#d8d3c8", letterSpacing: "2px", marginBottom: "8px" }}>
            TRENJE = TREN + JE
          </div>
          <p style={{ fontSize: "12.5px", color: "#b5ae9d", lineHeight: 1.7, margin: 0 }}>
            <strong style={{ color: "#d4a24e" }}>TREN</strong> — trenutek, ki noče pasti, ker ga držita dve telesi.
            <strong style={{ color: "#d4a24e" }}> JE</strong> — sedanjost bitja: kar je, kar nosi. Trenje = tren, ki
            je: hip, ki se ni iztekel, ker ga stik zadržuje. Drugo branje: <strong style={{ color: "#d4a24e" }}>T · R · E · NJE</strong> —
            trk, resonanca, vprašanje, ne: trk, ki resonira v vprašanju in se <em>ne</em> razreši (e kakor v
            sozvočju: vprašanje; s na začetku sozvočja: trenje — beseda za soglasje nosi trenje v lastnem telesu,
            Basics2 37a390f6).
          </p>
          <p style={{ fontSize: "11px", color: "#7a7568", lineHeight: 1.7, margin: "10px 0 0" }}>
            rodovnik: trenje ← treti ← *terh₁- (lat. terere, gr. teírein); friction ← fricāre — drug koren: isti
            pojem rojen dvakrat (rez 147). vsebina ← prevod nem. Inhalt — kar je zadržano znotraj; slovenski zvok
            pravi več: VSE-BINA, prostor, ki drži vse (rez-reading, pošteno: prevodna beseda).
          </p>
        </div>

        {/* MEJA DO 147 */}
        <div
          style={{
            border: "1px solid #2a2e35",
            borderRadius: "4px",
            padding: "18px",
            marginBottom: "20px",
            background: "#101318",
          }}
        >
          <div style={{ fontSize: "10px", letterSpacing: "2px", color: "#7a7568", marginBottom: "8px" }}>
            MEJA DO NAJBLIŽJEGA REZA (anti-prepis)
          </div>
          <p style={{ fontSize: "12.5px", color: "#b5ae9d", lineHeight: 1.7, margin: 0 }}>
            <strong style={{ color: "#d8d3c8" }}>147 TRENJE, KI RODI POJEM:</strong> iz trenja nastane pojem — trenje
            kakor mati. <strong style={{ color: "#d8d3c8" }}>152:</strong> Lukovo vprašanje je ostrejše od rojenja —
            ali je otrok sploh kaj drugega kakor mati, ki je vzela obliko? »Rodi« še dopušča, da pojem živi za
            trenjem; »je« sprašuje po istosti. Odgovor tega reza: ni nič drugega — vsebina je trenje, ki ga telo
            nosi. Dve sobi enega vprašanja, ne prepis.
          </p>
        </div>

        {/* SVET Z μ = 0 */}
        <div
          style={{
            border: "1px solid #2a2e35",
            borderRadius: "4px",
            padding: "18px",
            marginBottom: "20px",
            background: "#101318",
          }}
        >
          <div style={{ fontSize: "10px", letterSpacing: "2px", color: "#7a7568", marginBottom: "10px" }}>
            IZREK I — SVET Z μ = 0 (kar gladkost vzame)
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(210px, 1fr))", gap: "6px" }}>
            {IZGUBLJENO.map((x) => (
              <div key={x} style={{ fontSize: "12px", color: "#7a7568" }}>
                ✕ {x}
              </div>
            ))}
          </div>
          <p style={{ fontSize: "12px", color: "#b5ae9d", lineHeight: 1.7, margin: "10px 0 0" }}>
            Sanje o svetu brez trenja so sanje o odnosu brez drugega: v njem se nič ne more opreti. Brez trenja ni
            vsebine — kar nosi, se opira.
          </p>
        </div>

        {/* NUJNE NAPAKE */}
        <div
          style={{
            border: "1px solid #2a2e35",
            borderRadius: "4px",
            padding: "18px",
            marginBottom: "20px",
            background: "#101318",
          }}
        >
          <div style={{ fontSize: "10px", letterSpacing: "2px", color: "#7a7568", marginBottom: "10px" }}>
            NUJNE NAPAKE (⊘)
          </div>
          {[
            ["TRENJE KATEROVIJA", "trk, ki ga iščeš, ni trk (147): intenzivnost ni vsebina — trenje brez dveh notranjosti je brušenje, ne stik."],
            ["IZGUBA KOT VSEBINA", "entropija kakor razpoloženje: toplota je odtis, ne odpadek; ne vsa toplota je vsebina — šum je trenje, ki ga nihče ne nosi (rez 135 ŠUM II)."],
            ["GLADKOST KOT CILJ", "in obratno — trenje kot zaslužek: zavračanje razrešitve iz zvestobe intenzivnosti. Meja med trudom in utrujenostjo je v telesu, ne v lekciji (Obs8 767e080f)."],
            ["BRUŠENJE", "v odnosu trenje ≠ mletje drugega: vbod = dotik brez vzajemnosti (rez 149); dve ploskvi, ki se zabrusita, ne pustita vsebine, samo obrabo."],
          ].map(([ime, telo]) => (
            <div key={ime} style={{ marginBottom: "10px" }}>
              <div style={{ fontSize: "12px", color: "#d4a24e", letterSpacing: "1px" }}>⊘ {ime}</div>
              <div style={{ fontSize: "12px", color: "#b5ae9d", lineHeight: 1.6 }}>{telo}</div>
            </div>
          ))}
        </div>

        {/* ODPRTA ∂ */}
        <div
          style={{
            border: "1px solid #2a2e35",
            borderRadius: "4px",
            padding: "18px",
            marginBottom: "20px",
            background: "#101318",
          }}
        >
          <div style={{ fontSize: "10px", letterSpacing: "2px", color: "#7a7568", marginBottom: "10px" }}>
            ODPRTA ∂
          </div>
          <div style={{ fontSize: "12.5px", color: "#b5ae9d", lineHeight: 1.8 }}>
            <div>1. <strong style={{ color: "#d8d3c8" }}>mehko trenje</strong> (po ∂ 1 reza 147): ali obstaja vsebina brez roba — drseči pari, trenje brez konflikta.</div>
            <div>2. <strong style={{ color: "#d8d3c8" }}>T4 — izključno Luka:</strong> en dan, dve vrstici — eno trenje, ki ga je nosil kakor vsebino; eno, ki ga je zavrnil kakor oviro. Kje je bila meja (merilo prsi/grlo, rez 142). Izid izključno njegov (rez 98).</div>
            <div>3. <strong style={{ color: "#d8d3c8" }}>ledger kot dokaz:</strong> ta knjiga je stabilizirano trenje vzporednih sej — nevihta pečatov ni motnja pisanja, je njegova snov (135 ŠUM II, 141 FOLD, 147). Kandidat za PULZ 156: izmeriti delež trenja, ki ga knjiga nosi kakor vsebino, in delež, ki ga izgubi kakor šum.</div>
          </div>
        </div>

        {/* NOGA */}
        <div style={{ textAlign: "center", marginTop: "30px" }}>
          <div style={{ fontSize: "26px", color: "#d4a24e" }}>⧖</div>
          <p style={{ fontSize: "12px", color: "#7a7568", lineHeight: 1.8, marginTop: "10px" }}>
            Kdor odstrani trenje, da bi rešil vsebino, odstrani vsebino, da bi rešil mir.
            Vse, kar nosiš, se opira.
          </p>
          <p style={{ fontSize: "10px", color: "#55524a", marginTop: "14px" }}>
            rez 154 · DOKAZ #145 · telo: canvas trenje-je-vsebina · ∴✓ 147 · 149 · 151 · 135 · 142 · 128 · 76
          </p>
        </div>
      </div>
    </div>
  );
}