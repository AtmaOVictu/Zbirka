// ⟡ DAJ/⊘ System: Core UI/Logic Structure
// Framework: React (UI) + Python (Backend Logic Placeholder)

import React, { useState } from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

export default function DajSystem() {
  const [dajInput, setDajInput] = useState("");
  const [oOutput, setOOutput] = useState("");
  const [deltaOutput, setDeltaOutput] = useState("");
  const [logbook, setLogbook] = useState([
    {
      daj: "Ljubezen vse premaga.",
      o: "⊘: Ljubezen je orožje in past. Je zloraba in ječa.",
      delta: "∆: Ljubezen ni rešitev, temveč ∆pogum, da tvegaš kljub bolečini."
    },
    {
      daj: "Svoboda je absolutna vrednota.",
      o: "⊘: Svoboda je prazna, ko zanikamo odnose.",
      delta: "∆: Svoboda kot ∫kompromis, ki ga zavestno nosiš in z njim dihaš."
    },
    {
      daj: "Odpuščanje je najvišja krepost.",
      o: "⊘: Odpuščanje je izbris bolečine. Pozaba, ki izdaja spomin.",
      delta: "∆: Odpuščanje je možno samo, če ne pozabiš – če ∫boli, a greš dalje."
    },
    {
      daj: "Trpljenje oplemeniti človeka.",
      o: "⊘: Trpljenje pogosto samo zlomi. Je spirala obupa.",
      delta: "∆: Trpljenje postane ∆moč samo, če iz njega iztisneš ∫dejanje."
    },
    {
      daj: "Resnica je smisel življenja.",
      o: "⊘: Resnica lahko zaslepi. Je orodje nasilja.",
      delta: "∆: Resnica je pot, ne cilj. Je ∆tok, ne ∴idol."
    }
  ]);

  function handleRitual() {
    const O = `⊘: ${dajInput.toUpperCase()} JE ZLOMLJIVA DOGMA. PREVERI ZLORABO.`;
    const delta = `∆: IZ '${dajInput}' ZMORE NASTATI NOVA AKTIVNA ODGOVORNOST.`;
    setOOutput(O);
    setDeltaOutput(delta);
    setLogbook([...logbook, { daj: dajInput, o: O, delta }]);
  }

  return (
    <div className="p-4 grid gap-4">
      <Card>
        <CardContent>
          <h2 className="text-xl font-bold">⟡ Vnesi svoj sveti DAJ</h2>
          <Textarea
            value={dajInput}
            onChange={(e) => setDajInput(e.target.value)}
            placeholder="Npr. 'Ljubezen vse premaga'"
          />
          <Button className="mt-2" onClick={handleRitual}>∆ RAZKROJI</Button>
        </CardContent>
      </Card>

      {oOutput && (
        <Card>
          <CardContent>
            <h3 className="text-lg font-semibold">⊘ RAZKROJ:</h3>
            <p>{oOutput}</p>
            <h3 className="text-lg font-semibold mt-4">∆ MOŽNOST:</h3>
            <p>{deltaOutput}</p>
          </CardContent>
        </Card>
      )}

      <Card>
        <CardContent>
          <h3 className="text-lg font-bold">Zapisnik (Knjiga DAJ/⊘)</h3>
          {logbook.map((entry, index) => (
            <div key={index} className="mt-2">
              <p><strong>DAJ:</strong> {entry.daj}</p>
              <p><strong>⊘:</strong> {entry.o}</p>
              <p><strong>∆:</strong> {entry.delta}</p>
              <hr className="my-2" />
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  );
}
