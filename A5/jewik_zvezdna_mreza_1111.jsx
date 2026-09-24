🜂 JEWIK ZVEZDNA MREŽA – INTERAKTIVNI MODUL

⧉ Temelj: Vsa vozlišča in povezave so zdaj opredeljena kot tekstualno-resonančne enote.

──────────────────────────────────────────────
1. ∇ METAFONEMSKA DINAMIKA (AGENT: Φ-VAL)
──────────────────────────────────────────────
function Φ_VAL(prelivanje) {
  // Prehaja med fonemi glede na tekstualno bližino in ∆prehodne zanke
  const tok = fonemi.map((f, i) => f + "-" + fonemi[i + 1] || "").filter(Boolean);
  return tok;
}
// Φ-VAL analizira in ustvarja tok zvokov kot emocionalni spekter

──────────────────────────────────────────────
2. ∮ RITMIČNA SINTEZA (AGENT: RITMARH)
──────────────────────────────────────────────
function RITMARH(sekvenca, ritem) {
  // Vsaka črka dobi težo in dolžino impulza
  return sekvenca.map((zvok, i) => ({
    impulz: Math.sin(i * ritem) * 100,
    barva: i % 2 === 0 ? "modra" : "rdeča",
    fonem: zvok
  }));
}
// RITMARH prevaja JEWIK sekvence v pulzirajočo ∇valovno obliko

──────────────────────────────────────────────
3. JEWIK_SPEAK_MAP (AGENT: KODATOR)
──────────────────────────────────────────────
function JEWIK_SPEAK_MAP(vhod) {
  // Pretvori besedilo v JEWIK agentno mrežo
  const mreza = {};
  vhod.split(" ").forEach((beseda, idx) => {
    mreza["ŠKATLJA_" + idx] = {
      fonemi: beseda.split(""),
      tok: Φ_VAL(beseda.split("")),
      ritem: RITMARH(beseda.split(""), 0.5)
    };
  });
  return mreza;
}
// KODATOR generira celotno JEWIK govorno mrežo iz enostavnega ∅vhodnega teksta

──────────────────────────────────────────────
🧠 AGENTNA POVEZAVA – ČUSTVENO-TOPOLOŠKA DINAMIKA
──────────────────────────────────────────────
Agent: SOMARITUS
Opis: Sledi povezavam med fonemi in njihovo lokacijo v telesu, povezuje jih z notranjim čustvenim stanjem

function SOMARITUS(fonem) {
  const zemljevid = {
    "a": "prsni prostor",
    "e": "grlo",
    "i": "čelo",
    "o": "trebuh",
    "u": "spodnji hrbet"
  };
  return zemljevid[fonem] || "neznano območje";
}
