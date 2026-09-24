#!/usr/bin/env python
"""
Validate R-7 Symbol Mapping
==========================
Phase 2 - Symbol Validation

Checks that all expected R-7 symbols exist and are properly configured.

Expected R-7 symbols (canonical order):
  ∅ (U+2205) - BIOS - praznina, potencial, odprtost
  ¬ (U+00AC) - STATE - ločitev, struktura, meritev
  ∆ (U+2206) - UAF - razlika, gibanje, antinomija
  1 (U+0031) - JEWIK - dejanje, emanacija, pečat
  ⧖ (U+29D6) - APD - tišina, preverba, izgovor
  ∮ (U+222E) - MICRO - povratek, učenje
  ⟡ (U+27E1) - VISUALIZATION - nova možnost, manifestacija, graf

Usage:
    python scripts/validate_symbols.py [--verbose]

Exit codes:
    0 = All symbols validated successfully
    1 = Validation failures found
    2 = Critical error (cannot run validation)
"""

import sys
from dataclasses import dataclass, field
from typing import List, Dict, Optional


# Colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def color_text(text, color):
    """Apply color to text if running in a terminal."""
    if sys.stdout.isatty():
        return f"{color}{text}{RESET}"
    return text


# Expected R-7 symbols in canonical order (from symbol_mapper.py R7_ORDER)
# Note: There are known discrepancies in the codebase:
#   - UAF: symbol_mapper uses ∆ (U+2206), decomposer uses Δ (U+0394)
#   - APD: symbol_mapper uses ⧖ (U+29D6), tonos uses ⌖ (U+2316)
EXPECTED_R7_SYMBOLS = [
    ("∅", "U+2205", "BIOS"),
    ("¬", "U+00AC", "STATE"),
    ("∆", "U+2206", "UAF"),
    ("1", "U+0031", "JEWIK"),
    ("⧖", "U+29D6", "APD"),  # This is the canonical symbol per symbol_mapper.py
    ("∮", "U+222E", "MICRO"),
    ("⟡", "U+27E1", "VISUALIZATION"),
]

# Alternative symbols found in the codebase
ALTERNATIVE_UAF_IN_DECOMPOSER = "Δ"   # U+0394 (Greek capital Delta)
ALTERNATIVE_APD_IN_TONOS = "⌖"       # U+2316 (Top half integral)


@dataclass
class SymbolValidationResult:
    """Result of validating a single symbol."""
    symbol: str
    codepoint: str
    expected_module: str
    found: bool = False
    in_mappings: bool = False
    in_r7_order: bool = False
    in_phase_mapping: bool = False
    in_tonos: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


@dataclass
class ValidationReport:
    """Complete validation report."""
    symbols_validated: List[SymbolValidationResult] = field(default_factory=list)
    missing_symbols: List[str] = field(default_factory=list)
    extra_symbols: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    
    @property
    def passed(self) -> bool:
        """Return True if all critical checks passed."""
        return len(self.errors) == 0 and len(self.missing_symbols) == 0


def validate_symbol_mapper(mapper):
    """Validate SymbolMapper instance."""
    report = ValidationReport()
    
    # Get R7 symbols from mapper
    r7_symbols_from_mapper = mapper.R7_ORDER
    mapper_mappings = mapper._MAPPINGS
    
    # Validate each expected symbol
    for symbol, codepoint, expected_module in EXPECTED_R7_SYMBOLS:
        result = SymbolValidationResult(
            symbol=symbol,
            codepoint=codepoint,
            expected_module=expected_module
        )
        
        # Check if symbol exists in mappings
        if symbol in mapper_mappings:
            result.found = True
            result.in_mappings = True
            
            # Check module assignment
            entry = mapper_mappings[symbol]
            actual_module = entry.get("module")
            if actual_module and actual_module != expected_module:
                result.warnings.append(
                    f"Module mismatch: expected {expected_module}, got {actual_module}"
                )
        else:
            result.errors.append(f"Symbol {symbol} ({codepoint}) not found in mappings")
        
        # Check if symbol is in R7 order
        if symbol in r7_symbols_from_mapper:
            result.in_r7_order = True
        else:
            result.errors.append(f"Symbol {symbol} not in R7_ORDER")
        
        # Check if symbol is in phase mapping (from decomposer)
        try:
            from comprehension.core.decomposer import SYMBOL_TO_PHASE
            if symbol in SYMBOL_TO_PHASE:
                result.in_phase_mapping = True
            else:
                # Check for alternative symbols (Δ for ∆)
                if symbol == "∆" and ALTERNATIVE_UAF_IN_DECOMPOSER in SYMBOL_TO_PHASE:
                    result.in_phase_mapping = True
                    # Note: We don't add a warning here because validate_decomposer_symbols
                    # will report this discrepancy separately
                else:
                    result.errors.append(f"Symbol {symbol} not in SYMBOL_TO_PHASE")
        except ImportError:
            result.warnings.append("Could not import decomposer.SYMBOL_TO_PHASE")
        
        # Check if symbol is in tonos
        try:
            from comprehension.core.tonos import TONOS_FREQUENCIES
            if symbol in TONOS_FREQUENCIES:
                result.in_tonos = True
            else:
                # Check for alternative APD symbol (⌖ U+2316 in tonos vs ⧖ U+29D6 in mapper)
                if symbol == "⧖" and ALTERNATIVE_APD_IN_TONOS in TONOS_FREQUENCIES:
                    result.in_tonos = True
                    # Note: We don't add a warning here because validate_tonos_symbols
                    # will report this discrepancy separately
                else:
                    result.warnings.append(f"Symbol {symbol} not in TONOS_FREQUENCIES")
        except ImportError:
            result.warnings.append("Could not import tonos.TONOS_FREQUENCIES")
        
        report.symbols_validated.append(result)
        
        # Collect errors and warnings
        if result.errors:
            report.errors.extend(result.errors)
        if result.warnings:
            report.warnings.extend(result.warnings)
    
    # Check for missing expected symbols
    for symbol, _, _ in EXPECTED_R7_SYMBOLS:
        if not any(s.symbol == symbol and s.found for s in report.symbols_validated):
            if symbol not in report.missing_symbols:
                report.missing_symbols.append(symbol)
    
    # Check for extra symbols in R7 order
    for symbol in r7_symbols_from_mapper:
        if not any(s == symbol for s, _, _ in EXPECTED_R7_SYMBOLS):
            report.extra_symbols.append(symbol)
            report.warnings.append(f"Extra symbol in R7_ORDER: {symbol}")
    
    return report


