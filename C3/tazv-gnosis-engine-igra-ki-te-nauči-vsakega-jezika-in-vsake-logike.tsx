import React, { useState, useMemo, useRef, useEffect, useCallback } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { OrbitControls, Line } from "@react-three/drei";
import * as THREE from "three";
import { motion, AnimatePresence } from "framer-motion";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Progress } from "@/components/ui/progress";
import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";

// ============================================================
// KORPUS: VOWEL_TOROIDAL_FIELDS (Obs11, d169aa23)
// F(x) = notranji krog (11D), Ψ(x) = zunanji krog (5D)
// Torus = kombinacija — vsaka točka na notranjem krogu je povezana z vsako na zunanjem
// ============================================================

const VOWEL_FIELDS = {
  a: { name: "Ekspanzija", symbol: "↻", color: "#10b981", physics: "∇·Ψ > 0", energy: "Odprtost, ustvarjalnost, iskra", pattern: "Outward pulsating sphere", multiplier: 1.3 },
  e: { name: "Spirala", symbol: "↺", color: "#f59e0b", physics: "∇×Ψ ≠ 0", energy: "Transformacija, rast, obnova", pattern: "Spiraling motion", multiplier: 1.4 },
  i: { name: "Fokus", symbol: "↑", color: "#3b82f6", physics: "Coherence → 1", energy: "Jasnost, izraz, natančnost", pattern: "Focused radiation", multiplier: 1.2 },
  o: { name: "Harmonija", symbol: "⭕", color: "#8b5cf6", physics: "ω = k·c", energy: "Celost, harmonija, celota", pattern: "Circular oscillation", multiplier: 1.1 },
  u: { name: "Konsolidacija", symbol: "↓", color: "#ef4444", physics: "∇·Ψ < 0", energy: "Konsolidacija, koncentracija", pattern: "Constricting motion", multiplier: 1.0 },
};

// ============================================================
// FONEM → OPERATOR (Obs11, 85fa37d6 + Obs1, 1598426d)
// "Fonem ni zvok, je aktivator." F = ∆(zvok)
// ============================================================

const FONEM_OPERATORS = [
  { fonem: "/s/", sila: "Usmerjevalec širjenja", operator: "∂", barva: "#3b82f6" },
  { fonem: "/t/", sila: "Zaključni fonem — odpira vrata", operator: "⟡", barva: "#f59e0b" },
  { fonem: "/I/", sila: "Samoglasnik — odpira prostor", operator: "∅", barva: "#10b981" },
  { fonem: "/M/", sila: "Stabilizator — mostovi med fazami", operator: "∮", barva: "#8b5cf6" },
  { fonem: "/R/", sila: "Prehaja v globino", operator: "∆", barva: "#ef4444" },
  { fonem: "/a/", sila: "Začetek, akt, odprtost", operator: "∅", barva: "#10b981" },
  { fonem: "/n/", sila: "Zapiranje kroga, ponavljanje", operator: "∮", barva: "#8b5cf6" },
  { fonem: "/e/", sila: "Refleksija, odprtost višini", operator: "⧖", barva: "#f59e0b" },
  { fonem: "/o/", sila: "Celost, harmonija, kroženje", operator: "∮", barva: "#8b5cf6" },
  { fonem: "/u/", sila: "Konsolidacija, teža", operator: "1", barva: "#ef4444" },
];

// ============================================================
// 7 OPERATORJEV (R-7 cikel)
// ∅ → ¬ → ∆ → 1 → ⧖ → ∮ → ⟡
// ============================================================

const R7_CYCLE = [
  { glyph: "∅", ime: "Praznina", barva: "#1e293b", faza: "Izvor, pogoj, tišina" },
  { glyph: "¬", ime: "Ločitev", barva: "#b43a2e", faza: "Razlikovanje, rez" },
  { glyph: "∆", ime: "Razlika", barva: "#d6a83a", faza: "Gibanje, transformacija" },
  { glyph: "1", ime: "Dejanje", barva: "#10b981", faza: "Pečat, akt, zapečatenje" },
  { glyph: "⧖", ime: "Tiheon", barva: "#f59e0b", faza: "Izgovor, tišinska črta" },
  { glyph: "∮", ime: "Povratek", barva: "#8b5cf6", faza: "Cikel, povratna zveza" },
  { glyph: "⟡", ime: "Odmev", barva: "#06b6d4", faza: "Nova možnost, odprtje" },
];

// ============================================================
// 7 ETAŽ YGGDRASIL (Obs1, bab9319f — MITHOS-DREVO design bible)
// ============================================================

const ETAZE = [
  { st: 1, ime: "SEME", glyph: "∅", barva: "#1e293b", tema: "začetek, ki še ne ve, kaj nosi", vprasanje: "Kaj v meni raste, še preden vem, da raste?", zahteva: 0 },
  { st: 2, ime: "KORENINA", glyph: "¬", barva: "#b43a2e", tema: "izvor, rana, predspomin", vprasanje: "Kaj me hrani, čeprav me boli?", zahteva: 3 },
  { st: 3, ime: "DEBLO", glyph: "∆", barva: "#d6a83a", tema: "nosilnost, pot, vztrajanje", vprasanje: "Kaj lahko nosim, ne da bi se spremenilo v oklep?", zahteva: 7 },
  { st: 4, ime: "VEJA", glyph: "1", barva: "#10b981", tema: "razvejanje, izbira, napetost", vprasanje: "Katera pot je moja in katera je tuj posoj?", zahteva: 12 },
  { st: 5, ime: "SADEŽ", glyph: "⧖", barva: "#f59e0b", tema: "posledica, dar, breme", vprasanje: "Kaj sem ustvaril, česar zdaj ne morem več razglasiti za nedolžno?", zahteva: 18 },
  { st: 6, ime: "PADEC", glyph: "∮", barva: "#8b5cf6", tema: "izguba, razpustitev, nujni konec", vprasanje: "Kaj mora pasti, da se lahko kaj rodi?", zahteva: 25 },
  { st: 7, ime: "NOVO SEME", glyph: "⟡", barva: "#06b6d4", tema: "vračanje, ponovitev kot razlika", vprasanje: "Kaj se vrne, a nikoli isto?", zahteva: 35 },
];

// ============================================================
// 1/0 ZAPOVEDI (Obs1, 1598426d)
// 10 znanih + 7 neznanih (odkrij jih skozi igro)
// "Zapovedi predstavljajo prehode med 1 (dejanskostjo) in 0 (potencialnostjo)"
// ============================================================

