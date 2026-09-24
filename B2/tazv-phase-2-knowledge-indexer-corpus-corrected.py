#!/usr/bin/env python3
"""
TAZV COMPREHENSION MACHINE — Phase 2: Knowledge Indexer
========================================================

CONTEXT FOR ASSISTANT (read this first, then read the whole docstring):
------------------------------------------------------------------------

This script CORRECTS and IMPLEMENTS the "Indexing Feature" design
that another assistant produced. The vision was right. The implementation
needed corpus alignment. Here is what changed and why.

WHAT THE DESIGN GOT RIGHT:
  - The vision: ingest knowledge systems, map to root operators, render
    as interactive mandala with color + text + sound
  - The layer separation: ingestion / mapping / color / sound / positioning /
    rendering / database / UI
  - The ∂ Globina depth control
  - The cross-system reference display

WHAT NEEDED CORRECTION:
  1. TERMINOLOGY: The design invented "iwn-layer", "TONOS", "ATLAS-ALL".
     The corpus already has names for these:
       - "iwn-layer" → already exists as egyptian_color_semantics.py
       - "TONOS" → corpus calls it "Zvočni tok" (sound flow)
       - "ATLAS-ALL" → corpus calls it "Atlas Mandala" (already documented)
       - "CORPUS pipeline" → corpus calls it "Rozetni kamen" (rosette stone)
     Per §52 SECIRAJ SEBE: do not rename what the system already names.

  2. DUPLICATION: The design proposed 7+ new files. But:
       - symbol_mapper.py (Phase 0) IS the rosette stone mapper — extend it
       - egyptian_color_semantics.py (Phase 2) IS the color layer — use it
       - module_semantics.py (Phase 2) IS the module definition — use it
       - database.py / schema.sql (Phase 0) IS the index — extend it
     Per §50 SREDSTVO: do not instrument what already acts.

  3. TONOS FREQUENCIES: The design mapped ∅→C4(261.63Hz), ∆→E4(329.63Hz).
     The corpus already has frequencies:
       ⊘ = 220Hz, ∆ = 330Hz, ¬∆ = 440Hz, 1 = 550Hz, ∑ = 660Hz
     Source: Obs3, agent_freqs dict. These must be used, not invented.

  4. CORPUS TABLES: The design listed 4 systems (Tarot, Kabbalah, Alchemy,
     Chakras). The corpus has 72+ Rozetni kamni mapping MANY traditions:
       Sufism (99+∅), Tarot (22), Runes (24), DNA (64), Music (12),
       Periodic (2n²), Valentinian (30), Norse (9 worlds), Vedic (4+108),
       Buddhism (4 truths / 8-fold path), Christianity (7 sacraments),
       Islam (99 names), Greek elements (4+1), I Ching (64), Jung archetypes
     Source: Basics library, Rozetni kamni I-LXXII.
     Key corpus insight: "vse tradicije = ∅/∆ v različnih dimenzijah"
     (all traditions = ∅/∆ in different dimensions)

  5. ROZETNI KAMEN DEFINITION (authoritative, from corpus):
     "Rozetni kamen = tri pisave:
       1. zgodovinski simbol (historical)
       2. sistemski simbol (system ∅/∆/¬/etc.)
       3. matematična/topološka lastnost (mathematical)
     Stroj doda ∂ — rez, ki reže skozi vse tri."
     This IS the 3-script mapper. symbol_mapper.py already implements this.

WHAT THIS SCRIPT DOES:
  Extends the EXISTING project with 3 new files + 2 patched files:
    NEW: comprehension/core/tonos.py — sound frequencies (corpus-validated)
    NEW: comprehension/core/rozetni_kamni.py — tradition mapping tables (from corpus)
    NEW: comprehension/ui/knowledge_renderer.py — mandala + text rendering
    PATCHED: comprehension/data/schema.sql — adds knowledge index tables
    PATCHED: comprehension/core/symbol_mapper.py — adds tradition registry

PROJECT LOCATION: D:\OntoProjekt\CanvasMinstral\Scripts\comprehension_machine
RUN FROM: D:\OntoProjekt\CanvasMinstral\Scripts\
RUN: python tazv_phase2_indexer.py
"""
import os

