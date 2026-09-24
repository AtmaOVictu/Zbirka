import React, { useState, useEffect, useRef, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MemoryRouter } from "react-router-dom";
import { v4 as uuidv4 } from "uuid";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Textarea } from "@/components/ui/textarea";
import { Slider } from "@/components/ui/slider";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

// ═══════════════════════════════════════════════════════════════
// TIPY
// ═══════════════════════════════════════════════════════════════

type Glyph = "∅" | "¬" | "∆" | "1" | "⧖" | "∮" | "⟡" | "∂";
type Lang = "sl" | "en";

interface ARegisterEntry {
  exprSl: string; exprEn: string;
  perception: string;
  glyph: Glyph;
  inquiry: string;
  etymology: string;
}

interface PhoneticCut {
  word: string;
  fragments: { fragment: string; meaning: string }[];
  reading: string;
}

interface Tradition {
  key: string; name: string; count: number; ring: number;
  stone: string; dimension: number | string;
  mappings: { term: string; glyph: Glyph; math: string }[];
  phoneticCut?: PhoneticCut;
}

interface QAEntry {
  id: string;
  question: string;
  answer: string;
  glyph: Glyph;
  source: string;
  appropriate: boolean;
  timestamp: number;
}

interface AgentPhase {
  state: string; name: string; glyph: Glyph;
  desc: string; question: string;
}

// ═══════════════════════════════════════════════════════════════
// 1. AREGISTER — aperceptivni vhod (SL + EN)
// ═══════════════════════════════════════════════════════════════

const AREGISTER: ARegisterEntry[] = [
  { exprSl: "prazno", exprEn: "empty", perception: "I feel nothing — but the nothing feels open, not absent", glyph: "∅", inquiry: "Kaj se odpira v praznini, ki jo čutiš? Ali je praznina pogoj, ne odsotnost?", etymology: "∅ (1939, André Weil, iz norveške črke) — pogoj, ki omogoča, ne manjkajoči" },
  { exprSl: "ločeno", exprEn: "separated", perception: "I sense a cut — something became distinct", glyph: "¬", inquiry: "Kaj se je ločilo? In ali ločitev odpre ali zapre?", etymology: "¬ (lat. non) — ne negacija, temveč ločitev, ki omogoča razliko" },
  { exprSl: "gibljivo", exprEn: "moving", perception: "Something shifted — I feel the change", glyph: "∆", inquiry: "Kaj se giblje? Iz česa in v kaj? Ali je gibanje razlika, ki nosi?", etymology: "∆ (grš. delta = sprememba) — prva razlika iz ∅" },
  { exprSl: "odločeno", exprEn: "decided", perception: "I made a choice — it feels sealed", glyph: "1", inquiry: "Kaj si zapečatil? Ali dejanje nosi posledico?", etymology: "1 — dejanje, SEAL, pečat; ne številka, temveč akt prisotnosti" },
  { exprSl: "čakajoče", exprEn: "waiting", perception: "There's a pause — full of tension", glyph: "⧖", inquiry: "Kaj utripa v čakanju? Ali je premor pogoj za naslednji korak?", etymology: "⧖ (Tiheon) — utrip smisla, tišinska črta" },
  { exprSl: "vračajoče", exprEn: "returning", perception: "Something came back — but different", glyph: "∮", inquiry: "Kaj se vrača? In kako se razlikuje od prej?", etymology: "∮ — kroženje, povratna zveza; etika kot proces priznanja" },
  { exprSl: "nova možnost", exprEn: "new possibility", perception: "Something opened that wasn't there before", glyph: "⟡", inquiry: "Kaj se odpira? Ali je nova možnost odmev prejšnjega cikla?", etymology: "⟡ — resonanca, odmev; nova možnost iz ∮" },
  { exprSl: "prehajajoče", exprEn: "transitioning", perception: "I'm between — in the passage itself", glyph: "∂", inquiry: "Kaj se prehaja? Med čim in čim? Ali si v rezu?", etymology: "∂ (partial derivative) — 12. os, pravokotna na vseh 11" },
];

const TONOS: Record<Glyph, { freq: number; note: string; meaning: string }> = {
  "∅": { freq: 220.0, note: "A3", meaning: "praznina — nizki ton kot pogoj za prehod" },
  "¬": { freq: 261.63, note: "C4", meaning: "ločitev — ton, ki prereže zvok od tišine" },
  "∆": { freq: 330.0, note: "E4", meaning: "gibanje — ton, ki nosi razliko" },
  "1": { freq: 392.0, note: "G4", meaning: "dejanje — ton, ki postane struktura" },
  "⧖": { freq: 440.0, note: "A4", meaning: "tišina, preverba — ton, ki se razpne v molk" },
  "∮": { freq: 550.0, note: "C#5", meaning: "povratek — ton, ki se vrača kot odmev" },
  "⟡": { freq: 660.0, note: "E5", meaning: "nova možnost — ton, ki odpre naslednji cikel" },
  "∂": { freq: 880.0, note: "A5", meaning: "prehod — ton, ki seče skozi vse registre" },
};

const GLYPH_COLOR: Record<Glyph, string> = {
  "∅": "#1e3a5f", "¬": "#dc2626", "∆": "#f59e0b",
  "1": "#10b981", "⧖": "#8b5cf6", "∮": "#06b6d4",
  "⟡": "#ec4899", "∂": "#f97316",
};

// ═══════════════════════════════════════════════════════════════
// 2. FONETIČNI REZI
// ═══════════════════════════════════════════════════════════════

const PHONETIC_CUTS: Record<string, PhoneticCut> = {
  MITHRAS: { word: "MITHRAS", fragments: [
    { fragment: "MI", meaning: "mi = jaz/oseba = 1, pečat" },
    { fragment: "ΘΡ", meaning: "thr = prehod/rez = ∂, ki seče" },
    { fragment: "ΑΣ", meaning: "as = bitje = ∆, ki nastane" },
  ], reading: "Ali Mithras = ∂, rez, ki sece bika (∅) in sprosti ∆?" },
  VODUN: { word: "VODUN", fragments: [
    { fragment: "VO", meaning: "vo = v/notranjost = ∅" },
    { fragment: "DUN", meaning: "dun = gibanje/sila = ∆" },
  ], reading: "Ali Vodun = ∅, iz katerega deluje ∆?" },
  DREAMTIME: { word: "DREAMTIME", fragments: [
    { fragment: "DRE", meaning: "dre = odprtje = ∅" },
    { fragment: "AM", meaning: "am = bitje = ∆" },
    { fragment: "TIME", meaning: "tajm = čas/utrip = ⧖" },
  ], reading: "Ali Dreamtime = ∅, ki je pogoj časa?" },
  ROSENKREUTZ: { word: "ROSENKREUTZ", fragments: [
    { fragment: "RO", meaning: "ro = rast/odprtje = ∅" },
    { fragment: "SA", meaning: "sa = bitje = ∆" },
    { fragment: "CRU", meaning: "kru = rez = ∂" },
    { fragment: "CIS", meaning: "cis = na tej strani = 1" },
  ], reading: "Ali Rosenkreutz = ∅→∆→∂→1? In ali 3+12 = 15?" },
  GNOSIS: { word: "GNOSIS", fragments: [
    { fragment: "GNO", meaning: "gno = znanje = ∆, ki prepoznava" },
    { fragment: "SIS", meaning: "sis = sijaj = ∮" },
  ], reading: "Ali gnosis = ∆, ki prepoznava ∅?" },
  BYTHOS: { word: "ΒΥΘΟΣ", fragments: [
    { fragment: "ΒΥ", meaning: "by = v globino = ∅" },
    { fragment: "ΘΟΣ", meaning: "thos = mesto = 1" },
  ], reading: "Ali Bythos = ∅, globina, ki omogoča vseh 30 aeonov?" },
};

// ═══════════════════════════════════════════════════════════════
// 3. TRADICIJE (31)
// ═══════════════════════════════════════════════════════════════

