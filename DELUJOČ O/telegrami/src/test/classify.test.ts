// =============================================================================
// TESTS: classify.ts - Razvrščanje telegramov
// =============================================================================

import { describe, it, expect, beforeEach } from 'vitest';
import { classifyTelegram, classifyWithReason } from '../utils/classify';
import { Telegram } from '../types';
import { CONFIG } from '../utils/constants';

// Testni telegrami
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

describe('classifyTelegram', () => {
  beforeEach(() => {
    // Resetuj vsa spremenljiva stanja pred testom (A6: Protokol pred delom)
  });

  describe('EPIZODIČNI razred', () => {
    it('should return epizodicni when novOdkrita >= 0.45', () => {
      const telegram = createTestTelegram({ novelty: 0.9 });
      const result = classifyTelegram(telegram, 0, 100, false);
      expect(result).toBe('epizodicni');
    });

    it('should return epizodicni with dopamin boost', () => {
      const telegram = createTestTelegram({ novelty: 0.3, goal: true });
      const result = classifyTelegram(telegram, 0, 100, true);
      // 0.3 * 1 * 1 + 0.3 = 0.6 >= 0.45
      expect(result).toBe('epizodicni');
    });

    it('should consider utrujenost (high utrujenost = low pozornost)', () => {
      const telegram = createTestTelegram({ novelty: 0.8 });
      const result = classifyTelegram(telegram, 90, 100, false);
      // pozornost = (100-90)/100 = 0.1
      // novOdkrita = 0.8 * 1 * 0.1 = 0.08 < 0.45
      expect(result).not.toBe('epizodicni');
    });
  });

  describe('PROCEDURALNI razred', () => {
    it('should return proceduralni when rep >= 1', () => {
      const telegram = createTestTelegram({ novelty: 0.3, rep: 1 });
      const result = classifyTelegram(telegram, 0, 100, false);
      expect(result).toBe('proceduralni');
    });

    it('should prioritize epizodicni over proceduralni when both conditions met', () => {
      const telegram = createTestTelegram({ novelty: 0.9, rep: 1 });
      const result = classifyTelegram(telegram, 0, 100, false);
      // novOdkrita = 0.9 * 1 * 1 = 0.9 >= 0.45 → epizodicni
      expect(result).toBe('epizodicni');
    });
  });

  describe('SEMANTIČNI razred', () => {
    it('should return semanticni when below threshold and rep = 0', () => {
      const telegram = createTestTelegram({ novelty: 0.3 });
      const result = classifyTelegram(telegram, 0, 50, false);
      // novOdkrita = 0.3 * 0.5 * 1 = 0.15 < 0.45
      expect(result).toBe('semanticni');
    });

    it('should return semanticni for low novelty with high cudenje but high utrujenost', () => {
      const telegram = createTestTelegram({ novelty: 0.5 });
      const result = classifyTelegram(telegram, 80, 100, false);
      // pozornost = 0.2, novOdkrita = 0.5 * 1 * 0.2 = 0.1 < 0.45
      expect(result).toBe('semanticni');
    });
  });

  describe('classifyWithReason', () => {
    it('should return category, reason, and value for epizodicni', () => {
      const telegram = createTestTelegram({ novelty: 0.9, goal: true });
      const result = classifyWithReason(telegram, 0, 100, true);
      
      expect(result.category).toBe('epizodicni');
      expect(result.reason).toContain('novost × čudenje × pozornost');
      expect(result.reason).toContain('+ δ');
      expect(result.value).toBeCloseTo(1.2, 1); // 0.9 * 1 * 1 + 0.3
    });

    it('should return correct reason for proceduralni', () => {
      const telegram = createTestTelegram({ rep: 1 });
      const result = classifyWithReason(telegram, 0, 100, false);
      
      expect(result.category).toBe('proceduralni');
      expect(result.reason).toContain('ponovitev brez novosti');
    });

    it('should return correct reason for semanticni', () => {
      const telegram = createTestTelegram({ novelty: 0.3 });
      const result = classifyWithReason(telegram, 0, 50, false);
      
      expect(result.category).toBe('semanticni');
      expect(result.reason).toContain('poimenovan, a brez novosti');
    });
  });
});
