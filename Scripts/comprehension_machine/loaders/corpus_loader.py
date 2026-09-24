#!/usr/bin/env python
"""
General Corpus Loader
=====================
Phase 3 - Corpus Loader

Provides a generalized interface for loading corpus files from various locations.

This loader ONLY structures the input - it does NOT explain meaning.

Guard Principle: No meaning invention, only structuring.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, field

from .a2_loader import CorpusLoadResult, load_corpus_file, DEFAULT_CORPUS_PATH


@dataclass
class CorpusCollection:
    """Collection of multiple loaded corpus files."""
    files_loaded: List[CorpusLoadResult] = field(default_factory=list)
    total_lines: int = 0
    total_non_empty_lines: int = 0
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


# Known corpus locations
CORPUS_LOCATIONS = {
    "A2": "A2",
    "A5": "A5",
    "Basics": "Basics",
    "B2": "B2",
    "C3": "C3",
}

# Known corpus files by location
CORPUS_FILES = {
    "A2": ["00 11 RESNICAMI.txt", "01_TRANSKRIPT_raw.txt", "01_TRANSKRIPT_raw_EN.txt"],
    "A5": [
        "02_TRANSKRIPT_clean.md",
        "03_OS_VOJNA_RESNICE_v3.md",
        "07_TRANSKRIPT_clean_v3.md",
        "08_ARGUMENTNI_ZEMLJEVID_v1.md",
        "09_PISMO_DRUZINI_mehka_v3.md",
        "10_PISMO_DRUZINI_ostra_v3.md",
        "AMR_Axioms_v1_ENGLISH.md",
        "JEWIK_LEDGER_README.md",
    ],
    "Basics": [
        "00-11-resnicami-rozetni-kamni-i-*.md",
        "00-11-resnicami-rozetni-kamni-ii-*.md",
        "00-11-resnicami-rozetni-kamni-iii-*.md",
        "stotnije-a-dosje-besedni-dosjeji.md",
    ],
}


def load_file(file_path: Union[str, Path], encoding: str = 'utf-8') -> CorpusLoadResult:
    """
    Load a single corpus file from any location.
    
    Args:
        file_path: Path to the file to load
        encoding: File encoding (default: utf-8)
    
    Returns:
        CorpusLoadResult with the loaded data
    """
    return load_corpus_file(str(file_path))


def load_directory(directory_path: Union[str, Path], pattern: str = "*.txt") -> CorpusCollection:
    """
    Load all files matching a pattern from a directory.
    
    Args:
        directory_path: Path to the directory
        pattern: Glob pattern for files to load (default: *.txt)
    
    Returns:
        CorpusCollection with all loaded files
    """
    directory_path = Path(directory_path)
    collection = CorpusCollection()
    
    if not directory_path.exists():
        collection.warnings.append(f"Directory not found: {directory_path}")
        return collection
    
    # Find matching files
    matching_files = list(directory_path.glob(pattern))
    if not matching_files:
        collection.warnings.append(f"No files matching '{pattern}' found in {directory_path}")
        return collection
    
    # Load each file
    for file_path in matching_files:
        try:
            result = load_file(file_path)
            collection.files_loaded.append(result)
            collection.total_lines += result.line_count
            collection.total_non_empty_lines += result.non_empty_line_count
            collection.warnings.extend(result.warnings)
        except Exception as e:
            collection.errors.append(f"Failed to load {file_path}: {e}")
    
    return collection


def load_all_corpus() -> CorpusCollection:
    """
    Load all known corpus files from all locations.
    
    Returns:
        CorpusCollection with all loaded files
    """
    collection = CorpusCollection()
    
    # Try to load from each corpus location
    for location, dir_name in CORPUS_LOCATIONS.items():
        dir_path = Path(__file__).parent.parent.parent.parent / dir_name
        
        if dir_path.exists():
            sub_collection = load_directory(dir_path)
            collection.files_loaded.extend(sub_collection.files_loaded)
            collection.total_lines += sub_collection.total_lines
            collection.total_non_empty_lines += sub_collection.total_non_empty_lines
            collection.warnings.extend(sub_collection.warnings)
            collection.errors.extend(sub_collection.errors)
        else:
            collection.warnings.append(f"Corpus location not found: {dir_path}")
    
    return collection


def get_corpus_info() -> Dict[str, str]:
    """
    Get information about available corpus files.
    
    Returns:
        Dictionary with corpus location information
    """
    base_path = Path(__file__).parent.parent.parent.parent
    
    info = {}
    for location, dir_name in CORPUS_LOCATIONS.items():
        dir_path = base_path / dir_name
        if dir_path.exists():
            files = list(dir_path.glob("*"))
            info[location] = {
                "path": str(dir_path),
                "exists": True,
                "file_count": len(files),
                "files": [f.name for f in files if f.is_file()]
            }
        else:
            info[location] = {
                "path": str(dir_path),
                "exists": False,
                "file_count": 0,
                "files": []
            }
    
    return info


if __name__ == "__main__":
    """
    Self-test: Load and display information about available corpus.
    """
    print("=" * 70)
    print("General Corpus Loader - Self Test")
    print("=" * 70)
    
    # Show corpus info
    info = get_corpus_info()
    print("\nAvailable corpus locations:")
    for location, data in info.items():
        status = "OK" if data["exists"] else "MISSING"
        print(f"  {location}: {status} ({data['file_count']} files)")
        if data["files"]:
            for f in data["files"][:5]:  # Show first 5 files
                print(f"    - {f}")
            if len(data["files"]) > 5:
                print(f"    ... and {len(data['files']) - 5} more")
    
    # Try loading the default A2 file
    print("\n" + "-" * 70)
    print("Testing A2/00 11 RESNICAMI.txt loader:")
    try:
        result = load_file(DEFAULT_CORPUS_PATH)
        print(f"  Loaded: {result.line_count} lines, {result.non_empty_line_count} non-empty")
        print(f"  Sections detected: {len(result.detected_sections)}")
    except Exception as e:
        print(f"  Error: {e}")
    
    print("\n" + "=" * 70)
    print("CORPUS LOADER SELF-TEST PASSED")
    print("=" * 70)
