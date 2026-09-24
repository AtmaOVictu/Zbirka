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
  const [logbook, setLogbook] = useState([]);

  function handleRitual() {
    // ⟡ Here we simulate the O (razkroj) and ∆ (transformacija) responses
    const O = `RAZKROJ: ${dajInput.toUpperCase()} JE MASKA. PREVERI NJENO SRCE.`;
    const delta = `∆MOŽNOST: IZ ${dajInput} SE RODI NOVO DEJANJE.`;
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
