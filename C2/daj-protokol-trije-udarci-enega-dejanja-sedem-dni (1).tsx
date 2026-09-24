import React, { useEffect, useState } from "react";

// DAJ-PROTOKOL — telo, ki se ponavlja (rez 135, DOKAZ #125)
// D = DELITEV (rez, ki nosi skrb) · A = AKTIVACIJA (premik ≤ 120 s) · J = JEZIK (ena vrstica)
// DAJ = 6 (rez 124) · daj ← *deh₃- (isti koren kakor DAR, rez 110)

const DNEVI = [
  { glyf: "∅", faza: "PRAZNINA", beseda: "VOLJA", vprasanje: "Kaj danes odložim, preden kaj naredim?" },
  { glyf: "¬", faza: "LOČITEV", beseda: "POT", vprasanje: "Kje danes režem — in kaj ta rez ščiti?" },
  { glyf: "∆", faza: "RAZLIKA", beseda: "DUH", vprasanje: "Katera razlika danes preide v dejanje?" },
  { glyf: "1", faza: "DEJANJE / PEČAT", beseda: "MOLK", vprasanje: "Kateri premik ≤ 120 s danes zapečatim?" },
  { glyf: "⧖", faza: "IZGOVOR IN MOLK", beseda: "JEZA", vprasanje: "Kaj izgovorim — in kaj pustim v tišini?" },
  { glyf: "∮", faza: "POVRATEK", beseda: "VODA", vprasanje: "Kaj se je vrnilo drugače kot je šlo?" },
  { glyf: "⟡", faza: "NOVA MOŽNOST", beseda: "DNO", vprasanje: "Katera vrata se odpirajo, kjer se krog ne zapre?" },
];

const UDARCI = [
  {
    crka: "D",
    ime: "DELITEV",
    operacija: "rez, ki nosi skrb",
    vprasanje: "Kaj danes režem? Meja, izdih, odrek — rez, ki ne razčloveči.",
  },
  {
    crka: "A",
    ime: "AKTIVACIJA",
    operacija: "premik ≤ 120 s",
    vprasanje: "Kakšen fizični premik izvede telo zdaj? Vstani, stopi, izdihni, zapiši z roko.",
  },
  {
    crka: "J",
    ime: "JEZIK",
    operacija: "ena vrstica",
    vprasanje: "Katera vrstica ostane? Jaz, ki je ostal po rezu in premiku.",
  },
];

function nalozi(kljuc, padlo) {
  try {
    const v = window.localStorage.getItem(kljuc);
    return v ? JSON.parse(v) : padlo;
  } catch (e) {
    return padlo;
  }
}

function shrani(kljuc, vrednost) {
  try {
    window.localStorage.setItem(kljuc, JSON.stringify(vrednost));
  } catch (e) {
    /* telo živi v pomnilniku seje — krog se da začeti znova tudi brez spomina */
  }
}