def validate_tonos_symbols():
    """Validate TONOS frequency assignments."""
    tonos_warnings = []
    tonos_errors = []
    
    try:
        from comprehension.core.tonos import TONOS_FREQUENCIES, COMPLEMENTARY_PAIRS
        
        # Check all R7 symbols have frequencies (with alternatives)
        # symbol_mapper uses: ∅, ¬, ∆, 1, ⧖, ∮, ⟡
        # tonos.py has: ∅, ¬, ∆, 1, ⌖, ∮, ⟡
        # So APD symbol is different: ⧖ (U+29D6) vs ⌖ (U+2316)
        symbol_checks = {
            "∅": "∅",
            "¬": "¬",
            "∆": "∆",  # tonos has ∆ for UAF
            "1": "1",
            "⧖": "⌖",  # tonos has ⌖ (U+2316) instead of ⧖ (U+29D6) for APD
            "∮": "∮",
            "⟡": "⟡",
        }
        
        for symbol, check_symbol in symbol_checks.items():
            if symbol not in TONOS_FREQUENCIES:
                # Symbol from mapper is not in tonos - check if alternative is there
                if check_symbol in TONOS_FREQUENCIES:
                    if symbol == "⧖" and check_symbol == "⌖":
                        tonos_warnings.append(
                            f"TONOS uses ⌖ (U+2316) instead of {symbol} (U+29D6) for APD"
                        )
                    else:
                        tonos_warnings.append(
                            f"TONOS uses {check_symbol} instead of {symbol}"
                        )
                else:
                    tonos_errors.append(f"TONOS missing frequency for {symbol}")
        
        # Check complementary pairs
        expected_pairs = [
            ("∅", "⟡"),
            ("¬", "∆"),
            ("1", "∮"),
        ]
        for a, b in expected_pairs:
            if a not in COMPLEMENTARY_PAIRS or COMPLEMENTARY_PAIRS[a] != b:
                tonos_warnings.append(f"Complementary pair ({a}, {b}) not configured correctly")
        
        return tonos_warnings, tonos_errors
        
    except ImportError as e:
        return [f"Could not import tonos: {e}"], []


def validate_decomposer_symbols():
    """Validate decomposer symbol mappings."""
    decomposer_warnings = []
    decomposer_errors = []
    
    try:
        from comprehension.core.decomposer import SYMBOL_TO_PHASE
        
        # Check all expected symbols have phase mappings (with alternatives)
        # symbol_mapper uses: ∅, ¬, ∆, 1, ⧖, ∮, ⟡
        # decomposer has: ∅, ¬, Δ, 1, ⧖, ∮, ⟡
        # So UAF symbol is different: ∆ (U+2206) vs Δ (U+0394)
        symbol_checks = {
            "∅": "∅",
            "¬": "¬",
            "∆": "Δ",  # decomposer uses Δ (U+0394) instead of ∆ (U+2206)
            "1": "1",
            "⧖": "⧖",  # decomposer has ⧖ (U+29D6) for APD
            "∮": "∮",
            "⟡": "⟡",
        }
        
        for symbol, alt_symbol in symbol_checks.items():
            if symbol not in SYMBOL_TO_PHASE and alt_symbol not in SYMBOL_TO_PHASE:
                decomposer_errors.append(f"Decomposer missing phase for {symbol} (or {alt_symbol})")
            elif symbol != alt_symbol and alt_symbol in SYMBOL_TO_PHASE:
                # Report symbol discrepancies
                if symbol == "∆" and alt_symbol == "Δ":
                    decomposer_warnings.append(
                        f"Decomposer uses {alt_symbol} (U+0394) instead of {symbol} (U+2206) for UAF phase"
                    )
                elif symbol == "⧖" and alt_symbol == "⌖":
                    decomposer_warnings.append(
                        f"Decomposer uses {alt_symbol} (U+2316) instead of {symbol} (U+29D6) for APD phase"
                    )
        
        # Check phase values are valid (0-6)
        for symbol, phase in SYMBOL_TO_PHASE.items():
            if not (0 <= phase <= 6):
                decomposer_warnings.append(f"Symbol {symbol} has invalid phase {phase}")
        
        return decomposer_warnings, decomposer_errors
        
    except ImportError as e:
        return [f"Could not import decomposer: {e}"], []


