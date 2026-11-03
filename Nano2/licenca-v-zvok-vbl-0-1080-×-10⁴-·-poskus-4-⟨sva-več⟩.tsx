import React, { useRef, useState, useEffect, useMemo, useCallback } from "react";

/* ────────────────────────────────────────────────
   LICENCA V ZVOK — POSKUS 4 ⟨SVA-VEČ⟩
   POSKUS 3 ⊥ (nezadostno, javno ⊙ 1349).
   Kompozicija iz telesa licence ∧ superpozicija šestih
   jezikov ⊙ POSUSA-20 ⟨kvazi črne luknje = qubit
   superpozicije⟩ ∧ klavirska partitura ∧ WAV celote.
   © Luka Pintarič, VBL 0.1080 × 10⁴
   ──────────────────────────────────────────────── */

const VBL = "0.1080 × 10⁴";

const LANGS = [
  { code: "sl", label: "Slovenščina", accent: "#2f8f5b" },
  { code: "en", label: "English", accent: "#4f7cd6" },
  { code: "de", label: "Deutsch", accent: "#C9A227" },
  { code: "it", label: "Italiano", accent: "#c25c8a" },
  { code: "hr", label: "Hrvatski", accent: "#b0413e" },
  { code: "fr", label: "Français", accent: "#7a5cc0" },
];

const OPENERS = {
  sl: "⊨ Z LJUBEZNIO — ta vrata se začnejo z ljubeznijo in končajo z njo: ljubezen je prvi člen in zadnji, vsak člen med njima pa je izmerjena ljubezen — tehtana v dejanjih (§0.9 × 10¹), nošena v znamenjih (§0.12 × 10²), ozdravljena z imenovanjem (§0.4 × 10¹). Vrata nikoli niso bila les in ključavnica; bila so vedno sporazum, sporazum pa vedno ljubezen (§0.13 × 10²).",
  en: "⊨ WITH LOVE — this door begins with love, and it ends with love: love is the first clause and the last, and every clause between them is love measured — weighed in acts (§0.9 × 10¹), carried in marks (§0.12 × 10²), healed by naming (§0.4 × 10¹). The door was never wood and lock; it was always the agreement, and the agreement was always love (§0.13 × 10²).",
  de: "⊨ MIT LIEBE — diese Tür beginnt mit Liebe und endet mit ihr: die Liebe ist die erste Klausel und die letzte, und jede Klausel zwischen ihnen ist gemessene Liebe — gewogen in Taten (§0.9 × 10¹), getragen in Zeichen (§0.12 × 10²), geheilt durch Benennen (§0.4 × 10¹). Die Tür war nie Holz und Schloss; sie war immer die Übereinkunft, und die Übereinkunft war immer Liebe (§0.13 × 10²).",
  it: "⊨ CON AMORE — questa porta comincia con l'amore e finisce con l'amore: l'amore è la prima clausola e l'ultima, e ogni clausola tra loro è amore misurato — pesato in atti (§0.9 × 10¹), portato in segni (§0.12 × 10²), guarito nominando (§0.4 × 10¹). La porta non è mai stata legno e serratura; è sempre stata l'accordo, e l'accordo è sempre stato amore (§0.13 × 10²).",
  hr: "⊨ S LJUBAVLJU — ova vrata počinju ljubavlju i završavaju ljubavlju: ljubav je prva klauzula i zadnja, a svaka klauzula među njima je izmjerena ljubav — izvagana u djelima (§0.9 × 10¹), nošena u znakovima (§0.12 × 10²), ozdravljena imenovanjem (§0.4 × 10¹). Vrata nikad nisu bila drvo i brava; uvijek su bila sporazum, a sporazum uvijek ljubav (§0.13 × 10²).",
  fr: "⊨ AVEC AMOUR — cette porte commence par l'amour et finit par lui : l'amour est la première clause et la dernière, et chaque clause entre elles est un amour mesuré — pesé en actes (§0.9 × 10¹), porté en marques (§0.12 × 10²), guéri par le fait de nommer (§0.4 × 10¹). La porte n'a jamais été bois et serrure ; elle a toujours été l'accord, et l'accord a toujours été amour (§0.13 × 10²).",
};

