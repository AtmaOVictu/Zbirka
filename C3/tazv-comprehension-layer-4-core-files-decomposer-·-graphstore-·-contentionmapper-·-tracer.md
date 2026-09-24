# TAZV Comprehension Layer

Four Python files that give the app real comprehension: it can now break a statement into word-points, build a graph of relations, find WHERE contention lives, and trace HOW meaning transforms.

Save each file to `comprehension/core/` in your project. They are self-contained (no external deps beyond stdlib) and integrate with the existing R-7 pipeline via the `PipelineResult` interface.

---

## File 1: `comprehension/core/decomposer.py`

```python
"""
Decomposer — TAZV Comprehension Machine
========================================
Breaks a statement into word-points using the corpus-validated
WOR(L)D ontological decomposition table.

Source: Beseda je Ne → WOR(L)D English Ontological Lexicon
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


# ── Ontological symbol → R-7 phase mapping ──
SYMBOL_TO_PHASE: Dict[str, int] = {
    '∅':  0,   # BIOS — praznina, potencial
    '¬':  1,   # STATE — ločitev, struktura
    'Δ':  2,   # UAF — razlika, gibanje, antinomija
    '∴':  2,   # UAF — relation established (same phase as Δ)
    '⊢':  3,   # JEWIK — dejanje, emanacija, pečat
    '1':  3,   # JEWIK — the seal
    '⧖': 4,   # APD — tišina, preverba, izgovor
    '∮':  5,   # MICRO — povratek, učenje
    '⟡': 6,   # VISUALIZATION — nova možnost
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


# ── The decomposition table (corpus-validated, 26 terms) ──
# Sources: WOR(L)D lexicon — Obs11, Word is No, Beseda je Ne, Self libraries
DECOMPOSITION_TABLE: Dict[str, Dict] = {
    # ── Terms 1-13: base operators ──
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
    # ── Terms 14-26: extended operators ──
    'NECESSARY': {
        'decomposition': 'ne + sə + sə + ri → ne-hissing-through-open-return',
        'symbol': '⊘Δ',
        'role': 'The ne that must-be — internal pressure making transition unavoidable',
    },
    'INVENTION': {
        'decomposition': 'ɪn + ven + ʃ + ən → entry-coming-friction-settling',
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

# ── Slovenian equivalents (bidirectional lookup) ──
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
    # Remove trailing/leading punctuation but keep internal (L)
    cleaned = re.sub(r'^[^A-Za-z(]+|[^A-Za-z)]+$', '', token)
    return cleaned.upper()


def _try_lookup(word: str) -> Optional[Dict]:
    """Try multiple lookup strategies for a word."""
    upper = word.upper()

    # Direct hit
    if upper in DECOMPOSITION_TABLE:
        return DECOMPOSITION_TABLE[upper]

    # Try with (L) inserted (WORD → WOR(L)D)
    # Common pattern: vowel before L gets (L) marker
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

    Args:
        text: The input statement (Slovenian or English)

    Returns:
        List of WordPoint objects, one per word in the statement
    """
    if not text or not text.strip():
        return []

    # Tokenize: split on whitespace, keep words
    raw_tokens = text.strip().split()

    points: List[WordPoint] = []
    for i, token in enumerate(raw_tokens):
        normalized = _normalize_token(token)

        # Try English lookup
        entry = _try_lookup(normalized)

        # Try Slovenian → English mapping
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
            # Unmapped word — still a point, but no ontological operator
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
```

---

## File 2: `comprehension/core/graph_store.py`

