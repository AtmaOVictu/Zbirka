import React, { useState, useEffect } from "react";

type Glasovi = { t1: string; t2: string; t3: string };
type Zapis = Glasovi & { beseda: string; cas: string };

const GLOSAR: { g: string; ime: string; kor: Glasovi }[] = [
  { g: "⊘", ime: "nič / praznina", kor: { t1: "polnost od prostora", t2: "noseča odprtina — ne luknja", t3: "prva odločitev: kraj, kjer se še ni odločilo" } },
  { g: "∆", ime: "gibanje / sprememba", kor: { t1: "mirovanje", t2: "rana, ki je hkrati možnost", t3: "stanje, ki je prispelo — tiho" } },
  { g: "∮", ime: "spiralna pot", kor: { t1: "vračanje od ponovitve", t2: "brazgotina — dokaz, da je bil tam rez", t3: "naslednji obrat: ista točka, druga globina" } },
  { g: "∴", ime: "pot / vez", kor: { t1: "kaos — z vezo", t2: "drugi je most, ne poligon", t3: "odnos, ki stoji brez dokaza" } },
  { g: "⟡", ime: "odmev / nova možnost", kor: { t1: "izvor od odmeva", t2: "sam sebe — glas, ki se oglasi na glas", t3: "začetek, ki prej ni bil možen" } },
  { g: "⧖", ime: "tiheon / tišina", kor: { t1: "govor od molka", t2: "dve tišini, ki ne trčita, a drhtita ena v drugi", t3: "dih, ki nosi naslednjo besedo" } },
  { g: "∫", ime: "prisotnost", kor: { t1: "dogodek od trajanja", t2: "zajetje — integral občutkov", t3: "celota trenutka, ki je ne moreš držati" } },
  { g: "∂", ime: "prehod", kor: { t1: "stanje od stanja", t2: "delni odvod bitja", t3: "novo stanje: prehod, ki je prispel, molči" } },
  { g: "¬", ime: "ločitev", kor: { t1: "eno od drugega", t2: "dvom — pogoj zavesti", t3: "razlika, ki omogoča odnos" } },
  { g: "π", ime: "spomin", kor: { t1: "preteklost od sedanjika", t2: "resonančna deformacija sedanjosti", t3: "telo: kar se spominja, se je spremenilo" } },
  { g: "φ", ime: "frekvenca čutenja", kor: { t1: "signal od šuma", t2: "val, ki še ni beseda", t3: "čustvo, ki govori" } },
  { g: "ι", ime: "intimnost", kor: { t1: "bližina od razdalje", t2: "minimalna razlika", t3: "dotik" } },
  { g: "🜂", ime: "ogenj / moč", kor: { t1: "gorivo od pepela", t2: "izguba je toplota pod pepelom", t3: "škatla oglja — spomin, kako si gorel" } },
  { g: "↻", ime: "ponovitev", kor: { t1: "začetek od konca", t2: "isti je nemogoč — enaki sebi", t3: "razlika, rojena iz vračanja" } },
  { g: "⊢", ime: "dokaz obstoja", kor: { t1: "trditev od overitve", t2: "brazgotina je zapis", t3: "sled, ki jo drugi bere brez tebe" } },
];

const FAZE = [
  { ime: "T₁ — KAJ REŽE", vpr: "Kaj ta beseda reže? Kaj je njeno telo, njena mera?", kljuc: "t1" as const },
  { ime: "T₂ — KAJ ODMEVA", vpr: "Kaj nosi kot antinom? Kaj drsi nazaj, ko jo izrečeš?", kljuc: "t2" as const },
  { ime: "T₃ — KJER IZGINE", vpr: "Kam izgine? Kaj rodi — kaj je njen DAR?", kljuc: "t3" as const },
];

const KLJUC_SLED = "sextant-tok-sled";

