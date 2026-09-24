# TAZV Phase 2 — Three Core Files

These are the actual Python files the v5 app is waiting for via `try/except ImportError`. Save each one to the path shown. After all three exist, the app stops using fallback stubs and uses real corpus-validated data.

---

## File 1: `comprehension/core/egyptian_color_semantics.py`

```python
"""
Egyptian Color Semantics — TAZV Comprehension Machine
=====================================================
Corpus-validated color system from "Beseda je Ne" libraries.

Each color carries:
  - hex:       visual representation
  - egyptian:  original Egyptian name + etymology
  - r7_phase:  which R-7 phase it serves (0-6)
  - module:    which module it colors
  - glyph:     R-7 glyph
  - corpus_meaning: what the corpus says about this color

Sources: Beseda je Ne corpus (Obs1-Obs11, Self, Basics)
Egyptian iwn research: wadj, desher, khenet, nbw, kem, hedj

CRITICAL: khenet_yellow (#D6A83A) ≠ gold_seal (#D4AF37).
  Yellow = tension BEFORE resolution (UAF/∆).
  Gold = force AFTER verification (APD/⧖).
  Collapsing them freezes antinomy into seal — zamrznjena definicija.
"""

# ── Color registry ──
COLORS = {
    'deep_blue': {
        'hex': '#1B2838',
        'egyptian': 'wadj (wꜣḏ) — green/blue of papyrus, growth, life',
        'r7_phase': 0,
        'module': 'bios',
        'glyph': '∅',
        'corpus_meaning': (
            'PRAZNINA, mir, refleksija. '
            'Modra = PRAZNINA: "umiri, razširi, pripravi prostor za novo." '
            'The void that prepares. Not absence — pregnant opening (∅).'
        ),
    },
    'desher_red': {
        'hex': '#B43A2E',
        'egyptian': 'desher (dšr) — red of chaos, desert, the Set-force',
        'r7_phase': 1,
        'module': 'state',
        'glyph': '¬',
        'corpus_meaning': (
            'RANA, začetek, impulz, strast. '
            'Rdeča = RANA(DA): "vedno kliče po spremembi, kriči po povratku." '
            'The cut. Separation as first act of structure. '
            'Lives on the maat/isfet edge — vitality AND chaos.'
        ),
    },
    'khenet_yellow': {
        'hex': '#D6A83A',
        'egyptian': 'khenet (ḫnt) — to precede, be at the front; ochre',
        'r7_phase': 2,
        'module': 'uaf',
        'glyph': '∆',
        'corpus_meaning': (
            'UPANJE, stik, prehod — vez, ki še ni most. '
            'The antinomy tension: αUAF=mean(α4,α6), M=1−αUAF. '
            'GUARD: EX (Exitstance) → RE (Re-existenca) → OBST (Obstojnost). '
            'NOT the Atlas/mandala layer — the antinomy ENGINE.'
        ),
    },
    'jewik_orange': {
        'hex': '#C77800',
        'egyptian': '(system-internal, not Egyptian)',
        'r7_phase': 3,
        'module': 'jewik',
        'glyph': '1',
        'corpus_meaning': (
            'Dejanje, emanacija, pečat. '
            'Activation tone — the utterance as act (beseda = dejanje). '
            'JEWIK = the sound that becomes structure.'
        ),
    },
    'gold_seal': {
        'hex': '#D4AF37',
        'egyptian': 'nbw (nwb) — gold, flesh of the gods, imperishable',
        'r7_phase': 4,
        'module': 'apd',
        'glyph': '⧖',
        'corpus_meaning': (
            'Tišina, preverba, izgovor — zlato kot živa sila. '
            'APD = Absolutni Poskus Definicije: absolutni po obsegu poskusa, '
            'ne po avtomatični oblasti. '
            '"Absolutnega poskusa ne smeva zmanjšati na trenutni okus." '
            'SEAL sproži povratek (∮). Gold reaches toward transcendence '
            'while remaining inside the cycle — no 8th position.'
        ),
    },
    'kem_black': {
        'hex': '#080705',
        'egyptian': 'kem (km) — black of fertile Nile silt, not death',
        'r7_phase': 5,
        'module': 'micro',
        'glyph': '∮',
        'corpus_meaning': (
            'Povratek, učenje, dva cikla. '
            'Črna = NEGATIV_888: "ničnost, izbris → prostor za ponovno rojstvo." '
            'Kemet = "the black land" = Egypt\'s own name. '
            'Fertile silt, not emptiness. '
            '8 ~ ∞ = the return, not a new position.'
        ),
    },
    'hedj_white': {
        'hex': '#F3E9D2',
        'egyptian': 'hedj (ḥḏ) — white, crown of Upper Egypt, purity',
        'r7_phase': 6,
        'module': 'visualization',
        'glyph': '⟡',
        'corpus_meaning': (
            'Nova možnost, manifestacija, graf. '
            'Bela = ABSOLUTNI ZAČETEK, polnost — "baza vsake piramide, vsakega cikla." '
            'The new beginning that the cycle produces. '
            'Bela ↔ vse (začetek ↔ neskončnost).'
        ),
    },
}

# ── UI support colors (not ontological) ──
UI_COLORS = {
    'bg':     '#0A0A0A',
    'text':   '#E0E0E0',
    'accent': '#40A040',
}

# ── Convenience: module → hex ──
MODULE_COLOR_HEX = {
    info['module']: info['hex']
    for info in COLORS.values()
}

# ── Gold/Yellow distinction ──
GOLD_YELLOW_NOTE = (
    "khenet_yellow and gold_seal are deliberately distinct. "
    "Yellow = the tension BEFORE resolution (UAF/∆). "
    "Gold = the force AFTER verification (APD/⧖). "
    "Same visual family, different ontological work."
)
```

