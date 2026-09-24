#!/usr/bin/env python
"""
A2 Corpus Loader
=================
Phase 3 - Corpus Loader

Loads the canonical corpus file: A2/00 11 RESNICAMI.txt

This loader ONLY structures the input - it does NOT explain meaning.

Returns:
    dict with keys:
        - source_path: str (absolute path to the file)
        - raw_text: str (full text content)
        - line_count: int (total lines)
        - non_empty_line_count: int (lines with content)
        - detected_sections: list of dicts with section info
        - warnings: list of str (any issues detected)

Guard Principle: No meaning invention, only structuring.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class SectionInfo:
    """Information about a detected section in the corpus."""
    name: str
    start_line: int
    end_line: int = 0
    line_count: int = 0
    header: Optional[str] = None


@dataclass
class CorpusLoadResult:
    """Result of loading a corpus file."""
    source_path: str
    raw_text: str
    line_count: int
    non_empty_line_count: int
    detected_sections: List[SectionInfo] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


# Default path to the canonical corpus file
DEFAULT_CORPUS_PATH = Path(__file__).parent.parent.parent.parent / "A2" / "00 11 RESNICAMI.txt"


def detect_sections(lines: List[str]) -> List[SectionInfo]:
    """
    Detect sections in the corpus text.
    
    Sections are identified by:
    - Lines starting with '#' (Markdown headers)
    - Lines with specific patterns like 'PESEM', 'RES', 'REZ'
    - Blank lines separating sections
    
    Returns list of SectionInfo objects.
    """
    sections = []
    current_section = None
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Skip empty lines
        if not stripped:
            continue
        
        # Check for section markers
        if stripped.startswith('#'):
            # Markdown header - new section
            if current_section is not None:
                # Save previous section
                current_section.end_line = i - 1
                current_section.line_count = current_section.end_line - current_section.start_line + 1
                sections.append(current_section)
            
            # Start new section
            header_text = stripped.lstrip('#').strip()
            current_section = SectionInfo(
                name=header_text,
                start_line=i,
                end_line=i,
                header=stripped
            )
        elif any(marker in stripped for marker in ['PESEM', 'RES', 'REZ', 'AGENT']):
            # Possible section marker
            if current_section is None:
                current_section = SectionInfo(
                    name=stripped,
                    start_line=i,
                    end_line=i,
                    header=None
                )
        elif current_section is not None:
            # Continuation of current section
            current_section.end_line = i
    
    # Don't forget the last section
    if current_section is not None:
        current_section.end_line = len(lines) - 1
        current_section.line_count = current_section.end_line - current_section.start_line + 1
        sections.append(current_section)
    
    return sections


def load_corpus_file(file_path: Optional[str] = None) -> CorpusLoadResult:
    """
    Load the A2/00 11 RESNICAMI.txt corpus file.
    
    Args:
        file_path: Optional path to the corpus file. If None, uses DEFAULT_CORPUS_PATH.
    
    Returns:
        CorpusLoadResult with structured data about the loaded file.
    
    Raises:
        FileNotFoundError: If the corpus file cannot be found.
        UnicodeDecodeError: If the file cannot be decoded as UTF-8.
    """
    warnings = []
    
    # Determine the file path
    if file_path is not None:
        path = Path(file_path)
    else:
        path = DEFAULT_CORPUS_PATH
    
    # Resolve to absolute path
    path = path.resolve()
    
    # Check if file exists
    if not path.exists():
        # Try alternative locations
        alt_paths = [
            Path(__file__).parent.parent.parent / "A2" / "00 11 RESNICAMI.txt",
            Path("A2") / "00 11 RESNICAMI.txt",
            Path("../A2") / "00 11 RESNICAMI.txt",
            Path("../../A2") / "00 11 RESNICAMI.txt",
        ]
        
        for alt_path in alt_paths:
            if alt_path.exists():
                path = alt_path.resolve()
                warnings.append(f"Used alternative path: {path}")
                break
        else:
            raise FileNotFoundError(
                f"Corpus file not found at {DEFAULT_CORPUS_PATH} or any alternative location. "
                f"Please ensure A2/00 11 RESNICAMI.txt exists relative to the script location."
            )
    
    # Load the file with UTF-8 encoding
    try:
        with open(path, 'r', encoding='utf-8') as f:
            raw_text = f.read()
    except UnicodeDecodeError:
        # Try with different encodings
        for encoding in ['utf-8-sig', 'latin-1', 'cp1252']:
            try:
                with open(path, 'r', encoding=encoding) as f:
                    raw_text = f.read()
                warnings.append(f"File decoded with {encoding} encoding")
                break
            except UnicodeDecodeError:
                continue
        else:
            raise UnicodeDecodeError(
                f"Could not decode {path} with any tried encoding (utf-8, utf-8-sig, latin-1, cp1252)"
            )
    
    # Split into lines
    lines = raw_text.splitlines()
    line_count = len(lines)
    non_empty_line_count = sum(1 for line in lines if line.strip())
    
    # Detect sections
    detected_sections = detect_sections(lines)
    
    # Add warnings if no sections detected
    if not detected_sections:
        warnings.append("No sections detected in the corpus file")
    
    # Add warning if file is very small
    if line_count < 10:
        warnings.append(f"File appears very small ({line_count} lines)")
    
    return CorpusLoadResult(
        source_path=str(path),
        raw_text=raw_text,
        line_count=line_count,
        non_empty_line_count=non_empty_line_count,
        detected_sections=detected_sections,
        warnings=warnings
    )


def load():
    """
    Convenience function to load the default corpus file.
    
    Returns:
        CorpusLoadResult with the loaded data.
    
    Example:
        from loaders.a2_loader import load
        result = load()
        print(f"Loaded {result.line_count} lines from {result.source_path}")
    """
    return load_corpus_file()


if __name__ == "__main__":
    """
    Self-test: Load and display basic information about the corpus.
    """
    print("=" * 70)
    print("A2 Corpus Loader - Self Test")
    print("=" * 70)
    
    try:
        result = load()
        
        print(f"\nSource: {result.source_path}")
        print(f"Total lines: {result.line_count}")
        print(f"Non-empty lines: {result.non_empty_line_count}")
        print(f"Empty line ratio: {100 * (1 - result.non_empty_line_count / result.line_count):.1f}%")
        
        print(f"\nDetected {len(result.detected_sections)} section(s):")
        for section in result.detected_sections:
            print(f"  - {section.name} (lines {section.start_line}-{section.end_line}, {section.line_count} lines)")
        
        if result.warnings:
            print(f"\nWarnings:")
            for warning in result.warnings:
                print(f"  - {warning}")
        
        print("\n" + "=" * 70)
        print("LOADER SELF-TEST PASSED")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n{type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        print("\n" + "=" * 70)
        print("LOADER SELF-TEST FAILED")
        print("=" * 70)
        exit(1)