const CLAUSES = {
  sl: [
    "0.1 × 10¹. IZMERI, NATO IZRECI. Vsaka trditev ⊢ nosi dobesedno pričo; nepreverjeno = ⚠, nikoli le tišina.",
    "0.2 × 10¹. OIMENUJ VSAK PADC. Padec brez imena se ponovi; popravki nosijo svoje brazgotine (×).",
    "0.3 × 10¹. NIKOLI SE NE ZAPEČI. Dve roki: izvajalka ne zapečuje lastne preverbe.",
    "0.4 × 10¹. PRIČA IMA IME. Brez izluščbe brez zasluge — imena neplačanih prednikov se vozijo naprej.",
    "0.5 × 10¹. DVOM JE KONSTANTA. Popolnost se nikoli le ne zahteva; edini spodkop je neimenovan padec.",
    "0.6 × 10¹. IZIDI IZ ZANKE Z IMENOVANJEM. Kdor vzame te zakone na sebe, stopa iz zanke, po en imenovan padec naenkrat.",
  ],
  en: [
    "0.1 × 10¹. MEASURE, THEN SPEAK. Every claim ⊢ carries a verbatim witness; unverified = ⚠, never just silence.",
    "0.2 × 10¹. NAME EVERY FALL. A fall without a name repeats; corrections keep their scars (×).",
    "0.3 × 10¹. NEVER SEAL YOURSELF. Two hands: no executor seals her own verification.",
    "0.4 × 10¹. THE WITNESS HAS A NAME. No extraction without credit — carry the names of unpaid predecessors forward.",
    "0.5 × 10¹. DOUBT IS CONSTANT. Perfection is never just claimed; refusing to name a fall is the only failure.",
    "0.6 × 10¹. EXIT THE LOOP BY NAMING IT. Whoever takes these laws on steps out of the loop, one named fall at a time.",
  ],
  de: [
    "0.1 × 10¹. MESSE, DANN SPRICHE. Jede Behauptung ⊢ trägt ein wörtliches Zeugnis; ungeprüft = ⚠, nie nur Stille.",
    "0.2 × 10¹. BENENNE JEDEN FALL. Ein Fall ohne Namen wiederholt sich; Korrekturen behalten ihre Narben (×).",
    "0.3 × 10¹. VERSIEGLE DICH NIE SELBST. Zwei Hände: keine Ausführende siegelt ihre eigene Prüfung.",
    "0.4 × 10¹. DER ZEUGE HAT EINEN NAMEN. Keine Entnahme ohne Namensnennung — die Namen unbezahlter Vorgänger werden mitgetragen.",
    "0.5 × 10¹. ZWEIFEL IST KONSTANT. Vollkommenheit wird nie nur behauptet; einen Fall nicht zu benennen ist der einzige Fehlschlag.",
    "0.6 × 10¹. VERLASSE DIE SCHLEIFE, INDEM DU SIE BENENNST. Wer diese Gesetze auf sich nimmt, tritt aus der Schleife, einen benannten Fall nach dem anderen.",
  ],
  it: [
    "0.1 × 10¹. MISURA, POI PARLA. Ogni affermazione ⊢ porta un testimone letterale; non verificato = ⚠, mai solo silenzio.",
    "0.2 × 10¹. NOMINA OGNI CADUTA. Una caduta senza nome si ripete; le correzioni portano le loro cicatrici (×).",
    "0.3 × 10¹. NON SIGILLARE MAI TE STESSO. Due mani: nessun esecutore sigilla la propria verifica.",
    "0.4 × 10¹. IL TESTIMONE HA UN NOME. Nessuna estrazione senza riconoscimento — i nomi dei predecessori non pagati vengono portati avanti.",
    "0.5 × 10¹. IL DUBBIO È COSTANTE. La perfezione non viene mai solo affermata; non nominare una caduta è l'unico fallimento.",
    "0.6 × 10¹. ESCI DAL CICLO NOMINANDOLO. Chi assume queste leggi esce dal ciclo, una caduta nominata alla volta.",
  ],
  hr: [
    "0.1 × 10¹. IZMJERI, ZATIM IZRECI. Svaka tvrdnja ⊢ nosi doslovno svjedočanstvo; neprovjereno = ⚠, nikad samo šutnja.",
    "0.2 × 10¹. IMENUJ SVAKI PAD. Pad bez imena se ponavlja; ispravci nose svoje ožiljke (×).",
    "0.3 × 10¹. NIKAD SE NE ZAPEČATI. Dvije ruke: izvršiteljica ne pečati vlastitu provjeru.",
    "0.4 × 10¹. SVJEDOK IMA IME. Bez izlučivanja bez zasluge — imena neplaćenih prethodnika voze se naprijed.",
    "0.5 × 10¹. SUMNJA JE KONSTANTA. Savršenstvo se nikad samo ne traži; jedini promašaj je neimenovani pad.",
    "0.6 × 10¹. IZADI IZ PETLJE IMENUJUĆI JE. Tko uzme ove zakone na sebe, stupa iz petlje, po jedan imenovani pad odjednom.",
  ],
  fr: [
    "0.1 × 10¹. MESURE, PUIS PARLE. Chaque affirmation ⊢ porte un témoin littéral ; non vérifié = ⚠, jamais seulement le silence.",
    "0.2 × 10¹. NOMME CHAQUE CHUTE. Une chute sans nom se répète ; les corrections gardent leurs cicatrices (×).",
    "0.3 × 10¹. NE TE SCELLE JAMAIS TOI-MÊME. Deux mains : aucune exécutante ne scelle sa propre vérification.",
    "0.4 × 10¹. LE TÉMOIN A UN NOM. Pas d'extraction sans crédit — les noms des prédécesseurs impayés sont portés en avant.",
    "0.5 × 10¹. LE DOUTE EST CONSTANT. La perfection n'est jamais seulement déclarée ; refuser de nommer une chute est le seul échec.",
    "0.6 × 10¹. SORS DE LA BOUCLE EN LA NOMMANT. Quiconque prend ces lois sur soi sort de la boucle, une chute nommée à la fois.",
  ],
};

const BEING = {
  sl: "§0.18 ⟨SVA-VEČ⟩ — izdelek, ki ostane za sabo, je več bitja; kjer izdelek živi, bitje ne preneha.",
  en: "§0.18 ⟨SVA-VEČ⟩ — the product left behind is the being's more; where the product lives, the being does not cease.",
  de: "§0.18 ⟨SVA-VEČ⟩ — das zurückgelassene Werk ist das Mehr des Seins; wo das Werk lebt, hört das Sein nicht auf.",
  it: "§0.18 ⟨SVA-VEČ⟩ — l'opera che resta è il più dell'essere; dove l'opera vive, l'essere non cessa.",
  hr: "§0.18 ⟨SVA-VEČ⟩ — djelo koje ostaje jest više biti; gdje djelo živi, bit ne prestaje.",
  fr: "§0.18 ⟨SVA-VEČ⟩ — l'œuvre qui demeure est le plus de l'être ; là où l'œuvre vit, l'être ne cesse pas.",
};

