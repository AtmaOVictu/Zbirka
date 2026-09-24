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
        return f'Node({self.word}->{self.symbol or "?"})'


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
            word=f'[{from_node.word}->{to_node.word}]',
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
                    note=f'{from_node.word} -> {to_node.word}',
                    confidence=0.5,
                )
