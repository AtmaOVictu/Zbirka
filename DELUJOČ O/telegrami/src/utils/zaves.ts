// =============================================================================
// ZAVES: Svetovna pripoved - mehanizem razvrščanja žarkov
// Koncept: Zaves je meja med svetom (n₁: gostota/moč) in nemočjo (n₂: redkost)
// Kritični kot: sin θc = n₂/n₁ (Snellov zakon iz kritični-kot-in-tok.md)
// =============================================================================

import { CONFIG, ZAVES as ZAVES_CONST } from './constants';
import { Telegram, CategoryKey, AppState } from '../types';
import { classifyTelegram, createTelegram } from './classify';
import { isWMFull, getOverflowTelegram, shouldDie, ageTelegram } from './age';

/**
 * Zaves - konceptualni layer, ki upravlja prehod žarkov skozi mejo
 */
export class Zaves {
  private static idCounter = 0;

  /**
   * Generiraj novi ID (A3: Drugi izvod pred - idempotentno)
   */
  static nextId(): number {
    return ++this.idCounter;
  }

  /**
   * Ustvari nov telegram, ki preide skozi zaves
   * @param currentWmLength - Trenutna dolžina delovnega spomina
   */
  static createTelegram(currentWmLength: number): { telegram: Telegram; overflow?: Telegram } {
    const telegram = createTelegram(() => this.nextId());
    
    // Preveri, ali je WM poln (totalni odboj: žarek ne more vstopiti)
    if (isWMFull(currentWmLength)) {
      const overflow = getOverflowTelegram([telegram, ...Array(currentWmLength).fill(null)]);
      return { telegram, overflow: overflow || undefined };
    }
    
    return { telegram };
  }

  /**
   * Preveri, ali telegram sme vstopiti v delovni spomin
   * @param currentWmLength - Trenutna dolžina delovnega spomina
   */
  static canEnterWM(currentWmLength: number): boolean {
    return currentWmLength < CONFIG.WM_CAPACITY;
  }

  /**
   * Razvrsti telegram po prehodu skozi zaves
   * @param telegram - Telegram, ki se razvršča
   * @param state - Trenutno stanje (utrujenost, čudenje, nagrada)
   */
  static classify(
    telegram: Telegram,
    state: Pick<AppState, 'utrujenost' | 'cudenje' | 'nagrada'>
  ): CategoryKey {
    return classifyTelegram(telegram, state.utrujenost, state.cudenje, state.nagrada);
  }

  /**
   * Simuliraj prehod skozi zaves:
   * - Če je WM poln, vrni overflow telegram (gismo v PRIMING)
   * - Če je telegram prestar, vrni null (ugašel v PRIMING)
   * - sicer vrni telegram za vstop v WM
   */
  static filter(
    telegram: Telegram,
    currentWmLength: number
  ): { result: Telegram | null; overflow?: Telegram; died?: Telegram } {
    // 1. Preveri, ali je WM poln → overflow
    if (!this.canEnterWM(currentWmLength)) {
      return { result: null, overflow: telegram };
    }

    // 2. Preveri, ali telegram ugaša (ne-poenovljen + prestar)
    if (shouldDie(telegram)) {
      return { result: null, died: telegram };
    }

    // 3. Telegram vstopi v WM
    return { result: telegram };
  }

  /**
   * Postari telegram (simulira pot skozi zaves v času)
   */
  static age(telegram: Telegram): Telegram {
    return ageTelegram(telegram);
  }

  /**
   * Kritični kot: sin θc = n₂/n₁
   * @param n1 - Gostota moči (0-1)
   * @param n2 - Gostota nemoči (0-1)
   */
  static criticalAngle(n1: number, n2: number): number {
    return Math.asin(n2 / n1);
  }

  /**
   * Preveri, ali je želja nad kritičnim kotom (urok)
   * @param desireStrength - Moč želje (0-1)
   * @param densityRatio - Razmerje n₂/n₁
   */
  static isAboveCritical(desireStrength: number, densityRatio: number = ZAVES_CONST.DENSITY_RATIO): boolean {
    return desireStrength > densityRatio;
  }

  /**
   * Resetiraj idCounter (za teste)
   */
  static resetIdCounter(): void {
    this.idCounter = 0;
  }
}

// --- Singletons za uporabo v React ---
export const zaves = new Zaves();