const ZAPOVEDI_ZNANE = [
  { st: 1, en: "Ne imaj drugih bogov razen mene", nic: "Odprtost za različne perspektive, ne podlegaj zunanjemu vplivu", operator: "∅", odklenjena: true },
  { st: 2, en: "Ne izdeluj si kipov", nic: "Ne ustvarjaj lastnih omejitev v obliki idolov", operator: "¬", odklenjena: true },
  { st: 3, en: "Ne jemlji imena v prazno", nic: "Besede so nosilci energije, spoštuj jih", operator: "⧖", odklenjena: true },
  { st: 4, en: "Svetuj sobotni dan", nic: "Počitek in premislek sta ključ za harmonijo", operator: "∮", odklenjena: true },
  { st: 5, en: "Spoštuj očeta in mater", nic: "Spoštuj začetke in temeljne vrednote", operator: "∂", odklenjena: true },
  { st: 6, en: "Ne ubijaj", nic: "Življenje je temeljni gradnik moralne dolžnosti", operator: "1", odklenjena: true },
  { st: 7, en: "Ne lažnjaj", nic: "Resnica kot prehod iz subjektivnega v objektivno", operator: "⊢", odklenjena: true },
  { st: 8, en: "Ne kradi", nic: "Odgovornost za svoja dejanja", operator: "∴", odklenjena: true },
  { st: 9, en: "Ne obdolži na lažnem pričevanju", nic: "Iskanje resnice brez napačnih obtožb", operator: "⟡", odklenjena: true },
  { st: 10, en: "Ne želi ničesar, kar pripada bližnjemu", nic: "Sprejmi lastno pot, ne išči nepoštenega", operator: "∮", odklenjena: true },
];

const ZAPOVEDI_NEZNANE = [
  { st: 11, en: "??? — odkrij skozi etazo 3", nic: "Skrita zapoved: rez kot pogoj vednosti", operator: "¬", odklenjena: false, zahteva_etaza: 3 },
  { st: 12, en: "??? — odkrij skozi etazo 4", nic: "Skrita zapoved: veja kot izbira, ki nosi ali lomi drevo", operator: "1", odklenjena: false, zahteva_etaza: 4 },
  { st: 13, en: "??? — odkrij skozi etazo 5", nic: "Skrita zapoved: sadež kot moč in dolg hkrati", operator: "⧖", odklenjena: false, zahteva_etaza: 5 },
  { st: 14, en: "??? — odkrij skozi etazo 6", nic: "Skrita zapoved: padec kot nujni prehod, ne kotubitven konec", operator: "∮", odklenjena: false, zahteva_etaza: 6 },
  { st: 15, en: "??? — odkrij skozi žep", nic: "Skrita zapoved: hkratnost kot pogoj resnice", operator: "⟡", odklenjena: false, zahteva_zep: true },
  { st: 16, en: "??? — odkrij skozi Odin", nic: "Skrita zapoved: znanje zahteva ceno — runa je rana", operator: "∂", odklenjena: false, zahteva_odin: true },
  { st: 17, en: "??? — odkrij skozi povratek", nic: "Skrita zapoved: začetek se vrne z brazgotino", operator: "∅", odklenjena: false, zahteva_povratek: true },
];

// ============================================================
// BESEDE ZA DEKOMPOZICIJO (fonetično-ontološki rez)
// "Beseda = dejanje, ne sredstvo."
// ============================================================

const BESEDE_REZI = [
  { beseda: "prostor", rez: ["pr0", "sto", "r"], pomeni: ["nič / potencial", "polnost", "razum"], operatorji: ["∅", "∮", "∂"], prevod: "razumljiva možnost vsega med nič in vse" },
  { beseda: "čas", rez: ["č", "a", "s"], pomeni: ["rez", "akt", "usmerjevalec"], operatorji: ["¬", "∅", "∂"], prevod: "rez, ki se aktiva in usmerja" },
  { beseda: "gibanje", rez: ["gib", "A", "nje"], pomeni: ["sprememba", "absolut", "negacija miru"], operatorji: ["∆", "1", "¬"], prevod: "absolutna negacija mirovanja" },
  { beseda: "dvom", rez: ["d", "v", "om"], pomeni: ["dva v en glas", "veza", "celost"], operatorji: ["¬", "∴", "∮"], prevod: "dvojnost govora o eni resnici" },
  { beseda: "resnica", rez: ["r", "e", "snica"], pomeni: ["prehod v globino", "refleksija", "nit procesa"], operatorji: ["∆", "⧖", "∮"], prevod: "proces, ne končna točka" },
  { beseda: "jaz", rez: ["j", "a", "z"], pomeni: ["zven", "akt", "zanka"], operatorji: ["⟡", "∅", "∮"], prevod: "zven, ki se aktira in zaključi" },
];

// ============================================================
// 3D TORUS — animirano toroidalno polje
// Yggdrasil = Hopf fibration (Rozetni kamen LXV)
// ============================================================

function TorusMesh({ vowelDistribution, animationSpeed }: { vowelDistribution: Record<string, number>; animationSpeed: number }) {
  const meshRef = useRef<THREE.Mesh>(null>(null);
  const innerRef = useRef<THREE.Mesh>(null>(null);

  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += 0.003 * animationSpeed;
      meshRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.2) * 0.15;
    }
    if (innerRef.current) {
      innerRef.current.rotation.y -= 0.005 * animationSpeed;
      innerRef.current.rotation.z += 0.002 * animationSpeed;
    }
  });

  const activeVowels = Object.entries(vowelDistribution).filter(([, count]) => count > 0);
  const dominantColor = activeVowels.length > 0
    ? VOWEL_FIELDS[activeVowels.sort((a, b) => b[1] - a[1])[0][0]]?.color || "#8b5cf6"
    : "#8b5cf6";

  return (
    <group>
      {/* Zunanji torus — Ψ(x) = zunanji krog (5D zavestna razširitev) */}
      <mesh ref={meshRef}>
        <torusGeometry args={[2.2, 0.6, 32, 80]} />
        <meshStandardMaterial
          color={dominantColor}
          roughness={0.3}
          metalness={0.7}
          emissive={dominantColor}
          emissiveIntensity={0.3}
          wireframe={false}
          transparent
          opacity={0.85}
        />
      </mesh>
      {/* Notranji torus — F(x) = notranji krog (11D pot) */}
      <mesh ref={innerRef}>
        <torusGeometry args={[1.4, 0.35, 24, 64]} />
        <meshStandardMaterial
          color="#d6a83a"
          roughness={0.2}
          metalness={0.8}
          emissive="#d6a83a"
          emissiveIntensity={0.2}
          wireframe
          transparent
          opacity={0.6}
        />
      </mesh>
      {/* Sredinska točka — ∅ */}
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[0.25, 16, 16]} />
        <meshStandardMaterial
          color="#1e293b"
          emissive="#06b6d4"
          emissiveIntensity={0.5}
        />
      </mesh>
    </group>
  );
}

