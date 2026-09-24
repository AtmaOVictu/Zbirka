// =============================================================================
// AGE: Staranje telegramov v delovnem spominu
// Koncept: Ne-poenovljeni žarki ugasnejo (Zeigarnik: odprte zanke drži pozornost)
// =============================================================================

import { CONFIG } from './constants';
import { Telegram } from '../types';

/**
 * Postari telegram za 1 korak
 */
export const ageTelegram = (telegram: Telegram): Telegram => ({
  ...telegram,
  age: telegram.age + 1,
});

/**
 * Preveri, ali telegram ugaša (ne-poenovljen + prestar)
 * @param telegram - Telegram, ki se preverja
 * @param maxAge - Maksimalna dovoljena starost (A1: Obseg pred - ekspliciten)
 */
export const shouldDie = (telegram: Telegram, maxAge: number = 4): boolean => {
  // Ugaša, če je prestar in ni bil poimenovan
  return telegram.age > maxAge && !telegram.named;
};

/**
 * Postari vse telegrame v delovnem spominu in vrne:
 * - preživele telegrame
 * - telegrame, ki so ugasnili (gredo v PRIMING)
 */
export const ageAllTelegrams = (
  telegrams: Telegram[],
  maxAge: number = 4
): { survived: Telegram[]; died: Telegram[] } => {
  const result = {
    survived: [] as Telegram[],
    died: [] as Telegram[],
  };

  telegrams.forEach((t) => {
    const aged = ageTelegram(t);
    if (shouldDie(aged, maxAge)) {
      result.died.push(aged);
    } else {
      result.survived.push(aged);
    }
  });

  return result;
};

/**
 * Preveri, ali je delovni spomin poln (kapaciteta = CONFIG.WM_CAPACITY)
 */
export const isWMFull = (wmLength: number): boolean => {
  return wmLength >= CONFIG.WM_CAPACITY;
};

/**
 * Če je WM poln, vrni prvega telegrama za izrinitev v PRIMING
 */
export const getOverflowTelegram = (telegrams: Telegram[]): Telegram | null => {
  if (telegrams.length <= CONFIG.WM_CAPACITY) {
    return null;
  }
  return telegrams[0]; // FIFO: prvi v, prvi ven
};