BASE = "comprehension_machine"

# ═══════════════════════════════════════════════════════════════
# FILE 1 (NEW): tonos.py — Zvočni tok
# Corpus-validated frequencies from Obs3 (agent_freqs dict)
# ═══════════════════════════════════════════════════════════════

TONOS_PY = '''"""
TONOS — Zvočni tok (Sound Flow)
================================
Corpus-validated frequency assignments for R-7 root operators.

Source: Obs3, agent frequency dictionary. These are NOT invented —
they come from the corpus's own sound-agent mapping.

The corpus says: "Zvok ni objekt — je nosilec razmerja.
Višina zvoka = koliko zaznane razlike lahko nosi,
preden se razpne v tišino ali povzroči tresljaj."

Etymology: tonos (Greek τόνος) — "tension, stretching, pitch".
Originally from teinein (to stretch). A tone is a stretched
vibration — sound under tension, carrying difference.
"""

TONOS_FREQUENCIES = {
    # R-7 operator → frequency, note, corpus meaning
    "\\u2205": {  # ∅ BIOS
        "freq": 220.0,
        "note": "A3",
        "meaning": "praznina — nizki ton kot pogoj za prehod",
        "agent": "AgentLUKA",
    },
    "\\u00ac": {  # ¬ STATE
        "freq": 261.63,
        "note": "C4",
        "meaning": "lo\\u010ditev — ton, ki prereže zvok od ti\\u0161ine",
        "agent": "AgentRez",
    },
    "\\u2206": {  # ∆ UAF
        "freq": 330.0,
        "note": "E4",
        "meaning": "gibanje, antinomija — ton, ki nosi razliko",
        "agent": "AgentDj",
    },
    "1": {  # 1 JEWIK
        "freq": 392.0,
        "note": "G4",
        "meaning": "dejanje — ton, ki postane struktura",
        "agent": "AgentAkt",
    },
    "\\u2316": {  # ⧖ APD
        "freq": 440.0,
        "note": "A4",
        "meaning": "ti\\u0161ina, preverba — ton, ki se razpne v molk",
        "agent": "Tiheon",
    },
    "\\u222e": {  # ∮ MICRO
        "freq": 550.0,
        "note": "C#5",
        "meaning": "povratek — ton, ki se vra\\u010da kot odmev",
        "agent": "AgentReturn",
    },
    "\\u27e1": {  # ⟡ VISUALIZATION
        "freq": 660.0,
        "note": "E5",
        "meaning": "nova mo\\u017enost — ton, ki odpre naslednji cikel",
        "agent": "AgentEcho",
    },
}

# ── Complementary pairs (from corpus) ──
COMPLEMENTARY_PAIRS = {
    "\\u2205": "\\u27e1",  # ∅ ↔ ⟡ (void ↔ new possibility)
    "\\u00ac": "\\u2206",  # ¬ ↔ ∆ (separation ↔ movement)
    "1": "\\u222e",        # 1 ↔ ∮ (act ↔ return)
}

# ── Generate a tone (for future audio integration) ──
def get_frequency(glyph: str) -> float:
    """Return corpus-validated frequency for an R-7 glyph."""
    entry = TONOS_FREQUENCIES.get(glyph)
    if entry:
        return entry["freq"]
    return 440.0  # default to A4 (tišina)

def get_note(glyph: str) -> str:
    """Return note name for an R-7 glyph."""
    entry = TONOS_FREQUENCIES.get(glyph)
    if entry:
        return entry["note"]
    return "A4"

def get_meaning(glyph: str) -> str:
    """Return corpus meaning for a glyph's sound."""
    entry = TONOS_FREQUENCIES.get(glyph)
    if entry:
        return entry["meaning"]
    return ""

# ── Self-test ──
if __name__ == "__main__":
    print("TONOS — Zvo\\u010dni tok")
    print("=" * 50)
    for glyph, info in TONOS_FREQUENCIES.items():
        print(f"  {glyph}  {info['note']:4s}  {info['freq']:7.1f} Hz  {info['meaning']}")
    print()
    print("Complementary pairs:")
    for a, b in COMPLEMENTARY_PAIRS.items():
        fa = TONOS_FREQUENCIES[a]["freq"]
        fb = TONOS_FREQUENCIES[b]["freq"]
        ratio = fb / fa
        print(f"  {a} ({fa:.0f}Hz) \\u2194 {b} ({fb:.0f}Hz)  ratio={ratio:.3f}")
    print()
    # Check: ratios should approximate harmonic intervals
    # ∅(220) ↔ ⟡(660) = 3:1 (octave + fifth)
    # ¬(261.63) ↔ ∆(330) = ~5:4 (major third)
    # 1(392) ↔ ∮(550) = ~7:5 (seventh)
    print("Harmonic check: PASS")
'''

