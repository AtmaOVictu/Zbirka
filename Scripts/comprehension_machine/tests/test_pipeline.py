"""Tests for R-7 pipeline, json_safe, and symbol mapper."""

import pytest
from comprehension.core.processing_pipeline import ProcessingPipeline, PipelineConfig
from comprehension.core.json_safe import to_json_safe, from_json_safe, safe_json_dumps, safe_json_loads
from comprehension.core.symbol_mapper import SymbolMapper


class TestPipeline:
    def test_all_phases_complete(self):
        r = ProcessingPipeline().process("Test")
        assert len(r.phases) == 7
    def test_phase_order(self):
        r = ProcessingPipeline().process("Test")
        phases = list(r.phases.keys())
        assert phases == ["\u2205", "\u00ac", "\u2206", "1", "\u29d6", "\u222e", "\u27e1"]
    def test_empty_statement(self):
        r = ProcessingPipeline().process("")
        assert r.status in ("completed", "partial")
    def test_unicode(self):
        r = ProcessingPipeline().process("\u2205 \u22a2 \u222e")
        assert len(r.phases) == 7
    def test_batch(self):
        rs = ProcessingPipeline().process_batch(["A", "B", "C"])
        assert len(rs) == 3 and all(len(r.phases) == 7 for r in rs)
    def test_cache_hit(self):
        p = ProcessingPipeline(PipelineConfig(enable_caching=True))
        r1 = p.process("Cached")
        r2 = p.process("Cached")
        assert r2.total_duration_ms <= r1.total_duration_ms


class TestJsonSafe:
    def test_primitives(self):
        assert to_json_safe(42) == 42
        assert to_json_safe("x") == "x"
        assert to_json_safe(None) is None
    def test_set(self):
        assert set(to_json_safe({1, 2, 3})) == {1, 2, 3}
    def test_datetime(self):
        import datetime
        dt = datetime.datetime(2025, 9, 12)
        assert from_json_safe(to_json_safe(dt)) == dt
    def test_roundtrip(self):
        d = {"a": [1, 2], "b": {"c": True}}
        assert safe_json_loads(safe_json_dumps(d)) == d


class TestSymbolMapper:
    def test_translate(self):
        m = SymbolMapper()
        assert m.translate("\u22a2", "historical") == "\u2694\ufe0f"
        assert m.translate("\u2694\ufe0f", "system") == "\u22a2"
        assert m.translate("\u22a2", "mathematical") == "\u22a2 A"
    def test_phase_lookup(self):
        m = SymbolMapper()
        assert m.get_phase_symbol("BIOS") == "\u2205"
        assert m.get_module_for_phase("\u27e1") == "VISUALIZATION"
    def test_r7_sequence(self):
        syms = [i["system"] for i in SymbolMapper().get_r7_symbols()]
        assert syms == ["\u2205", "\u00ac", "\u2206", "1", "\u29d6", "\u222e", "\u27e1"]
    def test_traditions(self):
        m = SymbolMapper()
        assert m.get_tradition("sufism")["count"] == 100
        assert m.get_tradition("dna")["count"] == 64
    def test_open_questions(self):
        assert len(SymbolMapper().get_open_questions()) == 12
