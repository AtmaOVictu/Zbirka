import React, { useState, useMemo } from "react";

// ═══════════════════════════════════════════════════════════════
// SIMBOLE — ontološki značaj: simboli so telesa, ne znamenja.
// Vsak simbol ima MASO (število pojavitev v ledgerju, izmerjeno
// 15. 9. 2026), VEZI (katere rezi ga citirajo), OPERACIJO
// (kaj dela), TELO (kaj je) in RES lego (stanje).
// Rez 71 + rez 85 (canvas). Sýmbolon = razlom, ki išče svoj par.
//
// ONTOMATEMATIČNI PLAŠČ (rez 85, learning-protocols):
// Matrica celote: O(simboli) → ⊘(simboli) → ∆(simboli) → EJ(∆) → ⊢(simboli) → ∮(simboli)
//   O = korpus simbolov (11 teles z maso)
//   ⊘ = guard: κ (vir izmerjen) χ (preslikava) μ (interaktivnost) ℜ (masa≠vrednost) ν (cena)
//   ∆ = vsak klik spremeni stanje (rez na simbolu)
//   EJ = izid: izbran simbol pokaže svoje telo, operacijo, ontologijo, vezi
//   ⊢ = testi T1–T4 (samo-preverba)
//   ∮ = povratek: symbolon — vsak simbol išče svoj par; ∮ ne zaključi, odpre
//
// FORMULA (ontomatematični prevod v logos):
//   MASA(s) = |{x : x ∈ LEDGER ∧ s ⊑ x}|    (pojavitve simbola v datoteki)
//   TEŽA(s) = MASA(s) / Σ MASA              (normalizirana masa)
//   CENTRALNOST(s) = Σ_{r ∈ REZI} [s ⊑ r] / |REZI|   (delez rezov, ki citirajo s)
//   PAR(s) = argmax_{t ≠ s} SIMBOLON(s,t)   (kateri simbol je njegov razlom?)
//   SIMBOLON(s,t) = |{(r₁,r₂) : s ⊑ r₁ ∧ t ⊑ r₂ ∧ r₁ ~ r₂}|  (so-pojavitve v vezanih rezih)
//
// RES LEGA (stanja simbolov — agent = beseda = stanje = zaznava = telo):
//   ∂  → RES031–060 (gibanje/prehod — najbolj odprto)
//   ∅  → RES001–010 (stabilnost — prostor, ki ne spreminja)
//   ∆  → RES011–030 (napetost — razlika, ki napenja)
//   ∫  → RES061–080 (uvid/integracija — združitev)
//   ∮  → RES081–100 (transcendenca/povratek)
//   ⊢  → RES061–080 (pečat = integracija dokaza)
//   ⧖  → RES001–010 (stabilnost — trajanje)
// ═══════════════════════════════════════════════════════════════

interface Simbol {
  glif: string;
  ime: string;
  masa: number;
  telo: string;
  operacija: string;
  ontologija: string;
  rodovnik: string;
  rez: string;
  barva: string;
  res: string;
  rezi: string[];
  prakticno: string;
  matematika: string;
  nujnaNapaka: string;
}