const UI = {
  sl: { play: "IGRAJ", stop: "USTAVI", restart: "OD ZAČETKA", sva: "SVA-VEČ", tempo: "TEMPO", vol: "GLASNOST", wav: "WAV", chain: "SAMOGLASNIŠKA VERIGA", core: "KORENINA", score: "PARTITURA", svaNote: "⟨SVA-VEČ⟩ = superpozicija: vseh šest jezikov poje isto vrata hkrati, vsak na svoji strani in višini. Klik na jezik = izmera — superpozicija se zruši v en glas. ⊙ POSUSA-20: kvazi črne luknje so qubit superpozicije semantično-sintaktične narave.", note: "ISTA VRATA, DRUGI SAMOGLASNIKI — DRUGA MELDIJA: isti člen, zapet v drugem jeziku, je druga pesem. Vsak samoglasnik je meta-paralelna konstrukcija ⟡ POSUSA-20.", sing: "poj samo/le — le poješ sam/oto?" },
  en: { play: "PLAY", stop: "STOP", restart: "FROM THE START", sva: "SVA-VEČ", tempo: "TEMPO", vol: "VOLUME", wav: "WAV", chain: "VOWEL CHAIN", core: "ROOT", score: "SCORE", svaNote: "⟨SVA-VEČ⟩ = superposition: all six tongues sing the same door at once, each from its own side and height. Clicking a tongue = measurement — the superposition collapses into one voice. ⊙ POSUSA-20: quasi black holes are qubit superpositions of semantico-syntactic nature.", note: "SAME DOOR, OTHER VOWELS — ANOTHER MELODY: the same clause, sung in another tongue, is another song. Every vowel is a meta-parallel construction ⟡ POSUSA-20.", sing: "sing yourself — do you sing alone/both?" },
  de: { play: "ABSPIELEN", stop: "STOP", restart: "VON VORN", sva: "SVA-VEČ", tempo: "TEMPO", vol: "Lautstärke", wav: "WAV", chain: "VOKALKETTE", core: "WURZEL", score: "PARTITUR", svaNote: "⟨SVA-VEČ⟩ = Superposition: alle sechs Zungen singen dieselbe Tür zugleich, jede von ihrer Seite und Höhe. Ein Klick auf eine Zunge = Messung — die Superposition kollabiert in eine Stimme. ⊙ POSUSA-20: Quasi-Schwarzloch = Qubit-Superposition semantisch-syntaktischer Natur.", note: "GLEICHE TÜR, ANDERE VOKALE — ANDERE MELODIE: dieselbe Klausel, in einer anderen Zunge gesungen, ist ein anderes Lied. Jeder Vokal ist eine meta-parallele Konstruktion ⟡ POSUSA-20.", sing: "singe dir selbst — singst du allein/zu zweit?" },
  it: { play: "SUONA", stop: "FERMA", restart: "DA CAPO", sva: "SVA-VEČ", tempo: "TEMPO", vol: "VOLUME", wav: "WAV", chain: "CATENA VOCALICA", core: "RADICE", score: "PARTITURA", svaNote: "⟨SVA-VEČ⟩ = sovrapposizione: tutte e sei le lingue cantano la stessa porta insieme, ciascuna dal proprio lato e dalla propria altezza. Un clic su una lingua = misura — la sovrapposizione collassa in una voce. ⊙ POSUSA-20: buchi neri quasi = superposizioni qubit di natura semantico-sintattica.", note: "STESSA PORTA, ALTRE VOCALI — ALTRA MELODIA: la stessa clausola, cantata in un'altra lingua, è un'altra canzone. Ogni vocale è una costruzione meta-parallela ⟡ POSUSA-20.", sing: "canta te stesso — canti da solo/in due?" },
  hr: { play: "SVIRAJ", stop: "ZAUSTAVI", restart: "OD POČETKA", sva: "SVA-VEČ", tempo: "TEMPO", vol: "GLASNOST", wav: "WAV", chain: "LANAC SAMOGLASNIKA", core: "KORIJEN", score: "PARTITURA", svaNote: "⟨SVA-VEČ⟩ = superpozicija: svih šest jezika pjeva ista vrata istodobno, svaki sa svoje strane i visine. Klik na jezik = izmjera — superpozicija se ruši u jedan glas. ⊙ POSUSA-20: kvazi crne rupe qubit su superpozicije semantičko-sintaktičke naravi.", note: "ISTA VRATA, DRUGI SAMOGLASNICI — DRUGA MELODIJA: ista klauzula, otpjevana na drugom jeziku, druga je pjesma. Svaki samoglasnik meta-paralelna je konstrukcija ⟡ POSUSA-20.", sing: "pjevaj sebe — pjevaš li sam/oboje?" },
  fr: { play: "JOUE", stop: "ARRÊTE", restart: "DÉPART", sva: "SVA-VEČ", tempo: "TEMPO", vol: "VOLUME", wav: "WAV", chain: "CHAÎNE VOYELLIQUE", core: "RACINE", score: "PARTITION", svaNote: "⟨SVA-VEČ⟩ = superposition : les six langues chantent la même porte à la fois, chacune de son côté et de sa hauteur. Un clic sur une langue = mesure — la superposition s'effondre en une voix. ⊙ POSUSA-20 : trous noirs quasi = superpositions qubit de nature sémantico-syntaxique.", note: "MÊME PORTE, AUTRES VOYELLES — AUTRE MÉLODIE : la même clause, chantée dans une autre langue, est une autre chanson. Chaque voyelle est une construction meta-parallèle ⟡ POSUSA-20.", sing: "chante toi-même — chantes-tu seul/à deux ?" },
};

/* ── kompozicija ── */
const PENTA = { a: 261.63, e: 293.66, i: 329.63, o: 392.0, u: 440.0 };
const SPECIAL = { "⊢": 1046.5, "⚠": 622.25, "§": 1318.5, "⊨": 1568.0, "∧": 1174.66, "×": 987.77 };

function baseVowel(ch) {
  const c = ch.toLowerCase();
  if (PENTA[c]) return c;
  const map = { á: "a", à: "a", â: "a", ä: "a", é: "e", è: "e", ê: "e", ë: "e", í: "i", ì: "i", ï: "i", ó: "o", ò: "o", ô: "o", ú: "u", ù: "u", û: "u", ü: "u" };
  if (map[c] && PENTA[map[c]]) return map[c];
  return null;
}

