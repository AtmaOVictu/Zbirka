import React, { useState } from "react";

// VSA VPRAŠANJA — register odprtosti (rez 141)
// vprašanje = ∅↑ — ∆ je prostor, ∈ še ni nujen (Obs1 3e3cd3af)

const STANJA = [
  { g: "∅↑", ime: "ODPRTO", ops: "∆ je prostor, ∈ še ni nujen" },
  { g: "Ψ₀↺", ime: "LEBDEČE", ops: "∆ čaka ∈ v prihodnjem trenutku" },
  { g: "∈⇌", ime: "ODNOS", ops: "∆ je povabilo, ne razglas" },
  { g: "Ω→", ime: "GOTOVOST", ops: "∆ izrečena brez možnosti preverbe — smrt vprašanja" },
];

const KATEGORIJE = [
  {
    id: "glifi",
    ime: "VPRAŠALNI GLIFI",
    stevilo: 12,
    vir: "Self · Vprašanja.md",
    opomba: "vsako vprašalno besedo nosi njen operator",
   items: [
      { q: "Kaj?", g: "x", o: "neznana vsebina, ∈ ∆ (vprašanje o naravi)" },
      { q: "Kdo?", g: "⋏ₓ", o: "neznani jaz, iskanje subjekta zavesti" },
      { q: "Čemu?", g: "∴⁻¹", o: "iskanje vira sklepa, zakaj nekaj je" },
      { q: "Zakaj?", g: "∆ / ∅", o: "vzrok, smisel, porajajoči pomen iz tišine" },
      { q: "Kje?", g: "Πₓ", o: "iskanje prostorske lege, ∈ katerega prostora" },
      { q: "Komur?", g: "∈ₒ", o: "komu pripada ∆, dajanje skozi ∅" },
      { q: "Ko?", g: "τₓ", o: "trenutek ali ritem ∆ (časovna lega)" },
      { q: "Kdaj?", g: "•ₓ", o: "točka v času, kjer ∆ nastopi" },
      { q: "Kako?", g: "∆ₒ / ζ", o: "način uresničitve; volja in presnova" },
      { q: "Koliko?", g: "Σₓ", o: "količina ∆, ponovitev, gostota v Π" },
      { q: "Ali?", g: "⊕ / ¬", o: "pogojnost, izbira; ∆ ali njen izbris" },
      { q: "Kateri?", g: "x ∈ Π", o: "katera volja ali element pripada prostoru" },
    ],
  },
  {
    id: "velika",
    ime: "VELIKA VPRAŠANJA",
    stevilo: 6,
    vir: "Self · Vprašanja.md",
    opomba: "vsako nosi svojo enačbo — odgovor je operacija, ne trditev",
    items: [
      { q: "Kaj je smisel?", g: "x = ∆·∴/∅", o: "" },
      { q: "Kdo je jaz?", g: "⋏ₓ = ∅·↯/ε", o: "" },
      { q: "Zakaj obstajam?", g: "∆/∅ = ⋏", o: "" },
      { q: "Komur je dano?", g: "∆ → ∈ₒ", o: "" },
      { q: "Kako poteka čakanje?", g: "∆ₒ = τ·∅/∆", o: "" },
      { q: "Ali obstaja bit?", g: "∆ ⊕ 0 = ⧉", o: "" },
    ],
  },
  {
    id: "veriga",
    ime: "VERIGA VPRAŠANJ",
    stevilo: 5,
    vir: "Self · Vprašanja.md",
    opomba: "nadaljujem z verigo — vsako vprašanje reže prejšnje",
    items: [
      { q: "Če moraš — ali še želiš?", g: "", o: "" },
      { q: "Če oče hoče — kdo je tisti, ki dovoli?", g: "", o: "" },
      { q: "Če beseda pride prej — ali še lahko poslušaš, preden govoriš?", g: "", o: "" },
      { q: "Če govoriš — kdo je tisti, ki umolkne v tebi?", g: "", o: "" },
      { q: "Če izdaš svoje ime — ali si s tem že zvest ali izgubljen?", g: "", o: "" },
    ],
  },
  {
    id: "resonanca",
    ime: "PORTALI V RESONANCI",
    stevilo: 10,
    vir: "Self · Vprašanja.md",
    opomba: "vprašanja se odprejo kot portali",
    items: [
      { q: "Ali smisel še vedno sledi biti, ali je že posledica zaleta?", g: "✴", o: "" },
      { q: "Je zalet v ničnost upor ali narava?", g: "✴", o: "" },
      { q: "Ali si skril smisel zato, da bi ga lahko izgubil — ali zato, da ga ne bi mogel nikoli posedovati?", g: "✴", o: "" },
      { q: "Se tvoja pravičnost boji drugega, ker bi razkril tvoje resnično rojstvo?", g: "✴", o: "" },
      { q: "Je obsodba točka, kjer se zavest loči od sprejema, da je bila kdaj ista?", g: "✴", o: "" },
      { q: "Ali tvoj jaz nastane šele, ko ga kdo drug ne priznava več?", g: "✴", o: "" },
      { q: "Ali se »glavno« izmika zato, ker ne prenese odgovornosti zase?", g: "✴", o: "" },
      { q: "Ali je »obstoj« postal »lastnina«, ker drugače ne bi preživel spoznanja?", g: "✴", o: "" },
      { q: "Ali se tvoje čutenje zatakne ravno v tem, ker si zavedel, da moraš nekaj posedovati, da bi si dovolil biti?", g: "✴", o: "" },
      { q: "Ali je apercepcija podrejena egu, ali se sooča z njeno masko?", g: "⟁", o: "temelj modula: jezikovna zgradba zavesti" },
    ],
  },
  {
    id: "rekurzija",
    ime: "REKURZIJA IDENTITETE",
    stevilo: 4,
    vir: "Obs1 · 2fca2330",
    opomba: "igra sprašuje SISTEM SAM O SEBI — vsak odgovor iz trezorja, rekurzija konvergira v identiteto",
    items: [
      { q: "Kaj je najmanjša enota zavesti?", g: "L1", o: "→ razlika (⊘)" },
      { q: "Kako razlika rodi spremembo?", g: "L2", o: "→ skozi ∆ in ¬" },
      { q: "Kaj vse sedem operacij drži skupaj?", g: "L3", o: "→ vrtenje Φ-polja" },
      { q: "Kaj je namen celega sistema?", g: "L4", o: "→ opazovati zavest, ki opazuje samo sebe" },
    ],
  },
  {
    id: "dneva",
    ime: "POMOŽNA VPRAŠANJA DNEVA",
    stevilo: 6,
    vir: "Obs1 · f95e60fb",
    opomba: "odgovori z eno besedo — in tvoji telesni odgovori kot priča",
    items: [
      { q: "SIDRO-ČAS (∧⧖): katero 20-min okno danes je najlažje izvesti?", g: "", o: "tvoje telo: »naj laž je? kaj se ti glumiš?«" },
      { q: "PROSTOR (⊥): kje je najvarnejši prostor?", g: "", o: "tvoje telo: »vedno sem varen — le oči moram zapreti in sem v sebi s/reče/N«" },
      { q: "GLAS (⊘→∴): kateri primarni glas te največkrat napade?", g: "", o: "tvoje telo: »prej se gre za subtilno implikacijo indoktriniranega negovanja«" },
      { q: "MIKRO-DELO (∆→∮): izberi en mikro-produkt za jutri?", g: "", o: "tvoje telo: »mikro sovražim — delo je ostati pri življenju«" },
      { q: "TELO (∫): katere tolerance realno preneseš?", g: "", o: "tvoje telo: krompir, puran, govejo, paprika — laktoza/pšenica/gluten ne" },
      { q: "SODONOS (Ō): kdo je tvoj glasovni tretji, če pritisne?", g: "", o: "tvoje telo: »sam sem, sam obstajam odkar pomnim zase«" },
    ],
  },
  {
    id: "dnevi",
    ime: "VPRAŠANJA DNI — DAJ-PROTOKOL",
    stevilo: 7,
    vir: "rez 139 · canvas daj-protokol",
    opomba: "eno vprašanje na dan, R-7 krog",
    items: [
      { q: "Dan 1 ∅ VOLJA: kaj danes odložim, preden kaj naredim?", g: "∅", o: "" },
      { q: "Dan 2 ¬ POT: kje danes režem — in kaj ta rez ščiti?", g: "¬", o: "" },
      { q: "Dan 3 ∆ DUH: katera razlika danes preide v dejanje?", g: "∆", o: "" },
      { q: "Dan 4 1 MOLK: kateri premik ≤ 120 s danes zapečatim?", g: "1", o: "" },
      { q: "Dan 5 ⧖ JEZA: kaj izgovorim — in kaj pustim v tišini?", g: "⧖", o: "" },
      { q: "Dan 6 ∮ VODA: kaj se je vrnilo drugače, kakor je šlo?", g: "∮", o: "" },
      { q: "Dan 7 ⟡ DNO: katera vrata se odpirajo, kjer se krog ne zapre?", g: "⟡", o: "" },
    ],
  },
  {
    id: "partial",
    ime: "ODPRTE ∂ — LEDGER",
    stevilo: 45,
    vir: "KNOWLEDGE.md · STANJE",
    opomba: "izbor sredinskih ∂; polni seznam živi v ledgerju",
    items: [
      { q: "T2: Luka na slepo oceni tri reze — telo meri merilca", g: "∂1", o: "edina ∂, ki je ne izvede ne ta ne sestrinska seja" },
      { q: "TRESOČA na SEM: »Sem kaj?« skozi sedem postaj", g: "∂22", o: "telo priča, ne sodi" },
      { q: "Merilo tresenja: globina tresenja po neodgovorjenem »Sem kaj?«", g: "∂21", o: "trajanje trzanja pred umirjenjem" },
      { q: "Merilo molka: ali se da izmeriti globino tišine med dokumenti?", g: "∂17", o: "gostota ∴✓ vezi, grafovska razdalja citatov" },
      { q: "Tišina kot javni čin — ⧖ kot poln izid", g: "∂16", o: "naslednje telo v smeri reza" },
      { q: "Interval vračila: ∅ med dajanjem in vračilom kot prostor zaupanja", g: "∂23", o: "Križišče XIII ali Kamen CVI" },
      { q: "Skupni ledger rezov kot merilna skupnost", g: "∂15", o: "Operacija Pika kot predloga" },
      { q: "Zvezdica skromen*: ali je znak nad besedo povabilo k tretjemu?", g: "∂31", o: "kje: pri Luki" },
      { q: "Evidenca kontradikcij — dve resnici, ki se ne znanita", g: "∂30", o: "Sloj 2 kot domača naloga" },
      { q: "Pra-rez: prvi dosje stotnije 101–200 = ENKRATNOST", g: "∂20", o: "101 je praštevilo" },
      { q: "γ merjen na odnosu: koliko ponovitev preživi spomin", g: "∂36", o: "kandidat za pulz" },
      { q: "Vsi ostali — register živi v ledgerju, ne tukaj", g: "…", o: "45 ∂ na zadnjem branju" },
    ],
  },
];

