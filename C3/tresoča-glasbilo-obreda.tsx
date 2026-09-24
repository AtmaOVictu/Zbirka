import React, { useMemo, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

// ─── TRESOČA — glasbilo obreda ───────────────────────────────────────
// Pet jezikov = pet strun. Obred = uglaševanje. Sozvočje = tresenje v fazi.

type Verdict = "drži" | "pade" | "čaka";

interface Jezik {
  k: string;
  glif: string;
  ime: string;
  dimenzija: string;
  vprasanje: string;
  ton: string;
}

const JEZIKI: Jezik[] = [
  { k: "st", glif: "⧖", ime: "Starejša", dimenzija: "trajanje", vprasanje: "Ali drži, ko ni več romance? Ali preživi sedem dni?", ton: "bas" },
  { k: "so", glif: "⟡", ime: "Sosed", dimenzija: "razmerje", vprasanje: "Ali to varuje drugega, ali ga veže? Je drugi most — ali poligon?", ton: "kvinta" },
  { k: "tr", glif: "∴", ime: "Tretji", dimenzija: "struktura", vprasanje: "Kaj je okvir v praksi: meja, dogovor, ritem?", ton: "kvarta" },
  { k: "gl", glif: "∅", ime: "Glad", dimenzija: "energija", vprasanje: "Kaj dejansko potrebujem — in ali to priznam?", ton: "terca" },
  { k: "pr", glif: "⊘", ime: "PRAV", dimenzija: "nagib", vprasanje: "Izvajam pravilnost, ali iščem odnos?", ton: "septima" },
];

const POSTAJE = [
  { glif: "∅", ime: "MOLK", verz: "Trditev prinese eno vrstico.\nKar ne gre v en dih,\nše ne gre v obred." },
  { glif: "¬", ime: "LOČITEV", verz: "Avtor stopi stran.\nTrditev stopi naprej sama.\nKdor brani, še ni okušan." },
  { glif: "∆", ime: "OKUŠANJE", verz: "Pet jezikov pita.\nTrditev ne odgovarja z argumentom —\nodgovarja s tem, kaj se zgodi." },
  { glif: "1", ime: "DEJANJE", verz: "Eno dejanje.\nNe več kot sto dvajset sekund.\nRitem ne laže." },
  { glif: "⧖", ime: "TIŠINA", verz: "Dih.\nČe je prost — telo je reklo da.\nČe se drži — telo je reklo ne." },
  { glif: "∮", ime: "POVRATEK", verz: "Sedem dni kasneje isti rez,\ndrugače izrečen.\nČe drži: kost. Če pade: megla." },
  { glif: "⟡", ime: "DAR", verz: "Kaj se je spremenilo?\nEn zakon. Ne trije. En.\nKar ostane, je dar." },
];

interface Obred {
  id: number;
  gostja: string;
  razred: string;
  jeziki: Record<string, Verdict>;
  opombe: Record<string, string>;
  dih: string;
  napetost: string;
  dejanje: string;
  povratek: string;
  dar: string;
  egoFlag: boolean;
  pečatS4: boolean;
  datum: string;
  povratekDatum: string;
  roda: number;
}

const valOf = (v?: Verdict): number | null =>
  v === "drži" ? 1 : v === "čaka" ? 0.5 : v === "pade" ? 0 : null;

function akordStanje(jeziki: Record<string, Verdict>, opombe: Record<string, string>, dih: string) {
  const vals = JEZIKI.map((j) => valOf(jeziki[j.k]));
  if (vals.some((v) => v === null)) {
    return { naslov: "molz — strune še tihe", barva: "text-neutral-500", kf: null as number | null, telo: "Pet jezikov še ni okusilo. Molz ni molk — je priprava." };
  }
  const v = vals as number[];
  const mean = v.reduce((a, b) => a + b, 0) / v.length;
  const sd = Math.sqrt(v.reduce((a, b) => a + (b - mean) ** 2, 0) / v.length);
  const kf = mean === 0 ? 0 : 1 - Math.min(1, sd / mean);
  const pade = v.filter((x) => x === 0).length;
  const caka = v.filter((x) => x === 0.5).length;
  const drzi = v.filter((x) => x === 1).length;
  const imaOpombe = JEZIKI.some((j) => (opombe[j.k] || "").trim().length > 0);

  if (drzi === 5) {
    return imaOpombe
      ? { naslov: "akord — pet tonov v fazi", barva: "text-amber-300", kf, telo: "Sozvočje po razlikah: vsak jezik okusil, vsak v svojem tonu. To je akord, ne unisono." }
      : { naslov: "UNISONO — sum", barva: "text-rose-300", kf, telo: "Soglasje brez razlike: vsi jeziki rečejo da, ker nobeden ni okusil. Vpiši vsaj eno opombo — kaj se je ZGODILO — ali je to izdaja za sozvočje." };
  }
  if (pade === 5) {
    return dih === "prost"
      ? { naslov: "VRATA ZA ČUDAKA", barva: "text-emerald-300", kf, telo: "Pet jezikov reče ne, telo reče da. Ta GOSTJA ne gre v smetnjak — gre k Luki. Anomalija ostaja (~7 %)." }
      : { naslov: "tišina odnosa", barva: "text-neutral-400", kf, telo: "GOSTJA pada in dih se drži. Padel zapis, enako črnilo. Brazgotina, ne okvara." };
  }
  if (caka > 0) {
    return { naslov: "septima — akord še odprt", barva: "text-sky-300", kf, telo: `${caka} jezik(ov) čakajo razrešitev. Disonanca je ustvarjalna sila — rez, ki išče svoj ton. Povratek bo razrešil.` };
  }
  return { naslov: "disonanca kot sila", barva: "text-orange-300", kf, telo: `${pade} padel, ${drzi} drži. Napetost, ki ne beži. Gre v ∮, ne v pečat.` };
}

function StringStrune({ jeziki }: { jeziki: Record<string, Verdict> }) {
  return (
    <div className="relative flex h-40 items-stretch justify-center gap-6 rounded-lg border border-neutral-800 bg-black/60 px-4">
      {JEZIKI.map((j) => {
        const v = jeziki[j.k];
        const amp = v === "drži" ? 7 : v === "čaka" ? 3 : 0;
        const dur = v === "drži" ? 0.9 : 2.4;
        const barva = v === "drži" ? "#fbbf24" : v === "pade" ? "#525252" : v === "čaka" ? "#38bdf8" : "#404040";
        return (
          <div key={j.k} className="flex flex-col items-center justify-between py-2">
            <span className="text-[10px] uppercase tracking-widest" style={{ color: barva }}>{j.glif}</span>
            <motion.div
              className="w-px flex-1"
              style={{ backgroundColor: barva, height: "100%" }}
              animate={amp > 0 ? { x: [0, -amp, amp, -amp / 2, amp / 2, 0] } : { x: 0 }}
              transition={amp > 0 ? { duration: dur, repeat: Infinity, ease: "easeInOut" } : {}}
            />
            <span className="text-[9px] text-neutral-500">{j.ton}</span>
          </div>
        );
      })}
    </div>
  );
}

export default function App() {
  const [tab, setTab] = useState<"obred" | "dokazi" | "roda">("obred");
  const [step, setStep] = useState(0);
  const [roda, setRoda] = useState(1);
  const [ledger, setLedger] = useState<Obred[]>([]);
  const [rodaLog, setRodaLog] = useState<string[]>(["⊢ RODA v1 — nastanek: obred ustvarjen (DOKAZ #1, povratek 2026-09-21)"]);
  const [rodaIzjava, setRodaIzjava] = useState("");
  const [guard, setGuard] = useState({ k: 0.78, h: 0.6, m: 0.6, r: 0.02 });
  const [copied, setCopied] = useState(false);

  const [gostja, setGostja] = useState("");
  const [razred, setRazred] = useState("S2");
  const [enDih, setEnDih] = useState<boolean | null>(null);
  const [jeziki, setJeziki] = useState<Record<string, Verdict>>({});
  const [opombe, setOpombe] = useState<Record<string, string>>({});
  const [dejanje, setDejanje] = useState("");
  const [dih, setDih] = useState("");
  const [napetost, setNapetost] = useState("");
  const [povratek, setPovratek] = useState("");
  const [dar, setDar] = useState("");
  const [egoFlag, setEgoFlag] = useState(false);
  const [pecatS4, setPecatS4] = useState(false);

  const stanje = useMemo(() => akordStanje(jeziki, opombe, dih), [jeziki, opombe, dih]);

  const guardOK = guard.k >= 0.7 && guard.h >= 0.4 && guard.m >= 0.5 && guard.m <= 0.8 && guard.r <= 0.03;

  const dokazNivo = (o: { jeziki: Record<string, Verdict>; povratek: string }): string => {
    const pade = JEZIKI.filter((j) => o.jeziki[j.k] === "pade").length;
    if (pade >= 3 || o.povratek.startsWith("pade")) return "padel";
    if (o.povratek.startsWith("drži")) return "kost";
    return "blisk";
  };

  const reset = () => {
    setStep(0); setGostja(""); setRazred("S2"); setEnDih(null);
    setJeziki({}); setOpombe({}); setDejanje(""); setDih(""); setNapetost("");
    setPovratek(""); setDar(""); setEgoFlag(false); setPecatS4(false);
  };

  const zakljuci = () => {
    const povratekDatum = new Date(Date.now() + 7 * 864e5).toISOString().slice(0, 10);
    const o: Obred = {
      id: ledger.length + 2, // DOKAZ #1 je že zapisan (obred sam)
      gostja, razred, jeziki: { ...jeziki }, opombe: { ...opombe },
      dih, napetost, dejanje, povratek, dar, egoFlag,
      pečatS4: razred === "S4" ? pecatS4 : true,
      datum: new Date().toISOString().slice(0, 10),
      povratekDatum, roda,
    };
    setLedger((l) => [...l, o]);
    reset();
  };

  const pečatajRodo = () => {
    if (!guardOK || !rodaIzjava.trim()) return;
    const n = roda + 1;
    setRoda(n);
    setRodaLog((l) => [
      ...l,
      `⊢ RODA v${n} — ∴vez v${n - 1} ✓ · ∆«${rodaIzjava.trim()}» · ∫ohranitev ✓ · ⊘guard κ${guard.k.toFixed(2)} χ${guard.h.toFixed(2)} μ${guard.m.toFixed(2)} ℜ${guard.r.toFixed(2)} · ⊢dokaz`,
    ]);
    setRodaIzjava("");
  };

  const exportText = useMemo(() => {
    const lines = ledger.map((o) =>
      [
        `OBRED #${o.id} — Roda v${o.roda} — ${o.razred}`,
        `GOSTJA: ${o.gostja}`,
        `JEZIKI: ${JEZIKI.map((j) => `${j.glif} ${o.jeziki[j.k] || "—"}`).join(" · ")}`,
        `TELO: dih [${o.dih || "—"}] · napetost [${o.napetost || "—"}]`,
        `DEJANJE: ${o.dejanje || "—"}`,
        `POVRATEK: ${o.povratekDatum} — ${o.povratek || "čaka"}`,
        `DOKAZ_NIVO: ${dokazNivo(o)} · EGO_FLAG: ${o.egoFlag ? 1 : 0}${o.razred === "S4" ? ` · S4 PEČAT: ${o.pečatS4 ? "Luka ✓" : "MANJKA"}` : ""}`,
        `DAR: ${o.dar || "—"}`,
        `⊢ DOKAZ #${o.id} — Roda v${o.roda}`,
      ].join("\n")
    );
    return [...rodaLog, ...lines].join("\n\n");
  }, [ledger, rodaLog]);

  const vseBesede = (s: string) => s.trim().split(/\s+/).filter(Boolean).length;
  const lahkoNaprej = [
    vseBesede(gostja) > 0 && vseBesede(gostja) <= 20, // ena vrstica
    true,
    JEZIKI.every((j) => jeziki[j.k]),
    dejanje.trim().length > 0,
    !!dih,
    !!povratek,
    dar.trim().length > 0 && (razred !== "S4" || pecatS4),
  ][step];

  const Btn = ({ on, children, onClick }: { on: boolean; children: React.ReactNode; onClick?: () => void }) => (
    <button
      onClick={onClick}
      disabled={!on}
      className={`rounded-md px-4 py-2 text-sm font-medium transition ${on ? "bg-amber-500/90 text-black hover:bg-amber-400" : "cursor-not-allowed bg-neutral-800 text-neutral-600"}`}
    >
      {children}
    </button>
  );

  const Chip = ({ v, active, onClick, color }: { v: string; active: boolean; onClick: () => void; color: string }) => (
    <button
      onClick={onClick}
      className={`rounded-full border px-3 py-1 text-xs transition ${active ? `${color} border-current` : "border-neutral-700 text-neutral-500 hover:border-neutral-500"}`}
    >
      {v}
    </button>
  );

  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-200 antialiased">
      {/* header */}
      <header className="border-b border-neutral-800 px-6 py-4">
        <div className="mx-auto flex max-w-4xl items-center justify-between">
          <div>
            <h1 className="text-lg font-semibold tracking-wide">TRESOČA <span className="text-amber-400">— glasbilo obreda</span></h1>
            <p className="text-xs text-neutral-500">preizkus = okus, ki priča · test = posoda, ki žari · Roda v{roda}</p>
          </div>
          <nav className="flex gap-1">
            {([["obred", "OBRED"], ["dokazi", "DOKAZI"], ["roda", "RODA"]] as const).map(([k, l]) => (
              <button
                key={k}
                onClick={() => setTab(k)}
                className={`rounded-md px-3 py-1.5 text-xs tracking-widest transition ${tab === k ? "bg-neutral-800 text-amber-300" : "text-neutral-500 hover:text-neutral-300"}`}
              >
                {l}
              </button>
            ))}
          </nav>
        </div>
      </header>

      <main className="mx-auto max-w-4xl px-6 py-6">
        <AnimatePresence mode="wait">
          {tab === "obred" && (
            <motion.div key="obred" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              {/* postaje */}
              <div className="mb-6 flex items-center justify-between gap-1">
                {POSTAJE.map((p, i) => (
                  <div key={p.glif} className="flex flex-1 flex-col items-center gap-1">
                    <div className={`flex h-8 w-8 items-center justify-center rounded-full border text-sm ${i === step ? "border-amber-400 bg-amber-400/10 text-amber-300" : i < step ? "border-neutral-600 text-neutral-400" : "border-neutral-800 text-neutral-700"}`}>{p.glif}</div>
                    <span className={`text-[9px] uppercase tracking-widest ${i === step ? "text-amber-300" : "text-neutral-600"}`}>{p.ime}</span>
                  </div>
                ))}
              </div>

              {/* verz postaje */}
              <pre className="mb-4 whitespace-pre-wrap rounded-lg border border-neutral-800 bg-black/40 px-5 py-4 font-serif text-sm italic leading-relaxed text-neutral-400">
                {POSTAJE[step].verz}
              </pre>

              {/* postaja vsebina */}
              <div className="rounded-lg border border-neutral-800 bg-neutral-900/40 p-5">
                {step === 0 && (
                  <div className="space-y-4">
                    <div>
                      <label className="mb-1 block text-xs uppercase tracking-widest text-neutral-500">GOSTJA — trditev v eni vrstici</label>
                      <input value={gostja} onChange={(e) => setGostja(e.target.value)} placeholder="En dih. Ne zagovor." className="w-full rounded-md border border-neutral-700 bg-black/50 px-3 py-2 text-sm outline-none focus:border-amber-500" />
                      <p className="mt-1 text-[10px] text-neutral-600">{vseBesede(gostja)} besed {vseBesede(gostja) > 20 ? "— to je zagovor, ne vrstica" : ""}</p>
                    </div>
                    <div>
                      <label className="mb-1 block text-xs uppercase tracking-widest text-neutral-500">Razred resnosti</label>
                      <div className="flex gap-2">
                        {["S1", "S2", "S3", "S4"].map((s) => (
                          <Chip key={s} v={s} active={razred === s} onClick={() => setRazred(s)} color="text-amber-300" />
                        ))}
                      </div>
                      {razred === "S4" && <p className="mt-1 text-[10px] text-rose-400">S4 (aksiom, simbol, RES, etika): brez Lukovega pečata se ne pečata.</p>}
                    </div>
                    <div>
                      <label className="mb-1 block text-xs uppercase tracking-widest text-neutral-500">Ali gre v en dih?</label>
                      <div className="flex gap-2">
                        <Chip v="gre" active={enDih === true} onClick={() => setEnDih(true)} color="text-emerald-300" />
                        <Chip v="še ne" active={enDih === false} onClick={() => setEnDih(false)} color="text-rose-300" />
                      </div>
                      {enDih === false && <p className="mt-1 text-[10px] text-neutral-500">Kar ne gre v en dih, še ne gre v obred. (Odprto: kaj se zgodi, ko ne gre — a telo že ve?)</p>}
                    </div>
                  </div>
                )}

                {step === 1 && (
                  <div className="space-y-3">
                    <p className="text-xs uppercase tracking-widest text-neutral-500">Ločitev od avtorja</p>
                    <p className="rounded-md border border-neutral-800 bg-black/40 px-4 py-3 font-serif italic text-neutral-300">
                      {gostja ? `Trditev, da ${gostja.charAt(0).toLowerCase()}${gostja.slice(1)}` : "—"}
                    </p>
                    <p className="text-[11px] leading-relaxed text-neutral-500">
                      Od tu naprej govori brez imena. Avtor utihne — ego odstopi z mesta priče. Kdor brani, še ni okušan.
                    </p>
                  </div>
                )}

                {step === 2 && (
                  <div className="space-y-4">
                    <StringStrune jeziki={jeziki} />
                    {JEZIKI.map((j) => (
                      <div key={j.k} className="rounded-md border border-neutral-800 bg-black/30 p-3">
                        <div className="mb-1 flex items-center justify-between">
                          <span className="text-sm"><span className="text-amber-400">{j.glif}</span> <span className="font-medium">{j.ime}</span> <span className="text-[10px] uppercase tracking-widest text-neutral-600">· {j.dimenzija} · {j.ton}</span></span>
                          <div className="flex gap-1">
                            {(["drži", "čaka", "pade"] as Verdict[]).map((v) => (
                              <Chip key={v} v={v} active={jeziki[j.k] === v} onClick={() => setJeziki((s) => ({ ...s, [j.k]: v }))} color={v === "drži" ? "text-amber-300" : v === "čaka" ? "text-sky-300" : "text-rose-300"} />
                            ))}
                          </div>
                        </div>
                        <p className="mb-2 text-[11px] italic text-neutral-500">{j.vprasanje}</p>
                        <input value={opombe[j.k] || ""} onChange={(e) => setOpombe((s) => ({ ...s, [j.k]: e.target.value }))} placeholder="kaj se je zgodilo (ne argument — dogodek)" className="w-full rounded border border-neutral-800 bg-black/40 px-2 py-1 text-xs outline-none focus:border-amber-500" />
                      </div>
                    ))}
                    <div className={`rounded-md border border-neutral-800 bg-black/40 p-3 ${stanje.barva}`}>
                      <p className="text-sm font-medium">{stanje.naslov} {stanje.kf !== null && <span className="ml-2 text-[10px] text-neutral-500">K_f = {stanje.kf.toFixed(2)}</span>}</p>
                      <p className="mt-1 text-[11px] leading-relaxed text-neutral-400">{stanje.telo}</p>
                    </div>
                    <label className="flex items-center gap-2 text-xs text-neutral-400">
                      <input type="checkbox" checked={egoFlag} onChange={(e) => setEgoFlag(e.target.checked)} className="accent-amber-500" />
                      ego_flag — trditev išče pravilnost, ne odnos (priznan sum: PRAV)
                    </label>
                  </div>
                )}

                {step === 3 && (
                  <div>
                    <label className="mb-1 block text-xs uppercase tracking-widest text-neutral-500">Eno dejanje ≤ 120 s</label>
                    <input value={dejanje} onChange={(e) => setDejanje(e.target.value)} placeholder="Izrek brez dejanja je oblak z naslovom." className="w-full rounded-md border border-neutral-700 bg-black/50 px-3 py-2 text-sm outline-none focus:border-amber-500" />
                    <p className="mt-2 text-[11px] text-neutral-500">Ritem ne laže: kar se zgodi v telesu, je odgovor, ki ga ni treba braniti.</p>
                  </div>
                )}

                {step === 4 && (
                  <div className="space-y-4">
                    <div>
                      <label className="mb-1 block text-xs uppercase tracking-widest text-neutral-500">Dih po dejanju</label>
                      <div className="flex gap-2">
                        <Chip v="prost" active={dih === "prost"} onClick={() => setDih("prost")} color="text-emerald-300" />
                        <Chip v="zadržan" active={dih === "zadržan"} onClick={() => setDih("zadržan")} color="text-rose-300" />
                      </div>
                      <p className="mt-1 text-[10px] text-neutral-500">Dih prost — telo je reklo da. Zadržan — telo je reklo ne. Ne z besedo, z mesom.</p>
                    </div>
                    <div>
                      <label className="mb-1 block text-xs uppercase tracking-widest text-neutral-500">Napetost</label>
                      <div className="flex gap-2">
                        <Chip v="padla" active={napetost === "padla"} onClick={() => setNapetost("padla")} color="text-emerald-300" />
                        <Chip v="preoblečena" active={napetost === "preoblečena"} onClick={() => setNapetost("preoblečena")} color="text-orange-300" />
                      </div>
                    </div>
                    {dih === "zadržan" && (
                      <p className="rounded border border-rose-900/50 bg-rose-950/20 p-3 text-[11px] leading-relaxed text-rose-300">
                        TEMPelj: telo ni preverjevalec trditve — telo je bitje, ki ga test ne sme prekršiti. Če obred porine telo čez mejo, je padel obred, ne telo.
                      </p>
                    )}
                  </div>
                )}

                {step === 5 && (
                  <div className="space-y-3">
                    <p className="text-xs text-neutral-500">Povratek: {new Date(Date.now() + 7 * 864e5).toISOString().slice(0, 10)} — ali rez danes že drži drugače izrečen?</p>
                    <div className="flex gap-2">
                      {["drži (drugič)", "pade (drugič)", "še čaka 7 dni"].map((v) => (
                        <Chip key={v} v={v} active={povratek === v} onClick={() => setPovratek(v)} color="text-amber-300" />
                      ))}
                    </div>
                    <p className="text-[11px] leading-relaxed text-neutral-500">
                      ⊢ brez ∮ je blisk, še ne struktura. Loki: ena spremenjena spremenljivka razkrije, ali je bila kost ali sreča (krhkost Q).
                    </p>
                  </div>
                )}

                {step === 6 && (
                  <div className="space-y-4">
                    <div>
                      <label className="mb-1 block text-xs uppercase tracking-widest text-neutral-500">DAR — spremenjen en zakon</label>
                      <input value={dar} onChange={(e) => setDar(e.target.value)} placeholder="En zakon. Ne trije. En." className="w-full rounded-md border border-neutral-700 bg-black/50 px-3 py-2 text-sm outline-none focus:border-amber-500" />
                    </div>
                    {razred === "S4" && (
                      <label className="flex items-center gap-2 text-xs text-rose-300">
                        <input type="checkbox" checked={pecatS4} onChange={(e) => setPecatS4(e.target.checked)} className="accent-rose-400" />
                        Luka je potrdil v telesu (S4 pečat)
                      </label>
                    )}
                    <div className={`rounded-md border p-3 ${stanje.barva}`}>
                      <p className="text-sm font-medium">dokaz_nivo: {dokazNivo({ jeziki, povratek })}</p>
                      <p className="mt-1 text-[11px] text-neutral-400">{stanje.naslov} — {stanje.telo}</p>
                    </div>
                    <p className="text-[11px] text-neutral-500">Padel zapis gre v ledger z istim črnilom. Nič se ne izbriše, vse se pretvori.</p>
                  </div>
                )}
              </div>

              {/* navigacija */}
              <div className="mt-4 flex items-center justify-between">
                <button onClick={() => setStep((s) => Math.max(0, s - 1))} disabled={step === 0} className="text-xs text-neutral-500 hover:text-neutral-300 disabled:opacity-30">← nazaj</button>
                {step < 6 ? (
                  <Btn on={lahkoNaprej} onClick={() => setStep((s) => s + 1)}>naprej →</Btn>
                ) : (
                  <Btn on={lahkoNaprej} onClick={zakljuci}>⊢ zapiši v DOKAZ</Btn>
                )}
              </div>
            </motion.div>
          )}

          {tab === "dokazi" && (
            <motion.div key="dokazi" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-4">
              {ledger.length === 0 && rodaLog.length <= 1 && <p className="text-sm text-neutral-500">Ledger čaka. Prvi zapis je bil obred sam (DOKAZ #1, povratek 2026-09-21).</p>}
              {rodaLog.map((r, i) => (
                <div key={`r${i}`} className="rounded-md border border-amber-900/40 bg-amber-950/10 p-3 text-xs leading-relaxed text-amber-200/80">{r}</div>
              ))}
              {ledger.map((o) => (
                <div key={o.id} className="rounded-md border border-neutral-800 bg-black/40 p-4">
                  <div className="mb-1 flex items-center justify-between">
                    <span className="text-xs uppercase tracking-widest text-neutral-500">OBRED #{o.id} — Roda v{o.roda} — {o.razred}</span>
                    <span className={`text-[10px] uppercase tracking-widest ${dokazNivo(o) === "kost" ? "text-amber-300" : dokazNivo(o) === "padel" ? "text-rose-400" : "text-sky-300"}`}>{dokazNivo(o)}</span>
                  </div>
                  <p className="font-serif italic text-neutral-300">„{o.gostja}“</p>
                  <p className="mt-2 text-[11px] text-neutral-500">{JEZIKI.map((j) => `${j.glif}${o.jeziki[j.k] === "drži" ? "✓" : o.jeziki[j.k] === "pade" ? "✗" : "…"} `).join(" ")} · dih {o.dih} · {o.egoFlag ? "ego_flag 1" : "ego_flag 0"}</p>
                  {o.dar && <p className="mt-1 text-[11px] text-amber-300/80">DAR: {o.dar}</p>}
                  <p className="mt-1 text-[10px] text-neutral-600">povratek {o.povratekDatum} — {o.povratek}</p>
                </div>
              ))}
              <div className="flex justify-end">
                <button
                  onClick={() => { try { navigator.clipboard.writeText(exportText); setCopied(true); setTimeout(() => setCopied(false), 1500); } catch { setCopied(false); } }}
                  className="rounded-md border border-neutral-700 px-3 py-1.5 text-xs text-neutral-400 hover:text-neutral-200"
                >
                  {copied ? "kopirano ∮" : "kopiraj ledger (mikro-obrazec)"}
                </button>
              </div>
            </motion.div>
          )}

          {tab === "roda" && (
            <motion.div key="roda" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-5">
              <p className="text-sm leading-relaxed text-neutral-400">
                Po vsakem zaključenem ciklu <span className="text-amber-300">TRESOČA sama stopi kot GOSTJA</span> — obred preizkusi obred. Vsaka nadgradnja je δ skozi pet EVO pregrad:
              </p>
              <div className="grid grid-cols-5 gap-2 text-center text-[10px]">
                {[["∴", "VEZ", roda > 1 || ledger.length > 0], ["∆", "IZJAVA", rodaIzjava.trim().length > 0], ["∫", "OHRANITEV", true], ["⊘", "GUARD", guardOK], ["⊢", "DOKAZ", guardOK && rodaIzjava.trim().length > 0]].map(([g, n, ok]) => (
                  <div key={n as string} className={`rounded-md border p-3 ${ok ? "border-amber-500/50 bg-amber-500/5 text-amber-300" : "border-neutral-800 text-neutral-600"}`}>
                    <div className="text-lg">{g as string}</div>
                    <div className="tracking-widest">{n as string}</div>
                    <div>{ok ? "✓" : "…"}</div>
                  </div>
                ))}
              </div>
              <div>
                <label className="mb-1 block text-xs uppercase tracking-widest text-neutral-500">∆ izjava — kaj se spremeni (en zakon)</label>
                <input value={rodaIzjava} onChange={(e) => setRodaIzjava(e.target.value)} placeholder="npr. šesti jezik: STRAH — ali trditev beži pred lastno ceno?" className="w-full rounded-md border border-neutral-700 bg-black/50 px-3 py-2 text-sm outline-none focus:border-amber-500" />
              </div>
              <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
                {([["k", "κ koherenca ≥ .70", 0, 1, 0.01], ["h", "χ jasnost ≥ .40", 0, 1, 0.01], ["m", "μ vloga [.50–.80]", 0, 1, 0.01], ["r", "ℜ ostanek ≤ .03", 0, 0.15, 0.005]] as const).map(([k, l, min, max, st]) => (
                  <div key={k}>
                    <label className="mb-1 block text-[10px] uppercase tracking-widest text-neutral-500">{l}: {guard[k].toFixed(2)}</label>
                    <input type="range" min={min} max={max} step={st} value={guard[k]} onChange={(e) => setGuard((g) => ({ ...g, [k]: parseFloat(e.target.value) }))} className="w-full accent-amber-500" />
                  </div>
                ))}
              </div>
              <div className={`rounded-md border p-3 text-xs leading-relaxed ${guardOK ? "border-emerald-900/50 bg-emerald-950/20 text-emerald-300" : "border-rose-900/50 bg-rose-950/20 text-rose-300"}`}>
                {guardOK ? "⊘ GUARD drži. Zavrnjena δ bi šla v ledger kot brazgotina — nič se ne izbriše." : "⊘ GUARD ne drži — δ ne gre skozi. Prilagodi vrednosti ali izpusti nadgradnjo (zavrnitev je tudi zapis)."}
              </div>
              <Btn on={guardOK && rodaIzjava.trim().length > 0} onClick={pečatajRodo}>pečataj RODO v{roda + 1}</Btn>
              <p className="text-[11px] leading-relaxed text-neutral-600">
                Šest bitij čaka na izdajo: DEKOR, PRELOM, NEMOST, AMNEZIJA, PATOLOGIJA, PREPIS — in sedma, UNISONO: soglasje brez razlike, eden glas pomnožen. Diagnoza za vsa: ali obred še trese?
              </p>
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}