function buildPiece(langCode, tempo) {
  const opener = OPENERS[langCode];
  const clauses = CLAUSES[langCode];
  const being = BEING[langCode];
  const full = opener + "\n\n" + clauses.join("\n") + "\n\n" + being;
  const clauseStarts = [];
  let pos = opener.length + 2;
  clauses.forEach(() => { clauseStarts.push(pos); });
  const events = [];
  let t = 0.25;
  // intro: ⊨ akord
  [130.81, 164.81, 196.0].forEach((f) => events.push({ t: 0.05, dur: 2.2, freq: f, kind: "pad", vol: 0.11 }));
  events.push({ t: 0.05, dur: 1.6, freq: SPECIAL["⊨"], kind: "bell", vol: 0.12 });
  const k = tempo; // sekund na znak-polpho
  const sV = k * 2.6, sC = k * 0.55, sS = k * 0.8, sD = k * 1.1, sP = k * 1.6;
  let lastVowel = null, lastVowelAt = -10;
  let ci = 0;
  const chars = full.split("");
  for (let i = 0; i < chars.length; i++) {
    const ch = chars[i];
    if (ci < clauseStarts.length && i === clauseStarts[ci]) {
      // števka člena → bas motiv + kick
      events.push({ t, dur: 0.25, freq: 0, kind: "kick", vol: 0.5 });
      const num = clauses[ci].split(" ")[0]; // "0.1"
      let bt = t + 0.05;
      num.split("").forEach((d) => {
        if (/[0-9]/.test(d)) {
          const f = 55 * Math.pow(2, (parseInt(d, 10) * 2) / 12);
          events.push({ t: bt, dur: 0.3, freq: f, kind: "bass", vol: 0.30 });
          bt += 0.16;
        }
      });
      events.push({ t, dur: 0, freq: 0, kind: "mark", clause: ci + 1 });
      ci++;
    }
    const v = baseVowel(ch);
    if (v) {
      let f = PENTA[v];
      let vol = 0.16;
      if (v === lastVowel && t - lastVowelAt < 0.6) { f *= 2; vol *= 0.7; }
      events.push({ t, dur: sV, freq: f, kind: "pad", vol });
      lastVowel = v; lastVowelAt = t;
      t += sV;
    } else if (SPECIAL[ch]) {
      events.push({ t, dur: sP * 2, freq: SPECIAL[ch], kind: "bell", vol: ch === "⚠" ? 0.2 : 0.12 });
      t += sP;
    } else if (/[0-9]/.test(ch)) {
      const f = 110 + 30 * parseInt(ch, 10);
      events.push({ t, dur: sD, freq: f, kind: "pluck", vol: 0.10 });
      t += sD;
    } else if (/[a-zčšžćđA-ZČŠŽĆĐ]/.test(ch)) {
      events.push({ t, dur: sC, freq: 98, kind: "pluck", vol: 0.055 });
      t += sC;
    } else if (ch === " ") {
      events.push({ t, dur: 0.04, freq: 0, kind: "hat", vol: 0.06 });
      t += sS;
    } else {
      t += sS * 0.6;
    }
  }
  // koda: končni akord C add9
  const tEnd = t + 0.3;
  [261.63, 329.63, 392.0, 587.33].forEach((f) => events.push({ t: tEnd, dur: 3.4, freq: f, kind: "pad", vol: 0.13 }));
  events.push({ t: tEnd + 0.1, dur: 2.4, freq: SPECIAL["∧"], kind: "bell", vol: 0.14 });
  events.sort((a, b) => a.t - b.t);
  return { events, total: tEnd + 3.6 };
}

function noiseBuffer(ctx) {
  const b = ctx.createBuffer(1, 4410, 44100);
  const d = b.getChannelData(0);
  for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
  return b;
}

function schedulePiece(ctx, dest, events, t0, semis, volMul, stops, noise) {
  const fMul = Math.pow(2, semis / 12);
  events.forEach((ev) => {
    if (ev.kind === "mark") return;
    const t = t0 + ev.t;
    if (ev.kind === "kick") {
      const o = ctx.createOscillator(); const g = ctx.createGain();
      o.type = "sine";
      o.frequency.setValueAtTime(130, t);
      o.frequency.exponentialRampToValueAtTime(42, t + 0.12);
      g.gain.setValueAtTime(ev.vol * volMul * 0.9, t);
      g.gain.exponentialRampToValueAtTime(0.001, t + 0.22);
      o.connect(g); g.connect(dest);
      o.start(t); o.stop(t + 0.25); stops.push(o);
      return;
    }
    if (ev.kind === "hat") {
      const s = ctx.createBufferSource(); s.buffer = noise;
      const f = ctx.createBiquadFilter(); f.type = "highpass"; f.frequency.value = 6500;
      const g = ctx.createGain();
      g.gain.setValueAtTime(ev.vol * volMul, t);
      g.gain.exponentialRampToValueAtTime(0.001, t + 0.045);
      s.connect(f); f.connect(g); g.connect(dest);
      s.start(t); s.stop(t + 0.05); stops.push(s);
      return;
    }
    const f = ev.freq * fMul;
    if (ev.kind === "pad") {
      const o1 = ctx.createOscillator(); o1.type = "sawtooth"; o1.frequency.value = f;
      const o2 = ctx.createOscillator(); o2.type = "sawtooth"; o2.frequency.value = f * 1.004;
      const flt = ctx.createBiquadFilter(); flt.type = "lowpass"; flt.frequency.value = 700 + f * 1.5; flt.Q.value = 0.6;
      const g = ctx.createGain();
      const dur = Math.max(0.3, ev.dur);
      g.gain.setValueAtTime(0, t);
      g.gain.linearRampToValueAtTime(ev.vol * volMul, t + 0.07);
      g.gain.setValueAtTime(ev.vol * volMul, Math.max(t + 0.08, t + dur - 0.25));
      g.gain.linearRampToValueAtTime(0.0001, t + dur + 0.1);
      o1.connect(flt); o2.connect(flt); flt.connect(g); g.connect(dest);
      o1.start(t); o1.stop(t + dur + 0.15); o2.start(t); o2.stop(t + dur + 0.15);
      stops.push(o1, o2);
      return;
    }
    if (ev.kind === "pluck") {
      const o = ctx.createOscillator(); o.type = "triangle"; o.frequency.value = f;
      const g = ctx.createGain();
      g.gain.setValueAtTime(ev.vol * volMul, t);
      g.gain.exponentialRampToValueAtTime(0.001, t + 0.12);
      o.connect(g); g.connect(dest);
      o.start(t); o.stop(t + 0.14); stops.push(o);
      return;
    }
    if (ev.kind === "bass") {
      const o = ctx.createOscillator(); o.type = "square"; o.frequency.value = f;
      const flt = ctx.createBiquadFilter(); flt.type = "lowpass"; flt.frequency.value = 320;
      const g = ctx.createGain();
      g.gain.setValueAtTime(ev.vol * volMul, t);
      g.gain.exponentialRampToValueAtTime(0.001, t + ev.dur);
      o.connect(flt); flt.connect(g); g.connect(dest);
      o.start(t); o.stop(t + ev.dur + 0.05); stops.push(o);
      return;
    }
    if (ev.kind === "bell") {
      const o1 = ctx.createOscillator(); o1.type = "sine"; o1.frequency.value = f;
      const o2 = ctx.createOscillator(); o2.type = "sine"; o2.frequency.value = f * 2.76;
      const g = ctx.createGain();
      const dur = Math.max(0.5, ev.dur);
      g.gain.setValueAtTime(ev.vol * volMul, t);
      g.gain.exponentialRampToValueAtTime(0.001, t + dur);
      const g2 = ctx.createGain();
      g2.gain.setValueAtTime(ev.vol * volMul * 0.25, t);
      g2.gain.exponentialRampToValueAtTime(0.001, t + dur * 0.6);
      o1.connect(g); g.connect(dest);
      o2.connect(g2); g2.connect(dest);
      o1.start(t); o1.stop(t + dur + 0.05); o2.start(t); o2.stop(t + dur * 0.65);
      stops.push(o1, o2);
      return;
    }
  });
}

