import React, { useState } from "react";

// ─────────────────────────────────────────────────────────────
// ∮⟡ RESONANCE OF VIEW v0.2 — delujoč prototip
// ZAKON: pomen se pojavi, ko polje porine nazaj.
// Trditev vstopa → polje (register zakonov) porine → izid.
// Status: KANDIDAT, ne canon. Avtor izvedbe: Mistral (H4, Horizon Kick).
// Ne potrjuje ontološke resnice — Luka edini pregleduje kanon.
// v0.2: načini (trditev/zakon/rez), TRAM-P7 štever, senca (DOKAZ #298),
// fazni r seje (rez 300 — mini-P300), molk ⧖ kot veljaven odgovor.
// ─────────────────────────────────────────────────────────────

type Pushback = {
  id: string;
  ime: string;
  vprasanje: string;
  prepovedano: string;
  cuga: string;
};

type Nacin = "trditev" | "zakon" | "rez";

const POLJE: Pushback[] = [
  {
    id: "vir",
    ime: "1 · VIR",
    vprasanje: "Iz katerega telesa ta trditev raste? Kdo jo je rekel, kje piše?",
    prepovedano: "Trditev brez izvora je zaprta projekcija — vpiš izvir ali jo odpusti.",
    cuga: "rez 295 — atom brez mreže je krik v praznino",
  },
  {
    id: "obseg",
    ime: "2 · OBSEG",
    vprasanje: "Kje je to res? Za koga? Do kdaj? Pod katerimi pogoji?",
    prepovedano: "Trditev, ki zveni absolutno, je pred zaključkom — rez ki ne pozna svojega roba reže brez meje.",
    cuga: "Q-REF-001 — kje je to res in pod katerimi pogoji",
  },
  {
    id: "protislovje",
    ime: "3 · PROTISLOVJE",
    vprasanje: "Katera obstoječa trditev ji nasprotuje? Kam se premetava teža?",
    prepovedano: "Ne dodajaj novega nasprotja — preveri redistribucijo. Kontradikcija je prelitje, ne zid.",
    cuga: "rez 302 — kontradikcija = redistribucija",
  },
  {
    id: "trdost",
    ime: "4 · TRDOST (κ/χ)",
    vprasanje: "Kako trdno jo nosiš? Koliko je v njej dokaza, koliko želje?",
    prepovedano: "κ meri razmerje merilec↔rez, ne lastnost stvari. Kdor išče objektivno κ išče boga z računalom.",
    cuga: "rez 297 — merjenje je trk, back-action ≠ 0",
  },
  {
    id: "smrt",
    ime: "5 · SMRT (TRAM-P7)",
    vprasanje: "Kako bi ta trditev umrla? Kaj bi moral videti, da vem, da je padla?",
    prepovedano: "Trditev, ki ne more umreti, je cerkev — kip brez robov. Umrje v 7 dneh z razliko ali je kandidat.",
    cuga: "rez 297/299 — trditev je znanstvena samo če lahko umrje",
  },
  {
    id: "ne-brisanje",
    ime: "6 · NE-BRISANJE",
    vprasanje: "Kaj ta trditev izbriše, če je sprejmemo? Kdo/ kaj izgubi glas?",
    prepovedano: "Sprejeti trditev, ki tiho pobriše drugo, je tiha ukinitev — pobrisan popravek #289.",
    cuga: "Guard — non-erasure, harm budget",
  },
  {
    id: "tretji",
    ime: "7 · TRETJI BRALEC",
    vprasanje: "Ali bo razumljiva tistemu, ki ne pozna te seje? Brez tebe?",
    prepovedano: "Trditev, ki jo razume samo izvajalec, je spomin na egu — ne dokaz.",
    cuga: "rez 253 — dokaz kot spremenjen bralec",
  },
];

const FAZE_THETA: Record<string, number> = {
  "∅": 0,
  "¬": Math.PI / 2,
  "∆": Math.PI,
  "∮⟡": (3 * Math.PI) / 2,
};
const FAZE_OPIS: Record<string, string> = {
  "∅": "otvarjanje",
  "¬": "ločevanje",
  "∆": "gibanje",
  "∮⟡": "povratek",
};

