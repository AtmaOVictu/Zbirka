# TAZV Comprehension Layer — Rebuilt

The old version treated words as self-sufficient nodes on a line. That was the mess. This version is built on the **SO-OBSTAJANJE Protocol** — every word is a relation-event carrying its antinom, its internal division, and its resistance field. Nothing stands alone.

---

## The SO-OBSTAJANJE Protocol

Distilled from the corpus. Every line of code in this layer must obey these.

```
SO-OBSTAJANJE PROTOCOL — Co-existence Protocol
═══════════════════════════════════════════════

P1  No word stands alone.
    A word is a relation-event, not an entity.
    Isolation = unreality. "A word is nothing without a world —
    it is UNREAL. And unreality is worse than silence."

P2  Every word carries its antinom.
    Assertion and negation co-exist WITHIN the word,
    not between words. They don't alternate — they co-occur.
    "Word negates itself" AND "Word confirms itself." Both. Always.
    "One A is impossible" AND "One A is possible." Both. Always.

P3  Every word has an internal division:
    what divides / what gets divided.
    The word IS this division, not a container for it.
    "þ touches ə and singles out" — THE is the event of touching-
    the-field, not a box labeled δ.

P4  Relation is primary. Words emerge from relations,
    not the other way around.
    The primitive unit is the relation-event, not the node.
    "Storage Primitive = Relation. Operational Primitive = Difference."

P5  A word requires a world to push back.
    Without resistance, the word is unreal.
    "No material → no cut. No cut → no articulation."
    The "world" for a statement = the other words in it.

P6  The line is surface. Linear reading order is not
    ontological structure. The topology of meaning is non-linear:
    it radiates, folds, and co-exists.
    "The linearity of language is what we have to break first."

P7  ∅ and 1 are in so-obstajanje. They don't alternate in phases.
    Every 1 carries the possibility of 0, and vice versa.
    R-7 phases CO-EXIST within each word, they don't sequence.
    "Absolute without antinomy is death of language."

═══════════════════════════════════════════════
```

---

## File 1: `comprehension/core/decomposer.py`

