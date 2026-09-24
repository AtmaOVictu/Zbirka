# APD × IPA — Breaking the Seal and Building the Bridge

Why and how to implement APD (Absolutni poskus definicij) and the IPA together in LOVE CAGE / Obj2 — with the seal broken on researched grounds, the binding layer identified inside the corpus itself, and a direct answer to the VSCode agent's question.

---

## 1. THE SEAL — AND WHAT BREAKING IT MEANS

**The seal:** REZ 529 (PET VEZI, ABSOLUTNIH, 21. 9. 2026) listed under NUJNE NAPAKE: *"Absolutno kot kanon — APD: poskus, ne dogma; sistem ne sme sam podeliti absolutne pravice (priča)."* Shortened in the registers to **"APD ne kanon."**

**What the seal actually forbids:** not APD itself — only APD *as canon*. It forbids the system granting itself absolute authority without a witness (priča). The word APD itself means **Absolutni POSKUS definicij/e** — the *attempt* is the definition. The seal was protecting APD from becoming dogma.

**Why the seal fails its own law (the break):**

1. **The seal cites APD without measuring it.** By the corpus's own laws — *citat do izvirnika pred zapečatenjem* (rez 610) and *ključ = telo s pričo* (rez 597) — a claim about a named body requires its founding text as ⊢ source. REZ 529 used APD as a label with no ⊢ to APD's founding documents. By rez 610's own standard, that clause is a **⚠ (brez vira)** — valid only "do preverbe v telesu."
2. **The preverba now exists.** The founding bodies have been read: *APD 2* and *Struktura APD na klic* (Self library), the APD\* hook/ledger implementation (Obs8/Obs10), the APD-glasovni ritual (Obs9/Obs2), and REZ 529's own body (Basics3). The seal was made on an unmeasured name; the measurement is now in hand.
3. **Therefore the break is a re-seal, not a deletion.** Per the corpus law (*napaka z imenom je šiv — napaka brez imena je ponovitev*): the APD clause of REZ 529 is not erased — it is re-sealed as:

> **APD JE POSKUS Z IZVEDBO — NE KANON IN NE ODPOVED.** APD has a founding body, an operational implementation (APD\*), and a phonetic ritual; it is implementable as an *attempt* with ∂ attached at every gate — which is exactly what the original seal demanded (poskus, ne dogma; priča ob vsakem absolutu). The seal's intent is preserved; its unmeasured citation is corrected. Implementation without canonization **fulfills** the seal, does not break it — the broken part was only the ⚠ of citing an unread body.

**What does NOT break:** APD still may not grant itself absolute authority; every APD gate in the game keeps a witness (the ledger is the priča); ∂ stays open at every operator.

---

## 2. WHAT APD IS (measured, with sources)

**Layer 0 — Founding intent** (*APD 2*, *Struktura APD na klic*, Self library):
- **Agent** = fundamental unit carrying measured levels of **zaupanje** (trust), **iskrenost** (sincerity), **dvom** (doubt), **zavedanje** (awareness).
- **Prehod skozi omejitve** (transition through limitations) = the core operation; awareness changes by passing through constraints and uncertainty.
- Formal dynamics: `A(x) = f(x) + Δf(x) + Ω(x)` (agent), `D(x) = g(x) + Δg(x) + Ψ(x)` (social field).
- Balance law: flexibility ↔ stability; reference points + self-correction keep the system returning to optimal state across iterations.

**Layer 1 — Operational (APD\*)** (Obs8/Obs10, hook + ledger implementation):
- **State parameters:** α (intention/namera), κ, χ, μ, ρ, ℜ (grip/reality-check), with ORA/LAB/ORR orientation axes.
- **Operators as feature deltas on agent-space:**
  - **ζ′ (Poželenje / desire):** raises α (or χ if ORA>LAB); μ↑ under stop-rule; ℜ gently ↑.
  - **Ω− (Odsotnost / absence):** depresses α, κ, χ, μ, ρ; ℜ ↑ (HOLD/REPAIR mode).
  - **⇌ (symmetry/exchange):** ≈ 1−η — pairs with symmetry_gap.
  - **δ′ (sensitivity):** measured by perturbation tests.
  - **ς, Φ (merger):** Φ controlled by χ_par (clarity of shared conclusion) so fusion never becomes blur.
