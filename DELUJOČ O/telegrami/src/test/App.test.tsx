// =============================================================================
// INTEGRATION TESTS: App.tsx + Components
// Koncept: Testira celoten tok (React Testing Library + Vitest)
// =============================================================================

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { App } from '../App';
import { CONFIG } from '../utils/constants';

// Mock useMemory hook
vi.mock('../hooks/useMemory', () => ({
  useMemory: () => ({
    state: {
      utrujenost: 30,
      cudenje: 60,
      nagrada: false,
      running: true,
      wm: [
        {
          id: 1,
          text: 'Test telegram 1',
          kind: 'rez',
          novelty: 0.9,
          age: 0,
          named: false,
          rep: 0,
          goal: true,
        },
        {
          id: 2,
          text: 'Test telegram 2',
          kind: 'korpus',
          novelty: 0.5,
          age: 1,
          named: false,
          rep: 0,
        },
      ],
      stored: {
        epizodicni: [],
        semanticni: ['Semantični test'],
        proceduralni: [],
        priming: ['Priming test'],
        delovni: [],
      },
      log: [
        { id: 1, msg: 'Test log 1', tone: 'text-zinc-600' },
        { id: 2, msg: 'Test log 2', tone: 'text-amber-700' },
      ],
      flash: undefined,
    },
    setUtrujenost: vi.fn(),
    setCudenje: vi.fn(),
    toggleNagrada: vi.fn(),
    toggleRunning: vi.fn(),
    nameTelegram: vi.fn(),
    sleep: vi.fn(),
    totalStored: 2,
  }),
}));

// Mock Zaves component (to avoid DOM issues)
vi.mock('../components/Zaves', () => ({
  Zaves: ({ telegramsProcessed, isActive }: { telegramsProcessed: number; isActive?: boolean }) => (
    <div data-testid="zaves" data-processed={telegramsProcessed} data-active={isActive} />
  ),
}));

describe('App Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render the main header', () => {
    render(<App />);
    expect(screen.getByText('TELEGRAMI — simulacija spominskih sistemov')).toBeInTheDocument();
  });

  it('should render Controls section', () => {
    render(<App />);
    expect(screen.getByText('Detektorja (rez 62 + rez 63)')).toBeInTheDocument();
    expect(screen.getByLabelText('Utrujenost (pozornostna vrata):')).toBeInTheDocument();
    expect(screen.getByLabelText('Čudenje (novostni detektor):')).toBeInTheDocument();
  });

  it('should render WorkingMemory with telegrams', () => {
    render(<App />);
    expect(screen.getByText('Delovni spomin — odprta ∂')).toBeInTheDocument();
    expect(screen.getByText('Test telegram 1')).toBeInTheDocument();
    expect(screen.getByText('Test telegram 2')).toBeInTheDocument();
  });

  it('should render MemoryStorage with categories', () => {
    render(<App />);
    expect(screen.getByText('Shramba — kam je padel vsak žarek')).toBeInTheDocument();
    expect(screen.getByText('EPISODIČNI')).toBeInTheDocument();
    expect(screen.getByText('SEMANTIČNI')).toBeInTheDocument();
    expect(screen.getByText('PRIMING')).toBeInTheDocument();
    expect(screen.getByText('PROCEDURALNI')).toBeInTheDocument();
  });

  it('should render EventLog with entries', () => {
    render(<App />);
    expect(screen.getByText('Dnevnik klasifikacij')).toBeInTheDocument();
    expect(screen.getByText('· Test log 1')).toBeInTheDocument();
    expect(screen.getByText('· Test log 2')).toBeInTheDocument();
  });

  it('should render ResearchReferences', () => {
    render(<App />);
    expect(screen.getByText('Raziskovalna podlaga')).toBeInTheDocument();
    expect(screen.getByText('Squire')).toBeInTheDocument();
  });

  it('should render Zaves component', () => {
    render(<App />);
    expect(screen.getByTestId('zaves')).toBeInTheDocument();
  });

  it('should display correct working memory count', () => {
    render(<App />);
    expect(screen.getByText(/Delovni spomin — odprta ∂ \(2\/4\)/)).toBeInTheDocument();
  });

  it('should display total stored count', () => {
    render(<App />);
    expect(screen.getByText('Shramba — kam je padel vsak žarek (2)')).toBeInTheDocument();
  });

  it('should have proper accessibility attributes', () => {
    render(<App />);
    
    // Utrujenost slider
    const utrujenostSlider = screen.getByLabelText('Nastavi utrujenost');
    expect(utrujenostSlider).toHaveAttribute('type', 'range');
    
    // Čudenje slider
    const cudenjeSlider = screen.getByLabelText('Nastavi čudenje');
    expect(cudenjeSlider).toHaveAttribute('type', 'range');
  });
});