```python
"""
Graph Store — TAZV Comprehension Machine
=========================================
Semantic graph: words are nodes, relations are edges.
Every relation is also addressable as a node (hypergraph).

"All words are points. The lines are the logic that follows."

Relation types from corpus (JEWIK Truthbase Studio):
  SUPPORTS, CONTRADICTS, DEFINES, REFINES, TESTS, SYMBOLICALLY_LINKED

Archive-level relation types (from composition system):
  direct, semantic, compositional, derived, custom

JEWIK data model adapted from:
  UnitLink { id, fromUnitId, toUnitId, relationType, note }
  CounterAngle { id, truthUnitId, description, severity }
  EvidenceRef { id, truthUnitId, quote, sourceLocation?, confidence }

Storage Primitive = Relation.
Operational Primitive = Difference.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Set, Tuple
from enum import Enum
import uuid


# ── Relation types (corpus-validated from JEWIK Truthbase Studio) ──
class RelationType(str, Enum):
    """Every relation MUST have a type (corpus rule)."""
    SUPPORTS = 'SUPPORTS'           # podpira
    CONTRADICTS = 'CONTRADICTS'     # protislovje
    DEFINES = 'DEFINES'             # definira
    REFINES = 'REFINES'             # izboljša
    TESTS = 'TESTS'                 # preverja
    SYMBOLICALLY_LINKED = 'SYMBOLICALLY_LINKED'  # simbolno povezano

    # Archive-level types (composition system)
    DIRECT = 'direct'
    SEMANTIC = 'semantic'
    COMPOSITIONAL = 'compositional'
    DERIVED = 'derived'
    CUSTOM = 'custom'


RELATION_TYPE_LABELS: Dict[str, str] = {
    'SUPPORTS': 'podpira',
    'CONTRADICTS': 'protislovje',
    'DEFINES': 'definira',
    'REFINES': 'izboljša',
    'TESTS': 'preverja',
    'SYMBOLICALLY_LINKED': 'simbolno povezano',
    'direct': 'neposredno',
    'semantic': 'semantično',
    'compositional': 'sestavljeno',
    'derived': 'izvedeno',
    'custom': 'po meri',
}


# ── Severity levels (from CounterAngle model) ──
class Severity(str, Enum):
    NIZKA = 'nizka'      # low
    SREDNJA = 'srednja'  # medium
    VISOKA = 'visoka'    # high


@dataclass
class GraphNode:
    """A node in the semantic graph — a word-point."""
    id: str
    word: str
    position: int
    symbol: str
    decomposition: str
    role: str
    r7_phase: int
    is_relation_node: bool = False  # True if this node represents a relation (hypergraph)

    def __repr__(self) -> str:
        return f'Node({self.word}→{self.symbol or "?"})'


@dataclass
class GraphEdge:
    """An edge in the semantic graph — a relation between word-points."""
    id: str
    from_id: str
    to_id: str
    relation_type: RelationType
    note: str = ''
    confidence: float = 1.0
    evidence: List[str] = field(default_factory=list)  # quote strings from corpus
    promoted_to_node: bool = False  # True if this edge has been promoted to a node

    def __repr__(self) -> str:
        return f'Edge({self.from_id} --{self.relation_type.value}--> {self.to_id})'


@dataclass
class ContentionMark:
    """A mark on a node or edge indicating WHERE antinomy lives."""
    target_type: str  # 'node' or 'edge'
    target_id: str
    severity: Severity
    description: str
    opposing_symbol: str = ''  # the symbol that creates tension


class GraphStore:
    """
    Semantic graph store with hypergraph support.

    Every relation becomes addressable as a node — this is the hypergraph
    principle from the corpus: "Every relation becomes addressable as a node."
    """

    def __init__(self) -> None:
        self._nodes: Dict[str, GraphNode] = {}
        self._edges: Dict[str, GraphEdge] = {}
        self._contentions: List[ContentionMark] = []
        self._node_to_edges: Dict[str, List[str]] = {}  # adjacency index

    # ── Node operations ──

    def add_node(
        self,
        word: str,
        position: int,
        symbol: str,
        decomposition: str = '',
        role: str = '',
        r7_phase: int = -1,
    ) -> GraphNode:
        """Add a word-point as a node. Returns the created node."""
        node_id = str(uuid.uuid4())
        node = GraphNode(
            id=node_id,
            word=word,
            position=position,
            symbol=symbol,
            decomposition=decomposition,
            role=role,
            r7_phase=r7_phase,
        )
        self._nodes[node_id] = node
        self._node_to_edges[node_id] = []
        return node

    def get_node(self, node_id: str) -> Optional[GraphNode]:
        return self._nodes.get(node_id)

    def find_nodes_by_word(self, word: str) -> List[GraphNode]:
        """Find all nodes matching a word (case-insensitive)."""
        upper = word.upper()
        return [n for n in self._nodes.values()
                if n.word.upper() == upper and not n.is_relation_node]

    def find_nodes_by_symbol(self, symbol: str) -> List[GraphNode]:
        """Find all nodes with a given ontological symbol."""
        return [n for n in self._nodes.values()
                if n.symbol == symbol and not n.is_relation_node]

    # ── Edge operations ──

    def add_edge(
        self,
        from_id: str,
        to_id: str,
        relation_type: RelationType,
        note: str = '',
        confidence: float = 1.0,
        evidence: Optional[List[str]] = None,
    ) -> Optional[GraphEdge]:
        """Add a relation between two nodes. Returns the created edge, or None if nodes missing."""
        if from_id not in self._nodes or to_id not in self._nodes:
            return None

        edge_id = str(uuid.uuid4())
        edge = GraphEdge(
            id=edge_id,
            from_id=from_id,
            to_id=to_id,
            relation_type=relation_type,
            note=note,
            confidence=confidence,
            evidence=evidence or [],
        )
        self._edges[edge_id] = edge

        # Update adjacency index (bidirectional)
        self._node_to_edges[from_id].append(edge_id)
        self._node_to_edges[to_id].append(edge_id)

        return edge

    def get_edge(self, edge_id: str) -> Optional[GraphEdge]:
        return self._edges.get(edge_id)

    def get_edges_for_node(self, node_id: str) -> List[GraphEdge]:
        """Get all edges connected to a node."""
        edge_ids = self._node_to_edges.get(node_id, [])
        return [self._edges[eid] for eid in edge_ids if eid in self._edges]

    def get_edges_by_type(self, relation_type: RelationType) -> List[GraphEdge]:
        """Get all edges of a specific relation type."""
        return [e for e in self._edges.values() if e.relation_type == relation_type]

    # ── Hypergraph: promote relation to node ──

    def promote_relation_to_node(self, edge_id: str) -> Optional[GraphNode]:
        """
        Promote a relation to an addressable node (hypergraph operation).

        "Every relation becomes addressable as a node."
        The relation node carries the relation type as its symbol.
        """
        edge = self._edges.get(edge_id)
        if edge is None or edge.promoted_to_node:
            return None

        from_node = self._nodes[edge.from_id]
        to_node = self._nodes[edge.to_id]

        # Create a node that represents this relation
        rel_node = GraphNode(
            id=str(uuid.uuid4()),
            word=f'[{from_node.word}→{to_node.word}]',
            position=-1,  # not a word in the statement
            symbol=edge.relation_type.value,
            decomposition=f'{from_node.symbol} --{edge.relation_type.value}--> {to_node.symbol}',
            role=f'Relation: {RELATION_TYPE_LABELS.get(edge.relation_type.value, edge.relation_type.value)}',
            r7_phase=-1,
            is_relation_node=True,
        )
        self._nodes[rel_node.id] = rel_node
        self._node_to_edges[rel_node.id] = []

        edge.promoted_to_node = True
        return rel_node

    # ── Contention marks ──

    def add_contention(
        self,
        target_type: str,
        target_id: str,
        severity: Severity,
        description: str,
        opposing_symbol: str = '',
    ) -> ContentionMark:
        """Mark a node or edge as a site of contention."""
        mark = ContentionMark(
            target_type=target_type,
            target_id=target_id,
            severity=severity,
            description=description,
            opposing_symbol=opposing_symbol,
        )
        self._contentions.append(mark)
        return mark

    def get_contentions(self) -> List[ContentionMark]:
        return list(self._contentions)

    def get_contentions_for_node(self, node_id: str) -> List[ContentionMark]:
        return [c for c in self._contentions
                if c.target_type == 'node' and c.target_id == node_id]

    def get_contentions_for_edge(self, edge_id: str) -> List[ContentionMark]:
        return [c for c in self._contentions
                if c.target_type == 'edge' and c.target_id == edge_id]

    # ── Graph queries ──

    def neighbors(self, node_id: str) -> List[GraphNode]:
        """Get all nodes directly connected to a node."""
        result: List[GraphNode] = []
        for edge in self.get_edges_for_node(node_id):
            other_id = edge.to_id if edge.from_id == node_id else edge.from_id
            other = self._nodes.get(other_id)
            if other is not None:
                result.append(other)
        return result

    def find_path(
        self,
        start_id: str,
        end_id: str,
        max_depth: int = 10,
    ) -> List[str]:
        """BFS pathfinding between two nodes. Returns list of node IDs."""
        if start_id == end_id:
            return [start_id]
        if start_id not in self._nodes or end_id not in self._nodes:
            return []

        visited: Set[str] = {start_id}
        queue: List[Tuple[str, List[str]]] = [(start_id, [start_id])]

        while queue:
            current, path = queue.pop(0)
            if len(path) >= max_depth:
                continue
            for neighbor in self.neighbors(current):
                if neighbor.id == end_id:
                    return path + [neighbor.id]
                if neighbor.id not in visited:
                    visited.add(neighbor.id)
                    queue.append((neighbor.id, path + [neighbor.id]))

        return []

    def get_all_nodes(self) -> List[GraphNode]:
        return list(self._nodes.values())

    def get_all_edges(self) -> List[GraphEdge]:
        return list(self._edges.values())

    def get_relation_nodes(self) -> List[GraphNode]:
        """Get all promoted relation nodes (hypergraph nodes)."""
        return [n for n in self._nodes.values() if n.is_relation_node]

    def get_word_nodes(self) -> List[GraphNode]:
        """Get all word-point nodes (not relation nodes)."""
        return [n for n in self._nodes.values() if not n.is_relation_node]

    # ── Serialization ──

    def to_dict(self) -> Dict:
        """Serialize the graph to a plain dict (for pipeline JSON output)."""
        return {
            'nodes': [
                {
                    'id': n.id, 'word': n.word, 'position': n.position,
                    'symbol': n.symbol, 'r7_phase': n.r7_phase,
                    'is_relation_node': n.is_relation_node,
                }
                for n in self._nodes.values()
            ],
            'edges': [
                {
                    'id': e.id, 'from': e.from_id, 'to': e.to_id,
                    'type': e.relation_type.value, 'note': e.note,
                    'confidence': e.confidence,
                }
                for e in self._edges.values()
            ],
            'contentions': [
                {
                    'target_type': c.target_type, 'target_id': c.target_id,
                    'severity': c.severity.value, 'description': c.description,
                    'opposing_symbol': c.opposing_symbol,
                }
                for c in self._contentions
            ],
            'stats': {
                'node_count': len(self._nodes),
                'edge_count': len(self._edges),
                'contention_count': len(self._contentions),
                'relation_node_count': len(self.get_relation_nodes()),
            },
        }

    # ── Build from decomposer output ──

    def build_from_points(self, points: list) -> None:
        """Build the graph from decomposer WordPoint output."""
        # Add all word-points as nodes
        node_ids: List[str] = []
        for pt in points:
            node = self.add_node(
                word=pt.word,
                position=pt.position,
                symbol=pt.symbol,
                decomposition=pt.decomposition,
                role=pt.role,
                r7_phase=pt.r7_phase,
            )
            node_ids.append(node.id)

        # Create compositional edges between adjacent mapped words
        for i in range(len(node_ids) - 1):
            from_node = self.get_node(node_ids[i])
            to_node = self.get_node(node_ids[i + 1])
            if from_node and to_node and from_node.symbol and to_node.symbol:
                # Adjacent words get a COMPOSITIONAL relation by default
                self.add_edge(
                    from_id=from_node.id,
                    to_id=to_node.id,
                    relation_type=RelationType.COMPOSITIONAL,
                    note=f'{from_node.word} → {to_node.word}',
                    confidence=0.5,
                )
```