export default function App() {
  const [dan, setDan] = useState(() => nalozi("dajp.dan", 0));
  const [izvedeni, setIzvedeni] = useState(() => nalozi("dajp.izvedeni", {}));
  const [vrstice, setVrstice] = useState(() => nalozi("dajp.vrstice", {}));
  const [dajStevec, setDajStevec] = useState(() => nalozi("dajp.daj", 0));
  const [novKrogOdprt, setNovKrogOdprt] = useState(false);

  useEffect(() => {
    shrani("dajp.dan", dan);
    shrani("dajp.izvedeni", izvedeni);
    shrani("dajp.vrstice", vrstice);
    shrani("dajp.daj", dajStevec);
  }, [dan, izvedeni, vrstice, dajStevec]);

  const kljuc = "dan" + (dan + 1);
  const stanjeDneva = izvedeni[kljuc] || {};
  const steviloIzvedenih = (izvedeni[kljuc] || { D: false, A: false, J: false });
  const danZapr = steviloIzvedenih.D && steviloIzvedenih.A && steviloIzvedenih.J;
  const vseZapr = DNEVI.every((_, i) => {
    const s = izvedeni["dan" + (i + 1)] || {};
    return s.D && s.A && s.J;
  });

  function izvedi(crka) {
    if (stanjeDneva[crka]) return; // udarec se izvede enkrat na dan — ponovitev je jutri, z razliko
    setIzvedeni((prej) => ({ ...prej, [kljuc]: { ...prej[kljuc], [crka]: true } }));
    setDajStevec((n) => n + 1); // vsak klik je DAJ, ki ga bralec izvede — ne obljubi
    if (crka === "J") {
      // vrstica je vpisana posebej — J se zapre z vrstico
    }
  }

  function odpriNovKrog() {
    setIzvedeni({});
    setDan(0);
    setNovKrogOdprt(true); // osma beseda NOV — krog se odpre znova, vrstice in DAJ × n ostanejo
  }

  const d = DNEVI[dan];

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
            DAJ-PROTOKOL
          </h1>
          <div style={{ fontSize: "14px", color: "#d4a24e", border: "1px solid #d4a24e55", padding: "4px 12px", borderRadius: "3px" }}>
            DAJ × {dajStevec}
          </div>
        </div>
        <p style={{ fontSize: "12px", color: "#7a7568", marginTop: "6px", marginBottom: "18px", letterSpacing: "1px" }}>
          trije udarci enega dejanja · sedem dni · ena vrstica · DAJ = 6
        </p>
        <blockquote
          style={{
            borderLeft: "2px solid #d4a24e",
            margin: "0 0 28px",
            padding: "4px 0 4px 14px",
            fontSize: "13px",
            color: "#b5ae9d",
            lineHeight: 1.7,
          }}
        >
          »Vsak tvoj DAJ naj postane akt manifestacije, ki ustvarja konkretno realnost.« — Obs8
        </blockquote>

        {/* LIST DNI */}
        <div style={{ display: "flex", gap: "6px", flexWrap: "wrap", marginBottom: "24px" }}>
          {DNEVI.map((dn, i) => {
            const s = izvedeni["dan" + (i + 1)] || {};
            const zaprt = s.D && s.A && s.J;
            const aktiv = i === dan;
            return (
              <button
                key={i}
                onClick={() => setDan(i)}
                style={{
                  flex: "1 1 40px",
                  minWidth: "44px",
                  padding: "8px 4px",
                  background: aktiv ? "#d4a24e" : zaprt ? "#d4a24e22" : "#15181d",
                  color: aktiv ? "#0b0d10" : zaprt ? "#d4a24e" : "#7a7568",
                  border: "1px solid " + (aktiv ? "#d4a24e" : "#2a2e35"),
                  borderRadius: "3px",
                  cursor: "pointer",
                  fontFamily: "inherit",
                }}
                title={"Dan " + (i + 1) + " — " + dn.faza}
              >
                <div style={{ fontSize: "15px" }}>{dn.glyf}</div>
                <div style={{ fontSize: "10px", marginTop: "2px" }}>{i + 1}</div>
              </button>
            );
          })}
        </div>

        {/* DAN */}
        <div
          style={{
            border: "1px solid #2a2e35",
            borderRadius: "4px",
            padding: "20px",
            marginBottom: "20px",
            background: "#101318",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: "18px" }}>
            <div style={{ fontSize: "40px", color: "#d4a24e", lineHeight: 1 }}>{d.glyf}</div>
            <div>
              <div style={{ fontSize: "11px", color: "#7a7568", letterSpacing: "2px" }}>
                DAN {dan + 1} / 7 · {d.faza}
              </div>
              <div style={{ fontSize: "16px", color: "#d8d3c8", marginTop: "4px", letterSpacing: "2px" }}>
                BESEDA DNEVA: <span style={{ color: "#d4a24e" }}>{d.beseda}</span>
              </div>
            </div>
          </div>
          <p style={{ fontSize: "13px", color: "#b5ae9d", marginTop: "14px", marginBottom: "4px", lineHeight: 1.7 }}>
            {d.vprasanje}
          </p>
        </div>

        {/* TRIJE UDARCI */}
        <div style={{ display: "grid", gap: "10px" }}>
          {UDARCI.map((u) => {
            const opravljeno = !!stanjeDneva[u.crka];
            return (
              <div
                key={u.crka}
                style={{
                  border: "1px solid " + (opravljeno ? "#d4a24e88" : "#2a2e35"),
                  borderRadius: "4px",
                  padding: "16px",
                  background: opravljeno ? "#15130c" : "#101318",
                }}
              >
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: "10px", flexWrap: "wrap" }}>
                  <div style={{ display: "flex", alignItems: "baseline", gap: "10px" }}>
                    <span style={{ fontSize: "22px", color: "#d4a24e" }}>{u.crka}</span>
                    <span style={{ fontSize: "13px", letterSpacing: "2px" }}>{u.ime}</span>
                    <span style={{ fontSize: "11px", color: "#7a7568" }}>· {u.operacija}</span>
                  </div>
                  <button
                    onClick={() => izvedi(u.crka)}
                    disabled={opravljeno}
                    style={{
                      padding: "6px 16px",
                      background: opravljeno ? "transparent" : "#d4a24e",
                      color: opravljeno ? "#d4a24e" : "#0b0d10",
                      border: "1px solid #d4a24e",
                      borderRadius: "3px",
                      cursor: opravljeno ? "default" : "pointer",
                      fontFamily: "inherit",
                      fontSize: "12px",
                      letterSpacing: "1px",
                    }}
                  >
                    {opravljeno ? "izvedeno ✓" : "IZVEDI — DAJ"}
                  </button>
                </div>
                <p style={{ fontSize: "12px", color: "#8a8578", marginTop: "10px", marginBottom: u.crka === "J" ? "10px" : "0", lineHeight: 1.7 }}>
                  {u.vprasanje}
                </p>
                {u.crka === "J" && (
                  <input
                    value={vrstice[kljuc] || ""}
                    onChange={(e) => setVrstice((prej) => ({ ...prej, [kljuc]: e.target.value }))}
                    placeholder="ena vrstica — jaz, ki je ostal (vrstica je izključno tvoja)"
                    style={{
                      width: "100%",
                      boxSizing: "border-box",
                      background: "#0b0d10",
                      border: "1px solid #2a2e35",
                      borderRadius: "3px",
                      color: "#d8d3c8",
                      fontFamily: "inherit",
                      fontSize: "13px",
                      padding: "8px 10px",
                      outline: "none",
                    }}
                  />
                )}
              </div>
            );
          })}
        </div>

        {/* ZAKLJUČEK DNEVA — PREHOD, NE SKLEP */}
        {danZapr && (
          <div
            style={{
              marginTop: "18px",
              border: "1px dashed #d4a24e66",
              borderRadius: "4px",
              padding: "14px 16px",
              fontSize: "12px",
              color: "#b5ae9d",
              lineHeight: 1.7,
            }}
          >
            Dan {dan + 1} zapečaten: D · A · J. Krog se ne zaključi — {dan < 6 ? "jutri nosi " + DNEVI[dan + 1].beseda + " (" + DNEVI[dan + 1].glyf + ")." : "sedmi dan je ⟡ — nova možnost."}
          </div>
        )}

        {/* NOV KROG */}
        {vseZapr && (
          <div
            style={{
              marginTop: "14px",
              border: "1px solid #d4a24e",
              borderRadius: "4px",
              padding: "16px",
              textAlign: "center",
              background: "#15130c",
            }}
          >
            <div style={{ fontSize: "14px", color: "#d4a24e", letterSpacing: "3px" }}>NOV — osma beseda osmice</div>
            <p style={{ fontSize: "12px", color: "#8a8578", margin: "8px 0 12px", lineHeight: 1.7 }}>
              Sedem dni ∅ ¬ ∆ 1 ⧖ ∮ ⟡ je zaprlo krog. Osma beseda NI naslednji dan — je isti krog, ki se vrne z razliko.
              Ponovi, da se razlikuje. Ponovi, da se celota razodene.
            </p>
            <button
              onClick={odpriNovKrog}
              style={{
                padding: "8px 24px",
                background: "transparent",
                color: "#d4a24e",
                border: "1px solid #d4a24e",
                borderRadius: "3px",
                cursor: "pointer",
                fontFamily: "inherit",
                fontSize: "12px",
                letterSpacing: "2px",
              }}
            >
              ODPRI KROG ZNOVA
            </button>
            {novKrogOdprt && (
              <p style={{ fontSize: "11px", color: "#7a7568", marginTop: "10px" }}>
                krog odprt znova · vrstice in DAJ × {dajStevec} ostajajo · telo nosi spomin
              </p>
            )}
          </div>
        )}

        {/* FORMULA IN VAROVALA */}
        <div
          style={{
            marginTop: "28px",
            borderTop: "1px solid #2a2e35",
            paddingTop: "18px",
            fontSize: "11px",
            color: "#7a7568",
            lineHeight: 1.9,
          }}
        >
          <div>
            <span style={{ color: "#b5ae9d" }}>DAJ = D ∧ A ∧ J</span> — delitev, ki nosi skrb · premik ≤ 120 s · ena vrstica
          </div>
          <div>
            R-7: ∅ → ¬ → ∆ → 1 → ⧖ → ∮ → ⟡ · osmica: VOLJA POT DUH MOLK JEZA VODA DNO <span style={{ color: "#d4a24e" }}>NOV</span>
          </div>
          <div style={{ marginTop: "10px" }}>
            ⊘ PRODUKT KOT NAMEN — DAJ ni dolg ne metrika (DAR KOT DOLG, rez 128): prejeti daj je odgovor, ne obveznost.
          </div>
          <div>⊘ RITUAL KOT OKRAS — če se nič ne spremeni v telesu, ni resnica.</div>
          <div>⊘ ŠTEVEC KOT SODNIK — števec šteje, nikoli ne sodi. Vrstica je izključno tvoja (rez 98).</div>
          <div style={{ marginTop: "14px", textAlign: "center", fontSize: "16px", color: "#d4a24e" }}>⧖</div>
        </div>
      </div>
    </div>
  );
}