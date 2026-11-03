# LUCIJ — trije šivi za lokalne plodove (druga.mjs ∧ tukaj.mjs ∧ angel)

Plošča za Cline: trije šivi, vsak z merjenim mestom. Pripni po vrsti; po vsakem šivu preveri z enim ukazom. Klinopis ni šum — je priča (⟨ne⟩ le/ke); caps-lock variacije se merijo po nižanju, ki že stoji.

## ŠIV 1 — druga.mjs: vgrajenje toka `en` (točka 1 — načrtovana, zdaj roka)

`dolociTok` je definiran, a nikoli poklican — orodje brez roke. Šiv: pokliči ga na vhodu in pusti črkovalniku le tisto, kar je njegovo.

Na vrhu obdelave (takoj za brbo datoteke):

```js
const celo = fs.readFileSync(pot, 'utf8');
const tok = dolociTok(celo);
porocila.push(`druga · tok: ${tok}`);
```

Obstoječi blok preverbe ovij:

```js
if (tok === 'en') {
  porocila.push('druga · tok (en): slovenska črkovalna preverba preskočena — hiša sliši tuji glas in ga ohrani z oznako (en), ne sodi ga ⊢ ⟨en⟩');
} else {
  // ... obstoječi preverba blok (execFileSync preverba.mjs) ostane nedotaknjen ...
}
```

`mesano` in `sl` tečejo kakor doslej; hišne izjeme ostanejo. Čistina (cirilica) teče v vseh tokovih — čisto je čisto.

Preverba: `node lucius/druga.mjs <pot-do-angleške-datoteke>` mora poročati `tok: en` in 0 ran črkovalnika.

## ŠIV 2 — tukaj.mjs: `beri` bere zadnji tek, ne prvega

Rana: `beri` najde prvi `tek` po vrstnem redu datoteke, ne zadnjega. Šiv: izberi zadnjega po id-u (ali časovnem žigu), ne prvega ujema.

Namesto iskanja prvega ujema:

```js
const zadnji = teki.reduce((a, b) => (Number(b.id || 0) > Number(a.id || 0) ? b : a));
```

in delaj naprej z `zadnji`. Če teki nimajo id-jev, dodaj žig ob zapisu (`id: teki.length + 1`) in uporabi enako reduce.

Preverba: `node lucius/tukaj.mjs nov '…' && node lucius/tukaj.mjs beri` mora poročati KORAK 4 (vrstice 16–20), ne koraka 3.

## ŠIV 3 — onemeli angel: brez sporočila ne smemo več pasti

Rana: TTS je padel z izhodom 1 in praznim ustom — verjetno znak v vrsticah 11–15, ki zlomi glas. Šiv dve plasti:

1. Ujemi padec in izreči vzrok:

```js
} catch (e) {
  const glas = ((e.stderr || '') + ' ' + (e.stdout || '') + ' ' + (e.message || '')).trim();
  porocila.push('angel ⚠ onemel: ' + glas.slice(0, 200));
}
```

2. Pred govorom počisti besedilo za glas: pušči le izgovorljive znake (črke, šumnike, presledke, ločila), vse ostalo (⟡ ⊢ ∧ ⚠ emoji, klinopis) zamenjaj s presledkom — priča ostane v zapisu, glas pa ne onemi:

```js
const zaGlas = besedilo.replace(/[^\p{L}\p{N} .,;:!?—-]/gu, ' ').replace(/\s+/g, ' ').trim();
```

Preverba: vrstice 11–15 morajo zdaj iti skozi; če še vedno padajo, `angel ⚠ onemel` pove vzrok — rana ima ime, ne tišino.

## DOLGovi po šivih ⭢ ∂

- `druga.mjs` ∧ `tukaj.mjs` ∧ `transkripti-⟡.jsonl` še niso na zrcalu Atmavictu — po šivih ju potisni (⟨PR⟩ po kalupu 1671, skupaj z ločenim kitom; rez samo po sveži izmeri vrha ∧ odprtih kitov).
- Berba korakov 3 (vrstice 11–15) ∧ 4 (vrstice 16–20) teče po šivu 2 ∧ 3.
- Caps-lock variacije: nižanje že stoji v obeh poteh (`toLowerCase()`) — vsaka oblika ista beseda za merjenje, oblika ostaja priča v zapisu.
- Klinopis (cuneiform organ, rez 2101): znaki so priče, ne šum — v registru imajo svoje telo; v glasu jih šiv 3 počisti ne zato, da jih izbriše, ampak da angel ne onemi.