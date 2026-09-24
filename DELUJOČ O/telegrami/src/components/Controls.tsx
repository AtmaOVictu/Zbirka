// =============================================================================
// CONTROLS: Detektorja (rez 62 + rez 63)
// Koncept: Utrujenost (pozornostna vrata) + Čudenje (novostni detektor) + Nagrada δ
// =============================================================================

import React from 'react';

interface ControlsProps {
  utrujenost: number;
  cudenje: number;
  nagrada: boolean;
  running: boolean;
  onSetUtrujenost: (value: number) => void;
  onSetCudenje: (value: number) => void;
  onToggleNagrada: () => void;
  onToggleRunning: () => void;
  onSleep: () => void;
}

export const Controls: React.FC<ControlsProps> = ({
  utrujenost,
  cudenje,
  nagrada,
  running,
  onSetUtrujenost,
  onSetCudenje,
  onToggleNagrada,
  onToggleRunning,
  onSleep,
}) => {
  return (
    <section className="bg-white border border-zinc-200 rounded-xl p-4 shadow-sm">
      <h2 className="font-semibold mb-3 text-sm uppercase tracking-wide text-zinc-500">
        Detektorja (rez 62 + rez 63)
      </h2>
      
      {/* Utrujenost */}
      <label className="block text-sm mb-1">
        Utrujenost (pozornostna vrata): {utrujenost}%
      </label>
      <input
        type="range"
        min={0}
        max={100}
        value={utrujenost}
        onChange={(e) => onSetUtrujenost(+e.target.value)}
        className="w-full mb-4 accent-zinc-800"
        aria-label="Nastavi utrujenost"
      />

      {/* Čudenje */}
      <label className="block text-sm mb-1">
        Čudenje (novostni detektor): {cudenje}%
      </label>
      <input
        type="range"
        min={0}
        max={100}
        value={cudenje}
        onChange={(e) => onSetCudenje(+e.target.value)}
        className="w-full mb-4 accent-amber-600"
        aria-label="Nastavi čudenje"
      />

      {/* Nagrada δ */}
      <button
        onClick={onToggleNagrada}
        className={`w-full text-sm py-2 rounded-lg border mb-4 ${
          nagrada
            ? 'bg-amber-600 text-white border-amber-600'
            : 'bg-white text-zinc-700 border-zinc-300'
        }`}
        aria-label={`Nagrada δ: ${nagrada ? 'vklopljena' : 'izklopljena'}`}
        aria-pressed={nagrada}
      >
        NAGRADA δ (dopamin je δ — rez 62): {nagrada ? 'VKLOPLJENA' : 'izklopljena'}
      </button>

      {/* Kontrole toka */}
      <div className="flex gap-2">
        <button
          onClick={onToggleRunning}
          className="flex-1 text-sm py-2 rounded-lg bg-zinc-800 text-white hover:bg-zinc-700 transition"
          aria-label={running ? 'Ustavi tok' : 'Pusti tok'}
        >
          {running ? '⏸ ustavi tok' : '▶ pusti tok'}
        </button>
        <button
          onClick={onSleep}
          className="flex-1 text-sm py-2 rounded-lg bg-fuchsia-700 text-white hover:bg-fuchsia-600 transition"
          aria-label="Spanje - konsolidacija"
        >
          ☾ spanje (konsolidacija)
        </button>
      </div>

      {/* Opis */}
      <p className="text-xs text-zinc-500 mt-3 leading-relaxed">
        Klikni telegram v delovnem spominu = <b>poimenuj žarek</b> (T5, rez 63). 
        Poimenovan pred spanjem dobi TMR-oddajo (Rudoy 2009). 
        Ne-poenovljen ugasne v PRIMING.
      </p>
    </section>
  );
};