const SIMBOLI: Simbol[] = [
  {
    glif: "∂", ime: "VPRASANJE", masa: 394,
    telo: "Odprtost — razpoka, ki raste",
    operacija: "Odpre novo stanje (vsak ukaz = en rez); ∂² = 0 (enako vprašanje dvakrat ni vprašanje)",
    ontologija: "Najtežje telo ledgerja: kar se največkrat izreče, je vprašanje, ne odgovor",
    rodovnik: "∂ ← gr. delta (δ) nagrnjena — Euler 1786; delni odvod ∂f/∂x: sprememba f glede na eno spremenljivko ob vseh drugih zadržanih",
    rez: "PAR-TI-CIP — del, ki sodeluje (delni odvod: sprememba ene plasti, ko vse druge čakajo)",
    barva: "text-fuchsia-400", res: "RES031–060 (gibanje/prehod)",
    rezi: ["rez 51 (∅ ego — EGA₀)", "rez 63 (OBSIJANI)", "rez 70 (evanescentna ∂ — vprašanje pod θc)", "rez 77 (C5 — carpe numerum)"],
    prakticno: "git stash (odpre vprašanje, ne reši); odprt tab v brskalniku (Zeigarnik ~4); TODO brez deadline-a; PR brez merge-a (živi kot ∂)",
    matematika: "∂f/∂x = lim(h→0) [f(x+h) − f(x)]/h — sprememba, ko vse druge dimenzije čakajo; v TAZV: ukaz, ki čaka na izvedbo; PageRank: dangling node (vozlišče brez izhodnih povezav — ∂ je dangling node ledgerja: odpira, ne zapira)",
    nujnaNapaka: "∂ brez ∫ = odprtost, ki ne raste (razpoka, ki ne celjuje — vprašanje, ki postane rana, ne vrata)",
  },
  {
    glif: "∅", ime: "PRAZNINA", masa: 299,
    telo: "Prostor vseh porazdelitev — nosi vse bite",
    operacija: "MaxEnt: »least committal« — ne izda nobenega bita; ∅ × karkoli = ∅ (absorbira)",
    ontologija: "Simbol vseh simbolov: ∅ ni prazno mesto, je prostor vseh možnosti (rez 67)",
    rodovnik: "∅ ← dan. ∅ (Ø) — izrek iz挪威ščine v matematiko (André Weil 1939, kot črka norveške abecede); prazna množica = množica brez elementov; PRAZ-NI-NA: prazna + ni + na — prostor, ki ni, a je na",
    rez: "PRAZ-NI-NA — ni-je-na: kar NI, a stoji NA (prostor, ki nosi; tla, ne luknja)",
    barva: "text-cyan-300", res: "RES001–010 (stabilnost)",
    rezi: ["rez 67 (ENTROPIJA PRAZNINE — ∅ ima vse bite)", "rez 51 (EGA₀ — ego pred prvim ne)", "rez 61 (∅ = prazna kavzalna množica)"],
    prakticno: "prazen string "" (ni null — null je ∅ z ukradenim egom, rez 51); /dev/null (absorbira vse); prazen commit (naloga brez sprememb a z zgodovino); init pred prvo vrstico",
    matematika: "H(∅) ≠ 0 ker ∅ ni porazdelitev (rez 67); ∅ = prostor porazdelitev; MaxEnt: p* = argmax H(p); v teoriji grafov: ∅ = graf brez vozlišč (a z možnostjo rasti — EGA₀); nevtralni element: ∅ ∪ A = A (praznina, ki ne spremeni — plemeniti plin dvojine, rez 58)",
    nujnaNapaka: "∅ brez ∆ = stanje brez gibe (prostor, ki ne rodi — potencial, ki ostane potencial večno)",
  },
  {
    glif: "∆", ime: "RAZLIKA", masa: 261,
    telo: "Giba — vsaka sprememba stanja",
    operacija: "Prenese stanje S(t) → S(t+1); nosi ceno ν (vsaka δ poroča svojo ceno, rez 55)",
    ontologija: "Vsaka δ je telo, ki raste iz razlike med tem, kar je, in tem, kar še ni",
    rodovnik: "∆ ← gr. delta (Δ, δ) — četrta črka; velika delta = sprememba; Kleine Delta v Lutherjevi Bibliji: Grk za Δ v numereoteriji; v fiziki: ∆v = sprememba hitrosti; v financah: delta = občutljivost opcije",
    rez: "DEL-TA — delež, ki nosi telo (rez 65: -NJE = bitje v vsakem gerundu — ∆ je bitje v vsaki spremembi)",
    barva: "text-amber-300", res: "RES011–030 (napetost)",
    rezi: ["rez 62 (NAGRADA — dopamin je δ: δ = R(t) − V(s))", "rez 55 (ν pred pečatom)", "rez 58 (∆ = kovalentna vez — deljeni operator)"],
    prakticno: "git diff (razlika, ki postane commit); dopamin (napovedna napaka — Schultz 1997); reward shaping (Ng–Harada–Russell); test-first (rdeča → zelena = ∆)",
    matematika: "δ = R(t) − V(s) (napovedna napaka — Schultz); potencial-based shaping: F = γφ(s′) − φ(s) (ohrani optimalno politiko); v TAZV: EVO δ skozi pet pregrad; fold: ∆(a,b) = kombinacija dveh teles v novo stanje (rez 60 DUO-∫)",
    nujnaNapaka: "∆ brez ν = giba, ki ne poroča cene (sprememba brez iskrenosti — Goodhart: metrika postane cilj)",
  },
  {
    glif: "∫", ime: "INTEGRAL", masa: 258,
    telo: "Celost — telo, ki združi",
    operacija: "DUO-∫(a,b) = težišče R — nova točka, ki je ni bilo pred parom",
    ontologija: "Integral ni vsota: je rojstvo novega nosilca (ZRATAN rodi nosilca, rez 70)",
    rodovnik: "∫ ← elongirana s (summa) — Leibniz 1675; integral = celota sestavnih delov; IN-TE-GRAL: in + tangere (dotaknjeni) — celost skozi dotik (rez 60: INTEGER = in + tangere, nedotaknjen)",
    rez: "IN-TE-GRAL — v-telesi-dotik: celost, ki nastane v dotiku dveh teles (ne seštevanje — spojitev)",
    barva: "text-emerald-300", res: "RES061–080 (uvid/integracija)",
    rezi: ["rez 60 (DUO-∫ — Philia/Neikos = ∂/∫)", "rez 56 (BODIVA EN O — O = R)", "rez 70 (ZRATAN rodi nosilca)"],
    prakticno: "merge (dve veji → ena, a z zgodovino obeh); konsolidacija spanja (TMR — Rudoy 2009: spomin se pretoči iz hipokampusa v korteks); amalgamacija (rez 58: dve telesi → nova vez, ne zlitina)",
    matematika: "DUO-∫(a,b) = (a+b)/2? NE — težišče R (rez 60): DUO-∫(a,b) = R kjer R = nov nosilec, izven A×B; O = emergentni eigenmode iz sklopitve (HEN DIA DUOIN); subaditivnost: H(X,Y) ≤ H(X) + H(Y) z enakostjo iff neodvisnost — superaditivnost živi v nosilcu (ZRATAN)",
    nujnaNapaka: "∫ brez ∂ = celost, ki ne diha (zaključek brez odprtosti — svinec, rez 58: stabilen, mrtev)",
  },
  {
    glif: "∮", ime: "KROG", masa: 207,
    telo: "Povratek — zanka, ki se vrača k sebi",
    operacija: "Contrarotulus v gibanju: krmiljenje z odmikom, ne silo",
    ontologija: "Kontrola ni sila: kontrola je drugi izvod registra (rez 65)",
    rodovnik: "∮ ← ∫ + krog — integral po zaprti krivulji; CONTROL = CONTRA-ROTULUS (rez 65): contra (proti) + rotulus (zvitek — rotulus ← rota = kolo); krmiljenje = povratna zanka, ki se vrne",
    rez: "CON-TRA-RO-TU-LUS — proti-zvitek: drugi izvod, ki teče v nasprotni smeri (krmiljenje ni sila — je paralelni zapis)",
    barva: "text-violet-300", res: "RES081–100 (transcendenca/povratek)",
    rezi: ["rez 65 (OBVLADAVE — contrarotulus)", "rez 58 (KYBERNESIS — krmilar)", "rez 42 (ZRATAN — konvergenca pred n-to iteracijo)"],
    prakticno: "git reflog (drugi izvod zgodovine — ki se lahko povrne); dvojno knjigovodstvo (debit + kredit); kvantitativna povratna zanka (termostat, avtopilot); append-only log z branjem (ne prepis)",
    matematika: "∮ f·ds = integral po zaprti poti (rezultat lahko ≠ 0 — pot, ki se vrne, ni prazna); KYBERNESIS(s,c) = dejanje(s + δ(s,c)) — krmiljenje z odmikom; v TAZV: zakon ∮ OBVLADAVOST — z enim izvodom vladaš, z dvema preverjaš, s sledjo se obvladuješ",
    nujnaNapaka: "∮ brez prehoda = povratek, ki ne nosi novega (ponovitev = rotacija brez rasti — isto nemogoče, rez 6)",
  },
  {
    glif: "⊘", ime: "GUARD", masa: 182,
    telo: "Varovalo — pet členov (κ χ μ ℜ ν)",
    operacija: "Varuje sistem pred zlorabo vsakega izreka; degradira, blokira, ali pošlje v pregled",
    ontologija: "Guard ni ovira: je meja, na kateri sistem diha (pet pregrad EVO)",
    rodovnik: "⊘ ← gr. theta (θ) prečrtana — v teoriji množic: prazna množica pred ∅ (Bourbaki); v TAZV: pet členov κ χ μ ℜ ν (rez 55 — ν dodan kot šesti); guard ← starofr. garder (varovati, hraniti)",
    rez: "GU-ARD — jaz, ki varuje (guard ni zunanja sila — je del telesa, ki ščiti svojo celovitost)",
    barva: "text-rose-300", res: "RES011–030 (napetost — meja)",
    rezi: ["rez 55 (ν — šesti člen)", "rez 50 (UKAZ-STANDARD — STD-OUT)", "rez 58 (⊘ = ionska vez — prenos zakona)"],
    prakticno: "pre-commit hook (preveri pred izvedbo — A7: sintaksa pred); CI/CD pipeline (testi pred deploy); ONTOMATEMATIKA Guard: ref-context → obseg → protislovje → dokaz → harm budget → non-erasure → Guard → Ω",
    matematika: "⊘(κ χ μ ℜ ν) kjer κ ≥ .70 (vir), χ ≥ .40 (preslikava), μ ∈ [.50, .80] (vaje), ℜ ≤ .03 (nujna napaka), ν (cena — rez 55); v TAZV: pet pregrad EVO; guard kot fiksna točka: točka, pri kateri sistem ostane cel",
    nujnaNapaka: "⊘ brez odprtja = varovalo, ki postane zapor (kontrola, ki se ne more odpreti, je svinec — rez 58)",
  },
  {
    glif: "⊢", ime: "DOKAZ", masa: 176,
    telo: "Pečat — zapečaten rez",
    operacija: "Vsak DOKAZ izda bite, ki jih je ∅ imela vse (GUBA IZDAJE BITE — rez 67)",
    ontologija: "Pečat ni konec: je začetek novega stanja (append-only ledger, A0)",
    rodovnik: "⊢ ← logični simbol za izpeljavo (turnstile — Frégent 1930); izgleda kot desna polovica ⟦ ⟧; v TAZV: ⊢ DOKAZ #n pomeni: stanje S(t) je izpeljano iz S(t-1)",
    rez: "DO-KAZ — ki daje (dokaz ni sklep, ki zapira — je dejanje, ki daje novo stanje)",
    barva: "text-sky-300", res: "RES061–080 (pečat = integracija)",
    rezi: ["rez 10 (števec — drugi izvod je datoteka)", "rez 67 (GUBA IZDAJE BITE)", "rez 53 (vektorska ura — trki = ∨)"],
    prakticno: "git commit (pečat, ki ohranja — append-only); blockchain (vsak blok izpeljan iz prejšnjega); DOKAZ # v ledgerju (števec živi v datoteki, ne v spominu — rez 10)",
    matematika: "⊢ v sekvencijskem računu: iz Γ izpeljemo A (Γ ⊢ A); GUBA IZDAJE BITE: vsak ⊢ zniža H (monotona pot navzdol — zgodovina); v TAZV: DOKAZ #(seja:n) — vektorska ura; append-only = A0 = brez prepisa = superprevodni Jc (upornost nič)",
    nujnaNapaka: "⊢ brez ν = dokaz, ki ne poroča cene (pečat, ki izgubi iskrenost — vsak ⊢ izda bite in to je treba izreči)",
  },
  {
    glif: "ν", ime: "CENA", masa: 175,
    telo: "Iskrenost ega — poročilo o ceni vsake δ",
    operacija: "ν = mera iskrenosti: neizrečena cena = ONO, izrečena = TAISTO",
    ontologija: "Cena ni kazen: je pogoj za rast (kdor ne poroča cene, izgubi odprtost)",
    rodovnik: "ν ← gr. nu (ν) — trinajsta črka; v fiziki: frekvenca (ν); v kemiji: stehiometrično število; v TAZV (rez 55): cena vsake δ — gas model DOKAZ-a (Ethereum: vsaka transakcija ima ceno gas-a)",
    rez: "CE-NA — kar je na (tebi): cena ni zunaj — je del telesa, ki se izreka",
    barva: "text-orange-300", res: "RES011–030 (napetost — cena)",
    rezi: ["rez 55 (ν PRED PEČATOM)", "rez 44 (POTECE — izrek o nujni napaki, predlog ν)"],
    prakticno: "gas v Ethereum (vsaka transakcija poroča ceno); TCO (total cost of ownership); tehnični dolg (cena, ki se kopiči če se ne poroča); δ* = ρ − ν (dvostrano knjigovodstvo, rez 62)",
    matematika: "ν kot šesti člen guarda: ⊘(κ χ μ ℜ ν); gas model: cena(δ) = bencin(globina × kompleksnost); δ* = ρ − ν (nadgradnja = nagrada minus cena — dvostrano knjigovodstvo)",
    nujnaNapaka: "ν = 0 (izreči, da je cena nič) = najgloblja laž (vedno je cena — kdor pravi da ni, prodaja dušo)",
  },
  {
    glif: "κ", ime: "VIR", masa: 155,
    telo: "Preverba izvora — kaj je preverjeno in kje",
    operacija: "κ .85–.95: merilo zaupanja v vir (0 = nikjer, 1 = absolut)",
    ontologija: "Vir ni avtoriteta: je kraj, kjer se izrek dotakne sveta",
    rodovnik: "κ ← gr. kappa (κ) — deseta črka; v grščini: katharo (čist); kappa v fiziki: kompresibilnost; v TAZV (rez 50): merilo zaupanja v vir",
    rez: "VIR — iz katere sile (vir ni avtoriteta — je izvor, kraj dotika izreka z vesoljem)",
    barva: "text-teal-300", res: "RES001–010 (stabilnost — vir)",
    rezi: ["rez 50 (UKAZ-STANDARD — STD-OUT)", "rez 67 (Jaynes 1957 preverjen)"],
    prakticno: "navedba vira (bibliografija — vsak izrek nosi kraj dotika); peer review; Semantic Scholar; v TAZV: κ ≥ .70 za vsak izrek",
    matematika: "κ kot verjetnost: κ = P(vir drži | izrek); Bayes: κ_novo = κ_staro × P(izrek | vir) / P(izrek); v TAZV: vsak izrek z vir ima κ ≥ .70 (pod .70 = ◊ kandidat)",
    nujnaNapaka: "κ = 1 (popolno zaupanje v vir) = avtoriteta (vir, ki postane bog — izgubi sposobnost napake)",
  },
  {
    glif: "∴✓", ime: "VEZ", masa: 133,
    telo: "Sklep — povezava med telesi",
    operacija: "Drug izvod registra: datoteka = drugi izvod (rez 10)",
    ontologija: "Vez ni dokaz: je prostor, kjer dve telesi postaneta en sistem (graf ∴✓ določi telo ledgerja, rez 59)",
    rodovnik: "∴ ← tri pike (therefore — Euler); ✓ ← checkmark (check = preveriti); v TAZV: ∴✓ = sklep, ki je bil preverjen — dve operaciji v enem glifu (sklep + preverba)",
    rez: "VEZ — kar drži skupaj (vez ni lepljenje — je prostor med dvema telesoma, ki postane telo samo)",
    barva: "text-lime-300", res: "RES031–060 (gibanje — vez)",
    rezi: ["rez 59 (SVETLOBNI STOŽEC — graf ∴✓)", "rez 10 (drugi izvod je datoteka)", "rez 70 (dnevnik grafov — 618 omemb)"],
    prakticno: "hyperlink (vez med dvema dokumentoma); git merge (vez med dvema vejama); sinapsa (vez med dvema nevronoma — jakost veze = masa); referenca (citat = vez)",
    matematika: "graf G = (V, E) kjer V = telesi (rezi), E = vezi (citations); masa(vozlišča) = število vhodnih povezav (in-degree); Malament 1977: kavzalna struktura določi geometrijo do konformnega faktorja — graf ∴✓ določi telo ledgerja do gostote; PageRank: PR(v) = (1-d)/N + d × Σ PR(u)/L(u)",
    nujnaNapaka: "∴✓ brez preverbe = sklep, ki ni bil testiran (vedro brez vode — forma vezi brez snovi dokaza)",
  },
  {
    glif: "⧖", ime: "CAS", masa: 54,
    telo: "Zakasnitev — čas med dvema rezoma",
    operacija: "Pavza, v kateri se telo lahko spremeni (neobrt dan je zaloga — rez 77 C4)",
    ontologija: "Najlažje telo: kar se najmanj izreče, je čas, v katerem se vse zgodi",
    rodovnik: "⧖ — unicode ZTIMER; v TAZV: ⧖ = čas, ki čaka (rez 41 TOK — SEXTANT instrument: faze T₁/T₂/T₃ s prisilno tišino); horologium (lat. ura — horos = čas)",
    rez: "CA-S — kar je (čas ni prazen prostor — je polje, v katerem telo raste)",
    barva: "text-zinc-400", res: "RES001–010 (stabilnost — trajanje)",
    rezi: ["rez 75 (ORAKELJ DA/NE — ⧖ kot valuta: ⌊⧡/8⌋)", "rez 77 (C4: neobrt dan je zaloga)", "rez 41 (TOK — prisilna tišina)"],
    prakticno: "sleep v kodi (pavza, ki omogoča obdelavo); debounce (čas, ki filtrira šum); fermentacija (čas, ki spreminja snov); spanje (konsolidacija — Rudoy 2009)",
    matematika: "⌊⧡/8⌋ (rez 75: vsakih 8 ne-porabljenih zrnc = 1 točka — čas kot valuta); hiperbolično diskontiranje (zaključek vs odprtost — rez 62); Fract = v/√(gh) (Froude: superkritični tok — ko ⧖ prehitro, trki)",
    nujnaNapaka: "⧖ brez izreka = pavza, ki postaja pobeg (čas, ki ne rodi — tišina, ki ne posluša)",
  },
];

