import React, { useState, useMemo } from "react";

const REZI = [
{"n":53,"t":"VEKTORSKA URA","k":.82,"c":.70,"m":.62,"r":.05,"v":.80,"ref":11,"q":3,"len":2744},
{"n":54,"t":"NARCIS IN ODMEV","k":.83,"c":.70,"m":.62,"r":.05,"v":.75,"ref":13,"q":6,"len":3787},
{"n":55,"t":"ν PRED PEČATOM","k":.81,"c":.72,"m":.65,"r":.06,"v":.70,"ref":9,"q":4,"len":2716},
{"n":56,"t":"BODIVA EN O","k":.78,"c":.70,"m":.60,"r":.06,"v":.70,"ref":14,"q":3,"len":4605},
{"n":57,"t":"VEKTORSKA URA DVA","k":.84,"c":.70,"m":.62,"r":.06,"v":.75,"ref":11,"q":7,"len":3970},
{"n":58,"t":"URANUS AMALGAMACIJA","k":.79,"c":.68,"m":.58,"r":.06,"v":.72,"ref":18,"q":8,"len":7096},
{"n":59,"t":"SVETLOBNI STOŽEC REZA","k":.83,"c":.70,"m":.60,"r":.06,"v":.72,"ref":27,"q":3,"len":4806},
{"n":60,"t":"DUO-∫","k":.81,"c":.70,"m":.60,"r":.06,"v":.70,"ref":29,"q":11,"len":6416},
{"n":61,"t":"VELIKI POK","k":.80,"c":.68,"m":.60,"r":.06,"v":.72,"ref":23,"q":4,"len":5514},
{"n":62,"t":"NAGRADA","k":.82,"c":.70,"m":.60,"r":.07,"v":.70,"ref":14,"q":9,"len":6622},
{"n":63,"t":"OBSIJANI","k":.83,"c":.70,"m":.62,"r":.06,"v":.72,"ref":16,"q":3,"len":4499},
{"n":64,"t":"TELEGRAMI","k":.85,"c":.74,"m":.68,"r":.06,"v":.73,"ref":19,"q":3,"len":5988},
{"n":65,"t":"OBVLADAVE | OBVLADAVANJE","k":.81,"c":.68,"m":.60,"r":.06,"v":.70,"ref":17,"q":11,"len":6271},
{"n":66,"t":"ENTROPIJA TELEGRAMOV","k":.84,"c":.72,"m":.70,"r":.06,"v":.74,"ref":18,"q":2,"len":5537},
{"n":67,"t":"ENTROPIJA PRAZNINE","k":.88,"c":.74,"m":.66,"r":.07,"v":.72,"ref":26,"q":6,"len":5476},
{"n":70,"t":"ENTROPIJA PRAZNINE","k":.85,"c":.70,"m":.78,"r":.06,"v":.76,"ref":40,"q":2,"len":8943},
{"n":71,"t":"SIMBOLE","k":.88,"c":.80,"m":.75,"r":.05,"v":.78,"ref":73,"q":7,"len":11575},
{"n":75,"t":"ORAKELJ DA/NE","k":.83,"c":.69,"m":.74,"r":.06,"v":.75,"ref":24,"q":5,"len":6156},
{"n":77,"t":"CARPE DIEM","k":.85,"c":.71,"m":.73,"r":.05,"v":.72,"ref":20,"q":3,"len":5804},
{"n":78,"t":"CARPEVAVA DIEM","k":.86,"c":.72,"m":.70,"r":.05,"v":.68,"ref":213,"q":26,"len":65342},
{"n":33,"t":"LATINŠČINA V","k":.84,"c":.66,"m":.62,"r":.02,"v":.70,"ref":1,"q":2,"len":3716},
{"n":34,"t":"NUJNI NAGLASI","k":.82,"c":.66,"m":.62,"r":.02,"v":.68,"ref":1,"q":2,"len":3852},
{"n":35,"t":"DRUŽINE VALA","k":.82,"c":.66,"m":.62,"r":.02,"v":.68,"ref":2,"q":5,"len":4126},
{"n":36,"t":"REGISTER BISTEV","k":.86,"c":.68,"m":.62,"r":.02,"v":.68,"ref":0,"q":8,"len":3769},
{"n":37,"t":"DELO","k":.80,"c":.70,"m":.62,"r":.02,"v":.68,"ref":1,"q":11,"len":3192},
{"n":38,"t":"ZDRAVJE","k":.82,"c":.70,"m":.62,"r":.02,"v":.68,"ref":1,"q":12,"len":3755},
{"n":38,"t":"JEZIK JE RAZVOJ","k":.84,"c":.70,"m":.63,"r":.04,"v":.68,"ref":6,"q":10,"len":4932},
{"n":0,"t":"Dopis k rezoma 37 in 38","k":.80,"c":.70,"m":.62,"r":.03,"v":.66,"ref":5,"q":11,"len":2597},
{"n":39,"t":"MOTOR IN ROTACIJA + TONEMI-TONOS","k":.82,"c":.70,"m":.65,"r":.05,"v":.69,"ref":5,"q":6,"len":5277},
{"n":68,"t":"SMRT","k":.82,"c":.70,"m":.64,"r":.04,"v":.70,"ref":11,"q":10,"len":5466},
{"n":40,"t":"KONJUNKTIV","k":.84,"c":.72,"m":.66,"r":.04,"v":.68,"ref":3,"q":4,"len":3179},
{"n":69,"t":"POMLAD","k":.83,"c":.71,"m":.66,"r":.03,"v":.69,"ref":8,"q":11,"len":4621},
{"n":0,"t":"Dopis k rezu 69","k":.84,"c":.72,"m":.65,"r":.05,"v":.71,"ref":7,"q":6,"len":2614},
{"n":41,"t":"KRITIČNI KOT IN TOK","k":.83,"c":.70,"m":.66,"r":.05,"v":.69,"ref":1,"q":4,"len":3703},
{"n":0,"t":"Drugi dopis k rezu 69","k":.83,"c":.72,"m":.70,"r":.05,"v":.72,"ref":3,"q":4,"len":2985},
{"n":42,"t":"ANJA PROTOKOLI","k":.84,"c":.70,"m":.66,"r":.05,"v":.69,"ref":8,"q":4,"len":4074},
{"n":70,"t":"TIŠINA","k":.85,"c":.72,"m":.70,"r":.04,"v":.72,"ref":10,"q":16,"len":5397},
{"n":43,"t":"VRSTA SOPHIE","k":.82,"c":.72,"m":.66,"r":.05,"v":.68,"ref":3,"q":3,"len":3178},
{"n":44,"t":"PLJUBČIŽNI","k":.83,"c":.72,"m":.68,"r":.05,"v":.70,"ref":3,"q":4,"len":3919},
{"n":73,"t":"LEGITIMEN ODGOVOR NA VSE IN NIČ","k":.84,"c":.72,"m":.66,"r":.04,"v":.70,"ref":11,"q":16,"len":5269},
{"n":45,"t":"MITHOS APERCEPCIJA","k":.83,"c":.72,"m":.68,"r":.05,"v":.70,"ref":7,"q":6,"len":8265},
{"n":75,"t":"ONTOFÍZA","k":.83,"c":.71,"m":.65,"r":.05,"v":.70,"ref":22,"q":9,"len":5779},
{"n":76,"t":"CELOST VSEGA","k":.84,"c":.72,"m":.66,"r":.05,"v":.72,"ref":18,"q":11,"len":5333},
{"n":47,"t":"PLEROMA IN AEONI","k":.84,"c":.72,"m":.68,"r":.05,"v":.72,"ref":16,"q":12,"len":9496},
{"n":77,"t":"MIDVA","k":.84,"c":.72,"m":.67,"r":.04,"v":.72,"ref":9,"q":7,"len":3448},
{"n":78,"t":"VSE-ENO","k":.88,"c":.75,"m":.70,"r":.02,"v":.75,"ref":7,"q":3,"len":3743},
{"n":78,"t":"78-REK VSE-ENO","k":.89,"c":.76,"m":.71,"r":.01,"v":.76,"ref":8,"q":2,"len":2249},
{"n":79,"t":"GAIA","k":.85,"c":.75,"m":.70,"r":.02,"v":.75,"ref":5,"q":2,"len":3459},
{"n":80,"t":"ODMEV","k":.90,"c":.77,"m":.72,"r":.01,"v":.77,"ref":17,"q":2,"len":2836},
{"n":81,"t":"ROHONC CODEX","k":.87,"c":.74,"m":.69,"r":.02,"v":.74,"ref":7,"q":2,"len":2571},
{"n":82,"t":"SIMBOLON-KOTEL","k":.92,"c":.80,"m":.75,"r":.01,"v":.80,"ref":12,"q":2,"len":3090},
{"n":82,"t":"82-rek SIMBOLON-KOTEL-REK","k":.93,"c":.82,"m":.76,"r":.01,"v":.81,"ref":3,"q":4,"len":3608},
{"n":83,"t":"ROHONC-SUPERPOZICIJA","k":.83,"c":.76,"m":.70,"r":.04,"v":.74,"ref":6,"q":8,"len":5793},
{"n":84,"t":"ZIPF-PODPIS","k":.85,"c":.78,"m":.72,"r":.05,"v":.76,"ref":10,"q":5,"len":5868},
{"n":85,"t":"SIMBOLE","k":.95,"c":.85,"m":.78,"r":.05,"v":.75,"ref":10,"q":2,"len":2682},
{"n":85,"t":"N-GRAM-VEZ","k":.84,"c":.79,"m":.71,"r":.04,"v":.77,"ref":14,"q":10,"len":6483},
{"n":85,"t":"NAKLON","k":.82,"c":.74,"m":.74,"r":.05,"v":.76,"ref":19,"q":10,"len":6009},
{"n":86,"t":"VEZ V SENCI","k":.84,"c":.72,"m":.73,"r":.05,"v":.75,"ref":11,"q":11,"len":5963},
{"n":86,"t":"VEZ N-GRAM","k":.84,"c":.80,"m":.72,"r":.04,"v":.78,"ref":11,"q":23,"len":6953},
{"n":86,"t":"86-rek O DEFINIRAN","k":.83,"c":.80,"m":.74,"r":.04,"v":.77,"ref":16,"q":13,"len":6876},
{"n":87,"t":"ZLOGOVNO TKIVO","k":.85,"c":.78,"m":.72,"r":.04,"v":.77,"ref":20,"q":4,"len":9775},
{"n":88,"t":"ZAKON DVOJNEGA KANALA","k":.86,"c":.82,"m":.76,"r":.03,"v":.79,"ref":19,"q":4,"len":4056},
{"n":89,"t":"VREDNO OMEMBE","k":.88,"c":.85,"m":.78,"r":.02,"v":.75,"ref":8,"q":2,"len":2172},
{"n":90,"t":"KVALITETA V KORPUSU","k":.87,"c":.83,"m":.75,"r":.02,"v":.76,"ref":13,"q":3,"len":3392},
{"n":90,"t":"OKRASNI GLIFI","k":.86,"c":.84,"m":.77,"r":.03,"v":.80,"ref":2,"q":3,"len":2307},
{"n":91,"t":"NIKOLI JE MERILO, NE SVET","k":.87,"c":.86,"m":.76,"r":.03,"v":.78,"ref":2,"q":12,"len":2545},
{"n":92,"t":"SAMO JE OPERATOR, KI DELI","k":.87,"c":.85,"m":.77,"r":.03,"v":.79,"ref":4,"q":11,"len":3869},
{"n":93,"t":"∧ NI PRELOMLJEN — ZVARJEN JE","k":.88,"c":.86,"m":.78,"r":.03,"v":.80,"ref":5,"q":27,"len":4748},
{"n":94,"t":"OKTAVA","k":.88,"c":.84,"m":.75,"r":.04,"v":.80,"ref":27,"q":3,"len":5675},
{"n":95,"t":"TRAJEKTORIJA V GUARD PROSTORU","k":.88,"c":.85,"m":.76,"r":.03,"v":.78,"ref":15,"q":2,"len":3831},
{"n":95,"t":"SEKIRAM SEBE","k":.90,"c":.82,"m":.70,"r":.05,"v":.75,"ref":3,"q":8,"len":2376},
{"n":95,"t":"POVZETEK NI TELO","k":.80,"c":.70,"m":.75,"r":.03,"v":.80,"ref":2,"q":1,"len":2799},
{"n":94,"t":"ODGOVOR = POTRDITEV SLIŠANJA","k":.89,"c":.87,"m":.78,"r":.03,"v":.81,"ref":5,"q":23,"len":5186},
{"n":96,"t":"PESEM = EN DIH, TRI TELESA","k":.85,"c":.75,"m":.70,"r":.03,"v":.75,"ref":4,"q":10,"len":3168},
{"n":96,"t":"OPREMA JAZA","k":.86,"c":.80,"m":.70,"r":.04,"v":.72,"ref":7,"q":5,"len":3562},
{"n":95,"t":"PERO DRŽI IN RANI HKRATI","k":.88,"c":.86,"m":.78,"r":.03,"v":.80,"ref":10,"q":7,"len":4852},
{"n":97,"t":"OPREMI SI IDENTITETO","k":.80,"c":.75,"m":.75,"r":.03,"v":.75,"ref":2,"q":1,"len":3347},
{"n":98,"t":"NIČ = INTERVAL, KI UČI","k":.88,"c":.86,"m":.76,"r":.03,"v":.80,"ref":8,"q":5,"len":4239},
{"n":99,"t":"AMALGAMACIJA GNOSTIK+LATINŠČINA","k":.82,"c":.66,"m":.62,"r":.03,"v":.70,"ref":3,"q":2,"len":3145},
{"n":96,"t":"PERO JE MOJE","k":.87,"c":.86,"m":.78,"r":.03,"v":.80,"ref":7,"q":18,"len":4489},
{"n":97,"t":"TOK JE ROD","k":.88,"c":.87,"m":.78,"r":.03,"v":.80,"ref":4,"q":15,"len":4871},
{"n":100,"t":"AKTIVATOR BRAXAS","k":.87,"c":.82,"m":.72,"r":.04,"v":.74,"ref":11,"q":9,"len":4938},
{"n":100,"t":"MALENKOST Z KOSTJO","k":.80,"c":.75,"m":.70,"r":.03,"v":.75,"ref":6,"q":9,"len":3220},
{"n":101,"t":"VIJAČNICA","k":.89,"c":.85,"m":.77,"r":.03,"v":.79,"ref":21,"q":2,"len":4120},
{"n":98,"t":"BRALNIK","k":.85,"c":.90,"m":.80,"r":.02,"v":.75,"ref":2,"q":3,"len":2092},
{"n":102,"t":"STD-OUT INFRASTRUKTURA","k":.87,"c":.85,"m":.74,"r":.04,"v":.72,"ref":30,"q":3,"len":7057},
{"n":103,"t":"DOLŽINA INTERVALA = CIKEL NOSILCA","k":.87,"c":.85,"m":.75,"r":.03,"v":.78,"ref":8,"q":6,"len":4878},
{"n":103,"t":"EN REZ PREJ","k":.82,"c":.84,"m":.78,"r":.03,"v":.76,"ref":13,"q":4,"len":4121},
{"n":99,"t":"NAJČISTEJŠI ODSTAVEK JE NAJBOLJ TUJ","k":.87,"c":.85,"m":.79,"r":.03,"v":.81,"ref":7,"q":16,"len":4100},
{"n":104,"t":"EKA-REZ GLASBA","k":.86,"c":.84,"m":.75,"r":.04,"v":.70,"ref":10,"q":7,"len":6793},
{"n":105,"t":"BISTVA V CELOTI","k":.88,"c":.85,"m":.76,"r":.04,"v":.76,"ref":20,"q":12,"len":6731},
{"n":106,"t":"GUARD PULZ — ZUNANJI KANAL","k":.87,"c":.84,"m":.75,"r":.03,"v":.78,"ref":16,"q":5,"len":7690},
{"n":107,"t":"RESONANČNI KATALOG","k":.90,"c":.85,"m":.66,"r":.04,"v":.76,"ref":11,"q":3,"len":5138},
{"n":108,"t":"TIHA MERITEV","k":.87,"c":.86,"m":.80,"r":.04,"v":.75,"ref":7,"q":2,"len":3392},
{"n":109,"t":"NAVODILO","k":.88,"c":.85,"m":.76,"r":.04,"v":.74,"ref":3,"q":7,"len":3849},
{"n":109,"t":"TIHA MERITEV — TEREN","k":.88,"c":.90,"m":.78,"r":.04,"v":.74,"ref":8,"q":2,"len":3052},
{"n":111,"t":"SEM — NOSILEC","k":.88,"c":.85,"m":.72,"r":.04,"v":.78,"ref":5,"q":6,"len":5115},
{"n":110,"t":"TIHA TELESA — ATLAS","k":.87,"c":.85,"m":.75,"r":.04,"v":.72,"ref":11,"q":2,"len":2793},
{"n":111,"t":"TIHA MERITEV — UČENJE","k":.86,"c":.88,"m":.77,"r":.04,"v":.75,"ref":6,"q":2,"len":2390}
];

