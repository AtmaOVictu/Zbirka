// =============================================================================
// INTEGRATION TESTS: WorkingMemory.tsx
// Koncept: Testira delovni spomin (WM) UI
// =============================================================================

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { WorkingMemory } from '../components/WorkingMemory';
import { Telegram } from '../types';

describe('WorkingMemory Component', () => {
  const mockTelegrams: Telegram[] = [
    {
      id: 1,
      text: 'Visoko novost',
      kind: 'rez',
      novelty: 0.9,
      age: 0,
      named: false,
      rep: 0,
      goal: true,
    },
    {
      id: 2,
      text: 'Nizko novost',
      kind: 'korpus',
      novelty: 0.3,
      age: 2,
      named: false,
      rep: 0,
    },
    {
      id: 3,
      text: 'Star',
      kind: 'svet',
      novelty: 0.5,
      age: 4,
      named: false,
      rep: 0,
    },
  ];

  const mockOnName = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render section header', () => {
    render(<WorkingMemory telegrams={[]} onName={mockOnName} />);
    expect(screen.getByText('Delovni spomin — odprta ∂')).toBeInTheDocument();
  });

  it('should show count (length/capacity)', () => {
    render(<WorkingMemory telegrams={mockTelegrams} onName={mockOnName} />);
    expect(screen.getByText(/Delovni spomin — odprta ∂ \(3\/4\)/)).toBeInTheDocument();
  });

  it('should show empty message when no telegrams', () => {
    render(<WorkingMemory telegrams={[]} onName={mockOnName} />);
    expect(screen.getByText(/tok je prazen…/i)).toBeInTheDocument();
  });

  it('should render all telegrams', () => {
    render(<WorkingMemory telegrams={mockTelegrams} onName={mockOnName} />);
    expect(screen.getByText('Visoko novost')).toBeInTheDocument();
    expect(screen.getByText('Nizko novost')).toBeInTheDocument();
    expect(screen.getByText('Star')).toBeInTheDocument();
  });

  it('should show telegram metadata', () => {
    render(<WorkingMemory telegrams={mockTelegrams} onName={mockOnName} />);
    
    // Visoko novost telegram
    expect(screen.getByText(/novost 90%/)).toBeInTheDocument();
    expect(screen.getByText(/starost 0/)).toBeInTheDocument();
    expect(screen.getByText(/∂ cilj/)).toBeInTheDocument();
    
    // Nizko novost telegram
    expect(screen.getByText(/novost 30%/)).toBeInTheDocument();
    expect(screen.getByText(/starost 2/)).toBeInTheDocument();
  });

  it('should show ugaša indicator for old unnamed telegrams', () => {
    render(<WorkingMemory telegrams={mockTelegrams} onName={mockOnName} />);
    expect(screen.getByText(/ugaša…/)).toBeInTheDocument();
  });

  it('should call onName when telegram is clicked', () => {
    render(<WorkingMemory telegrams={mockTelegrams} onName={mockOnName} />);
    const button = screen.getByText('Visoko novost');
    fireEvent.click(button);
    expect(mockOnName).toHaveBeenCalledWith(mockTelegrams[0]);
  });

  it('should call onName when Enter key is pressed', () => {
    render(<WorkingMemory telegrams={mockTelegrams} onName={mockOnName} />);
    const button = screen.getByText('Visoko novost');
    fireEvent.keyDown(button, { key: 'Enter', code: 'Enter' });
    expect(mockOnName).toHaveBeenCalledWith(mockTelegrams[0]);
  });

  it('should call onName when Space key is pressed', () => {
    render(<WorkingMemory telegrams={mockTelegrams} onName={mockOnName} />);
    const button = screen.getByText('Visoko novost');
    fireEvent.keyDown(button, { key: ' ', code: 'Space' });
    expect(mockOnName).toHaveBeenCalledWith(mockTelegrams[0]);
  });

  it('should have proper accessibility attributes', () => {
    render(<WorkingMemory telegrams={mockTelegrams} onName={mockOnName} />);
    
    const buttons = screen.getAllByRole('button');
    expect(buttons).toHaveLength(3);
    
    buttons.forEach((button, index) => {
      expect(button).toHaveAttribute('tabindex', '0');
      expect(button).toHaveAttribute('aria-label', expect.stringContaining('Poimenuj telegram'));
    });
  });

  it('should apply correct styling based on novelty', () => {
    render(<WorkingMemory telegrams={mockTelegrams} onName={mockOnName} />);
    
    // High novelty should have amber styling
    const highNoveltyButton = screen.getByText('Visoko novost');
    expect(highNoveltyButton.className).toContain('amber');
    
    // Goal telegram should have fuchsia styling
    expect(highNoveltyButton.className).toContain('fuchsia');
  });

  it('should show Zeigarnik description', () => {
    render(<WorkingMemory telegrams={[]} onName={mockOnName} />);
    expect(screen.getByText(/Zeigarnik/)).toBeInTheDocument();
    expect(screen.getByText(/Kapaciteta štirih/)).toBeInTheDocument();
  });
});