```python
"""
Decomposer — TAZV Comprehension Machine
========================================
SO-OBSTAJANJE Protocol: every word is a relation-event.

A word is NOT a node on a line. A word is:
  - an internal division (what divides / what gets divided)
  - an antinom (the counter-statement, always already present)
  - a resistance field (the other words it must push against)
  - co-existing R-7 phases (not one phase — multiple, simultaneously)

Source: WOR(L)D English Ontological Lexicon (26 terms)
        Beseda je Ne — Critical Retro Edition (antinom pairs)
        JEWIK Core axioms (JEWIK_001-006)

R-7: ∅ → ¬ → ∆ → 1 → ⧖ → ∮ → ⟡  (display-only — phases CO-EXIST, not sequence)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Set
import re


# ── R-7 symbol → phase (display-only; phases co-exist per P7) ──
SYMBOL_PHASE: Dict[str, int] = {
    '∅': 0, '¬': 1, 'Δ': 2, '⊢': 3, '⧖': 4, '∮': 5, '⟡': 6,
    'δ': 1, '∴': 2, '||': 5, '∥': 5, 'ʃ': 4, '⊥': 0,
    '∂': 6, 'ð': 6, 'W': 3, '⊘': 0, '∫': 4,
    '⊘Δ': 2, '¬∴': 2,
}


@dataclass
class RelationEvent:
    """
    A word is not a node. A word is a relation-event.

    Per SO-OBSTAJANJE Protocol:
      P3: internal division (divider / divided)
      P2: antinom (counter-statement, always already present)
      P5: resistance (other events it pushes against)
      P7: co-existing phases (not one phase — multiple)
    """
    word: str
    surface_position: int           # where it sits on the surface line (display only, P6)

    # P3: Internal division — the word IS this division
    divider: str                    # what divides (the active face — consonants, stops, cuts)
    divided: str                    # what gets divided (the receptive face — vowels, resonance, flow)
    symbol: str                     # the ontological operator (display-only label for the division)
    role: str                       # what the division DOES

    # P2: Antinom — always already present, not added later
    antinom_word: str               # the counter-word
    antinom_symbol: str             # the counter-operator
    antinom_note: str               # why these co-exist in tension

    # P7: Co-existing phases — not one phase, but the phases present simultaneously
    co_phases: List[int]            # [phase of symbol, phase of antinom] — both always present

    # P5: Resistance — what this event pushes against (filled by RelationField)
    resistance_targets: List[str] = field(default_factory=list)  # surface_positions of pushing-back events

    mapped: bool                    # True if found in decomposition table

    def __repr__(self) -> str:
        antinom = f' ↔ {self.antinom_word}({self.antinom_symbol})' if self.antinom_word else ''
        return f'Event({self.word}→{self.symbol or "?"}{antinom} phases={self.co_phases})'


# ── The decomposition table (26 terms, corpus-validated) ──
# Each entry now carries: divider, divided, antinom data
# Source: WOR(L)D lexicon + Critical Retro Edition antinom pairs
DECOMPOSITION_TABLE: Dict[str, Dict] = {
    'THE': {
        'divider': 'ð', 'divided': 'ə',
        'symbol': 'δ',
        'role': 'The operator that singles out — carries one ripple from the field into presence',
        'antinom_word': '(unmarked field)', 'antinom_symbol': '∅',
        'antinom_note': 'singling out ↔ letting be — THE chooses, its antinom is the field it chose FROM',
    },
    'WORD': {
        'divider': 'w+d', 'divided': 'ɜːr',
        'symbol': '⊢',
        'role': 'The act of cutting being into form — proof that something is',
        'antinom_word': 'SILENCE', 'antinom_symbol': '⧖',
        'antinom_note': 'utterance ↔ silence — "Word is Not" AND "Word is Yes"',
    },
    'WOR(L)D': {
        'divider': 'w+d', 'divided': 'a:r',
        'symbol': '⊢',
        'role': 'The act of cutting being into form — the (L) keeps the word flowing',
        'antinom_word': 'SILENCE', 'antinom_symbol': '⧖',
        'antinom_note': 'utterance ↔ silence — the (L) flows, its antinom is the stop',
    },
    'IS': {
        'divider': '1', 'divided': 'z',
        'symbol': 'Δ',
        'role': 'The hum of continuing-to-be — activation that sustains',
        'antinom_word': 'NOT', 'antinom_symbol': '¬',
        'antinom_note': 'being ↔ non-being — "IS" AND "IS NOT" co-exist',
    },
    'NO': {
        'divider': 'n', 'divided': 'ou',
        'symbol': '∅',
        'role': 'The ne-operator — the passage between inward and outward; condition of the next YES',
        'antinom_word': 'YES', 'antinom_symbol': 'Δ',
        'antinom_note': 'negation ↔ affirmation — NO is the condition of YES, not its absence',
    },
    'NOT': {
        'divider': 'n+t', 'divided': 'o',
        'symbol': '¬',
        'role': 'The act of cutting open — separation-as-distinction — the cut that opens',
        'antinom_word': 'IS', 'antinom_symbol': 'Δ',
        'antinom_note': 'non-being ↔ being — NOT carries IS as its antinom',
    },
    'MEANING': {
        'divider': 'm+n+1+η', 'divided': 'i:',
        'symbol': '∴',
        'role': 'The act of reaching-toward returning into body — relation established',
        'antinom_word': 'EMPTINESS', 'antinom_symbol': '∅',
        'antinom_note': 'meaning ↔ emptiness — "One word could embrace everything – if it were emptiness"',
    },
    'MEAN(L)ING': {
        'divider': 'm+n+1+η', 'divided': 'i:',
        'symbol': '∴',
        'role': 'The act of reaching-toward returning into body — relation established',
        'antinom_word': 'EMPTINESS', 'antinom_symbol': '∅',
        'antinom_note': 'meaning ↔ emptiness — the (L) sustains, its antinom is the void',
    },
    'CUT': {
        'divider': 'k+t', 'divided': 'λ',
        'symbol': 'δ',
        'role': 'The rez that makes difference visible — condition of clarity',
        'antinom_word': 'FLOW', 'antinom_symbol': '∫',
        'antinom_note': 'separation ↔ continuity — the cut AND the L that flows through it',
    },
    'MIND': {
        'divider': 'm+n+d', 'divided': 'æt',
        'symbol': '||',
        'role': 'The spiral: reach-and-return that composes sense from pressure',
        'antinom_word': 'BODY', 'antinom_symbol': '⊥',
        'antinom_note': 'spiral ↔ ground — mind composes, body bears',
    },
    'M(L)IND': {
        'divider': 'm+n+d', 'divided': 'æt',
        'symbol': '||',
        'role': 'The spiral: reach-and-return that composes sense from pressure',
        'antinom_word': 'BODY', 'antinom_symbol': '⊥',
        'antinom_note': 'spiral ↔ ground — the (L) flows, body grounds',
    },
    'FROM': {
        'divider': 'f+m', 'divided': 'r+o',
        'symbol': 'δ',
        'role': 'Origin-as-departure — the passage that carries its starting point forward',
        'antinom_word': 'TO', 'antinom_symbol': '∴',
        'antinom_note': 'departure ↔ arrival — FROM carries TO as its antinom',
    },
    'TO': {
        'divider': 't', 'divided': 'u:',
        'symbol': '∴',
        'role': 'Directed relation — the arrow that establishes the path',
        'antinom_word': 'FROM', 'antinom_symbol': 'δ',
        'antinom_note': 'arrival ↔ departure — TO carries FROM as its antinom',
    },
    'CREATE': {
        'divider': 'kr+t', 'divided': 'i+ei',
        'symbol': 'Δ',
        'role': 'Transformation that responds to necessity — the act that brings forth from pressure',
        'antinom_word': 'DISSOLVE', 'antinom_symbol': '∮',
        'antinom_note': 'bringing forth ↔ returning — CREATE carries DISSOLVE as its antinom',
    },
    'THOUGHT': {
        'divider': 'θ+t', 'divided': 'o:',
        'symbol': '||',
        'role': 'The echo that connects states — response-operator resonating to pressure',
        'antinom_word': 'SILENCE', 'antinom_symbol': '⧖',
        'antinom_note': 'echo ↔ stillness — thought resonates, silence listens',
    },
    'REFLECTION': {
        'divider': 'r+k+∫+an', 'divided': '1+fle',
        'symbol': '∅',
        'role': 'The folding-back that differs — repetition-as-difference',
        'antinom_word': 'PRESENCE', 'antinom_symbol': '∫',
        'antinom_note': 'folding back ↔ immediate — reflection carries direct presence as antinom',
    },
    'NECESSARY': {
        'divider': 'ne+ri', 'divided': 'sə+sə',
        'symbol': '⊘Δ',
        'role': 'The ne that must-be — internal pressure making transition unavoidable',
        'antinom_word': 'CONTINGENT', 'antinom_symbol': '∴',
        'antinom_note': 'must-be ↔ might-not-be — necessity carries contingency',
    },
    'INVENTION': {
        'divider': 'ɪn+t', 'divided': 'ven+ʃ+ən',
        'symbol': 'Δ',
        'role': 'The act that brings forth from necessity — response to pressure that demands voice',
        'antinom_word': 'DISCOVERY', 'antinom_symbol': '⊢',
        'antinom_note': 'making ↔ finding — invention carries discovery as antinom',
    },
    'CHARACTER': {
        'divider': 'k+k+t', 'divided': 'æ+r+ə+ə',
        'symbol': '∥',
        'role': 'The seal through duration — what stands through the double test',
        'antinom_word': 'CHANGE', 'antinom_symbol': 'Δ',
        'antinom_note': 'duration ↔ transformation — character carries change as antinom',
    },
    'TIME': {
        'divider': 't+m', 'divided': 'aɪ',
        'symbol': '∥',
        'role': 'The pulse of meaning — time as the body-hum that holds the cut',
        'antinom_word': 'TIMELESS', 'antinom_symbol': '⧖',
        'antinom_note': 'pulse ↔ eternal — time carries timelessness as antinom',
    },
    'T(L)IME': {
        'divider': 't+m', 'divided': 'aɪ',
        'symbol': '∥',
        'role': 'The pulse of meaning — the (L) holds the cut in flow',
        'antinom_word': 'TIMELESS', 'antinom_symbol': '⧖',
        'antinom_note': 'pulse ↔ eternal — the (L) flows through time, timelessness is its antinom',
    },
    'DOUBT': {
        'divider': 'd+t', 'divided': 'au',
        'symbol': '¬∴',
        'role': 'The condition of consciousness — the double-cut that opens truth',
        'antinom_word': 'FAITH', 'antinom_symbol': 'ʃ',
        'antinom_note': 'double-cut ↔ persistence — doubt carries faith as antinom',
    },
    'TRUTH': {
        'divider': 't+θ', 'divided': 'r+u:',
        'symbol': '∴',
        'role': 'The path lived — process, the living path; presses, dissects, cuts through',
        'antinom_word': 'LIE', 'antinom_symbol': '¬',
        'antinom_note': 'truth ↔ lie — "Truth is a lie" AND "Truth is not a lie" — both, always',
    },
    'FAITH': {
        'divider': 'f+θ', 'divided': 'eɪ',
        'symbol': 'ʃ',
        'role': 'Persistence that holds the open question — presence sustained through friction',
        'antinom_word': 'DOUBT', 'antinom_symbol': '¬∴',
        'antinom_note': 'persistence ↔ double-cut — faith carries doubt as antinom',
    },
    'FA(L)TH': {
        'divider': 'f+θ', 'divided': 'eɪ',
        'symbol': 'ʃ',
        'role': 'Persistence that holds the open question — the (L) sustains through friction',
        'antinom_word': 'DOUBT', 'antinom_symbol': '¬∴',
        'antinom_note': 'persistence ↔ double-cut — the (L) flows, doubt cuts',
    },
    'WILL': {
        'divider': 'w+l', 'divided': 'ɪ',
        'symbol': 'W',
        'role': 'The wanting that transforms through presence into address',
        'antinom_word': 'SURRENDER', 'antinom_symbol': '∮',
        'antinom_note': 'wanting ↔ letting go — will carries surrender as antinom',
    },
    'W(L)LL': {
        'divider': 'w+l', 'divided': 'ɪ',
        'symbol': 'W',
        'role': 'The wanting that transforms through presence — the (L) flows into address',
        'antinom_word': 'SURRENDER', 'antinom_symbol': '∮',
        'antinom_note': 'wanting ↔ letting go — the (L) flows, surrender returns',
    },
    'BODY': {
        'divider': 'b+d', 'divided': 'b+i',
        'symbol': '⊥',
        'role': 'The bearer — what exists before the question; the ground that allows error',
        'antinom_word': 'VOID', 'antinom_symbol': '∅',
        'antinom_note': 'bearer ↔ absence — body carries void as antinom',
    },
    'SOUL': {
        'divider': 's+l', 'divided': 'ou',
        'symbol': 'ʃ',
        'role': 'The breath-stream that opens into totality and keeps flowing — presence carrying',
        'antinom_word': 'MATTER', 'antinom_symbol': '⊥',
        'antinom_note': 'flow ↔ ground — soul carries matter as antinom',
    },
    'SPIRIT': {
        'divider': 's+p+ɪ+t', 'divided': 'r+ɪ',
        'symbol': '∥',
        'role': 'The fire of axiomatic force — the power that breaks through and returns',
        'antinom_word': 'FLESH', 'antinom_symbol': '⊥',
        'antinom_note': 'fire ↔ body — spirit carries flesh as antinom',
    },
    'SP(L)RIT': {
        'divider': 's+p+ɪ+t', 'divided': 'r+ɪ',
        'symbol': '∥',
        'role': 'The fire of axiomatic force — the (L) breaks through and returns',
        'antinom_word': 'FLESH', 'antinom_symbol': '⊥',
        'antinom_note': 'fire ↔ body — the (L) flows through fire, flesh grounds',
    },
    'EGO': {
        'divider': 'i:+g', 'divided': 'ou',
        'symbol': '⊘',
        'role': 'The boundary, the membrane, the cut — the part bearing the whole',
        'antinom_word': 'SELF-OTHER', 'antinom_symbol': '∂',
        'antinom_note': 'boundary ↔ passage — ego carries self-other as antinom',
    },
    'SELF': {
        'divider': 's+f', 'divided': 'ɛ+l',
        'symbol': '∂',
        'role': 'The passage itself — the observer of transitions',
        'antinom_word': 'OTHER', 'antinom_symbol': '⊘',
        'antinom_note': 'observer ↔ observed — self carries other as antinom',
    },
    'BEING': {
        'divider': 'b+ŋ', 'divided': 'i:+ɪ',
        'symbol': '∫',
        'role': 'The sustained act — presence that sustains itself by returning into the body',
        'antinom_word': 'NOTHING', 'antinom_symbol': '∅',
        'antinom_note': 'sustaining ↔ absenting — being carries nothing as antinom',
    },
    'NOTHING': {
        'divider': 'n+ŋ', 'divided': 'ʌ+θ+ɪ',
        'symbol': '∅',
        'role': 'The inward turn through friction back into body — absence that prepares',
        'antinom_word': 'BEING', 'antinom_symbol': '∫',
        'antinom_note': 'absenting ↔ sustaining — nothing carries being as antinom',
    },
    'GOD': {
        'divider': 'g+d', 'divided': 'ɒ',
        'symbol': '∮',
        'role': 'The spiral totality that returns — keeps the question open',
        'antinom_word': 'NOT-GOD', 'antinom_symbol': '¬',
        'antinom_note': 'word ↔ more-than-word — "God is only a word" AND "God is more than a word"',
    },
    'SILENCE': {
        'divider': 's+əns', 'divided': 'aɪ+l',
        'symbol': '⧖',
        'role': 'Tiheon — the sacred silence that is full of listening; the body becomes ear',
        'antinom_word': 'WORD', 'antinom_symbol': '⊢',
        'antinom_note': 'listening ↔ utterance — silence carries word as antinom',
    },
}

# ── Slovenian equivalents (bidirectional) ──
SLOVENIAN_MAP: Dict[str, str] = {
    'BESEDA': 'WORD', 'NE': 'NO', 'NI': 'NOT', 'POMEN': 'MEANING',
    'REZ': 'CUT', 'UM': 'MIND', 'IZ': 'FROM', 'V': 'TO',
    'USTVARJAJ': 'CREATE', 'MISEL': 'THOUGHT', 'ZRCALO': 'REFLECTION',
    'NUJNO': 'NECESSARY', 'IZUM': 'INVENTION', 'ZNANJE': 'CHARACTER',
    'CAS': 'TIME', 'DVOM': 'DOUBT', 'RESNICA': 'TRUTH', 'VERA': 'FAITH',
    'VOLJA': 'WILL', 'TELO': 'BODY', 'DUSA': 'SOUL', 'DUH': 'SPIRIT',
    'JAZ': 'EGO', 'SE': 'SELF', 'BITI': 'BEING', 'NIC': 'NOTHING',
    'BOG': 'GOD', 'TISINA': 'SILENCE',
}


def _normalize(token: str) -> str:
    cleaned = re.sub(r'^[^A-Za-z(]+|[^A-Za-z)]+$', '', token)
    return cleaned.upper()


def _try_lookup(word: str) -> Optional[Dict]:
    upper = word.upper()
    if upper in DECOMPOSITION_TABLE:
        return DECOMPOSITION_TABLE[upper]
    # Try with (L) inserted
    for suffix_len in [2, 3, 4]:
        if len(upper) > suffix_len + 1:
            insert_pos = len(upper) - suffix_len
            if upper[insert_pos] == 'L':
                variant = upper[:insert_pos] + '(L)' + upper[insert_pos + 1:]
                if variant in DECOMPOSITION_TABLE:
                    return DECOMPOSITION_TABLE[variant]
    # Try without (L)
    stripped = upper.replace('(L)', 'L')
    if stripped in DECOMPOSITION_TABLE:
        return DECOMPOSITION_TABLE[stripped]
    return None


def _compute_co_phases(symbol: str, antinom_symbol: str) -> List[int]:
    """
    P7: co-existing phases. Not one phase — the phases present simultaneously.
    Every event carries at minimum: its own phase AND its antinom's phase.
    """
    phases: Set[int] = set()
    if symbol in SYMBOL_PHASE:
        phases.add(SYMBOL_PHASE[symbol])
    if antinom_symbol in SYMBOL_PHASE:
        phases.add(SYMBOL_PHASE[antinom_symbol])
    return sorted(phases) if phases else []


def decompose_statement(text: str) -> List[RelationEvent]:
    """
    Decompose a statement into relation-events.

    "All words are points. The lines are the logic that follows."
    But the points are NOT on a line — they co-exist (P6).

    Each event carries:
      - its internal division (P3)
      - its antinom (P2)
      - its co-existing phases (P7)
    Resistance (P5) is filled later by RelationField.
    """
    if not text or not text.strip():
        return []

    raw_tokens = text.strip().split()
    events: List[RelationEvent] = []

    for i, token in enumerate(raw_tokens):
        normalized = _normalize(token)
        entry = _try_lookup(normalized)

        # Try Slovenian → English
        if entry is None and normalized in SLOVENIAN_MAP:
            entry = _try_lookup(SLOVENIAN_MAP[normalized])

        if entry is not None:
            symbol = entry['symbol']
            antinom_sym = entry['antinom_symbol']
            events.append(RelationEvent(
                word=token,
                surface_position=i,
                divider=entry['divider'],
                divided=entry['divided'],
                symbol=symbol,
                role=entry['role'],
                antinom_word=entry['antinom_word'],
                antinom_symbol=antinom_sym,
                antinom_note=entry['antinom_note'],
                co_phases=_compute_co_phases(symbol, antinom_sym),
                mapped=True,
            ))
        else:
            events.append(RelationEvent(
                word=token,
                surface_position=i,
                divider='',
                divided='',
                symbol='',
                role='UNMAPPED — no ontological operator found',
                antinom_word='',
                antinom_symbol='',
                antinom_note='',
                co_phases=[],
                mapped=False,
            ))

    return events


def get_symbol_sequence(events: List[RelationEvent]) -> str:
    """Display-only: the surface symbol string (P6: this is the line, not the topology)."""
    return ''.join(e.symbol for e in events if e.mapped)


def get_antinom_sequence(events: List[RelationEvent]) -> str:
    """The antinom string — what co-exists beneath the surface (P2)."""
    return ''.join(e.antinom_symbol for e in events if e.mapped)


def get_mapped_ratio(events: List[RelationEvent]) -> float:
    if not events:
        return 0.0
    return sum(1 for e in events if e.mapped) / len(events)
```