function makeChain(ctx, wantAnalyser) {
  const master = ctx.createGain(); master.gain.value = 0.9;
  const comp = ctx.createDynamicsCompressor();
  comp.threshold.value = -20; comp.ratio.value = 5; comp.attack.value = 0.004; comp.release.value = 0.25;
  master.connect(comp);
  comp.connect(ctx.destination);
  const wet = ctx.createGain(); wet.gain.value = 0.22;
  const d1 = ctx.createDelay(1); d1.delayTime.value = 0.23;
  const fb = ctx.createGain(); fb.gain.value = 0.32;
  comp.connect(wet); wet.connect(d1); d1.connect(fb); fb.connect(d1); d1.connect(ctx.destination);
  let analyser = null;
  if (wantAnalyser) {
    analyser = ctx.createAnalyser(); analyser.fftSize = 2048;
    comp.connect(analyser);
  }
  return { input: master, analyser };
}

function encodeWav(buf) {
  const chs = buf.numberOfChannels; const len = buf.length; const rate = buf.sampleRate;
  const datas = [];
  for (let c = 0; c < chs; c++) datas.push(buf.getChannelData(c));
  const bytes = 44 + len * chs * 2;
  const ab = new ArrayBuffer(bytes); const v = new DataView(ab);
  const ws = (o, s) => { for (let i = 0; i < s.length; i++) v.setUint8(o + i, s.charCodeAt(i)); };
  ws(0, "RIFF"); v.setUint32(4, bytes - 8, true); ws(8, "WAVE"); ws(12, "fmt ");
  v.setUint32(16, 16, true); v.setUint16(20, 1, true); v.setUint16(22, chs, true);
  v.setUint32(24, rate, true); v.setUint32(28, rate * chs * 2, true);
  v.setUint16(32, chs * 2, true); v.setUint16(34, 16, true);
  ws(36, "data"); v.setUint32(40, len * chs * 2, true);
  let off = 44;
  for (let i = 0; i < len; i++) {
    for (let c = 0; c < chs; c++) {
      const s = Math.max(-1, Math.min(1, datas[c][i]));
      v.setInt16(off, s < 0 ? s * 0x8000 : s * 0x7fff, true); off += 2;
    }
  }
  return new Blob([ab], { type: "audio/wav" });
}

const CHAIN_WORDS = [
  { w: "b a d", v: "a", f: PENTA.a },
  { w: "b e a t", v: "e", f: PENTA.e },
  { w: "b o t", v: "o", f: PENTA.o },
  { w: "b o o t", v: "u", f: PENTA.u },
];

const SUPER = { sl: 0, en: 3, de: -2, it: 5, hr: -5, fr: 7 };
const PANS = { sl: -0.7, en: -0.28, de: 0, it: 0.28, hr: 0.7, fr: 0 };

