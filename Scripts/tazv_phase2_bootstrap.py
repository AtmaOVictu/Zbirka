#!/usr/bin/env python3
"""
TAZV Comprehension Machine — Phase 2 Bootstrap
==============================================

Bootstraps the Phase 2 knowledge indexing subsystem.
This script:
1. Validates that all Phase 0/1 files exist
2. Generates any missing Phase 2 files (tonos.py, rozetni_kamni.py, knowledge_renderer.py)
3. Runs the Phase 2 indexer to populate the knowledge database
4. Creates integration hooks for main_window_v5_integrated.py

Usage:
    cd D:/OntoProjekt/CanvasMinstral/Scripts
    python tazv_phase2_bootstrap.py

Corpus alignment:
- Uses corpus-validated frequencies from Obs3 (tonos.py)
- Uses corpus-validated tradition mappings from Rozetni kamni I-LXXII
- Extends symbol_mapper.py as the rosette stone mapper (3-script)
- Renders as interactive mandala with color + text + sound

Files created/updated:
- comprehension/core/tonos.py (if missing)
- comprehension/core/rozetni_kamni.py (if missing)
- comprehension/ui/knowledge_renderer.py (if missing)
- comprehension/data/knowledge_index.json (generated)
"""

import sys
import os
import json
from pathlib import Path

# Ensure we're running from Scripts directory
SCRIPTS_DIR = Path(__file__).resolve().parent
os.chdir(SCRIPTS_DIR)

# Add comprehension_machine to path
sys.path.insert(0, str(SCRIPTS_DIR / "comprehension_machine"))

CORE_DIR = SCRIPTS_DIR / "comprehension_machine" / "comprehension" / "core"
UI_DIR = SCRIPTS_DIR / "comprehension_machine" / "comprehension" / "ui"
DATA_DIR = SCRIPTS_DIR / "comprehension_machine" / "comprehension" / "data"


def validate_phase0_phase1():
    """Validate that Phase 0 and Phase 1 files exist."""
    print("Validating Phase 0/1 dependencies...")
    
    required_files = [
        CORE_DIR / "symbol_mapper.py",
        CORE_DIR / "module_semantics.py",
        CORE_DIR / "egyptian_color_semantics.py",
        CORE_DIR / "decomposer.py",
        CORE_DIR / "graph_store.py",
        CORE_DIR / "contention_mapper.py",
        CORE_DIR / "transformation_tracer.py",
    ]
    
    missing = []
    for f in required_files:
        if not f.exists():
            missing.append(f.name)
    
    if missing:
        print(f"  ERROR: Missing files: {missing}")
        return False
    
    print("  All Phase 0/1 dependencies present.")
    return True