---

## File 2: `comprehension/core/graph_store.py`

```python
"""
Relation Field — TAZV Comprehension Machine
=============================================
SO-OBSTAJANJE Protocol: relation is primary (P4).

Not a graph of nodes and edges. A FIELD of relation-events.
Words emerge from relations, not the other way around.

"Storage Primitive = Relation. Operational Primitive = Difference."

What changed from the old version:
  OLD: GraphNode (standalone) → GraphEdge (connects nodes)
  NEW: RelationEvent (primary) → Resonance (co-existence between events)

  OLD: nodes are added first, edges second
  NEW: events ARE the field; resonances are how they co-exist

  OLD: promote_relation_to_node (hypergraph workaround)
  NEW: relations are already the primary unit — no promotion needed

Relation types from JEWIK Truthbase Studio:
  SUPPORTS, CONTRADICTS, DEFINES, REFINES, TESTS, SYMBOLICALLY_LINKED
Archive types: direct, semantic, compositional, derived, custom
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Set, Tuple
from enum import Enum
import uuid


class RelationType(str, Enum):
    SUPPORTS = 'SUPPORTS'
    CONTRADICTS = 'CONTRADICTS'
    DEFINES = 'DEFINES'
    REFINES = 'REFINES'
    TESTS = 'TESTS'
    SYMBOLICALLY_LINKED = 'SYMBOLICALLY_LINKED'
    DIRECT = 'direct'
    SEMANTIC = 'semantic'
    COMPOSITIONAL = 'compositional'
    DERIVED = 'derived'
    CUSTOM = 'custom'


RELATION_TYPE_LABELS: Dict[str, str] = {
    'SUPPORTS': 'podpira', 'CONTRADICTS': 'protislovje',
    'DEFINES': 'definira', 'REFINES': 'izboljša',
    'TESTS': 'preverja', 'SYMBOLICALLY_LINKED': 'simbolno povezano',
    'direct': 'neposredno', 'semantic': 'semantično',
    'compositional': 'sestavljeno', 'derived': 'izvedeno', 'custom': 'po meri',
}


class Severity(str, Enum):
    NIZKA = 'nizka'
    SREDNJA = 'srednja'
    VISOKA = 'visoka'


@dataclass
class Resonance:
    """
    Not an edge between two nodes. A resonance between two events.

    P4: relation is primary. This IS the primary unit.
    The events it connects are its faces, not its endpoints.
    """
    id: str
    event_a_pos: int              # surface position of event A (display only)
    event_b_pos: int              # surface position of event B (display only)
    resonance_type: RelationType
    note: str = ''
    confidence: float = 0.5
    # P2: the resonance carries its own antinom
    antinom_note: str = ''        # what the counter-resonance would be

    def __repr__(self) -> str:
        return f'Resonance(p{self.event_a_pos} --{self.resonance_type.value}--> p{self.event_b_pos})'


@dataclass
class ContentionMark:
    """
    A mark revealing WHERE antinomy lives.

    Per P2: contention is always already present (every event carries its antinom).
    This mark doesn't discover contention — it REVEALS it.
    """
    event_position: int           # which event
    severity: Severity
    description: str               # what the internal antinom is doing
    antinom_pair: str             # the co-existing pair (e.g. "∅ ↔ Δ")


class RelationField:
    """
    A field of relation-events and their resonances.

    P4: relation is primary. Events don't stand alone — they exist
    only in the field, pushing against each other (P5).

    The "graph" is not nodes + edges. It's events + resonances.
    Contention is not found BETWEEN events — it's revealed WITHIN them (P2).
    """

    def __init__(self) -> None:
        # P4: events are the field, not nodes in a graph
        self._events: Dict[int, object] = {}  # position → RelationEvent (imported from decomposer)
        self._resonances: List[Resonance] = []
        self._contentions: List[ContentionMark] = []
        # P5: resistance — which events push against which
        self._resistance_map: Dict[int, List[int]] = {}

    # ── Event operations ──

    def add_event(self, event) -> None:
        """Add a relation-event to the field. P1: no event stands alone —
        it exists only in relation to the other events in the field."""
        self._events[event.surface_position] = event

    def get_event(self, position: int) -> Optional[object]:
        return self._events.get(position)

    def get_all_events(self) -> List[object]:
        return [self._events[pos] for pos in sorted(self._events)]

    def get_mapped_events(self) -> List[object]:
        return [e for e in self.get_all_events() if e.mapped]

    # ── Resonance operations (P4: relation is primary) ──

    def add_resonance(
        self,
        event_a_pos: int,
        event_b_pos: int,
        resonance_type: RelationType,
        note: str = '',
        confidence: float = 0.5,
        antinom_note: str = '',
    ) -> Optional[Resonance]:
        """Add a resonance between two events. P4: this is the primary operation."""
        if event_a_pos not in self._events or event_b_pos not in self._events:
            return None

        resonance = Resonance(
            id=str(uuid.uuid4()),
            event_a_pos=event_a_pos,
            event_b_pos=event_b_pos,
            resonance_type=resonance_type,
            note=note,
            confidence=confidence,
            antinom_note=antinom_note,
        )
        self._resonances.append(resonance)
        return resonance

    def get_resonances_for_event(self, position: int) -> List[Resonance]:
        """Get all resonances involving an event."""
        return [r for r in self._resonances
                if r.event_a_pos == position or r.event_b_pos == position]

    def get_resonances_by_type(self, rtype: RelationType) -> List[Resonance]:
        return [r for r in self._resonances if r.resonance_type == rtype]

    def get_all_resonances(self) -> List[Resonance]:
        return list(self._resonances)

    # ── P5: Resistance — the world that pushes back ──

    def compute_resistance(self) -> None:
        """
        P5: "A word requires a world to push back."
        For each event, find which other events create resistance.

        Resistance = events whose symbol or antinom symbol
        is in tension with this event's symbol or antinom.
        """
        events = self.get_mapped_events()
        for event in events:
            targets: List[int] = []
            for other in events:
                if event.surface_position == other.surface_position:
                    continue
                # Check if there's symbol tension
                if _symbols_in_tension(event.symbol, other.symbol):
                    targets.append(other.surface_position)
                elif _symbols_in_tension(event.antinom_symbol, other.symbol):
                    targets.append(other.surface_position)
                elif _symbols_in_tension(event.symbol, other.antinom_symbol):
                    targets.append(other.surface_position)
            event.resistance_targets = targets
            self._resistance_map[event.surface_position] = targets

    # ── Contention (P2: revealed, not discovered) ──

    def reveal_contention(
        self,
        event_position: int,
        severity: Severity,
        description: str,
        antinom_pair: str,
    ) -> ContentionMark:
        """Reveal the antinom already present in an event. P2."""
        mark = ContentionMark(
            event_position=event_position,
            severity=severity,
            description=description,
            antinom_pair=antinom_pair,
        )
        self._contentions.append(mark)
        return mark

    def get_contentions(self) -> List[ContentionMark]:
        return list(self._contentions)

    def get_contentions_for_event(self, position: int) -> List[ContentionMark]:
        return [c for c in self._contentions if c.event_position == position]

    # ── Resonance queries (non-linear — P6) ──

    def find_resonance_path(
        self,
        start_pos: int,
        end_pos: int,
        max_depth: int = 10,
    ) -> List[int]:
        """BFS through resonances (NOT through surface order). P6: the line is surface."""
        if start_pos == end_pos:
            return [start_pos]
        if start_pos not in self._events or end_pos not in self._events:
            return []

        visited: Set[int] = {start_pos}
        queue: List[Tuple[int, List[int]]] = [(start_pos, [start_pos])]

        while queue:
            current, path = queue.pop(0)
            if len(path) >= max_depth:
                continue
            for res in self.get_resonances_for_event(current):
                other = res.event_b_pos if res.event_a_pos == current else res.event_a_pos
                if other == end_pos:
                    return path + [other]
                if other not in visited:
                    visited.add(other)
                    queue.append((other, path + [other]))
        return []

    # ── Build from decomposer output ──

    def build_from_events(self, events: List) -> None:
        """Build the field from decomposer RelationEvent output."""
        for event in events:
            self.add_event(event)

        # P5: compute resistance
        self.compute_resistance()

        # Create resonances between events that push against each other
        for event in self.get_mapped_events():
            for target_pos in event.resistance_targets:
                target = self.get_event(target_pos)
                if target and target.surface_position > event.surface_position:
                    # Determine resonance type from the tension
                    rtype = _determine_resonance_type(event, target)
                    self.add_resonance(
                        event_a_pos=event.surface_position,
                        event_b_pos=target_pos,
                        resonance_type=rtype,
                        note=f'{event.word}({event.symbol}) ↔ {target.word}({target.symbol})',
                        confidence=0.7,
                        antinom_note=f'co-existing: {event.antinom_word} ↔ {target.antinom_word}',
                    )

        # Also create compositional resonances between adjacent mapped events
        # (surface adjacency — but this is display order, P6)
        mapped = self.get_mapped_events()
        for i in range(len(mapped) - 1):
            a, b = mapped[i], mapped[i + 1]
            existing = [r for r in self.get_resonances_for_event(a.surface_position)
                        if r.event_b_pos == b.surface_position]
            if not existing:
                self.add_resonance(
                    event_a_pos=a.surface_position,
                    event_b_pos=b.surface_position,
                    resonance_type=RelationType.COMPOSITIONAL,
                    note=f'{a.word} → {b.word} (surface adjacency)',
                    confidence=0.4,
                    antinom_note=f'surface: {a.antinom_word} → {b.antinom_word}',
                )

    # ── Serialization ──

    def to_dict(self) -> Dict:
        return {
            'events': [
                {
                    'word': e.word, 'position': e.surface_position,
                    'symbol': e.symbol, 'divider': e.divider, 'divided': e.divided,
                    'antinom_word': e.antinom_word, 'antinom_symbol': e.antinom_symbol,
                    'antinom_note': e.antinom_note,
                    'co_phases': e.co_phases,
                    'resistance_targets': e.resistance_targets,
                    'mapped': e.mapped,
                }
                for e in self.get_all_events()
            ],
            'resonances': [
                {
                    'a': r.event_a_pos, 'b': r.event_b_pos,
                    'type': r.resonance_type.value, 'note': r.note,
                    'confidence': r.confidence, 'antinom_note': r.antinom_note,
                }
                for r in self._resonances
            ],
            'contentions': [
                {
                    'event': c.event_position, 'severity': c.severity.value,
                    'description': c.description, 'antinom_pair': c.antinom_pair,
                }
                for c in self._contentions
            ],
            'stats': {
                'event_count': len(self._events),
                'resonance_count': len(self._resonances),
                'contention_count': len(self._contentions),
            },
        }


# ── Symbol tension detection (P2: antinomy is always already present) ──
SYMBOL_OPPOSITIONS: List[Tuple[str, str, str]] = [
    ('∅', 'Δ', 'stasis vs movement — void confronts change'),
    ('¬', '∴', 'separation vs relation — cut confronts connection'),
    ('⊢', '∅', 'assertion vs negation — proof confronts void'),
    ('∫', '¬', 'sustaining vs separating — presence confronts cut'),
    ('⊥', '∴', 'ground vs relation — bearer confronts connection'),
    ('∅', '⊢', 'void vs proof — negation confronts assertion'),
    ('Δ', '¬', 'movement vs stasis — change confronts cut'),
    ('∅', '1', 'void vs seal — negation confronts the sealed act'),
    ('δ', '∫', 'passage vs presence — cut confronts sustaining'),
    ('⧖', '⊢', 'silence vs proof — listening confronts assertion'),
]


def _symbols_in_tension(sym_a: str, sym_b: str) -> bool:
    if not sym_a or not sym_b:
        return False
    for a, b, _ in SYMBOL_OPPOSITIONS:
        if (sym_a == a and sym_b == b) or (sym_a == b and sym_b == a):
            return True
    return False


def _determine_resonance_type(event_a, event_b) -> RelationType:
    """Determine the resonance type from the antinom relationship."""
    if _symbols_in_tension(event_a.symbol, event_b.symbol):
        return RelationType.CONTRADICTS
    if event_a.symbol == event_b.symbol:
        return RelationType.SUPPORTS
    if event_a.antinom_symbol == event_b.symbol:
        return RelationType.CONTRADICTS
    if event_b.antinom_symbol == event_a.symbol:
        return RelationType.CONTRADICTS
    # Check if they're in the same co-phase
    shared_phases = set(event_a.co_phases) & set(event_b.co_phases)
    if shared_phases:
        return RelationType.SEMANTIC
    return RelationType.DERIVED
```