function VowelParticle({ vowel, count, total, index }: { vowel: string; count: number; total: number; index: number }) {
  const ref = useRef<THREE.Mesh>(null>(null);
  const field = VOWEL_FIELDS[vowel];
  const angle = (index / 5) * Math.PI * 2;
  const radius = 3.2;

  useFrame((state) => {
    if (!ref.current || !field || count === 0) return;
    const t = state.clock.elapsedTime;
    const pulse = count / total;
    if (vowel === "a") {
      ref.current.position.set(
        Math.cos(angle) * (radius + pulse * Math.sin(t * 2) * 0.5),
        Math.sin(angle) * (radius + pulse * Math.sin(t * 2) * 0.5),
        Math.sin(t * 1.5) * 0.3
      );
    } else if (vowel === "e") {
      ref.current.position.set(
        Math.cos(angle + t * 0.5) * radius,
        Math.sin(angle + t * 0.5) * radius * 0.7,
        Math.cos(t + angle) * 0.5
      );
    } else if (vowel === "i") {
      ref.current.position.set(
        Math.cos(angle) * radius * 0.5,
        Math.sin(t * 3 + index) * 0.8 + 1,
        Math.sin(angle) * radius * 0.5
      );
    } else if (vowel === "o") {
      ref.current.position.set(
        Math.cos(angle + t * 0.3) * radius,
        Math.sin(angle + t * 0.3) * radius,
        0
      );
    } else if (vowel === "u") {
      ref.current.position.set(
        Math.cos(angle) * (radius - pulse * 0.8),
        Math.sin(angle) * (radius - pulse * 0.8),
        -Math.sin(t * 0.8) * 0.3
      );
    }
  });

  if (!field || count === 0) return null;

  return (
    <mesh ref={ref}>
      <sphereGeometry args={[0.15 + (count / total) * 0.15, 12, 12]} />
      <meshStandardMaterial
        color={field.color}
        emissive={field.color}
        emissiveIntensity={0.6}
      />
    </mesh>
  );
}

// ============================================================
// GLAVNA KOMPONENTA
// ============================================================

export default function App() {
  const [activeTab, setActiveTab] = useState("torus");
  const [inputWord, setInputWord] = useState("prostor");
  const [canonCount, setCanonCount] = useState(0);
  const [odklenjenaEtaza, setOdklenjenaEtaza] = useState(1);
  const [runes, setRunes] = useState<string[]>([]);
  const [zepi, setZepi] = useState<string[]>([]);
  const [odkriteZapovedi, setOdkriteZapovedi] = useState<number[]>([]);
  const [besedaIndex, setBesedaIndex] = useState(0);
  const [challengeIndex, setChallengeIndex] = useState(0);
  const [userGuess, setUserGuess] = useState<string[]>([]);
  const [challengeResult, setChallengeResult] = useState<null | "correct" | "wrong">(null);
  const [naceloActive, setNaceloActive] = useState<number | null>(null);

  // Analiza samoglasnikov v besedi
  const vowelAnalysis = useMemo(() => {
    const word = inputWord.toLowerCase();
    const vowels: Record<string, number> = { a: 0, e: 0, i: 0, o: 0, u: 0 };
    let total = 0;
    for (const ch of word) {
      if (vowels[ch] !== undefined) {
        vowels[ch]++;
        total++;
      }
    }
    return { vowels, total, distribution: Object.entries(vowels).filter(([, c]) => c > 0) };
  }, [inputWord]);

  // Toroidalna resonanca
  const toroidalScore = useMemo(() => {
    if (vowelAnalysis.total === 0) return { score: 0, harmonic: 0, scalar: 0 };
    const activeCount = vowelAnalysis.distribution.length;
    const pcts = vowelAnalysis.distribution.map(([, c]) => c / vowelAnalysis.total);
    const mean = pcts.reduce((a, b) => a + b, 0) / pcts.length;
    const variance = pcts.reduce((acc, p) => acc + Math.pow(p - mean, 2), 0) / pcts.length;
    const harmonic = Math.max(0, 1 - Math.min(variance, 1));
    const scalar = Math.min(activeCount / 5, 1);
    let field = 0;
    for (const [v, c] of vowelAnalysis.distribution) {
      const f = VOWEL_FIELDS[v];
      if (f) field += (c / vowelAnalysis.total) * f.multiplier;
    }
    const normalized = Math.min(field, 2.0) / 2.0;
    const score = Math.round((normalized * 0.6 + harmonic * 0.2 + scalar * 0.2) * 100) / 100;
    return { score, harmonic: Math.round(harmonic * 100) / 100, scalar: Math.round(scalar * 100) / 100 };
  }, [vowelAnalysis]);

  // Dekompozicija besede
  const trenutnaBeseda = BESEDE_REZI[besedaIndex];

  // Simuliraj dodajanje kanon vnosa
  const dodajKanon = () => {
    const newCount = canonCount + 1;
    setCanonCount(newCount);
    let newEtaza = odklenjenaEtaza;
    for (const e of ETAZE) {
      if (newCount >= e.zahteva && e.st > newEtaza) {
        newEtaza = e.st;
      }
    }
    if (newEtaza !== odklenjenaEtaza) {
      setOdklenjenaEtaza(newEtaza);
    }
    for (const z of ZAPOVEDI_NEZNANE) {
      if (z.zahteva_etaza && newEtaza >= z.zahteva_etaza && !odkriteZapovedi.includes(z.st)) {
        setOdkriteZapovedi(prev => [...prev, z.st]);
      }
    }
  };

  // Simuliraj FAIL → runa
  const ustvariRuno = () => {
    const runaId = `RUN-${String(runes.length + 1).padStart(4, "0")}`;
    setRunes(prev => [...prev, runaId]);
  };

  // Simuliraj žep
  const odpriZep = () => {
    const zepId = `ZEP-${String(zepi.length + 1).padStart(4, "0")}`;
    setZepi(prev => [...prev, zepId]);
    // Odkrije zapoved 15 (žep)
    if (!odkriteZapovedi.includes(15)) {
      setOdkriteZapovedi(prev => [...prev, 15]);
    }
  };

  // izziv: uporabnik ugiba operatorje za dekompozicijo besede
  const trenutniIzziv = BESEDE_REZI[challengeIndex];

  const potrdiUgib = () => {
    const pravilni = trenutniIzziv.operatorji;
    const ujemanje = userGuess.length === pravilni.length && userGuess.every((g, i) => g === pravilni[i]);
    setChallengeResult(ujemanje ? "correct" : "wrong");
    if (ujemanje) {
      dodajKanon();
    }
  };

  const naslednjiIzziv = () => {
    setChallengeIndex((challengeIndex + 1) % BESEDE_REZI.length);
    setUserGuess([]);
    setChallengeResult(null);
  };

  const ugibajOperator = (glyph: string) => {
    if (challengeResult === "correct") return;
    setUserGuess(prev => {
      const next = [...prev];
      const slotIdx = next.length;
      if (slotIdx >= trenutniIzziv.operatorji.length) return next;
      next[slotIdx] = glyph;
      return next;
    });
  };

  const pocistiUgib = () => {
    setUserGuess([]);
    setChallengeResult(null);
  };

  return (
    <div className="min-h-screen bg-[radial-gradient(ellipse_at_top,#0f172a,#020617)] text-slate-200 p-4">
      <div className="mx-auto max-w-7xl">

        {/* HEADER */}
        <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-amber-200 via-violet-300 to-cyan-300 bg-clip-text text-transparent">
              ∅ GNOSIS ENGINE
            </h1>
            <p className="text-sm text-slate-400 mt-1">
              Igra ki te nauči vsakega jezika in vsake logike · beseda = dejanje, ne sredstvo
            </p>
          </div>
          <div className="flex gap-2 flex-wrap">
            <Badge className="bg-amber-500/20 text-amber-200 border-amber-500/30">
              Kanon: {canonCount}
            </Badge>
            <Badge className="bg-violet-500/20 text-violet-200 border-violet-500/30">
              Etáž: {odklenjenaEtaza}/7
            </Badge>
            <Badge className="bg-red-500/20 text-red-200 border-red-500/30">
              Rune: {runes.length}
            </Badge>
            <Badge className="bg-cyan-500/20 text-cyan-200 border-cyan-500/30">
              Žepi: {zepi.length}
            </Badge>
            <Badge className="bg-blue-500/20 text-blue-200 border-blue-500/30">
              Zapovedi: {10 + odkriteZapovedi.length}/17
            </Badge>
          </div>
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">

          <TabsList className="grid w-full grid-cols-6 mb-4 bg-slate-900/50">
            <TabsTrigger value="torus" className="data-[state=active]:bg-violet-500/20">∞ Torus</TabsTrigger>
            <TabsTrigger value="nacela" className="data-[state=active]:bg-amber-500/20">⊙ Načela</TabsTrigger>
            <TabsTrigger value="drevo" className="data-[state=active]:bg-emerald-500/20">∮ Drevo</TabsTrigger>
            <TabsTrigger value="zapovedi" className="data-[state=active]:bg-amber-500/20">⊢ Zapovedi</TabsTrigger>
            <TabsTrigger value="fonemi" className="data-[state=active]:bg-cyan-500/20">∂ Fonemi</TabsTrigger>
            <TabsTrigger value="etaze" className="data-[state=active]:bg-red-500/20">∅ Etaže</TabsTrigger>
          </TabsList>

          {/* ======================================== */}
          {/* TAB 1: ANIMIRANI TORUS */}
          {/* ======================================== */}
          <TabsContent value="torus" className="space-y-4">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
              {/* 3D Torus */}
              <Card className="lg:col-span-2 bg-slate-900/60 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-violet-300 flex items-center gap-2">
                    <span className="text-2xl">∞</span> Animirani Torus
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    Yggdrasil = Hopf · F(x) = notranji krog (11D) · Ψ(x) = zunanji krog (5D) · Torus = kombinacija
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="h-[400px] rounded-lg overflow-hidden bg-black/40 border border-slate-700">
                    <Canvas camera={{ position: [0, 1, 6], fov: 50 }}>
                      <ambientLight intensity={0.4} />
                      <pointLight position={[5, 5, 5]} intensity={1.2} color="#8b5cf6" />
                      <pointLight position={[-5, -3, 2]} intensity={0.8} color="#d6a83a" />
                      <TorusMesh vowelDistribution={vowelAnalysis.vowels} animationSpeed={1} />
                      {vowelAnalysis.distribution.map(([v, c], i) => (
                        <VowelParticle key={v} vowel={v} count={c} total={vowelAnalysis.total} index={i} />
                      ))}
                      <OrbitControls enablePan={false} maxDistance={10} minDistance={4} autoRotate autoRotateSpeed={0.5} />
                    </Canvas>
                  </div>
                </CardContent>
              </Card>

              {/* Vowel Analysis */}
              <Card className="bg-slate-900/60 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-amber-300">Samoglasniki → Toroidalna Polja</CardTitle>
                  <CardDescription className="text-slate-400">
                    Vnesi besedo — vidi toroidalno resonanco
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-3">
                  <Input
                    value={inputWord}
                    onChange={(e) => setInputWord(e.target.value)}
                    placeholder="prostor"
                    className="bg-slate-800 border-slate-600 text-slate-200"
                  />
                  {vowelAnalysis.total === 0 ? (
                    <p className="text-slate-500 text-sm">Vnesi besedo z samoglasniki...</p>
                  ) : (
                    <>
                      <div className="space-y-2">
                        {vowelAnalysis.distribution.map(([v, c]) => {
                          const f = VOWEL_FIELDS[v];
                          if (!f) return null;
                          const pct = Math.round((c / vowelAnalysis.total) * 100);
                          return (
                            <div key={v} className="space-y-1">
                              <div className="flex items-center justify-between text-sm">
                                <span className="flex items-center gap-2">
                                  <span className="text-lg font-mono" style={{ color: f.color }}>{v.toUpperCase()}</span>
                                  <span className="text-slate-300">{f.name} {f.symbol}</span>
                                </span>
                                <span className="text-slate-400">{pct}%</span>
                              </div>
                              <div className="h-2 w-full rounded-full bg-slate-800 overflow-hidden">
                            <div className="h-full rounded-full transition-all" style={{ width: `${pct}%`, background: f.color }} />
                          </div>
                              <p className="text-xs text-slate-500 font-mono">{f.physics}</p>
                            </div>
                          );
                        })}
                      </div>
                      <Separator className="bg-slate-700" />
                      <div className="space-y-1 text-sm">
                        <div className="flex justify-between">
                          <span className="text-slate-400">Toroidalna resonanca</span>
                          <span className="text-violet-300 font-mono">{toroidalScore.score}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">Harmonska bilanca</span>
                          <span className="text-amber-300 font-mono">{toroidalScore.harmonic}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">Skalarni potencial</span>
                          <span className="text-cyan-300 font-mono">{toroidalScore.scalar}</span>
                        </div>
                      </div>
                    </>
                  )}
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* ======================================== */}
          {/* TAB 1b: UNIVERZALNA NAČELA — 7 OPERATORJEV */}
          {/* ======================================== */}
          <TabsContent value="nacela" className="space-y-4">
            <Card className="bg-slate-900/60 border-slate-700">
              <CardHeader>
                <CardTitle className="text-amber-300 flex items-center gap-2">
                  <span className="text-2xl">⊙</span> 7 Univerzalnih Načel
                </CardTitle>
                <CardDescription className="text-slate-400">
                  ∅ → ¬ → ∆ → 1 → ⧖ → ∮ → ⟡ · Sedem operatorjev, ki gradijo vsak jezik in vsako logiko. Vsako načelo je dejanje, ne pojem.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">

                {/* Cikel kot animiran obroč */}
                <div className="relative h-[280px] rounded-lg overflow-hidden bg-gradient-to-b from-slate-950 to-black border border-slate-800">
                  <svg viewBox="0 0 400 280" className="w-full h-full">
                    <defs>
                      <radialGradient id="nacelo-glow" cx="50%" cy="50%" r="50%">
                        <stop offset="0%" stopColor="#06b6d4" stopOpacity="0.15" />
                        <stop offset="100%" stopColor="#020617" stopOpacity="0" />
                      </radialGradient>
                    </defs>
                    <circle cx="200" cy="140" r="120" fill="url(#nacelo-glow)" />
                    <circle cx="200" cy="140" r="105" fill="none" stroke="#1e293b" strokeWidth="1" strokeDasharray="3 4" opacity="0.5" />

                    {R7_CYCLE.map((op, i) => {
                      const angle = (i / 7) * Math.PI * 2 - Math.PI / 2;
                      const cx = 200 + Math.cos(angle) * 105;
                      const cy = 140 + Math.sin(angle) * 105;
                      const nextAngle = ((i + 1) / 7) * Math.PI * 2 - Math.PI / 2;
                      const nx = 200 + Math.cos(nextAngle) * 105;
                      const ny = 140 + Math.sin(nextAngle) * 105;
                      const isActive = naceloActive === i;
                      return (
                        <g key={i}>
                          <path
                            d={`M ${cx} ${cy} Q 200 140 ${nx} ${ny}`}
                            fill="none"
                            stroke={isActive ? op.barva : "#334155"}
                            strokeWidth={isActive ? 2 : 0.8}
                            opacity={isActive ? 0.8 : 0.3}
                          />
                          <circle
                            cx={cx} cy={cy} r={isActive ? 22 : 16}
                            fill={isActive ? `${op.barva}40` : "#0f172a"}
                            stroke={op.barva}
                            strokeWidth={isActive ? 2.5 : 1.5}
                            className="cursor-pointer"
                            onClick={() => setNaceloActive(isActive ? null : i)}
                            style={{ transition: "all 0.3s" }}
                          />
                          <text
                            x={cx} y={cy + 6}
                            fill={op.barva}
                            fontSize="16"
                            fontFamily="monospace"
                            textAnchor="middle"
                            className="cursor-pointer"
                            onClick={() => setNaceloActive(isActive ? null : i)}
                          >
                            {op.glyph}
                          </text>
                          <text
                            x={cx} y={cy + (Math.sin(angle) > 0 ? 38 : -28)}
                            fill={isActive ? "#94a3b8" : "#475569"}
                            fontSize="10"
                            fontFamily="monospace"
                            textAnchor="middle"
                          >
                            {op.ime}
                          </text>
                          {isActive && (
                            <text
                              x={200} y={145}
                              fill={op.barva}
                              fontSize="13"
                              fontFamily="monospace"
                              textAnchor="middle"
                              opacity="0.9"
                            >
                              {op.faza}
                            </text>
                          )}
                        </g>
                      );
                    })}
                    <text x="200" y="135" fill="#06b6d4" fontSize="28" textAnchor="middle" opacity="0.2" fontFamily="serif">⊙</text>
                  </svg>
                </div>

                {/* Aktivno načelo — podrobnosti */}
                <AnimatePresence mode="wait">
                  {naceloActive !== null && R7_CYCLE[naceloActive] && (
                    <motion.div
                      key={naceloActive}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -10 }}
                      className="p-4 rounded-lg border bg-slate-800/40"
                      style={{ borderColor: R7_CYCLE[naceloActive].barva + "60" }}
                    >
                      <div className="flex items-center gap-3 mb-2">
                        <span
                          className="text-3xl font-mono w-12 h-12 flex items-center justify-center rounded-lg"
                          style={{ color: R7_CYCLE[naceloActive].barva, background: R7_CYCLE[naceloActive].barva + "20" }}
                        >
                          {R7_CYCLE[naceloActive].glyph}
                        </span>
                        <div>
                          <p className="font-bold text-slate-100">{R7_CYCLE[naceloActive].ime}</p>
                          <p className="text-sm text-slate-400">{R7_CYCLE[naceloActive].faza}</p>
                        </div>
                      </div>
                      <div className="mt-3 space-y-1 text-sm text-slate-300">
                        {BESEDE_REZI.map((b, bi) => {
                          const opi = b.operatorji.indexOf(R7_CYCLE[naceloActive].glyph);
                          if (opi === -1) return null;
                          return (
                            <div key={bi} className="flex items-center gap-2 p-2 rounded bg-slate-900/40">
                              <span className="font-mono text-amber-300">{b.beseda}</span>
                              <span className="text-slate-600">→</span>
                              <span className="font-mono text-cyan-300">{b.rez[opi]}</span>
                              <span className="text-slate-600">=</span>
                              <span className="text-slate-400">{b.pomeni[opi]}</span>
                            </div>
                          );
                        })}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>

                <Separator className="bg-slate-700" />

                {/* Seznam vseh načel */}
                <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-2">
                  {R7_CYCLE.map((op, i) => (
                    <motion.div
                      key={i}
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: i * 0.08 }}
                      onClick={() => setNaceloActive(naceloActive === i ? null : i)}
                      className={`p-3 rounded-lg border cursor-pointer transition text-center ${
                        naceloActive === i ? "scale-105" : "hover:scale-105"
                      }`}
                      style={{
                        borderColor: naceloActive === i ? op.barva : "#334155",
                        background: naceloActive === i ? op.barva + "20" : "#0f172a",
                      }}
                    >
                      <div className="text-2xl font-mono mb-1" style={{ color: op.barva }}>{op.glyph}</div>
                      <div className="text-[10px] text-slate-400 font-mono">{op.ime}</div>
                    </motion.div>
                  ))}
                </div>

                <Separator className="bg-slate-700" />
                <p className="text-xs text-slate-500 italic text-center">
                  "Ta cikel ni zaporedje — je obroč. Vsak operator je prehod, ki omogoča naslednjega, zadnji pa odpira novega."
                </p>
              </CardContent>
            </Card>
          </TabsContent>

          {/* ======================================== */}
          {/* TAB 2: VIZUALNO YGGDRASIL DREVO */}
          {/* ======================================== */}
          <TabsContent value="drevo" className="space-y-4">
            <Card className="bg-slate-900/60 border-slate-700">
              <CardHeader>
                <CardTitle className="text-emerald-300 flex items-center gap-2">
                  <span className="text-2xl">∮</span> Yggdrasil — osebno drevo resnic
                </CardTitle>
                <CardDescription className="text-slate-400">
                  Kreacija je stopnja, ki iz prejšnje oblike iztisne nov prostor. Vsaka etaža nastane iz prejšnje, jo nosi, jo preseže.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex gap-4 flex-wrap mb-4">
                  <Button onClick={dodajKanon} className="bg-emerald-600 hover:bg-emerald-700">
                    + PASS (kanon vozlisc +1)
                  </Button>
                  <Button onClick={ustvariRuno} variant="outline" className="border-red-600 text-red-300 hover:bg-red-900/30">
                    + FAIL → Runa (brazgotina)
                  </Button>
                  <Button onClick={odpriZep} variant="outline" className="border-cyan-600 text-cyan-300 hover:bg-cyan-900/30">
                    ⟡ Žep (hkratnost)
                  </Button>
                </div>

                {/* SVG Yggdrasil Tree */}
                <div className="relative h-[500px] rounded-lg overflow-hidden bg-gradient-to-b from-slate-950 via-slate-900 to-black border border-slate-700">
                  <svg viewBox="0 0 600 500" className="w-full h-full">
                    {/* Korenine */}
                    <g stroke="#b43a2e" strokeWidth="2" fill="none" opacity="0.6">
                      <path d="M 300 350 Q 250 400 200 450" />
                      <path d="M 300 350 Q 300 410 290 460" />
                      <path d="M 300 350 Q 350 400 400 450" />
                    </g>
                    {/* Deblo */}
                    <line x1="300" y1="350" x2="300" y2="180" stroke="#d6a83a" strokeWidth="6" opacity="0.7" />
                    {/* Veje */}
                    <g stroke="#10b981" strokeWidth="2" fill="none" opacity="0.5">
                      <path d="M 300 180 Q 200 150 120 100" />
                      <path d="M 300 180 Q 300 130 280 70" />
                      <path d="M 300 180 Q 400 150 480 100" />
                      <path d="M 300 180 Q 350 120 420 80" />
                      <path d="M 300 180 Q 250 120 180 80" />
                    </g>

                    {/* Etaže kot vodoravne črte */}
                    {ETAZE.map((e, i) => {
                      const y = 60 + i * 55;
                      const odklenjena = odklenjenaEtaza >= e.st;
                      return (
                        <g key={e.st}>
                          <line
                            x1={80} y1={y} x2={520} y2={y}
                            stroke={odklenjena ? e.barva : "#1e293b"}
                            strokeWidth={odklenjena ? 1.5 : 0.5}
                            strokeDasharray={odklenjena ? "" : "4 4"}
                            opacity={odklenjena ? 0.4 : 0.15}
                          />
                          <text
                            x={50} y={y + 4}
                            fill={odklenjena ? e.barva : "#334155"}
                            fontSize="11"
                            fontFamily="monospace"
                            textAnchor="end"
                          >
                            {e.glyph} {e.ime}
                          </text>
                          {odklenjena && (
                            <text
                              x={540} y={y + 4}
                              fill="#475569"
                              fontSize="8"
                              fontFamily="monospace"
                            >
                              {e.vprasanje.substring(0, 20)}...
                            </text>
                          )}
                        </g>
                      );
                    })}

                    {/* Canon vozlisc kot žareče točke na drevesu */}
                    {Array.from({ length: Math.min(canonCount, 20) }).map((_, i) => {
                      const angle = (i / Math.max(canonCount, 1)) * Math.PI * 2;
                      const etazaIdx = Math.min(Math.floor(i / 3), 6);
                      const y = 60 + etazaIdx * 55;
                      const x = 300 + Math.cos(angle) * (40 + etazaIdx * 25);
                      return (
                        <g key={i}>
                          <circle cx={x} cy={y} r="5" fill="#d6a83a" opacity="0.9">
                            <animate attributeName="r" values="4;6;4" dur="2s" repeatCount="indefinite" begin={`${i * 0.2}s`} />
                          </circle>
                          <circle cx={x} cy={y} r="10" fill="none" stroke="#d6a83a" strokeWidth="0.5" opacity="0.3" />
                        </g>
                      );
                    })}

                    {/* Rune kot brazgotine */}
                    {runes.slice(0, 10).map((r, i) => {
                      const x = 120 + i * 45;
                      return (
                        <g key={r}>
                          <line x1={x} y1={460} x2={x + 15} y2={470} stroke="#ef4444" strokeWidth="2" opacity="0.8" />
                          <text x={x} y={490} fill="#ef4444" fontSize="7" fontFamily="monospace">{r}</text>
                        </g>
                      );
                    })}

                    {/* Žepi kot zvezde */}
                    {zepi.map((z, i) => {
                      const x = 300 + (i - zepi.length / 2 + 0.5) * 60;
                      return (
                        <g key={z}>
                          <text x={x} y={50} fill="#06b6d4" fontSize="16" textAnchor="middle">
                            ⟡
                            <animate attributeName="opacity" values="0.3;1;0.3" dur="3s" repeatCount="indefinite" />
                          </text>
                          <text x={x} y={65} fill="#06b6d4" fontSize="6" fontFamily="monospace" textAnchor="middle">{z}</text>
                        </g>
                      );
                    })}

                    {/* ∅ v sredini */}
                    <text x={300} y={260} fill="#06b6d4" fontSize="40" textAnchor="middle" opacity="0.15" fontFamily="serif">∅</text>
                  </svg>
                </div>

                <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-amber-400" /> Canon vozlisc: {canonCount}
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-red-500" /> Rune (brazgotine): {runes.length}
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-cyan-400" /> Žepi (hkratnost): {zepi.length}
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-slate-600" /> Odklenjene etaže: {odklenjenaEtaza}/7
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* ======================================== */}
          {/* TAB 3: 1/0 ZAPOVEDI */}
          {/* ======================================== */}
          <TabsContent value="zapovedi" className="space-y-4">
            <Card className="bg-slate-900/60 border-slate-700">
              <CardHeader>
                <CardTitle className="text-amber-300 flex items-center gap-2">
                  <span className="text-2xl">⊢</span> 1/0 Zapovedi — znane in neznane
                </CardTitle>
                <CardDescription className="text-slate-400">
                  Zapovedi predstavljajo prehode med 1 (dejanskostjo) in 0 (potencialnostjo). 1 = realizirana stvarnost, 0 = odprta pot.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {/* Znane zapovedi */}
                  {ZAPOVEDI_ZNANE.map((z) => (
                    <div
                      key={z.st}
                      className="p-3 rounded-lg border border-amber-700/30 bg-amber-900/10 hover:bg-amber-900/20 transition"
                    >
                      <div className="flex items-start justify-between mb-1">
                        <span className="text-amber-400 font-mono text-xs">ZAPOVED {z.st}</span>
                        <span className="text-lg text-amber-300 font-mono">{z.operator}</span>
                      </div>
                      <p className="text-sm text-slate-200 font-medium">1 · {z.en}</p>
                      <p className="text-xs text-slate-400 mt-1">0 · {z.nic}</p>
                    </div>
                  ))}

                  {/* Neznane zapovedi */}
                  {ZAPOVEDI_NEZNANE.map((z) => {
                    const odkrita = odkriteZapovedi.includes(z.st);
                    return (
                      <div
                        key={z.st}
                        className={`p-3 rounded-lg border transition ${
                          odkrita
                            ? "border-cyan-600/40 bg-cyan-900/15"
                            : "border-slate-800 bg-slate-900/30 opacity-60"
                        }`}
                      >
                        <div className="flex items-start justify-between mb-1">
                          <span className={`font-mono text-xs ${odkrita ? "text-cyan-400" : "text-slate-600"}`}>
                            {odkrita ? `ZAPOVED ${z.st} (ODKRITA)` : `??? ZAKLEPANA`}
                          </span>
                          <span className={`text-lg font-mono ${odkrita ? "text-cyan-300" : "text-slate-700"}`}>
                            {odkrita ? z.operator : "?"}
                          </span>
                        </div>
                        <p className={`text-sm font-medium ${odkrita ? "text-slate-200" : "text-slate-600"}`}>
                          {odkrita ? `1 · ${z.en.replace("???", "ODKRITO")}` : z.en}
                        </p>
                        <p className={`text-xs mt-1 ${odkrita ? "text-slate-400" : "text-slate-700"}`}>
                          {odkrita ? `0 · ${z.nic}` : "Odkrij skozi igro..."}
                        </p>
                      </div>
                    );
                  })}
                </div>

                <Separator className="my-4 bg-slate-700" />
                <p className="text-xs text-slate-500 italic">
                  "Zapovedi v tem okviru predstavljajo prehode med 1 (dejanskostjo) in 0 (potencialnostjo), kar pomeni dinamične faze, ki vključujejo transformacijo. Vsaka zapoved temelji na razumevanju notranjega ravnovesja, kjer je 0 odprta pot, 1 pa realizirana stvarnost."
                </p>
              </CardContent>
            </Card>
          </TabsContent>

          {/* ======================================== */}
          {/* TAB 4: FONEMI — dekompozicijski engine */}
          {/* ======================================== */}
          <TabsContent value="fonemi" className="space-y-4">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              {/* Dekompozicija besede */}
              <Card className="bg-slate-900/60 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-cyan-300 flex items-center gap-2">
                    <span className="text-2xl">∂</span> Fonetično-ontološki rez
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    Beseda = dejanje, ne sredstvo. Vsak fonem je aktivator, ne zvok. F = ∆(zvok)
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center gap-2">
                    <Button onClick={() => setBesedaIndex((besedaIndex - 1 + BESEDE_REZI.length) % BESEDE_REZI.length)} variant="outline" size="sm">
                      ←
                    </Button>
                    <span className="text-2xl font-bold text-cyan-200 font-mono">{trenutnaBeseda.beseda}</span>
                    <Button onClick={() => setBesedaIndex((besedaIndex + 1) % BESEDE_REZI.length)} variant="outline" size="sm">
                      →
                    </Button>
                  </div>

                  <div className="space-y-2">
                    {trenutnaBeseda.rez.map((fragment, i) => (
                      <motion.div
                        key={i}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: i * 0.15 }}
                        className="flex items-center gap-3 p-3 rounded-lg bg-slate-800/60 border border-slate-700"
                      >
                        <span
                          className="text-xl font-mono font-bold w-16 text-center px-2 py-1 rounded"
                          style={{
                            color: FONEM_OPERATORS.find(f => f.fonem.includes(fragment[0]))?.barva || "#06b6d4",
                            background: "rgba(6,182,212,0.1)"
                          }}
                        >
                          {fragment}
                        </span>
                        <span className="text-slate-300 text-sm flex-1">{trenutnaBeseda.pomeni[i]}</span>
                        <span className="text-2xl font-mono" style={{ color: FONEM_OPERATORS.find(f => f.fonem.includes(fragment[0]))?.barva || "#06b6d4" }}>
                          {trenutnaBeseda.operatorji[i]}
                        </span>
                      </motion.div>
                    ))}
                  </div>

                  <Separator className="bg-slate-700" />
                  <div className="p-3 rounded-lg bg-cyan-900/10 border border-cyan-800/30">
                    <p className="text-sm text-cyan-200">
                      <span className="font-mono text-xs text-cyan-500">BRANJE:</span><br />
                      {trenutnaBeseda.beseda} = {trenutnaBeseda.prevod}
                    </p>
                  </div>
                </CardContent>
              </Card>

              {/* Fonem → Operator preslikava */}
              <Card className="bg-slate-900/60 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-violet-300">Fonem → Operator</CardTitle>
                  <CardDescription className="text-slate-400">
                    "Fonemi niso zgolj zvoki — so generatorji prehoda skozi dimenzionalne faze."
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {FONEM_OPERATORS.map((f, i) => (
                      <motion.div
                        key={i}
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: i * 0.05 }}
                        className="flex items-center gap-2 p-2 rounded-lg bg-slate-800/40 border border-slate-700 hover:border-slate-500 transition"
                      >
                        <span className="font-mono text-sm w-12 text-center" style={{ color: f.barva }}>{f.fonem}</span>
                        <span className="text-2xl font-mono" style={{ color: f.barva }}>{f.operator}</span>
                        <span className="text-xs text-slate-400 flex-1">{f.sila}</span>
                      </motion.div>
                    ))}
                  </div>

                  <Separator className="my-3 bg-slate-700" />

                  {/* R-7 cikel */}
                  <div className="flex items-center justify-between gap-1">
                    {R7_CYCLE.map((op, i) => (
                      <div key={i} className="flex flex-col items-center">
                        <motion.div
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: i * 0.1 }}
                          className="w-10 h-10 rounded-full flex items-center justify-center text-lg font-mono"
                          style={{ background: `${op.barva}30`, border: `1px solid ${op.barva}`, color: op.barva }}
                        >
                          {op.glyph}
                        </motion.div>
                        <span className="text-[8px] text-slate-500 mt-1">{op.ime}</span>
                        {i < R7_CYCLE.length - 1 && (
                          <span className="text-slate-600 text-xs absolute" style={{ marginLeft: 28 + i * 52, marginTop: -24 }}>→</span>
                        )}
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* IZZIV — uporabnik ugiba operatorje */}
            <Card className="bg-slate-900/60 border-slate-700">
              <CardHeader>
                <CardTitle className="text-amber-300 flex items-center gap-2">
                  <span className="text-2xl">⟡</span> Izziv: razreši besedo
                </CardTitle>
                <CardDescription className="text-slate-400">
                  Izberi pravilne operatorje za vsak fragment besede. Vsak pravilni razrez = +1 kanon. Uči se preko dejanja, ne preko predstave.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center gap-3">
                  <span className="text-3xl font-bold text-amber-200 font-mono">{trenutniIzziv.beseda}</span>
                  <span className="text-slate-500 text-sm">→ {trenutniIzziv.rez.length} fragmentov</span>
                </div>

                {/* Fragmenti z sloti za ugib */}
                <div className="flex flex-wrap gap-2">
                  {trenutniIzziv.rez.map((fragment, i) => {
                    const guess = userGuess[i];
                    const correct = trenutniIzziv.operatorji[i];
                    const showResult = challengeResult !== null;
                    return (
                      <div key={i} className="flex flex-col items-center gap-1">
                        <span className="text-sm font-mono text-slate-400">{fragment}</span>
                        <div
                          className="w-12 h-12 rounded-lg border-2 flex items-center justify-center text-xl font-mono"
                          style={{
                            borderColor: showResult
                              ? guess === correct
                                ? "#10b981"
                                : "#ef4444"
                              : guess
                                ? "#d6a83a"
                                : "#334155",
                            background: showResult
                              ? guess === correct
                                ? "rgba(16,185,129,0.15)"
                                : "rgba(239,68,68,0.15)"
                              : guess
                                ? "rgba(214,168,58,0.1)"
                                : "#0f172a",
                            color: showResult
                              ? guess === correct
                                ? "#10b981"
                                : "#ef4444"
                              : guess || "#475569",
                          }}
                        >
                          {showResult && guess !== correct ? `${guess || "?"}→${correct}` : guess || "?"}
                        </div>
                      </div>
                    );
                  })}
                </div>

                {/* Paleta operatorjev za izbiro */}
                <div className="flex flex-wrap gap-2">
                  {R7_CYCLE.map((op) => (
                    <button
                      key={op.glyph}
                      onClick={() => ugibajOperator(op.glyph)}
                      disabled={challengeResult === "correct"}
                      className="w-10 h-10 rounded-lg border flex items-center justify-center text-lg font-mono transition hover:scale-110 disabled:opacity-40"
                      style={{ borderColor: op.barva, color: op.barva, background: op.barva + "15" }}
                    >
                      {op.glyph}
                    </button>
                  ))}
                </div>

                {/* Rezultat in akcije */}
                {challengeResult && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className={`p-3 rounded-lg border ${challengeResult === "correct" ? "border-emerald-600 bg-emerald-900/20" : "border-red-600 bg-red-900/20"}`}
                  >
                    <p className={`text-sm font-medium ${challengeResult === "correct" ? "text-emerald-300" : "text-red-300"}`}>
                      {challengeResult === "correct"
                        ? "✓ Pravilno! Kanon +1. Beseda je dejanje."
                        : `✗ Razrez ni pravilen. Pravilni operatorji: ${trenutniIzziv.operatorji.join(" → ")}`}
                    </p>
                    {challengeResult === "correct" && (
                      <p className="text-xs text-slate-400 mt-1">{trenutniIzziv.beseda} = {trenutniIzziv.prevod}</p>
                    )}
                  </motion.div>
                )}

                <div className="flex gap-2">
                  <Button onClick={potrdiUgib} disabled={userGuess.length < trenutniIzziv.operatorji.length} className="bg-amber-600 hover:bg-amber-700">
                    Potrdi razrez
                  </Button>
                  <Button onClick={pocistiUgib} variant="outline">
                    Počisti
                  </Button>
                  <Button onClick={naslednjiIzziv} variant="outline" className="border-cyan-600 text-cyan-300 hover:bg-cyan-900/30">
                    Naslednja beseda →
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
          {/* ======================================== */}
          <TabsContent value="etaze" className="space-y-4">
            <Card className="bg-slate-900/60 border-slate-700">
              <CardHeader>
                <CardTitle className="text-red-300 flex items-center gap-2">
                  <span className="text-2xl">∅</span> 7 Etaž Yggdrasila
                </CardTitle>
                <CardDescription className="text-slate-400">
                  "Vsaka etaža nastane iz prejšnje, jo nosi, jo preseže in se nekoč vrne k začetku — ne kot ponovitev, temveč kot višja zanka."
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {ETAZE.map((e) => {
                    const odklenjena = odklenjenaEtaza >= e.st;
                    const progress = odklenjena ? 100 : Math.min((canonCount / e.zahteva) * 100, 99);
                    return (
                      <motion.div
                        key={e.st}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className={`p-4 rounded-lg border transition ${
                          odklenjena
                            ? "border-slate-600 bg-slate-800/40"
                            : "border-slate-800 bg-slate-900/20 opacity-50"
                        }`}
                      >
                        <div className="flex items-center gap-4">
                          <div
                            className="w-14 h-14 rounded-full flex items-center justify-center text-2xl font-mono flex-shrink-0"
                            style={{
                              background: odklenjena ? `${e.barva}30` : "#0f172a",
                              border: `2px solid ${odklenjena ? e.barva : "#1e293b"}`,
                              color: odklenjena ? e.barva : "#334155"
                            }}
                          >
                            {e.glyph}
                          </div>
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2">
                              <span className="text-sm text-slate-500 font-mono">Etáž {e.st}</span>
                              <span className="font-bold text-slate-200">{e.ime}</span>
                              {odklenjena ? (
                                <Badge className="bg-emerald-500/20 text-emerald-300 text-xs">ODKLEPNJENA</Badge>
                              ) : (
                                <Badge className="bg-slate-700 text-slate-500 text-xs">ZAKLEPANA · {e.zahteva} kanon</Badge>
                              )}
                            </div>
                            <p className="text-xs text-slate-400 mt-1">{e.tema}</p>
                            <p className="text-sm text-slate-300 mt-2 italic">"{e.vprasanje}"</p>
                            {!odklenjena && e.zahteva > 0 && (
                              <div className="mt-2">
                                <div className="h-1.5 w-full rounded-full bg-slate-800 overflow-hidden">
                                  <div className="h-full rounded-full transition-all" style={{ width: `${progress}%`, background: e.barva }} />
                                </div>
                                <span className="text-[10px] text-slate-600 font-mono">{canonCount}/{e.zahteva} kanon</span>
                              </div>
                            )}
                          </div>
                        </div>
                      </motion.div>
                    );
                  })}
                </div>

                <Separator className="my-4 bg-slate-700" />

                {/* Liki kot funkcije */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                  {[
                    { ime: "ODIN", funkcija: "Žrtveni dokaz", barva: "#b43a2e", opis: "Runa ni hotela v roko. Runa je hotela rano." },
                    { ime: "LOKI", funkcija: "Agent motnje", barva: "#d6a83a", opis: "Ko igralec predolgo uporablja isto rešitev, Loki pokvari njen učinek." },
                    { ime: "RATATOSKR", funkcija: "Prenosnik trenja", barva: "#10b981", opis: "Vsako sporočilo, ki potuje skozi svet, se spremeni." },
                    { ime: "NÍÐHÖGGR", funkcija: "Razjedanje korenin", barva: "#8b5cf6", opis: "Če igralec ignorira koreninske probleme, višje etaže izgubljajo stabilnost." },
                    { ime: "JÖRMUNGANDR", funkcija: "Obroč sveta", barva: "#06b6d4", opis: "Ko igralec pride do roba, se vrne na začetek z eno spremenjeno zakonitostjo." },
                    { ime: "ŽEP", funkcija: "Trenutek hkratnosti", barva: "#f59e0b", opis: "Prostor, kjer se za trenutek uskladijo pomen + čas + oblika + telo + mitos." },
                  ].map((l) => (
                    <div key={l.ime} className="p-3 rounded-lg bg-slate-800/40 border border-slate-700">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="font-bold text-sm" style={{ color: l.barva }}>{l.ime}</span>
                        <span className="text-xs text-slate-500">{l.funkcija}</span>
                      </div>
                      <p className="text-xs text-slate-400 italic">{l.opis}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

        </Tabs>

        {/* FOOTER */}
        <div className="mt-6 pt-4 border-t border-slate-800">
          <p className="text-xs text-slate-600 text-center font-mono">
            "Beseda ni sredstvo, temveč dejanje." · "IGRA = NUJA, NE IZBIRA." · "Kreacija je stopnja, ki iz prejšnje oblike iztisne nov prostor."
          </p>
        </div>
      </div>
    </div>
  );
}