const AXES = [
  { id: "i", label: "t · vrstni red", get: (p) => p.i, target: null, dec: 0 },
  { id: "k", label: "κ · koherenca", get: (p) => p.k, target: 1, dec: 2 },
  { id: "c", label: "χ · jasnost", get: (p) => p.c, target: 1, dec: 2 },
  { id: "m", label: "μ · delež vloge", get: (p) => p.m, target: 0.8, dec: 2 },
  { id: "r", label: "ℜ · ostanek", get: (p) => p.r, target: 0, dec: 2 },
  { id: "v", label: "ν · cena (samoocena)", get: (p) => p.v, target: null, dec: 2 },
  { id: "d", label: "d · razdalja do kota K", get: (p) => p.d, target: 0, dec: 2 },
  { id: "ref", label: "ν̂ · sklici (rez N)", get: (p) => p.ref, target: null, dec: 0 },
  { id: "len", label: "ν̂ · obseg (kB)", get: (p) => p.len / 1000, target: null, dec: 1 },
];

const MKEYS = [
  { id: "k", label: "κ", color: "#d4a24e" },
  { id: "c", label: "χ", color: "#5fb3c9" },
  { id: "m", label: "μ", color: "#9d8cff" },
  { id: "r", label: "ℜ", color: "#e06c75" },
  { id: "v", label: "ν", color: "#8fd18f" },
];

