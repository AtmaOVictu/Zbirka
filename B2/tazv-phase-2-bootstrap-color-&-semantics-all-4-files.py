#!/usr/bin/env python3
"""
TAZV COMPREHENSION MACHINE — Phase 2 Color & Semantics Bootstrap
================================================================

CONTEXT FOR ASSISTANT (read this first):
----------------------------------------
This script is the authoritative corpus-validated alignment of the
TAZV Comprehension Machine's color system, module semantics, and
file architecture. It was generated from analysis of Luka Pintarič's
"Beseda je Ne" document libraries (Self, Obs1-Obs11).

PROJECT LOCATION: D:\OntoProjekt\CanvasMinstral\Scripts\comprehension_machine
WORKING DIR for this script: run from D:\OntoProjekt\CanvasMinstral\Scripts\

R-7 PIPELINE: ∅ → ¬ → ∆ → 1 → ⧖ → ∮ → ⟡
MODULES: BIOS, STATE, UAF, JEWIK, APD, MICRO, VISUALIZATION

4 ANSWERS FROM CORPUS ANALYSIS (authoritative):
  1. UAF = Univerzalno Antinomijsko Polje (∆ phase)
     - Measures antinomy amplitude: αUAF=mean(α4,α6), M=1−αUAF
     - GUARD protocol: EX (Exitstance) → RE (Re-existenca) → OBST (Obstojnost)
     - NOT the Atlas/mandala layer — it is the antinomy engine
     - Color: khenet_yellow — UPANJE, "vez ki še ni most" (bridge not yet bridge)
  2. Three color changes CONFIRMED:
     - APD → gold (⧖): "zlato kot živa sila", imperishable SEAL force
     - MICRO → kem_black (∮): NEGATIV_888, void as space for rebirth, 8~∞=povratek
     - VISUALIZATION → hedj_white (⟡): ABSOLUTNI ZAČETEK, polnost
  3. "Indent" menu → ∂ Globina (depth-control, not editor formatting)
     - Each level = one ontological layer deeper
     - ∂ = passage, partial derivative of being
  4. Gold = APD, NO 8th position
     - Atlas Mandala = 6 + 1 epilogue (ALL IS ONE O) = 7
     - "8" appears only as OSEM(∞) = the return = ∮ = 7 returning as difference
     - Gold belongs to APD (⧖), reaching toward transcendence while inside the cycle

GOLD/YELLOW DISTINCTION (critical):
  - khenet_yellow (#D6A83A) = UAF (∆) — ochre, antinomy tension, "vez ki še ni most"
  - gold_seal   (#D4AF37) = APD (⧖) — metallic gold, imperishable seal, "zlato kot živa sila"
  These are different phases doing different work. Identical hex would collapse
  the antinomy phase into the seal phase — a zamrznjena definicija (§49 JUST/ICE).

4-FILE ARCHITECTURE:
  egyptian_color_semantics.py → hex values + color names + etymology (what color IS)
  module_semantics.py         → phase, symbol, historical witness, meaning (what module DOES)
  hit_grammar.py              → hit reaction rules (what happens when statement enters phase)
  egyptian.qss                → visual application (how it LOOKS)

RUN: python tazv_phase2_bootstrap.py
Then: cd comprehension_machine && python main.py
"""
import os

BASE = "comprehension_machine"

# ═══════════════════════════════════════════════════════════════
# FILE 1: egyptian_color_semantics.py
# ═══════════════════════════════════════════════════════════════