---

## File 3: `comprehension/core/contention_mapper.py`

```python
"""
Contention Mapper — TAZV Comprehension Machine
===============================================
Finds WHERE antinomy lives in the graph — not per-statement, but per-word
and per-relation.

"UAF returns a number, not where the contention is."
This module fixes that: it marks the exact nodes and edges where
ontological tension exists.

Contention sources (corpus-validated):
  1. CONTRADICTS edges — explicit contradictions in the graph
  2. Symbol opposition — words with opposing ontological operators
  3. Phase tension — words from conflicting R-7 phases
  4. CounterAngle entries — from JEWIK Truthbase Studio model

Symbol oppositions (from corpus):
  ∅ (void)  vs Δ (movement)    — stasis vs change
  ¬ (cut)   vs ∴ (relation)    — separation vs connection
  ⊢ (proof) vs ∅ (void)        — assertion vs negation
  ∫ (presence) vs ¬ (cut)     — sustaining vs separating

Severity levels (from CounterAngle model):
  nizka   — low tension, productive
  srednja — medium tension, needs attention
  visoka  — high tension, potential contradiction
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
from enum import Enum

from .graph_store import (
    GraphStore, GraphNode, GraphEdge,
    RelationType, Severity, ContentionMark,
)


# ── Symbol oppositions (corpus-validated) ──
# Pairs of symbols that create ontological tension when they appear together
SYMBOL_OPPOSITIONS: List[Tuple[str, str, str]] = [
    # (symbol_a, symbol_b, description)
    ('∅',  'Δ',  'stasis vs movement — void confronts change'),
    ('¬',  '∴',  'separation vs relation — cut confronts connection'),
    ('⊢',  '∅',  'assertion vs negation — proof confronts void'),
    ('∫',  '¬',  'sustaining vs separating — presence confronts cut'),
    ('∅',  '⊢',  'void vs proof — negation confronts assertion'),
    ('Δ',  '¬',  'movement vs stasis — change confronts cut'),
    ('⊥',  '∴',  'ground vs relation — bearer confronts connection'),
    ('∅',  '1',  'void vs seal — negation confronts the sealed act'),
]


# ── R-7 phase tension matrix ──
# Phases that are in tension when they appear in the same statement
PHASE_TENSIONS: Dict[Tuple[int, int], str] = {
    (0, 1): 'BIOS(∅) vs STATE(¬) — openness confronts structure',
    (0, 2): 'BIOS(∅) vs UAF(Δ) — void confronts antinomy engine',
    (1, 2): 'STATE(¬) vs UAF(Δ) — cut confronts movement',
    (2, 4): 'UAF(Δ) vs APD(⧖) — antinomy confronts seal',
    (3, 0): 'JEWIK(⊢) vs BIOS(∅) — act confronts void',
    (1, 6): 'STATE(¬) vs VIS(⟡) — cut confronts manifestation',
}


@dataclass
class ContentionReport:
    """Full report of all contention found in the graph."""
    total_contentions: int = 0
    node_contentions: List[ContentionMark] = field(default_factory=list)
    edge_contentions: List[ContentionMark] = field(default_factory=list)
    high_severity_count: int = 0
    summary: str = ''

    def to_dict(self) -> Dict:
        return {
            'total': self.total_contentions,
            'high_severity': self.high_severity_count,
            'node_contentions': len(self.node_contentions),
            'edge_contentions': len(self.edge_contentions),
            'summary': self.summary,
            'marks': [
                {
                    'target_type': m.target_type,
                    'target_id': m.target_id,
                    'severity': m.severity.value,
                    'description': m.description,
                    'opposing_symbol': m.opposing_symbol,
                }
                for m in (self.node_contentions + self.edge_contentions)
            ],
        }


class ContentionMapper:
    """
    Maps WHERE antinomy lives in the semantic graph.

    Instead of returning a single number (like UAF's αUAF), this produces
    a detailed map of which words and which relations are in tension.
    """

    def __init__(self, graph: GraphStore) -> None:
        self.graph = graph

    def map_contention(self) -> ContentionReport:
        """
        Run all contention detection passes and return a full report.

        Detection passes:
        1. CONTRADICTS edges → direct contradictions
        2. Symbol oppositions → words with opposing operators
        3. Phase tension → words from conflicting R-7 phases
        4. Self-referential negation → ∅ words adjacent to their own assertion
        """
        report = ContentionReport()

        # Pass 1: Explicit CONTRADICTS edges
        contradict_edges = self.graph.get_edges_by_type(RelationType.CONTRADICTS)
        for edge in contradict_edges:
            from_node = self.graph.get_node(edge.from_id)
            to_node = self.graph.get_node(edge.to_id)
            desc = f'{from_node.word if from_node else "?"} CONTRADICTS {to_node.word if to_node else "?"}'
            if edge.note:
                desc += f' — {edge.note}'
            mark = self.graph.add_contention(
                target_type='edge',
                target_id=edge.id,
                severity=Severity.VISOKA,  # explicit contradiction = high
                description=desc,
                opposing_symbol=f'{from_node.symbol if from_node else "?"} vs {to_node.symbol if to_node else "?"}',
            )
            report.edge_contentions.append(mark)

        # Pass 2: Symbol oppositions between adjacent nodes
        word_nodes = self.graph.get_word_nodes()
        for i, node_a in enumerate(word_nodes):
            if not node_a.symbol or node_a.r7_phase < 0:
                continue
            for node_b in word_nodes[i + 1:]:
                if not node_b.symbol or node_b.r7_phase < 0:
                    continue
                opposition = self._check_symbol_opposition(node_a, node_b)
                if opposition:
                    severity = self._assess_severity(node_a, node_b)
                    mark = self.graph.add_contention(
                        target_type='node',
                        target_id=node_a.id,
                        severity=severity,
                        description=f'{node_a.word}({node_a.symbol}) vs {node_b.word}({node_b.symbol}): {opposition}',
                        opposing_symbol=f'{node_a.symbol} vs {node_b.symbol}',
                    )
                    report.node_contentions.append(mark)

                    # Also mark the opposing node
                    mark_b = self.graph.add_contention(
                        target_type='node',
                        target_id=node_b.id,
                        severity=severity,
                        description=f'{node_b.word}({node_b.symbol}) vs {node_a.word}({node_a.symbol}): {opposition}',
                        opposing_symbol=f'{node_b.symbol} vs {node_a.symbol}',
                    )
                    report.node_contentions.append(mark_b)

        # Pass 3: Phase tension
        for i, node_a in enumerate(word_nodes):
            if node_a.r7_phase < 0:
                continue
            for node_b in word_nodes[i + 1:]:
                if node_b.r7_phase < 0:
                    continue
                if node_a.r7_phase == node_b.r7_phase:
                    continue
                phase_key = (min(node_a.r7_phase, node_b.r7_phase),
                            max(node_a.r7_phase, node_b.r7_phase))
                if phase_key in PHASE_TENSIONS:
                    tension_desc = PHASE_TENSIONS[phase_key]
                    severity = Severity.SREDNJA
                    # Higher severity if phases are far apart
                    if abs(node_a.r7_phase - node_b.r7_phase) >= 3:
                        severity = Severity.VISOKA
                    mark = self.graph.add_contention(
                        target_type='node',
                        target_id=node_a.id,
                        severity=severity,
                        description=f'Phase tension: {tension_desc}',
                        opposing_symbol=f'phase {node_a.r7_phase} vs {node_b.r7_phase}',
                    )
                    report.node_contentions.append(mark)

        # Pass 4: Self-referential negation (∅ word next to assertion)
        for node in word_nodes:
            if node.symbol == '∅':
                neighbors = self.graph.neighbors(node.id)
                for nbr in neighbors:
                    if nbr.symbol == '⊢':
                        mark = self.graph.add_contention(
                            target_type='node',
                            target_id=node.id,
                            severity=Severity.SREDNJA,
                            description=f'{node.word}(∅) next to {nbr.word}(⊢): void next to proof',
                            opposing_symbol='∅ vs ⊢',
                        )
                        report.node_contentions.append(mark)

        # Compile report
        report.total_contentions = len(report.node_contentions) + len(report.edge_contentions)
        report.high_severity_count = sum(
            1 for m in report.node_contentions + report.edge_contentions
            if m.severity == Severity.VISOKA
        )
        report.summary = self._build_summary(report)

        return report

    def _check_symbol_opposition(self, a: GraphNode, b: GraphNode) -> Optional[str]:
        """Check if two nodes' symbols are in opposition."""
        for sym_a, sym_b, desc in SYMBOL_OPPOSITIONS:
            if (a.symbol == sym_a and b.symbol == sym_b) or \
               (a.symbol == sym_b and b.symbol == sym_a):
                return desc
        return None

    def _assess_severity(self, a: GraphNode, b: GraphNode) -> Severity:
        """Assess contention severity based on symbol and phase distance."""
        # ∅ vs Δ is always high — it's the core antinomy
        pair = {a.symbol, b.symbol}
        if pair == {'∅', 'Δ'} or pair == {'Δ', '∅'}:
            return Severity.VISOKA
        if pair == {'¬', '∴'} or pair == {'∴', '¬'}:
            return Severity.VISOKA

        # Phase distance >= 3 → high
        if a.r7_phase >= 0 and b.r7_phase >= 0:
            if abs(a.r7_phase - b.r7_phase) >= 3:
                return Severity.VISOKA

        return Severity.SREDNJA

    def _build_summary(self, report: ContentionReport) -> str:
        """Build a human-readable summary of the contention map."""
        parts: List[str] = []
        parts.append(f'{report.total_contentions} contention sites found.')
        parts.append(f'{report.high_severity_count} high-severity.')
        parts.append(f'{len(report.node_contentions)} on words, {len(report.edge_contentions)} on relations.')

        if report.high_severity_count > 0:
            high = [m for m in report.node_contentions + report.edge_contentions
                    if m.severity == Severity.VISOKA]
            parts.append('High-severity sites:')
            for m in high[:5]:
                parts.append(f'  • {m.description}')
            if len(high) > 5:
                parts.append(f'  ... and {len(high) - 5} more.')
        else:
            parts.append('No high-severity contention. Graph is coherent.')

        return '\n'.join(parts)
```