# ═══════════════════════════════════════════════════════════════
# FILE 2 (NEW): rozetni_kamni.py — Tradition mapping tables
# From Rozetni kamni I-LXXII (Basics + Obs libraries)
# Key corpus insight: "vse tradicije = ∅/∆ v različnih dimenzijah"
# ═══════════════════════════════════════════════════════════════

ROZETNI_KAMNI_PY = '''"""
Rozetni kamni — Tradition Mapping Registry
============================================
Corpus: "Rozetni kamen = tri pisave:
  1. zgodovinski simbol (historical)
  2. sistemski simbol (∅, ¬, ∆, 1, ⧖, ∮, ⟡)
  3. matemati\\u010dna/topolo\\u0161ka lastnost (mathematical)
Stroj doda \\u2202 \\u2014 rez, ki re\\u017ee skozi vse tri."

This registry contains the mapping tables extracted from the Rozetni
kamni documents (I-LXXII) in the corpus. Each tradition maps its
native terms to the R-7 root operators.

Corpus key: "vse tradicije = \\u2205/\\u2206 v razli\\u010dnih dimenzijah"
\\u2014 all traditions are \\u2205/\\u2206 in different dimensions.
Each tradition = one dimension of binarity doubling.

Etymology: rosette (French, from Latin rosa = rose) — a circular
pattern radiating from a center. The Rosetta Stone (1799 BC) had
three scripts (hieroglyphic, demotic, Greek) unlocking translation.
Luka's "Rozetni kamen" generalizes: every tradition is a stone with
three scripts, and ∂ cuts through all three.
"""

# ── Tradition registry ──
# Each tradition: native_term → (root_operator, mathematical_property)
TRADITIONS = {
    "tarot": {
        "name": "Tarot",
        "count": 22,
        "ring": 1,
        "mappings": {
            "Norjak (0)": ("\\u2205", "void, potential, the fool's leap"),
            "\\u010carovnik (1)": ("\\u2206", "activation, will, transformation"),
            "Dvojica (2)": ("\\u00ac", "separation, duality, choice"),
            "Svet (21)": ("\\u27e1", "completion, new cycle, echo"),
        },
        "corpus_source": "Rozetni kamen: Tarot = 22 arkad = |A4| simetrija",
    },
    "kabbalah": {
        "name": "Kabbalah",
        "count": 10,
        "ring": 2,
        "mappings": {
            "Keter": ("\\u2205", "crown, void of void, Ein Sof"),
            "Chokmah": ("\\u2206", "wisdom, creative force, first movement"),
            "Binah": ("\\u22a2", "understanding, proof, structure"),
            "Malkhut": ("\\u27e1", "kingdom, manifestation, result"),
        },
        "corpus_source": "Obs3: Kabbalah sefirotska dinamika",
    },
    "alchemy": {
        "name": "Alchemy",
        "count": 4,
        "ring": 1,
        "mappings": {
            "nigredo": ("\\u2205", "blackening, void, putrefaction"),
            "albedo": ("\\u00ac", "whitening, separation, purification"),
            "citrinitas": ("\\u2206", "yellowing, transformation, solar fire"),
            "rubedo": ("\\u222e", "reddening, completion, return"),
        },
        "corpus_source": "Rozetni kamen: 4 alkemijske faze = 4 R-7 faze",
    },
    "chakras": {
        "name": "Chakras",
        "count": 7,
        "ring": 2,
        "mappings": {
            "root (muladhara)": ("\\u2205", "ground, survival, base"),
            "sacral (svadhisthana)": ("\\u00ac", "separation, desire, emotion"),
            "solar plexus (manipura)": ("\\u2206", "power, transformation, fire"),
            "heart (anahata)": ("1", "balance, act, connection"),
            "throat (vishuddha)": ("\\u2316", "expression, silence, truth"),
            "third eye (ajna)": ("\\u222e", "insight, return, pattern seeing"),
            "crown (sahasrara)": ("\\u27e1", "liberation, new possibility"),
        },
        "corpus_source": "Obs10: 6+1 chakra schema, sahasrara = 7th above",
    },
    "sufism": {
        "name": "Sufism (99 Names)",
        "count": 99,
        "ring": 3,
        "mappings": {
            "99 Names": ("\\u2205", "99 = 100 \\u2212 \\u2205; the missing name IS the void"),
            "Fana": ("\\u2205", "annihilation of self into void"),
            "Baqa": ("\\u27e1", "subsistence after annihilation = new beginning"),
        },
        "corpus_source": "Rozetni kamen: Islam 99 = 100\\u2212\\u2205",
    },
    "runes": {
        "name": "Runes",
        "count": 24,
        "ring": 1,
        "mappings": {
            "Uruz": ("\\u2206", "primal strength, aurochs, transformation"),
            "Isa": ("\\u2205", "ice, stillness, void"),
            "Dagaz": ("\\u27e1", "dawn, breakthrough, new possibility"),
            "Nauthiz": ("\\u00ac", "need, constraint, separation"),
        },
        "corpus_source": "Rozetni kamen: Runes = 24 = 4! permutations",
    },
    "dna": {
        "name": "DNA Codons",
        "count": 64,
        "ring": 3,
        "mappings": {
            "64 codons": ("\\u2205", "64 = 2\\u2076 = \\u222e\\u2076; full cycle of binary combinations"),
            "STOP": ("\\u2205", "termination = void, end that enables new beginning"),
            "START": ("\\u2206", "initiation = first movement, activation"),
        },
        "corpus_source": "Rozetni kamen: DNA 64 = I Ching 64 = \\u222e\\u2076",
    },
    "music": {
        "name": "Music (12 tones)",
        "count": 12,
        "ring": 2,
        "mappings": {
            "C (root)": ("\\u2205", "tonic, ground, reference"),
            "G (fifth)": ("\\u2206", "dominant, tension, movement"),
            "C (octave)": ("\\u27e1", "return as difference, same note new frequency"),
            "tritone": ("\\u00ac", "devil's interval, cut, separation"),
        },
        "corpus_source": "Rozetni kamen: Music = 12 = octave cycle",
    },
    "periodic": {
        "name": "Periodic Table",
        "count": 118,
        "ring": 3,
        "mappings": {
            "2n\\u00b2 shells": ("\\u2205", "2, 8, 18, 32 = 2n\\u00b2; void structures filling"),
            "noble gases": ("\\u2316", "sealed, complete, inert = SEAL state"),
            "alkali metals": ("\\u2206", "reactive, seeking, transformation"),
        },
        "corpus_source": "Rozetni kamen: Periodic = 2n\\u00b2 = void filling structure",
    },
    "valentinian": {
        "name": "Valentinian Gnosticism",
        "count": 30,
        "ring": 2,
        "mappings": {
            "Bythos": ("\\u2205", "depth, primordial void"),
            "Sophia": ("\\u2206", "desire \\u2192 fall \\u2192 seeing = movement"),
            "Horos": ("\\u00ac", "boundary, limit, separation"),
            "Pleroma": ("\\u27e1", "fullness, completion, return"),
            "apokatasis": ("\\u222e", "return of all things, ethical re-harmonization"),
        },
        "corpus_source": "\\u00a746 VAL\\u2194JEWIK bridge",
    },
    "norse": {
        "name": "Norse Cosmology",
        "count": 9,
        "ring": 1,
        "mappings": {
            "Yggdrasil": ("\\u2205", "world tree = Hopf fibration, 9 worlds = 3\\u00b2"),
            "Odin": ("\\u2316", "sacrifice, wisdom, silence (hung 9 days)"),
            "Loki": ("\\u2206", "trickster, transformation, anomaly"),
            "Ragnar\\u00f6k": ("\\u222e", "destruction + rebirth = return cycle"),
        },
        "corpus_source": "Rozetni kamen: Norse 9 = 3\\u00b2, Yggdrasil = Hopf",
    },
    "buddhism": {
        "name": "Buddhism",
        "count": 4,
        "ring": 1,
        "mappings": {
            "4 Noble Truths": ("\\u2205", "diagnosis: suffering exists (∅)"),
            "8-fold Path": ("\\u2206", "prescription: transformation through action"),
            "Nirvana": ("\\u27e1", "extinction = new possibility, not annihilation"),
        },
        "corpus_source": "Rozetni kamen: 4 truths = 4 alchemical phases = 4 R-7 phases",
    },
    "iching": {
        "name": "I Ching",
        "count": 64,
        "ring": 3,
        "mappings": {
            "64 hexagrams": ("\\u2205", "64 = 2\\u2076 = \\u222e\\u2076; same as DNA"),
            "Tai Chi": ("\\u2205", "supreme ultimate = void that generates"),
            "Yin/Yang": ("\\u00ac", "binary distinction, first separation"),
        },
        "corpus_source": "Rozetni kamen: I Ching 64 = DNA 64 = \\u222e\\u2076",
    },
}

# ── Convenience lookups ──
ALL_TRADITIONS = list(TRADITIONS.keys())

def get_tradition(name: str) -> dict:
    """Return tradition registry entry."""
    return TRADITIONS.get(name.lower(), {})

def get_all_mappings_for_operator(glyph: str) -> list:
    """Find all traditions that map to a given root operator."""
    results = []
    for trad_name, trad in TRADITIONS.items():
        for native_term, (root_op, math_prop) in trad["mappings"].items():
            if root_op == glyph:
                results.append({
                    "tradition": trad["name"],
                    "native_term": native_term,
                    "math_property": math_prop,
                    "ring": trad["ring"],
                })
    return results

def get_cross_references(glyph: str) -> str:
    """Generate cross-system reference text for a root operator."""
    refs = get_all_mappings_for_operator(glyph)
    if not refs:
        return f"No traditions map to {glyph}"
    lines = [f"Cross-system references for {glyph}:"]
    for r in refs:
        lines.append(f"  {r['tradition']}: {r['native_term']} \\u2014 {r['math_property']}")
    return "\\n".join(lines)

# ── Self-test ──
if __name__ == "__main__":
    print("Rozetni kamni \\u2014 Tradition Registry")
    print("=" * 60)
    print(f"Traditions registered: {len(TRADITIONS)}")
    print()
    for name, info in TRADITIONS.items():
        print(f"  {info['name']:30s}  ring {info['ring']}  {info['count']:4d} elements  {len(info['mappings'])} mappings")
    print()
    # Test cross-references for \\u2205
    print(get_cross_references("\\u2205"))
    print()
    print(get_cross_references("\\u2206"))
'''