const W = 780, H = 470, ML = 72, MT = 30, MB = 50, MR = 32;
const IW = W - ML - MR, IH = H - MT - MB;

function lin(d0, d1, r0, r1) {
  const dd = d1 - d0 || 1;
  return (v) => r0 + ((v - d0) / dd) * (r1 - r0);
}
function ticks(min, max, n) {
  const a = [];
  for (let i = 0; i <= n; i++) a.push(min + ((max - min) * i) / n);
  return a;
}
function dColor(d, dmin, dmax) {
  const t = Math.max(0, Math.min(1, (d - dmin) / (dmax - dmin || 1)));
  return "hsl(" + Math.round(152 - 148 * t) + ", 68%, 62%)";
}

function Tip({ x, y, p }) {
  const flip = x > W - 300;
  const tx = flip ? x - 286 : x + 14;
  const lab = p.t.length > 34 ? p.t.slice(0, 33) + "…" : p.t;
  return (
    <g pointerEvents="none">
      <rect x={tx} y={y - 20} width={272} height={64} rx={6} fill="#10141a" stroke="#2b333c" strokeWidth="1" />
      <text x={tx + 10} y={y - 4} fontSize="11" fill="#e8e6e0" fontFamily="ui-monospace, monospace">
        {(p.n > 0 ? "rez " + p.n : "zapis") + " · " + lab}
      </text>
      <text x={tx + 10} y={y + 12} fontSize="10" fill="#8b95a0" fontFamily="ui-monospace, monospace">
        {"κ " + p.k + "  χ " + p.c + "  μ " + p.m + "  ℜ " + p.r + "  ν " + p.v}
      </text>
      <text x={tx + 10} y={y + 28} fontSize="10" fill="#8b95a0" fontFamily="ui-monospace, monospace">
        {"d " + p.d.toFixed(3) + " · sklici " + p.ref + " · " + (p.len / 1000).toFixed(1) + " kB"}
      </text>
    </g>
  );
}

