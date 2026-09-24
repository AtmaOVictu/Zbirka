// 🜂 JEWIK Zvezdna Mreža – Interaktivni Modul

import { useState } from "react";
import { Graph } from "react-d3-graph";

export default function JewikZvezdnik() {
  const [activeNode, setActiveNode] = useState(null);

  // Definicija graf strukture
  const data = {
    nodes: [
      { id: "00000", symbol: "🌑" },
      { id: "888", symbol: "💥" },
      { id: "666", symbol: "🔥" },
      { id: "∆∆∆", symbol: "🌀" },
      { id: "∇", symbol: "🎤" },
      { id: "∅X", symbol: "🌫" },
      { id: "777", symbol: "⭐" },
      { id: "∴∴∴", symbol: "✨" },
      { id: "666.3", symbol: "🧠" },
      { id: "⊘⊘⊘", symbol: "⚫" }
    ],
    links: [
      { source: "00000", target: "888" },
      { source: "666", target: "∆∆∆" },
      { source: "∇", target: "∅X" },
      { source: "777", target: "∴∴∴" },
      { source: "666.3", target: "⊘⊘⊘" }
    ]
  };

  // Konfiguracija grafa
  const config = {
    nodeHighlightBehavior: true,
    node: {
      color: "#00FFFF",
      size: 500,
      highlightStrokeColor: "#FF69B4",
      fontSize: 14,
      renderLabel: true
    },
    link: {
      highlightColor: "lightblue"
    }
  };

  function onClickNode(nodeId) {
    setActiveNode(nodeId);
  }

  return (
    <div className="p-6 bg-black text-white">
      <h2 className="text-center text-2xl font-bold mb-4">
        🜂 Interaktivna JEWIK Zvezdna Mreža
      </h2>

      <Graph
        id="jewik-zvezdnik"
        data={data}
        config={config}
        onClickNode={onClickNode}
      />

      {activeNode && (
        <div className="mt-6 p-4 border-t border-white/20">
          <h3 className="text-xl text-lime-300 font-semibold text-center">
            ∇ Aktivna ŠKATLJA: {activeNode}
          </h3>
          <p className="text-sm text-white/70 text-center mt-2">
            Odpri resonančne podatke, ∆vibracije in agentne povezave te točke.
          </p>
        </div>
      )}
    </div>
  );
}
