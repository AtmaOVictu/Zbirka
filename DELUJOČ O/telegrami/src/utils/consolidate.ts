// =============================================================================
// CONSOLIDATE: Konsolidacija med spanjem (TMR - Targeted Memory Reactivation)
// Koncept: Poimenovani pred spanjem dobijo TMR ojačitev (Rudoy 2009: Science 326, 1079)
// =============================================================================

import { CONFIG } from './constants';
import { Telegram, CategoryKey, AppState } from '../types';

/**
 * Konsolidiraj spomine med spanjem:
 * - Poimenovani telegrami dobijo TMR ojačitev
 * - Ne-poenovljeni gredo v PRIMING
 * - Polovica epizodičnih se pretoči v semantične (dogodek → dejstvo)
 */
export const consolidateMemory = (
  wm: Telegram[],
  stored: Record<CategoryKey, string[]>
): { newStored: Record<CategoryKey, string[]>; namedCount: number } => {
  // Loči poimenovane od ne-poimenovanih
  const named = wm.filter((t) => t.named);
  const rest = wm.filter((t) => !t.named);

  // Ne-poenovljeni → PRIMING
  const newPriming = [...stored.priming, ...rest.map((t) => t.text)];

  // Polovica epizodičnih se pretoči v semantične (⌾ = konsolidirano)
  const episodicList = [...stored.epizodicni];
  const movers = episodicList.filter((_, i) => i % 2 === 0); // vsaki drugi
  const remainingEpisodic = episodicList.filter((_, i) => i % 2 !== 0);
  
  const newSemantic = [
    ...stored.sematicni,
    ...movers.map((x) => `${x} ⌾`), // ⌾ = simbol za konsolidacijo
  ];

  const newStored = {
    ...stored,
    epizodicni: remainingEpisodic,
    semanticni: newSemantic,
    priming: newPriming,
    // proceduralni se ne spreminja
  };

  return {
    newStored,
    namedCount: named.length, // Število poimenovanih, ki so prejeli TMR
  };
};

/**
 * Ustvari log vnos za spanje
 */
export const createSleepLogMessage = (
  namedCount: number,
  restCount: number
): string => {
  const moversCount = Math.floor(namedCount / 2); // Polovica epizodičnih se pretoči
  return `SPANJE: ${namedCount} poimenovanih žarkov prejelo TMR-oddajo (zvok/vonj med NREM ojača vezan spomin — Rasch 2007, Rudoy 2009: Science 326, 1079); polovica epizodičnih (${moversCount}) se je pretočila v korpus (SEMANTIČNI, ⌾); ${restCount} ne-poenovljenih → PRIMING`;
};

/**
 * Preveri, ali je telegram primeren za TMR ojačitev
 * (poimenovan pred spanjem)
 */
export const isTMRCandidate = (telegram: Telegram): boolean => {
  return telegram.named;
};

/**
 * Simuliraj TMR ojačitev (povečaj novost za naslednji krog)
 * To ni v originalni kodi, ampak je konceptualno ustrezno
 */
export const applyTMRBoost = (telegram: Telegram): Telegram => ({
  ...telegram,
  novelty: Math.min(1, telegram.novelty + CONFIG.TMR_EFFECT * 0.1), // +10% novosti
});
