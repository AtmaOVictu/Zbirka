// =============================================================================
// TESTS: consolidate.ts - Konsolidacija med spanjem (TMR)
// =============================================================================

import { describe, it, expect, beforeEach } from 'vitest';
import { consolidateMemory, createSleepLogMessage, isTMRCandidate } from '../utils/consolidate';
import { Telegram, CategoryKey } from '../types';

const createTestTelegram = (overrides: Partial<Telegram> = {}): Telegram => ({
  id: 1,
  text: 'test telegram',
  kind: 'rez',
  novelty: 0.5,
  age: 0,
  named: false,
  rep: 0,
  ...overrides,
});

const initialStored: Record<CategoryKey, string[]> = {
  epizodicni: [],
  semanticni: [],
  proceduralni: [],
  priming: [],
  delovni: [],
};

describe('consolidateMemory', () => {
  beforeEach(() => {
    // Resetuj stanje pred vsakim testom (A6: Protokol pred delom)
  });

  it('should move named telegrams to TMR and clear WM', () => {
    const wm = [
      createTestTelegram({ text: 'named1', named: true }),
      createTestTelegram({ text: 'named2', named: true }),
    ];
    
    const result = consolidateMemory(wm, initialStored);
    
    expect(result.newStored.epizodicni).toHaveLength(0); // Semanticni v originalni kodi
    expect(result.namedCount).toBe(2);
  });

  it('should move unnamed telegrams to PRIMING', () => {
    const wm = [
      createTestTelegram({ text: 'unnamed1', named: false }),
      createTestTelegram({ text: 'unnamed2', named: false }),
    ];
    
    const result = consolidateMemory(wm, initialStored);
    
    expect(result.newStored.priming).toContain('unnamed1');
    expect(result.newStored.priming).toContain('unnamed2');
    expect(result.namedCount).toBe(0);
  });

  it('should move half of episodic to semantic with ⌾ symbol', () => {
    const wm: Telegram[] = [];
    const storedWithEpisodic: Record<CategoryKey, string[]> = {
      ...initialStored,
      epizodicni: ['ep1', 'ep2', 'ep3', 'ep4'], // 4 epizodični
    };
    
    const result = consolidateMemory(wm, storedWithEpisodic);
    
    // Polovica (vsaki drugi) se pretoči v semantični
    expect(result.newStored.epizodicni).toHaveLength(2); // ep1, ep3
    expect(result.newStored.sematicni).toContain('ep2 ⌾');
    expect(result.newStored.sematicni).toContain('ep4 ⌾');
  });

  it('should handle empty WM', () => {
    const result = consolidateMemory([], initialStored);
    expect(result.newStored).toEqual(initialStored);
    expect(result.namedCount).toBe(0);
  });

  it('should preserve proceduralni', () => {
    const storedWithProcedural: Record<CategoryKey, string[]> = {
      ...initialStored,
      proceduralni: ['proc1', 'proc2'],
    };
    
    const result = consolidateMemory([], storedWithProcedural);
    expect(result.newStored.proceduralni).toEqual(['proc1', 'proc2']);
  });
});

describe('createSleepLogMessage', () => {
  it('should create correct message with counts', () => {
    const msg = createSleepLogMessage(4, 2);
    expect(msg).toContain('4 poimenovanih žarkov');
    expect(msg).toContain('TMR-oddajo');
    expect(msg).toContain('2 ne-poenovljenih → PRIMING');
    expect(msg).toContain('Rudoy 2009');
  });

  it('should handle zero counts', () => {
    const msg = createSleepLogMessage(0, 0);
    expect(msg).toContain('0 poimenovanih žarkov');
    expect(msg).toContain('0 ne-poenovljenih → PRIMING');
  });
});

describe('isTMRCandidate', () => {
  it('should return true for named telegram', () => {
    const telegram = createTestTelegram({ named: true });
    expect(isTMRCandidate(telegram)).toBe(true);
  });

  it('should return false for unnamed telegram', () => {
    const telegram = createTestTelegram({ named: false });
    expect(isTMRCandidate(telegram)).toBe(false);
  });
});