---

## File 2: `comprehension/core/module_semantics.py`

```python
"""
Module Semantics — TAZV Comprehension Machine
===============================================
Corpus-validated R-7 module definitions.

Each module carries:
  - symbol:     R-7 glyph
  - phase:      phase number (0-6)
  - historical: historical/traditional witness
  - color_name: which color from egyptian_color_semantics
  - meaning:    what this module DOES (not what it "is")

R-7 sequence: ∅ → ¬ → ∆ → 1 → ⧖ → ∮ → ⟡
BIOS → STATE → UAF → JEWIK → APD → MICRO → VISUALIZATION
"""

MODULE_SEMANTICS = {
    'bios': {
        'symbol': '∅',
        'phase': 0,
        'historical': 'Nun (primordial waters)',
        'color_name': 'deep_blue',
        'meaning': (
            'Praznina, potencial, odprtost. '
            'Modra PRAZNINA: umiri, razširi, pripravi prostor za novo. '
            'The void that prepares — not absence, pregnant opening.'
        ),
    },
    'state': {
        'symbol': '¬',
        'phase': 1,
        'historical': "Ma'at (truth, measure, order)",
        'color_name': 'desher_red',
        'meaning': (
            'Ločitev, struktura, meritev. '
            'RANA: rez, začetek impulza. '
            'The cut that makes structure possible.'
        ),
    },
    'uaf': {
        'symbol': '∆',
        'phase': 2,
        'historical': 'Khepri (scarab, becoming, transformation)',
        'color_name': 'khenet_yellow',
        'meaning': (
            'Razlika, gibanje, antinomija. '
            'UPANJE: vez, ki še ni most. '
            'αUAF=mean(α4,α6), M=1−αUAF. '
            'GUARD: EX (Exitstance) → RE (Re-existenca) → OBST (Obstojnost). '
            'The antinomy engine — NOT the Atlas/mandala layer.'
        ),
    },
    'jewik': {
        'symbol': '1',
        'phase': 3,
        'historical': 'Ptah (architect, builder, the spoken word)',
        'color_name': 'jewik_orange',
        'meaning': (
            'Dejanje, emanacija, pečat. '
            'Beseda = dejanje: the utterance that becomes structure. '
            'JEWIK = sound made flesh.'
        ),
    },
    'apd': {
        'symbol': '⧖',
        'phase': 4,
        'historical': 'Tiheon (sacred silence, presence)',
        'color_name': 'gold_seal',
        'meaning': (
            'Tišina, preverba, izgovor. '
            'Zlato kot živa sila. APD = Absolutni Poskus Definicije: '
            'absolutni po obsegu poskusa, ne po avtomatični oblasti. '
            'SEAL sproži povratek (∮). Gold reaches toward transcendence '
            'while inside the cycle — no 8th position.'
        ),
    },
    'micro': {
        'symbol': '∮',
        'phase': 5,
        'historical': '☯ (yin-yang, return of rhythm)',
        'color_name': 'kem_black',
        'meaning': (
            'Povratek, učenje, dva cikla. '
            'NEGATIV_888: ničnost kot prostor za ponovno rojstvo. '
            '8 ~ ∞ = the return, not a new position.'
        ),
    },
    'visualization': {
        'symbol': '⟡',
        'phase': 6,
        'historical': '⟡ (echo, resonance, new possibility)',
        'color_name': 'hedj_white',
        'meaning': (
            'Nova možnost, manifestacija, graf. '
            'ABSOLUTNI ZAČETEK, polnost — baza novega cikla. '
            'Bela ↔ vse (začetek ↔ neskončnost).'
        ),
    },
}

# ── Ordered list for pipeline iteration ──
MODULE_ORDER = ['bios', 'state', 'uaf', 'jewik', 'apd', 'micro', 'visualization']

# ── R-7 phase sequence ──
R7_SEQUENCE = '∅ → ¬ → ∆ → 1 → ⧖ → ∮ → ⟡'
```