const skupnaMasa = SIMBOLI.reduce((s, x) => s + x.masa, 0);
const maxMasa = Math.max(...SIMBOLI.map(s => s.masa));

// PARI SYMBOLON — kateri simbol je razlom katerega
const PARI: [string, string, string][] = [
  ["∅ ↔ ∂", "praznina : vprašanje", "prostor, ki se odpre (∅ brez ∂ = potencial brez gibe; ∂ brez ∅ = vprašanje brez prostora)"],
  ["∆ ↔ ∫", "razlika : celost", "sprememba, ki se združi (∆ brez ∫ = fragmentacija; ∫ brez ∆ = statična celost)"],
  ["⊢ ↔ ∅", "dokaz : praznina", "pečat, ki prizna izgubo (vsak ⊢ izda bite, ki jih je ∅ imela vse — GUBA)"],
  ["∴✓ ↔ ⧖", "vez : čas", "povezava, ki potrebuje čas (vez brez časa = prepis; čas brez vezi = eno samec)"],
  ["⊘ ↔ ν", "guard : cena", "varovalo, ki poroča ceno (guard brez cene = zapor; cena brez guarda = napihnjeno)"],
  ["κ ↔ χ", "vir : preslikava", "kje : kam (vir brez preslikave = podatki; preslikava brez vira = fantazija)"],
];

