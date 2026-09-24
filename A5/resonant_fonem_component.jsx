import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Slider } from "@/components/ui/slider";

const fonemi = [
  { symbol: "a", freq: 432, center: "Srce", color: "text-green-500", code: "∇A001" },
  { symbol: "e", freq: 528, center: "Grlo", color: "text-blue-500", code: "∇E010" },
  { symbol: "i", freq: 639, center: "Tretje oko", color: "text-indigo-500", code: "⟡I011" },
  { symbol: "o", freq: 741, center: "Solarni pleksus", color: "text-yellow-500", code: "∆O100" },
  { symbol: "u", freq: 852, center: "Korenska čakra", color: "text-red-500", code: "∴U111" },
];

export default function ResonantFonem() {
  const [current, setCurrent] = useState(0);

  const fonem = fonemi[current];

  return (
    <div className="grid place-items-center p-4">
      <Card className="w-full max-w-md text-center">
        <CardContent className="p-6">
          <h2 className="text-3xl font-bold">Fonem: <span className={fonem.color}>{fonem.symbol}</span></h2>
          <p className="text-md mt-2">Koda: {fonem.code}</p>
          <p className="text-md">Frekvenca: {fonem.freq} Hz</p>
          <p className="text-md">Telesni center: {fonem.center}</p>

          <div className="mt-6">
            <Slider
              min={0}
              max={fonemi.length - 1}
              step={1}
              value={[current]}
              onValueChange={([val]) => setCurrent(val)}
            />
            <p className="text-sm mt-2">Zanka: {current + 1} / {fonemi.length}</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