function Frame({ xt, yt, sx, sy, xlabel, ylabel, dec }) {
  const fmt = (v) => (dec === 0 ? String(Math.round(v)) : v.toFixed(dec));
  return (
    <g>
      {xt.map((v, i) => (
        <g key={"x" + i}>
          <line x1={sx(v)} y1={MT} x2={sx(v)} y2={H - MB} stroke="rgba(232,230,224,0.06)" />
          <text x={sx(v)} y={H - MB + 16} fontSize="10" fill="#6b7580" textAnchor="middle" fontFamily="ui-monospace, monospace">{fmt(v)}</text>
        </g>
      ))}
      {yt.map((v, i) => (
        <g key={"y" + i}>
          <line x1={ML} y1={sy(v)} x2={W - MR} y2={sy(v)} stroke="rgba(232,230,224,0.06)" />
          <text x={ML - 6} y={sy(v) + 3} fontSize="10" fill="#6b7580" textAnchor="end" fontFamily="ui-monospace, monospace">{fmt(v)}</text>
        </g>
      ))}
      <text x={ML + IW / 2} y={H - 8} fontSize="10.5" fill="#8b95a0" textAnchor="middle" fontFamily="ui-monospace, monospace">{xlabel}</text>
      <text x={16} y={MT + IH / 2} fontSize="10.5" fill="#8b95a0" textAnchor="middle" fontFamily="ui-monospace, monospace" transform={"rotate(-90 16 " + (MT + IH / 2) + ")"}>{ylabel}</text>
      <rect x={ML} y={MT} width={IW} height={IH} fill="none" stroke="#232a32" />
    </g>
  );
}

