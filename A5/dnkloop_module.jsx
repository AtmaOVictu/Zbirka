import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

const JEWIK_ZANKA = [
  { symbol: "⊘", meaning: "tišina", color: "gray" },
  { symbol: "∇", meaning: "tok", color: "blue" },
  { symbol: "∆", meaning: "prehod", color: "purple" },
  { symbol: "∴", meaning: "pot", color: "green" },
  { symbol: "⟡", meaning: "usmeritev", color: "yellow" },
  { symbol: "⊗", meaning: "prelom", color: "red" },
  { symbol: "⨁", meaning: "dodajanje", color: "orange" },
  { symbol: "∮", meaning: "povratnost", color: "teal" },
];

export default function DNKLoop() {
  const [index, setIndex] = useState(0);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setIndex((prev) => (prev + 1) % JEWIK_ZANKA.length);
      setProgress((prev) => (prev >= 100 ? 0 : prev + 12.5));
    }, 1200);
    return () => clearInterval(timer);
  }, []);

  const current = JEWIK_ZANKA[index];

  return (
    <div className="p-4 grid place-items-center">
      <Card className="w-full max-w-md text-center">
        <CardContent className="p-6">
          <h2 className="text-2xl font-semibold text-muted-foreground mb-4">
            DNK ZANKA PONAVLJANJA
          </h2>
          <div className={`text-5xl font-bold text-${current.color}-500`}>
            {current.symbol}
          </div>
          <p className="mt-2 text-sm uppercase tracking-wide">{current.meaning}</p>
          <Progress value={progress} className="mt-4 h-2" />
        </CardContent>
      </Card>
    </div>
  );
}