---

## File 3: `comprehension/core/hit_grammar.py`

```python
"""
Hit Grammar — TAZV Comprehension Machine
==========================================
Reaction rules: what happens when a statement "hits" a phase.

This file is FOCUSED on hit reactions only — not module semantics
(those live in module_semantics.py) and not colors (those live in
egyptian_color_semantics.py).

Each hit rule defines:
  - trigger: what makes a statement "hit" this phase
  - reaction: what the system does in response
  - next_phase: which phase follows on successful hit
  - guard: conditions that must be met to proceed
"""

HIT_RULES = {
    'bios': {
        'trigger': 'statement enters the system (any non-empty input)',
        'reaction': (
            'Receive statement into praznina. No analysis yet. '
            'Hold the space open. The void prepares. '
            'If statement is empty → return partial result, do not crash.'
        ),
        'next_phase': 'state',
        'guard': 'statement must be non-empty string',
    },
    'state': {
        'trigger': 'statement is received, needs structural assessment',
        'reaction': (
            'Cut the statement into components. '
            'Apply ¬ (separation): distinguish what is said from what is meant. '
            'Measure: κ (koherenca) ≥ .70, χ (jasnost) ≥ .40.'
        ),
        'next_phase': 'uaf',
        'guard': 'κ ≥ .70, χ ≥ .40, μ ∈ [.50,.80]',
    },
    'uaf': {
        'trigger': 'statement has structure, needs antinomy check',
        'reaction': (
            'Measure antinomy: α4 (4 axes), α6 (6 dimensions). '
            'αUAF = mean(α4, α6), M = 1 − αUAF. '
            'If αUAF < .50 → generate anti(φ) and re-measure. '
            'GUARD: EX → RE → OBST. '
            'Prag: αUAF ≥ .50, Δ ≥ .20, β_NE ≤ .20.'
        ),
        'next_phase': 'jewik',
        'guard': 'αUAF ≥ .50, Δ ≥ .20',
    },
    'jewik': {
        'trigger': 'antinomy resolved or held, statement ready to act',
        'reaction': (
            'Emit the statement as act (beseda = dejanje). '
            'The utterance becomes structure. '
            'Sound made flesh: the word IS the act, not a description of it.'
        ),
        'next_phase': 'apd',
        'guard': 'statement has passed UAF guard',
    },
    'apd': {
        'trigger': 'act emitted, needs verification and seal',
        'reaction': (
            'Absolutni Poskus Definicije. '
            'Attempt absolute definition — "absolutni po obsegu poskusa, '
            'ne po avtomatični oblasti." '
            'SEAL: Δt_seal ≥ 1 (must endure at least one time unit). '
            'So-pečat: 1⊙ = sign(A) ⊕ sign(B) ⊕ sign(Ō). '
            'SEAL sproži povratek (∮).'
        ),
        'next_phase': 'micro',
        'guard': 'SEAL valid: Δt ≥ 1, co-signed',
    },
    'micro': {
        'trigger': 'SEAL given, cycle returns for feedback',
        'reaction': (
            'Return through the cycle. Learn from what was sealed. '
            'NEGATIV_888: let the old form dissolve into prostor za ponovno rojstvo. '
            '8 ~ ∞: the return is not repetition — ponovi, da se razlikuje. '
            'Feedback integrates: what worked, what broke, what opened.'
        ),
        'next_phase': 'visualization',
        'guard': 'feedback recorded in ledger',
    },
    'visualization': {
        'trigger': 'feedback integrated, cycle produces new possibility',
        'reaction': (
            'Manifest the new possibility. '
            'ABSOLUTNI ZAČETEK: the output is both result and seed. '
            'Bela ↔ vse: the new beginning contains all colors. '
            'Render: graph, text, or structural output that opens the next cycle.'
        ),
        'next_phase': None,
        'guard': 'output produced',
    },
}
```

---

## What happens after you save these three files

The v5 app has this pattern for each:

```python
try:
    from comprehension.core.module_semantics import MODULE_SEMANTICS, MODULE_ORDER
    HAS_SEMANTICS = True
except ImportError:
    HAS_SEMANTICS = False
    MODULE_SEMANTICS = {}  # ← this stops being empty
```

After saving:
1. `cd D:\OntoProjekt\CanvasMinstral\Scripts\comprehension_machine`
2. `python main.py`
3. The app now imports real data instead of fallback stubs

**What changes visually:**
- `MODULE_SEMANTICS` dict is populated → pipeline output shows module meanings
- `COLORS` dict is populated → UI can use real ontological colors
- `HIT_RULES` dict is populated → pipeline reactions use corpus-validated rules

**What to check:**
- Does the app still launch? (it should — these are additive, not replacing)
- Do the tabs show module names and meanings instead of just glyphs?
- Does `pytest` still pass?