---

## File 3: `comprehension/core/contention_mapper.py`

```python
"""
Contention Mapper — TAZV Comprehension Machine
===============================================
SO-OBSTAJANJE Protocol: contention is always already present (P2).

The old version FOUND contention between separate nodes.
This version REVEALS contention that was always there —
within each event (its antinom) and between events (resonance).

"Absolute without antinomy is death of language."
Every event carries its antinom. The mapper shows WHERE
that internal antinom is most active, and WHERE events'
antinoms resonate with each other.

Severity (from CounterAngle model): nizka / srednja / visoka
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum

from .graph_store import (
    RelationField, Resonance, RelationType, Severity, ContentionMark,
    SYMBOL_OPPOSITIONS,
)


# ── Phase tension: co-existing phases in conflict (P7) ──
PHASE_TENSIONS: Dict[tuple, str] = {
    (0, 1): 'BIOS(∅) vs STATE(¬) — openness confronts structure',
    (0, 2): 'BIOS(∅) vs UAF(Δ) — void confronts antinomy engine',
    (1, 2): 'STATE(¬) vs UAF(Δ) — cut confronts movement',
    (2, 4): 'UAF(Δ) vs APD(⧖) — antinomy confronts seal',
    (3, 0): 'JEWIK(⊢) vs BIOS(∅) — act confronts void',
    (1, 6): 'STATE(¬) vs VIS(⟡) — cut confronts manifestation',
}


@dataclass
class ContentionReport:
    """Full report of all contention revealed in the field."""
    total_contentions: int = 0
    internal_contentions: List[ContentionMark] = field(default_factory=list)  # within events
    resonance_contentions: List[ContentionMark] = field(default_factory=list)  # between events
    high_severity_count: int = 0
    summary: str = ''

    def to_dict(self) -> Dict:
        return {
            'total': self.total_contentions,
            'high_severity': self.high_severity_count,
            'internal': len(self.internal_contentions),
            'resonance': len(self.resonance_contentions),
            'summary': self.summary,
            'marks': [
                {
                    'event': m.event_position,
                    'severity': m.severity.value,
                    'description': m.description,
                    'antinom_pair': m.antinom_pair,
                }
                for m in self.internal_contentions + self.resonance_contentions
            ],
        }


class ContentionMapper:
    """
    Reveals WHERE antinomy lives.

    P2: contention is always already present. Every event carries its antinom.
    This mapper doesn't discover contention — it reveals what was always there.

    Two kinds of revelation:
      1. INTERNAL — the antinom within each event (assertion ↔ negation)
      2. RESONANCE — where events' antinoms amplify each other
    """

    def __init__(self, field: RelationField) -> None:
        self.field = field

    def reveal(self) -> ContentionReport:
        """
        Reveal all contention in the field.

        Pass 1: Internal antinom intensity — how active is the antinom within each event?
        Pass 2: Resonance contention — where do events' antinoms create shared tension?
        Pass 3: Phase co-existence tension — where do co-existing phases conflict? (P7)
        """
        report = ContentionReport()

        # Pass 1: Internal antinom
        for event in self.field.get_mapped_events():
            severity = self._assess_internal_severity(event)
            if severity:
                mark = self.field.reveal_contention(
                    event_position=event.surface_position,
                    severity=severity,
                    description=(
                        f'{event.word}({event.symbol}) carries {event.antinom_word}'
                        f'({event.antinom_symbol}): {event.antinom_note}'
                    ),
                    antinom_pair=f'{event.symbol} ↔ {event.antinom_symbol}',
                )
                report.internal_contentions.append(mark)

        # Pass 2: Resonance contention
        for res in self.field.get_all_resonances():
            if res.resonance_type == RelationType.CONTRADICTS:
                event_a = self.field.get_event(res.event_a_pos)
                event_b = self.field.get_event(res.event_b_pos)
                if event_a and event_b:
                    severity = Severity.VISOKA  # explicit contradiction
                    mark = self.field.reveal_contention(
                        event_position=res.event_a_pos,
                        severity=severity,
                        description=(
                            f'{event_a.word} CONTRADICTS {event_b.word}: {res.note}. '
                            f'Co-existing antinom: {res.antinom_note}'
                        ),
                        antinom_pair=f'{event_a.symbol} ↔ {event_b.symbol}',
                    )
                    report.resonance_contentions.append(mark)

        # Pass 3: Phase co-existence tension (P7)
        events = self.field.get_mapped_events()
        for i, event_a in enumerate(events):
            for event_b in events[i + 1:]:
                shared = set(event_a.co_phases) & set(event_b.co_phases)
                if not shared:
                    continue
                # They share a phase — but do their symbols oppose within that shared phase?
                if _symbols_in_tension_external(event_a.symbol, event_b.symbol):
                    phase_key = (
                        min(event_a.co_phases[0] if event_a.co_phases else 0,
                            event_b.co_phases[0] if event_b.co_phases else 0),
                        max(event_a.co_phases[-1] if event_a.co_phases else 0,
                            event_b.co_phases[-1] if event_b.co_phases else 0),
                    )
                    tension_desc = PHASE_TENSIONS.get(phase_key, f'phase co-existence: {event_a.co_phases} & {event_b.co_phases}')
                    severity = Severity.SREDNJA
                    if abs(event_a.co_phases[0] - event_b.co_phases[0]) >= 3 if event_a.co_phases and event_b.co_phases else False:
                        severity = Severity.VISOKA
                    mark = self.field.reveal_contention(
                        event_position=event_a.surface_position,
                        severity=severity,
                        description=f'Phase tension: {tension_desc}',
                        antinom_pair=f'phases {event_a.co_phases} ↔ {event_b.co_phases}',
                    )
                    report.resonance_contentions.append(mark)

        # Compile
        report.total_contentions = len(report.internal_contentions) + len(report.resonance_contentions)
        report.high_severity_count = sum(
            1 for m in report.internal_contentions + report.resonance_contentions
            if m.severity == Severity.VISOKA
        )
        report.summary = self._build_summary(report)
        return report

    def _assess_internal_severity(self, event) -> Optional[Severity]:
        """How active is the antinom within this event? P2."""
        if not event.antinom_symbol:
            return None

        # ∅ ↔ Δ is the core antinomy — always visoka
        pair = {event.symbol, event.antinom_symbol}
        if pair == {'∅', 'Δ'} or pair == {'Δ', '∅'}:
            return Severity.VISOKA
        if pair == {'¬', '∴'} or pair == {'∴', '¬'}:
            return Severity.VISOKA
        if pair == {'⊢', '∅'} or pair == {'∅', '⊢'}:
            return Severity.VISOKA

        # Any symbol opposition is at least srednja
        for a, b, _ in SYMBOL_OPPOSITIONS:
            if (event.symbol == a and event.antinom_symbol == b) or \
               (event.symbol == b and event.antinom_symbol == a):
                return Severity.SREDNJA

        # If co_phases are far apart, srednja
        if len(event.co_phases) >= 2:
            if max(event.co_phases) - min(event.co_phases) >= 3:
                return Severity.SREDNJA

        # Antinom is present but quiet — nizka
        return Severity.NIZKA

    def _build_summary(self, report: ContentionReport) -> str:
        parts: List[str] = []
        parts.append(f'{report.total_contentions} contention sites revealed.')
        parts.append(f'{report.high_severity_count} high-severity.')
        parts.append(f'{len(report.internal_contentions)} internal (within events), '
                     f'{len(report.resonance_contentions)} in resonance (between events).')

        high = [m for m in report.internal_contentions + report.resonance_contentions
                if m.severity == Severity.VISOKA]
        if high:
            parts.append('High-severity:')
            for m in high[:5]:
                parts.append(f'  • {m.description}')
            if len(high) > 5:
                parts.append(f'  ... and {len(high) - 5} more.')
        else:
            parts.append('No high-severity contention. Field is coherent.')

        return '\n'.join(parts)


def _symbols_in_tension_external(sym_a: str, sym_b: str) -> bool:
    if not sym_a or not sym_b:
        return False
    for a, b, _ in SYMBOL_OPPOSITIONS:
        if (sym_a == a and sym_b == b) or (sym_a == b and sym_b == a):
            return True
    return False
```