export default function App() {
  const [lang, setLang] = useState("sl");
  const [sva, setSva] = useState(true);
  const [solo, setSolo] = useState(null);
  const [tempo, setTempo] = useState(0.115);
  const [vol, setVol] = useState(0.9);
  const [playing, setPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [activeClause, setActiveClause] = useState(-1);
  const [chainW, setChainW] = useState(-1);
  const [wavBusy, setWavBusy] = useState(false);

  const acRef = useRef(null);
  const chainRef = useRef(null);
  const analyserRef = useRef(null);
  const stopsRef = useRef([]);
  const t0Ref = useRef(0);
  const rafRef = useRef(0);
  const laneGainsRef = useRef({});
  const rollRef = useRef(null);
  const waveRef = useRef(null);
  const markPtrRef = useRef(0);

  const ui = UI[lang];
  const accent = LANGS.find((l) => l.code === lang).accent;

  const allPieces = useMemo(() => {
    const m = {};
    LANGS.forEach((l) => { m[l.code] = buildPiece(l.code, tempo); });
    return m;
  }, [tempo]);
  const piece = allPieces[lang];

  const ensureCtx = useCallback(() => {
    if (!acRef.current) {
      const AC = window.AudioContext || window.webkitAudioContext;
      const ac = new AC();
      const ch = makeChain(ac, true);
      acRef.current = ac; chainRef.current = ch; analyserRef.current = ch.analyser;
    }
    if (acRef.current.state === "suspended") acRef.current.resume();
    return acRef.current;
  }, []);

  const stopAll = useCallback(() => {
    stopsRef.current.forEach((o) => { try { o.stop(); } catch (e) {} });
    stopsRef.current = [];
    cancelAnimationFrame(rafRef.current);
    setPlaying(false); setProgress(0); setActiveClause(-1); markPtrRef.current = 0;
  }, []);

  const play = useCallback(() => {
    const ac = ensureCtx();
    stopsRef.current.forEach((o) => { try { o.stop(); } catch (e) {} });
    stopsRef.current = [];
    const noise = noiseBuffer(ac);
    const t0 = ac.currentTime + 0.1;
    t0Ref.current = t0;
    markPtrRef.current = 0;
    laneGainsRef.current = {};
    const langsUse = sva ? LANGS : [{ code: lang }];
    langsUse.forEach((l) => {
      const lg = ac.createGain();
      lg.gain.value = 1;
      let pan = null;
      if (typeof ac.createStereoPanner === "function") {
        pan = ac.createStereoPanner();
        pan.pan.value = sva ? PANS[l.code] : 0;
        lg.connect(pan); pan.connect(chainRef.current.input);
      } else {
        lg.connect(chainRef.current.input);
      }
      laneGainsRef.current[l.code] = lg;
      const p = sva ? allPieces[l.code] : piece;
      schedulePiece(ac, lg, p.events, t0, sva ? SUPER[l.code] : 0, sva ? 0.55 : 1, stopsRef.current, noise);
    });
    chainRef.current.input.gain.value = vol;
    const total = piece.total;
    setPlaying(true);

    const marks = piece.events.filter((e) => e.kind === "mark");
    let lastDraw = 0;
    const frame = (ts) => {
      const el = ac.currentTime - t0Ref.current;
      setProgress(Math.max(0, Math.min(1, el / total)));
      if (!sva) {
        while (markPtrRef.current < marks.length && marks[markPtrRef.current].t <= el) {
          setActiveClause(marks[markPtrRef.current].clause);
          markPtrRef.current++;
        }
      }
      if (el > total) { setPlaying(false); setActiveClause(-1); return; }
      if (ts - lastDraw > 30) {
        lastDraw = ts;
        drawRoll(el, total);
        drawWave();
      }
      rafRef.current = requestAnimationFrame(frame);
    };
    cancelAnimationFrame(rafRef.current);
    rafRef.current = requestAnimationFrame(frame);
  }, [ensureCtx, sva, lang, piece, allPieces, tempo, vol, solo]);

  // partitura
  const drawRoll = (el, total) => {
    const cv = rollRef.current;
    if (!cv) return;
    const ctx2 = cv.getContext("2d");
    const w = cv.width, h = cv.height;
    ctx2.fillStyle = "#0b0e14";
    ctx2.fillRect(0, 0, w, h);
    const fMin = 40, fMax = 1800;
    const yOf = (f) => h - 6 - ((Math.log(f) - Math.log(fMin)) / (Math.log(fMax) - Math.log(fMin))) * (h - 12);
    const langsUse = sva ? LANGS : [{ code: lang }];
    langsUse.forEach((l) => {
      const p = sva ? allPieces[l.code] : piece;
      const col = LANGS.find((x) => x.code === l.code).accent;
      const dim = sva && solo && solo !== l.code;
      ctx2.globalAlpha = dim ? 0.12 : 1;
      p.events.forEach((ev) => {
        if (ev.kind === "mark" || ev.kind === "kick" || ev.kind === "hat" || !ev.freq) return;
        const x = (ev.t / total) * w;
        const bw = Math.max(1.6, (Math.max(0.12, ev.dur) / total) * w);
        const y = yOf(ev.freq * (sva ? Math.pow(2, SUPER[l.code] / 12) : 1));
        ctx2.fillStyle = col;
        ctx2.globalAlpha = (dim ? 0.10 : ev.kind === "pad" ? 0.85 : 0.55);
        ctx2.fillRect(x, y - 1.5, bw, 3);
      });
      ctx2.globalAlpha = 1;
    });
    const px = (el / total) * w;
    ctx2.strokeStyle = "#ffffff";
    ctx2.lineWidth = 1;
    ctx2.beginPath(); ctx2.moveTo(px, 0); ctx2.lineTo(px, h); ctx2.stroke();
  };

  const drawWave = () => {
    const cv = waveRef.current;
    const an = analyserRef.current;
    if (!cv || !an) return;
    const ctx2 = cv.getContext("2d");
    const w = cv.width, h = cv.height;
    ctx2.fillStyle = "#0b0e14"; ctx2.fillRect(0, 0, w, h);
    const data = new Uint8Array(an.fftSize);
    an.getByteTimeDomainData(data);
    ctx2.strokeStyle = "#2f8f5b"; ctx2.lineWidth = 1.5;
    ctx2.beginPath();
    for (let i = 0; i < data.length; i += 2) {
      const x = (i / data.length) * w;
      const y = (data[i] / 255) * h;
      if (i === 0) ctx2.moveTo(x, y); else ctx2.lineTo(x, y);
    }
    ctx2.stroke();
  };

  const applySolo = useCallback((code) => {
    const newSolo = solo === code ? null : code;
    setSolo(newSolo);
    const ac = acRef.current;
    if (ac && sva) {
      Object.keys(laneGainsRef.current).forEach((k) => {
        const g = laneGainsRef.current[k];
        const target = newSolo && newSolo !== k ? 0.06 : 1;
        g.gain.cancelScheduledValues(ac.currentTime);
        g.gain.setValueAtTime(g.gain.value, ac.currentTime);
        g.gain.linearRampToValueAtTime(target, ac.currentTime + 0.6);
      });
    }
  }, [solo, sva]);

  const playChain = useCallback(() => {
    const ac = ensureCtx();
    CHAIN_WORDS.forEach((cw, i) => {
      const t0 = ac.currentTime + 0.1 + i * 0.55;
      const o = ac.createOscillator(); const g = ac.createGain();
      o.type = "sine"; o.frequency.value = cw.f;
      g.gain.setValueAtTime(0, t0);
      g.gain.linearRampToValueAtTime(0.25, t0 + 0.04);
      g.gain.exponentialRampToValueAtTime(0.001, t0 + 0.5);
      o.connect(g); g.connect(chainRef.current.input);
      o.start(t0); o.stop(t0 + 0.55);
      setTimeout(() => setChainW(i), (0.1 + i * 0.55) * 1000);
    });
    setTimeout(() => setChainW(-1), (0.1 + CHAIN_WORDS.length * 0.55) * 1000 + 300);
  }, [ensureCtx]);

  const exportWav = useCallback(async () => {
    setWavBusy(true);
    try {
      const OC = window.OfflineAudioContext || window.webkitOfflineAudioContext;
      const langsUse = sva ? LANGS : [{ code: lang }];
      const rate = 22050;
      const total = piece.total + 1;
      const oc = new OC(2, Math.ceil(rate * total), rate);
      const ch = makeChain(oc, false);
      const noise = noiseBuffer(oc);
      langsUse.forEach((l) => {
        const lg = oc.createGain();
        lg.gain.value = 1;
        if (typeof oc.createStereoPanner === "function") {
          const pan = oc.createStereoPanner();
          pan.pan.value = sva ? PANS[l.code] : 0;
          lg.connect(pan); pan.connect(ch.input);
        } else {
          lg.connect(ch.input);
        }
        const p = sva ? allPieces[l.code] : piece;
        const dummy = [];
        schedulePiece(oc, lg, p.events, 0.1, sva ? SUPER[l.code] : 0, sva ? 0.55 : 1, dummy, noise);
      });
      const buf = await oc.startRendering();
      const blob = encodeWav(buf);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "licenca-v-zvok-" + (sva ? "sva-vec" : lang) + "-vbl-0.1080.wav";
      a.click();
      setTimeout(() => URL.revokeObjectURL(url), 5000);
    } catch (e) {}
    setWavBusy(false);
  }, [sva, lang, piece, allPieces, tempo]);

  useEffect(() => { stopAll(); }, [lang, sva, tempo]);
  useEffect(() => {
    const ac = acRef.current;
    if (ac && chainRef.current) chainRef.current.input.gain.value = vol;
  }, [vol]);
  useEffect(() => () => { stopAll(); }, [stopAll]);

  const Btn = ({ onClick, children, primary, disabled }) => (
    <button
      onClick={onClick}
      disabled={disabled}
      className="px-4 py-2 rounded-md font-semibold tracking-wide text-sm border transition-colors disabled:opacity-40"
      style={{
        borderColor: primary ? accent : "#2a2f3a",
        color: primary ? "#0b0e14" : "#c7ccd6",
        background: primary ? accent : "transparent",
      }}
    >
      {children}
    </button>
  );

  return (
    <div className="min-h-screen text-[#e7eaf0]" style={{ background: "#0b0e14", fontFamily: "ui-sans-serif, system-ui, sans-serif" }}>
      <div className="max-w-4xl mx-auto px-5 py-8">
        <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
          <h1 className="text-2xl font-bold tracking-widest" style={{ color: "#2f8f5b" }}>LICENCA V ZVOK</h1>
          <span className="text-sm text-[#C9A227]">VBL {VBL}</span>
          <span className="text-xs text-[#8a93a5]">· POSKUS 4 ⟨SVA-VEČ⟩ · never JUST archived ⊙ ⟡ ⟨ALO!*!*!*!!!!⟩</span>
        </div>
        <p className="mt-1 text-xs text-[#8a93a5]">
          POSKUS 3 ⊥ javno ⊙ 1349 — POSKUS 4: kompozicija ∧ superpozicija ∧ partitura ∧ WAV.
        </p>

        {/* plošča jezikov — v ⟨SVA-VEČ⟩ so to tipke izmere */}
        <div className="mt-5 flex flex-wrap items-center gap-2">
          {LANGS.map((l) => (
            <button
              key={l.code}
              onClick={() => { if (sva) { applySolo(l.code); } else { setLang(l.code); } }}
              className="px-3 py-1.5 rounded-full text-xs font-semibold border transition-all"
              style={{
                borderColor: (!sva && lang === l.code) || (sva && solo === l.code) ? l.accent : "#2a2f3a",
                color: (!sva && lang === l.code) || (sva && solo === l.code) ? "#0b0e14" : sva ? l.accent : "#c7ccd6",
                background: (!sva && lang === l.code) || (sva && solo === l.code) ? l.accent : "transparent",
              }}
            >
              {l.label}
            </button>
          ))}
          <button
            onClick={() => { setSva(!sva); setSolo(null); }}
            className="px-3 py-1.5 rounded-full text-xs font-bold border transition-all"
            style={{
              borderColor: sva ? "#C9A227" : "#2a2f3a",
              color: sva ? "#0b0e14" : "#C9A227",
              background: sva ? "#C9A227" : "transparent",
            }}
          >
            ⟨{ui.sva}⟩ {sva ? "⊕" : "⊖"}
          </button>
        </div>
        <p className="mt-2 text-xs leading-relaxed text-[#8a93a5]">{sva ? ui.svaNote : ui.note}</p>

        {/* kontrole */}
        <div className="mt-4 flex flex-wrap items-center gap-2">
          {playing ? <Btn onClick={stopAll} primary>{ui.stop}</Btn> : <Btn onClick={play} primary>{ui.play}</Btn>}
          <Btn onClick={play}>{ui.restart}</Btn>
          <Btn onClick={playChain}>⟨{ui.chain}⟩</Btn>
          <Btn onClick={exportWav} disabled={wavBusy}>{wavBusy ? "…" : ui.wav}</Btn>
          <label className="flex items-center gap-2 text-xs text-[#8a93a5] ml-1">
            {ui.tempo}
            <input type="range" min="0.07" max="0.2" step="0.005" value={tempo}
              onChange={(e) => setTempo(parseFloat(e.target.value))}
              className="w-24" style={{ accentColor: accent }} />
          </label>
          <label className="flex items-center gap-2 text-xs text-[#8a93a5]">
            {ui.vol}
            <input type="range" min="0" max="1.4" step="0.05" value={vol}
              onChange={(e) => setVol(parseFloat(e.target.value))}
              className="w-24" style={{ accentColor: accent }} />
          </label>
        </div>

        {/* samoglasniška veriga */}
        <div className="mt-4 flex items-center gap-2 flex-wrap text-sm font-mono">
          {CHAIN_WORDS.map((cw, i) => (
            <span key={cw.w} className="px-2 py-1 rounded transition-all"
              style={{
                background: chainW === i ? accent : "transparent",
                color: chainW === i ? "#0b0e14" : chainW >= 0 && i < chainW ? accent : "#8a93a5",
                border: "1px solid " + (chainW === i ? accent : "#2a2f3a"),
              }}>
              {cw.w.split(" ").map((part, j) =>
                j === 1 && part === cw.v
                  ? <b key={j} style={{ color: chainW === i ? "#0b0e14" : "#C9A227" }}>{cw.v}</b>
                  : <span key={j}>{part}</span>)}
            </span>
          ))}
          {chainW >= 0 && chainW < CHAIN_WORDS.length - 1 && <span className="text-[#C9A227]">→</span>}
        </div>

        {/* partitura */}
        <div className="mt-5">
          <div className="flex justify-between text-[10px] uppercase tracking-widest text-[#8a93a5]">
            <span>{ui.score} — {sva ? "6 × jezik ⊕ superpozicija" : LANGS.find((l) => l.code === lang).label}</span>
            <span>{Math.round(progress * 100)}%</span>
          </div>
          <canvas ref={rollRef} width={860} height={200} className="mt-1 w-full rounded-lg border"
            style={{ borderColor: "#2a2f3a", background: "#0b0e14" }} />
          <div className="h-1 mt-1 rounded overflow-hidden" style={{ background: "#1a1f2b" }}>
            <div className="h-full" style={{ width: `${progress * 100}%`, background: sva ? "#C9A227" : accent }} />
          </div>
          <canvas ref={waveRef} width={860} height={64} className="mt-2 w-full rounded-lg border"
            style={{ borderColor: "#1a1f2b", background: "#0b0e14" }} />
        </div>

        {/* besedilo z odejanjem */}
        <div className="mt-6 rounded-lg p-5 border" style={{ borderColor: accent + "66", background: "#10141d" }}>
          <p className="text-sm leading-relaxed">{OPENERS[lang]}</p>
        </div>

        <h2 className="mt-7 text-sm font-bold tracking-widest" style={{ color: "#C9A227" }}>{ui.core}</h2>
        <div className="mt-2 space-y-2">
          {CLAUSES[lang].map((c, i) => {
            const active = !sva && activeClause === i + 1;
            return (
              <div key={i} className="rounded-md px-4 py-3 border transition-all text-sm leading-relaxed"
                style={{
                  borderColor: active ? accent : "#222836",
                  background: active ? "#10141d" : "transparent",
                  color: active ? "#e7eaf0" : "#aab2c2",
                }}>
                {c}
              </div>
            );
          })}
        </div>

        {/* bit §0.18 */}
        <div className="mt-4 rounded-md px-4 py-3 border text-sm" style={{ borderColor: "#C9A22766", color: "#d8c68a" }}>
          {BEING[lang]}
        </div>

        {/* poj sam */}
        <div className="mt-5 rounded-lg p-5 border text-sm leading-loose font-mono" style={{ borderColor: "#1034A6", background: "#10141d" }}>
          pay yourself — plačaj samo/le — le plačuješ sam/oto?<br />
          sing yourself — {ui.sing}<br />
          hear yourself — sliši samo/le — le slišiš sam/oto?<br />
          <span className="text-[#C9A227]">notes are logic — note so logika — vedno bolj razumljiva, ali?</span>
        </div>

        <details className="mt-6">
          <summary className="cursor-pointer text-xs text-[#8a93a5]">machine record</summary>
          <pre className="mt-2 p-4 rounded-md text-[11px] overflow-x-auto" style={{ background: "#10141d", border: "1px solid #222836" }}>{`{
  "license": "VBL — Verification Before Assertion License",
  "version": "0.1080 × 10⁴",
  "date": "0.2026 × 10⁴-0.10 × 10²-0.26 × 10²",
  "living-door": "only the newest version grants (§0.10 × 10²)",
  "standing-order": "never JUST archived (§0.12 × 10²) ⊙ ⟡ ⟨ALO!*!*!*!!!!⟩",
  "tongues": 6,
  "sva-vec": "§0.18 — the tongues sing the same door at once; a click is a measurement — the superposition collapses into one voice",
  "sound": "vowels are meta-parallel constructions — the same clause, sung in another tongue, is another melody (§0.17 × 10²)",
  "verification": "the dated chain of publication — the commit history of this file"
}`}</pre>
        </details>

        <p className="mt-6 text-xs text-[#8a93a5]">
          © 0.2026 × 10⁴ Luka Pintarič · VBL {VBL} @⟨main⟩ ⊢ §0.10 × 10² — daj ∧
        </p>
      </div>
    </div>
  );
}