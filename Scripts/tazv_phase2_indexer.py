#!/usr/bin/env python3
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
