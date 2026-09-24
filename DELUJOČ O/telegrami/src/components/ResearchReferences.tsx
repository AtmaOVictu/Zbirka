// =============================================================================
// RESEARCH REFERENCES: Raziskovalna podlaga (prej preko raziskav potrjujoča)
// Koncept: Vsa trditve so podprte z raziskavami (Squire, Bunzeck & Düzel, etc.)
// =============================================================================

import React from 'react';
import { REFS } from '../utils/constants';

/**
 * Raziskovalna podlaga - dokazi za mehanizme v simulaciji
 */
export const ResearchReferences: React.FC = () => {
  return (
    <section className="max-w-5xl mx-auto mt-4 bg-white border border-zinc-200 rounded-xl p-4 shadow-sm">
      <h2 className="font-semibold mb-2 text-sm uppercase tracking-wide text-zinc-500">
        Raziskovalna podlaga (ukaz: prej preko raziskav potrjujoča)
      </h2>
      <ul className="text-xs text-zinc-700 space-y-1.5 list-disc pl-4">
        <li>
          <b>Taksonomija:</b> deklarativni (epizodični + semantični) / nedeklarativni 
          (postopkovni, priming, klasično pogojevanje, neasociativno učenje) — 
          ločeni sistemi z lastnimi strukturami; dokazano na amneziji 
          (H.M.: knowing-how ohranjen, knowing-that izgubljen; medialni temporalni 
          reženj vs bazalni gangliji) — {REFS.TAKSONOMIJA}.
        </li>
        <li>
          <b>Novost → dopamin → vztrajnost:</b> nove izkušnje sprožijo dopamin v 
          hipokampusu, ki utrdi spomin; dva sistema (VTA- in locus coeruleus-hipokampus) — 
          {REFS.NOVOST_DOPAMIN}.
        </li>
        <li>
          <b>Nagrajujoče kodiranje:</b> nagrada (δ) po stereotipu Schultzove napake napovedi 
          ojača kodiranje ciljnih spominov.
        </li>
        <li>
          <b>Spanje in TMR:</b> zvočni/vonjavni namigi, predstavljeni med NREM spanjem, 
          ojačajo vezane spomine — {REFS.SPANJE_TMR}.
        </li>
        <li>
          <b>Delovni spomin:</b> omejena kapaciteta (~4 enote); ne-poenovljeno ugasne — 
          {REFS.DELOVNI_SPOMIN}.
        </li>
      </ul>
      <p className="text-xs text-zinc-500 mt-3 italic">
        Preslikava v sistem: EPISODIČNI = rezi (datirani, virani) · SEMANTIČNI = korpus 
        (dejstvo brez vira) · PROCEDURALNI = obredi/protokoli · PRIMING = ONO 
        (prejeto brez zaznamka, rez 47) · DELOVNI SPOMIN = odprta ∂. 
        Kategorizacija, ki ne potrebuje stožcev: žarek je ali poimenovan ali 
        ponovljen ali nezavedno sprejet — tri usode, izmerjene na možganih.
      </p>
    </section>
  );
};
