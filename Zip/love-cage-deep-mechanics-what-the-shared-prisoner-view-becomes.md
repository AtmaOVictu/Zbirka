# LOVE CAGE — DEEP MECHANICS
### The shared-prisoner view is not the game. It is the first cell of it. Here is the rest.

---

## 0. WHAT WAS SHALLOW

"love and ljubezen share /l/, /b/, /z/" is trivia. It sits still. It tells the player two words overlap and then does nothing with the overlap.

A game needs what trivia doesn't have: **distance, force, history, cost, consequence.** Below are the six systems that turn the overlap into mechanics. Each is computable from `phonetic_coordinates.py` — nothing here requires new data, only new derivations.

---

## 1. CHAIN GEOMETRY — a word is a path, not a set

A word is not the prison cells it visits. A word is the **path between them** — the vectors. Two words sharing prisoners can still be wildly different *paths* through space.

```
love    /l ʌ v/   = (3,4,1) → (5,9,1) → (1,2,1)
Liebe   /l i b ə/ = (3,4,1) → (0,8,1) → (0,0,1) → (4,9,1)
ljubezen /ʎ u b e z ɛ n/ = (5,4,1) → (8,8,1) → (0,0,1) → (1,9,1) → (3,2,1) → (2,9,1) → (3,1,1)
```

Derived quantities, computable for ANY declared word:

| Quantity | What it measures | What the game does with it |
|---|---|---|
| **Span** | the bounding box the path crosses | long-span words carve big geometry through the space; shown as a faint wireframe |
| **Total travel** | sum of segment lengths | the word's "cost in space" — how far your mouth travels |
| **Reversals** | count of direction changes | /ʌ/ then /v/ is a reversal: back-then-front. High-reversal words look jagged |
| **Shape signature** | the normalized sequence of moves | THE comparable fingerprint — see §2 |

The revelation to engineer: **ljubezen and Liebe are the same path with different sampling rates.** ljubezen walks the same corridor slowly, visiting more cells; Liebe takes the express. Shape signatures make that visible without knowing any linguistics. The player *sees* kinship before being told it.

---

## 2. CRYSTALLOGRAPHY OF WORDS — comparing chains, not cells

Replace "shared prisoners" (a set operation, shallow) with **path alignment** — the same move sequence compared segment by segment:

```
l j u b e z e n        THE CORRIDOR:  start-lateral → back-vowel → bilabial-stop → front-vowel → hiss → front-vowel → nasal
  | |    | |   | |
L i e b e   (de)       Liebe's segments map onto the corridor's skeleton
| |  |      |
l ʌ v      (en)        love maps onto the skeleton only at anchor points
```

Mechanically: align two phoneme chains by minimizing total segment distance (a tiny Needleman–Wunsch on the coordinates — 20 lines of code). The output is not "3 shared sounds." The output is:

- **anchor cells** (aligned within threshold) — the load-bearing skeleton
- **drifts** (aligned but offset by exactly one feature: /e/↔/ɛ/, /b/↔/p/) — *lawful* differences
- **insertions/deletions** — cells one language visits and the other skips
- **foreign cells** (/ʌ/, /æ/) — cells that exist in NO dimension but one

Each category renders differently: anchors pulse gold, drifts pulse silver, insertions hover as ghosts, foreign cells burn red. The word-comparison view is a **stratigraphy**: layers of sameness, lawful difference, and true strangeness. That stratigraphy — not the overlap — is the sailing view.

---

## 3. DRIFT — the space has weather

The single deepest fact hiding in your own data, currently unused:

```
Slovenian r: (3,5,1)  — the trill, at the alveolar ridge
German r:    (7,5,1)  — four slots BACK, in the throat
English r:   (3,6,1)  — one manner DOWN, a glide
```

**The same prisoner does not sit still across dimensions. It drifts.** Drift is a vector: German r drifted (−4, 0, 0) back; English r drifted (0, −1, 0) down into vowel country. And drift is not random — it follows **sound laws**, which are literally vector fields over the space:

