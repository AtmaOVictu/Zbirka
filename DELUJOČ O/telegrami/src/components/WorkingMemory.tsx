// =============================================================================
// WORKING MEMORY: Delovni spomin — odprta ∂ (Zeigarnik, kapaciteta 4)
// Koncept: Nedovršno drži. Kapaciteta štirih; peti izrine prvega v implicitno.
// =============================================================================

import React from 'react';
import { Telegram } from '../types';
import { CONFIG, CATEGORIES } from '../utils/constants';

interface WorkingMemoryProps {
  telegrams: Telegram[];
  onName: (telegram: Telegram) => void;
}

export const WorkingMemory: React.FC<WorkingMemoryProps> = ({ telegrams, onName }) => {
  return (
    <section className="bg-white border border-zinc-200 rounded-xl p-4 shadow-sm">
      <h2 className="font-semibold mb-1 text-sm uppercase tracking-wide text-zinc-500">
        Delovni spomin — odprta ∂ ({telegrams.length}/{CONFIG.WM_CAPACITY})
      </h2>
      <p className="text-xs text-zinc-500 mb-3">
        Zeigarnik: nedovršno drži. Kapaciteta štirih; peti izrine prvega v implicitno.
      </p>
      <div className="space-y-2 min-h-[220px]">
        {telegrams.length === 0 && (
          <p className="text-xs text-zinc-400 italic">tok je prazen…</p>
        )}
        {telegrams.map((t) => (
          <button
            key={t.id}
            onClick={() => onName(t)}
            aria-label={`Poimenuj telegram: ${t.text}`}
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                onName(t);
              }
            }}
            tabIndex={0}
            className={`
              w-full text-left px-3 py-2 rounded-lg border text-sm 
              transition hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-offset-1
              ${t.novelty > 0.7 ? 'border-amber-400 bg-amber-50' : 
                 t.goal ? 'border-fuchsia-400 bg-fuchsia-50' : 
                 'border-zinc-300 bg-zinc-50'}
            `}
          >
            <span className="font-medium">{t.text}</span>
            <span className="block text-[11px] text-zinc-500 mt-0.5">
              novost {(t.novelty * 100).toFixed(0)}% · starost {t.age}
              {t.goal && ' · ∂ cilj'}
              {t.age >= 3 && !t.named ? ' · ugaša…' : ''}
            </span>
          </button>
        ))}
      </div>
    </section>
  );
};