EGYPTIAN_COLOR_SEMANTICS = '''"""
Egyptian Color Semantics — TAZV Comprehension Machine
=====================================================
Corpus-validated color system from "Beseda je Ne" libraries.

Each color carries:
  - hex:       visual representation
  - egyptian:  original Egyptian name + etymology
  - r7_phase:  which R-7 phase it serves
  - module:    which module it colors
  - corpus_meaning: what the corpus says about this color

Etymology notes:
  khenet (ḫnt) — "to be at the front, to precede" — ochre/yellow as the
    forward-facing tension, the bridge-not-yet-bridge. Source: corpus
    color system: "Rumena = UPANJE, stik, prehod — vez, ki še ni most."
  desher (dšr) — "red" — the color of chaos, desert, the Set-force.
    Corpus: "Rdeča = RANA, začetek, impulz, strast."
  kem (km) — "black" — the black of the fertile Nile silt, NOT death.
    Corpus: "Črna = NEGATIV_888, ničnost, izbris → prostor za ponovno rojstvo."
  hedj (ḥḏ) — "white" — the color of purity, the crown of Upper Egypt.
    Corpus: "Bela = ABSOLUTNI ZAČETEK, polnost — baza vsake piramide."
  wadj (wꜣḏ) — "green" — growth, the papyrus plant. Used here as deep_blue
    for BIOS (∅): praznina, mir, refleksija — the void that prepares.
  nbw (nwb) — "gold" — the flesh of the gods, imperishable.
    Corpus: "zlato kot živa sila", "zlati rez kot most med nasprotji."
  jewik_orange — not Egyptian; system-internal. JEWIK = dejanje, emanacija.
    Corpus: activation tone, the act of utterance as fire.
"""

# ── Color registry ──
COLORS = {
    'deep_blue': {
        'hex': '#1B2838',
        'egyptian': 'wadj (wꜣḏ) — green/blue of papyrus, growth',
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
        'egyptian': 'desher (dšr) — red of chaos, desert, Set-force',
        'r7_phase': 1,
        'module': 'state',
        'glyph': '¬',
        'corpus_meaning': (
            'RANA, začetek, impulz, strast. '
            'Rdeča = RANA(DA): "vedno kliče po spremembi, kriči po povratku." '
            'The cut. Separation as first act of structure.'
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
            'Not the Atlas/mandala layer — the antinomy ENGINE.'
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
            'APD = Absolutni Poskus Deficije: absolutni po obsegu poskusa, '
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
            'A_PRAZNINA(NEGATIV): the space where rebirth becomes possible. '
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
# These share the same family but are ontologically different:
#   khenet_yellow (#D6A83A) = ∆ antinomy tension (ochre)
#   gold_seal   (#D4AF37) = ⧖ imperishable seal (metallic)
# Collapsing them would freeze the antinomy phase into the seal phase.
GOLD_YELLOW_NOTE = (
    "khenet_yellow and gold_seal are deliberately distinct. "
    "Yellow = the tension BEFORE resolution (UAF/∆). "
    "Gold = the force AFTER verification (APD/⧖). "
    "Same visual family, different ontological work."
)
'''

# ═══════════════════════════════════════════════════════════════
# FILE 2: module_semantics.py
# ═══════════════════════════════════════════════════════════════