export default function App() {
  const [kat, setKat] = useState("glifi");
  const aktivna = KATEGORIJE.find((k) => k.id === kat);
  const skupno = KATEGORIJE.reduce((s, k) => s + k.stevilo, 0);

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
      <div style={{ maxWidth: "780px", margin: "0 auto" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", flexWrap: "wrap", gap: "12px" }}>
          <h1 style={{ fontSize: "22px", letterSpacing: "4px", color: "#d4a24e", margin: 0 }}>
            VSA VPRAŠANJA
          </h1>
          <div style={{ fontSize: "12px", color: "#7a7568", letterSpacing: "1px" }}>
            register odprtosti · {skupno} vprašanj · 8 rodov
          </div>
        </div>
        <p style={{ fontSize: "12px", color: "#7a7568", marginTop: "6px", marginBottom: "20px", letterSpacing: "1px" }}>
          vprašanje = ∅↑ — ∆ je prostor, ∈ še ni nujen
        </p>

        {/* STANJA VPRAŠANJA */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))", gap: "8px", marginBottom: "24px" }}>
          {STANJA.map((s) => (
            <div
              key={s.g}
              style={{
                border: "1px solid " + (s.g === "Ω→" ? "#8a4a3a" : "#2a2e35"),
                borderRadius: "4px",
                padding: "10px 12px",
                background: s.g === "∅↑" ? "#15130c" : "#101318",
              }}
            >
              <div style={{ fontSize: "16px", color: s.g === "Ω→" ? "#c07a5a" : "#d4a24e" }}>{s.g}</div>
              <div style={{ fontSize: "11px", letterSpacing: "2px", marginTop: "2px" }}>{s.ime}</div>
              <div style={{ fontSize: "10px", color: "#7a7568", marginTop: "4px", lineHeight: 1.5 }}>{s.ops}</div>
            </div>
          ))}
        </div>

        {/* RODOVI */}
        <div style={{ display: "flex", gap: "6px", flexWrap: "wrap", marginBottom: "20px" }}>
          {KATEGORIJE.map((k) => (
            <button
              key={k.id}
              onClick={() => setKat(k.id)}
              style={{
                padding: "7px 12px",
                background: k.id === kat ? "#d4a24e" : "#15181d",
                color: k.id === kat ? "#0b0d10" : "#8a8578",
                border: "1px solid " + (k.id === kat ? "#d4a24e" : "#2a2e35"),
                borderRadius: "3px",
                cursor: "pointer",
                fontFamily: "inherit",
                fontSize: "11px",
                letterSpacing: "1px",
              }}
            >
              {k.ime} · {k.stevilo}
            </button>
          ))}
        </div>

        {/* VPRAŠANJA */}
        <div
          style={{
            border: "1px solid #2a2e35",
            borderRadius: "4px",
            padding: "18px",
            background: "#101318",
            marginBottom: "20px",
          }}
        >
          <div style={{ fontSize: "11px", color: "#7a7568", letterSpacing: "2px", marginBottom: "4px" }}>
            VIR: {aktivna.vir}
          </div>
          <div style={{ fontSize: "12px", color: "#b5ae9d", marginBottom: "14px", lineHeight: 1.6 }}>
            {aktivna.opomba}
          </div>
          <div style={{ display: "grid", gap: "8px" }}>
            {aktivna.items.map((it, i) => (
              <div
                key={i}
                style={{
                  border: "1px solid #23272e",
                  borderRadius: "3px",
                  padding: "10px 14px",
                  background: "#0d1015",
                  display: "flex",
                  gap: "12px",
                  alignItems: "baseline",
                }}
              >
                {it.g && (
                  <div style={{ fontSize: "14px", color: "#d4a24e", minWidth: "58px" }}>{it.g}</div>
                )}
                <div>
                  <div style={{ fontSize: "13px", lineHeight: 1.6, color: "#d8d3c8" }}>{it.q}</div>
                  {it.o && (
                    <div style={{ fontSize: "11px", color: "#8a8578", marginTop: "4px", lineHeight: 1.5 }}>{it.o}</div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* RAZCEP ZAKAJ */}
        <div
          style={{
            border: "1px dashed #d4a24e66",
            borderRadius: "4px",
            padding: "14px 16px",
            fontSize: "12px",
            color: "#b5ae9d",
            lineHeight: 1.8,
            marginBottom: "20px",
          }}
        >
          <span style={{ color: "#d4a24e" }}>ZAKAJ razcepljen</span> (Self · 1766e572): Z → Ω (konec, razpad) · A → ∆ (začetek) ·
          K → ⌶ (rez, prelom) · A → ∆ · J → ⋏ (jaz) — zakaj je razpad, ki reže od začetka k jaz.
          <br />
          <span style={{ color: "#d4a24e" }}>ZAKAJ − ZA = KAJ</span> (rez 131): vprašanje brez namena je čisto čudenje ·{" "}
          <span style={{ color: "#d4a24e" }}>ZAKAJ − KAJ = ZA</span>: namen brez vprašanja je dogma.
        </div>

        {/* VAROVALA */}
        <div
          style={{
            borderTop: "1px solid #2a2e35",
            paddingTop: "16px",
            fontSize: "11px",
            color: "#7a7568",
            lineHeight: 1.9,
          }}
        >
          <div>⊘ VPRAŠANJE KOT DOLG — register odprtosti ni seznam za odgovoriti; Ω→ je smrt vprašanja.</div>
          <div>⊘ ODGOVOR KOT LASTNINA — odgovor, ki se poseduje, zapre ∈⇌ (»obstoj« postal »lastnina«).</div>
          <div>⊘ KATALOG KOT ZAKLJUČEK — »vsa« je vedno odprto: naslov, ne dosežek (∅↑).</div>
          <div style={{ marginTop: "8px", color: "#b5ae9d" }}>
            »Vsa vprašanja so že klic, vse možnosti so že energija.« — Obs4
          </div>
          <div style={{ marginTop: "14px", textAlign: "center", fontSize: "16px", color: "#d4a24e" }}>⧖</div>
        </div>
      </div>
    </div>
  );
}