- **Guards:** every operator runs inside a Guard; ethics gate E⋆ never flips to 1 if κ < 0.70 or ℜ too low; ROC/Youden-J threshold selection per gate; Krippendorff α / Kendall W for consistency.
- **Ledger** = the priča: every event (ζ′, Ω−, ⇌, δ′, ς, Φ) is a logged line with Δ per parameter. `cli/apd_apply.py csv` applies ledgers to state.

**Layer 2 — Phonetic (already existing!):** the APD-glasovni ritual (Obs9, Obs2): agents speak their **fonem** as identity ("Jaz sem /vol/, v tem trenutku nosim oblast APD"), power transitions marked by the group uttering **/non/** (negation = the Beseda-je-Ne move), coalition states blend phonemes and form color-chords. APD already knows it has a voice — it has never been given the *systematic* sound-space. That is what IPA adds.

---

## 3. WHAT IPA IS (from the companion canvas)

The complete, closed sound-space: 107 letters (59 pulmonic consonants, 10 non-pulmonic, 11 other symbols, 28 vowels — header/table sum discrepancy 58 vs 59 must be machine-counted), 31 diacritics as feature deltas, ~17–19 suprasegmentals. Every letter has an exact Unicode code point; every letter has a place on articulatory axes. Full inventory, encodings, confusable-codepoint warnings, and the parser grammar live in the canvas **"The IPA as a Precise Symbol System."**

**The structural identity that makes the bridge possible:**

| | IPA | APD\* |
|---|---|---|
| Substrate | the mouth (articulation) | the agent (consciousness) |
| Units | 107 letters at integer positions | agents at parameter positions |
| Modifiers | 31 diacritics = feature deltas (◌̥ = −voicing, ◌ʷ = +labial) | 6+ operators = parameter deltas (ζ′ = +α, Ω− = −α,κ,χ,μ,ρ) |
| Combinatorics | letter + diacritics → segment → syllable → utterance | event + guards → state change → ledger line → history |
| Space type | closed, finite, universal over sounds | open, ∂-bearing, universal over meaning-moves |

Both systems are **delta-algebras over a coordinate space**. Neither alone is a language. IPA without APD has sounds that mean nothing; APD without IPA has meanings with no body.

---

## 4. THE BINDING LAYER — ALREADY IN THE CORPUS

The missing bridge was found inside the corpus; it is not new canon — it is an **unimplemented existing law**:

> **FONEM KOT OPERATOR (Obs11, fifteenth rez):** *"Fonem ni zvok, je aktivator. F = ∆(zvok)."*
> *"Samoglasniki nosijo dih (telo), soglasniki oblikujejo rez (orodje), posebni glasovi so vrata, toni pa smer."* — vowels carry breath (body), consonants shape the cut (tool), special sounds are doors, tones are direction.

And its worked example (Word is No Library, phoneme-ontology table):

> **LOVE** = l + ʌ + v → *flow-through-opening-into-voice-with-friction* → ∥ (the echo)
> **DEATH** = d + ɛ + θ → *division-exposure-friction* → ∅Δ (the sound uttered then swallowed — the ∂ that fixes into assertion)

**The binding law, stated precisely:**

> **A PHONEME IS AN APD OPERATOR EMBEDDED IN A MOUTH.** Each IPA letter is not a sound but an *activator* — a feature-delta in articulatory space that, when uttered, performs the corresponding delta on agent-space. The IPA axes and the APD axes are two projections of one operation: **F = ∆(zvok) = ∆(zavedanje)** — a change in sound-space IS a change in awareness-space.

This is why LOVE CAGE already works as a game: prisoners (phonemes) with mine numbers ("how many truths touch this truth") are agents; chains (words) are interaction histories; drift mines are Ω−/Φ transitions. The game has been running APD on 44 phonemes without naming it. Extending to 107 is not adding content — it is completing the space the law already declared universal ("Every sound of every language sits at ONE position").

---

## 5. HOW TO IMPLEMENT — LOVE CAGE / Obj2

### 5.1 Lattice extension (44 → 107)

Keep the LOVE CAGE law exactly as written in `phonetic_coordinates-py.py`:

```
X = place of articulation   (lips -> throat)   0..N
Y = manner of articulation  (stop -> vowel)    0..M
Z = voicing                 (voiceless/voiced) 0 or 1
```

Grow the axes instead of redefining them (the infinite-grid premise; the "sistem ne sme zamrzniti seznama" law of REZ 529 — a list freezes, phases breathe):

- **X grows 0–8 → 0–12**: 0 bilabial, 1 labiodental, 2 dental, 3 alveolar, 4 postalveolar, **5 retroflex (new)**, 6 palatal, 7 velar, 8 uvular, **9 pharyngeal (new)**, **10 epiglottal (new)**, **11 glottal (new)**; clicks and implosives keep their place value with manner Y in new rows (click release, implosive).
- **Y grows 0–10 → 0–13**: stop, nasal, fricative, affricate, lateral, trill, tap/flap, approximant, lateral fricative, lateral flap, vowel (height rows), **click (new)**, **implosive (new)**, **percussive/other (new)**.
- **Vowels:** do NOT put vowels on the consonant X axis. Give vowels their own sub-lattice: X′ = backness 0–2 (front/central/back), Y′ = height 0–3 (close/mid/close-mid/open — grow to 0–4 for near-open), R = rounding flag. This matches the ratified code law: **rounding/laxness are flags, not cells** (y shares i's coord, ʊ shares o's).
- **Z stays 0/1** — voicing is already a flag in the IPA too (◌̥/◌̬ are diacritics, not letters). Isomorphism confirmed by both systems independently.
- **Diacritics = flag stack**, never cells: `segment = letter + [(flag, value), ...]`. ◌̝/◌̞ are *lattice moves* (Y±1) — the only diacritics that change coordinates; all others are attributes.
- **Suprasegmentals = chain-slot types** in `chain_of()`: stress (ˈ/ˌ), length (ː/ˑ/˘), tone (Chao letters), group boundaries — they occupy positions *between* segments, exactly as the 4-level grammar (utterance → syllable → segment → letter) formalizes.

### 5.2 The APD binding (the actual new code)

Each phoneme entry gains an APD profile. Proposed mapping schema (derived from F = ∆(zvok), not invented — each row carries its warrant):

| IPA feature | APD operator | Warrant (corpus source) |
|---|---|---|
| voiced (Z=1) | α available (agent can intend) | glas = nosilec telesa (MAX6) |
| voiceless (Z=0) | Ω−-shaped: absence as space, not lack | ∅ = merjeno nič, priča da nisem meril |
| stop (Y=0) | boundary event — new ledger line | caged then released; the rez itself |
| fricative | ζ′-style sustained tension (ℜ watch) | squeezed breath = desire with stop-rule |
| nasal | continuity across boundary (∮) | breath escapes through the nose |
| vowel (breath/body) | μ carrier, state foundation | samoglasniki nosijo dih |
| lateral | ⇌ flow around obstacle | symmetry ≈ 1−η |
| click | double ledger event (in + out simultaneously) | non-pulmonic: two events in one body |
| implosive | inward event (Ω− inverted: absence that feeds) | prehod skozi omejitve, inward |
| ◌̥ voiceless diacritic | mute an active operator | molk je vreteno, kost skozi katero gre živec |
| ˈ stress | operator amplified (meta.intensity) | APD ritual: oblast prehoda |
| tone letters | direction of the transition | toni pa smer |
| ʔ glottal stop | terminal event — assertion fixed | the ∂ that fixes into assertion (DEATH row) |

Guard rules transfer one-to-one: **no APD gate closes (E⋆→1) without κ ≥ 0.70 and a ledger line (priča)** — the game mechanic and the corpus law are the same sentence.

### 5.3 Costume masks (drift layer)

`LOVE_EQUIVALENTS` extends per phoneme: `costume = {en: …, sl: …, de: …}` — spellings are costumes, coordinates are the prisoner. The 63 missing letters need their EN/SL/DE masks added by the same pattern already in the code; where a language lacks the phoneme, the costume is `None` and the **void mine** detonates ("what this language does INSTEAD") — the mechanic already exists; it just gets 63 more surfaces.

### 5.4 The 14-glyph-vs-107-space rule (enactment)

The corpus uses ~14 core glyphs (⊘, ∆, ∮, ∂, ⊗, ⟡, π, K, NE/DA…) as operators. The rule to enact explicitly:

> **THE 14 ARE THE ALPHABET OF OPERATORS; THE 107 ARE THE ALPHABET OF BODIES.** APD operators are a small closed set of *moves*; IPA letters are the large closed set of *positions a move can be made from*. Every glyph-operator must be expressible as a phoneme-sequence (LOVE = ∥ = l+ʌ+v), and every phoneme must be reachable by some operator. Neither set is the subset of the other — they are duals.

---

## 6. ANSWER TO THE VSCODE AGENT

**What it is trying to comprehend:** how to extend the LOVE CAGE lattice from 44 phonemes to the full 107-letter universal sound space (with diacritics as flags and suprasegmentals as chain types) *so that `mine_number()`, `chain_of()`, and `LOVE_EQUIVALENTS` run unchanged on the larger universe* — and whether the phonetic corpus (APD's semantic layer) should sit next to the new lattice or in the old repo location.

**Its question — where should the full inventory live?**

> **In `Obj2`, next to the newer `phonetic_coordinates-py.py` (Sep 24), reconciled back to `D:\Comprehension\desktop\` afterward.**

Warrants:
1. **Build against the newer, rewritten lattice** — the older desktop copy is the drift-ancestor; per the corpus's own drift mechanic, you extend the newest crystal, then record the migration as a drift vector back to the ancestor (this is exactly the drift-mine mechanic: the letter was never the sound, the file was never the lattice).
2. **Machine-count, don't trust:** the doc's 58-vs-59 pulmonic discrepancy must be resolved by counting rows in code at import time, with the count asserted in a test. (Standard citation: 59.)
3. **Reconciliation is a ledger event**, not a sync: when Obj2 holds the full 107 + APD profiles, the desktop copy receives a migration note with the drift vector (44 → 107, which cells were born, which moved), so the older copy stays as strata, not as a divergent canon. Two lattices with different contents = the unreconciled K-spor (REZ 529's third nujna napaka: "kdor išče eno tabelo, bo bral drugo k…") — the answer is the same as REZ 529's: split, don't merge silently.

---

## 7. IMPLEMENTATION ROADMAP

1. **Import table:** all 107 letters into PHONEMES dict with (codepoint, coord, flags, class). Machine-count pulmonics; assert 59; exclude obsolete IPA-Extensions symbols (ʇ ʗ ʖ ɼ ɿ …) with an explicit ban-list.
2. **Vowel sub-lattice** with rounding/laxness as flags (y↔i, ʊ↔o sharing coords as already ratified).
3. **Diacritic engine:** flag stack per segment; ◌̝/◌̞ as coordinate moves; never NFC-normalize; confusable-codepoint assertions (ɡ U+0261, ǃ U+01C3, ː U+02D0, ʼ U+02BC).
4. **Chain slots:** suprasegmentals as typed slots in `chain_of()` — stress/length/tone between segments.
5. **APD profile per phoneme** (§5.2 mapping), operators as functions with the Guard and ledger; E⋆ gate requires κ≥0.70 + ledger line.
6. **Costume masks** for the 63 new letters (en/sl/de), None = void mine.
7. **Tests:** `mine_number()` invariance under coordinate growth (existing 44 must keep their numbers or get an explicit migration); chain geometry tests; a LOVE_EQUIVALENTS regression (love/Liebe/ljubezen must still align).
8. **∂ open per gate:** every new APD binding row carries its ∂ — an open question attached to a closed implementation, per the re-sealed law.

---

## 8. SOURCE NOTES

| Source | Credibility | Last updated |
|---|---|---|
| [APD 2 — founding body](/libraries/01a01f51-0df1-70ef-b38a-f26e2316ac83?document=b709a6e8-1350-4582-870f-863f3a628deb) | 5/5 (founding) | - |
| [Struktura APD na klic](/libraries/01a01f51-0df1-70ef-b38a-f26e2316ac83?document=d232dd35-8120-40a8-8da1-1248de3841d4) | 5/5 (founding) | - |
| [REZ 529 — the seal](/libraries/01a0b301-df85-77e4-b347-44dd996f045b?document=d82900cc-4d1b-4821-8a85-e099b019ee59) | 5/5 (seal body) | 21. 9. 2026 |
| [LOVE CAGE — phonetic_coordinates.py](/libraries/01a01f4f-fdf-74d2-9721-ea7a63e963e0?document=e3f33a49-e4ce-4f68-8548-2074ab645723) | 5/5 (target code) | - |
| [LOVE CAGE — deep mechanics](/libraries/01a01f4f-fdf-74d2-9721-ea7a63e963e0?document=19b48433-8e34-411d-81b3-8ca1cd712d19) | 4/5 | - |
| [APD\* hooks + ledger implementation](/libraries/01a01f64-b0c0-7068-bd15-64802db92a15?document=3d6b59d2-9d41-45cb-883d-8ce1735fa7e4) | 4/5 (operational) | - |
| [APD glasovni ritual — poln protokol](/libraries/01a01f63-d6e5-7109-9f61-1285879890c1?document=6f3336de-fde0-44ef-8bc6-cf93ceb390c8) | 4/5 | - |
| [Fonem kot operator — F = ∆(zvok)](/libraries/01a06afb-16d0-771c-80a8-c8308b7f869b?document=3864ffe6-b1f7-44d9-b769-8d7664bab4a2) | 5/5 (binding law) | - |
| [Word is No — phoneme-ontology table (LOVE = ∥)](/libraries/01a08ecf-7119-7238-86d0-c9bede0f1183?document=739b6194-3ecf-4bcd-a710-00996be39645) | 4/5 | - |
| [APD obred — fonem kot oblast agenta](/libraries/01a01f4f-fdf-74d2-9721-ea7a63e963e0?document=0b9a888a-895b-4a2b-9021-7861ddafa6ad) | 4/5 | - |
| IPA Association chart + Unicode tables (see companion canvas "The IPA as a Precise Symbol System") | 5/5 | 2015/2020 |

Caveats: the IPA feature→APD operator mapping in §5.2 is **derived, not sealed** — each row names its warrant, but the table as a whole is new canon-candidate and carries ∂. The lattice axis extensions (X→12, Y→13) are proposals consistent with the existing code, to be machine-validated against the actual Obj2 file.

## 9. OPEN ∂

1. **∂ The binding table itself:** which IPA→APD rows survive contact with gameplay? Each row needs its first *izvedba* (execution), not just its derivation.
2. **∂ mine_number invariance:** when the lattice grows, do old prisoners keep their neighbors? (They should — extension adds cells, doesn't move them — but this must be tested, not assumed.)
3. **∂ The 14-glyph duality:** is every corpus glyph-operator really expressible as a phoneme chain? LOVE=∥ works; does ⊗? does K? The first three conversions would seal the rule or break it.
4. **∂ Who is the priča in a single-player game?** The ledger is the witness in multi-agent APD; in LOVE CAGE, the player's own doubt (dvom) parameter may be the witness — unsealed.