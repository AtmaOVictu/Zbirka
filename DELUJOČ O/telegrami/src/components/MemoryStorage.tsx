// =============================================================================
// MEMORY STORAGE: Shramba — kam je padel vsak žarek
// Koncept: Epizodični, Semantični, Proceduralni, Priming (ONO)
// =============================================================================

import React from 'react';
import { CategoryKey } from '../types';
import { CATEGORIES } from '../utils/constants';

interface MemoryStorageProps {
  stored: Record<CategoryKey, string[]>;
  flash?: { cat: CategoryKey; timestamp: number };
  total: number;
}

export const MemoryStorage: React.FC<MemoryStorageProps> = ({ stored, flash, total }) => {
  // Filtriraj iz delovni (ta ni v shrambi)
  const displayCategories = Object.entries(CATEGORIES).filter(
    ([k]) => k !== 'delovni'
  ) as [CategoryKey, typeof CATEGORIES[CategoryKey]][];

  return (
    <section className="bg-white border border-zinc-200 rounded-xl p-4 shadow-sm">
      <h2 className="font-semibold mb-3 text-sm uppercase tracking-wide text-zinc-500">
        Shramba — kam je padel vsak žarek ({total})
      </h2>
      <div className="space-y-3">
        {displayCategories.map(([k, c]) => {
          const isFlashing = flash?.cat === k && Date.now() - flash.timestamp < 1200;
          return (
            <div
              key={k}
              className={`rounded-lg border p-2 ${c.color} ${isFlashing ? 'ring-2 ring-offset-1' : ''}`}
              aria-label={`Kategorija ${c.label}, ${stored[k].length} vnosov`}
            >
              <div className="flex justify-between items-baseline">
                <span className="text-xs font-bold">{c.label}</span>
                <span className="text-xs">{stored[k].length}</span>
              </div>
              <div className="text-[11px] opacity-80 mb-1">{c.desc}</div>
              <div className="flex flex-wrap gap-1">
                {stored[k].slice(-8).map((x, i) => (
                  <span
                    key={i}
                    className="text-[10px] bg-white/60 rounded px-1.5 py-0.5"
                  >
                    {x}
                  </span>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
};
