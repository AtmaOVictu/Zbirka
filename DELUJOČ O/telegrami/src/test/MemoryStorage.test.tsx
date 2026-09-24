// =============================================================================
// INTEGRATION TESTS: MemoryStorage.tsx
// Koncept: Testira shrambo spominskih sistemov
// =============================================================================

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryStorage } from '../components/MemoryStorage';
import { CategoryKey } from '../types';

describe('MemoryStorage Component', () => {
  const mockStored: Record<CategoryKey, string[]> = {
    epizodicni: ['Dogodek 1', 'Dogodek 2', 'Dogodek 3'],
    semanticni: ['Dejstvo 1', 'Dejstvo 2'],
    proceduralni: ['Navada 1'],
    priming: ['Implicitno 1', 'Implicitno 2', 'Implicitno 3', 'Implicitno 4'],
    delovni: [],
  };

  const mockTotal = 9;

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render section header with total count', () => {
    render(<MemoryStorage stored={mockStored} total={mockTotal} />);
    expect(screen.getByText(`Shramba — kam je padel vsak žarek (${mockTotal})`)).toBeInTheDocument();
  });

  it('should render all categories except delovni', () => {
    render(<MemoryStorage stored={mockStored} total={mockTotal} />);
    
    expect(screen.getByText('EPISODIČNI')).toBeInTheDocument();
    expect(screen.getByText('SEMANTIČNI')).toBeInTheDocument();
    expect(screen.getByText('PROCEDURALNI')).toBeInTheDocument();
    expect(screen.getByText('PRIMING')).toBeInTheDocument();
    
    // delovni should NOT be rendered
    expect(screen.queryByText('DELOVNI SPOMIN')).not.toBeInTheDocument();
  });

  it('should show correct count for each category', () => {
    render(<MemoryStorage stored={mockStored} total={mockTotal} />);
    
    expect(screen.getByText('3')).toBeInTheDocument(); // epizodicni
    expect(screen.getByText('2')).toBeInTheDocument(); // semanticni
    expect(screen.getByText('1')).toBeInTheDocument(); // proceduralni
    expect(screen.getAllByText('4')[0]).toBeInTheDocument(); // priming
  });

  it('should show category descriptions', () => {
    render(<MemoryStorage stored={mockStored} total={mockTotal} />);
    
    expect(screen.getByText(/rezi — datirani/)).toBeInTheDocument();
    expect(screen.getByText(/korpus — dejstvo/)).toBeInTheDocument();
    expect(screen.getByText(/obredi\/protokoli/)).toBeInTheDocument();
    expect(screen.getByText(/ONO — prejeto/)).toBeInTheDocument();
  });

  it('should show last 8 items for each category', () => {
    render(<MemoryStorage stored={mockStored} total={mockTotal} />);
    
    // epizodicni has 3 items
    expect(screen.getByText('Dogodek 1')).toBeInTheDocument();
    expect(screen.getByText('Dogodek 2')).toBeInTheDocument();
    expect(screen.getByText('Dogodek 3')).toBeInTheDocument();
    
    // semanticni has 2 items
    expect(screen.getByText('Dejstvo 1')).toBeInTheDocument();
    expect(screen.getByText('Dejstvo 2')).toBeInTheDocument();
  });

  it('should show flash animation for specified category', () => {
    const flash = { cat: 'epizodicni' as const, timestamp: Date.now() };
    render(<MemoryStorage stored={mockStored} total={mockTotal} flash={flash} />);
    
    const epizodicniElement = screen.getByText('EPISODIČNI').parentElement?.parentElement;
    expect(epizodicniElement?.className).toContain('ring-2');
  });

  it('should not show flash animation when flash is undefined', () => {
    render(<MemoryStorage stored={mockStored} total={mockTotal} />);
    
    const elements = screen.getAllByRole('generic');
    elements.forEach(el => {
      expect(el.className).not.toContain('ring-2');
    });
  });

  it('should have proper accessibility attributes', () => {
    render(<MemoryStorage stored={mockStored} total={mockTotal} />);
    
    const categories = screen.getAllByRole('generic');
    expect(categories.length).toBeGreaterThan(0);
    
    categories.forEach(cat => {
      expect(cat).toHaveAttribute('aria-label', expect.stringContaining('Kategorija'));
    });
  });
});