MODULE_SEMANTICS = '''"""
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
"""

MODULE_SEMANTICS = {
    'bios': {
        'symbol': '\\u2205',
        'phase': 0,
        'historical': 'Nun (primordial waters)',
        'color_name': 'deep_blue',
        'meaning': (
            'Praznina, potencial, odprtost. '
            'Modra PRAZNINA: umiri, raz\\u0161iri, pripravi prostor za novo. '
            'The void that prepares \\u2014 not absence, pregnant opening.'
        ),
    },
    'state': {
        'symbol': '\\u00ac',
        'phase': 1,
        'historical': "Ma'at (truth, measure, order)",
        'color_name': 'desher_red',
        'meaning': (
            'Lo\\u010ditev, struktura, meritev. '
            'RANA: rez, za\\u010detek impulza. '
            'The cut that makes structure possible.'
        ),
    },
    'uaf': {
        'symbol': '\\u2206',
        'phase': 2,
        'historical': 'Khepri (scarab, becoming, transformation)',
        'color_name': 'khenet_yellow',
        'meaning': (
            'Razlika, gibanje, antinomija. '
            'UPANJE: vez, ki \\u0161e ni most. '
            '\\u03b1UAF=mean(\\u03b14,\\u03b16), M=1\\u2212\\u03b1UAF. '
            'GUARD: EX (Exitstance) \\u2192 RE (Re-existenca) \\u2192 OBST (Obstojnost). '
            'The antinomy engine \\u2014 NOT the Atlas/mandala layer.'
        ),
    },
    'jewik': {
        'symbol': '1',
        'phase': 3,
        'historical': 'Ptah (architect, builder, the spoken word)',
        'color_name': 'jewik_orange',
        'meaning': (
            'Dejanje, emanacija, pe\\u010dat. '
            'Beseda = dejanje: the utterance that becomes structure. '
            'JEWIK = sound made flesh.'
        ),
    },
    'apd': {
        'symbol': '\\u2316',
        'phase': 4,
        'historical': 'Tiheon (sacred silence, presence)',
        'color_name': 'gold_seal',
        'meaning': (
            'Ti\\u0161ina, preverba, izgovor. '
            'Zlato kot \\u017eiva sila. APD = Absolutni Poskus Deficije: '
            'absolutni po obsegu poskusa, ne po avtomati\\u010dni oblasti. '
            'SEAL spro\\u017ei povratek (\\u222e). '
            'Gold reaches toward transcendence while inside the cycle \\u2014 no 8th position.'
        ),
    },
    'micro': {
        'symbol': '\\u222e',
        'phase': 5,
        'historical': '\\u262f (yin-yang, return of rhythm)',
        'color_name': 'kem_black',
        'meaning': (
            'Povratek, u\\u010denje, dva cikla. '
            'NEGATIV_888: ni\\u010dnost kot prostor za ponovno rojstvo. '
            '8 ~ \\u221e = the return, not a new position.'
        ),
    },
    'visualization': {
        'symbol': '\\u27e1',
        'phase': 6,
        'historical': '\\u27e1 (echo, resonance, new possibility)',
        'color_name': 'hedj_white',
        'meaning': (
            'Nova mo\\u017enost, manifestacija, graf. '
            'ABSOLUTNI ZA\\u010cETEK, polnost \\u2014 baza novega cikla. '
            'Bela \\u2194 vse (za\\u010detek \\u2194 neskon\\u010dnost).'
        ),
    },
}

# ── Ordered list for pipeline iteration ──
MODULE_ORDER = ['bios', 'state', 'uaf', 'jewik', 'apd', 'micro', 'visualization']

# ── R-7 phase sequence ──
R7_SEQUENCE = '\\u2205 \\u2192 \\u00ac \\u2192 \\u2206 \\u2192 1 \\u2192 \\u2316 \\u2192 \\u222e \\u2192 \\u27e1'
'''

# ═══════════════════════════════════════════════════════════════
# FILE 3: hit_grammar.py
# ═══════════════════════════════════════════════════════════════

HIT_GRAMMAR = '''"""
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
            'Absolutni Poskus Deficije. '
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

# ── Hit cascade: ordered execution ──
HIT_CASCADE = [
    'bios', 'state', 'uaf', 'jewik', 'apd', 'micro', 'visualization'
]
'''

# ═══════════════════════════════════════════════════════════════
# FILE 4: ta3v_colors.qss
# ═══════════════════════════════════════════════════════════════

