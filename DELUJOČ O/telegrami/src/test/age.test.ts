// =============================================================================
// TESTS: age.ts - Staranje telegramov
// =============================================================================

import { describe, it, expect } from 'vitest';
import { ageTelegram, shouldDie, ageAllTelegrams, isWMFull, getOverflowTelegram } from '../utils/age';
import { Telegram } from '../types';
import { CONFIG } from '../utils/constants';

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

describe('ageTelegram', () => {
  it('should increment age by 1', () => {
    const telegram = createTestTelegram({ age: 0 });
    const result = ageTelegram(telegram);
    expect(result.age).toBe(1);
  });

  it('should preserve all other properties', () => {
    const telegram = createTestTelegram({ id: 42, text: 'test', novelty: 0.9 });
    const result = ageTelegram(telegram);
    expect(result.id).toBe(42);
    expect(result.text).toBe('test');
    expect(result.novelty).toBe(0.9);
    expect(result.named).toBe(false);
  });
});

describe('shouldDie', () => {
  it('should return false for named telegram', () => {
    const telegram = createTestTelegram({ age: 10, named: true });
    expect(shouldDie(telegram)).toBe(false);
  });

  it('should return false for young unnamed telegram', () => {
    const telegram = createTestTelegram({ age: 2, named: false });
    expect(shouldDie(telegram)).toBe(false);
  });

  it('should return true for old unnamed telegram (age > 4)', () => {
    const telegram = createTestTelegram({ age: 5, named: false });
    expect(shouldDie(telegram)).toBe(true);
  });

  it('should respect custom maxAge parameter', () => {
    const telegram = createTestTelegram({ age: 3, named: false });
    expect(shouldDie(telegram, 2)).toBe(true); // age > 2
    expect(shouldDie(telegram, 4)).toBe(false); // age <= 4
  });
});

describe('ageAllTelegrams', () => {
  it('should age all telegrams', () => {
    const telegrams = [
      createTestTelegram({ age: 0 }),
      createTestTelegram({ age: 1 }),
    ];
    const result = ageAllTelegrams(telegrams);
    expect(result.survived[0].age).toBe(1);
    expect(result.survived[1].age).toBe(2);
    expect(result.died).toHaveLength(0);
  });

  it('should separate died telegrams', () => {
    const telegrams = [
      createTestTelegram({ age: 0, named: false }),
      createTestTelegram({ age: 5, named: false }), // should die
      createTestTelegram({ age: 6, named: false }), // should die
    ];
    const result = ageAllTelegrams(telegrams);
    expect(result.survived).toHaveLength(1);
    expect(result.died).toHaveLength(2);
    expect(result.died[0].age).toBe(6);
    expect(result.died[1].age).toBe(7);
  });

  it('should keep named telegrams alive', () => {
    const telegrams = [
      createTestTelegram({ age: 10, named: true }), // named, should survive
      createTestTelegram({ age: 5, named: false }), // should die
    ];
    const result = ageAllTelegrams(telegrams);
    expect(result.survived).toHaveLength(1);
    expect(result.survived[0].named).toBe(true);
    expect(result.died).toHaveLength(1);
    expect(result.died[0].named).toBe(false);
  });
});

describe('isWMFull', () => {
  it('should return false when WM is not full', () => {
    expect(isWMFull(0)).toBe(false);
    expect(isWMFull(3)).toBe(false);
  });

  it('should return true when WM is full', () => {
    expect(isWMFull(CONFIG.WM_CAPACITY)).toBe(true);
    expect(isWMFull(5)).toBe(true);
  });
});

describe('getOverflowTelegram', () => {
  it('should return null when WM is not full', () => {
    const telegrams = [
      createTestTelegram({ id: 1 }),
      createTestTelegram({ id: 2 }),
    ];
    expect(getOverflowTelegram(telegrams)).toBeNull();
  });

  it('should return first telegram when WM is full', () => {
    const telegrams = [
      createTestTelegram({ id: 1, text: 'first' }),
      createTestTelegram({ id: 2, text: 'second' }),
      createTestTelegram({ id: 3, text: 'third' }),
      createTestTelegram({ id: 4, text: 'fourth' }),
      createTestTelegram({ id: 5, text: 'fifth' }), // overflow
    ];
    const result = getOverflowTelegram(telegrams);
    expect(result?.id).toBe(1);
    expect(result?.text).toBe('first');
  });
});