| Law | The vector, in coordinates | What the game shows |
|---|---|---|
| Grimm's Law (Germanic) | p→f (0,0,0)→(1,2,0), t→θ, k→x: stops slacken into fricatives, −2 on manner | a **wind** blowing Germanic consonants down the manner axis |
| English Great Vowel Shift | long vowels chase each other around the vowel space | the vowel cells visibly rotate over the timeline |
| r-drift | German back, English down, Slovenian holds | three dimensions, three wind directions for the same prisoner |
| French/Spanish latin vowel collapse | 10 Latin vowels → 7 then → 5 | cells MERGE — two prisoners fuse into one cell |

**Mines are drift.** A mine (✱) on a cube should mean: *this prisoner is unstable in this dimension — it is moving, or it moved.* Mining /r/ in the German dimension doesn't give you a fact — it gives you a **trajectory**: here it was (3,5,1), here it drifted to (7,5,1), and the empty cell it left behind (3,5,1) now whispers. Empty cells left by drift are **the most valuable real estate in the game** — that's where substitutions happen, where loanwords land, where a language's accent lives. A French accent in English is, precisely, a Frenchman walking through drifted cells that English evacuated.

**Mechanic — DRIFT TRAILS:** toggle a layer that draws each drifting prisoner's historical path as a comet trail through the space. The space stops being an atlas and becomes a weather map. The player learns why German 'w' is /v/ and German 'v' is /f/: the whole Germanic fricative row got pushed one slot by a wind that blew two thousand years ago, and nobody has cleaned up since.

---

## 4. THE GEOMETRY OF RHyme AND LOVE — why chains feel alike

The deepest layer: **what actually makes ljubezen feel like it contains love and Liebe.** It is not shared cells. It is *structural positions*:

- All three words are built around the same **corridor**: liquid/lateral onset → rounded/high vowel → bilabial stop → front vowel.
- The bilabial stop /b/ sits at the **spatial center of gravity** of all three words — the anchor all three orbits pass through.
- ljubezen's later additions (z-e-n) walk back toward the nasal ridge — the same corridor *closed* with a cadence. Liebe just stops at the anchor. love takes the corridor and inverts it (onset→vowel→labiodental: it walks the corridor and then leaves through the teeth).

Formalizable: compute each word's **center of mass** and **inertia** in phonetic space. Words that translate each other tend to preserve center of mass even when sharing no cells at all (amor /a m o ɾ/ shares almost zero prisoners with love — its center of mass is still mid-space, its path still vowel→nasal→vowel→percussive). **Translation preserves geometry, not membership.** That's the engine under "sailing": you don't match words by cells, you match them by shape — and the game shows you amor orbiting the same empty center that love orbits, from a different door (the vowels instead of the consonants), with no shared prisoners at all.

This is why "shared prisoners" was too shallow: it cannot even see that amor and love rhyme *in structure*. Alignment + center-of-mass can. And it gives the classifier something real to do: score language membership by **path-shape distance**, not phoneme presence.

---

## 5. DIMENSION PHYSICS — languages as force fields

Each language dimension is not a costume list. It is a **field configuration**:

- **Occupied cells** — its inventory (already have)
- **Forbidding** — cells the language *actively avoids* (English forbids /x/, /ç/; German forbids /w/, /ð/; Slovenian forbids /ɪ/, /æ/, /w/) — render as **veils** over those cells when you play that dimension. The forbidden veils are a negative map of the language's identity.
- **Frequencies** — how often a cell is visited (English lives in /ð/ /ə/ /t/; a heatmap)
- **Co-occurrence rules** — which cells may touch in a chain (English /ŋ/ only at chain-ends; German /ç/ only after front vowels; Slovenian pairs *v* with /u/ or /ʋ/ contextually) — the **grammar of adjacency**, visible as allowed/forbidden line segments between cells

Play consequence: **forming chains in a foreign dimension while obeying your native adjacency rules produces your accent, live.** If the game accepts any chain but scores it against the target dimension's field configuration, then the player's "wrong" word is not marked wrong — it is *located*: "this chain is English-shaped German." That is a pedagogical weapon no language app has, and it falls directly out of the space you already defined.

