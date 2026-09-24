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
from typing import List, Optional, Dict
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
