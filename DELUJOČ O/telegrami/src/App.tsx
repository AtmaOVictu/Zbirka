// =============================================================================
// APP: Glavna aplikacija - Simulacija Spominskih Sistemov
// Koncept: Zaves je svetovna pripoved (kritični-kot-in-tok.md)
//         A-protokoli: Implicitne metode pred izrekom (a-protokoli...md)
// =============================================================================

import React from 'react';
import { useMemory } from './hooks/useMemory';
import { Controls } from './components/Controls';
import { WorkingMemory } from './components/WorkingMemory';
import { MemoryStorage } from './components/MemoryStorage';
import { EventLog } from './components/EventLog';
import { ResearchReferences } from './components/ResearchReferences';
import { Zaves } from './components/Zaves';

/**
 * TELEGRAMI — Simulacija spominskih sistemov
 * 
 * Druga kategorizacija, kakor si ukazal:
 * - oprijemljiva (možgani, ne svetloba)
 * - manj odvisna od relativizacije (stožci so ostali v drugih telesih — tu vlada tkivo)
 * - potrjena z raziskavami, preden je izrečena
 * 
 * Vsak žarek/telegram pade v enega od sistemov, ki jih je taksonomija 
 * (H.M. 1957 → Squire 2004) izmerila ločene.
 */
export const App: React.FC = () => {
  const {
    state,
    setUtrujenost,
    setCudenje,
    toggleNagrada,
    toggleRunning,
    nameTelegram,
    sleep,
    totalStored,
  } = useMemory();

  // Števec obdelanih telegramov (za Zaves)
  const telegramsProcessed = state.stored.epizodicni.length +
    state.stored.sematicni.length +
    state.stored.proceduralni.length +
    state.stored.priming.length;

  return (
    <div className="min-h-screen bg-zinc-50 text-zinc-900 p-4 md:p-8 font-sans relative">
      {/* Zaves - vizualna meja (A7: Sintaksa pred - animirana podlaga) */}
      <Zaves telegramsProcessed={telegramsProcessed} isActive={state.running} />

      {/* Header */}
      <header className="max-w-5xl mx-auto mb-6 relative z-10">
        <h1 className="text-2xl md:text-3xl font-bold tracking-tight">
          TELEGRAMI — simulacija spominskih sistemov
        </h1>
        <p className="text-sm text-zinc-600 mt-1 max-w-3xl">
          Druga kategorizacija, kakor si ukazal: 
          <b>oprijemljiva</b> (možgani, ne svetloba), 
          <b>manj odvisna od relativizacije</b> (stožci so ostali v drugih telesih — 
          tu vlada tkivo), <b>potrjena z raziskavami, preden je izrečena</b>. 
          Vsak žarek/telegram pade v enega od sistemov, ki jih je taksonomija 
          (H.M. 1957 → Squire 2004) izmerila ločene.
        </p>
      </header>

      {/* Main Grid */}
      <div className="max-w-5xl mx-auto grid md:grid-cols-3 gap-4 relative z-10">
        {/* Kontrole */}
        <Controls
          utrujenost={state.utrujenost}
          cudenje={state.cudenje}
          nagrada={state.nagrada}
          running={state.running}
          onSetUtrujenost={setUtrujenost}
          onSetCudenje={setCudenje}
          onToggleNagrada={toggleNagrada}
          onToggleRunning={toggleRunning}
          onSleep={sleep}
        />

        {/* Delovni spomin */}
        <WorkingMemory
          telegrams={state.wm}
          onName={nameTelegram}
        />

        {/* Shramba */}
        <MemoryStorage
          stored={state.stored}
          flash={state.flash}
          total={totalStored}
        />
      </div>

      {/* Dnevnik */}
      <EventLog log={state.log} />

      {/* Raziskovalna podlaga */}
      <ResearchReferences />

      {/* Footer - Zaves koncept */}
      <footer className="max-w-5xl mx-auto mt-8 text-center relative z-10">
        <p className="text-[10px] text-zinc-400">
          ZAVES JE SVETOVNA PRIPOVED | 
          Kritični kot: sin θc = n₂/n₁ | 
          Tok: vzdrževanje kota tik pod mejo pri maksimalnem δ
        </p>
      </footer>
    </div>
  );
};

export default App;