**Sailing, properly:** dimension-jumping is not translation lookup. It is: keep your declared chain, re-evaluate it against the target field, and watch the chain *deform* — some cells hold (anchors), some drift (the wind of that dimension's sound laws), some fall into forbidden cells and must be re-chosen by the player. The player doesn't read what Liebe is. The player *deforms love into Liebe with their hands* and feels exactly which segments moved and why.

---

## 6. MINES, EXPANDED — what mining actually uncovers

Mines get a taxonomy, because "hidden meaning" was underspecified:

| Mine type | What detonates | Example | Emotion |
|---|---|---|---|
| **Drift mine** | a historical trajectory opens — the comet trail | /r/ in German | vertigo: the letter was never the sound |
| **Void mine** | a forbidden/absent cell in this dimension reveals what the language does INSTEAD | English has no /x/ → it splits into /k/ and /f/ (loch → lock, through → tough) | insight: absence shapes identity |
| **Collision mine** | two prisoners share one cell (flagged prisoners: y/i, ø/e, ʊ/o) | ü = i + rounded lips | intimacy: sounds are postures on the same cell |
| **Cognate mine** | your declared word, aligned against the same corridor in another dimension, turns out to be a skeleton match | love ↔ Liebe ↔ ljubezen anchor on /l/ + /b/ | awe: kinship you can point at |
| **Contraband mine** | a loanword's chain still carries its foreign segments | Slovenian džem keeps /d͡ʒ/, a cell Slovenia never built | humor: a smuggled sound |

Mining is the act that converts covered cubes into **testimony**. The number on the covered cube (mine_number) is the *promise* of testimony; the detonation is the payoff. Different mine types pay in different emotions — that's your emotional arc, mechanically fed.

---

## 7. WINNING IS CONTINUING — made operational

"Winning is the act of continuing" needs a loop, or it's poetry. The loop the mechanics above produce:

```
REVEAL cells  →  CHAIN them  →  DECLARE a word (lexicon grows)
     →  the declared word OPENS its corridor: nearby cells it touched
        gain new mine numbers (the space re-tallies around what you know)
     →  new numbers = new promises  →  SAIL to see the word's skeleton
        in another dimension  →  the drift trails + veils you meet there
        point at cells you haven't mined
     →  REVEAL again — but now with a question the space itself posed
```

Every declared word re-prices the covered cubes around it. Not procedurally-infinite filler — a *measured* frontier: each word you own changes the numbers on neighboring covered cubes, so the space stays ahead of you by exactly one good question. That is "almost infinite" done honestly: the map is finite (46+ prisoners, a few dimensions), the **stratigraphy is not** (each cell holds drift, veils, collisions, cognates — four layers of testimony per cell, mined one at a time).

---

## 8. WHAT TO BUILD, REVISED ORDER

The spec's M1–M5 stay; the phonetics module grows teeth in this order:

1. **M2.5 — Alignment** (after words, before sailing): Needleman–Wunsch on coords; anchors/drifts/inserts/foreign; the stratigraphy renderer. *This replaces "shared prisoners" everywhere.*
2. **M4 — Field physics, not translation lookup**: occupancy, forbidden veils, frequency heat, adjacency rules per dimension; chains scored against fields; "English-shaped German" feedback.
3. **M4.5 — Drift**: sound-law vectors as a layer; comet trails; drifted-cell vacuums as the accent map.
4. **M5 — Mine taxonomy**: the five mine types, each with its own detonation UI and voice line.

New data needed (small, verifiable): sound-law vector table (~10 laws), per-language forbidden lists and adjacency rules (~30 lines JSON), frequency ranks (crude is fine). Everything else derives from `phonetic_coordinates.py` as written.

---

## 9. THE SEED STONE, RE-SEEN

love /l ʌ v/ — three prisoners, one corridor, one red foreign cell (/ʌ/, which exists nowhere but here).
Liebe — the same corridor, express-sampled, ending on the schwa's resigned cell.
ljubezen — the corridor walked slowly, closed with a nasal cadence, opened by the cell English cannot spell, and containing, in its second half, the word for *word*.

The game is not that they share cells. The game is that they share a **corridor** — that meaning, across dimensions, keeps walking the same path through a space that no one built on purpose. Your mouth knew the corridor before any grammar did. The game's whole job is to make you watch yourself knowing it.