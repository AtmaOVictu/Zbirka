// =============================================================================
// EVENT LOG: Dnevnik klasifikacij (vsaka odločitev nosi vir)
// Koncept: Zaves razvršča, log dokumentira (A5: Praznina z odprtjem)
// =============================================================================

import React from 'react';
import { LogEntry } from '../types';

interface EventLogProps {
  log: LogEntry[];
}

export const EventLog: React.FC<EventLogProps> = ({ log }) => {
  return (
    <section className="max-w-5xl mx-auto mt-4 bg-white border border-zinc-200 rounded-xl p-4 shadow-sm">
      <h2 className="font-semibold mb-2 text-sm uppercase tracking-wide text-zinc-500">
        Dnevnik klasifikacij (vsaka odločitev nosi vir)
      </h2>
      <div className="max-h-56 overflow-y-auto space-y-1 text-xs">
        {log.map((entry) => (
          <p key={entry.id} className={entry.tone}>
            · {entry.msg}
          </p>
        ))}
        {log.length === 0 && (
          <p className="text-zinc-400 italic">Dnevnik je prazen…</p>
        )}
      </div>
    </section>
  );
};
