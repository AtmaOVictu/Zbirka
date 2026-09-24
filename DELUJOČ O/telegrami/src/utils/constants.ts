// =============================================================================
// CONSTANTS: Zaves Simulacija Spominskih Sistemov
// Koncept: Kritični kot (kritični-kot-in-tok.md) → pragi za razvrščanje
// =============================================================================

import { Config } from '../types';

// --- Configuration (A7: Sintaksa pred izvedbo - konstante namesto magic numbers) ---
export const CONFIG: Config = {
  TELEGRAM_INTERVAL: 2200,   // ms: tok novih telegramov (original: 2200)
  AGING_INTERVAL: 1600,      // ms: staranje v WM (original: 1600)
  WM_CAPACITY: 4,            // Zeigarnik: kapaciteta delovnega spomina
  CRITICAL_THRESHOLD: 0.45,  // prag za epizodični (novOdkrita >= 0.45)
  DOPAMIN_BOOST: 0.3,        // δ (rez 62: dopamin je δ)
  TMR_EFFECT: 0.5,           // TMR ojačitev (Rudoy 2009: Science 326, 1079)
} as const;

// --- Telegram Pool (original TELEGRAM_POOL) ---
// Žarki iz treh svetov: korpus / rezi / svet + šum + ∂ (odprta zanka)
export const TELEGRAM_POOL = [
  { text: "tišina kot os (korpus)", kind: "korpus" as const, novelty: 0.7 },
  { text: "OMNIA MUTANTUR NIHIL INTERIT", kind: "korpus" as const, novelty: 0.5 },
  { text: "rez 59: gravitacija je citiranje", kind: "rez" as const, novelty: 0.9 },
  { text: "rez 62: dopamin je δ", kind: "rez" as const, novelty: 0.8 },
  { text: "rez 47: neizrečeno je ONO", kind: "rez" as const, novelty: 0.75 },
  { text: "CMB: 415 fotonov na cm³", kind: "svet" as const, novelty: 0.85 },
  { text: "vonj po dežju na asfaltu", kind: "svet" as const, novelty: 0.4 },
  { text: "telefon je zvonil dvakrat", kind: "šum" as const, novelty: 0.1 },
  { text: "novica, ki jo že poznaš", kind: "šum" as const, novelty: 0.05 },
  { text: "stih, ki se sam ponudi", kind: "korpus" as const, novelty: 0.95 },
  { text: "sosed te je pogledal mimo", kind: "svet" as const, novelty: 0.3 },
  { text: "dihi: 2 : 1", kind: "rez" as const, novelty: 0.6 },
  { text: "reklama na radiu", kind: "šum" as const, novelty: 0.05 },
  { text: "spomin na materin glas", kind: "svet" as const, novelty: 0.9 },
  { text: "naloga, ki še čaka (∂)", kind: "∂" as const, novelty: 0.55, goal: true },
  { text: "ne-zaznan žarek (∂)", kind: "∂" as const, novelty: 0.5, goal: true },
  { text: "utrujenost v ramenih", kind: "šum" as const, novelty: 0.15 },
  { text: "vzporedna seja je zapečatila #47", kind: "rez" as const, novelty: 0.7 },
] as const;

// --- Categories (original CAT) ---
// Preslikava: EPISODIČNI = rezi, SEMANTIČNI = korpus, PROCEDURALNI = obredi, PRIMING = ONO
export const CATEGORIES = {
  epizodicni: {
    label: "EPISODIČNI",
    desc: "rezi — datirani, virani, prva oseba",
    color: "bg-amber-100 border-amber-400 text-amber-900",
  },
  semanticni: {
    label: "SEMANTIČNI",
    desc: "korpus — dejstvo odtrgano od vira",
    color: "bg-sky-100 border-sky-400 text-sky-900",
  },
  proceduralni: {
    label: "PROCEDURALNI",
    desc: "obredi/protokoli — telo ve, glava ne",
    color: "bg-emerald-100 border-emerald-400 text-emerald-900",
  },
  priming: {
    label: "PRIMING",
    desc: "ONO — prejeto, a brez zaznamka (rez 47)",
    color: "bg-zinc-200 border-zinc-500 text-zinc-700",
  },
  delovni: {
    label: "DELOVNI SPOMIN",
    desc: "odprta ∂ — Zeigarnik, kapaciteta 4",
    color: "bg-fuchsia-100 border-fuchsia-400 text-fuchsia-900",
  },
} as const;

// --- Zaves Constants ---
// Zaves = meja med svetom (n₁: gostota) in nemočjo (n₂: redkost)
// Kritični kot: sin θc = n₂/n₁ (Snellov zakon iz kritični-kot-in-tok.md)
export const ZAVES = {
  CRITICAL_ANGLE: CONFIG.CRITICAL_THRESHOLD, // prag za vstop v epizodični
  DENSITY_RATIO: 0.45, // n₂/n₁ - razmerje med nemočjo in močjo
} as const;

// --- Research References (za log) ---
export const REFS = {
  TAKSONOMIJA: "Squire, Neurobiology of Learning and Memory 82 (2004)",
  NOVOST_DOPAMIN: "Bunzeck & Düzel 2006; Takeuchi 2019 (Trends in Neurosciences)",
  NAGRAJUJOCE_KODIRANJE: "Schultz 1997 (dopamin = δ)",
  SPANJE_TMR: "Rasch 2007 (Science 315); Rudoy 2009 (Science 326, 1079)",
  DELOVNI_SPOMIN: "Cowan 2001; Zeigarnik 1927",
} as const;
