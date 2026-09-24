#!/usr/bin/env python3
"""
TAZV Comprehension Machine — Phase 2 Integration
=================================================
Integrates Phase 2 components into the main pipeline.

This script provides:
1. Integration hooks for main_window_v5_integrated.py
2. Helper functions for using knowledge_renderer with the pipeline
3. Bridge between Layer 4 (comprehension) and Phase 2 (knowledge)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "comprehension_machine"))

from comprehension.core.decomposer import decompose_statement, get_symbol_sequence
from comprehension.core.graph_store import GraphStore, RelationType
from comprehension.core.contention_mapper import ContentionMapper, ContentionReport
from comprehension.core.transformation_tracer import TransformationTracer, DOKAZ
from comprehension.ui.knowledge_renderer import MandalaView, KnowledgeRenderer


class Phase2Bridge:
    """Bridge between Layer 4 comprehension and Phase 2 knowledge rendering."""

    def __init__(self):
        self.graph = None
        self.points = []
        self.contention_report = None
        self.dokaz_trails = []

    def process_statement(self, statement):
        """Run full Layer 4 pipeline on a statement."""
        # Decompose
        self.points = decompose_statement(statement)
        
        # Build graph
        self.graph = GraphStore()
        self.graph.build_from_points(self.points)
        
        # Map contention
        mapper = ContentionMapper(self.graph)
        self.contention_report = mapper.map_contention()
        
        # Trace transformations
        tracer = TransformationTracer(self.graph)
        self.dokaz_trails = tracer.trace_statement(self.points)
        
        return {
            "points": self.points,
            "graph": self.graph.to_dict(),
            "contention": self.contention_report.to_dict(),
            "dokaz": [d.to_dict() for d in self.dokaz_trails],
        }

    def get_symbol_sequence(self):
        """Get the symbol sequence from the last processed statement."""
        return get_symbol_sequence(self.points)

    def get_highest_contention_symbols(self):
        """Get symbols involved in high-severity contention."""
        if not self.contention_report:
            return []
        
        high_symbols = set()
        for mark in self.contention_report.node_contentions + self.contention_report.edge_contentions:
            if mark.severity.value == "visoka":
                if mark.opposing_symbol:
                    for sym in mark.opposing_symbol.split(" vs "):
                        high_symbols.add(sym.strip())
        
        return list(high_symbols)

    def get_dokaz_symbols(self):
        """Get all symbols involved in DOKAZ trails."""
        symbols = set()
        for trail in self.dokaz_trails:
            symbols.add(trail.start_symbol)
            symbols.add(trail.end_symbol)
            for step in trail.steps:
                symbols.add(step.from_symbol)
                symbols.add(step.to_symbol)
        
        return list(symbols)

    def get_tradition_highlights(self, symbols=None):
        """Get tradition terms that correspond to the given symbols."""
        from comprehension.core.rozetni_kamni import get_cross_references
        
        if symbols is None:
            symbols = self.get_dokaz_symbols() + self.get_highest_contention_symbols()
        
        highlights = {}
        for symbol in symbols:
            refs = get_cross_references(symbol)
            if refs:
                highlights[symbol] = refs
        
        return highlights


# Integration hooks for main_window_v5_integrated.py

def integrate_with_main_window():
    """
    Returns a dictionary of integration hooks to add to main_window_v5_integrated.py.
    
    Usage in main_window_v5_integrated.py:
        from tazv_phase2_integration import integrate_with_main_window
        
        class TazvMainWindowIntegrated(QMainWindow):
            def __init__(self):
                # ... existing code ...
                
                # Phase 2 integration
                integration_hooks = integrate_with_main_window()
                for attr_name, attr_value in integration_hooks.items():
                    setattr(self, attr_name, attr_value)
    """
    bridge = Phase2Bridge()
    
    return {
        "phase2_bridge": bridge,
        "process_with_phase2": bridge.process_statement,
        "get_tradition_highlights": bridge.get_tradition_highlights,
    }


if __name__ == "__main__":
    print("Phase 2 Integration — running test...")
    
    bridge = Phase2Bridge()
    
    # Test with a sample statement
    statement = "The word is no"
    result = bridge.process_statement(statement)
    
    print(f"Statement: {statement}")
    print(f"Symbol sequence: {bridge.get_symbol_sequence()}")
    print(f"High contention symbols: {bridge.get_highest_contention_symbols()}")
    print(f"DOKAZ symbols: {bridge.get_dokaz_symbols()}")
    print(f"Tradition highlights: {bridge.get_tradition_highlights()}")
    
    print("
Integration test complete.")