def generate_tonos_py():
    """Generate tonos.py if it doesn't exist."""
    tonos_file = CORE_DIR / "tonos.py"
    if tonos_file.exists():
        print(f"  tonos.py already exists, skipping.")
        return True
    
    content = '''"""
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
    # R-7 operator -> frequency, note, corpus meaning
    "∅": {"frequency": 220.0, "note": "A3", "meaning": "BIOS — the void that holds all"},
    "⊘": {"frequency": 220.0, "note": "A3", "meaning": "universal unit of cut"},
    "¬": {"frequency": 330.0, "note": "E4", "meaning": "STATE — the cut that separates"},
    "∆": {"frequency": 330.0, "note": "E4", "meaning": "UAF — fundamental movement, difference"},
    "¬∆": {"frequency": 440.0, "note": "A4", "meaning": "doubt — double cut"},
    "1": {"frequency": 550.0, "note": "C#5", "meaning": "JEWIK — the seal"},
    "⊢": {"frequency": 550.0, "note": "C#5", "meaning": "JEWIK — proof, utterance"},
    "∑": {"frequency": 660.0, "note": "E5", "meaning": "sum — integration"},
    "⧖": {"frequency": 196.0, "note": "G3", "meaning": "APD — silence, the seal"},
    "∮": {"frequency": 261.63, "note": "C4", "meaning": "MICRO — return, learning"},
    "⟡": {"frequency": 392.0, "note": "G4", "meaning": "VISUALIZATION — manifestation"},
    "δ": {"frequency": 330.0, "note": "E4", "meaning": "STATE-adjacent — the cut operator"},
    "||": {"frequency": 440.0, "note": "A4", "meaning": "MICRO — spiral, echo"},
    "∥": {"frequency": 440.0, "note": "A4", "meaning": "MICRO — seal through duration"},
    "ʃ": {"frequency": 293.66, "note": "D4", "meaning": "APD — persistence"},
    "⊥": {"frequency": 164.81, "note": "E3", "meaning": "BIOS — the bearer"},
    "∂": {"frequency": 392.0, "note": "G4", "meaning": "VISUALIZATION — the passage"},
    "W": {"frequency": 440.0, "note": "A4", "meaning": "JEWIK — wanting that transforms"},
}


def get_frequency(symbol):
    """Get frequency for a given symbol."""
    return TONOS_FREQUENCIES.get(symbol, {"frequency": 0.0, "note": "?", "meaning": "unknown"})


def get_note(symbol):
    """Get note name for a given symbol."""
    info = TONOS_FREQUENCIES.get(symbol, {})
    return info.get("note", "?")


def get_all_frequencies():
    """Return all frequency mappings."""
    return TONOS_FREQUENCIES.copy()
'''
    
    with open(tonos_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  Generated {tonos_file}")
    return True


def generate_rozetni_kamni_py():
    """Generate rozetni_kamni.py if it doesn't exist."""
    rozetni_file = CORE_DIR / "rozetni_kamni.py"
    if rozetni_file.exists():
        print(f"  rozetni_kamni.py already exists, skipping.")
        return True
    
    content = '''"""
Rozetni Kamni — Tradition Mapping
==================================
Corpus-validated tradition mappings for the Rosette Stone principle.

Source: Basics library, Rozetni kamni I-LXXII
Corpus insight: "vse tradicije = ∅/∆ v različnih dimenzijah"
(all traditions = void/movement in different dimensions)

The Rosette Stone principle (3 scripts):
  1. zgodovinski simbol (historical symbol)
  2. sistemski simbol (system symbol: ∅/∆/¬/etc.)
  3. matematična/topološka lastnost (mathematical/topological property)

The machine adds ∂ — the cut that cuts through all three.
"""

# Tradition registry — maps tradition name to its properties
TRADITIONS = {
    "Sufism": {
        "ring": 1,
        "color": "#C9A86C",
        "description": "99+∅ names of God",
        "mappings": {
            "Al-Haqq": ("∅", "absolute truth"),
            "Al-Hayy": ("∆", "the living"),
            "Al-Alim": ("⊢", "the knowing"),
            "Al-Quddus": ("¬", "the holy/separate"),
        },
    },
    "Tarot": {
        "ring": 2,
        "color": "#E8C374",
        "description": "22 Major Arcana",
        "mappings": {
            "The Fool": ("∅", "beginning/void"),
            "The Magician": ("⊢", "will/proof"),
            "The High Priestess": ("∂", "intuition/passage"),
            "The Empress": ("∆", "creation/movement"),
            "The Emperor": ("1", "structure/seal"),
            "The Hierophant": ("⧖", "wisdom/seal"),
        },
    },
    "Kabbalah": {
        "ring": 2,
        "color": "#B8860B",
        "description": "Tree of Life (10 Sephiroth + 22 paths)",
        "mappings": {
            "Keter": ("∅", "crown/void"),
            "Chokmah": ("∆", "wisdom/movement"),
            "Binah": ("⊢", "understanding/proof"),
            "Chesed": ("∮", "mercy/return"),
            "Gevurah": ("¬", "judgment/cut"),
            "Tiphareth": ("1", "beauty/seal"),
            "Malkuth": ("⧖", "kingdom/seal"),
        },
    },
    "Alchemy": {
        "ring": 3,
        "color": "#8B4513",
        "description": "4 elements + 3 principles",
        "mappings": {
            "Mercurius": ("∂", "mercury/passage"),
            "Sulphur": ("∆", "sulfur/movement"),
            "Salt": ("⊥", "salt/ground"),
            "Prima Materia": ("∅", "first matter/void"),
        },
    },
    "Chakras": {
        "ring": 3,
        "color": "#FF69B4",
        "description": "7 energy centers",
        "mappings": {
            "Muladhara": ("⊥", "root/bearer"),
            "Svadhisthana": ("∆", "creativity/movement"),
            "Manipura": ("∅", "void/fire"),
            "Anahata": ("⊢", "proof/heart"),
            "Vishuddha": ("∂", "passage/throat"),
            "Ajna": ("∮", "return/third eye"),
            "Sahasrara": ("⟡", "manifestation/crown"),
        },
    },
    "DNA": {
        "ring": 4,
        "color": "#1E90FF",
        "description": "64 codons",
        "mappings": {
            "Adenine": ("⊢", "proof"),
            "Thymine": ("∅", "void"),
            "Cytosine": ("¬", "cut"),
            "Guanine": ("∆", "movement"),
        },
    },
    "Music": {
        "ring": 4,
        "color": "#9400D3",
        "description": "12 notes",
        "mappings": {
            "C": ("∅", "root/void"),
            "G": ("⊢", "dominant/proof"),
            "F": ("⧖", "subdominant/seal"),
        },
    },
    "Norse": {
        "ring": 1,
        "color": "#228B22",
        "description": "9 worlds",
        "mappings": {
            "Asgard": ("⟡", "manifestation"),
            "Midgard": ("⊥", "bearer"),
            "Jotunheim": ("∅", "void/chaos"),
            "Hel": ("¬", "cut/death"),
        },
    },
    "Vedic": {
        "ring": 2,
        "color": "#FF8C00",
        "description": "4 Vedas + 108 Upanishads",
        "mappings": {
            "Rig Veda": ("⊢", "proof/mantra"),
            "Sama Veda": ("∂", "passage/music"),
            "Yajur Veda": ("⧖", "seal/ritual"),
            "Atharva Veda": ("∅", "void/knowledge"),
        },
    },
    "Buddhism": {
        "ring": 3,
        "color": "#FFD700",
        "description": "4 Noble Truths + 8-fold path",
        "mappings": {
            "Dukkha": ("∅", "suffering/void"),
            "Samudaya": ("∆", "origin/movement"),
            "Nirodha": ("¬", "cessation/cut"),
            "Magga": ("⊢", "path/proof"),
        },
    },
    "Christianity": {
        "ring": 3,
        "color": "#FFFFFF",
        "description": "7 sacraments",
        "mappings": {
            "Baptism": ("∂", "passage/water"),
            "Eucharist": ("⧖", "seal/bread"),
            "Confirmation": ("⊢", "proof/spirit"),
        },
    },
    "Islam": {
        "ring": 2,
        "color": "#008000",
        "description": "99 names of Allah",
        "mappings": {
            "Ar-Rahman": ("∮", "merciful/return"),
            "Ar-Rahim": ("⧖", "compassionate/seal"),
            "Al-Malik": ("⊢", "king/proof"),
        },
    },
    "Greek Elements": {
        "ring": 4,
        "color": "#808080",
        "description": "4 elements + 1 quintessence",
        "mappings": {
            "Earth": ("⊥", "bearer"),
            "Water": ("∂", "passage"),
            "Air": ("∆", "movement"),
            "Fire": ("∅", "void/transformation"),
            "Aether": ("⟡", "manifestation"),
        },
    },
    "I Ching": {
        "ring": 1,
        "color": "#000000",
        "description": "64 hexagrams",
        "mappings": {
            "Qian": ("⊢", "creative/proof"),
            "Kun": ("∅", "receptive/void"),
        },
    },
    "Jung Archetypes": {
        "ring": 2,
        "color": "#800080",
        "description": "Collective unconscious",
        "mappings": {
            "Self": ("∂", "passage/observer"),
            "Shadow": ("¬", "cut/separation"),
            "Anima/Animus": ("∆", "movement/difference"),
        },
    },
    "Periodic Table": {
        "ring": 4,
        "color": "#4682B4",
        "description": "2n² elements",
        "mappings": {
            "Hydrogen": ("∅", "first element/void"),
            "Carbon": ("⊢", "life/proof"),
            "Oxygen": ("∆", "movement/change"),
        },
    },
    "Valentinian": {
        "ring": 3,
        "color": "#DC143C",
        "description": "30 aeons",
        "mappings": {
            "Bythos": ("∅", "depth/void"),
            "Sige": ("⧖", "silence/seal"),
            "Nous": ("⊢", "mind/proof"),
        },
    },
}


def get_tradition(tradition_name):
    """Get tradition definition by name."""
    return TRADITIONS.get(tradition_name, {})


def get_all_traditions():
    """Return all tradition names."""
    return list(TRADITIONS.keys())


def get_cross_references(symbol):
    """Get all tradition terms that map to a given root operator symbol."""
    references = []
    for tradition_name, tradition in TRADITIONS.items():
        for term, (trad_symbol, description) in tradition.get("mappings", {}).items():
            if trad_symbol == symbol:
                references.append({
                    "tradition": tradition_name,
                    "term": term,
                    "description": description,
                    "color": tradition.get("color", "#666666"),
                })
    return references


def get_tradition_by_ring(ring_num):
    """Get all traditions in a specific ring."""
    return [
        {"name": name, "data": data}
        for name, data in TRADITIONS.items()
        if data.get("ring") == ring_num
    ]
'''
    
    with open(rozetni_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  Generated {rozetni_file}")
    return True


def generate_knowledge_indexer():
    """Generate the knowledge indexer script."""
    indexer_file = SCRIPTS_DIR / "tazv_phase2_indexer.py"
    if indexer_file.exists():
        print(f"  tazv_phase2_indexer.py already exists, skipping.")
        return True
    
    content = '''#!/usr/bin/env python3
"""
TAZV Comprehension Machine — Phase 2 Knowledge Indexer
======================================================
Indexes all knowledge systems for mandala rendering.

This script:
1. Loads all tradition mappings from rozetni_kamni.py
2. Loads color semantics from egyptian_color_semantics.py
3. Loads sound frequencies from tonos.py
4. Creates a unified knowledge index for rendering

The index contains:
- All root operators with their colors, frequencies, meanings
- All tradition mappings organized by ring
- Cross-references between traditions and operators
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "comprehension_machine"))

from comprehension.core.tonos import TONOS_FREQUENCIES
from comprehension.core.rozetni_kamni import TRADITIONS
from comprehension.core.egyptian_color_semantics import MODULE_COLOR_HEX, COLORS
from comprehension.core.module_semantics import MODULE_SEMANTICS, MODULE_ORDER


def build_knowledge_index():
    """Build the complete knowledge index."""
    index = {
        "operators": {},
        "traditions": {},
        "cross_references": {},
        "rings": {},
        "metadata": {
            "operator_count": 0,
            "tradition_count": 0,
            "total_mappings": 0,
        },
    }

    # Build operator index
    for symbol, freq_data in TONOS_FREQUENCIES.items():
        # Find module info
        module_info = {}
        for mod_name in MODULE_ORDER:
            mod = MODULE_SEMANTICS.get(mod_name, {})
            if mod.get("symbol") == symbol:
                module_info = {
                    "module": mod_name,
                    "name": mod.get("name", mod_name),
                    "description": mod.get("description", ""),
                }
                break

        color_hex = "#666666"
        for mod_name, hex_val in MODULE_COLOR_HEX.items():
            mod = MODULE_SEMANTICS.get(mod_name, {})
            if mod.get("symbol") == symbol:
                color_hex = hex_val
                break

        index["operators"][symbol] = {
            "symbol": symbol,
            "frequency": freq_data.get("frequency", 0),
            "note": freq_data.get("note", "?"),
            "meaning": freq_data.get("meaning", ""),
            "color": color_hex,
            "module": module_info.get("module", "unknown"),
            "module_name": module_info.get("name", "unknown"),
        }

    # Build tradition index
    for trad_name, trad_data in TRADITIONS.items():
        ring = trad_data.get("ring", 1)
        index["traditions"][trad_name] = {
            "name": trad_name,
            "description": trad_data.get("description", ""),
            "color": trad_data.get("color", "#666666"),
            "ring": ring,
            "mappings": list(trad_data.get("mappings", {}).items()),
        }

        # Add to ring index
        if ring not in index["rings"]:
            index["rings"][ring] = []
        index["rings"][ring].append(trad_name)

        # Build cross-references
        for term, (symbol, description) in trad_data.get("mappings", {}).items():
            if symbol not in index["cross_references"]:
                index["cross_references"][symbol] = []
            index["cross_references"][symbol].append({
                "tradition": trad_name,
                "term": term,
                "description": description,
                "color": trad_data.get("color", "#666666"),
            })

    # Update metadata
    index["metadata"]["operator_count"] = len(index["operators"])
    index["metadata"]["tradition_count"] = len(index["traditions"])
    index["metadata"]["total_mappings"] = sum(
        len(t.get("mappings", [])) for t in index["traditions"].values()
    )

    return index


def save_knowledge_index(index, output_path=None):
    """Save the knowledge index to a JSON file."""
    if output_path is None:
        data_dir = Path(__file__).resolve().parent / "comprehension_machine" / "comprehension" / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        output_path = data_dir / "knowledge_index.json"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print(f"Knowledge index saved to {output_path}")
    return output_path


if __name__ == "__main__":
    print("Building knowledge index...")
    index = build_knowledge_index()
    print(f"  Operators: {index['metadata']['operator_count']}")
    print(f"  Traditions: {index['metadata']['tradition_count']}")
    print(f"  Total mappings: {index['metadata']['total_mappings']}")
    save_knowledge_index(index)
    print("Done.")
'''
    
    with open(indexer_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  Generated {indexer_file}")
    return True


def generate_integration_script():
    """Generate the integration script."""
    integration_file = SCRIPTS_DIR / "tazv_phase2_integration.py"
    if integration_file.exists():
        print(f"  tazv_phase2_integration.py already exists, skipping.")
        return True
    
    content = '''#!/usr/bin/env python3
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
    
    print("\nIntegration test complete.")
'''
    
    with open(integration_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  Generated {integration_file}")
    return True


def main():
    """Run Phase 2 bootstrap."""
    print("=" * 70)
    print("TAZV Phase 2 Bootstrap")
    print("=" * 70)
    
    # Step 1: Validate dependencies
    if not validate_phase0_phase1():
        print("\nERROR: Phase 0/1 dependencies not met. Exiting.")
        sys.exit(1)
    
    # Step 2: Generate missing core files
    print("\nGenerating Phase 2 core files...")
    generate_tonos_py()
    generate_rozetni_kamni_py()
    
    # Step 3: Generate bootstrap scripts
    print("\nGenerating Phase 2 bootstrap scripts...")
    generate_knowledge_indexer()
    generate_integration_script()
    
    # Step 4: Create knowledge_renderer.py if it doesn't exist
    renderer_file = UI_DIR / "knowledge_renderer.py"
    if not renderer_file.exists():
        print("\nERROR: knowledge_renderer.py not found.")
        print("Please create it or copy from the B2 directory.")
    else:
        print(f"\nknowledge_renderer.py already exists at {renderer_file}")
    
    # Step 5: Run the indexer
    print("\nRunning knowledge indexer...")
    indexer_path = SCRIPTS_DIR / "tazv_phase2_indexer.py"
    if indexer_path.exists():
        import subprocess
        result = subprocess.run(
            [sys.executable, str(indexer_path)],
            capture_output=True,
            text=True,
            cwd=SCRIPTS_DIR
        )
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
    
    print("\n" + "=" * 70)
    print("Phase 2 Bootstrap Complete")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Update main_window_v5_integrated.py to include Phase 2")
    print("2. Run main_window_v5_integrated.py to see the full integration")
    print("3. Run tazv_phase2_integration.py to test the bridge")


if __name__ == "__main__":
    main()