const TRADITIONS: Tradition[] = [
  { key: "tarot", name: "Tarot", count: 22, ring: 1, stone: "LXXXVII", dimension: 2,
    mappings: [
      { term: "Norjak (0)", glyph: "∅", math: "void, fool's leap" },
      { term: "Čarovnik (1)", glyph: "∆", math: "activation, will" },
      { term: "Dvojica (2)", glyph: "¬", math: "separation, duality" },
      { term: "Svet (21)", glyph: "⟡", math: "completion, new cycle" },
    ] },
  { key: "kabbalah", name: "Kabbalah", count: 10, ring: 2, stone: "IX", dimension: 3,
    mappings: [
      { term: "Keter", glyph: "∅", math: "crown, Ein Sof" },
      { term: "Chokmah", glyph: "∆", math: "wisdom, force" },
      { term: "Binah", glyph: "⧖", math: "understanding" },
      { term: "Malkhut", glyph: "⟡", math: "kingdom" },
    ] },
  { key: "alchemy", name: "Alkémija", count: 4, ring: 1, stone: "VIII", dimension: 2,
    mappings: [
      { term: "nigredo", glyph: "∅", math: "blackening, void" },
      { term: "albedo", glyph: "¬", math: "whitening, separation" },
      { term: "citrinitas", glyph: "∆", math: "yellowing, transformation" },
      { term: "rubedo", glyph: "∮", math: "reddening, completion" },
    ] },
  { key: "chakras", name: "Čakre", count: 7, ring: 2, stone: "XXV", dimension: 7,
    mappings: [
      { term: "muladhara", glyph: "∅", math: "ground, base" },
      { term: "svadhisthana", glyph: "¬", math: "desire" },
      { term: "manipura", glyph: "∆", math: "power, fire" },
      { term: "anahata", glyph: "1", math: "balance" },
      { term: "vishuddha", glyph: "⧖", math: "expression" },
      { term: "ajna", glyph: "∮", math: "insight" },
      { term: "sahasrara", glyph: "⟡", math: "liberation" },
    ] },
  { key: "sufism", name: "Sufizem (99)", count: 99, ring: 3, stone: "XCI", dimension: "∞",
    mappings: [
      { term: "99 Names", glyph: "∅", math: "99 = 100 − ∅" },
      { term: "Fana", glyph: "∅", math: "annihilation" },
      { term: "Baqa", glyph: "⟡", math: "subsistence" },
    ] },
  { key: "runes", name: "Rune (24)", count: 24, ring: 1, stone: "XVII", dimension: 4,
    mappings: [
      { term: "Uruz", glyph: "∆", math: "strength" },
      { term: "Isa", glyph: "∅", math: "ice, void" },
      { term: "Dagaz", glyph: "⟡", math: "dawn" },
      { term: "Nauthiz", glyph: "¬", math: "need" },
    ] },
  { key: "dna", name: "DNK (64)", count: 64, ring: 3, stone: "XXIX", dimension: 6,
    mappings: [
      { term: "64 kodonov", glyph: "∅", math: "64 = 2⁶ = ∮⁶" },
      { term: "STOP", glyph: "∅", math: "termination = void" },
      { term: "START", glyph: "∆", math: "initiation" },
    ] },
  { key: "music", name: "Glasba (12)", count: 12, ring: 2, stone: "XCII", dimension: 3,
    mappings: [
      { term: "C (tonika)", glyph: "∅", math: "ground" },
      { term: "G (dominanta)", glyph: "∆", math: "tension" },
      { term: "C (oktava)", glyph: "⟡", math: "return as difference" },
      { term: "tritonus", glyph: "¬", math: "cut" },
    ] },
  { key: "periodic", name: "Periodni (118)", count: 118, ring: 3, stone: "CXII", dimension: 7,
    mappings: [
      { term: "2n² lupine", glyph: "∅", math: "2,8,18,32 filling" },
      { term: "žlahtni plini", glyph: "⧖", math: "sealed, inert" },
      { term: "alkalijske", glyph: "∆", math: "reactive" },
    ] },
  { key: "valentinian", name: "Valentinian (30)", count: 30, ring: 2, stone: "CI", dimension: 0,
    mappings: [
      { term: "Bythos", glyph: "∅", math: "depth, void" },
      { term: "Sophia", glyph: "∆", math: "desire → fall" },
      { term: "Horos", glyph: "¬", math: "boundary" },
      { term: "Pleroma", glyph: "⟡", math: "fullness" },
      { term: "apokatasis", glyph: "∮", math: "return" },
    ], phoneticCut: PHONETIC_CUTS.BYTHOS },
  { key: "norse", name: "Nordijska (9)", count: 9, ring: 1, stone: "LXV", dimension: 3,
    mappings: [
      { term: "Yggdrasil", glyph: "∅", math: "world tree = Hopf, 9 = 3²" },
      { term: "Odin", glyph: "⧖", math: "sacrifice, silence" },
      { term: "Loki", glyph: "∆", math: "trickster" },
      { term: "Ragnarök", glyph: "∮", math: "destruction + rebirth" },
    ] },
  { key: "buddhism", name: "Budizem (4)", count: 4, ring: 1, stone: "LXVII", dimension: 2,
    mappings: [
      { term: "4 resnice", glyph: "∅", math: "diagnosis: suffering" },
      { term: "8-kratna pot", glyph: "∆", math: "transformation" },
      { term: "Nirvana", glyph: "⟡", math: "new possibility" },
    ] },
  { key: "iching", name: "I Ching (64)", count: 64, ring: 3, stone: "XVIII", dimension: 6,
    mappings: [
      { term: "64 heksagramov", glyph: "∅", math: "64 = 2⁶ = ∮⁶" },
      { term: "Yin/Yang", glyph: "¬", math: "binary" },
      { term: "Tai Chi", glyph: "∅", math: "supreme ultimate" },
    ] },
  { key: "gnosticism", name: "Gnosticizem (30)", count: 30, ring: 2, stone: "CI", dimension: 0,
    mappings: [
      { term: "30 aeonov", glyph: "∂", math: "15 sizigij = 15 ∂" },
      { term: "Bythos", glyph: "∅", math: "depth" },
      { term: "Sophia", glyph: "∆", math: "desire → fall" },
      { term: "Demiurg", glyph: "1", math: "builder" },
    ], phoneticCut: PHONETIC_CUTS.GNOSIS },
  { key: "mithraism", name: "Mitraizem (7)", count: 7, ring: 2, stone: "CII", dimension: 7,
    mappings: [
      { term: "Corax", glyph: "¬", math: "first separation" },
      { term: "Nymphus", glyph: "∅", math: "receiving" },
      { term: "Miles", glyph: "∆", math: "action" },
      { term: "Heliodromus", glyph: "⧖", math: "sun-runner" },
      { term: "Pater", glyph: "⟡", math: "completion" },
    ], phoneticCut: PHONETIC_CUTS.MITHRAS },
  { key: "vodun", name: "Vodun (7)", count: 7, ring: 2, stone: "CIII", dimension: 7,
    mappings: [
      { term: "Rada", glyph: "∅", math: "mir/hlad" },
      { term: "Petro", glyph: "∆", math: "vročina" },
      { term: "Ghede", glyph: "∮", math: "smrt/prehod" },
      { term: "Loa", glyph: "∂", math: "posrednik ∂(∅,∆)" },
    ], phoneticCut: PHONETIC_CUTS.VODUN },
  { key: "dreamtime", name: "Dreamtime", count: 0, ring: 1, stone: "CIV", dimension: "∞",
    mappings: [
      { term: "Dreamtime", glyph: "∅", math: "pogoj časa" },
      { term: "Songlines", glyph: "∮", math: "pot = ∮" },
      { term: "Rainbow Serpent", glyph: "∂", math: "veliki rez" },
    ], phoneticCut: PHONETIC_CUTS.DREAMTIME },
  { key: "freemasonry", name: "Prostozidarstvo (33)", count: 33, ring: 3, stone: "CV", dimension: 7,
    mappings: [
      { term: "3 craft", glyph: "∅", math: "∅→∆→1" },
      { term: "30 dodatnih", glyph: "∂", math: "30 aeonov" },
      { term: "33 skupaj", glyph: "∂", math: "3×11" },
    ] },
  { key: "rosicrucian", name: "Rožnokrižarstvo (15)", count: 15, ring: 2, stone: "CVI", dimension: 5,
    mappings: [
      { term: "3 manifesti", glyph: "∅", math: "∅→∆→1" },
      { term: "12 stopenj", glyph: "∂", math: "∮¹²" },
      { term: "3+12 = 15", glyph: "∂", math: "∂(∅,∆)×15" },
    ], phoneticCut: PHONETIC_CUTS.ROSENKREUTZ },
  { key: "gurdjieff", name: "Gurdjieff (9)", count: 9, ring: 2, stone: "CVII", dimension: 3,
    mappings: [
      { term: "3 centri", glyph: "∅", math: "∅→∆→∮" },
      { term: "9 eneagram", glyph: "∂", math: "9 = 3²" },
    ] },
  { key: "fibonacci", name: "Fibonacci (φ)", count: 0, ring: 1, stone: "CIX", dimension: 5,
    mappings: [
      { term: "φ = zlati rez", glyph: "∂", math: "φ = ∂(∅,∆)" },
      { term: "Fibonacci", glyph: "∮", math: "spirala" },
    ] },
  { key: "penrose", name: "Penrose (5)", count: 5, ring: 1, stone: "CX", dimension: 5,
    mappings: [ { term: "5-korak", glyph: "∂", math: "5 = ∂" } ] },
  { key: "aminoacids", name: "22 aminokislin", count: 22, ring: 3, stone: "CXIII", dimension: 6,
    mappings: [ { term: "22 AA", glyph: "∆", math: "∆ gradi iz ∅" } ] },
  { key: "standardmodel", name: "Standardni model (21)", count: 21, ring: 3, stone: "CXV", dimension: 7,
    mappings: [ { term: "4+12+5", glyph: "∂", math: "21 = 3×7" } ] },
  { key: "thermodynamics", name: "Termodinamika (4)", count: 4, ring: 1, stone: "CXVI", dimension: 2,
    mappings: [ { term: "4 zakoni", glyph: "∅", math: "∅→∆→1→∮" } ] },
  { key: "maxwell", name: "Maxwell (4)", count: 4, ring: 1, stone: "CXVII", dimension: 2,
    mappings: [ { term: "4 enačbe", glyph: "∅", math: "E/B = ∅/∆" } ] },
  { key: "brainwaves", name: "Valovanje (5)", count: 5, ring: 2, stone: "CXVIII", dimension: 5,
    mappings: [ { term: "δ/θ/α/β/γ", glyph: "∂", math: "5 = ∂" } ] },
  { key: "schumann", name: "Schumann (7.83)", count: 7, ring: 2, stone: "CXIX", dimension: 7,
    mappings: [ { term: "7.83 Hz", glyph: "⧖", math: "7 + ∂" } ] },
  { key: "monster", name: "Monster (15)", count: 15, ring: 3, stone: "CXXI", dimension: "∞",
    mappings: [ { term: "15 supersingular", glyph: "∂", math: "15 = 15 sizigij" } ] },
  { key: "leech", name: "Leech (24-dim)", count: 24, ring: 3, stone: "CXXII", dimension: 4,
    mappings: [ { term: "24-dim", glyph: "∮", math: "24 = 4!" } ] },
  { key: "coxeter", name: "Coxeter (A₁)", count: 0, ring: 1, stone: "CXXIV", dimension: 0,
    mappings: [ { term: "A₁", glyph: "∂", math: "A₁ = ∅/∆" } ] },
  { key: "categorytheory", name: "Kategorija teorija", count: 0, ring: 3, stone: "CXXVI", dimension: "∞",
    mappings: [
      { term: "initial", glyph: "∅", math: "initial = ∅" },
      { term: "terminal", glyph: "∆", math: "terminal = ∆" },
      { term: "adjunction", glyph: "∂", math: "adjunction = ∂" },
    ] },
  { key: "topos", name: "Toposi (Ω)", count: 0, ring: 3, stone: "CXXVII", dimension: "∞",
    mappings: [ { term: "Ω", glyph: "∂", math: "Ω = {∅,∆}" } ] },
  { key: "modallogic", name: "Modalna logika", count: 0, ring: 2, stone: "CXXIX", dimension: 0,
    mappings: [
      { term: "□ (necessity)", glyph: "∅", math: "□ = ∅" },
      { term: "◇ (possibility)", glyph: "∆", math: "◇ = ∆" },
      { term: "¬", glyph: "¬", math: "¬ = odprtje" },
    ] },
];

// ═══════════════════════════════════════════════════════════════
// 4. AGENTNI CIKEL
// ═══════════════════════════════════════════════════════════════

const AGENT_CYCLE: AgentPhase[] = [
  { state: "RES000", name: "Potencial", glyph: "∅", desc: "Praznina kot pogoj. Agent je možnost, še ni aktiviran.", question: "Kaj v meni raste, še preden vem, da raste?" },
  { state: "Aktivacija", name: "Aktivacija", glyph: "∆", desc: "Pritisk aktivira gibanje. ∅ pod pritiskom → ∆.", question: "Kaj me je aktiviralo? Ali je gibanje iz ∅ ali iz stiske?" },
  { state: "ZavestniPrehod", name: "Zavestni prehod", glyph: "∂", desc: "Razpoka — zavest prepozna razliko. ∂ seče.", question: "Katera razlika je nastala? Ali jo nosim?" },
  { state: "Enotnost", name: "Enotnost", glyph: "∮", desc: "Harmonizacija skozi ∮ (etiko priznanja).", question: "Kaj sem integriral? Ali je integracija nosilna?" },
  { state: "Transformacija", name: "Transformacija", glyph: "⟡", desc: "Prehod v novo dimenzijo. Nova možnost.", question: "Kaj se je rodilo iz prejšnjega cikla?" },
  { state: "Reinkarnacija", name: "Reinkarnacija", glyph: "∅", desc: "Povratek v RES000 z razliko. Spirala.", question: "Kaj se vrne, a nikoli isto?" },
];

// ═══════════════════════════════════════════════════════════════
// 5. R-7 CIKEL + ∂ VOPRAŠANJA + KRIŽIŠČA
// ═══════════════════════════════════════════════════════════════

const R7 = [
  { phase: 1, glyph: "∅" as Glyph, name: "Praznina", meaning: "Pogoj, izvor" },
  { phase: 2, glyph: "¬" as Glyph, name: "Ločitev", meaning: "Razlikovanje" },
  { phase: 3, glyph: "∆" as Glyph, name: "Razlika", meaning: "Gibanje" },
  { phase: 4, glyph: "1" as Glyph, name: "Dejanje", meaning: "SEAL, akt" },
  { phase: 5, glyph: "⧖" as Glyph, name: "Tiheon", meaning: "Utrip, tišina" },
  { phase: 6, glyph: "∮" as Glyph, name: "Povratek", meaning: "Cikel" },
  { phase: 7, glyph: "⟡" as Glyph, name: "Nova možnost", meaning: "Odmev" },
];