QSS = """\
/* ═══════════════════════════════════════════════════════════════
   TAZV Comprehension Machine — Egyptian QSS
   Corpus-validated R-7 color mapping
   ∅(blue) → ¬(red) → ∆(yellow) → 1(orange) → ⧖(gold) → ∮(black) → ⟡(white)
   ═══════════════════════════════════════════════════════════════ */

QWidget {
    background-color: #0A0A0A;
    color: #E0E0E0;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 13px;
}

QMainWindow {
    background-color: #0A0A0A;
}

/* ── Module tabs ── each phase carries its ontological color ── */

QTabWidget::pane {
    border: 1px solid #333;
    background-color: #111;
}

QTabBar::tab {
    background-color: #1a1a1a;
    color: #E0E0E0;
    padding: 8px 16px;
    border: 1px solid #333;
    border-bottom: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar::tab:selected {
    background-color: #222;
    font-weight: bold;
}

/* ∅ BIOS — deep blue (praznina) */
QTabBar::tab:nth-child(1) {
    color: #1B2838;
    border-top: 3px solid #1B2838;
}

/* ¬ STATE — desher red (RANA, cut) */
QTabBar::tab:nth-child(2) {
    color: #B43A2E;
    border-top: 3px solid #B43A2E;
}

/* ∆ UAF — khenet yellow (antinomy) */
QTabBar::tab:nth-child(3) {
    color: #D6A83A;
    border-top: 3px solid #D6A83A;
}

/* 1 JEWIK — orange (dejanje) */
QTabBar::tab:nth-child(4) {
    color: #C77800;
    border-top: 3px solid #C77800;
}

/* ⧖ APD — gold (imperishable seal) */
QTabBar::tab:nth-child(5) {
    color: #D4AF37;
    border-top: 3px solid #D4AF37;
    font-weight: bold;
}

/* ∮ MICRO — kem black (void for rebirth) */
QTabBar::tab:nth-child(6) {
    color: #555;
    border-top: 3px solid #080705;
}

/* ⟡ VISUALIZATION — hedj white (new beginning) */
QTabBar::tab:nth-child(7) {
    color: #F3E9D2;
    border-top: 3px solid #F3E9D2;
}

/* ── R-7 progress bar ── */
QProgressBar {
    border: 1px solid #333;
    border-radius: 3px;
    background-color: #111;
    text-align: center;
    height: 22px;
}

QProgressBar::chunk {
    background-color: #40A040;
    border-radius: 2px;
}

/* ── Input ── */
QTextEdit, QLineEdit {
    background-color: #111;
    color: #E0E0E0;
    border: 1px solid #333;
    border-radius: 3px;
    padding: 4px;
}

/* ── Buttons ── */
QPushButton {
    background-color: #1a1a1a;
    color: #E0E0E0;
    border: 1px solid #333;
    padding: 6px 16px;
    border-radius: 3px;
}

QPushButton:hover {
    background-color: #222;
    border-color: #40A040;
}

QPushButton:pressed {
    background-color: #0a0a0a;
}

/* ── Menu bar — ∂ Globina replaces "Indent" ── */
QMenuBar {
    background-color: #0a0a0a;
    color: #E0E0E0;
    border-bottom: 1px solid #333;
}

QMenuBar::item:selected {
    background-color: #1a1a1a;
}

QMenu {
    background-color: #111;
    border: 1px solid #333;
}

QMenu::item:selected {
    background-color: #222;
}

/* ── Status bar ── */
QStatusBar {
    background-color: #0a0a0a;
    color: #888;
    border-top: 1px solid #333;
}

/* ── Scrollbar ── */
QScrollBar:vertical {
    border: none;
    background: #0a0a0a;
    width: 10px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #333;
    min-height: 20px;
    border-radius: 4px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
"""

# ═══════════════════════════════════════════════════════════════
# WRITE FILES
# ═══════════════════════════════════════════════════════════════

files = {
    "comprehension/core/egyptian_color_semantics.py": EGYPTIAN_COLOR_SEMANTICS,
    "comprehension/core/module_semantics.py": MODULE_SEMANTICS,
    "comprehension/core/hit_grammar.py": HIT_GRAMMAR,
    "ta3v_colors.qss": QSS,
}

print("=" * 60)
print("TAZV Phase 2 — Color & Semantics Bootstrap")
print("Corpus-validated R-7 mapping")
print("=" * 60)
print()

for relpath, content in files.items():
    fullpath = os.path.join(BASE, relpath)
    dirpath = os.path.dirname(fullpath)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(fullpath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    size = os.path.getsize(fullpath)
    print(f"  OK  {relpath}  ({size} bytes)")

print()
print("Color assignments:")
print("  void  BIOS  ->  deep_blue      #1B2838  (praznina)")
print("  cut   STATE ->  desher_red     #B43A2E  (RANA)")
print("  diff  UAF   ->  khenet_yellow  #D6A83A  (antinomy)")
print("  act   JEWIK ->  jewik_orange   #C77800  (dejanje)")
print("  seal  APD   ->  gold_seal      #D4AF37  (imperishable)")
print("  ret   MICRO ->  kem_black      #080705  (rebirth void)")
print("  new   VIS   ->  hedj_white     #F3E9D2  (new beginning)")
print()
print("Gold/Yellow distinction:")
print("  khenet_yellow #D6A83A = antinomy tension (ochre)")
print("  gold_seal    #D4AF37 = imperishable seal (metallic)")
print()
print("4-file architecture:")
print("  egyptian_color_semantics.py -> what color IS")
print("  module_semantics.py         -> what module DOES")
print("  hit_grammar.py              -> what happens on HIT")
print("  ta3v_colors.qss             -> how it LOOKS")
print()
print("Next:")
print("  cd comprehension_machine")
print("  python main.py")
print()
print("Then continue to Phase 2 features:")
print("  - SQLite logging wired to UI")
print("  - 3 themes: void Temno / diff Ognjeno / ret Tok")
print("  - Export: JSON + HTML")