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
                parts.append(f'  * {m.description}')
            if len(high) > 5:
                parts.append(f'  ... and {len(high) - 5} more.')
        else:
            parts.append('No high-severity contention. Graph is coherent.')

        return '\n'.join(parts)