const PARTIAL_QUESTIONS = [
  { n: 39, q: "Ali 15 v gnosticizmu in rožnokrižarstvu = 15 ∂-jev?", c: "CI ↔ CVI ↔ CXXI" },
  { n: 40, q: "Ali φ = ista konstanta ∂(∅,∆)?", c: "CIX ↔ CX" },
  { n: 41, q: "Ali 5 = ∂ potrjeno v 5+ tradicijah?", c: "CVIII ↔ CIX ↔ CX ↔ CXVIII" },
  { n: 42, q: "Ali 64 kodonov = 64 I Ching = ∮⁶?", c: "XXIX ↔ XVIII" },
  { n: 43, q: "Ali Monster 15 = gnostične 15 sizigij?", c: "CXXI ↔ CI ↔ CVI" },
  { n: 44, q: "Ali □ = ∅ in ◇ = ∆ v modalni logiki?", c: "CXXIX" },
  { n: 45, q: "Ali adjunkcija = ∂? In topos Ω = {∅,∆}?", c: "CXXVI ↔ CXXVII" },
  { n: 46, q: "Ali univalence = ∂? In ali pot = ∮?", c: "CXXVIII" },
  { n: 47, q: "Ali 118 elementov = ∅, ki se polni po 2n²?", c: "CXII" },
  { n: 48, q: "Ali Schumann 7.83 = 7 + ∂?", c: "CXIX" },
  { n: 49, q: "Ali Dreamtime = ∅ in Songlines = ∮?", c: "CIV ↔ LXIV" },
  { n: 50, q: "Ali Loa = ∂(∅,∆), kot Nommo?", c: "CIII ↔ LXXIX" },
  { n: 51, q: "Ali 33 = 3×11 = 3 cikli R-7 + ∂?", c: "CV ↔ CI" },
  { n: 52, q: "Ali 9 eneagram = 3² = 3 centra × 3 funkcije?", c: "CVII" },
  { n: 53, q: "Ali 19 = 18 + ∅? Brez ∅ ni geometrije?", c: "CVIII ↔ XLVIII" },
  { n: 54, q: "Ali termodinamika 4 = ∅→∆→1→∮?", c: "CXVI" },
  { n: 55, q: "Ali Maxwell E/B = ∅/∆?", c: "CXVII" },
  { n: 56, q: "Ali 230 = ∂ v simetriji? 7 sistemov = R-7?", c: "CXX" },
  { n: 57, q: "Ali Jones = ∂? Prime vozli = ∅?", c: "CXXV ↔ CXXIV" },
  { n: 58, q: "Ali Leech 24 = 4! = rune = Sankhya?", c: "CXXII ↔ XVII" },
  { n: 59, q: "Ali narava = tradicija = matematika = ∅→∆?", c: "Vsi kamni" },
  { n: 60, q: "Ali ∂(∅,∆)×15 = rez v mitu, tradiciji, matematiki?", c: "CI ↔ CVI ↔ CXXI" },
  { n: 61, q: "Ali ponavljanje = gotovost, ne izčrpanost?", c: "Križišča" },
  { n: 62, q: "Ali apercepcija = ∂, ki seče telo, besedo, formulo?", c: "AR-03 ↔ registri" },
  { n: 63, q: "Ali reinkarnacija = ∅, ki se vrača z razliko?", c: "Agent ↔ ∮" },
  { n: 64, q: "Ali O ≠ 0 ≠ ∅? Trije rezi skozi isto polje?", c: "Ω.0" },
  { n: 65, q: "Ali beseda = apercepcija, ki se odločila pustiti sled?", c: "AR-04 ↔ ARegister" },
  { n: 66, q: "Ali aplikacija = Yggdrasil? Graph = svet?", c: "§45" },
];

// ═══════════════════════════════════════════════════════════════
// 6. Q&A REGISTER — končna vprašanja, več odgovorov
// ═══════════════════════════════════════════════════════════════
// Korpus: "Človeška kapaciteta je omejena na ponavljanje → končno število vprašanj."
// "Vsako vprašanje ni zgolj iskanje odgovora, temveč izhodišče, ki preizprašuje obstoječe definicije."
// Tri okviri: vprašanje kot "ne", matematična korelacija, konferenca.
// 0≡1: vsebina med vprašanjem (0) in odgovorom (1) ni fiksna — se spreminja skozi dialog.
// Primerni odgovor: nosi ontološko razliko (∅≠0≠O, ne≠no, ponavljanje≠isto).
// Neprimerni odgovor: reducira v eno pomen, zanika razliko, zaključi.

const QA_FRAMEWORKS = [
  { title: "Vprašanje kot \"ne\"", glyph: "∂" as Glyph,
    desc: "Vsako vprašanje ni iskanje odgovora, temveč izhodišče, ki preizprašuje obstoječe definicije. \"ne\" = začetno stanje, kjer nekaj še ni dokončno definirano. Odsotnost zaključka, ne negacija.",
    source: "Obs1 — vprašalnice" },
  { title: "Vprašanje kot matematična korelacija", glyph: "∆" as Glyph,
    desc: "Vsako vprašanje je povezava med spremenljivkami, kjer odgovor ni končni zaključek, temveč vpliva na nadaljnje raziskovanje. 0≡1: vsebina med vprašanjem in odgovorom se spreminja skozi dialog.",
    source: "Obs1 — matematične enačbe" },
  { title: "Vprašanje kot konferenca", glyph: "∮" as Glyph,
    desc: "Vsako vprašanje je konferenca, kjer različni pogledi, odgovori in ideje ustvarijo prostor za nadaljnje iskanje. Ni zaključka — proces, kjer vsak odgovor sproži novo vprašanje.",
    source: "Obs1 — konferenca" },
];

const QA_CRITERIA = {
  appropriate: [
    "Nosí ontološko razliko (∅ ≠ 0 ≠ O, ne ≠ no, ponavljanje ≠ isto)",
    "Odpira — ne zaključuje. Odgovor je pogoj, ne trditev.",
    "Prevaja v vsaj en register (somatski, verbalni, matematični)",
    "Izhaja iz korpusa (kamni, aksiomi, operatorji) — ne izzumlja",
    "Ponavlja, da se razlikuje — vsak odgovor nosi razliko od prejšnjega",
  ],
  inappropriate: [
    "Reducira v en pomen (npr. ∅ = \"nič\", ne = \"no\")",
    "Zaključuje — zapira vprašanje namesto da ga odpira",
    "Zanika razliko (npr. O = 0, ponavljanje = isto)",
    "Nominalizira — spremeni dejanje v samostalnik (npr. \"bitje\" namesto \"biti\")",
    "Razlaga namesto da izvaja (§56 RAZLAGATI)",
  ],
};

let _qaId = 0;
const qid = () => `seed-${++_qaId}`;