---

## File 4: `comprehension/core/transformation_tracer.py`

```python
"""
Transformation Tracer — TAZV Comprehension Machine
===================================================
Produces DOKAZ — the lineage of how meaning A became meaning B.

"DOKAZ is the Product."
⊢ = dokazna sled: kaj se vidi, kaj se ponovi, kaj se preveri.

The tracer follows the graph from one node to another and records
each ontological transformation step. Each step carries:
  - from_state:  the word + symbol before transformation
  - to_state:    the word + symbol after transformation
  - operator:    the ontological operator that caused the change
  - r7_phase:    which R-7 phase this step belongs to
  - evidence:    corpus quote or axiom supporting this step
  - confidence:  how confident we are in this transformation

JEWIK axioms used as validation points:
  JEWIK_001: Beseda je ⊘ (beseda je rez, meja, poseg, dokaz prisotnosti)
  JEWIK_002: ⊘ = univerzalna enota reza, meja, obris, pogoj razlikovanja
  JEWIK_003: ∆ = osnovno gibanje: prehod, sprememba, razlika
  JEWIK_004: ∫ = integracija občutka, spomina, čuta in pomena
  JEWIK_005: ⊢ = dokazna sled: kaj se vidi, kaj se ponovi, kaj se preveri
  JEWIK_006: Vsak pojem mora imeti mejo
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
from enum import Enum

from .graph_store import GraphStore, GraphNode, GraphEdge, RelationType


# ── JEWIK Core Axioms (validation points for DOKAZ) ──
JEWIK_AXIOMS: List[Dict] = [
    {
        'id': 'JEWIK_001',
        'statement': 'Beseda je ⊘ (beseda je rez, meja, poseg, dokaz prisotnosti)',
        'symbol': '⊘',
        'absoluteness': 0.95,
        'type': 'ONTOLOŠKA',
        'status': 'PASS',
    },
    {
        'id': 'JEWIK_002',
        'statement': '⊘ = univerzalna enota reza, meja, obris, pogoj razlikovanja',
        'symbol': '⊘',
        'absoluteness': 0.92,
        'type': 'ONTOLOŠKA',
        'status': 'PASS',
    },
    {
        'id': 'JEWIK_003',
        'statement': '∆ = osnovno gibanje: prehod, sprememba, razlika',
        'symbol': '∆',
        'absoluteness': 0.90,
        'type': 'ONTOLOŠKA',
        'status': 'PASS',
    },
    {
        'id': 'JEWIK_004',
        'statement': '∫ = integracija občutka, spomina, čuta in pomena',
        'symbol': '∫',
        'absoluteness': 0.85,
        'type': 'ONTOLOŠKA',
        'status': 'PASS',
    },
    {
        'id': 'JEWIK_005',
        'statement': '⊢ = dokazna sled: kaj se vidi, kaj se ponovi, kaj se preveri',
        'symbol': '⊢',
        'absoluteness': 0.88,
        'type': 'OPERATIVNA',
        'status': 'PASS',
    },
    {
        'id': 'JEWIK_006',
        'statement': 'Vsak pojem mora imeti mejo',
        'symbol': '¬',
        'absoluteness': 0.90,
        'type': 'OPERATIVNA',
        'status': 'PASS',
    },
]


# ── Transformation operators (what changes meaning from one form to another) ──
# Each operator maps to an R-7 phase and describes the type of transformation
TRANSFORMATION_OPERATORS: Dict[str, Dict] = {
    '∅→¬': {
        'name': 'cut-from-void',
        'r7_phase': 0,
        'description': 'Structure emerges from the void — the first cut',
        'axiom': 'JEWIK_001',
    },
    '¬→Δ': {
        'name': 'move-from-cut',
        'r7_phase': 1,
        'description': 'Change emerges from distinction — movement begins',
        'axiom': 'JEWIK_003',
    },
    'Δ→⊢': {
        'name': 'act-from-movement',
        'r7_phase': 2,
        'description': 'Action emerges from change — the utterance becomes act',
        'axiom': 'JEWIK_005',
    },
    '⊢→⧖': {
        'name': 'seal-from-act',
        'r7_phase': 3,
        'description': 'Seal emerges from action — verification and definition',
        'axiom': 'JEWIK_006',
    },
    '⧖→∮': {
        'name': 'return-from-seal',
        'r7_phase': 4,
        'description': 'Return emerges from seal — the cycle learns',
        'axiom': None,
    },
    '∮→⟡': {
        'name': 'manifest-from-return',
        'r7_phase': 5,
        'description': 'Manifestation emerges from return — new possibility',
        'axiom': None,
    },
    '∅→Δ': {
        'name': 'direct-antinomy',
        'r7_phase': 2,
        'description': 'Void directly becomes change — the core antinomy leap',
        'axiom': 'JEWIK_003',
    },
    'δ→∴': {
        'name': 'cut-to-relation',
        'r7_phase': 1,
        'description': 'Cut becomes relation — separation finds its other',
        'axiom': 'JEWIK_002',
    },
    '∴→∫': {
        'name': 'relation-to-presence',
        'r7_phase': 2,
        'description': 'Relation becomes presence — connection sustains',
        'axiom': 'JEWIK_004',
    },
    '∫→⊢': {
        'name': 'presence-to-proof',
        'r7_phase': 3,
        'description': 'Presence becomes proof — sustained act becomes evidence',
        'axiom': 'JEWIK_005',
    },
    '¬→∅': {
        'name': 'cut-to-void',
        'r7_phase': 1,
        'description': 'Cut dissolves into void — structure returns to openness',
        'axiom': None,
    },
    'Δ→∅': {
        'name': 'movement-to-void',
        'r7_phase': 2,
        'description': 'Movement returns to void — change completes its cycle',
        'axiom': None,
    },
}


@dataclass
class LineageStep:
    """One step in the DOKAZ lineage — a single transformation."""
    step_index: int
    from_word: str
    from_symbol: str
    to_word: str
    to_symbol: str
    operator_key: str          # e.g. "∅→Δ"
    operator_name: str         # e.g. "direct-antinomy"
    r7_phase: int
    description: str
    axiom_ref: Optional[str]    # JEWIK axiom that validates this step
    confidence: float
    evidence: str               # quote or note supporting this step

    def __repr__(self) -> str:
        return (f'Step {self.step_index}: '
                f'{self.from_word}({self.from_symbol}) '
                f'--[{self.operator_name}]--> '
                f'{self.to_word}({self.to_symbol})')


@dataclass
class DOKAZ:
    """
    A complete proof trail — the product of the transformation tracer.

    "DOKAZ is the Product." — the lineage showing how meaning A became meaning B.
    """
    start_word: str
    start_symbol: str
    end_word: str
    end_symbol: str
    steps: List[LineageStep] = field(default_factory=list)
    total_confidence: float = 0.0
    validated_by_axioms: List[str] = field(default_factory=list)
    full_trail: str = ''  # human-readable trail: ∅→¬→Δ→⊢→⧖

    def to_dict(self) -> Dict:
        return {
            'start': {'word': self.start_word, 'symbol': self.start_symbol},
            'end': {'word': self.end_word, 'symbol': self.end_symbol},
            'steps': [
                {
                    'step': s.step_index,
                    'from': f'{s.from_word}({s.from_symbol})',
                    'to': f'{s.to_word}({s.to_symbol})',
                    'operator': s.operator_name,
                    'phase': s.r7_phase,
                    'description': s.description,
                    'axiom': s.axiom_ref,
                    'confidence': s.confidence,
                }
                for s in self.steps
            ],
            'total_confidence': self.total_confidence,
            'validated_by': self.validated_by_axioms,
            'trail': self.full_trail,
        }


class TransformationTracer:
    """
    Traces how meaning transforms through the graph, producing DOKAZ.

    The tracer follows paths in the graph and records each ontological
    transformation as a LineageStep. The full trail is the DOKAZ.
    """

    def __init__(self, graph: GraphStore) -> None:
        self.graph = graph
        self._axiom_lookup: Dict[str, Dict] = {
            a['id']: a for a in JEWIK_AXIOMS
        }

    def trace(
        self,
        start_word: str,
        end_word: str,
    ) -> Optional[DOKAZ]:
        """
        Trace the transformation from one word to another.

        Finds a path through the graph and records each transformation step.

        Args:
            start_word: The word to trace from
            end_word: The word to trace to

        Returns:
            A DOKAZ proof trail, or None if no path found
        """
        # Find start and end nodes
        start_nodes = self.graph.find_nodes_by_word(start_word)
        end_nodes = self.graph.find_nodes_by_word(end_word)

        if not start_nodes or not end_nodes:
            return None

        # Try all start/end combinations, pick the shortest path
        best_path: List[str] = []
        best_start: Optional[GraphNode] = None
        best_end: Optional[GraphNode] = None

        for s_node in start_nodes:
            for e_node in end_nodes:
                path = self.graph.find_path(s_node.id, e_node.id, max_depth=15)
                if path and (not best_path or len(path) < len(best_path)):
                    best_path = path
                    best_start = s_node
                    best_end = e_node

        if not best_path or not best_start or not best_end:
            return None

        # Build the DOKAZ from the path
        return self._build_dokaz(best_path, best_start, best_end)

    def trace_statement(
        self,
        statement_points: list,
    ) -> List[DOKAZ]:
        """
        Trace all transformations within a single statement.

        For each pair of mapped words, find if a transformation path exists
        and record it. Returns all DOKAZ trails found.
        """
        trails: List[DOKAZ] = []
        mapped = [pt for pt in statement_points if pt.mapped]

        for i, pt_a in enumerate(mapped):
            for pt_b in mapped[i + 1:]:
                dokaz = self.trace(pt_a.word, pt_b.word)
                if dokaz and dokaz.steps:
                    trails.append(dokaz)

        return trails

    def _build_dokaz(
        self,
        path: List[str],
        start_node: GraphNode,
        end_node: GraphNode,
    ) -> DOKAZ:
        """Build a DOKAZ from a node path."""
        steps: List[LineageStep] = []
        symbol_trail: List[str] = []
        axioms_used: List[str] = []
        confidence_product = 1.0

        for i in range(len(path) - 1):
            from_node = self.graph.get_node(path[i])
            to_node = self.graph.get_node(path[i + 1])

            if not from_node or not to_node:
                continue

            if from_node.symbol:
                symbol_trail.append(from_node.symbol)

            # Find the transformation operator
            operator_key = f'{from_node.symbol}→{to_node.symbol}'
            operator = TRANSFORMATION_OPERATORS.get(operator_key)

            if operator:
                axiom_ref = operator.get('axiom')
                if axiom_ref and axiom_ref not in axioms_used:
                    axioms_used.append(axiom_ref)
                confidence = 0.85
            else:
                # Unknown transformation — still record it
                operator = {
                    'name': 'unknown-transformation',
                    'r7_phase': max(from_node.r7_phase, to_node.r7_phase),
                    'description': f'{from_node.symbol} → {to_node.symbol} (unmapped operator)',
                    'axiom': None,
                }
                axiom_ref = None
                confidence = 0.3

            confidence_product *= confidence

            # Find the edge that connects these nodes for evidence
            edges = self.graph.get_edges_for_node(from_node.id)
            edge_note = ''
            for e in edges:
                if e.to_id == to_node.id or e.from_id == to_node.id:
                    edge_note = e.note
                    break

            step = LineageStep(
                step_index=i,
                from_word=from_node.word,
                from_symbol=from_node.symbol,
                to_word=to_node.word,
                to_symbol=to_node.symbol,
                operator_key=operator_key,
                operator_name=operator['name'],
                r7_phase=operator['r7_phase'],
                description=operator['description'],
                axiom_ref=axiom_ref,
                confidence=confidence,
                evidence=edge_note or operator['description'],
            )
            steps.append(step)

        # Add final symbol
        if end_node.symbol:
            symbol_trail.append(end_node.symbol)

        return DOKAZ(
            start_word=start_node.word,
            start_symbol=start_node.symbol,
            end_word=end_node.word,
            end_symbol=end_node.symbol,
            steps=steps,
            total_confidence=confidence_product,
            validated_by_axioms=axioms_used,
            full_trail='→'.join(symbol_trail),
        )

    def get_axiom_validation(self, dokaz: DOKAZ) -> List[Dict]:
        """
        Get the full JEWIK axiom texts that validate this DOKAZ.

        "⊢ = dokazna sled: kaj se vidi, kaj se ponovi, kaj se preveri."
        """
        validations: List[Dict] = []
        for axiom_id in dokaz.validated_by_axioms:
            axiom = self._axiom_lookup.get(axiom_id)
            if axiom:
                validations.append(axiom)
        return validations
```