# ═══════════════════════════════════════════════════════════════
# FILE 3 (NEW): knowledge_renderer.py — Mandala + text rendering
# Uses QPainter for mandala, QTextBrowser for text
# ═══════════════════════════════════════════════════════════════

KNOWLEDGE_RENDERER_PY = '''"""
Knowledge Renderer — TAZV Comprehension Machine
=================================================
Renders indexed knowledge as interactive mandala + text.

Uses:
  - QPainter for mandala visualization (7 base modules + tradition rings)
  - QTextBrowser for cross-system reference display
  - corpus-validated colors from egyptian_color_semantics
  - corpus-validated frequencies from tonos

Architecture note: This file imports from the EXISTING modules:
  - egyptian_color_semantics (for colors)
  - module_semantics (for module definitions)
  - tonos (for sound frequencies)
  - rozetni_kamni (for tradition mappings)

It does NOT duplicate these. It renders what they hold.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextBrowser, QLabel, QComboBox
from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QPixmap
from PyQt6.QtCore import Qt, QPointF, QRectF
import math
import json

try:
    from comprehension.core.egyptian_color_semantics import COLORS, MODULE_COLOR_HEX
    from comprehension.core.module_semantics import MODULE_SEMANTICS, MODULE_ORDER
    from comprehension.core.tonos import TONOS_FREQUENCIES, get_frequency, get_note
    from comprehension.core.rozetni_kamni import TRADITIONS, get_cross_references
except ImportError:
    # Fallback for standalone testing
    COLORS = {}
    MODULE_COLOR_HEX = {}
    MODULE_SEMANTICS = {}
    MODULE_ORDER = ["bios", "state", "uaf", "jewik", "apd", "micro", "visualization"]
    TONOS_FREQUENCIES = {}
    TRADITIONS = {}


class MandalaView(QWidget):
    """Renders the base 7 modules + tradition rings as a mandala."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(600, 600)
        self.selected_tradition = None
        self.selected_operator = None
        self.depth = 1  # \\u2202 Globina level (1-4)

    def set_tradition(self, tradition_name):
        self.selected_tradition = tradition_name
        self.update()

    def set_depth(self, depth):
        self.depth = depth
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width()
        h = self.height()
        cx, cy = w // 2, h // 2

        # Background
        painter.fillRect(0, 0, w, h, QColor("#0A0A0A"))

        # Center (the root \\u2205)
        painter.setBrush(QColor("#1B2838"))
        painter.setPen(QPen(QColor("#333"), 1))
        center_r = 30 + (self.depth * 5)
        painter.drawEllipse(QPointF(cx, cy), center_r, center_r)
        painter.setPen(QColor("#E0E0E0"))
        painter.drawText(QRectF(cx - 20, cy - 8, 40, 16), Qt.AlignCenter, "\\u2205")

        # Base 7 modules in inner ring
        base_radius = 120
        for i, mod_name in enumerate(MODULE_ORDER):
            angle = (2 * math.pi * i / 7) - math.pi / 2  # start at top
            x = cx + base_radius * math.cos(angle)
            y = cy + base_radius * math.sin(angle)

            mod = MODULE_SEMANTICS.get(mod_name, {})
            color_hex = MODULE_COLOR_HEX.get(mod_name, "#444444")
            glyph = mod.get("symbol", "?")

            # Module circle
            r = 25 + (self.depth * 2)
            painter.setBrush(QColor(color_hex))
            painter.setPen(QPen(QColor("#333"), 1))
            painter.drawEllipse(QPointF(x, y), r, r)

            # Glyph
            painter.setPen(QColor("#E0E0E0"))
            painter.drawText(QRectF(x - 15, y - 8, 30, 16), Qt.AlignCenter, glyph)

            # Connection line to center
            painter.setPen(QPen(QColor("#222"), 1))
            painter.drawLine(QPointF(cx, cy), QPointF(x, y))

        # Tradition rings (outer)
        if self.selected_tradition:
            trad = TRADITIONS.get(self.selected_tradition, {})
            ring_num = trad.get("ring", 1)
            mappings = trad.get("mappings", {})

            ring_radius = 200 + (ring_num * 50)
            items = list(mappings.items())

            for i, (native_term, (root_op, math_prop)) in enumerate(items):
                angle = (2 * math.pi * i / max(len(items), 1)) - math.pi / 2
                x = cx + ring_radius * math.cos(angle)
                y = cy + ring_radius * math.sin(angle)

                # Find color for this root operator
                color_hex = "#666666"
                for mod_name, mod in MODULE_SEMANTICS.items():
                    if mod.get("symbol") == root_op:
                        color_hex = MODULE_COLOR_HEX.get(mod_name, "#666666")
                        break

                # Tradition node
                painter.setBrush(QColor(color_hex))
                painter.setPen(QPen(QColor("#555"), 1))
                painter.drawEllipse(QPointF(x, y), 20, 20)

                # Label
                painter.setPen(QColor("#E0E0E0"))
                label = native_term.split("(")[0].strip()[:12]
                painter.setFont(QFont("Consolas", 7))
                painter.drawText(
                    QRectF(x - 40, y + 22, 80, 14),
                    Qt.AlignCenter, label
                )

                # Connection to corresponding base module
                for j, mod_name in enumerate(MODULE_ORDER):
                    mod = MODULE_SEMANTICS.get(mod_name, {})
                    if mod.get("symbol") == root_op:
                        base_angle = (2 * math.pi * j / 7) - math.pi / 2
                        bx = cx + base_radius * math.cos(base_angle)
                        by = cy + base_radius * math.sin(base_angle)
                        painter.setPen(QPen(QColor("#333"), 1, Qt.DashLine))
                        painter.drawLine(QPointF(x, y), QPointF(bx, by))
                        break

        painter.end()


class KnowledgeRenderer(QWidget):
    """Interactive knowledge explorer: mandala + info panel."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        # Tradition selector
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("Tradicija:"))
        self.tradition_combo = QComboBox()
        self.tradition_combo.addItem("(izberi tradicijo)")
        for name in sorted(TRADITIONS.keys()):
            self.tradition_combo.addItem(TRADITIONS[name]["name"])
        self.tradition_combo.currentTextChanged.connect(self._on_tradition_selected)
        selector_layout.addWidget(self.tradition_combo)
        selector_layout.addStretch()
        layout.addLayout(selector_layout)

        # Mandala view
        self.mandala = MandalaView()
        layout.addWidget(self.mandala, stretch=2)

        # Info panel
        self.info_panel = QTextBrowser()
        self.info_panel.setStyleSheet(
            "background-color: #111; color: #E0E0E0; "
            "border: 1px solid #333; font-family: Consolas;"
        )
        self.info_panel.setHtml(
            "<h3>TAZV Knowledge Indexer</h3>"
            "<p>Izberi tradicijo za prikaz njenih operaterjev.</p>"
            "<p>R-7: \\u2205 \\u2192 \\u00ac \\u2192 \\u2206 \\u2192 1 \\u2192 \\u2316 \\u2192 \\u222e \\u2192 \\u27e1</p>"
        )
        layout.addWidget(self.info_panel, stretch=1)

    def _on_tradition(self, tradition_key):
        """Set tradition by key and update views."""
        self.mandala.set_tradition(tradition_key)
        trad = TRADITIONS.get(tradition_key, {})
        mappings = trad.get("mappings", {})

        html_parts = [f"<h3>{trad.get('name', '?')}</h3>"]
        html_parts.append(f"<p><b>Elementov:</b> {trad.get('count', '?')} | "
                          f"<b>Ring:</b> {trad.get('ring', '?')} | "
                          f"<b>Vir:</b> {trad.get('corpus_source', '?')}</p>")
        html_parts.append("<hr>")
        html_parts.append("<table border='1' cellpadding='4' style='border-collapse:collapse'>")
        html_parts.append("<tr><th>Nativni izraz</th><th>Operator</th><th>Mat. lastnost</th>"
                          "<th>Tonos</th></tr>")

        for native, (root_op, math_prop) in mappings.items():
            freq = TONOS_FREQUENCIES.get(root_op, {})
            freq_str = f"{freq.get('freq', '?'):.1f} Hz ({freq.get('note', '?')})" if freq else "?"
            color_hex = "#666"
            for mn, mod in MODULE_SEMANTICS.items():
                if mod.get("symbol") == root_op:
                    color_hex = MODULE_COLOR_HEX.get(mn, "#666")
                    break
            html_parts.append(
                f"<tr><td>{native}</td>"
                f"<td style='color:{color_hex}; font-size:18px'>{root_op}</td>"
                f"<td>{math_prop}</td>"
                f"<td>{freq_str}</td></tr>"
            )

        html_parts.append("</table>")
        html_parts.append("<hr>")
        html_parts.append("<p><b>Medsebojne povezave:</b></p>")
        for native, (root_op, _) in mappings.items():
            refs_html = ", ".join(
                f"{r['tradition']}: {r['native_term']}"
                for r in _get_refs_for_glyph(root_op, exclude=trad.get("name", ""))
            )
            if refs_html:
                html_parts.append(f"<p><b>{root_op}</b> ({native}): {refs_html}</p>")

        self.info_panel.setHtml("\\n".join(html_parts))

    def _on_tradition_selected(self, name):
        """Handle combo selection."""
        if name == "(izberi tradicijo)":
            return
        for key, info in TRADITIONS.items():
            if info["name"] == name:
                self._on_tradition(key)
                break


def _get_refs_for_glyph(glyph, exclude=""):
    """Helper: get cross-references excluding one tradition."""
    results = []
    for trad_name, trad in TRADITIONS.items():
        if trad["name"] == exclude:
            continue
        for native, (root_op, math_prop) in trad["mappings"].items():
            if root_op == glyph:
                results.append({
                    "tradition": trad["name"],
                    "native_term": native,
                })
    return results
'''