---

## File 4: `comprehension/core/transformation_tracer.py`

```python
"""
Transformation Tracer — TAZV Comprehension Machine
=============================================
SO-OBSTAJANJE Protocol: traces co-existing resonances, not linear paths (P6/P7).

"DOKAZ is the Product."
⊢ = dokazna sled: kaj se vidi, kaj se ponovi, kaj se preveri.

The old version traced linear paths through nodes (A→B→C→D).
This version traces how the INTERNAL DIVISION of one event
RESONATES with the internal division of another.

DOKAZ is not a path through a graph. DOKAZ is the lineage of
how meaning transforms — through co-existing resonance, not
sequential steps. The trail shows which divisions amplify,
which cancel, which create new possibilities.

JEWIK axioms (validation points):
  JEWIK_001: Beseda je ⊘ (beseda je rez, meja, poseg, dokaz prisotnosti)
  JEWIK_002: ⊘ = univerzalna enota reza, meja, obris, pogoj razlikovanja
  JEWIK_003: ∆ = osnovno gibanje: prehod, sprememba, razlika
  JEWIK_004: ∫ = integracija občutka, spomina, čuta in pomena
  JEWIK_005: ⊢ = dokazna sled: kaj se vidi, kaj se ponovi, kaj se preveri
  JEWIK_006: Vsak pojem mora imeti mejo
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum

from .graph_store import RelationField, Resonance, RelationType


# ── JEWIK Core Axioms ──
JEWIK_AXIOMS: List[Dict] = [
    {'id': 'JEWIK_001', 'statement': 'Beseda je ⊘ (beseda je rez, meja, poseg, dokaz prisotnosti)',
     'symbol': '⊘', 'absoluteness': 0.95, 'type': 'ONTOLOŠKA'},
    {'id': 'JEWIK_002', 'statement': '⊘ = univerzalna enota reza, meja, obris, pogoj razlikovanja',
     'symbol': '⊘', 'absoluteness': 0.92, 'type': 'ONTOLOŠKA'},
    {'id': 'JEWIK_003', 'statement': '∆ = osnovno gibanje: prehod, sprememba, razlika',
     'symbol': '∆', 'absoluteness': 0.90, 'type': 'ONTOLOŠKA'},
    {'id': 'JEWIK_004', 'statement': '∫ = integracija občutka, spomina, čuta in pomena',
     'symbol': '∫', 'absoluteness': 0.85, 'type': 'ONTOLOŠKA'},
    {'id': 'JEWIK_005', 'statement': '⊢ = dokazna sled: kaj se vidi, kaj se ponovi, kaj se preveri',
     'symbol': '⊢', 'absoluteness': 0.88, 'type': 'OPERATIVNA'},
    {'id': 'JEWIK_006', 'statement': 'Vsak pojem mora imeti mejo',
     'symbol': '¬', 'absoluteness': 0.90, 'type': 'OPERATIVNA'},
]

_AXIOM_LOOKUP = {a['id']: a for a in JEWIK_AXIOMS}


# ── Division resonance operators (how one division resonates with another) ──
# Not "∅→¬" (sequential transformation) but "∅∥¬" (co-existing resonance)
RESONANCE_OPERATORS: Dict[str, Dict] = {
    '∅∥Δ': {
        'name': 'void-movement-resonance',
        'description': 'Void resonates with movement — the core antinomy. Stasis and change co-exist.',
        'axiom': 'JEWIK_003',
        'intensity': 1.0,
    },
    '¬∥∴': {
        'name': 'cut-relation-resonance',
        'description': 'Cut resonates with relation — separation and connection co-exist.',
        'axiom': 'JEWIK_006',
        'intensity': 0.9,
    },
    '⊢∥∅': {
        'name': 'proof-void-resonance',
        'description': 'Proof resonates with void — assertion and negation co-exist.',
        'axiom': 'JEWIK_001',
        'intensity': 0.85,
    },
    '∫∥¬': {
        'name': 'presence-cut-resonance',
        'description': 'Presence resonates with cut — sustaining and separating co-exist.',
        'axiom': 'JEWIK_004',
        'intensity': 0.8,
    },
    'δ∥∫': {
        'name': 'passage-presence-resonance',
        'description': 'Passage resonates with presence — the cut that opens and the sustaining flow.',
        'axiom': 'JEWIK_002',
        'intensity': 0.75,
    },
    '⧖∥⊢': {
        'name': 'silence-proof-resonance',
        'description': 'Silence resonates with proof — listening and assertion co-exist.',
        'axiom': 'JEWIK_005',
        'intensity': 0.7,
    },
}


@dataclass
class ResonanceStep:
    """One step in the DOKAZ — a resonance between two events' divisions."""
    step_index: int
    event_a_word: str
    event_a_symbol: str
    event_a_divider: str
    event_a_divided: str
    event_b_word: str
    event_b_symbol: str
    event_b_divider: str
    event_b_divided: str
    resonance_key: str
    resonance_name: str
    description: str
    axiom_ref: Optional[str]
    intensity: float
    # P2: the antinom of this resonance
    antinom_resonance: str = ''

    def __repr__(self) -> str:
        return (f'Step {self.step_index}: '
                f'{self.event_a_word}({self.event_a_symbol}) ∥ '
                f'{self.event_b_word}({self.event_b_symbol}) [{self.resonance_name}]')


@dataclass
class DOKAZ:
    """
    A proof trail — NOT a linear path, but a resonance map.

    "DOKAZ is the Product." — the lineage showing how meaning
    transforms through co-existing resonance (P6/P7), not
    sequential steps.
    """
    statement: str
    events: List[ResonanceStep] = field(default_factory=list)
    total_intensity: float = 0.0
    validated_by_axioms: List[str] = field(default_factory=list)
    trail: str = ''  # human-readable: the resonance map

    def to_dict(self) -> Dict:
        return {
            'statement': self.statement,
            'steps': [
                {
                    'step': s.step_index,
                    'event_a': f'{s.event_a_word}({s.event_a_symbol})',
                    'division_a': f'{s.event_a_divider} | {s.event_a_divided}',
                    'event_b': f'{s.event_b_word}({s.event_b_symbol})',
                    'division_b': f'{s.event_b_divider} | {s.event_b_divided}',
                    'resonance': s.resonance_name,
                    'description': s.description,
                    'axiom': s.axiom_ref,
                    'intensity': s.intensity,
                    'antinom_resonance': s.antinom_resonance,
                }
                for s in self.events
            ],
            'total_intensity': self.total_intensity,
            'validated_by': self.validated_by_axioms,
            'trail': self.trail,
        }


class TransformationTracer:
    """
    Traces how meaning transforms — through co-existing resonance (P6/P7).

    The old tracer followed linear paths through nodes.
    This tracer follows how the INTERNAL DIVISION of one event
    resonates with the INTERNAL DIVISION of another.

    DOKAZ = the resonance map. Not "A became B" but
    "A's division resonates with B's division, and here is the proof."
    """

    def __init__(self, field: RelationField) -> None:
        self.field = field

    def trace_statement(self, statement: str) -> DOKAZ:
        """
        Trace the resonance map of an entire statement.

        For every pair of mapped events, check if their divisions
        resonate. Record each resonance as a step in the DOKAZ.
        """
        dokaz = DOKAZ(statement=statement)
        events = self.field.get_mapped_events()
        axioms_used: List[str] = []
        intensity_product = 1.0

        step_idx = 0
        trail_parts: List[str] = []

        for i, event_a in enumerate(events):
            for event_b in events[i + 1:]:
                resonance = self._check_resonance(event_a, event_b)
                if resonance:
                    op_key, operator = resonance

                    if operator['axiom'] and operator['axiom'] not in axioms_used:
                        axioms_used.append(operator['axiom'])

                    intensity_product *= operator['intensity']

                    step = ResonanceStep(
                        step_index=step_idx,
                        event_a_word=event_a.word,
                        event_a_symbol=event_a.symbol,
                        event_a_divider=event_a.divider,
                        event_a_divided=event_a.divided,
                        event_b_word=event_b.word,
                        event_b_symbol=event_b.symbol,
                        event_b_divider=event_b.divider,
                        event_b_divided=event_b.divided,
                        resonance_key=op_key,
                        resonance_name=operator['name'],
                        description=operator['description'],
                        axiom_ref=operator.get('axiom'),
                        intensity=operator['intensity'],
                        antinom_resonance=(
                            f'{event_a.antinom_word}({event_a.antinom_symbol}) ∥ '
                            f'{event_b.antinom_word}({event_b.antinom_symbol})'
                        ),
                    )
                    dokaz.events.append(step)
                    trail_parts.append(
                        f'{event_a.word}({event_a.symbol})∥{event_b.word}({event_b.symbol})'
                    )
                    step_idx += 1

        dokaz.total_intensity = intensity_product if dokaz.events else 0.0
        dokaz.validated_by_axioms = axioms_used
        dokaz.trail = ' ∥ '.join(trail_parts) if trail_parts else '(no resonances found)'

        return dokaz

    def _check_resonance(self, event_a, event_b) -> Optional[tuple]:
        """Check if two events' divisions resonate."""
        # Try all orderings of their symbols
        for sym_a, sym_b in [
            (event_a.symbol, event_b.symbol),
            (event_b.symbol, event_a.symbol),
            (event_a.antinom_symbol, event_b.symbol),
            (event_a.symbol, event_b.antinom_symbol),
            (event_a.antinom_symbol, event_b.antinom_symbol),
        ]:
            if not sym_a or not sym_b:
                continue
            key = f'{sym_a}∥{sym_b}'
            if key in RESONANCE_OPERATORS:
                return key, RESONANCE_OPERATORS[key]
        return None

    def get_axiom_validation(self, dokaz: DOKAZ) -> List[Dict]:
        """Get the full JEWIK axiom texts that validate this DOKAZ."""
        return [_AXIOM_LOOKUP[aid] for aid in dokaz.validated_by_axioms
                if aid in _AXIOM_LOOKUP]
```