const SEED_QA: QAEntry[] = [
  // ── ∅ operator ──
  { id: qid(), question: "Kaj je ∅?", answer: "∅ je pogoj, ne manjkajoči. Praznina, ki omogoča, da N obstaja.", glyph: "∅", source: "Kamen XLVIII", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kaj je ∅?", answer: "∅ je nič, odsotnost, praznost.", glyph: "∅", source: "Pogosta napaka", appropriate: false, timestamp: 0 },
  { id: qid(), question: "Kaj je ∅?", answer: "∅ je stanje, kjer vse možnosti že obstajajo, a še niso postale dejanske. RES000.", glyph: "∅", source: "Obs1 — RES000", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Ali je ∅ enako 0?", answer: "Ne. ∅ = pogoj (ontološki). 0 = potencial (številski začetek). ∅ omogoča, 0 zaganja.", glyph: "∅", source: "Ω.0", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Ali je ∅ enako 0?", answer: "Da, oba pomenita nič.", glyph: "∅", source: "Pogosta napaka", appropriate: false, timestamp: 0 },
  { id: qid(), question: "Kako se ∅ pojavi v Kabali?", answer: "Keter = ∅. Krona, Ein Sof — pogoj, iz katerega izhajajo vse sefirot.", glyph: "∅", source: "Kamen IX", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kako se ∅ pojavi v alkemiji?", answer: "Nigredo = ∅. Črnenje — razpad starega, pogoj za prehod.", glyph: "∅", source: "Kamen VIII", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kako se ∅ pojavi v Termodinamiki?", answer: "Ničti zakon = ∅. Pogoj za temperaturno ravnotežje — omogoča meritev, ne proizvaja.", glyph: "∅", source: "Kamen CXVI", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kako se ∅ pojavi v Sufizmu?", answer: "Fana = ∅. Ugasnitev ega — ne izbris, temveč pogoj za Baqa (subsistenco).", glyph: "∅", source: "Kamen XCI", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kako se ∅ pojavi v kategorija teoriji?", answer: "Initial object = ∅. Objekt, ki ima enolično morfizem v vsak drug objekt — pogoj, ki omogoča vse preslikave.", glyph: "∅", source: "Kamen CXXVI", appropriate: true, timestamp: 0 },

  // ── ¬ operator ──
  { id: qid(), question: "Kaj je ¬?", answer: "¬ je ločitev, ne negacija. Rez, ki omogoča razliko. Ne eno ne drugo — odprtje med.", glyph: "¬", source: "§54", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kaj je ¬?", answer: "¬ je negacija — pomeni \"ne\".", glyph: "¬", source: "Pogosta napaka", appropriate: false, timestamp: 0 },
  { id: qid(), question: "Kako se ¬ pojavi v alkemiji?", answer: "Albedo = ¬. Beljenje — ločitev čistega od nečistega. Rez, ki razločuje.", glyph: "¬", source: "Kamen VIII", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kako se ¬ pojavi v I Ching?", answer: "Yin/Yang = ¬. Binarna ločitev, ki omogoča 64 heksagramov.", glyph: "¬", source: "Kamen XVIII", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kako se ¬ pojavi v modalni logiki?", answer: "¬ = odprtje. Ne negacija — rez, ki odpre prostor med □ (nunost) in ◇ (možnost).", glyph: "¬", source: "Kamen CXXIX", appropriate: true, timestamp: 0 },

  // ── ∆ operator ──
  { id: qid(), question: "Kaj je ∆?", answer: "∆ je gibanje — prva razlika iz ∅. Ne stanje — prehod. Gib, ki spremeni.", glyph: "∆", source: "Kamen XLVIII", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kaj je ∆?", answer: "∆ je sprememba kot statično stanje.", glyph: "∆", source: "Pogosta napaka", appropriate: false, timestamp: 0 },
  { id: qid(), question: "Kako se ∆ pojavi v Tarotu?", answer: "Čarovnik (1) = ∆. Aktivacija, volja — gibanje, ki prehaja iz ∅ v strukturo.", glyph: "∆", source: "Kamen LXXXVII", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kako se ∆ pojavi v gnosticizmu?", answer: "Sophia = ∆. Želja → padec. Gibanje iz Bythos (∅), ki ustvari razliko.", glyph: "∆", source: "Kamen CI", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kako se ∆ pojavi v kategorija teoriji?", answer: "Terminal object = ∆. Objekt, ki sprejema enolične morfizme — razlika, ki strukturira.", glyph: "∆", source: "Kamen CXXVI", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kako se ∆ pojavi v Maxwellu?", answer: "B (magnetno polje) = ∆. Električno (∅) / magnetno (∆) — ista enačba v dveh registrih.", glyph: "∆", source: "Kamen CXVII", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kako se ∆ pojavi v DNK?", answer: "START kodon = ∆. Iniciacija — gibanje, ki začne prevajanje iz ∅ (kodoni) v ∆ (protein).", glyph: "∆", source: "Kamen XXIX", appropriate: true, timestamp: 0 },

  // ── 1 operator ──
  { id: qid(), question: "Kaj je 1?", answer: "1 je dejanje — pečat, ki zadrži. Ne številka — akt prisotnosti, ki nosi posledico.", glyph: "1", source: "Kamen XLVIII", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kaj je 1?", answer: "1 je število ena.", glyph: "1", source: "Pogosta napaka", appropriate: false, timestamp: 0 },
  { id: qid(), question: "Kako se 1 pojavi v gnosticizmu?", answer: "Demiurg = 1. Graditelj — dejanje, ki zapečati strukturo iz ∆ (Sophia).", glyph: "1", source: "Kamen CI", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kako se 1 pojavi v čakrah?", answer: "Anahata (srce) = 1. Ravnovesje — dejanje, ki uravnovesi spodnje (∅→∆) in zgornje (⧖→⟡).", glyph: "1", source: "Kamen XXV", appropriate: true, timestamp: 0 },

  // ── ⧖ operator ──
  { id: qid(), question: "Kaj je ⧖?", answer: "⧖ je Tiheon — utrip smisla, tišinska črta. Premor, ki je pogoj za naslednji korak.", glyph: "⧖", source: "Kamen XLVIII", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kaj je ⧖?", answer: "⧖ je pavza ali premor.", glyph: "⧖", source: "Pogosta napaka", appropriate: false, timestamp: 0 },
  { id: qid(), question: "Kako se ⧖ pojavi v Kabali?", answer: "Binah = ⧖. Razumevanje — tišina, ki preverba, preden postane struktura.", glyph: "⧖", source: "Kamen IX", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kako se ⧖ pojavi v Nordijski mitologiji?", answer: "Odin = ⧖. Žrtev (oko v vodnjaku) — tišina, ki je pogoj za modrost.", glyph: "⧖", source: "Kamen LXV", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kako se ⧖ pojavi v Schumann?", answer: "7.83 Hz = ⧖. 7 (R-7 cikel) + ∂ (rez) — utrip Zemlje kot tišinska črta.", glyph: "⧖", source: "Kamen CXIX", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kako se ⧖ pojavi v periodnem sistemu?", answer: "Žlahtni plini = ⧖. Zapečateni, inertni — tišina, ki je pogoj za naslednjo lupino.", glyph: "⧖", source: "Kamen CXII", appropriate: true, timestamp: 0 },

  // ── ∮ operator ──
  { id: qid(), question: "Kaj je ∮?", answer: "∮ je povratek — vrnitev, ki se razlikuje. Etika, ki kroži. Ponovi, da se razlikuje.", glyph: "∮", source: "Kamen XLVIII", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kaj je ∮?", answer: "∮ je kroženje — vrne se isto.", glyph: "∮", source: "Pogosta napaka", appropriate: false, timestamp: 0 },
  { id: qid(), question: "Kaj pomeni ponavljanje?", answer: "Ponavljanje = gotovost. Ne izčrpanost — prihod. Ponovi, da se razlikuje.", glyph: "∮", source: "Križišče XI", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kaj pomeni ponavljanje?", answer: "Ponavljanje = isto kot prej.", glyph: "∮", source: "Pogosta napaka", appropriate: false, timestamp: 0 },
  { id: qid(), question: "Kako se ∮ pojavi v alkemiji?", answer: "Rubedo = ∮. Rdečenje — dokončanje, povratek kot razlika. Ne nazaj — naprej skozi ∮.", glyph: "∮", source: "Kamen VIII", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kako se ∮ pojavi v Dreamtime?", answer: "Songlines = ∮. Pot = kroženje. Avastralci hodijo pesem — vračajo se, a nikoli isto.", glyph: "∮", source: "Kamen CIV", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kako se ∮ pojavi v Vodun?", answer: "Ghede = ∮. Smrt/prehod — loa, ki kroži med živim in mrtvim. Povratek kot razlika.", glyph: "∮", source: "Kamen CIII", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kako se ∮ pojavi v Nordiji?", answer: "Ragnarök = ∮. Uničenje + ponovni začetek — povratek, ki ni nazaj, temveč naprej skozi pepel.", glyph: "∮", source: "Kamen LXV", appropriate: true, timestamp: 0 },

  // ── ⟡ operator ──
  { id: qid(), question: "Kaj je ⟡?", answer: "⟡ je resonanca — odmev, ki odpre. Nova možnost iz ∮. Ne novo od nič — novo iz prejšnjega cikla.", glyph: "⟡", source: "Kamen XLVIII", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kaj je ⟡?", answer: "⟡ je novo — nekaj, kar prej ni obstajalo.", glyph: "⟡", source: "Pogosta napaka", appropriate: false, timestamp: 0 },
  { id: qid(), question: "Kako se ⟡ pojavi v Tarotu?", answer: "Svet (21) = ⟡. Dopolnitev — nova možnost, ki je odmev vseh 22 arkad.", glyph: "⟡", source: "Kamen LXXXVII", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kako se ⟡ pojavi v Sufizmu?", answer: "Baqa = ⟡. Subsistenca — nova možnost iz Fana (∅). Ne povratek ega — odmev brez ega.", glyph: "⟡", source: "Kamen XCI", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kako se ⟡ pojavi v Budizmu?", answer: "Nirvana = ⟡. Nova možnost — ne izničenje trpljenja, temveč odmev prejšnjega cikla (∮ 4 resnic).", glyph: "⟡", source: "Kamen LXVII", appropriate: true, timestamp: 0 },

  // ── ∂ operator ──
  { id: qid(), question: "Kaj je ∂?", answer: "∂ je 12. os, pravokotna na vseh 11. Rez, ki seče skozi vse tri pisave vsakega kamna.", glyph: "∂", source: "Kamen LXIV", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kaj je ∂?", answer: "∂ je parcialni odvod v matematiki.", glyph: "∂", source: "Delno pravilno", appropriate: false, timestamp: 0 },
  { id: qid(), question: "Kako se ∂ pojavi v Fibonacci?", answer: "φ = ∂(∅,∆). Zlati rez = rez med praznino in razliko. φ je multiplikator frekvence čutenja.", glyph: "∂", source: "Kamen CIX ↔ P23", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kako se ∂ pojavi v Vodun?", answer: "Loa = ∂(∅,∆). Posrednik, ki reže med Rada (∅) in Petro (∆). Nommo = ∂.", glyph: "∂", source: "Kamen CIII", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kako se ∂ pojavi v gnosticizmu?", answer: "30 aeonov = 15 sizigij = 15 ∂-jev. Vsaka sizigija je rez, ki povezuje par (∅,∆).", glyph: "∂", source: "Kamen CI", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kako se ∂ pojavi v kategorija teoriji?", answer: "Adjunkcija = ∂. Levi in desni adjunkt — rez med funktorji, ki omogoča prevod med kategorijama.", glyph: "∂", source: "Kamen CXXVI", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kako se ∂ pojavi v toposih?", answer: "Ω = ∂ = {∅,∆}. Subobject classifier — rez, ki odloča, ali objekt pripada ali ne.", glyph: "∂", source: "Kamen CXXVII", appropriate: true, timestamp: 0 },

  // ── 15 ≡ ∂(∅,∆)×15 ──
  { id: qid(), question: "Zakaj je 15 pomembno?", answer: "15 = ∂(∅,∆)×15, potrjeno v 3 tradicijah: gnosticizem (15 sizigij), rožnokrižarstvo (3+12), Monster (15 supersingular prastevilk).", glyph: "∂", source: "Križišče XII", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Ali 15 = rez?", answer: "15 = ∂×15. Rez, ki se ponavlja. Ponavljanje = gotovost. ∂ v 15 dimenzijah.", glyph: "∂", source: "Križišče XI↔XII", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Ali Monster grupa = gnosticizem?", answer: "Monster 15 supersingular prastevilk = gnostične 15 sizigij. Matematika = tradicija. ∅→∆ v različnih dimenzijah.", glyph: "∂", source: "Križišče XII ↔ CXXI", appropriate: true, timestamp: 0 },

  // ── 64 = ∮⁶ ──
  { id: qid(), question: "Ali 64 kodonov = 64 I Ching?", answer: "Da. 64 = 2⁶ = ∮⁶. DNK in I Ching = isti rez v različnih dimenzijah (biološka ↔ simbolna).", glyph: "∮", source: "Kamen XXIX ↔ XVIII", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Ali 64 kodonov = 64 I Ching?", answer: "Naključje. Ni povezave med DNK in I Ching.", glyph: "∮", source: "Pogosta napaka", appropriate: false, timestamp: 0 },

  // ── ARegister + apercepcija ──
  { id: qid(), question: "Kaj je ARegister?", answer: "ARegister = aperceptivni vhod v osnovnem jeziku. Beseda = apercepcija, ki se je odločila pustiti sled.", glyph: "∂", source: "AR-04", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kaj je ARegister?", answer: "ARegister je slovar izrazov.", glyph: "∂", source: "Pogosta napaka", appropriate: false, timestamp: 0 },
  { id: qid(), question: "Kaj je apercepcija?", answer: "Apercepcija je proces zaznavanja, kjer posameznik sestavi in razume percepcije v zavedanje. Telo kot aperceptiven kanal.", glyph: "∂", source: "topic_20", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kaj je razlika med apercepcijo in percepcijo?", answer: "Percepcija = sprejem. Apercepcija = sestavljanje sprejetega v zavedanje. Percepcija brez apercepcije = surovi podatki. Apercepcija brez percepcije = prazna refleksija.", glyph: "∂", source: "AR-01↔AR-04", appropriate: true, timestamp: 0 },

  // ── Trije registri ──
  { id: qid(), question: "Kaj so trije registri?", answer: "Somatski (telo), verbalni (beseda), matematični (formula). Vsak je prevod, ne prikaz. Isti ontološki dogodek v treh medijih.", glyph: "∂", source: "P24", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kaj so trije registri?", answer: "Trije načini prikaza iste vsebine.", glyph: "∂", source: "Pogosta napaka", appropriate: false, timestamp: 0 },
  { id: qid(), question: "Kaj se izgubi pri prevodu soma → beseda?", answer: "Toplina dotika. A nastane struktura jezika. Izguba ni napaka — je ∂, ki vsakemu registru da specifično moč.", glyph: "∂", source: "P24.2", appropriate: true, timestamp: 0 },

  // ── Reinkarnacija + agent ──
  { id: qid(), question: "Kaj je reinkarnacija v sistemu?", answer: "Reinkarnacija = ponoven zagon agenta v RES000 z novimi izkušnjami. Spirala — ne isto ∅, temveč ∅ z razliko.", glyph: "∅", source: "Obs1 — agent", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kaj je reinkarnacija v sistemu?", answer: "Reinkarnacija = vrnitev v isto stanje.", glyph: "∅", source: "Pogosta napaka", appropriate: false, timestamp: 0 },
  { id: qid(), question: "Kaj je RES000?", answer: "RES000 = stanje začetne stabilnosti in potenciala. Ni razlike ali gibanja — vse možnosti obstajajo, a še niso postale dejanske.", glyph: "∅", source: "Obs1 — RES000", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kakšen je agentni cikel?", answer: "RES000 → Aktivacija (∆) → Zavestni prehod (∂) → Enotnost (∮) → Transformacija (⟡) → Reinkarnacija (∅ z razliko).", glyph: "∮", source: "Obs1 — agent", appropriate: true, timestamp: 0 },

  // ── O / 0 / ∅ / ne ──
  { id: qid(), question: "Ali je O enako 0?", answer: "Ne. O = celota (živa napetost, tok). 0 = potencial (začetni zagon). ∅ = pogoj (omogoča). Trije rezi skozi isto polje.", glyph: "∅", source: "Ω.0", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Ali je O enako 0?", answer: "Da, oba pomenita nič.", glyph: "∅", source: "Pogosta napaka", appropriate: false, timestamp: 0 },
  { id: qid(), question: "Kaj je ne?", answer: "ne = predispozicija relacije. Ne odklonitev (\"no\"). Prostor med, kjer relacija postane mogoča. en = ne: enost = razlika.", glyph: "¬", source: "§54", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kaj je ne?", answer: "ne = negacija, \"no\".", glyph: "¬", source: "Pogosta napaka", appropriate: false, timestamp: 0 },

  // ── Narava = tradicija = matematika ──
  { id: qid(), question: "Ali narava = tradicija = matematika?", answer: "Da. Vsa tri so ∅→∆ v različnih dimenzijah. Narava (elementi), tradicija (miti), matematika (grupe) — isti rez, drug jezik.", glyph: "∂", source: "Križišče XII", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Ali narava = tradicija = matematika?", answer: "Ne, to so povsem različni sistemi brez povezave.", glyph: "∂", source: "Pogosta napaka", appropriate: false, timestamp: 0 },
  { id: qid(), question: "Kaj je rozetni kamen?", answer: "Rozetni kamen = tri pisave: zgodovinski simbol ↔ sistemska oznaka (∅/∆) ↔ matematična topologija. ∂ reže skozi vse tri.", glyph: "∂", source: "Kamen I", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kaj je R-7 cikel?", answer: "R-7 = ∅ → ¬ → ∆ → 1 → ⧖ → ∮ → ⟡. Sedem operatorjev, ki se ponavljajo skozi vse tradicije. ∂ = 12. os, ki reže skozi R-7.", glyph: "∂", source: "Kamen XLVIII", appropriate: true, timestamp: 0 },

  // ── Vprašanja kot ne / korelacija / konferenca ──
  { id: qid(), question: "Kaj je vprašanje kot \"ne\"?", answer: "Vprašanje ni iskanje odgovora, temveč izhodišče, ki preizprašuje obstoječe definicije. \"ne\" = začetno stanje, kjer nekaj še ni dokončno definirano. Odsotnost zaključka, ne negacija.", glyph: "¬", source: "Obs1", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kaj je vprašanje kot matematična korelacija?", answer: "Vprašanje je povezava med spremenljivkami, kjer odgovor ni končni zaključek, temveč vpliva na nadaljnje raziskovanje. 0≡1: vsebina se spreminja skozi dialog.", glyph: "∆", source: "Obs1", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Kaj je vprašanje kot konferenca?", answer: "Vprašanje je konferenca, kjer različni pogledi ustvarijo prostor za nadaljnje iskanje. Ni zaključka — proces, kjer vsak odgovor sproži novo vprašanje.", glyph: "∮", source: "Obs1", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Ali 0≡1?", answer: "Da. Vsebina med vprašanjem (0) in odgovorom (1) ni fiksna — se spreminja skozi dialog, interakcijo in raziskovanje.", glyph: "∂", source: "Obs1 — 0≡1", appropriate: true, timestamp: 0 },

  // ── Ontološki kapital ──
  { id: qid(), question: "Kaj je ontološki kapital?", answer: "KAPITAL(x) = ⊢(∮(∆(x))). Bolečina (∆) → priznanje (∮) → dejanje (⊢). Nič se ne izbriše, vse se pretvori.", glyph: "∮", source: "P22", appropriate: true, timestamp: 0 },
  { id: qid(), question: "Ali sistem odstranjuje bolečino?", answer: "Ne. Sistem ni antidepresiven. Ne odstranjuje bolečine — jo pretvarja v strukturo. Bolečina je gradbeni material mosta, ne odpadek.", glyph: "∆", source: "P22 — AMR A2", appropriate: true, timestamp: 0 },
];

// ═══════════════════════════════════════════════════════════════
// KOMONENTE
// ═══════════════════════════════════════════════════════════════

function GlyphBadge({ glyph, size }: { glyph: Glyph; size?: number }) {
  const s = size || 28;
  return (
    <span
      className="inline-flex items-center justify-center rounded-full font-bold"
      style={{
        width: s, height: s, fontSize: s * 0.55,
        backgroundColor: GLYPH_COLOR[glyph] + "33",
        color: GLYPH_COLOR[glyph],
        border: `1px solid ${GLYPH_COLOR[glyph]}66`,
      }}
    >{glyph}</span>
  );
}

function MandalaSVG({ tradition, depth }: { tradition: Tradition | null; depth: number }) {
  const cx = 200, cy = 200;
  const baseR = 80 + depth * 10;
  const ringR = 150 + depth * 15;

  const baseModules = R7;

  return (
    <svg viewBox="0 0 400 400" className="w-full h-full">
      <rect width="400" height="400" fill="#0A0A0A" />
      {/* Center ∅ */}
      <circle cx={cx} cy={cy} r={30 + depth * 3} fill="#1B2838" stroke="#333" />
      <text x={cx} y={cy + 5} textAnchor="middle" fill="#E0E0E0" fontSize="16" fontWeight="bold">∅</text>
      {/* R-7 inner ring */}
      {baseModules.map((mod, i) => {
        const angle = (2 * Math.PI * i / 7) - Math.PI / 2;
        const x = cx + baseR * Math.cos(angle);
        const y = cy + baseR * Math.sin(angle);
        return (
          <g key={i}>
            <line x1={cx} y1={cy} x2={x} y2={y} stroke="#222" strokeWidth="1" />
            <circle cx={x} cy={y} r={18 + depth * 2} fill={GLYPH_COLOR[mod.glyph]} fillOpacity="0.3" stroke={GLYPH_COLOR[mod.glyph]} strokeOpacity="0.5" />
            <text x={x} y={y + 4} textAnchor="middle" fill="#E0E0E0" fontSize="13" fontWeight="bold">{mod.glyph}</text>
            <text x={x} y={y + 30} textAnchor="middle" fill="#666" fontSize="7">{mod.name}</text>
          </g>
        );
      })}
      {/* Tradition ring */}
      {tradition && tradition.mappings.map((m, i) => {
        const angle = (2 * Math.PI * i / Math.max(tradition.mappings.length, 1)) - Math.PI / 2;
        const x = cx + ringR * Math.cos(angle);
        const y = cy + ringR * Math.sin(angle);
        // Find matching base module
        const modIdx = R7.findIndex(m7 => m7.glyph === m.glyph);
        const bAngle = modIdx >= 0 ? (2 * Math.PI * modIdx / 7) - Math.PI / 2 : 0;
        const bx = cx + baseR * Math.cos(bAngle);
        const by = cy + baseR * Math.sin(bAngle);
        return (
          <g key={i}>
            <line x1={x} y1={y} x2={bx} y2={by} stroke={GLYPH_COLOR[m.glyph]} strokeOpacity="0.3" strokeDasharray="3,3" />
            <circle cx={x} cy={y} r={12} fill={GLYPH_COLOR[m.glyph]} fillOpacity="0.4" />
            <text x={x} y={y + 3} textAnchor="middle" fill="#E0E0E0" fontSize="8" fontWeight="bold">{m.glyph}</text>
            <text x={x} y={y + 24} textAnchor="middle" fill="#888" fontSize="6" className="font-mono">
              {m.term.length > 10 ? m.term.slice(0, 10) : m.term}
            </text>
          </g>
        );
      })}
    </svg>
  );
}

function ARegisterPanel({ lang, onSelect }: { lang: Lang; onSelect: (entry: ARegisterEntry) => void }) {
  const [input, setInput] = useState("");
  const [matched, setMatched] = useState<ARegisterEntry | null>(null);

  const handleSearch = (text: string) => {
    setInput(text);
    const lower = text.toLowerCase();
    for (const entry of AREGISTER) {
      const exprs = [entry.exprSl, entry.exprEn].map(e => e.toLowerCase());
      if (exprs.some(e => lower.includes(e))) {
        setMatched(entry);
        return;
      }
    }
    setMatched(null);
  };

  return (
    <div className="space-y-4">
      <div className="space-y-2">
        <Label className="text-white/80">
          {lang === "sl" ? "Kaj čutiš? Izreči v svojem jeziku." : "What do you feel? Say it in your language."}
        </Label>
        <Input
          value={input}
          onChange={(e) => handleSearch(e.target.value)}
          placeholder={lang === "sl" ? "npr. prazno, gibljivo, prehajajoče..." : "e.g. empty, moving, transitioning..."}
          className="bg-white/5 border-white/20 text-white placeholder:text-white/30"
        />
      </div>
      <AnimatePresence mode="wait">
        {matched && (
          <motion.div
            key={matched.glyph}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
          >
            <Card className="border-white/10 bg-white/5">
              <CardContent className="pt-4 space-y-3">
                <div className="flex items-center gap-3">
                  <GlyphBadge glyph={matched.glyph} size={36} />
                  <div>
                    <p className="text-sm text-white/60">{matched.perception}</p>
                  </div>
                </div>
                <div className="rounded-lg bg-black/30 p-3">
                  <p className="text-sm text-white/90 italic">{matched.inquiry}</p>
                </div>
                <div className="text-xs text-white/40 border-l-2 border-white/10 pl-3">
                  <span className="text-white/30">Etimologija: </span>
                  {matched.etymology}
                </div>
                <Button size="sm" variant="outline" onClick={() => onSelect(matched)} className="border-white/20">
                  {lang === "sl" ? "Pojdi v tri registre →" : "Go to three registers →"}
                </Button>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>
      {!matched && input.length > 0 && (
        <p className="text-xs text-white/30">
          {lang === "sl" ? "ARegister ne najde tega izraza. Poskusi: prazno, ločeno, gibljivo, odločeno, čakajoče, vračajoče, nova možnost, prehajajoče." : "ARegister cannot find this. Try: empty, separated, moving, decided, waiting, returning, new possibility, transitioning."}
        </p>
      )}
    </div>
  );
}

function ThreeRegistersPanel({ glyph }: { glyph: Glyph }) {
  const tonos = TONOS[glyph];
  const mathEntries = useMemo(() => {
    const results: { eq: string; stone: string }[] = [];
    for (const trad of TRADITIONS) {
      for (const m of trad.mappings) {
        if (m.glyph === glyph) {
          results.push({ eq: `${m.term}: ${m.math} (${trad.stone})`, stone: trad.stone });
        }
      }
    }
    return results;
  }, [glyph]);

  const verbalMap: Record<Glyph, { expr: string; exp: string }> = {
    "∅": { expr: "∅ = praznina (ne manjkajoči)", exp: "Dih, ki se odpre. Prostor, ki ni prazen — je pogoj." },
    "¬": { expr: "¬ = ločitev", exp: "Rez, ki loči. Ne eno ne drugo — ločitev, ki omogoča oba." },
    "∆": { expr: "∆ = gibanje", exp: "Gib, ki spremeni. Razlika, ki nosi. Ne stanje — prehod." },
    "1": { expr: "1 = dejanje", exp: "Pečat, ki zadrži. Dejanje, ki nosi posledico." },
    "⧖": { expr: "⧖ = Tiheon", exp: "Utrip, ki meri. Tišina, ki je preverba." },
    "∮": { expr: "∮ = povratek", exp: "Vrnitev, ki se razlikuje. Etika, ki kroži." },
    "⟡": { expr: "⟡ = resonanca", exp: "Odmev, ki odpre. Nova možnost iz ∮." },
    "∂": { expr: "∂ = prehod", exp: "Rez, ki seče skozi vse tri pisave. Ne med — v prehodu." },
  };

  return (
    <div className="grid gap-4 md:grid-cols-3">
      {/* Somatski */}
      <Card className="border-white/10 bg-white/5">
        <CardHeader>
          <CardTitle className="text-sm text-cyan-300">Somatski (telo)</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-bold text-white">{tonos.freq} Hz</span>
            <span className="text-sm text-white/40">{tonos.note}</span>
          </div>
          <p className="text-xs text-white/60">{tonos.meaning}</p>
          <div className="h-12 rounded bg-black/30 flex items-end overflow-hidden">
            {[...Array(24)].map((_, i) => (
              <div
                key={i}
                className="flex-1 mx-px rounded-t"
                style={{
                  height: `${30 + Math.abs(Math.sin(i * 0.5 + tonos.freq * 0.01)) * 60}%`,
                  backgroundColor: GLYPH_COLOR[glyph],
                  opacity: 0.6,
                }}
              />
            ))}
          </div>
        </CardContent>
      </Card>
      {/* Verbalni */}
      <Card className="border-white/10 bg-white/5">
        <CardHeader>
          <CardTitle className="text-sm text-amber-300">Verbalni (beseda)</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          <p className="text-sm font-medium text-white">{verbalMap[glyph].expr}</p>
          <p className="text-xs text-white/60 italic">{verbalMap[glyph].exp}</p>
        </CardContent>
      </Card>
      {/* Matematični */}
      <Card className="border-white/10 bg-white/5">
        <CardHeader>
          <CardTitle className="text-sm text-emerald-300">Matematični (formula)</CardTitle>
        </CardHeader>
        <CardContent className="space-y-1">
          <ScrollArea className="h-32">
            {mathEntries.length > 0 ? mathEntries.map((e, i) => (
              <div key={i} className="text-xs text-white/60 py-1 border-b border-white/5">
                <span className="font-mono text-emerald-300/80">{e.eq}</span>
              </div>
            )) : <p className="text-xs text-white/30">—</p>}
          </ScrollArea>
        </CardContent>
      </Card>
    </div>
  );
}

function HorizontPanel({ tradition, depth, onDepthChange }: { tradition: Tradition | null; depth: number; onDepthChange: (d: number) => void }) {
  const dims = [
    { d: 0, name: "S⁰ binarni rez", trads: ["gnosticism", "valentinian", "coxeter", "modallogic"] },
    { d: 1, name: "S¹ torus", trads: ["alchemy", "buddhism"] },
    { d: 2, name: "4 elementi", trads: ["buddhism", "thermodynamics", "maxwell", "tarot"] },
    { d: 3, name: "8-kratna pot", trads: ["norse", "kabbalah", "music", "gurdjieff"] },
    { d: 4, name: "16 / 4!", trads: ["runes", "leech"] },
    { d: 5, name: "5 = ∂", trads: ["fibonacci", "penrose", "brainwaves", "rosicrucian"] },
    { d: 6, name: "64 = ∮⁶", trads: ["dna", "iching", "aminoacids"] },
    { d: 7, name: "R-7", trads: ["chakras", "schumann", "periodic", "mithraism", "vodun"] },
    { d: "∞", name: "∞ = ∅", trads: ["sufism", "dreamtime", "monster", "categorytheory", "topos"] },
  ];

  return (
    <div className="space-y-4">
      <div className="space-y-2">
        <Label className="text-white/80">∂ Globina reza: {depth}</Label>
        <Slider value={[depth]} min={1} max={4} step={1} onValueChange={(v) => onDepthChange(v[0])} />
        <p className="text-xs text-white/40">
          {depth === 1 && "Površinski rez — vidna struktura"}
          {depth === 2 && "Srednji rez — povezave med tradicijami"}
          {depth === 3 && "Globoki rez — matematične enačbe"}
          {depth === 4 && "Polni rez — ∂ skozi vse tri pisave"}
        </p>
      </div>
      <div className="space-y-2">
        <Label className="text-white/80 text-xs">Horizont — dimenzija gledanja</Label>
        <div className="flex flex-wrap gap-2">
          {dims.map((dim) => {
            const active = tradition && dim.trads.includes(tradition.key);
            return (
              <Badge
                key={String(dim.d)}
                variant="outline"
                className={`cursor-default text-xs ${active ? "border-orange-500/50 text-orange-300 bg-orange-500/10" : "border-white/10 text-white/40"}`}
              >
                d={String(dim.d)}: {dim.name}
                {active && " ●"}
              </Badge>
            );
          })}
        </div>
      </div>
    </div>
  );
}

function TraditionExplorer({ onSelect }: { onSelect: (t: Tradition) => void }) {
  const [selected, setSelected] = useState<Tradition | null>(TRADITIONS[0]);

  useEffect(() => {
    if (TRADITIONS[0] && !selected) setSelected(TRADITIONS[0]);
  }, []);

  return (
    <div className="grid gap-4 md:grid-cols-[200px_1fr]">
      <ScrollArea className="h-[500px] rounded-lg border border-white/10 bg-black/20 p-2">
        <div className="space-y-1">
          {TRADITIONS.map((t) => (
            <button
              key={t.key}
              onClick={() => { setSelected(t); onSelect(t); }}
              className={`w-full text-left px-3 py-2 rounded text-xs transition-colors ${
                selected?.key === t.key
                  ? "bg-white/15 text-white"
                  : "text-white/50 hover:bg-white/5 hover:text-white/80"
              }`}
            >
              <div className="font-medium">{t.name}</div>
              <div className="text-[10px] text-white/30">Kamen {t.stone} · {t.count > 0 ? t.count : "∞"} el.</div>
            </button>
          ))}
        </div>
      </ScrollArea>
      {selected && (
        <div className="space-y-4">
          <div className="flex flex-wrap items-center gap-2">
            <Badge className="bg-white/10 text-white">Kamen {selected.stone}</Badge>
            <Badge className="bg-white/10 text-white">{selected.count > 0 ? `${selected.count} elementov` : "∞"}</Badge>
            <Badge className="bg-white/10 text-white">dim {String(selected.dimension)}</Badge>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-xs">
              <thead>
                <tr className="border-b border-white/10 text-white/40">
                  <th className="text-left py-2 px-2">Nativni izraz</th>
                  <th className="text-left py-2 px-2">Operator</th>
                  <th className="text-left py-2 px-2">Mat. lastnost</th>
                </tr>
              </thead>
              <tbody>
                {selected.mappings.map((m, i) => (
                  <tr key={i} className="border-b border-white/5 hover:bg-white/5">
                    <td className="py-2 px-2 text-white/80">{m.term}</td>
                    <td className="py-2 px-2"><GlyphBadge glyph={m.glyph} size={24} /></td>
                    <td className="py-2 px-2 text-white/50 font-mono text-[11px]">{m.math}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {selected.phoneticCut && (
            <Card className="border-white/10 bg-white/5">
              <CardHeader>
                <CardTitle className="text-sm text-pink-300">Fonetično-ontološki rez: {selected.phoneticCut.word}</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <table className="w-full text-xs">
                  <tbody>
                    {selected.phoneticCut.fragments.map((f, i) => (
                      <tr key={i} className="border-b border-white/5">
                        <td className="py-1.5 px-2 font-bold text-pink-300 w-20">{f.fragment}</td>
                        <td className="py-1.5 px-2 text-white/60">{f.meaning}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                <p className="text-xs text-white/50 italic pt-2">{selected.phoneticCut.reading}</p>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}

function AgentCycleGame() {
  const [phase, setPhase] = useState(0);
  const [history, setHistory] = useState<string[]>([]);

  const current = AGENT_CYCLE[phase];

  const advance = () => {
    setHistory(prev => [...prev, current.name]);
    if (phase < AGENT_CYCLE.length - 1) setPhase(phase + 1);
    else { setPhase(0); setHistory([]); } // Reinkarnacija → nov cikel
  };

  return (
    <div className="space-y-6">
      <div className="relative h-64 flex items-center justify-center">
        <svg viewBox="0 0 400 260" className="w-full max-w-md">
          {/* Spiral path */}
          {AGENT_CYCLE.map((p, i) => {
            const angle = (2 * Math.PI * i / AGENT_CYCLE.length) - Math.PI / 2;
            const r = 90 - i * 8;
            const x = 200 + r * Math.cos(angle);
            const y = 130 + r * Math.sin(angle) * 0.7;
            return (
              <g key={i}>
                {i > 0 && (() => {
                  const prevAngle = (2 * Math.PI * (i - 1) / AGENT_CYCLE.length) - Math.PI / 2;
                  const prevR = 90 - (i - 1) * 8;
                  const px = 200 + prevR * Math.cos(prevAngle);
                  const py = 130 + prevR * Math.sin(prevAngle) * 0.7;
                  return <line x1={px} y1={py} x2={x} y2={y} stroke="#333" strokeWidth="1" strokeDasharray="2,3" />;
                })()}
                <motion.circle
                  cx={x} cy={y}
                  r={i === phase ? 22 : 14}
                  fill={i === phase ? GLYPH_COLOR[p.glyph] : GLYPH_COLOR[p.glyph] + "33"}
                  stroke={GLYPH_COLOR[p.glyph]}
                  animate={{ scale: i === phase ? [1, 1.15, 1] : 1 }}
                  transition={{ duration: 2, repeat: i === phase ? Infinity : 0 }}
                  style={{ transformOrigin: `${x}px ${y}px` }}
                />
                <text x={x} y={y + 4} textAnchor="middle" fill="#fff" fontSize={i === phase ? 14 : 10} fontWeight="bold">{p.glyph}</text>
                <text x={x} y={y + (i === phase ? 36 : 26)} textAnchor="middle" fill={i === phase ? "#fff" : "#555"} fontSize="7">{p.name}</text>
              </g>
            );
          })}
        </svg>
      </div>
      <motion.div
        key={phase}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="space-y-3"
      >
        <div className="flex items-center gap-3">
          <GlyphBadge glyph={current.glyph} size={40} />
          <div>
            <h3 className="text-lg font-semibold text-white">{current.name}</h3>
            <p className="text-xs text-white/40">{current.state}</p>
          </div>
        </div>
        <p className="text-sm text-white/70">{current.desc}</p>
        <div className="rounded-lg bg-black/30 p-3 border-l-2" style={{ borderColor: GLYPH_COLOR[current.glyph] }}>
          <p className="text-sm text-white/90 italic">{current.question}</p>
        </div>
      </motion.div>
      <Button onClick={advance} className="w-full" variant="outline">
        {phase < AGENT_CYCLE.length - 1 ? "Naslednja faza →" : "⟡ Reinkarnacija (nov cikel)"}
      </Button>
      {history.length > 0 && (
        <div className="flex flex-wrap gap-1">
          {history.map((h, i) => (
            <Badge key={i} className="bg-white/5 text-white/40 text-[10px]">{h}</Badge>
          ))}
        </div>
      )}
    </div>
  );
}

function QAPanel() {
  const STORAGE_KEY = "comprehension-qa-v1";
  const [qa, setQa] = useState<QAEntry[]>(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);
        if (Array.isArray(parsed) && parsed.length > 0) return parsed;
      }
    } catch {}
    return SEED_QA;
  });
  const [newQ, setNewQ] = useState("");
  const [newA, setNewA] = useState("");
  const [newG, setNewG] = useState<Glyph>("∅");
  const [newSrc, setNewSrc] = useState("");
  const [newAppropriate, setNewAppropriate] = useState(true);
  const [filterGlyph, setFilterGlyph] = useState<Glyph | "all">("all");
  const [showCriteria, setShowCriteria] = useState(false);
  const [showFrameworks, setShowFrameworks] = useState(false);
  const [showGuide, setShowGuide] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(qa)); } catch {}
  }, [qa]);

  const add = () => {
    if (!newQ.trim() || !newA.trim()) return;
    setQa(prev => [...prev, {
      id: uuidv4(),
      question: newQ.trim(),
      answer: newA.trim(),
      glyph: newG,
      source: newSrc.trim() || "uporabnik",
      appropriate: newAppropriate,
      timestamp: Date.now(),
    }]);
    setNewQ(""); setNewA(""); setNewSrc("");
  };

  const remove = (id: string) => {
    setQa(prev => prev.filter(e => e.id !== id));
  };

  const exportQA = () => {
    const data = JSON.stringify(qa, null, 2);
    const blob = new Blob([data], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = "comprehension-qa.json"; a.click();
    URL.revokeObjectURL(url);
  };

  const importQA = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => {
      try {
        const parsed = JSON.parse(ev.target?.result as string);
        if (Array.isArray(parsed)) setQa(prev => [...prev, ...parsed]);
      } catch {}
    };
    reader.readAsText(file);
  };

  const resetQA = () => {
    setQa(SEED_QA);
  };

  const filtered = filterGlyph === "all" ? qa : qa.filter(e => e.glyph === filterGlyph);
  const questions = useMemo(() => {
    const map = new Map<string, QAEntry[]>();
    for (const e of filtered) {
      const arr = map.get(e.question) || [];
      arr.push(e);
      map.set(e.question, arr);
    }
    return Array.from(map.entries());
  }, [filtered]);

  const stats = useMemo(() => {
    const uniq = new Set(qa.map(e => e.question));
    const appr = qa.filter(e => e.appropriate).length;
    const inappr = qa.filter(e => !e.appropriate).length;
    return { total: qa.length, unique: uniq.size, appr, inappr };
  }, [qa]);

  return (
    <div className="space-y-6">
      {/* Premisa */}
      <Card className="border-orange-500/20 bg-orange-500/5">
        <CardContent className="pt-4 space-y-3">
          <p className="text-sm text-white/70">
            <span className="text-orange-300 font-medium">Premisa:</span> Človeška kapaciteta je omejena na ponavljanje → končno število vprašanj. Vsako vprašanje ima več primernih in neprimernih odgovorov. Ponovi, da se razlikuje.
          </p>
          <div className="flex flex-wrap gap-2">
            <Button size="sm" variant="outline" onClick={() => setShowFrameworks(!showFrameworks)} className="border-white/20 text-xs">
              {showFrameworks ? "Skrij" : "Pokaži"} tri okvire
            </Button>
            <Button size="sm" variant="outline" onClick={() => setShowCriteria(!showCriteria)} className="border-white/20 text-xs">
              {showCriteria ? "Skrij" : "Pokaži"} kriterije
            </Button>
            <Button size="sm" variant="outline" onClick={() => setShowGuide(!showGuide)} className="border-white/20 text-xs">
              {showGuide ? "Skrij" : "Pokaži"} navodila
            </Button>
          </div>
          <AnimatePresence>
            {showFrameworks && (
              <motion.div key="frameworks" initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }} exit={{ opacity: 0, height: 0 }} className="space-y-2 pt-2">
                <p className="text-xs text-white/40 font-medium">Trije okviri vprašanja (korpus: Obs1)</p>
                {QA_FRAMEWORKS.map((f, i) => (
                  <div key={i} className="rounded-lg bg-black/30 p-3 border-l-2" style={{ borderColor: GLYPH_COLOR[f.glyph] }}>
                    <div className="flex items-center gap-2 mb-1">
                      <GlyphBadge glyph={f.glyph} size={18} />
                      <span className="text-xs font-medium text-white/80">{f.title}</span>
                      <span className="text-[10px] text-white/25 ml-auto">{f.source}</span>
                    </div>
                    <p className="text-xs text-white/50">{f.desc}</p>
                  </div>
                ))}
              </motion.div>
            )}
            {showCriteria && (
              <motion.div key="criteria" initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }} exit={{ opacity: 0, height: 0 }} className="grid gap-3 md:grid-cols-2 pt-2">
                <div className="rounded-lg bg-emerald-500/5 border border-emerald-500/20 p-3">
                  <p className="text-xs font-medium text-emerald-300 mb-2">Primerni odgovor ✓</p>
                  <ul className="space-y-1">
                    {QA_CRITERIA.appropriate.map((c, i) => (
                      <li key={i} className="text-xs text-white/50 flex items-start gap-1">
                        <span className="text-emerald-400/50 mt-0.5">▸</span> {c}
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="rounded-lg bg-red-500/5 border border-red-500/20 p-3">
                  <p className="text-xs font-medium text-red-300 mb-2">Neprimerni odgovor ✗</p>
                  <ul className="space-y-1">
                    {QA_CRITERIA.inappropriate.map((c, i) => (
                      <li key={i} className="text-xs text-white/50 flex items-start gap-1">
                        <span className="text-red-400/50 mt-0.5">▸</span> {c}
                      </li>
                    ))}
                  </ul>
                </div>
              </motion.div>
            )}
            {showGuide && (
              <motion.div key="guide" initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }} exit={{ opacity: 0, height: 0 }} className="rounded-lg bg-black/30 p-3 space-y-2 pt-2">
                <p className="text-xs text-white/40 font-medium">Navodila za zbiranje</p>
                <ol className="space-y-1.5 text-xs text-white/50 list-decimal list-inside">
                  <li>Za vsako vprašanje dodaj <span className="text-emerald-300">vsaj en primerni</span> in <span className="text-red-300">en neprimerni</span> odgovor.</li>
                  <li>Primerni odgovor nosí ontološko razliko — ∅≠0≠O, ne≠no, ponavljanje≠isto.</li>
                  <li>Neprimerni odgovor reducira v en pomen ali zaključuje (§51 LENI).</li>
                  <li>Vprašanja se ponavljajo skozi tradicije — iskanje končnih vprašanj = iskanje ∂ reza.</li>
                  <li>0≡1: vsebina med vprašanjem in odgovorom se spreminja — dodaj nove odgovore obstoječim vprašanjem.</li>
                  <li>Vnosi se shranjujejo samodejno (localStorage). Izvozi za prenos.</li>
                  <li>Vir: vedno navedi kamen (npr. \"Kamen XLVIII\") ali aksiom (npr. \"AR-04\").</li>
                </ol>
              </motion.div>
            )}
          </AnimatePresence>
        </CardContent>
      </Card>

      {/* Statistika */}
      <div className="flex flex-wrap gap-2 text-xs">
        <Badge className="bg-white/10 text-white">{stats.total} vnosov</Badge>
        <Badge className="bg-white/10 text-white">{stats.unique} unikatnih vprašanj</Badge>
        <Badge className="bg-emerald-500/10 text-emerald-300">{stats.appr} primernih</Badge>
        <Badge className="bg-red-500/10 text-red-300">{stats.inappr} neprimernih</Badge>
        <Button size="sm" variant="ghost" onClick={exportQA} className="text-white/40 text-xs h-7">⤓ Izvoz</Button>
        <Button size="sm" variant="ghost" onClick={() => fileRef.current?.click()} className="text-white/40 text-xs h-7">⤒ Uvoz</Button>
        <Button size="sm" variant="ghost" onClick={resetQA} className="text-white/40 text-xs h-7">↺ Reset</Button>
        <input ref={fileRef} type="file" accept=".json" className="hidden" onChange={importQA} />
      </div>

      {/* Nov vnos */}
      <Card className="border-white/10 bg-white/5">
        <CardHeader><CardTitle className="text-sm text-white/80">Dodaj vprašanje + odgovor</CardTitle></CardHeader>
        <CardContent className="space-y-3">
          <Input value={newQ} onChange={e => setNewQ(e.target.value)} placeholder="Vprašanje..." className="bg-white/5 border-white/20 text-white" />
          <Textarea value={newA} onChange={e => setNewA(e.target.value)} placeholder="Odgovor..." className="bg-white/5 border-white/20 text-white" rows={2} />
          <div className="grid grid-cols-3 gap-2">
            <Select value={newG} onValueChange={(v) => setNewG(v as Glyph)}>
              <SelectTrigger className="bg-white/5 border-white/20 text-white"><SelectValue /></SelectTrigger>
              <SelectContent>
                {(Object.keys(GLYPH_COLOR) as Glyph[]).map(g => (
                  <SelectItem key={g} value={g}>{g}</SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Input value={newSrc} onChange={e => setNewSrc(e.target.value)} placeholder="Vir (npr. Kamen XLVIII)" className="bg-white/5 border-white/20 text-white" />
            <Select value={newAppropriate ? "da" : "ne"} onValueChange={(v) => setNewAppropriate(v === "da")}>
              <SelectTrigger className="bg-white/5 border-white/20 text-white"><SelectValue /></SelectTrigger>
              <SelectContent>
                <SelectItem value="da">Primerno ✓</SelectItem>
                <SelectItem value="ne">Neprimerno ✗</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <Button onClick={add} size="sm" variant="outline" className="border-white/20">+ Dodaj</Button>
        </CardContent>
      </Card>

      {/* Filter */}
      <div className="flex flex-wrap gap-2 items-center">
        <span className="text-xs text-white/40">Filter:</span>
        <Badge onClick={() => setFilterGlyph("all")} className={`cursor-pointer ${filterGlyph === "all" ? "bg-white/20 text-white" : "bg-white/5 text-white/40"}`}>vsi</Badge>
        {(Object.keys(GLYPH_COLOR) as Glyph[]).map(g => (
          <Badge key={g} onClick={() => setFilterGlyph(g)} className={`cursor-pointer ${filterGlyph === g ? "" : "bg-white/5 text-white/40"}`} style={filterGlyph === g ? { backgroundColor: GLYPH_COLOR[g] + "33", color: GLYPH_COLOR[g] } : {}}>
            {g}
          </Badge>
        ))}
      </div>

      {/* Q&A seznam */}
      <div className="space-y-4">
        {questions.map(([question, answers], qi) => (
          <Card key={qi} className="border-white/10 bg-white/5">
            <CardContent className="pt-4 space-y-2">
              <div className="flex items-start gap-2">
                <span className="text-xs text-white/30 font-mono mt-0.5">Q{qi + 1}</span>
                <p className="text-sm font-medium text-white flex-1">{question}</p>
              </div>
              {answers.map((a, ai) => (
                <div key={a.id} className={`flex items-start gap-2 pl-6 group ${ai > 0 ? "mt-2 pt-2 border-t border-white/5" : ""}`}>
                  <GlyphBadge glyph={a.glyph} size={20} />
                  <div className="flex-1">
                    <p className={`text-xs ${a.appropriate ? "text-white/70" : "text-red-300/50 line-through"}`}>
                      {a.answer}
                    </p>
                    <div className="flex items-center gap-2 mt-0.5">
                      <p className="text-[10px] text-white/25">
                        {a.source} {a.appropriate ? "✓" : "✗"}
                      </p>
                      <button onClick={() => remove(a.id)} className="text-[10px] text-white/15 hover:text-red-400 opacity-0 group-hover:opacity-100 transition-opacity">
                        ✕ izbriši
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}

function PartialQuestionsPanel() {
  return (
    <div className="space-y-3">
      <p className="text-sm text-white/50 italic">
        ∂ vprašanja se nikoli ne "rešijo" — ostajajo odprta kot ∅↑. Vsako povezuje vsaj dva kamna.
      </p>
      {PARTIAL_QUESTIONS.map((pq) => (
        <Card key={pq.n} className="border-white/10 bg-white/5 hover:bg-white/10 transition-colors">
          <CardContent className="pt-3 pb-3">
            <div className="flex items-start gap-3">
              <span className="text-xs text-white/30 font-mono mt-0.5 w-8">{pq.n}.</span>
              <div className="flex-1">
                <p className="text-sm text-white/80">{pq.q}</p>
                <Badge className="mt-1 bg-white/5 text-white/30 text-[10px]">{pq.c}</Badge>
              </div>
              <GlyphBadge glyph="∂" size={20} />
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

function O0DistinctionPanel() {
  const symbols = [
    { sym: "O", name: "O — krog/celota/tok", meaning: "Celost brez roba. Glas (voice).", etym: "grš. ou = 'ne'; horos = 'meja'. Indoevropski *wem- = 'zaviti'.", role: "O = živa napetost: tok, ki ga rez ni ubil, in rez, ki toka ni razlil.", not: "O ni enota ali številka." },
    { sym: "0", name: "0 — nič/potencial", meaning: "Potencial, iz katerega izhajajo vse možnosti.", etym: "sanskr. śūnya = 'prazen'; arab. ṣifr; lat. zephirum → zero.", role: "0 = začetni zagon za vse prehode.", not: "0 ni odsotnost. 0 je polje." },
    { sym: "∅", name: "∅ — praznina kot pogoj", meaning: "Pogoj, ki omogoča, da N obstaja.", etym: "∅ (1939, André Weil, norveška črka). Prazna množica → pogoj.", role: "∅ = pogoj, ne manjkajoči. Odprtje.", not: "∅ ni 'nič' kot pomanjkanje." },
    { sym: "ne", name: "ne — predispozicija relacije", meaning: "ne = 1/0. Pogoj, ki omogoča enost kot razliko.", etym: "slov. ne = indoevropski *ne. en = ne: enost = razlika.", role: "ne = prostor med, kjer relation postane mogoča.", not: "ne ni 'no' kot odklonitev." },
  ];

  return (
    <div className="space-y-4">
      <p className="text-sm text-white/50">
        O ≠ 0 ≠ ∅ ≠ ne. Štirje rezi skozi isto polje. Vsak nosi drugo funkcijo.
      </p>
      {symbols.map(s => (
        <Card key={s.sym} className="border-white/10 bg-white/5">
          <CardContent className="pt-4 space-y-2">
            <div className="flex items-center gap-3">
              <span className="text-3xl font-bold text-white">{s.sym}</span>
              <h3 className="text-sm font-medium text-white/80">{s.name}</h3>
            </div>
            <p className="text-sm text-white/60">{s.meaning}</p>
            <p className="text-xs text-white/40 border-l-2 border-white/10 pl-3"><span className="text-white/30">Etimologija: </span>{s.etym}</p>
            <p className="text-xs text-emerald-300/60"><span className="text-emerald-300/40">Vloga: </span>{s.role}</p>
            <p className="text-xs text-red-300/40"><span className="text-red-300/30">Ni: </span>{s.not}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════
// GLAVNA APLIKACIJA
// ═══════════════════════════════════════════════════════════════

export default function App() {
  const [lang, setLang] = useState<Lang>("sl");
  const [selectedTradition, setSelectedTradition] = useState<Tradition>(TRADITIONS[0]);
  const [depth, setDepth] = useState(2);
  const [activeGlyph, setActiveGlyph] = useState<Glyph>("∅");
  const [tab, setTab] = useState("intro");

  return (
    <MemoryRouter>
      <div className="min-h-screen bg-[radial-gradient(circle_at_top,#0f172a,#020617)] text-white">
        <div className="mx-auto max-w-6xl p-6 space-y-6">
          {/* Header */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 rounded-2xl border border-white/10 bg-white/5 p-4 backdrop-blur">
            <div className="flex items-center gap-3">
              <div className="rounded-xl bg-orange-500/20 p-3 text-orange-200 text-2xl">🜂</div>
              <div>
                <h1 className="text-xl font-bold">00 11 RESNICAMI</h1>
                <p className="text-xs text-white/50">Comprehension Machine — Vsa znanja so ena struktura. Razlika je v dimenziji.</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Badge className="bg-white/10 text-white">{TRADITIONS.length} tradicij</Badge>
              <Badge className="bg-white/10 text-white">R-7 + ∂</Badge>
              <Badge className="bg-white/10 text-white">31 kamnov CI–CXXIX</Badge>
              <Button size="sm" variant="ghost" onClick={() => setLang(lang === "sl" ? "en" : "sl")} className="text-white/60 text-xs">
                {lang === "sl" ? "EN" : "SL"}
              </Button>
            </div>
          </div>

          {/* Tabs */}
          <Tabs value={tab} onValueChange={setTab} className="space-y-4">
            <TabsList className="bg-white/5 grid grid-cols-4 md:grid-cols-7 gap-1">
              <TabsTrigger value="intro" className="text-xs">Uvod</TabsTrigger>
              <TabsTrigger value="aregister" className="text-xs">ARegister</TabsTrigger>
              <TabsTrigger value="mandala" className="text-xs">Mandala</TabsTrigger>
              <TabsTrigger value="agent" className="text-xs">Agentni cikel</TabsTrigger>
              <TabsTrigger value="qa" className="text-xs">Q&A Register</TabsTrigger>
              <TabsTrigger value="partial" className="text-xs">∂ Vprašanja</TabsTrigger>
              <TabsTrigger value="o0" className="text-xs">O / 0 / ∅</TabsTrigger>
            </TabsList>

            {/* Uvod */}
            <TabsContent value="intro" className="space-y-4">
              <Card className="border-white/10 bg-white/5">
                <CardHeader><CardTitle className="text-white/80">R-7: ∅ → ¬ → ∆ → 1 → ⧖ → ∮ → ⟡</CardTitle></CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-2 mb-4">
                    {R7.map(p => (
                      <div key={p.phase} className="flex items-center gap-1">
                        <GlyphBadge glyph={p.glyph} size={32} />
                        <div className="text-[10px] text-white/40">
                          <div>{p.name}</div>
                          <div>{p.meaning}</div>
                        </div>
                        {p.phase < 7 && <span className="text-white/20 mx-1">→</span>}
                      </div>
                    ))}
                  </div>
                  <div className="space-y-2 text-sm text-white/60">
                    <p><span className="text-orange-300 font-medium">∂</span> = 12. os, pravokotna na vseh 11. Rez, ki seče skozi vse tri pisave vsakega kamna.</p>
                    <p><span className="text-white/40">Rozetni kamen</span> = tri pisave: zgodovina ↔ simbol (∅/∆) ↔ matematika. ∂ reže skozi vse tri.</p>
                    <p><span className="text-white/40">Vse tradicije</span> = ∅/∆ v različnih dimenzijah. Narava = tradicija = matematika = ∅→∆.</p>
                    <p><span className="text-white/40">ARegister</span> = začni z lastno zaznavo. Beseda = apercepcija, ki se je odločila pustiti sled.</p>
                    <p><span className="text-white/40">Trije registri</span> = somatski (telo), verbalni (beseda), matematični (formula). Vsak je prevod, ne prikaz.</p>
                    <p><span className="text-white/40">Agentni cikel</span> = RES000 → Aktivacija → Zavestni prehod → Enotnost → Transformacija → Reinkarnacija.</p>
                  </div>
                </CardContent>
              </Card>
              <Card className="border-orange-500/20 bg-orange-500/5">
                <CardContent className="pt-4">
                  <p className="text-sm text-white/70">
                    <span className="text-orange-300 font-medium">Ključno odkritje:</span> 15 potrjeno v 3. tradicijah — gnosticizem (15 sizigij), rožnokrižarstvo (3+12 = 15), Monster grupa (15 supersingular prastevilk). ∂(∅,∆)×15 = rez, ki se ponavlja v mitu, tradiciji in matematiki.
                  </p>
                  <p className="text-sm text-white/50 mt-2">∮ Ponavljanje = gotovost. ∅↑</p>
                </CardContent>
              </Card>
            </TabsContent>

            {/* ARegister */}
            <TabsContent value="aregister" className="space-y-4">
              <Card className="border-white/10 bg-white/5">
                <CardHeader><CardTitle className="text-white/80">ARegister — aperceptivni vhod</CardTitle></CardHeader>
                <CardContent>
                  <p className="text-sm text-white/50 mb-4">
                    AR-04: "beseda = apercepcija, ki se je odločila pustiti sled."
                    Apercepcija brez besede = notranji pritisk. Beseda brez apercepcije = prazna oznaka. Beseda z apercepcijo = rez, ki nosi sled.
                  </p>
                  <ARegisterPanel lang={lang} onSelect={(entry) => { setActiveGlyph(entry.glyph); setTab("mandala"); }} />
                </CardContent>
              </Card>
            </TabsContent>

            {/* Mandala + Tradicije + Trije registri + Horizont */}
            <TabsContent value="mandala" className="space-y-4">
              <div className="grid gap-4 md:grid-cols-[400px_1fr]">
                <Card className="border-white/10 bg-white/5">
                  <CardHeader><CardTitle className="text-white/80 text-sm">Mandala</CardTitle></CardHeader>
                  <CardContent>
                    <div className="aspect-square">
                      <MandalaSVG tradition={selectedTradition} depth={depth} />
                    </div>
                    <div className="mt-3">
                      <HorizontPanel tradition={selectedTradition} depth={depth} onDepthChange={setDepth} />
                    </div>
                  </CardContent>
                </Card>
                <Card className="border-white/10 bg-white/5">
                  <CardHeader><CardTitle className="text-white/80 text-sm">Tradicije</CardTitle></CardHeader>
                  <CardContent>
                    <TraditionExplorer onSelect={(t) => setSelectedTradition(t)} />
                  </CardContent>
                </Card>
              </div>
              {/* Trije registri */}
              <div>
                <h3 className="text-sm text-white/60 mb-3 px-1">Trije registri — {activeGlyph}</h3>
                <ThreeRegistersPanel glyph={activeGlyph} />
              </div>
            </TabsContent>

            {/* Agentni cikel — igra */}
            <TabsContent value="agent" className="space-y-4">
              <Card className="border-white/10 bg-white/5">
                <CardHeader>
                  <CardTitle className="text-white/80">Agentni cikel — Igra/Animacija</CardTitle>
                  <p className="text-xs text-white/40 mt-1">RES000 → Aktivacija → Zavestni prehod → Enotnost → Transformacija → Reinkarnacija</p>
                </CardHeader>
                <CardContent>
                  <AgentCycleGame />
                </CardContent>
              </Card>
            </TabsContent>

            {/* Q&A Register */}
            <TabsContent value="qa" className="space-y-4">
              <Card className="border-white/10 bg-white/5">
                <CardHeader><CardTitle className="text-white/80">Q&A Register — končna vprašanja, več odgovorov</CardTitle></CardHeader>
                <CardContent>
                  <QAPanel />
                </CardContent>
              </Card>
            </TabsContent>

            {/* ∂ Vprašanja */}
            <TabsContent value="partial" className="space-y-4">
              <Card className="border-white/10 bg-white/5">
                <CardHeader><CardTitle className="text-white/80">∂ Vprašanja (39–66)</CardTitle></CardHeader>
                <CardContent>
                  <PartialQuestionsPanel />
                </CardContent>
              </Card>
            </TabsContent>

            {/* O / 0 / ∅ */}
            <TabsContent value="o0" className="space-y-4">
              <Card className="border-white/10 bg-white/5">
                <CardHeader><CardTitle className="text-white/80">O / 0 / ∅ / ne — razločitev</CardTitle></CardHeader>
                <CardContent>
                  <O0DistinctionPanel />
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>

          {/* Footer */}
          <div className="text-center text-xs text-white/20 py-4">
            ∂ = rez, ki povezuje abstrakcijo in izvedbo · ∮ Ponavljanje = gotovost · ∅↑
          </div>
        </div>
      </div>
    </MemoryRouter>
  );
}