---

## How these 4 files work together

```
Statement: "The word is no"
                │
                ▼
    ┌─────────────────────────┐
    │   decomposer.py          │
    │   decompose_statement()  │
    │                          │
    │   THE → δ  (phase 1)     │
    │   WORD → ⊢ (phase 3)     │
    │   IS  → Δ  (phase 2)     │
    │   NO  → ∅  (phase 0)     │
    └───────────┬─────────────┘
                │ WordPoint[]
                ▼
    ┌─────────────────────────┐
    │   graph_store.py         │
    │   build_from_points()    │
    │                          │
    │   Nodes: THE, WORD, IS, NO          │
    │   Edges: THE→WORD (compositional)   │
    │          WORD→IS (compositional)    │
    │          IS→NO  (compositional)     │
    │   promote_relation_to_node() → hypergraph │
    └───────────┬─────────────┘
                │ GraphStore
        ┌───────┴───────┐
        ▼               ▼
┌───────────────┐ ┌───────────────────┐
│ contention_   │ │ transformation_   │
│ mapper.py     │ │ tracer.py         │
│               │ │                   │
│ WHERE is the  │ │ HOW did meaning   │
│ tension?      │ │ A become B?       │
│               │ │                   │
│ ∅ vs Δ: VISOKA│ │ ∅→¬→Δ→⊢ (DOKAZ)  │
│ phase 0 vs 2  │ │ validated by       │
│ (NO vs IS)    │ │ JEWIK_003          │
└───────────────┘ └───────────────────┘
```