---

## How the 4 files work together now

```
Statement: "The word is no"
                │
                ▼
    ┌────────────────────────────────────────┐
    │   decomposer.py                         │
    │   decompose_statement()                 │
    │                                         │
    │   THE → divider: ð  divided: ə  symbol: δ│
    │         antinom: (unmarked field)(∅)     │
    │         co_phases: [0, 1]  ← P7          │
    │                                         │
    │   WORD → divider: w+d divided: ɜːr ⊢    │
    │         antinom: SILENCE(⧖)              │
    │         co_phases: [3, 4]                │
    │                                         │
    │   IS → divider: 1  divided: z  symbol: Δ │
    │         antinom: NOT(¬)                   │
    │         co_phases: [1, 2]                │
    │                                         │
    │   NO → divider: n  divided: ou  symbol: ∅│
    │         antinom: YES(Δ)                  │
    │         co_phases: [0, 2]                │
    └───────────────┬────────────────────────┘
                    │ RelationEvent[]
                    ▼
    ┌────────────────────────────────────────┐
    │   graph_store.py (RelationField)        │
    │   build_from_events()                   │
    │                                         │
    │   P5: resistance computed                │
    │   THE pushes against: IS, NO             │
    │   WORD pushes against: NO                │
    │   IS pushes against: THE, NO            │
    │   NO pushes against: THE, IS, WORD       │
    │                                         │
    │   Resonances (P4: relation is primary):  │
    │   THE(δ) ∥ IS(Δ)  — passage↔movement     │
    │   THE(δ) ∥ NO(∅)  — passage↔void         │
    │   WORD(⊢) ∥ NO(∅) — proof↔void           │
    │   IS(Δ) ∥ NO(∅)  — movement↔void (CORE)  │
    └───────────────┬────────────────────────┘
                    │ RelationField
            ┌───────┴───────┐
            ▼               ▼
    ┌───────────────┐ ┌───────────────────┐
    │ contention_   │ │ transformation_   │
    │ mapper.py     │ │ tracer.py         │
    │               │ │                   │
    │ P2: REVEALS   │ │ P6/P7: traces     │
    │ contention    │ │ co-existing       │
    │ that was      │ │ resonance, not    │
    │ always there  │ │ linear paths      │
    │               │ │                   │
    │ INTERNAL:     │ │ DOKAZ:            │
    │ NO(∅↔Δ) VISOKA│ │ IS(Δ)∥NO(∅)       │
    │ IS(Δ↔¬) SREDNJA│ │  = void-movement  │
    │ WORD(⊢↔⧖) NIZKA│ │   resonance      │
    │               │ │  validated by     │
    │ RESONANCE:    │ │  JEWIK_003        │
    │ IS∥NO = VISOKA│ │                   │
    └───────────────┘ └───────────────────┘
```