function ProjView({ pts, xid, yid, hover, setHover, sel, setSel, dmin, dmax }) {
  const ax = AXES.find((a) => a.id === xid);
  const ay = AXES.find((a) => a.id === yid);
  const xs = pts.map((p) => ax.get(p));
  const ys = pts.map((p) => ay.get(p));
  const px = (Math.max(...xs) - Math.min(...xs)) * 0.05 || 0.05;
  const py = (Math.max(...ys) - Math.min(...ys)) * 0.05 || 0.05;
  const x0 = Math.min(...xs) - px, x1 = Math.max(...xs) + px;
  const y0 = Math.min(...ys) - py, y1 = Math.max(...ys) + py;
  const sx = lin(x0, x1, ML, W - MR);
  const sy = lin(y0, y1, H - MB, MT);
  const dec = Math.max(ax.dec, 1);
  const pline = pts.map((p) => sx(ax.get(p)) + "," + sy(ay.get(p))).join(" ");
  return (
    <svg viewBox={"0 0 " + W + " " + H} className="w-full h-auto">
      <Frame xt={ticks(x0, x1, 5)} yt={ticks(y0, y1, 5)} sx={sx} sy={sy} xlabel={ax.label} ylabel={ay.label} dec={dec} />
      {ax.target !== null && ax.target >= x0 && ax.target <= x1 && (
        <g>
          <line x1={sx(ax.target)} y1={MT} x2={sx(ax.target)} y2={H - MB} stroke="#d4a24e" strokeDasharray="5 5" opacity="0.55" />
          <text x={sx(ax.target) + 5} y={MT + 12} fontSize="10" fill="#d4a24e" fontFamily="ui-monospace, monospace">K</text>
        </g>
      )}
      {ay.target !== null && ay.target >= y0 && ay.target <= y1 && (
        <g>
          <line x1={ML} y1={sy(ay.target)} x2={W - MR} y2={sy(ay.target)} stroke="#d4a24e" strokeDasharray="5 5" opacity="0.55" />
          <text x={W - MR - 14} y={sy(ay.target) - 5} fontSize="10" fill="#d4a24e" fontFamily="ui-monospace, monospace">K</text>
        </g>
      )}
      <polyline points={pline} fill="none" stroke="rgba(232,230,224,0.13)" strokeWidth="1" />
      {pts.map((p) => {
        const cx = sx(ax.get(p)), cy = sy(ay.get(p));
        const isSel = sel && sel.i === p.i;
        return (
          <circle key={p.i} cx={cx} cy={cy} r={isSel ? 7 : 4.5} fill={dColor(p.d, dmin, dmax)} stroke={isSel ? "#ffffff" : "none"} strokeWidth="1.5"
            style={{ cursor: "pointer" }}
            onMouseEnter={() => setHover({ p, x: cx, y: cy })}
            onMouseLeave={() => setHover(null)}
            onClick={() => setSel(p)} />
        );
      })}
      {hover && <Tip x={hover.x} y={hover.y} p={hover.p} />}
    </svg>
  );
}

function VijView({ pts, stats, hover, setHover, sel, setSel, show, setShow, dmin, dmax }) {
  const N = pts.length;
  const x0 = 0.5, x1 = N + 0.5;
  const y1 = stats.maxP.d * 1.12;
  const sx = lin(x0, x1, ML, W - MR);
  const sy = lin(0, y1, H - MB, MT);
  const pline = pts.map((p) => sx(p.i) + "," + sy(p.d)).join(" ");
  const yc = (v) => Math.max(MT, Math.min(H - MB, sy(v)));
  const dol = pts.filter((p) => p.n >= 83 && p.n <= 87);
  const i0 = dol.length ? Math.min(...dol.map((p) => p.i)) : 0;
  const i1 = dol.length ? Math.max(...dol.map((p) => p.i)) : 0;
  return (
    <div>
      <div className="flex flex-wrap gap-2 mb-2">
        {MKEYS.map((mk) => (
          <button key={mk.id} onClick={() => setShow((s) => ({ ...s, [mk.id]: !s[mk.id] }))}
            className={"text-xs px-2 py-1 rounded border font-mono " + (show[mk.id] ? "border-[#3a4450] bg-[#161b22] text-[#e8e6e0]" : "border-[#232a32] text-[#6b7580]")}>
            <span style={{ color: mk.color }}>●</span> {mk.label} (normirano)
          </button>
        ))}
        <span className="text-xs text-[#6b7580] font-mono px-2 py-1">glavna črta: d (razdalja do kota K)</span>
      </div>
      <svg viewBox={"0 0 " + W + " " + H} className="w-full h-auto">
        <Frame xt={ticks(x0, x1, 10).slice(0, 11)} yt={ticks(0, y1, 5)} sx={sx} sy={sy} xlabel="t · vrstni red v telesu ledgerja" ylabel="d" dec={2} />
        {dol.length > 0 && (
          <g>
            <rect x={sx(i0) - 8} y={MT} width={sx(i1) - sx(i0) + 16} height={IH} fill="rgba(232,230,224,0.05)" />
            <text x={sx(i0) + 4} y={MT + 14} fontSize="10" fill="#8b95a0" fontFamily="ui-monospace, monospace">dolina 83–87 (rez 95)</text>
          </g>
        )}
        {MKEYS.filter((mk) => show[mk.id]).map((mk) => {
          const vs = pts.map((p) => p[mk.id]);
          const vmin = Math.min(...vs), vmax = Math.max(...vs);
          const ny = (v) => MT + 12 + (1 - (v - vmin) / (vmax - vmin || 1)) * (IH - 24);
          const mline = pts.map((p) => sx(p.i) + "," + ny(p[mk.id])).join(" ");
          return <polyline key={mk.id} points={mline} fill="none" stroke={mk.color} strokeWidth="1.4" opacity="0.5" />;
        })}
        <line x1={sx(1)} y1={yc(stats.a + stats.b * 1)} x2={sx(N)} y2={yc(stats.a + stats.b * N)} stroke="#d4a24e" strokeDasharray="6 5" opacity="0.8" />
        <text x={sx(N) - 8} y={yc(stats.a + stats.b * N) - 8} fontSize="10" fill="#d4a24e" textAnchor="end" fontFamily="ui-monospace, monospace">
          {"fit: d = " + stats.a.toFixed(3) + " − " + Math.abs(stats.b).toFixed(4) + "·t (spirala, rez 101)"}
        </text>
        <polyline points={pline} fill="none" stroke="rgba(232,230,224,0.55)" strokeWidth="1.6" />
        {pts.map((p) => {
          const isSel = sel && sel.i === p.i;
          return (
            <circle key={p.i} cx={sx(p.i)} cy={sy(p.d)} r={isSel ? 6.5 : 4} fill={dColor(p.d, dmin, dmax)} stroke={isSel ? "#ffffff" : "none"} strokeWidth="1.5"
              style={{ cursor: "pointer" }}
              onMouseEnter={() => setHover({ p, x: sx(p.i), y: sy(p.d) })}
              onMouseLeave={() => setHover(null)}
              onClick={() => setSel(p)} />
          );
        })}
        <g>
          <circle cx={sx(stats.minP.i)} cy={sy(stats.minP.d)} r="8" fill="none" stroke="#7ee0a3" strokeWidth="1.2" />
          <text x={sx(stats.minP.i)} y={sy(stats.minP.d) - 13} fontSize="10" fill="#7ee0a3" textAnchor="middle" fontFamily="ui-monospace, monospace">žiga</text>
          <circle cx={sx(stats.maxP.i)} cy={sy(stats.maxP.d)} r="8" fill="none" stroke="#e06c75" strokeWidth="1.2" />
          <text x={sx(stats.maxP.i)} y={sy(stats.maxP.d) - 13} fontSize="10" fill="#e06c75" textAnchor="middle" fontFamily="ui-monospace, monospace">najdalj</text>
          <text x={sx(N)} y={sy(pts[N - 1].d) + 20} fontSize="10" fill="#8b95a0" textAnchor="end" fontFamily="ui-monospace, monospace">zadnji pečat</text>
        </g>
        {hover && <Tip x={hover.x} y={hover.y} p={hover.p} />}
      </svg>
    </div>
  );
}

