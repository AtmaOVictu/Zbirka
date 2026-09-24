// =============================================================================
// INTEGRATION TESTS: Controls.tsx
// Koncept: Testira kontrolne elemente (sliders, buttons)
// =============================================================================

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { Controls } from '../components/Controls';

describe('Controls Component', () => {
  const mockProps = {
    utrujenost: 30,
    cudenje: 60,
    nagrada: false,
    running: true,
    onSetUtrujenost: vi.fn(),
    onSetCudenje: vi.fn(),
    onToggleNagrada: vi.fn(),
    onToggleRunning: vi.fn(),
    onSleep: vi.fn(),
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render all control labels', () => {
    render(<Controls {...mockProps} />);
    
    expect(screen.getByText('Detektorja (rez 62 + rez 63)')).toBeInTheDocument();
    expect(screen.getByText(/Utrujenost.*30%/)).toBeInTheDocument();
    expect(screen.getByText(/Čudenje.*60%/)).toBeInTheDocument();
  });

  it('should render range inputs with correct values', () => {
    render(<Controls {...mockProps} />);
    
    const utrujenostSlider = screen.getByLabelText('Nastavi utrujenost');
    expect(utrujenostSlider).toHaveAttribute('type', 'range');
    expect(utrujenostSlider).toHaveValue('30');
    
    const cudenjeSlider = screen.getByLabelText('Nastavi čudenje');
    expect(cudenjeSlider).toHaveAttribute('type', 'range');
    expect(cudenjeSlider).toHaveValue('60');
  });

  it('should call onSetUtrujenost when utrujenost slider changes', () => {
    render(<Controls {...mockProps} />);
    const slider = screen.getByLabelText('Nastavi utrujenost');
    fireEvent.change(slider, { target: { value: '50' } });
    expect(mockProps.onSetUtrujenost).toHaveBeenCalledWith(50);
  });

  it('should call onSetCudenje when cudenje slider changes', () => {
    render(<Controls {...mockProps} />);
    const slider = screen.getByLabelText('Nastavi čudenje');
    fireEvent.change(slider, { target: { value: '80' } });
    expect(mockProps.onSetCudenje).toHaveBeenCalledWith(80);
  });

  it('should render Nagrada button with correct state', () => {
    render(<Controls {...mockProps} />);
    const button = screen.getByText(/NAGRADA δ/);
    expect(button).toBeInTheDocument();
    expect(button).toHaveTextContent('izklopljena');
  });

  it('should render Nagrada button as enabled when nagrada is true', () => {
    render(<Controls {...mockProps} nagrada={true} />);
    const button = screen.getByText(/NAGRADA δ/);
    expect(button).toHaveTextContent('VKLOPLJENA');
  });

  it('should call onToggleNagrada when Nagrada button is clicked', () => {
    render(<Controls {...mockProps} />);
    const button = screen.getByText(/NAGRADA δ/);
    fireEvent.click(button);
    expect(mockProps.onToggleNagrada).toHaveBeenCalledTimes(1);
  });

  it('should render Running toggle button', () => {
    render(<Controls {...mockProps} />);
    const button = screen.getByText('⏸ ustavi tok');
    expect(button).toBeInTheDocument();
  });

  it('should render Paused state when running is false', () => {
    render(<Controls {...mockProps} running={false} />);
    const button = screen.getByText('▶ pusti tok');
    expect(button).toBeInTheDocument();
  });

  it('should call onToggleRunning when running button is clicked', () => {
    render(<Controls {...mockProps} />);
    const button = screen.getByText('⏸ ustavi tok');
    fireEvent.click(button);
    expect(mockProps.onToggleRunning).toHaveBeenCalledTimes(1);
  });

  it('should render Sleep button', () => {
    render(<Controls {...mockProps} />);
    const button = screen.getByText('☾ spanje (konsolidacija)');
    expect(button).toBeInTheDocument();
  });

  it('should call onSleep when Sleep button is clicked', () => {
    render(<Controls {...mockProps} />);
    const button = screen.getByText('☾ spanje (konsolidacija)');
    fireEvent.click(button);
    expect(mockProps.onSleep).toHaveBeenCalledTimes(1);
  });

  it('should render instructions text', () => {
    render(<Controls {...mockProps} />);
    expect(screen.getByText(/Klikni telegram v delovnem spominu/)).toBeInTheDocument();
    expect(screen.getByText(/Poimenovan pred spanjem/)).toBeInTheDocument();
  });

  it('should have proper accessibility attributes', () => {
    render(<Controls {...mockProps} />);
    
    const nagradaButton = screen.getByLabelText(/Nagrada δ/);
    expect(nagradaButton).toHaveAttribute('aria-pressed', 'false');
    
    const runningButton = screen.getByLabelText('Ustavi tok');
    expect(runningButton).toBeInTheDocument();
  });
});
