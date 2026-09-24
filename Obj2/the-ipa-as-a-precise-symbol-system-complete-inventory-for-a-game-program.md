# The IPA as a Precise Symbol System

A complete, implementation-ready inventory of the International Phonetic Alphabet: every letter, diacritic, and suprasegmental mark, with its Unicode encoding, official meaning, and structural rules for parsing/validating IPA strings in software.

## Question

What is the exact, defined set of IPA symbols — with encodings and semantics — that can be embedded as a closed symbol system in a game or program?

## Executive Summary

1. **The core alphabet is 107 letters** (consonants and vowels), **31 diacritics**, and a set of **suprasegmental marks** (stress, length, tone, grouping — counted variously as 11 chart marks + 5 tone letters + up/downstep, hence the "17–19" you'll see quoted). Total full-chart inventory: **~160 distinct marks**.
2. **Every symbol has an exact Unicode encoding.** There are no ambiguous characters once you fix the encoding rules — the IPA is fully machine-representable today.
3. **The symbol set is compositional, not flat**: `letter + diacritics + modifiers` form a segment; segments + suprasegmentals form a syllable; syllables + prosodic marks form an utterance. Your game engine should model IPA as this 4-level grammar, not as a flat symbol list.
4. **Counting caveats you must know**: the "107" counts *letters* only; ejectives (pʼ) and affricates (t͡ʃ) are letter + modifier sequences, not distinct letters; pre-aspirated / vowel-modified forms like `ä` (a + ◌̈) are also sequences. Some sources inflate diacritic counts to 52 by including superscript release modifiers and extIPA marks.
5. **The last chart revision affecting symbol inventory was 2005** (added Ⱶ/ⱴ later withdrawn; current standard chart is the 2020/2023 revision). The chart is CC-BY-SA licensed by the IPA Association — free to reproduce with attribution.

## 1. The 107 Letters — Consonants

### 1.1 Pulmonic consonants (58, in the main table)

Ordered by manner, as on the official chart. "Pair = voiceless • voiced."

**Plosives (13)**

| Symbol | Unicode | Name |
|---|---|---|
| p | U+0070 | voiceless bilabial plosive |
| b | U+0062 | voiced bilabial plosive |
| t | U+0074 | voiceless alveolar plosive |
| d | U+0064 | voiced alveolar plosive |
| ʈ | U+0288 | voiceless retroflex plosive |
| ɖ | U+0256 | voiced retroflex plosive |
| c | U+0063 | voiceless palatal plosive |
| ɟ | U+025F | voiced palatal plosive |
| k | U+006B | voiceless velar plosive |
| ɡ | U+0261 | voiced velar plosive (note: single-storey g, U+0261, NOT U+0067) |
| q | U+0071 | voiceless uvular plosive |
| ɢ | U+0262 | voiced uvular plosive |
| ʔ | U+0294 | glottal plosive |

**Nasals (7)**

| Symbol | Unicode | Name |
|---|---|---|
| m | U+006D | bilabial nasal |
| ɱ | U+0271 | labiodental nasal |
| n | U+006E | alveolar nasal |
| ɳ | U+0273 | retroflex nasal |
| ɲ | U+0272 | palatal nasal |
| ŋ | U+014B | velar nasal |
| ɴ | U+0274 | uvular nasal |

**Trills (3) / Taps (2)**

| Symbol | Unicode | Name |
|---|---|---|
| ʙ | U+0299 | bilabial trill |
| r | U+0072 | alveolar trill |
| ʀ | U+0280 | uvular trill |
| ɾ | U+027E | alveolar tap/flap |
| ɽ | U+027D | retroflex tap/flap |

**Fricatives (23)**

| Symbol | Unicode | Name |
|---|---|---|
| ɸ | U+0278 | voiceless bilabial fricative |
| β | U+03B2 | voiced bilabial fricative (Greek beta) |
| f | U+0066 | voiceless labiodental fricative |
| v | U+0076 | voiced labiodental fricative |
| θ | U+03B8 | voiceless dental fricative (Greek theta) |
| ð | U+00F0 | voiced dental fricative |
| s | U+0073 | voiceless alveolar fricative |
| z | U+007A | voiced alveolar fricative |
| ʃ | U+0283 | voiceless postalveolar fricative (esh) |
| ʒ | U+0292 | voiced postalveolar fricative (ezh) |
| ʂ | U+0282 | voiceless retroflex fricative |
| ʐ | U+0290 | voiced retroflex fricative |
| ç | U+00E7 | voiceless palatal fricative (c-cedilla) |
| ʝ | U+029D | voiced palatal fricative |
| x | U+0078 | voiceless velar fricative |
| ɣ | U+0263 | voiced velar fricative (gamma) |
| χ | U+03C7 | voiceless uvular fricative (Greek chi) |
| ʁ | U+0281 | voiced uvular fricative |
| ħ | U+0127 | voiceless pharyngeal fricative (h-bar) |
| ʕ | U+0295 | voiced pharyngeal fricative (ayin) |
| ʜ | U+029C | voiceless epiglottal fricative |
| ʢ | U+02A2 | voiced epiglottal fricative |
| h | U+0068 | voiceless glottal fricative |
| ɦ | U+0266 | voiced glottal fricative |

**Lateral fricatives (2) / Approximants (5) / Lateral approximants (4)**

| Symbol | Unicode | Name |
|---|---|---|
| ɬ | U+026C | voiceless alveolar lateral fricative (belted l) |
| ɮ | U+026E | voiced alveolar lateral fricative |
| ʋ | U+028B | labiodental approximant |
| ɹ | U+0279 | alveolar approximant (turned r) |
| ɻ | U+027B | retroflex approximant |
| j | U+006A | palatal approximant |
| ɰ | U+0270 | velar approximant (turned m) |
| l | U+006C | alveolar lateral approximant |
| ɭ | U+026D | retroflex lateral approximant |
| ʎ | U+028E | palatal lateral approximant (turned y) |
| ʟ | U+029F | velar lateral approximant |

### 1.2 Non-pulmonic consonants (10 letters + ejective modifier)

| Symbol | Unicode | Name |
|---|---|---|
| ʘ | U+0298 | bilabial click |
| ǀ | U+01C0 | dental click (vertical bar) |
| ǃ | U+01C3 | (post)alveolar click — NOT the exclamation mark U+0021 |
| ǂ | U+01C2 | palatoalveolar click (double pipe) |
| ǁ | U+01C1 | alveolar lateral click (double pipe) |
| ɓ | U+0253 | voiced bilabial implosive |
| ɗ | U+0257 | voiced alveolar/dental implosive |
| ʄ | U+0284 | voiced palatal implosive |
| ɠ | U+0260 | voiced velar implosive |
| ʛ | U+029B | voiced uvular implosive |

**Ejectives** are not separate letters: formed as `letter + ʼ (U+02BC MODIFIER LETTER APOSTROPHE)` — e.g. pʼ, tʼ, kʼ, tɬʼ. Never use U+2019 (right single quote) for this.

### 1.3 "Other symbols" on the chart (coarticulated & extras)

| Symbol | Unicode | Name |
|---|---|---|
| ʍ | U+028D | voiceless labial-velar fricative (turned w) |
| w | U+0077 | voiced labial-velar approximant |
| ɥ | U+0265 | voiced labialized palatal approximant (turned h) |
| ɕ | U+0255 | voiceless alveolo-palatal fricative |
| ʑ | U+0291 | voiced alveolo-palatal fricative |
| ɺ | U+027A | alveolar lateral flap (turned long-leg r) |
| ɫ | U+026B | velarized alveolar lateral approximant (dark l) |
| ɧ | U+0267 | sj-sound (variable, Swedish) |
| ʡ | U+02A1 | epiglottal plosive |
| ɚ | U+025A | rhotacized schwa (schwa + r-hook, single code point) |
| ɝ | U+025D | rhotacized schwa (stressed variant, single code point) |

## 2. The 107 Letters — Vowels (28)

The vowel quadrilateral. Pairs = unrounded • rounded. These are the **cardinal reference values** — idealized tongue positions, excellent for a game grid (X = frontness/backness, Y = height, plus roundedness as a binary layer).

| Symbol | Unicode | Name |
|---|---|---|
| i | U+0069 | close front unrounded |
| y | U+0079 | close front rounded |
| ɨ | U+0268 | close central unrounded |
| ʉ | U+0289 | close central rounded |
| ɯ | U+026F | close back unrounded (turned m) |
| u | U+0075 | close back rounded |
| ɪ | U+026A | near-close near-front unrounded (small capital I) |
| ʏ | U+028F | near-close near-front rounded |
| ʊ | U+028A | near-close near-back rounded |
| e | U+0065 | close-mid front unrounded |
| ø | U+00F8 | close-mid front rounded |
| ɘ | U+0258 | close-mid central unrounded |
| ɵ | U+0275 | close-mid central rounded (barred o) |
| ɤ | U+0264 | close-mid back unrounded (ram's horn) |
| o | U+006F | close-mid back rounded |
| ə | U+0259 | mid central (schwa) |
| ɛ | U+025B | open-mid front unrounded (epsilon) |
| œ | U+0153 | open-mid front rounded |
| ɜ | U+025C | open-mid central unrounded (reversed epsilon) |
| ɞ | U+025E | open-mid central rounded |
| ʌ | U+028C | open-mid back unrounded (turned v) |
| ɔ | U+0254 | open-mid back rounded |
| æ | U+00E6 | near-open front unrounded (ash) |
| ɐ | U+0250 | open-mid/central (turned a) |
| a | U+0061 | open front unrounded |
| ɶ | U+0276 | open front rounded (small capital OE) |
| ɑ | U+0251 | open back unrounded (script a) |
| ɒ | U+0252 | open back rounded (turned script a) |

*(ä — open central — is written `a` + ◌̈ U+0308, i.e. a sequence, not one letter. That is why it is excluded from the 28-letter count.)*

## 3. The 31 Diacritics

Two encodings exist for many: the **combining** mark (attaches to a letter, ◌) and a **spacing modifier** "clone" (stands alone, e.g. ˳). For a program, always prefer the combining form on the letter.

| Mark | Unicode (combining) | Meaning |
|---|---|---|
| ◌̥ | U+0325 | voiceless |
| ◌̬ | U+032C | voiced |
| ◌ʰ | U+02B0 (spacing) | aspirated |
| ◌̤ | U+0324 | breathy voiced (murmured) |
| ◌̰ | U+0330 | creaky voiced |
| ◌̼ | U+033C | linguolabial |
| ◌̪ | U+032A | dental |
| ◌̺ | U+033A | apical |
| ◌̻ | U+033B | laminal |
| ◌̃ | U+0303 | nasalized |
| ◌̹ | U+0339 | more rounded |
| ◌̜ | U+031C | less rounded |
| ◌̟ | U+031F | advanced (articulated more front) |
| ◌̠ | U+0320 | retracted (articulated more back) |
| ◌̈ | U+0308 | centralized |
| ◌̽ | U+033D | mid-centralized |
| ◌̩ | U+0329 | syllabic |
| ◌̯ | U+032F | non-syllabic |
| ◌˞ | U+02DE (spacing) | rhoticity (r-colouring) |
| ◌ʷ | U+02B7 | labialized |
| ◌ʲ | U+02B2 | palatalized |
| ◌ˠ | U+02E0 | velarized |
| ◌ˤ | U+02E4 | pharyngealized |
| ◌̴ | U+0334 | velarized or pharyngealized |
| ◌̝ | U+031D | raised (→ closer vowel / fricative of plosive) |
| ◌̞ | U+031E | lowered (→ opener vowel / approximant of fricative) |
| ◌̘ | U+0318 | advanced tongue root (+ATR) |
| ◌̙ | U+0319 | retracted tongue root (−ATR) |
| ◌̚ | U+031A | no audible release (unreleased) |
| ◌ʼ | U+02BC | ejective |
| ◌͡ | U+0361 | affricate / double articulation tie (above); U+035C is the below variant |

**Release modifiers** (usually counted separately, spacing superscripts): ⁿ U+207F nasal release; ˡ U+02E1 lateral release; plus extIPA fricative-release marks.

**Combination rules** (important for a parser): diacritics have fixed canonical stacking positions — above, below, or superscript-after the letter. Multiple diacritics stack (e.g. [t̻ʰ] = laminal + aspirated, [n̥̊] etc.); Unicode canonical ordering sorts combining marks by combining class, which for IPA can conflict with typographic intent — **do not blindly NFC-normalize IPA strings**; NFC will merge some sequences into precomposed characters (ä, â) that the IPA treats as decomposed.

## 4. Suprasegmentals (prosody)

| Mark | Unicode | Meaning |
|---|---|---|
| ˈ | U+02C8 | primary stress (before the syllable) |
| ˌ | U+02CC | secondary stress |
| ː | U+02D0 | long (half again as long) — "triangle colon", not the colon U+003A |
| ˑ | U+02D1 | half-long |
| ˘ | U+02D8 | extra-short |
| \| | U+007C | minor (foot) group boundary |
| ‖ | U+2016 | major (intonation) group boundary |
| . | U+002E | syllable break |
| ‿ | U+203F | linking (no break) |
| ↗ | U+2197 | global rise |
| ↘ | U+2198 | global fall |

### Tone letters (Chao system)

Five level-tone letters form a composition system: one letter for a level tone, two joined for a contour.

| Mark | Unicode | Meaning |
|---|---|---|
| ˥ | U+02E5 | extra-high (top) tone |
| ˦ | U+02E6 | high tone |
| ˧ | U+02E7 | mid tone |
| ˨ | U+02E8 | low tone |
| ˩ | U+02E9 | extra-low (bottom) tone |
| ꜛ | U+A71B | upstep |
| ꜜ | U+A71C | downstep |

Contours are sequences: ˧˥ rising, ˥˩ falling, ˩˧˥ rising-falling, etc. Some contour tones also have precomposed combining marks in Combining Diacritical Marks Supplement (U+1DC0–1DFF), e.g. U+1DC8 rising-falling.

### Boundary/transcription marks

| Marks | Unicode | Meaning |
|---|---|---|
| [ ] | U+005B/U+005D | phonetic transcription (surface, concrete) |
| / / | U+002F | phonemic transcription (abstract, per language) |
| ( ) | U+0028/U+0029 | uncertain transcription |
| ⸨ ⸩ | U+2E28/U+2E29 | indistinguishable utterance |
| ⸢ ⸣ | U+2E22/U+2E23 | sound obscured |

## 5. Unicode blocks you will need

| Block | Range | Role |
|---|---|---|
| Basic Latin | U+0020–007E | p, b, t, d, a, e, i, o, u, j, k, w… |
| Latin-1 Supplement | U+0080–00FF | æ, ç, ø, ð |
| Latin Extended-A | U+0100–017F | ħ, œ, ŋ |
| Latin Extended-B | U+0180–024F | clicks ǀ ǁ ǂ ǃ, ɓ ɗ ɠ |
| **IPA Extensions** | **U+0250–02AF** | the core block (~90 chars; also holds obsolete symbols) |
| Spacing Modifier Letters | U+02B0–02FF | ʰ ʲ ʷ ː ˈ ˌ tone letters… |
| Combining Diacritical Marks | U+0300–036F | ◌̥ ◌̬ ◌̪ ◌̃ ◌̝ … |
| Greek and Coptic | U+0370–03FF | β θ χ |
| General Punctuation | U+2000–206F | ‖ ‿ |
| Superscripts/Subscripts | U+2070–209F | ⁿ |
| Arrows | U+2190–21FF | ↗ ↘ |
| Latin Extended-C/D/E/F, G | U+2C60–, A720–, AB30–, 10780–, 1DF00– | newer additions (ⱱ, ꞎ, 𝼄 𝼅 𝼆 …) |
| Combining Diacritical Marks Supplement | U+1DC0–1DFF | contour tones |
| Modifier Tone Letters | U+A700–A71F | ꜛ ꜜ |

**Fonts with full IPA coverage**: Doulos SIL, Charis SIL, Gentium Plus, Noto Sans/Serif, Brill. Generic system fonts (Arial, Times) miss IPA Extensions and mis-stack diacritics — critical if your game renders text.

## 6. Structural grammar (for your parser/validator)

A compact grammar of a well-formed IPA string — the backbone of a game engine:

```
utterance   := prosody* syllable (groupmark syllable)*
syllable    := stress? (onset)? nucleus coda? tone? length?
onset       := segment (link segment)?        ; affricates, e.g. t͡ʃ
segment     := letter diacritic*
letter      := pulmonic | click | implosive | other | vowel
diacritic   := combining* modifier*            ; e.g. ʷ, ʲ secondary articulations
nucleus     := vowel diacritic*
tone        := toneletter{1,3} | ꜜ | ꜛ
length      := ː | ˑ | ˘
stress      := ˈ | ˌ
groupmark   := | | ‖ | . | ‿
```

Validation logic worth implementing:
- **Letter class check**: every base character ∈ the 107-letter set (else warn: obsolete/nonstandard/extended).
- **Positional rules**: stress marks precede the syllable; length marks follow the nucleus; ˞ attaches to vowels; tie bars (◌͡) must have a letter on both sides.
- **Feature model**: each letter has attributes (place, manner, voicing / height, backness, rounding) — this is what makes the IPA *gameable*: diacritics are feature-deltas (e.g. ◌̥ = [voicing −], ◌ʷ = [+labial], ◌̝ = [height +1]). The whole system is essentially a 107-glyph encoding of a feature matrix, which is why it transcribes any human language.
- **Obscure/obsolete symbols warning**: IPA Extensions also contains retired symbols (ʇ, ʗ ʖ, ɼ, ɿ, ʅ, ʆ, ʓ, ʭ, ʬ, ɩ, ɷ, ǫ …). Exclude them or flag them.

## 7. Beyond the core chart (decide your scope)

- **extIPA** (Extensions for disordered speech, International Clinical Phonetics and Linguistics Association): extra symbols for whistling, gnashing, velopharyngeal fricatives (ʭ, ʬ), behavioral sounds. Include only if your game models non-speech.
- **Voice Quality Symbols (VoQS)**: phonation types over whole utterances (V, F, C).
- **IPA numbers** (Kiel 1989): every official symbol has a numeric ID (1–202), e.g. 301 = [a]. Superseded by Unicode but handy as compact internal IDs.
- **X-SAMPA / Kirshenbaum**: pure-ASCII equivalents of IPA (e.g. ʃ → "S", θ → "T"). Useful as an input fallback for players without an IPA keyboard.

## Source Notes

| Source | Credibility | Last updated |
|---|---|---|
| [International Phonetic Association — Full IPA Chart](https://www.internationalphoneticassociation.org/content/full-ipa-chart) | 5/5 | 2015 chart, CC-BY-SA |
| [Wikipedia — International Phonetic Alphabet](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet) | 4/5 | - |
| [Wikipedia — International Phonetic Alphabet chart](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet_chart) | 4/5 | 2020 chart revision |
| [Wikipedia — Phonetic symbols in Unicode](https://en.wikipedia.org/wiki/Phonetic_symbols_in_Unicode) | 4/5 | Unicode 17.0 era |

Conflicts: diacritic counts vary by source (31 core vs 52 including release modifiers and extIPA); "suprasegmental" counts range 17–19 depending on whether tone letters and upstep/downstep are included. The 107-letter figure is stable across all sources.

## Open Questions

1. Does your game need **tone** (relevant if you model tonal languages) or only segmental inventory?
2. Do you need **disordered speech / non-pulmonic extras** (extIPA scope)?
3. Input method: click-to-pick chart UI, IPA keyboard, or ASCII (X-SAMPA) fallback?

## Recommendations / Next Steps

1. **Model it as a feature matrix, not a glyph list** — encode each of the 107 letters as `{type, place, manner, voicing}` / `{height, backness, rounded}` and treat the 31 diacritics as feature deltas. This gives you validation, generation, and "sound blending" mechanics for free.
2. **Use the Unicode code points above as canonical IDs**; store strings decomposed (letter + combining marks), never NFC-normalized.
3. **Ship an IPA-capable font** (Doulos SIL or Noto) with the program.
4. For machine-readable data, the IPA Association chart page and the Unicode "Phonetic symbols in Unicode" table above can be scraped directly into your symbol table; cross-check with the IPA Numbers list in the 1999 Handbook.
5. If you want, I can generate the complete symbol table as **JSON/CSV** (symbol, code point, class, features) ready to drop into your codebase — say the word.