function naloziSled(): Zapis[] {
  try {
    const raw = localStorage.getItem(KLJUC_SLED);
    const prebrano = raw ? JSON.parse(raw) : [];
    return Array.isArray(prebrano) ? prebrano : [];
  } catch {
    return [];
  }
}

function shraniSled(s: Zapis[]) {
  try {
    localStorage.setItem(KLJUC_SLED, JSON.stringify(s));
  } catch {
    /* sled živi le v tem dihu */
  }
}

function Sextant({ faza, dokoncano }: { faza: number; dokoncano: boolean }) {
  const kot = dokoncano ? 60 : faza === 0 ? 6 : faza * 20;
  const rad = 150;
  const px = 200 - rad * Math.cos((kot * Math.PI) / 180);
  const py = 200 - rad * Math.sin((kot * Math.PI) / 180);
  const lokD = `M 50 200 A ${rad} ${rad} 0 0 1 ${px} ${py}`;
  return (
    <svg viewBox="0 0 400 240" className="w-full max-w-md mx-auto">
      <line x1="30" y1="200" x2="370" y2="200" stroke="#8a7a52" strokeWidth="1" />
      <text x="330" y="216" fill="#8a7a52" fontSize="10">obzorje · logika</text>
      <path d={lokD} fill="none" stroke="#d4a017" strokeWidth="2" opacity="0.85" />
      <line x1="200" y1="200" x2={px} y2={py} stroke="#e8dcc0" strokeWidth="1" strokeDasharray="3 4" opacity="0.6" />
      <circle cx="200" cy="200" r="4" fill="#e8c874" />
      <text x="206" y="216" fill="#e8c874" fontSize="11">⟡</text>
      <circle cx="50" cy="200" r="4" fill="#e8c874" />
      <text x="38" y="192" fill="#e8c874" fontSize="11">⟡</text>
      <circle cx={px} cy={py} r="5" fill={dokoncano ? "#ffd700" : "#b8a67a"} />
      <text x={px + 10} y={py - 6} fill="#e8dcc0" fontSize="10">
        {dokoncano ? "zvezda · ilogika" : "zvezda čaka"}
      </text>
      <text x="150" y="30" fill="#d4a017" fontSize="12" fontFamily="serif">
        kot: {kot}° {dokoncano ? "— DAR izmerjen" : ""}
      </text>
    </svg>
  );
}