### Integration with R-7 pipeline

```python
from comprehension.core.decomposer import decompose_statement
from comprehension.core.graph_store import RelationField
from comprehension.core.contention_mapper import ContentionMapper
from comprehension.core.transformation_tracer import TransformationTracer

def run_comprehension_layer(statement: str) -> dict:
    # P3/P2/P7: decompose into relation-events with antinoms and co-phases
    events = decompose_statement(statement)

    # P4/P5: build the field (relations primary, resistance computed)
    field = RelationField()
    field.build_from_events(events)

    # P2: reveal contention (always already present)
    mapper = ContentionMapper(field)
    contention_report = mapper.reveal()

    # P6/P7: trace co-existing resonance (DOKAZ)
    tracer = TransformationTracer(field)
    dokaz = tracer.trace_statement(statement)

    return {
        'events': [
            {
                'word': e.word, 'symbol': e.symbol,
                'divider': e.divider, 'divided': e.divided,
                'antinom': f'{e.antinom_word}({e.antinom_symbol})',
                'co_phases': e.co_phases,
                'mapped': e.mapped,
            }
            for e in events
        ],
        'field': field.to_dict(),
        'contention': contention_report.to_dict(),
        'dokaz': dokaz.to_dict(),
    }
```

### What changed (mess → fixed)