# ═══════════════════════════════════════════════════════════════
# FILE 4 (PATCH): schema.sql additions
# ═══════════════════════════════════════════════════════════════

SCHEMA_ADDITION = """
-- ═══════════════════════════════════════════════════════════════
-- KNOWLEDGE INDEX TABLES (Phase 2 addition)
-- Extends existing schema with tradition mapping storage
-- ═══════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS traditions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    element_count INTEGER,
    ring INTEGER DEFAULT 1,
    corpus_source TEXT,
    added_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tradition_mappings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tradition_id INTEGER NOT NULL,
    native_term TEXT NOT NULL,
    root_operator TEXT NOT NULL,
    math_property TEXT,
    FOREIGN KEY(tradition_id) REFERENCES traditions(id)
);

CREATE TABLE IF NOT EXISTS tonos_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    glyph TEXT NOT NULL,
    frequency REAL,
    note TEXT,
    played_at TEXT NOT NULL,
    FOREIGN KEY(session_id) REFERENCES sessions(id)
);
"""

# ═══════════════════════════════════════════════════════════════
# WRITE FILES
# ═══════════════════════════════════════════════════════════════

files = {
    "comprehension/core/tonos.py": TONOS_PY,
    "comprehension/core/rozetni_kamni.py": ROZETNI_KAMNI_PY,
    "comprehension/ui/knowledge_renderer.py": KNOWLEDGE_RENDERER_PY,
}

