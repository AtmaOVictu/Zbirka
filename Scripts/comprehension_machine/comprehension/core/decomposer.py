"""
Decomposer — TAZV Comprehension Machine
========================================
Breaks a statement into word-points using the corpus-validated
WOR(L)D ontological decomposition table.

Source: Beseda je Ne -> WOR(L)D English Ontological Lexicon
(26 terms confirmed across Obs1-Obs11, Self, Word is No libraries)

Each word becomes a WordPoint:
  - word:           original token
  - position:       index in the statement (0-based)
  - symbol:         ontological glyph (δ, ⊢, Δ, ∅, ¬, ∴, ...)
  - decomposition:  phonetic breakdown (e.g. "w + a:r + d")
  - role:           ontological role description
  - r7_phase:       which R-7 phase this word's operator belongs to
  - mapped:         True if found in the decomposition table

R-7: ∅ → ¬ → ∆ → 1 → ⧖ → ∮ → ⟡
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict
import re


# -- Ontological symbol -> R-7 phase mapping --
SYMBOL_TO_PHASE: Dict[str, int] = {
    '∅':  0,   # BIOS — praznina, potencial
    '¬':  1,   # STATE — locitev, struktura
    'Δ':  2,   # UAF — razlika, gibanje, antinomija
    '∴':  2,   # UAF — relation established (same phase as Δ)
    '⊢':  3,   # JEWIK — dejanje, emanacija, pecat
    '1':  3,   # JEWIK — the seal
    '⧖':  4,   # APD — tisina, preverba, izgovor
    '∮':  5,   # MICRO — povratek, ucenje
    '⟡':  6,   # VISUALIZATION — nova moznost
    'δ':  1,   # STATE-adjacent — the cut/rez operator
    '||': 5,   # MICRO — spiral, echo, return
    '∥': 5,   # MICRO — seal through duration
    'ʃ':  4,   # APD — persistence, presence sustained
    '⊥': 0,   # BIOS — the bearer, ground before question
    '∂':  6,   # VISUALIZATION — the passage, observer
    'ð':  6,   # VISUALIZATION — same as ∂ (the passage)
    'W':  3,   # JEWIK — wanting that transforms
    '⊘Δ': 2,   # UAF — ne that must-be (composite)
    '¬∴': 2,   # UAF — doubt, double-cut (composite)
}


@dataclass
class WordPoint:
    """A single word decomposed into its ontological operator."""
    word: str
    position: int
    symbol: str
    decomposition: str
    role: str
    r7_phase: int
    mapped: bool

    def __repr__(self) -> str:
        status = '✓' if self.mapped else '?'
        return f'WordPoint({self.word}→{self.symbol} [{status}] p{self.position})'


# -- The decomposition table (corpus-validated, 26 terms) --
# Sources: WOR(L)D lexicon — Obs11, Word is No, Beseda je Ne, Self libraries
DECOMPOSITION_TABLE: Dict[str, Dict] = {
    # -- Terms 1-13: base operators --
    'THE': {
        'decomposition': 'ð + ə → contact-with-open-space',
        'symbol': 'δ',
        'role': 'The operator that singles out — carries one ripple from the field into presence',
    },
    'WORD': {
        'decomposition': 'w + ɜːr + d → breath-resonance-cut',
        'symbol': '⊢',
        'role': 'The act of cutting being into form — proof that something is; the (L) keeps the word flowing',
    },
    'WOR(L)D': {
        'decomposition': 'w + a:r + d → breath-resonance-cut',
        'symbol': '⊢',
        'role': 'The act of cutting being into form — proof that something is; the (L) keeps the word flowing',
    },
    'IS': {
        'decomposition': '1 + z → minimal-opening-sustained',
        'symbol': 'Δ',
        'role': 'The hum of continuing-to-be — activation that sustains',
    },
    'NO': {
        'decomposition': 'n + ou → inward-resonance-into-circle',
        'symbol': '∅',
        'role': 'The ne-operator — the passage between inward and outward; condition of the next YES',
    },
    'NOT': {
        'decomposition': 'n + o + t → inward-through-depth-into-cut',
        'symbol': '¬',
        'role': 'The act of cutting open — separation-as-distinction — the cut that opens',
    },
    'MEANING': {
        'decomposition': 'm + i: + n + 1 + η → hum-reaching-swallowed',
        'symbol': '∴',
        'role': 'The act of reaching-toward returning into body — relation established',
    },
    'MEAN(L)ING': {
        'decomposition': 'm + i: + n + 1 + η → hum-reaching-swallowed',
        'symbol': '∴',
        'role': 'The act of reaching-toward returning into body — relation established',
    },
    'CUT': {
        'decomposition': 'k + λ + t → depth-force-through-opening-into-edge',
        'symbol': 'δ',
        'role': 'The rez that makes difference visible — condition of clarity',
    },
    'MIND': {
        'decomposition': 'm + æt + n + d → hum-wide-closure-division',
        'symbol': '||',
        'role': 'The spiral: reach-and-return that composes sense from pressure',
    },
    'M(L)IND': {
        'decomposition': 'm + æt + n + d → hum-wide-closure-division',
        'symbol': '||',
        'role': 'The spiral: reach-and-return that composes sense from pressure',
    },
    'FROM': {
        'decomposition': 'f + r + o + m → breath-ripple-out-of-depth-into-hum',
        'symbol': 'δ',
        'role': 'Origin-as-departure — the passage that carries its starting point forward',
    },
    'TO': {
        'decomposition': 't + u: → cut-into-sustained-direction',
        'symbol': '∴',
        'role': 'Directed relation — the arrow that establishes the path',
    },
    'CREATE': {
        'decomposition': 'kr + i + ei + t → depth-reaching-emission-seal',
        'symbol': 'Δ',
        'role': 'Transformation that responds to necessity — the act that brings forth from pressure',
    },
    'THOUGHT': {
        'decomposition': 'θ + o: + t → friction-sustained-into-cut',
        'symbol': '||',
        'role': 'The echo that connects states — response-operator resonating to pressure',
    },
    'REFLECTION': {
        'decomposition': 'r + 1 + fle + k + ∫ + an → return-fold-depth-friction-resonance',
        'symbol': '∅',
        'role': 'The folding-back that differs — repetition-as-difference',
    },
    # -- Terms 14-26: extended operators --
    'NECESSARY': {
        'decomposition': 'ne + sə + sə + ri → ne-hissing-through-open-return',
        'symbol': '⊘Δ',
        'role': 'The ne that must-be — internal pressure making transition unavoidable',
    },
    'INVENTION': {
        'decomposition': 'ɪn + ven + ʃ + ə → entry-coming-friction-settling',
        'symbol': 'Δ',
        'role': 'The act that brings forth from necessity — response to pressure that demands voice',
    },
    'CHARACTER': {
        'decomposition': 'k + æ + r + ə + k + t + ə → force-exposed-return-force-seal-open',
        'symbol': '∥',
        'role': 'The seal through duration — what stands through the double test',
    },
    'TIME': {
        'decomposition': 't + aɪ + m → cut-span-hum',
        'symbol': '∥',
        'role': 'The pulse of meaning — time as the body-hum that holds the cut',
    },
    'T(L)IME': {
        'decomposition': 't + aɪ + m → cut-span-hum',
        'symbol': '∥',
        'role': 'The pulse of meaning — time as the body-hum that holds the cut',
    },
    'DOUBT': {
        'decomposition': 'd + au + t → division-descent-into-cut',
        'symbol': '¬∴',
        'role': 'The condition of consciousness — the double-cut that opens truth',
    },
    'TRUTH': {
        'decomposition': 't + r + u: + θ → cut-return-sustained-friction',
        'symbol': '∴',
        'role': 'The path lived — process, the living path; presses, dissects, cuts through',
    },
    'FAITH': {
        'decomposition': 'f + eɪ + θ → breath-emission-into-friction',
        'symbol': 'ʃ',
        'role': 'Persistence that holds the open question — presence sustained through friction',
    },
    'FA(L)TH': {
        'decomposition': 'f + eɪ + θ → breath-emission-into-friction',
        'symbol': 'ʃ',
        'role': 'Persistence that holds the open question — presence sustained through friction',
    },
    'WILL': {
        'decomposition': 'w + ɪ + l → breath-into-opening-into-flow',
        'symbol': 'W',
        'role': 'The wanting that transforms through presence into address',
    },
    'W(L)LL': {
        'decomposition': 'w + ɪ + l → breath-into-opening-into-flow',
        'symbol': 'W',
        'role': 'The wanting that transforms through presence into address',
    },
    'BODY': {
        'decomposition': 'b + b + d + i → plosion-depth-division-reaching',
        'symbol': '⊥',
        'role': 'The bearer — what exists before the question; the ground that allows error',
    },
    'SOUL': {
        'decomposition': 's + ou + l → hiss-into-circle-into-flow',
        'symbol': 'ʃ',
        'role': 'The breath-stream that opens into totality and keeps flowing — presence carrying',
    },
    'SPIRIT': {
        'decomposition': 's + p + ɪ + r + ɪ + t → hiss-burst-opening-return-opening-cut',
        'symbol': '∥',
        'role': 'The fire of axiomatic force — the power that breaks through and returns to break through',
    },
    'SP(L)RIT': {
        'decomposition': 's + p + ɪ + r + ɪ + t → hiss-burst-opening-return-opening-cut',
        'symbol': '∥',
        'role': 'The fire of axiomatic force — the power that breaks through and returns to break through',
    },
    'EGO': {
        'decomposition': 'i: + g + ou → sustained-reaching-assertion-circle',
        'symbol': '⊘',
        'role': 'The boundary, the membrane, the cut — the part bearing the whole; acknowledges bearing',
    },
    'SELF': {
        'decomposition': 's + ɛ + l + f → hiss-exposure-flow-outward',
        'symbol': '∂',
        'role': 'The passage itself — the observer of transitions',
    },
    'BEING': {
        'decomposition': "b + i: + ɪ + ŋ → plosion-sustained-reaching-opening-swallowed",
        'symbol': '∫',
        'role': 'The sustained act — presence that sustains itself by returning into the body',
    },
    'NOTHING': {
        'decomposition': "n + ʌ + θ + ɪ + ŋ → inward-opening-friction-opening-swallowed",
        'symbol': '∅',
        'role': 'The inward turn through friction back into body — absence that prepares',
    },
    'GOD': {
        'decomposition': 'g + ɒ + d → depth-plosion-resonance-division',
        'symbol': '∮',
        'role': 'The spiral totality that returns — keeps the question open; if God exists, let God listen',
    },
    'SILENCE': {
        'decomposition': 's + aɪ + l + əns → hiss-span-flow-cessation',
        'symbol': '⧖',
        'role': 'Tiheon — the sacred silence that is full of listening; the body becomes ear',
    },
}

# -- Slovenian equivalents (bidirectional lookup) --
SLOVENIAN_MAP: Dict[str, str] = {
    'BESEDA': 'WORD',
    'NE': 'NO',
    'NI': 'NOT',
    'POMEN': 'MEANING',
    'REZ': 'CUT',
    'UM': 'MIND',
    'IZ': 'FROM',
    'V': 'TO',
    'USTVARJAJ': 'CREATE',
    'MISEL': 'THOUGHT',
    'ZRCALO': 'REFLECTION',
    'NUJNO': 'NECESSARY',
    'IZUM': 'INVENTION',
    'ZNANJE': 'CHARACTER',
    'CAS': 'TIME',
    'DVOM': 'DOUBT',
    'RESNICA': 'TRUTH',
    'VERA': 'FAITH',
    'VOLJA': 'WILL',
    'TELO': 'BODY',
    'DUSA': 'SOUL',
    'DUH': 'SPIRIT',
    'JAZ': 'EGO',
    'SE': 'SELF',
    'BITI': 'BEING',
    'NIC': 'NOTHING',
    'BOG': 'GOD',
    'TISINA': 'SILENCE',
}


def _normalize_token(token: str) -> str:
    """Normalize a token for lookup: strip punctuation, uppercase, preserve (L) markers."""
    cleaned = re.sub(r'^[^A-Za-z(]+|[^A-Za-z)]+$', '', token)
    return cleaned.upper()


def _try_lookup(word: str) -> Optional[Dict]:
    """Try multiple lookup strategies for a word."""
    upper = word.upper()

    if upper in DECOMPOSITION_TABLE:
        return DECOMPOSITION_TABLE[upper]

    # Try with (L) inserted (WORD -> WOR(L)D)
    for suffix_len in [2, 3, 4]:
        if len(upper) > suffix_len + 1:
            insert_pos = len(upper) - suffix_len
            if upper[insert_pos] == 'L':
                variant = upper[:insert_pos] + '(L)' + upper[insert_pos + 1:]
                if variant in DECOMPOSITION_TABLE:
                    return DECOMPOSITION_TABLE[variant]

    # Try without (L) markers
    stripped = upper.replace('(L)', 'L')
    if stripped in DECOMPOSITION_TABLE:
        return DECOMPOSITION_TABLE[stripped]

    return None


def decompose_statement(text: str) -> List[WordPoint]:
    """
    Decompose a statement into word-points.
    "All words are points. The lines are the logic that follows."
    """
    if not text or not text.strip():
        return []

    raw_tokens = text.strip().split()
    points: List[WordPoint] = []

    for i, token in enumerate(raw_tokens):
        normalized = _normalize_token(token)
        entry = _try_lookup(normalized)

        if entry is None:
            slovenian_key = normalized
            if slovenian_key in SLOVENIAN_MAP:
                english_equiv = SLOVENIAN_MAP[slovenian_key]
                entry = _try_lookup(english_equiv)

        if entry is not None:
            symbol = entry['symbol']
            points.append(WordPoint(
                word=token,
                position=i,
                symbol=symbol,
                decomposition=entry['decomposition'],
                role=entry['role'],
                r7_phase=SYMBOL_TO_PHASE.get(symbol, -1),
                mapped=True,
            ))
        else:
            points.append(WordPoint(
                word=token,
                position=i,
                symbol='',
                decomposition='',
                role='UNMAPPED — no ontological operator found',
                r7_phase=-1,
                mapped=False,
            ))

    return points


def get_symbol_sequence(points: List[WordPoint]) -> str:
    """Return the sequence of ontological symbols as a string: δ⊢Δ∅¬∴..."""
    return ''.join(p.symbol for p in points if p.mapped)


def get_mapped_ratio(points: List[WordPoint]) -> float:
    """Fraction of words that have an ontological mapping (0.0 - 1.0)."""
    if not points:
        return 0.0
    mapped = sum(1 for p in points if p.mapped)
    return mapped / len(points)