| Old (mess) | New (fixed) |
|------------|-------------|
| WordPoint: one symbol, one position on a line | RelationEvent: divider/divided + antinom + co-phases |
| GraphNode (standalone) + GraphEdge (connects) | RelationEvent (primary) + Resonance (co-existence) |
| Contention FOUND between separate nodes | Contention REVEALED within events (always already there) |
| DOKAZ = linear path A→B→C→D | DOKAZ = resonance map: A∥B, A∥C, B∥C (co-existing) |
| One phase per word (sequential) | Co-existing phases per word (so-obstajanje) |
| No antinom | Every word carries its antinom (P2) |
| No resistance | Every word pushes against others (P5) |
| Line preserved as data structure | Line is surface only (P6) |

### Protocol compliance checklist (for any future code in this layer)

- [ ] P1: Does this code treat any word as standalone? If yes, fix it.
- [ ] P2: Does every word carry its antinom? If not, add it.
- [ ] P3: Does every word show its internal division (divider/divided)?
- [ ] P4: Is relation the primary unit, or is node/entity primary?
- [ ] P5: Does every word have a resistance field (what it pushes against)?
- [ ] P6: Does this code rely on linear reading order as ontological structure?
- [ ] P7: Does this code assign ONE phase, or does it show co-existing phases?