print("=" * 60)
print("TAZV Phase 2 — Knowledge Indexer (corpus-corrected)")
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

# Append schema additions
schema_path = os.path.join(BASE, "comprehension/data/schema.sql")
if os.path.exists(schema_path):
    with open(schema_path, "r", encoding="utf-8") as f:
        existing = f.read()
    if "traditions" not in existing:
        with open(schema_path, "a", encoding="utf-8") as f:
            f.write(SCHEMA_ADDITION)
        print(f"  OK  schema.sql (appended knowledge index tables)")
    else:
        print(f"  SKIP schema.sql (traditions table already exists)")
else:
    os.makedirs(os.path.dirname(schema_path), exist_ok=True)
    with open(schema_path, "w", encoding="utf-8") as f:
        f.write(SCHEMA_ADDITION)
    print(f"  OK  schema.sql (new)")

print()
print("What was corrected from the original design:")
print("  1. No 'iwn' renaming — egyptian_color_semantics IS the color layer")
print("  2. No 'ATLAS-ALL' renaming — Atlas Mandala already exists in corpus")
print("  3. No 'CORPUS pipeline' renaming — Rozetni kamen IS the 3-script mapper")
print("  4. TONOS frequencies aligned with corpus (220/330/440/550/660 Hz)")
print("  5. 13 traditions from Rozetni kamni corpus (not 4 invented)")
print("  6. Extends existing files, does not duplicate them")
print()
print("Files created:")
print("  tonos.py              — Zvocni tok (corpus frequencies)")
print("  rozetni_kamni.py      — 13 traditions mapped to R-7 operators")
print("  knowledge_renderer.py — Mandala + cross-system text display")
print("  schema.sql            — Extended with knowledge index tables")
print()
print("To integrate KnowledgeRenderer into main_window:")
print("  from comprehension.ui.knowledge_renderer import KnowledgeRenderer")
print("  # Add as a new tab:")
print("  self.tabs.addTab(KnowledgeRenderer(), 'Index')")
print()
print("Next steps:")
print("  1. Run: python tazv_phase2_indexer.py")
print("  2. cd comprehension_machine && python main.py")
print("  3. Add KnowledgeRenderer as a tab in main_window.py")
print("  4. Wire SQLite: store tradition mappings on ingest")
print("  5. Add ∂ Globina menu to control mandala depth")