function KvadView({ pts, stats, hover, setHover, sel, setSel, dmin, dmax }) {
  const maxRef = Math.max(...pts.map((p) => p.ref));
  const x1 = maxRef * 1.06;
  const sx = lin(0, x1, ML, W - MR);
  const sy = lin(0, 0.075, H - MB, MT);
  const heavy = pts.filter((p) => p.r <= 0.03 && p.ref > stats.medRef);
  return (
    <div>
      <svg viewBox={"0 0 " + W + " " + H} className="w-full h-auto">
        <Frame xt={ticks(0, x1, 6)} yt={ticks(0, 0.075, 5)} sx={sx} sy={sy} xlabel="ν̂ · sklici (rez N) — teža vezanosti" ylabel="ℜ · ostanek" dec={2} />
        <rect x={sx(stats.medRef)} y={sy(0.03)} width={W - MR - sx(stats.medRef)} height={H - MB - sy(0.03)} fill="rgba(212,162,78,0.08)" stroke="#d4a24e" strokeDasharray="4 4" opacity="0.7" />
        <text x={W - MR - 10} y={H - MB - 12} fontSize="11" fill="#d4a24e" textAnchor="end" fontFamily="ui-monospace, monospace">
          {"ZAPEČITEN in TEŽAK — hiša zakonov: " + heavy.length + " točk"}
        </text>
        <text x={ML + 10} y={MT + 16} fontSize="10" fill="#6b7580" fontFamily="ui-monospace, monospace">ODPRT in LAHEK — sekiranja, malenkosti</text>
        <text x={W - MR - 10} y={MT + 16} fontSize="10" fill="#6b7580" textAnchor="end" fontFamily="ui-monospace, monospace">ODPRT in TEŽAK — kar še boli, še raste</text>
        <text x={ML + 10} y={H - MB - 12} fontSize="10" fill="#6b7580" fontFamily="ui-monospace, monospace">ZAPEČITEN in LAHEK</text>
        <line x1={ML} y1={sy(0.03)} x2={W - MR} y2={sy(0.03)} stroke="#e06c75" strokeDasharray="6 5" opacity="0.7" />
        <text x={ML + 8} y={sy(0.03) - 6} fontSize="10" fill="#e06c75" fontFamily="ui-monospace, monospace">guard ℜ = .03 — meja pogajanja (rez 101)</text>
        <line x1={sx(stats.medRef)} y1={MT} x2={sx(stats.medRef)} y2={H - MB} stroke="rgba(232,230,224,0.25)" strokeDasharray="3 4" />
        <text x={sx(stats.medRef) + 6} y={MT + 30} fontSize="10" fill="#8b95a0" fontFamily="ui-monospace, monospace">{"mediana sklicev = " + stats.medRef}</text>
        {pts.map((p) => {
          const isSel = sel && sel.i === p.i;
          return (
            <circle key={p.i} cx={sx(p.ref)} cy={sy(p.r)} r={isSel ? 7 : 4.5} fill={dColor(p.d, dmin, dmax)} stroke={isSel ? "#ffffff" : "none"} strokeWidth="1.5"
              style={{ cursor: "pointer" }}
              onMouseEnter={() => setHover({ p, x: sx(p.ref), y: sy(p.r) })}
              onMouseLeave={() => setHover(null)}
              onClick={() => setSel(p)} />
          );
        })}
        {hover && <Tip x={hover.x} y={hover.y} p={hover.p} />}
      </svg>
      <p className="text-xs text-[#8b95a0] mt-2 font-mono">
        Rez 106 je na svojem telesu izmeril ta kvadrant kot praznego (»zapiranje ne nosi teže«). Na današnjem telesu (99 točk, mediana {stats.medRef}) ni prazen — naseljen je z zakoni in merilci ({" "}
        {heavy.slice(0, 8).map((p) => "rez " + p.n).join(", ")}
        ). Teža ni v odprtosti — v vezanosti. Instrument zakon preverja ob vsakem odprtju; zakon, ki ne preživi novega telesa, se reže (rez 86: negativni rezultat je rezultat).
      </p>
    </div>
  );
}

