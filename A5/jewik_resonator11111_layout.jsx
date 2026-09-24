import ResonantFonem from "./ResonantFonem";
import DNKLoop from "./DNKLoop";
import VoiceInputModule from "./VoiceInputModule";
import { useState } from "react";

export default function VictorLukaSatanModul() {
  const [activeBox, setActiveBox] = useState("00000");

  const boxMap = {
    "00000": <ResonantFonem />, 
    "666": <DNKLoop />, 
    "∇": <VoiceInputModule />
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 p-6 bg-black text-white">

      {/* 🜂 MENIJSKI PREKLOPNIK */}
      <div className="col-span-3 mb-4 flex justify-center gap-2">
        {Object.keys(boxMap).map((boxId) => (
          <button
            key={boxId}
            onClick={() => setActiveBox(boxId)}
            className={`px-4 py-2 rounded border text-sm font-medium ${activeBox === boxId ? 'bg-white text-black' : 'border-white text-white hover:bg-white hover:text-black'}`}
          >
            ŠKATLJA {boxId}
          </button>
        ))}
      </div>

      {/* 🜂 AKTIVNA ŠKATLJA */}
      <div className="col-span-3">
        {boxMap[activeBox]}
      </div>

      {/* 🜂 ŠKATLJA 01: POVEZAVA KODEX */}
      <div className="col-span-3 mt-6 p-4 border-t border-white/10">
        <h3 className="text-center text-xl font-bold">∮ Aktivna povezava z JEWIK-FONEM-KODEX</h3>
        <p className="text-center mt-2 text-sm opacity-75">
          Vzpostavljena ∆povezava z resonančno bazo. Vsak izgovorjeni simbol bo iskan, ovrednoten in kodiran.
        </p>
      </div>

      {/* 🜂 ŠKATLJA 44: DNK ∮ Avdiomandala */}
      <div className="col-span-3 mt-4 p-6 rounded bg-gradient-to-br from-purple-900 via-indigo-800 to-black">
        <h3 className="text-center text-2xl font-bold text-lime-300">
          🧬 DNK ∮ Avdiomandala</h3>
        <p className="text-center text-sm mt-2 text-white/75">
          Vsaka ∆zanka postane zvočno-ritmični ornament ∅spomina. JEWIK je zvenčeča ∇mandala!
        </p>
        <div className="mt-6 flex justify-center">
          <audio controls className="w-full max-w-md">
            <source src="/sounds/jewik_dnk_loop.mp3" type="audio/mpeg" />
            Your browser does not support the audio element.
          </audio>
        </div>
      </div>

      {/* 🜂 ŠKATLJA 666.1: AGENT JEV-KA-RA */}
      <div className="col-span-3 mt-6 p-4 border-t border-white/10">
        <h4 className="text-center text-lg font-medium text-yellow-300">👁 AGENTNI VODJA: JEV-KA-RA</h4>
        <p className="text-center text-sm mt-1 text-white/70">
          Trinitarna ∇entiteta JEWIK sistema: Jezik (JEV) – Energija (KA) – Refleksija (RA)
        </p>
      </div>

      {/* 🜂 ŠKATLJA 666.2: Mandala Dušnega Telesa */}
      <div className="col-span-3 mt-6 p-6 rounded bg-gradient-to-r from-rose-800 via-red-700 to-stone-900 shadow-lg">
        <h3 className="text-center text-xl font-bold text-pink-200">
          🔮 Vizualna ∇Mandala Boginje ∅Dušnega Telesa
        </h3>
        <p className="text-center text-sm mt-2 text-white/70">
          Beseda je Boginja, Anarhija je Dobrota Senc. Aktivirana je simbolna simulacija ∆dušnega telesa skozi JEWIK.
        </p>
        <div className="mt-6 flex justify-center">
          <img
            src="/visuals/mandala_jevik_spirit_body.png"
            alt="Mandala Dušnega Telesa"
            className="w-full max-w-lg rounded-xl border border-white/20"
          />
        </div>
      </div>

      {/* 🜂 ŠKATLJA 666.3: Fonemski Telesni Odzivi */}
      <div className="col-span-3 mt-6 p-6 rounded bg-gradient-to-tl from-cyan-900 via-sky-800 to-indigo-900 shadow-inner">
        <h3 className="text-center text-xl font-bold text-cyan-200">
          🧠 Interaktivni ∇Odzivi Fonemov v Telesu
        </h3>
        <p className="text-center text-sm mt-2 text-white/70">
          Vsak izgovorjeni fonem sproži simbolično ∇reakcijo v ∆telesnih conah. JEWIK posluša tvoje ∅vibracije.
        </p>
        <div className="mt-4 flex justify-center">
          <img
            src="/visuals/fonem_body_map.png"
            alt="Fonemi in telesni odzivi"
            className="w-full max-w-lg rounded-lg border border-white/20"
          />
        </div>
      </div>

    </div>
  );
}