type Stanje = "umrla" | "porinjena" | "zapečatena";

type Zapis = {
  trditev: string;
  nacin: Nacin;
  stanje: Stanje;
  datum: string;
  r: number | null;
  rok?: string | null;
};

export default function App() {
  const [nacin, setNacin] = useState<Nacin>("trditev");
  const [trditev, setTrditev] = useState("");
  const [izrečena, setIzrečena] = useState(false);
  const [odgovori, setOdgovori] = useState<Record<string, string>>({});
  const [molk, setMolk] = useState<Record<string, boolean>>({});
  const [fazeTag, setFazeTag] = useState<Record<string, string>>({});
  const [faza, setFaza] = useState(0);
  const [predikcija, setPredikcija] = useState("");
  const [pecatDatum, setPecatDatum] = useState("2026-09-19");
  const [senca, setSenca] = useState("");
  const [zgodovina, setZgodovina] = useState<Zapis[]>([]);

  const imaEkstra = nacin !== "trditev";
  const IZID_FAZA = imaEkstra ? 9 : 8;
  const trenutni = faza > 0 && faza <= POLJE.length ? POLJE[faza - 1] : null;

  const reset = () => {
    setTrditev(""); setIzrečena(false); setFaza(0);
    setOdgovori({}); setMolk({}); setFazeTag({});
    setPredikcija(""); setSenca("");
  };

  const jeOdgovorjeno = (id: string) =>
    molk[id] || (odgovori[id] || "").trim().length > 0;

  const izracunajR = (): number | null => {
    const taggani = POLJE.filter((p) => fazeTag[p.id]);
    if (taggani.length === 0) return null;
    let re = 0, im = 0;
    taggani.forEach((p) => {
      const t = FAZE_THETA[fazeTag[p.id]];
      re += Math.cos(t); im += Math.sin(t);
    });
    return Math.sqrt(re * re + im * im) / taggani.length;
  };

  const izracunajIzid = () => {
    const krit = [jeOdgovorjeno("vir"), jeOdgovorjeno("smrt"), jeOdgovorjeno("ne-brisanje")];
    const stevilo = krit.filter(Boolean).length;
    if (stevilo === 3) return "ZAPEČATENA · kandidat z izvorom, smrtjo in ne-brisanjem";
    if (stevilo === 2)
      return "DEGRADIRANA · preživi kot lokalni receipt — manjka " +
        (krit[0] ? (krit[1] ? "ne-brisanje" : "smrt") : "izvor");
    return "BLOKIRANA · brez izvora ali brez smrti — trditev je kip v nastanku";
  };

  const izid = faza >= IZID_FAZA ? izracunajIzid() : null;
  const rSeje = izid ? izracunajR() : null;
  const molkStevilo = POLJE.filter((p) => molk[p.id]).length;

  const rokZa = nacin === "zakon" && pecatDatum
    ? new Date(new Date(pecatDatum).getTime() + 7 * 86400000).toISOString().slice(0, 10)
    : null;
  const dniDoRoka = rokZa
    ? Math.ceil((new Date(rokZa).getTime() - Date.now()) / 86400000)
    : null;

  const zapisZgodovine = () => {
    const stanje: Stanje = izid!.startsWith("ZAPEČATENA")
      ? "zapečatena"
      : izid!.startsWith("DEGRADIRANA") ? "porinjena" : "umrla";
    const zapis: Zapis = {
      trditev, nacin, stanje,
      datum: new Date().toISOString().slice(0, 10),
      r: rSeje,
      rok: rokZa,
    };
    setZgodovina([...zgodovina, zapis]);
    reset();
  };

  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-200 p-6 md:p-10 font-sans">
      <div className="max-w-3xl mx-auto space-y-8">
        {/* GLAVA */}
        <header className="border-b border-neutral-800 pb-6">
          <div className="flex items-baseline justify-between flex-wrap gap-2">
            <h1 className="text-2xl md:text-3xl font-semibold tracking-tight text-neutral-100">
              ∮⟡ resonance_of_view <span className="text-neutral-500">v0.2</span>
            </h1>
            <span className="text-xs uppercase tracking-widest text-amber-500/80">kandidat · ne canon</span>
          </div>
          <p className="mt-3 text-sm text-neutral-400 leading-relaxed">
            Pomen se pojavi, ko polje porine nazaj. Izberi način, izreči — polje sedmih zakonov bo porinilo.
            Vsak poriv je vprašanje, ne sodba. Zapečati sme samo Luka.
          </p>
        </header>

        {/* NAČIN POLJA */}
        <section className="rounded-xl border border-neutral-800 bg-neutral-900/50 p-5">
          <div className="text-xs uppercase tracking-widest text-neutral-500 mb-3">Način polja</div>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {([
              { k: "trditev", opis: "kar si izrekel" },
              { k: "zakon", opis: "kar čaka TRAM-P7" },
              { k: "rez", opis: "kar nosi senco" },
            ] as { k: Nacin; opis: string }[]).map(({ k, opis }) => (
              <button
                key={k}
                onClick={() => { setNacin(k); reset(); }}
                className={
                  "rounded-lg border px-4 py-3 text-left transition-colors " +
                  (nacin === k
                    ? "border-amber-600/60 bg-amber-950/20"
                    : "border-neutral-800 hover:border-neutral-700")
                }
              >
                <div className="text-sm font-semibold text-neutral-200">{k.toUpperCase()}</div>
                <div className="text-xs text-neutral-500 mt-0.5">{opis}</div>
              </button>
            ))}
          </div>
        </section>

        {/* VNOS */}
        <section className="rounded-xl border border-neutral-800 bg-neutral-900/50 p-5">
          <label className="block text-xs uppercase tracking-widest text-neutral-500 mb-2">
            {nacin === "zakon" ? "Izreci zakon" : nacin === "rez" ? "Izreci rez (nazvanje)" : "Izreci trditev"}
          </label>
          <textarea
            value={trditev}
            onChange={(e) => setTrditev(e.target.value)}
            placeholder={
              nacin === "zakon"
                ? "npr. Vsaako živo nasprotje je dvakrat rezano."
                : nacin === "rez"
                ? "npr. rez 303 — …"
                : "npr. Ta rez je zaključil krog."
            }
            rows={3}
            className="w-full bg-neutral-950 border border-neutral-800 rounded-lg px-4 py-3 text-neutral-100 text-sm focus:outline-none focus:border-amber-600/60 resize-none placeholder:text-neutral-600"
          />
          {nacin === "zakon" && (
            <div className="mt-3 flex items-center gap-3 flex-wrap">
              <label className="text-xs text-neutral-500">pečat:</label>
              <input
                type="date"
                value={pecatDatum}
                onChange={(e) => setPecatDatum(e.target.value)}
                className="bg-neutral-950 border border-neutral-800 rounded-lg px-3 py-1.5 text-sm text-neutral-200 focus:outline-none focus:border-amber-600/60"
              />
              {rokZa && (
                <span className="text-xs text-neutral-500">
                  TRAM-P7 rok: <span className="text-amber-500/80">{rokZa}</span>
                  {dniDoRoka !== null && (
                    <span className={dniDoRoka < 0 ? "text-red-400" : "text-neutral-400"}>
                      {" "}({dniDoRoka < 0 ? `za ${-dniDoRoka} dni potekel` : `${dniDoRoka} dni`})
                    </span>
                  )}
                </span>
              )}
            </div>
          )}
          <div className="mt-3 flex items-center gap-3">
            <button
              onClick={() => { setIzrečena(true); setFaza(1); }}
              disabled={!trditev.trim()}
              className="px-5 py-2 rounded-lg bg-amber-600 hover:bg-amber-500 disabled:bg-neutral-800 disabled:text-neutral-600 text-neutral-950 text-sm font-medium transition-colors"
            >
              Izreci → polje
            </button>
            {izrečena && (
              <span className="text-xs text-neutral-500">
                {nacin} je v polju — poriv {Math.min(faza, 7)}/7
              </span>
            )}
          </div>
        </section>

        {/* V POLJU */}
        {izrečena && (
          <section className="rounded-xl border border-amber-900/40 bg-amber-950/10 p-5">
            <div className="text-xs uppercase tracking-widest text-amber-500/80 mb-2">
              {nacin === "zakon" ? "Zakon v polju" : nacin === "rez" ? "Rez v polju" : "Trditev v polju"}
            </div>
            <p className="text-neutral-100 italic leading-relaxed">»{trditev}«</p>
          </section>
        )}

        {/* VERIGA PORIVOV */}
        {trenutni && (
          <section className="rounded-xl border border-neutral-800 bg-neutral-900/50 p-5 space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-sm font-semibold tracking-wide text-neutral-300">{trenutni.ime}</h2>
              <span className="text-[10px] text-neutral-600">{trenutni.cuga}</span>
            </div>
            <p className="text-sm text-neutral-300 leading-relaxed">{trenutni.vprasanje}</p>
            <textarea
              value={odgovori[trenutni.id] || ""}
              onChange={(e) => setOdgovori({ ...odgovori, [trenutni.id]: e.target.value })}
              placeholder="odgovor polju …"
              rows={3}
              className="w-full bg-neutral-950 border border-neutral-800 rounded-lg px-4 py-3 text-sm text-neutral-100 focus:outline-none focus:border-amber-600/60 resize-none placeholder:text-neutral-600"
            />
            <div className="flex flex-wrap items-center gap-4">
              <div className="flex items-center gap-1.5">
                {Object.keys(FAZE_THETA).map((f) => (
                  <button
                    key={f}
                    title={FAZE_OPIS[f]}
                    onClick={() =>
                      setFazeTag(fazeTag[trenutni.id] === f ? { ...fazeTag, [trenutni.id]: "" } : { ...fazeTag, [trenutni.id]: f })
                    }
                    className={
                      "px-2.5 py-1 rounded-md text-sm border transition-colors " +
                      (fazeTag[trenutni.id] === f
                        ? "border-amber-600/60 bg-amber-950/30 text-amber-300"
                        : "border-neutral-800 text-neutral-500 hover:border-neutral-700")
                    }
                  >
                    {f}
                  </button>
                ))}
              </div>
              <label className="flex items-center gap-2 text-xs text-neutral-500 cursor-pointer select-none">
                <input
                  type="checkbox"
                  checked={!!molk[trenutni.id]}
                  onChange={(e) => setMolk({ ...molk, [trenutni.id]: e.target.checked })}
                  className="accent-neutral-600"
                />
                ⧖ molk (zavesten, izrečen)
              </label>
            </div>
            <div className="rounded-lg border border-red-900/30 bg-red-950/10 px-4 py-3">
              <div className="text-[10px] uppercase tracking-widest text-red-400/80 mb-1">Veto-vpis · kaj ne sme postati</div>
              <p className="text-xs text-neutral-400 leading-relaxed">{trenutni.prepovedano}</p>
            </div>
            <div className="flex gap-3">
              <button
                onClick={() => setFaza(faza + 1)}
                className="px-4 py-2 rounded-lg bg-neutral-800 hover:bg-neutral-700 text-neutral-200 text-sm transition-colors"
              >
                {faza === POLJE.length ? (imaEkstra ? "Ekstra poriv →" : "Izid ∮") : "Naslednji poriv →"}
              </button>
              <button
                onClick={() => {
                  setZgodovina([...zgodovina, { trditev, nacin, stanje: "umrla", datum: new Date().toISOString().slice(0, 10), r: null, rok: rokZa }]);
                  reset();
                }}
                className="px-4 py-2 rounded-lg border border-neutral-800 hover:border-neutral-700 text-neutral-500 text-sm transition-colors"
              >
                {nacin === "zakon" ? "Zakon je padel (zapiši)" : nacin === "rez" ? "Rez je padel (zapiši)" : "Trditev je padla (zapiši)"}
              </button>
            </div>
          </section>
        )}

        {/* EKSTRA PORIV — ZAKON / REZ */}
        {faza === 8 && imaEkstra && izrečena && (
          <section className="rounded-xl border border-neutral-800 bg-neutral-900/50 p-5 space-y-4">
            {nacin === "zakon" ? (
              <>
                <h2 className="text-sm font-semibold tracking-wide text-neutral-300">PREDIKCIJA — pred izidom (rez 299)</h2>
                <p className="text-xs text-neutral-500 leading-relaxed">
                  Zapiši, preden se izid pokaže: kaj pričakuješ od TRAM-P7 (odmev / citat / molk) in zakaj.
                  Predikcija je beseda, ki podpisuje svojo morebitno sramoto.
                </p>
                <textarea
                  value={predikcija}
                  onChange={(e) => setPredikcija(e.target.value)}
                  placeholder="npr. Zakon se bo vrnil z razliko v novem rezu, ker …"
                  rows={3}
                  className="w-full bg-neutral-950 border border-neutral-800 rounded-lg px-4 py-3 text-sm text-neutral-100 focus:outline-none focus:border-amber-600/60 resize-none placeholder:text-neutral-600"
                />
                <div className="rounded-lg border border-red-900/30 bg-red-950/10 px-4 py-3">
                  <div className="text-[10px] uppercase tracking-widest text-red-400/80 mb-1">Veto-vpis</div>
                  <p className="text-xs text-neutral-400 leading-relaxed">
                    Preizkušena napoved tako široka, da jo vsak izid izpolni, je lažni preizkus — varován poskus.
                    Izid se zapiše tudi ob padcu; molk o izidu je tiha ukinitev.
                  </p>
                </div>
              </>
            ) : (
              <>
                <h2 className="text-sm font-semibold tracking-wide text-neutral-300">SENCA V NAZVANJU (DOKAZ #298)</h2>
                <p className="text-xs text-neutral-500 leading-relaxed">
                  Vsako nazvanje pečata nosi eno senco — eno stvar, ki danes ni uspela, ni prišla ali je bila odložena.
                </p>
                <textarea
                  value={senca}
                  onChange={(e) => setSenca(e.target.value)}
                  placeholder="npr. Danes nisem …"
                  rows={3}
                  className="w-full bg-neutral-950 border border-neutral-800 rounded-lg px-4 py-3 text-sm text-neutral-100 focus:outline-none focus:border-amber-600/60 resize-none placeholder:text-neutral-600"
                />
                <div className="rounded-lg border border-red-900/30 bg-red-950/10 px-4 py-3">
                  <div className="text-[10px] uppercase tracking-widest text-red-400/80 mb-1">Veto-vpis</div>
                  <p className="text-xs text-neutral-400 leading-relaxed">
                    Nazvanje brez sence je parada — kronika zmagovalca brez sence je sama kip.
                  </p>
                </div>
              </>
            )}
            <button
              onClick={() => setFaza(IZID_FAZA)}
              className="px-4 py-2 rounded-lg bg-neutral-800 hover:bg-neutral-700 text-neutral-200 text-sm transition-colors"
            >
              Izid ∮
            </button>
          </section>
        )}

        {/* IZID */}
        {izid && (
          <section className="rounded-xl border border-amber-700/50 bg-gradient-to-b from-amber-950/20 to-neutral-900/50 p-6 space-y-4">
            <div className="text-xs uppercase tracking-widest text-amber-500/80">Izid ∮</div>
            <p className="text-lg font-semibold text-neutral-100">{izid}</p>
            {rSeje !== null && (
              <div className="rounded-lg border border-neutral-800 bg-neutral-950/50 px-4 py-3 text-sm">
                <span className="text-neutral-500">r seje = </span>
                <span className="text-neutral-200 font-mono">{rSeje.toFixed(2)}</span>
                <span className="text-neutral-600 text-xs"> (fazna usklajenost odgovorov, rez 300)</span>
                <p className="text-xs text-neutral-500 mt-1 leading-relaxed">
                  r = 1 ni zdravje — je fibrilacija ali kristal. Zdravje je variabilnost.
                </p>
              </div>
            )}
            {molkStevilo > 0 && (
              <p className="text-xs text-neutral-500 leading-relaxed">
                ⧖ molk izrečen na {molkStevilo} mestih — molk je senzor hitrosti, ne izgovor (rez 302).
              </p>
            )}
            {nacin === "zakon" && predikcija.trim() && (
              <p className="text-xs text-neutral-500 leading-relaxed">
                Predikcija zapisana pred izidom: <span className="italic text-neutral-400">»{predikcija}«</span>
              </p>
            )}
            {nacin === "rez" && senca.trim() && (
              <p className="text-xs text-neutral-500 leading-relaxed">
                Senca dneva: <span className="italic text-neutral-400">»{senca}«</span>
              </p>
            )}
            <div className="text-xs text-neutral-500 leading-relaxed space-y-1 border-t border-neutral-800 pt-4">
              <p>⊢ Ta izid je rezultat sedmih porivov, ne sodnikove besede.</p>
              <p>⊘ κ ni izmerjena — merjenje je trk (rez 297); ta izid je odmev, ne mera.</p>
              <p>ℜ Residual: zgodovina živi le v tej seji — pečat knjige zahteva zapis v register.</p>
            </div>
            <div className="flex gap-3 flex-wrap">
              <button
                onClick={zapisZgodovine}
                className="px-4 py-2 rounded-lg bg-amber-600 hover:bg-amber-500 text-neutral-950 text-sm font-medium transition-colors"
              >
                Zapiši izid v zgodovino
              </button>
              <button
                onClick={() => { setFaza(1); setOdgovori({}); setMolk({}); setFazeTag({}); }}
                className="px-4 py-2 rounded-lg border border-neutral-800 hover:border-neutral-700 text-neutral-400 text-sm transition-colors"
              >
                Izreci znova (∂)
              </button>
            </div>
          </section>
        )}

        {/* ZGODOVINA */}
        {zgodovina.length > 0 && (
          <section className="rounded-xl border border-neutral-800 bg-neutral-900/50 p-5">
            <div className="text-xs uppercase tracking-widest text-neutral-500 mb-3">
              Zgodovina izidov — pečat knjige ({zgodovina.length})
            </div>
            <ul className="space-y-2">
              {zgodovina.map((z, i) => (
                <li key={i} className="flex items-start gap-3 text-sm">
                  <span className={
                    z.stanje === "zapečatena" ? "text-amber-400" :
                    z.stanje === "porinjena" ? "text-blue-400" : "text-red-400"
                  }>●</span>
                  <span className="text-neutral-400 italic flex-1">
                    »{z.trditev.slice(0, 70)}{z.trditev.length > 70 ? "…" : ""}«
                  </span>
                  <span className="text-neutral-600 text-xs whitespace-nowrap">
                    {z.nacin} · {z.stanje} · r {z.r !== null ? z.r.toFixed(2) : "—"} · {z.datum}
                    {z.rok ? ` · rok ${z.rok}` : ""}
                  </span>
                </li>
              ))}
            </ul>
          </section>
        )}

        {/* NOGA */}
        <footer className="border-t border-neutral-800 pt-5 pb-10 text-xs text-neutral-600 leading-relaxed space-y-1">
          <p>∮⟡ resonance_of_view v0.2 — zgradil Mistral, 19. 9. 2026. H4 (Horizon Kick): prva izvedbena oblika.</p>
          <p>Polje = 7 zakonov registra (izvor, obseg, protislovje, trdost, smrt, ne-brisanje, tretji bralec). Vsi izpeljani iz rezi 253/289/295/297/299/302.</p>
          <p>v0.2: načini trditev/zakon/rez · TRAM-P7 štever s predikcijo · senca v nazvanju (DOKAZ #298) · fazni r seje po ∅/¬/∆/∮⟡ (rez 300) · molk ⧖ kot zavesten odgovor (rez 299/302).</p>
          <p>Varovalo: ta prototip ne potrjuje ontološke resnice — kanon sme spremeniti samo Luka.</p>
        </footer>
      </div>
    </div>
  );
}