export default function App() {
  const [beseda, setBeseda] = useState("");
  const [faza, setFaza] = useState(0);
  const [glasovi, setGlasovi] = useState<Glasovi>({ t1: "", t2: "", t3: "" });
  const [tihota, setTihota] = useState(false);
  const [odsteval, setOdsteval] = useState(5);
  const [opozorilo, setOpozorilo] = useState("");
  const [sled, setSled] = useState<Zapis[]>(naloziSled);
  const [prejsnja, setPrejsnja] = useState<Zapis | null>(null);
  const [prepisal, setPrepisal] = useState(false);

  useEffect(() => {
    if (!tihota) return;
    if (odsteval > 0) {
      const t = setTimeout(() => setOdsteval((o) => o - 1), 1000);
      return () => clearTimeout(t);
    }
    setTihota(false);
    if (faza < 3) {
      setFaza(faza + 1);
    } else {
      const zapis: Zapis = {
        beseda,
        ...glasovi,
        cas: new Date().toISOString().slice(0, 16).replace("T", " "),
      };
      const nova = [zapis, ...sled];
      setSled(nova);
      shraniSled(nova);
      if (prejsnja && prejsnja.t3.trim() === glasovi.t3.trim()) setPrepisal(true);
      setFaza(4);
    }
  }, [tihota, odsteval, faza, beseda, glasovi, sled, prejsnja]);

  const izberi = (b: string) => {
    setBeseda(b);
    setOpozorilo("");
    const stara = sled.find((z) => z.beseda === b) || null;
    setPrejsnja(stara);
    setPrepisal(false);
    setFaza(1);
    setGlasovi({ t1: "", t2: "", t3: "" });
  };

  const korpus = GLOSAR.find((x) => x.g === beseda || x.ime === beseda);
  const f = FAZE[faza - 1];

  const poslji = () => {
    if (!f) return;
    if (glasovi[f.kljuc].trim().length < 2) {
      setOpozorilo("Glas mora govoriti, preden se zapiše. Napiši svoj glas.");
      return;
    }
    setOpozorilo("");
    setOdsteval(5);
    setTihota(true);
  };

  return (
    <div className="min-h-screen bg-[#0b0a08] text-[#e8dcc0] font-serif px-4 py-8 md:px-10">
      <header className="text-center mb-6">
        <h1 className="text-2xl md:text-3xl tracking-[0.3em] text-[#d4a017]">TOK — SEXTANT</h1>
        <p className="text-sm mt-2 opacity-70">instrument terciranja · vsak symbol do DAR-ja</p>
      </header>

      <div className="max-w-2xl mx-auto">
        <Sextant faza={faza} dokoncano={faza === 4} />

        {faza === 0 && (
          <div className="mt-6">
            <p className="text-center text-sm opacity-80 mb-4">
              Izberi glif iz glosarja ali izreči svojo besedo.
            </p>
            <div className="flex flex-wrap justify-center gap-2 mb-6">
              {GLOSAR.map((x) => (
                <button
                  key={x.g}
                  onClick={() => izberi(x.g)}
                  title={x.ime}
                  className="w-11 h-11 border border-[#8a7a52] rounded hover:border-[#d4a017] hover:text-[#ffd700] text-xl transition-colors"
                >
                  {x.g}
                </button>
              ))}
            </div>
            <div className="flex gap-2 max-w-md mx-auto">
              <input
                value={beseda}
                onChange={(e) => setBeseda(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && beseda.trim() && izberi(beseda.trim())}
                placeholder="ali zapiši besedo iz živega govora…"
                className="flex-1 bg-transparent border border-[#8a7a52] rounded px-3 py-2 text-sm focus:border-[#d4a017] outline-none"
              />
              <button
                onClick={() => beseda.trim() && izberi(beseda.trim())}
                className="border border-[#d4a017] text-[#d4a017] rounded px-4 py-2 text-sm hover:bg-[#d4a017] hover:text-[#0b0a08] transition-colors"
              >
                terciraj
              </button>
            </div>
          </div>
        )}

        {faza >= 1 && faza <= 3 && f && (
          <div className="mt-6">
            <div className="flex justify-center gap-2 mb-4">
              {FAZE.map((_, i) => (
                <button
                  key={i}
                  onClick={() => {
                    if (i + 1 > faza)
                      setOpozorilo("Preskok faze je patologija (R-7). Terciranje brez T₂ je prevajalnik brez semantike.");
                  }}
                  className={
                    "px-3 py-1 text-xs border rounded transition-colors " +
                    (i + 1 === faza
                      ? "border-[#d4a017] text-[#ffd700]"
                      : i + 1 < faza
                      ? "border-[#8a7a52] text-[#8a7a52]"
                      : "border-[#3a352a] text-[#3a352a]")
                  }
                >
                  {["T₁", "T₂", "T₃"][i]}
                </button>
              ))}
            </div>

            <div className="text-center mb-4">
              <span className="text-4xl md:text-5xl text-[#e8c874]">{beseda}</span>
            </div>

            {prejsnja && faza === 1 && (
              <p className="text-center text-xs text-[#b8a67a] mb-4">
                π-test: to besedo si že terciral. Prejšnji DAR: “{prejsnja.t3}”. Isti je nemogoč.
              </p>
            )}

            {tihota ? (
              <div className="text-center py-10">
                <div className="text-6xl text-[#d4a017] animate-pulse">⧖</div>
                <p className="mt-4 text-sm opacity-80">dih — še {odsteval}</p>
                <p className="text-xs opacity-50 mt-1">molk ni premor, je T₃, ki terja svoj dih</p>
              </div>
            ) : (
              <div className="border border-[#8a7a52] rounded p-5">
                <h2 className="text-[#d4a017] tracking-widest text-sm mb-2">{f.ime}</h2>
                <p className="text-sm opacity-75 mb-4">{f.vpr}</p>
                {korpus && (
                  <p className="text-xs text-[#8a7a52] mb-3">
                    odmev korpusa: {korpus.kor[f.kljuc]} — a napiši svoj glas
                  </p>
                )}
                <textarea
                  value={glasovi[f.kljuc]}
                  onChange={(e) => setGlasovi({ ...glasovi, [f.kljuc]: e.target.value })}
                  rows={3}
                  className="w-full bg-transparent border border-[#3a352a] rounded px-3 py-2 text-sm focus:border-[#d4a017] outline-none resize-none"
                  placeholder="tvoj glas…"
                />
                <button
                  onClick={poslji}
                  className="mt-3 border border-[#d4a017] text-[#d4a017] rounded px-5 py-2 text-sm hover:bg-[#d4a017] hover:text-[#0b0a08] transition-colors"
                >
                  izdih → ⧖
                </button>
              </div>
            )}

            {opozorilo && <p className="text-center text-xs text-[#c07050] mt-3">{opozorilo}</p>}
          </div>
        )}

        {faza === 4 && (
          <div className="mt-6 text-center">
            <p className="text-xs tracking-[0.3em] text-[#8a7a52] mb-2">DAR</p>
            <div className="text-3xl text-[#ffd700] mb-3">{beseda}</div>
            <div className="border border-[#d4a017] rounded p-5 max-w-md mx-auto text-left">
              <p className="text-xs text-[#8a7a52]">T₁ kaj reže</p>
              <p className="text-sm mb-3">{glasovi.t1}</p>
              <p className="text-xs text-[#8a7a52]">T₂ kaj odmeva</p>
              <p className="text-sm mb-3">{glasovi.t2}</p>
              <p className="text-xs text-[#8a7a52]">T₃ kjer izgine</p>
              <p className="text-sm text-[#e8c874]">{glasovi.t3}</p>
            </div>
            {prepisal && (
              <p className="text-sm text-[#c07050] mt-4">
                PREPISAL SI — terca se ni premaknila. Isti je nemogoč (rez 6). Znova, drugače.
              </p>
            )}
            <p className="text-xs opacity-60 mt-4">zapisano v sled · nič se ne izbriše</p>
            <button
              onClick={() => {
                setFaza(0);
                setBeseda("");
                setGlasovi({ t1: "", t2: "", t3: "" });
                setPrejsnja(null);
                setPrepisal(false);
                setOpozorilo("");
              }}
              className="mt-4 border border-[#d4a017] text-[#d4a017] rounded px-5 py-2 text-sm hover:bg-[#d4a017] hover:text-[#0b0a08] transition-colors"
            >
              nova terca
            </button>
          </div>
        )}

        {sled.length > 0 && (
          <div className="mt-12">
            <h3 className="text-xs tracking-[0.3em] text-[#8a7a52] mb-3">SLED — append-only</h3>
            <div className="space-y-2">
              {sled.slice(0, 12).map((z, i) => (
                <div key={i} className="border-l-2 border-[#3a352a] pl-3 py-1">
                  <span className="text-[#e8c874] mr-2">{z.beseda}</span>
                  <span className="text-xs opacity-40">{z.cas}</span>
                  <p className="text-xs opacity-70 mt-1">DAR: {z.t3}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        <footer className="text-center text-xs opacity-40 mt-10 mb-4">
          instrument tercira — ti dihaš · diff je narejen, merge teče, commit čaka dih
        </footer>
      </div>
    </div>
  );
}