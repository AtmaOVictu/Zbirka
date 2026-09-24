#!/usr/bin/env python
"""
TAZV CanvasMinstral - Decomposer CLI
====================================
Phase 4 - Decomposer CLI

Command-line interface for decomposing statements into R-7 word-points.

Usage:
    python main_cli.py "The truth is absolute"
    python main_cli.py --statement "The truth is absolute"
    python main_cli.py --file A2/00 11 RESNICAMI.txt

Output:
    JSON with structure:
    {
        "statement": str,
        "tokens": list,
        "word_points": [
            {
                "word": str,
                "position": int,
                "symbol": str or null,
                "decomposition": str or null,
                "role": str or null,
                "r7_phase": int or -1,
                "mapped": bool
            }
        ],
        "r7_distribution": {"phase_0": count, ...},
        "warnings": list,
        "residual": list  # Unknown/unmapped words
    }

Guard Principles:
    - Unknown words return symbol: null with residual warning
    - Do NOT invent unknown mappings
    - Never modify canon
"""

import sys
import json
import argparse
from dataclasses import asdict
from typing import List, Dict, Optional

from comprehension.core.decomposer import decompose_statement, get_symbol_sequence, get_mapped_ratio
from comprehension.core.symbol_mapper import SymbolMapper


def build_r7_distribution(points: List) -> Dict[str, int]:
    """
    Build R-7 phase distribution from word points.
    
    Returns dict with keys: ∅, ¬, ∆, 1, ⧖, ∮, ⟡
    """
    # Get R7 order from SymbolMapper
    mapper = SymbolMapper()
    r7_symbols = mapper.R7_ORDER  # ["∅", "¬", "∆", "1", "⧖", "∮", "⟡"]
    
    # Initialize distribution
    distribution = {}
    for phase_idx, symbol in enumerate(r7_symbols):
        phase_key = f"phase_{phase_idx}"
        distribution[phase_key] = {
            "symbol": symbol,
            "count": 0,
            "words": []
        }
    
    # Also track unmapped
    distribution["unmapped"] = {
        "symbol": None,
        "count": 0,
        "words": []
    }
    
    # Count word points by phase
    for point in points:
        if point.mapped and point.r7_phase >= 0:
            phase_idx = point.r7_phase
            phase_key = f"phase_{phase_idx}"
            if phase_key in distribution:
                distribution[phase_key]["count"] += 1
                distribution[phase_key]["words"].append(point.word)
        else:
            distribution["unmapped"]["count"] += 1
            distribution["unmapped"]["words"].append(point.word)
    
    return distribution


def serialize_word_point(point) -> Dict:
    """
    Convert WordPoint dataclass to JSON-serializable dict.
    
    Guard: Unknown words return symbol: null
    """
    result = {
        "word": point.word,
        "position": point.position,
        "symbol": point.symbol if point.mapped else None,
        "decomposition": point.decomposition if point.mapped else None,
        "role": point.role if point.mapped else None,
        "r7_phase": point.r7_phase,
        "mapped": point.mapped
    }
    return result


def decompose_to_json(statement: str) -> Dict:
    """
    Decompose a statement and return JSON output.
    
    Args:
        statement: The text statement to decompose
    
    Returns:
        JSON-serializable dictionary with decomposition results
    """
    # Decompose the statement
    points = decompose_statement(statement)
    
    # Build symbol sequence
    symbol_sequence = get_symbol_sequence(points)
    
    # Build word points list
    word_points = [serialize_word_point(p) for p in points]
    
    # Build R7 distribution
    r7_distribution = build_r7_distribution(points)
    
    # Identify residual (unmapped words)
    residual = [
        {
            "word": p.word,
            "position": p.position,
            "warning": "Unknown ontological operator"
        }
        for p in points if not p.mapped
    ]
    
    # Build warnings
    warnings = []
    
    # Check for unknown words
    if residual:
        warnings.append(
            f"{len(residual)} unknown word(s) with no R-7 mapping: "
            f"{[r['word'] for r in residual]}"
        )
    
    # Check mapping ratio
    mapped_ratio = get_mapped_ratio(points)
    if mapped_ratio < 1.0:
        warnings.append(
            f"Only {mapped_ratio * 100:.1f}% of words have R-7 mappings"
        )
    
    # Build result
    result = {
        "statement": statement,
        "tokens": list(statement.split()) if statement else [],
        "word_points": word_points,
        "symbol_sequence": symbol_sequence,
        "r7_distribution": r7_distribution,
        "mapped_ratio": mapped_ratio,
        "warnings": warnings,
        "residual": residual
    }
    
    return result


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="TAZV CanvasMinstral - Decompose statements into R-7 word-points"
    )
    parser.add_argument(
        "statement",
        nargs="?",
        default=None,
        help="Statement to decompose (e.g., 'The truth is absolute')"
    )
    parser.add_argument(
        "--statement", "-s",
        default=None,
        help="Statement to decompose"
    )
    parser.add_argument(
        "--file", "-f",
        default=None,
        help="File to read and decompose"
    )
    parser.add_argument(
        "--pretty", "-p",
        action="store_true",
        help="Pretty-print JSON output"
    )
    parser.add_argument(
        "--compact", "-c",
        action="store_true",
        help="Compact JSON output (no whitespace)"
    )
    
    args = parser.parse_args()
    
    # Determine input
    statement = None
    if args.statement:
        statement = args.statement
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                statement = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            return 1
    elif args.statement:
        statement = args.statement
    elif len(sys.argv) > 1 and not any(arg.startswith('-') for arg in sys.argv[1:]):
        # Positional argument
        statement = sys.argv[1]
    
    if statement is None:
        print("Error: No statement or file provided", file=sys.stderr)
        print('Usage: python main_cli.py "The truth is absolute"', file=sys.stderr)
        print('       python main_cli.py --statement "The truth is absolute"', file=sys.stderr)
        print("       python main_cli.py --file A2/00 11 RESNICAMI.txt", file=sys.stderr)
        return 1
    
    # Decompose
    try:
        result = decompose_to_json(statement)
        
        # Determine JSON formatting
        if args.compact:
            indent = None
            separators = (",", ":")
        else:
            indent = 2 if args.pretty else None
            separators = (",", ": ") if args.pretty else (",", ":")
        
        # Output JSON
        json_output = json.dumps(result, indent=indent, separators=separators, ensure_ascii=False)
        print(json_output)
        
        return 0
        
    except Exception as e:
        print(f"Error during decomposition: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