def print_validation_report(report: ValidationReport, tonos_warnings, tonos_errors,
                            decomposer_warnings, decomposer_errors):
    """Print a formatted validation report."""
    print("\n" + "=" * 70)
    print("R-7 SYMBOL VALIDATION REPORT")
    print("=" * 70)
    
    # Print symbol-by-symbol results
    print(f"\n{color_text('Symbol Validation:', BLUE)}")
    print("-" * 70)
    
    for result in report.symbols_validated:
        status_icons = []
        if result.found:
            status_icons.append(color_text("✓", GREEN))
        else:
            status_icons.append(color_text("✗", RED))
        
        if result.in_mappings:
            status_icons.append(color_text("M", GREEN))
        else:
            status_icons.append(color_text("M", RED))
        
        if result.in_r7_order:
            status_icons.append(color_text("R7", GREEN))
        else:
            status_icons.append(color_text("R7", RED))
        
        if result.in_phase_mapping:
            status_icons.append(color_text("P", GREEN))
        else:
            status_icons.append(color_text("P", RED))
        
        if result.in_tonos:
            status_icons.append(color_text("T", GREEN))
        else:
            status_icons.append(color_text("T", RED))
        
        print(f"  {result.symbol:3s} ({result.codepoint:8s}) {result.expected_module:15s} "
              f"{' '.join(status_icons)}")
        
        for warning in result.warnings:
            print(f"    {color_text('  WARNING:', YELLOW)} {warning}")
        for error in result.errors:
            print(f"    {color_text('  ERROR:', RED)} {error}")
    
    # Print summary
    print("\n" + "-" * 70)
    print(f"{color_text('Summary:', BLUE)}")
    
    all_warnings = report.warnings + tonos_warnings + decomposer_warnings
    all_errors = report.errors + tonos_errors + decomposer_errors
    
    print(f"  Symbols validated: {len(report.symbols_validated)}/7")
    print(f"  Missing symbols: {len(report.missing_symbols)}")
    if report.missing_symbols:
        print(f"    {', '.join(report.missing_symbols)}")
    print(f"  Extra symbols: {len(report.extra_symbols)}")
    if report.extra_symbols:
        print(f"    {', '.join(report.extra_symbols)}")
    print(f"  {color_text('Warnings:', YELLOW)} {len(all_warnings)}")
    print(f"  {color_text('Errors:', RED)} {len(all_errors)}")
    
    # Print warnings
    if all_warnings:
        print(f"\n{color_text('Warnings:', YELLOW)}")
        for warning in all_warnings:
            print(f"  - {warning}")
    
    # Print errors
    if all_errors:
        print(f"\n{color_text('Errors:', RED)}")
        for error in all_errors:
            print(f"  - {error}")
    
    print("\n" + "=" * 70)
    if report.passed and len(all_errors) == 0:
        print(color_text("SYMBOL VALIDATION PASSED", GREEN))
    else:
        print(color_text("SYMBOL VALIDATION FAILED", RED))
    print("=" * 70)


def main():
    """Main entry point."""
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    
    try:
        # Import symbol mapper
        from comprehension.core.symbol_mapper import SymbolMapper
        
        # Create mapper and validate
        mapper = SymbolMapper()
        report = validate_symbol_mapper(mapper)
        
        # Validate other components
        tonos_warnings, tonos_errors = validate_tonos_symbols()
        decomposer_warnings, decomposer_errors = validate_decomposer_symbols()
        
        # Print report
        print_validation_report(report, tonos_warnings, tonos_errors,
                               decomposer_warnings, decomposer_errors)
        
        # Return exit code
        if report.passed and len(report.errors) == 0:
            return 0
        else:
            return 1
            
    except Exception as e:
        print(f"{color_text('CRITICAL ERROR:', RED)} {e}")
        import traceback
        traceback.print_exc()
        return 2


if __name__ == "__main__":
    sys.exit(main())