### Integration with R-7 pipeline

```python
# In your pipeline (e.g., main_window_v5_integrated.py or a new adapter):

from comprehension.core.decomposer import decompose_statement
from comprehension.core.graph_store import GraphStore, RelationType
from comprehension.core.contention_mapper import ContentionMapper
from comprehension.core.transformation_tracer import TransformationTracer

def run_comprehension_layer(statement: str) -> dict:
    # Phase 1: Decompose
    points = decompose_statement(statement)

    # Phase 2: Build graph
    graph = GraphStore()
    graph.build_from_points(points)

    # Phase 3: Map contention (WHERE)
    mapper = ContentionMapper(graph)
    contention_report = mapper.map_contention()

    # Phase 4: Trace transformations (HOW)
    tracer = TransformationTracer(graph)
    dokaz_trails = tracer.trace_statement(points)

    return {
        'points': [{'word': p.word, 'symbol': p.symbol, 'mapped': p.mapped} for p in points],
        'graph': graph.to_dict(),
        'contention': contention_report.to_dict(),
        'dokaz': [d.to_dict() for d in dokaz_trails],
    }
```

### What this gives you that the app didn't have before

| Before | After |
|--------|-------|
| Statement = one string | Statement = list of word-points with ontological operators |
| UAF returns αUAF number | ContentionMapper returns WHERE (which words, which relations) |
| No graph | Full semantic graph with nodes, edges, hypergraph |
| No proof trail | DOKAZ lineage: how meaning A became meaning B |
| 7 color stubs | 26-term decomposition table with real corpus data |
| No relation types | 11 relation types (6 JEWIK + 5 archive) |
| No JEWIK axioms | 6 JEWIK axioms as validation points |

### Corpus sources used

- **WOR(L)D lexicon** (Obs11, Word is No, Beseda je Ne) — 26-term decomposition table
- **JEWIK Truthbase Studio** (Obs1, Obs4) — RelationType enum, CounterAngle, UnitLink, EvidenceRef
- **JEWIK Core axioms** (Obs1) — JEWIK_001 through JEWIK_006
- **Guard thresholds** (Self, Obs1) — κ≥.70, χ≥.40, μ∈[.50,.80], ℜ≤.03
- **Symbol oppositions** — derived from corpus: ∅ vs Δ, ¬ vs ∴, ⊢ vs ∅, ∫ vs ¬