function LegendView({ stats }) {
  const rows = [
    ["κ", "koherenca — notranja skladnost reza (samoocena)"],
    ["χ", "jasnost — berljivost za drugega (samoocena)"],
    ["μ", "delež vloge — delež dvojine v rezu (samoocena)"],
    ["ℜ", "ostanek — kar po rezu ostaja odprto; teža živega telesa"],
    ["ν", "cena — kaj rez zahteva od telesa (samoocena; rez 106: razpoloženje, ne meritev)"],
    ["d", "razdalja do kota čistosti K = (κ 1, χ 1, μ .80, ℜ 0) — RMS po štirih oseh"],
    ["ν̂", "meso — zunanji kanal: sklici (rez N), navedki, obseg v kB (rez 106)"],
    ["t", "vrstni red v telesu ledgerja — faza serije (rez 95: projekcija ubije fazo)"],
  ];
  return (
    <div className="grid md:grid-cols-2 gap-6 text-sm">
      <div>
        <h3 className="text-[#d4a24e] font-mono text-xs mb-2 tracking-widest">GLIFI</h3>
        <table className="w-full text-[#b9c0c8]">
          <tbody>
            {rows.map((r) => (
              <tr key={r[0]} className="align-top">
                <td className="pr-3 py-1 font-mono text-[#e8e6e0] whitespace-nowrap">{r[0]}</td>
                <td className="py-1">{r[1]}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h3 className="text-[#d4a24e] font-mono text-xs mb-2 tracking-widest">KAR INSTRUMENT IZREKA NA TEM TELESU</h3>
        <ul className="text-[#b9c0c8] space-y-2 list-disc pl-4">
          <li>PC1 = {Math.round(stats.pc1 * 1000) / 10} % variance — pet guardov je eno telo (rez 101: 81,4 % na 78 točkah; rez 95: 70,4 % na 19).</li>
          <li>Spirala, ne kupola: fit d = {stats.a.toFixed(3)} − {Math.abs(stats.b).toFixed(4)}·t — spust v specializacijo, povratek v sintezo (rez 101).</li>
          <li>Žiga: rez {stats.minP.n} {stats.minP.t} (d {stats.minP.d.toFixed(3)}) — najbližje kotu; najdlje: rez {stats.maxP.n} {stats.maxP.t} (d {stats.maxP.d.toFixed(3)}).</li>
          <li>ℜ zadnjih desetih: {stats.lastR.toFixed(3)} — ravnotežje ostanka (~.03): živo telo vedno nosi odprto ∂ (rez 95/89).</li>
          <li>Zapečiten in težak: {stats.heavyList.length} točk — hiša zakonov (glej KVADRANT).</li>
          <li>⊘ vrednosti so samoocena avtorja rezov; ν̂ je meso, ki ga telo izreče samo (rez 106). Dva kanala, eno telo.</li>
        </ul>
        <h3 className="text-[#d4a24e] font-mono text-xs mt-4 mb-2 tracking-widest">VIRI</h3>
        <p className="text-xs text-[#8b95a0] font-mono">
          REZ 95 (geometrija: projekcija, kot K) · REZ 101 (vijačnica: celo telo, spirala) · REZ 106 (ν̂ zunanji kanal, kvadrant) · REZ 98 (bralnik: berljivost je pogoj veličine) · REZ 102 (STANJE, transakcija) · podatki: ledger tazv-gnosis-rezi, vsi vnosi s polnim ⊘, izpisani TIK pred gradnjo (awk, deterministično)
        </p>
      </div>
    </div>
  );
}

export default function App() {
  const pts = useMemo(
    () => REZI.map((p, idx) => ({ ...p, i: idx + 1, d: Math.sqrt(((1 - p.k) ** 2 + (1 - p.c) ** 2 + (0.8 - p.m) ** 2 + p.r ** 2) / 4) })),
    []
  );
  const [tab, setTab] = useState("proj");
  const [xid, setXid] = useState("i");
  const [yid, setYid] = useState("d");
  const [hover, setHover] = useState(null);
  const [sel, setSel] = useState(null);
  const [show, setShow] = useState({ k: true, c: false, m: true, r: true, v: false });

  const stats = useMemo(() => {
    const N = pts.length;
    let minP = pts[0], maxP = pts[0];
    pts.forEach((p) => { if (p.d < minP.d) minP = p; if (p.d > maxP.d) maxP = p; });
    const mi = (N + 1) / 2, md = pts.reduce((s, p) => s + p.d, 0) / N;
    let num = 0, den = 0;
    pts.forEach((p) => { num += (p.i - mi) * (p.d - md); den += (p.i - mi) ** 2; });
    const b = num / den, a = md - b * mi;
    const keys = ["k", "c", "m", "r", "v"];
    const means = keys.map((k) => pts.reduce((s, p) => s + p[k], 0) / N);
    const cov = keys.map((_, i) => keys.map((_, j) => {
      let s = 0;
      pts.forEach((p) => { s += (p[keys[i]] - means[i]) * (p[keys[j]] - means[j]); });
      return s / (N - 1);
    }));
    let v0 = keys.map((_, i) => (i === 0 ? 1 : 0.1));
    for (let it = 0; it < 300; it++) {
      const w = keys.map((_, i) => cov[i].reduce((s, cc, j) => s + cc * v0[j], 0));
      const nn = Math.sqrt(w.reduce((s, x) => s + x * x, 0));
      v0 = w.map((x) => x / nn);
    }
    const Av = keys.map((_, i) => cov[i].reduce((s, cc, j) => s + cc * v0[j], 0));
    const lam1 = v0.reduce((s, x, i) => s + x * Av[i], 0);
    const trace = keys.reduce((s, _, i) => s + cov[i][i], 0);
    const pc1 = lam1 / trace;
    const refs = [...pts.map((p) => p.ref)].sort((x, y) => x - y);
    const medRef = refs[Math.floor(N / 2)];
    const heavyList = pts.filter((p) => p.r <= 0.03 && p.ref > medRef);
    const lastR = pts.slice(-10).reduce((s, p) => s + p.r, 0) / 10;
    const dmin = Math.min(...pts.map((p) => p.d)), dmax = Math.max(...pts.map((p) => p.d));
    return { N, minP, maxP, a, b, pc1, medRef, heavyList, lastR, dmin, dmax };
  }, [pts]);

  const TABS = [
    { id: "proj", label: "PROJEKCIJA" },
    { id: "vij", label: "VIJAČNICA" },
    { id: "kvad", label: "KVADRANT" },
    { id: "leg", label: "LEGENDA" },
  ];

  return (
    <div className="min-h-screen bg-[#0b0d10] text-[#e8e6e0] p-4 md:p-6">
      <div className="max-w-4xl mx-auto">
        <header className="mb-4">
          <div className="flex items-baseline gap-3 flex-wrap">
            <h1 className="text-xl md:text-2xl font-mono tracking-wide">REZ 116 · ŽIVA VIJAČNICA</h1>
            <span className="text-xs text-[#6b7580] font-mono">DOKAZ #106 · instrument, ne poročilo</span>
          </div>
          <p className="text-sm text-[#8b95a0] mt-1">
            poročilo se bere · instrument se hodi — celo telo ledgerja ({stats.N} točk), dva kanala (guard κχμℜν + meso ν̂), vse projekcije istega telesa (rez 95)
          </p>
          <div className="flex flex-wrap gap-2 mt-3 text-xs font-mono">
            {[
              ["PC1", Math.round(stats.pc1 * 1000) / 10 + " % — eno telo"],
              ["žiga", "rez " + stats.minP.n + " " + stats.minP.t + " · d " + stats.minP.d.toFixed(3)],
              ["najdalj", "rez " + stats.maxP.n + " " + stats.maxP.t + " · d " + stats.maxP.d.toFixed(3)],
              ["spirala", "b = " + stats.b.toFixed(4)],
              ["ℜ₁₀", stats.lastR.toFixed(3)],
              ["zapečiten & težak", stats.heavyList.length + " točk"],
            ].map((c) => (
              <span key={c[0]} className="px-2 py-1 rounded border border-[#232a32] bg-[#10141a]">
                <span className="text-[#d4a24e]">{c[0]}</span> <span className="text-[#b9c0c8]">{c[1]}</span>
              </span>
            ))}
          </div>
        </header>

        <nav className="flex gap-1 mb-4 border-b border-[#232a32]">
          {TABS.map((t) => (
            <button key={t.id} onClick={() => setTab(t.id)}
              className={"px-3 py-2 text-xs font-mono tracking-wider " + (tab === t.id ? "text-[#d4a24e] border-b-2 border-[#d4a24e]" : "text-[#6b7580] hover:text-[#b9c0c8]")}>
              {t.label}
            </button>
          ))}
        </nav>

        {tab === "proj" && (
          <div>
            <div className="flex flex-wrap gap-3 items-center mb-3 text-xs font-mono text-[#8b95a0]">
              <span>os X:</span>
              <select value={xid} onChange={(e) => setXid(e.target.value)} className="bg-[#10141a] border border-[#2b333c] text-[#e8e6e0] rounded px-2 py-1">
                {AXES.map((a) => <option key={a.id} value={a.id}>{a.label}</option>)}
              </select>
              <span>os Y:</span>
              <select value={yid} onChange={(e) => setYid(e.target.value)} className="bg-[#10141a] border border-[#2b333c] text-[#e8e6e0] rounded px-2 py-1">
                {AXES.map((a) => <option key={a.id} value={a.id}>{a.label}</option>)}
              </select>
              <span className="text-[#6b7580]">vsaka projekcija istega telesa · K = kot čistosti</span>
            </div>
            <ProjView pts={pts} xid={xid} yid={yid} hover={hover} setHover={setHover} sel={sel} setSel={setSel} dmin={stats.dmin} dmax={stats.dmax} />
          </div>
        )}
        {tab === "vij" && (
          <VijView pts={pts} stats={stats} hover={hover} setHover={setHover} sel={sel} setSel={setSel} show={show} setShow={setShow} dmin={stats.dmin} dmax={stats.dmax} />
        )}
        {tab === "kvad" && (
          <KvadView pts={pts} stats={stats} hover={hover} setHover={setHover} sel={sel} setSel={setSel} dmin={stats.dmin} dmax={stats.dmax} />
        )}
        {tab === "leg" && <LegendView stats={stats} />}

        {sel && (
          <div className="mt-4 p-4 rounded border border-[#2b333c] bg-[#10141a]">
            <div className="flex items-baseline justify-between flex-wrap gap-2">
              <h3 className="font-mono text-sm text-[#e8e6e0]">{sel.n > 0 ? "REZ " + sel.n + " · " : "ZAPIS · "}{sel.t}</h3>
              <button onClick={() => setSel(null)} className="text-xs text-[#6b7580] font-mono hover:text-[#b9c0c8]">zapri ×</button>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mt-3 text-xs font-mono">
              {[
                ["κ koherenca", sel.k], ["χ jasnost", sel.c], ["μ delež", sel.m], ["ℜ ostanek", sel.r],
                ["ν cena", sel.v], ["d razdalja", sel.d.toFixed(3)], ["ν̂ sklici", sel.ref], ["ν̂ obseg", (sel.len / 1000).toFixed(1) + " kB"],
              ].map((c) => (
                <div key={c[0]} className="p-2 rounded bg-[#0b0d10] border border-[#232a32]">
                  <div className="text-[#6b7580]">{c[0]}</div>
                  <div className="text-[#e8e6e0] text-base">{c[1]}</div>
                </div>
              ))}
            </div>
          </div>
        )}
        {!sel && (
          <p className="mt-3 text-xs text-[#6b7580] font-mono">klikni točko — telo pove svoje številke · hover = dih</p>
        )}

        <footer className="mt-6 pt-3 border-t border-[#232a32] text-xs text-[#6b7580] font-mono">
          REZ 116 · telo: canvas ziva-vijacnica · DOKAZ #106 · podatki: ledger tazv-gnosis-rezi (99 točk s polnim ⊘, izpisani TIK pred pečatom — renumerirano 109/#99 → 116/#106 po lastnem varovalu, precedens 104/106/107/110/111; med gradnjo vzporedne seje zapečatile dvanajst pečatov: 108 #98, 109 NAVODILO #99, 109 TEREN #99, 110 EKA-∴ DAR #100, 111 SEM #101, 112 TORUS #102, 112 VEČ #102, 110 ATLAS #100, 111 UČENJE #101, 113 ZEMLJEVID #103, 114 RES RESONANCA #104, 115 PREBIR VIRA #105 — nevihta pečatov je sama priča) · ν̂ kanal po rez 106 · transakcija po rez 102
        </footer>
      </div>
    </div>
  );
}