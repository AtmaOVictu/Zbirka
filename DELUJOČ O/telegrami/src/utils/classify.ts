// =============================================================================
// CLASSIFY: Razvrščanje telegramov v spominske sisteme
// Koncept: Novost × Čudenje × Pozornost = odločitev o razvrščanju
// (Bunzeck & Düzel 2006; Takeuchi 2019)
// =============================================================================

import { CONFIG } from './constants';
import { Telegram, CategoryKey, AppState } from '../types';

/**
 * Razvrsti telegram v enega od spominskih sistemov
 * 
 * @param telegram - Telegram, ki se razvršča
 * @param utrujenost - 0-100: utrujenost (100 = popolna blokada pozornosti)
 * @param cudenje - 0-100: novostni detektor (100 = maksimalno čudenje)
 * @param nagrada - Ali je vklopljena nagrada (δ, dopamin)
 * @returns CategoryKey - Kategorija, v katero gre telegram
 * 
 * @example
 * // Telegram z visoko novostjo + niske utrujenost + nagrada = EPIZODIČNI
 * classifyTelegram(telegram, 0, 100, true) => 'epizodicni'
 */
export const classifyTelegram = (
  telegram: Telegram,
  utrujenost: number,
  cudenje: number,
  nagrada: boolean
): CategoryKey => {
  // Pozornost: (100 - utrujenost) / 100
  // Čim večja utrujenost, manjša pozornost
  const pozornost = (100 - utrujenost) / 100;
  
  // Dopamin bonus: +0.3, če je nagrada vklopljena in je ciljni žarek (∂)
  const dopamin = nagrada && telegram.goal ? CONFIG.DOPAMIN_BOOST : 0;
  
  // Formula: novOdkrita = novelty × (cudenje/100) × pozornost + dopamin
  const novOdkrita = 
    telegram.novelty * (cudenje / 100) * pozornost + dopamin;
  
  // Kritični prag (Zaves: sin θc = n₂/n₁)
  if (novOdkrita >= CONFIG.CRITICAL_THRESHOLD) {
    return 'epizodicni'; // Rezi — datirani, virani (hipokampus)
  }
  
  // Ponovitev brez novosti = proceduralni (bazalni gangliji)
  if (telegram.rep >= 1) {
    return 'proceduralni';
  }
  
  // Poimenovan, a brez novosti = semantični (korpus, tulvingovska delitev)
  return 'semanticni';
};

/**
 * Razvrsti telegram in vrne polno obrazložitev (za log)
 */
export const classifyWithReason = (
  telegram: Telegram,
  utrujenost: number,
  cudenje: number,
  nagrada: boolean
): { category: CategoryKey; reason: string; value: number } => {
  const pozornost = (100 - utrujenost) / 100;
  const dopamin = nagrada && telegram.goal ? CONFIG.DOPAMIN_BOOST : 0;
  const novOdkrita = telegram.novelty * (cudenje / 100) * pozornost + dopamin;
  
  if (novOdkrita >= CONFIG.CRITICAL_THRESHOLD) {
    return {
      category: 'epizodicni',
      reason: `novost × čudenje × pozornost = ${novOdkrita.toFixed(2)}${dopamin ? ' + δ' : ''}; novost sproži dopamin v hipokampusu → vztrajnost — Bunzeck & Düzel 2006, Takeuchi 2019`,
      value: novOdkrita,
    };
  }
  
  if (telegram.rep >= 1) {
    return {
      category: 'proceduralni',
      reason: 'ponovitev brez novosti → navada; bazalni gangliji, amnezija prizanese knowing-how — Squire',
      value: novOdkrita,
    };
  }
  
  return {
    category: 'semanticni',
    reason: 'poimenovan, a brez novosti: dejstvo, odtrgano od trenutka — tulvingovska delitev',
    value: novOdkrita,
  };
};

import { TELEGRAM_POOL } from './constants';

/**
 * Ustvari nov telegram iz pool-a
 * @param idGenerator - Funkcija za generiranje ID-jev (A4: Implicitni korak)
 */
export const createTelegram = (idGenerator: () => number): Telegram => {
  const randomIndex = Math.floor(Math.random() * TELEGRAM_POOL.length);
  const template = TELEGRAM_POOL[randomIndex];
  
  return {
    id: idGenerator(),
    ...template,
    age: 0,
    named: false,
    rep: 0,
  };
};