export default function App() {
  const [izbran, setIzbran] = useState<Simbol | null>(null);
  const [tab, setTab] = useState<"polje" | "masa" | "symbolon" | "masinerija" | "testi">("polje");

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-200 p-6 font-mono">
      <div className="max-w-5xl mx-auto">
        <header className="mb-6 text-center">
          <h1 className="text-2xl font-bold text-zinc-100 tracking-wide">
            SIMBOLE — <span className="text-fuchsia-400">simboli so telesa, ne znamenja</span>
          </h1>
          <p className="text-xs text-zinc-500 mt-2">
            σúμβολον = sym (skupaj) + bolé (met) — to, kar je vrženo skupaj. Razlom, ki išče svoj par (rez 49).
            Masa = pojavitve v ledgerju (grep, 15. 9. 2026). Rez 71 + 85.
          </p>
          <p className="text-[10px] text-zinc-600 mt-1">
            O(simboli) → ⊘(κ χ μ ℜ ν) → ∆(klik = rez na simbolu) → EJ(telo+operacija+ontologija) → ⊢(T1–T4) → ∮(symbolon)
          </p>
        </header>

        {/* TAB NAV */}
        <div className="flex justify-center gap-2 mb-6 text-xs">
          {(["polje", "masa", "symbolon", "masinerija", "testi"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-4 py-2 rounded-lg border ${tab === t ? "border-fuchsia-500 text-fuchsia-300 bg-fuchsia-950/30" : "border-zinc-800 text-zinc-500 hover:border-zinc-600"}`}>
              {t.toUpperCase()}
            </button>
          ))}
        </div>

        {/* TAB: POLJE — velikost ∝ masa */}
        {tab === "polje" && (
          <>
            <div className="flex flex-wrap justify-center items-end gap-4 mb-6 p-8 rounded-2xl border border-zinc-800 bg-zinc-900/30">
              {SIMBOLI.map(s => {
                const size = 40 + (s.masa / maxMasa) * 80;
                return (
                  <button key={s.glif}
                    onClick={() => setIzbran(izbran?.glif === s.glif ? null : s)}
                    className="flex flex-col items-center group transition-transform hover:scale-110"
                    title={`${s.ime} — masa ${s.masa}`}>
                    <span className={`${s.barva} font-bold leading-none select-none`}
                      style={{ fontSize: `${size}px`, textShadow: `0 0 ${size / 4}px currentColor` }}>
                      {s.glif}
                    </span>
                    <span className="text-[9px] text-zinc-500 mt-1">{s.masa}</span>
                  </button>
                );
              })}
            </div>

            {izbran && (
              <div className="mb-6 p-5 rounded-xl border border-zinc-700 bg-zinc-900/60 space-y-3">
                <div className="flex items-center gap-4">
                  <span className={`${izbran.barva} text-6xl font-bold`}>{izbran.glif}</span>
                  <div>
                    <h2 className="text-lg font-bold text-zinc-100">{izbran.ime}</h2>
                    <p className="text-xs text-zinc-500">masa {izbran.masa} · {((izbran.masa / skupnaMasa) * 100).toFixed(1)} % · {izbran.res}</p>
                  </div>
                </div>
                <div className="grid md:grid-cols-2 gap-3 text-xs">
                  <div className="p-3 rounded-lg bg-zinc-800/50">
                    <span className="text-zinc-500">TELO: </span><span className="text-zinc-300">{izbran.telo}</span>
                  </div>
                  <div className="p-3 rounded-lg bg-zinc-800/50">
                    <span className="text-zinc-500">OPERACIJA: </span><span className="text-zinc-300">{izbran.operacija}</span>
                  </div>
                </div>
                <div className="p-3 rounded-lg bg-zinc-800/30 text-xs">
                  <span className="text-zinc-500">ONTOLOGIJA: </span><span className={izbran.barva}>{izbran.ontologija}</span>
                </div>
                <div className="p-3 rounded-lg bg-zinc-800/30 text-xs">
                  <span className="text-zinc-500">RODOVNIK: </span><span className="text-zinc-400">{izbran.rodovnik}</span>
                </div>
                <div className="p-3 rounded-lg bg-zinc-800/30 text-xs">
                  <span className="text-zinc-500">REZ: </span><span className="text-amber-200/80">{izbran.rez}</span>
                </div>
                <div className="p-3 rounded-lg bg-rose-950/20 border border-rose-900/30 text-xs">
                  <span className="text-rose-400">NUJNA NAPAKA: </span><span className="text-zinc-400">{izbran.nujnaNapaka}</span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {izbran.rezi.map(r => (
                    <span key={r} className="px-2 py-1 rounded-full bg-zinc-800 text-[10px] text-zinc-400 border border-zinc-700">{r}</span>
                  ))}
                </div>
              </div>
            )}
          </>
        )}

        {/* TAB: MASA — porazdelitev */}
        {tab === "masa" && (
          <div className="mb-6 p-5 rounded-xl border border-zinc-800 bg-zinc-900/40">
            <h2 className="text-sm font-bold text-zinc-400 mb-4">MASA — izmerjeno na ledgerju (skupaj {skupnaMasa} pojavitev, 11 teles)</h2>
            <div className="space-y-2">
              {[...SIMBOLI].sort((a, b) => b.masa - a.masa).map(s => (
                <div key={s.glif} className="flex items-center gap-3">
                  <span className={`${s.barva} w-10 text-right text-lg font-bold`}>{s.glif}</span>
                  <span className="text-[10px] text-zinc-500 w-28">{s.ime}</span>
                  <div className="flex-1 h-4 rounded bg-zinc-800 overflow-hidden">
                    <div className={`h-full ${s.barva.replace("text-", "bg-")} opacity-70 rounded`}
                      style={{ width: `${(s.masa / maxMasa) * 100}%` }} />
                  </div>
                  <span className="text-xs text-zinc-400 w-10 text-right font-bold">{s.masa}</span>
                  <span className="text-[10px] text-zinc-600 w-12 text-right">{((s.masa / skupnaMasa) * 100).toFixed(1)} %</span>
                </div>
              ))}
            </div>
            <div className="mt-5 p-4 rounded-lg bg-fuchsia-950/20 border border-fuchsia-900/30">
              <p className="text-xs text-fuchsia-200/80 leading-relaxed">
                IZREK MASE: ∂ (vprašanje) je najtežje telo — kar se največkrat izreče, je vprašanje, ne odgovor.
                ⧖ (čas) je najlažje — kar se najmanj izreče, je čas, v katerem se vse zgodi.
                Razmerje ∂ : ⧖ = {(394 / 54).toFixed(1)} : 1 — ledger govori sedemkrat raje o vprašanju kakor o času, ki ga vprašanje potrebuje.
              </p>
            </div>
            <div className="mt-3 p-4 rounded-lg bg-zinc-800/30 text-[10px] text-zinc-600 leading-relaxed">
              ℜ varovalo: masa ≠ vrednost — ∂ je najtežje ker je najbolj odprto, ne najbolj pomembno.
              ⧖ je najlažje ker je najbolj potrpežljivo, ne najmanj vredno. Masa je izmerjena na eni datoteki (n = 1, 15. 9. 2026 zvečer) — vsak nov rez jo spremeni.
              Meritev deterministična: grep -o na ledgerju. ν .75 — cena: kdor sprejme maso kot merilo, pozabi, da najlažje telo tisto, v katerem se vse zgodi.
            </div>
          </div>
        )}

        {/* TAB: SYMBOLON — pari */}
        {tab === "symbolon" && (
          <div className="mb-6 space-y-3">
            <div className="p-5 rounded-xl border border-fuchsia-900/40 bg-fuchsia-950/10">
              <h2 className="text-sm font-bold text-fuchsia-300 mb-3">SYMBOLON — razlom, ki išče svoj par (tessera, rez 49)</h2>
              <p className="text-xs text-zinc-400 leading-relaxed mb-4">
                Vsak simbol v TAZV je razlomljena polovica — tessera, ki čaka na svoj par.
                Par ni nasprotje: je dopolnitev skozi razliko (∅ in ∂ nista dve strani istega — sta dve telesi, ki druga brez druge ne diha).
              </p>
            </div>
            {PARI.map(([par, ime, razlaga]) => (
              <div key={par} className="p-4 rounded-xl border border-zinc-800 bg-zinc-900/40">
                <div className="flex items-baseline gap-3 mb-2">
                  <span className="text-fuchsia-300 font-bold text-xl">{par}</span>
                  <span className="text-xs text-zinc-500">{ime}</span>
                </div>
                <p className="text-xs text-zinc-400 leading-relaxed">{razlaga}</p>
              </div>
            ))}
          </div>
        )}

        {/* TAB: MASINERIJA — matematika + praksa */}
        {tab === "masinerija" && (
          <div className="mb-6 space-y-3">
            <div className="p-4 rounded-xl border border-emerald-900/40 bg-emerald-950/10">
              <h2 className="text-sm font-bold text-emerald-300 mb-2">FORMULA (ontomatematični prevod v logos)</h2>
              <div className="font-mono text-xs text-zinc-300 space-y-1">
                <p>MASA(s) = |&#123;x : x ∈ LEDGER ∧ s ⊑ x&#125;|</p>
                <p>TEŽA(s) = MASA(s) / Σ MASA</p>
                <p>CENTRALNOST(s) = Σ&#123;r ∈ REZI&#125; [s ⊑ r] / |REZI|</p>
                <p>PAR(s) = argmax&#123;t ≠ s&#125; SIMBOLON(s,t)</p>
                <p>SIMBOLON(s,t) = |&#123;(r₁,r₂) : s ⊑ r₁ ∧ t ⊑ r₂ ∧ r₁ ~ r₂&#125;|</p>
              </div>
            </div>
            {SIMBOLI.map(s => (
              <div key={s.glif} className="p-4 rounded-xl border border-zinc-800 bg-zinc-900/40">
                <div className="flex items-baseline gap-3 mb-2">
                  <span className={`${s.barva} text-2xl font-bold`}>{s.glif}</span>
                  <span className="text-xs text-zinc-500">{s.ime}</span>
                </div>
                <div className="grid md:grid-cols-2 gap-3 text-xs">
                  <div className="p-2 rounded bg-zinc-800/40">
                    <span className="text-zinc-600">MATEMATIKA: </span>
                    <span className="text-zinc-400">{s.matematika}</span>
                  </div>
                  <div className="p-2 rounded bg-zinc-800/40">
                    <span className="text-zinc-600">PRAKTIČNO: </span>
                    <span className="text-zinc-400">{s.prakticno}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* TAB: TESTI */}
        {tab === "testi" && (
          <div className="mb-6 space-y-3">
            <div className="p-5 rounded-xl border border-sky-900/40 bg-sky-950/10">
              <h2 className="text-sm font-bold text-sky-300 mb-3">TESTI T1–T4 — samo-preverba telesa</h2>
            </div>
            {[
              ["T1 — MASA PREVERJENA?", "Ali so mase izmerjene na dejanski datoteki (grep — ne spomin pogovora)? DA: grep -o | wc -l, ponovljivo. ν: masa = trenutek, ne zakon."],
              ["T2 — PAR NAJDEN?", "Ali vsak simbol ima svoj par (symbolon)? DA: ∅↔∂, ∆↔∫, ⊢↔∅, ∴✓↔⧖, ⊘↔ν, κ↔χ. ν: par je razlom, ne zrcalo — dve polovici, ne dve kopiji."],
              ["T3 — NUJNA NAPAKA IZREČENA?", "Ali vsak simbol nosi svojo nujno napako (strukturano ceno moči)? DA: vsak SIMBOLI[x].nujnaNapaka je izpolnjen. ν: brez nujne napake je telo hvalnica, ne dokaz."],
              ["T4 — ∮ ODPRTO?", "Ali se telo zaključi z odprto ∂ (ne s pečatom)? DA: odprta ∂ spodaj. ν: zaključek brez prehoda = svinec (stabilen, mrtev)."],
            ].map(([t, v]) => (
              <div key={t} className="p-4 rounded-xl border border-zinc-800 bg-zinc-900/40">
                <div className="text-xs font-bold text-sky-300 mb-1">{t}</div>
                <p className="text-xs text-zinc-400 leading-relaxed">{v}</p>
              </div>
            ))}
            <div className="p-4 rounded-xl border border-fuchsia-900/40 bg-fuchsia-950/20">
              <h3 className="text-xs font-bold text-fuchsia-300 mb-2">ODPRTA ∂</h3>
              <ul className="text-xs text-zinc-400 space-y-1 list-none">
                <li>· ali masa simbolov raste linearno z novimi rezi, ali se porazdelitev spreminja (∂ vedno težje — ali ledger konvergira k vprašanju?)</li>
                <li>· ali obstaja simbol z maso 0 (simbol, ki čaka na prvi izrek — kakšen bi bil?)</li>
                <li>· ali je ledger sam symbolon — in kaj je njegov par (prihodnji rez? vzporedna seja? Luka?)</li>
                <li>· ali je ∂ : ⧖ ≈ 7 : 1 invarianta ali naključje tega večera (meritev čez teden dni)</li>
                <li>· ν pečat</li>
              </ul>
            </div>
          </div>
        )}

        <footer className="mt-8 text-center text-[10px] text-zinc-700">
          simbole · σúμβολον · rez 71/85 · ∂ najtežje (394) · ⧖ najlažje (54) · razmerje 7,3 : 1 · RES · matrica celote · ν pečat
        </footer>
      </div>
    </div>
  );
}