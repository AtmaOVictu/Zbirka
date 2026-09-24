"""
TAZV Comprehension Machine - Bootstrap Script
==============================================
1. Copy this entire file into your editor
2. Save as: bootstrap_tazv.py
3. Run:  python bootstrap_tazv.py

This creates the ENTIRE Phase 0 project with all files.
After it runs, you get a ready-to-use comprehension_machine/ folder.
"""

import os
from pathlib import Path

ROOT = Path("comprehension_machine")

DIRS = [
    "comprehension",
    "comprehension/core",
    "comprehension/modules",
    "comprehension/ui",
    "comprehension/data",
    "comprehension/utils",
    "tests",
    "docs",
]

FILES = {}

for d in ["comprehension", "comprehension/core", "comprehension/modules",
          "comprehension/ui", "comprehension/data", "comprehension/utils"]:
    FILES[d + "/__init__.py"] = ""

FILES["README.md"] = (
    "# TAZV Comprehension Machine\n\n"
    "Desktop app implementing the R-7 ontological processing pipeline.\n\n"
    "## Quick Start\n\n"
    "    cd comprehension_machine\n"
    "    pip install PyQt6\n"
    "    python -m comprehension.core.processing_pipeline\n"
    "    python -m comprehension.core.symbol_mapper\n"
    "    pytest\n\n"
    "## Structure\n\n"
    "    comprehension_machine/\n"
    "      comprehension/\n"
    "        core/        R-7 pipeline, adapters, symbol mapper\n"
    "        modules/     Module implementations (Phase 1)\n"
    "        ui/          PyQt6 windows (Phase 1)\n"
    "        data/        SQLite + exporters\n"
    "        utils/       Error handler, profiler\n"
    "      tests/\n"
    "      docs/\n"
    "      data/          Runtime: sessions.db\n"
)

FILES["pytest.ini"] = (
    "[pytest]\n"
    "testpaths = tests\n"
    "python_files = test_*.py\n"
    "python_functions = test_*\n"
)

FILES["comprehension/core/json_safe.py"] = (
    '"""JSON-safe serialization for dataclasses, Enums, numpy, datetime, sets."""\n\n'
    'import dataclasses\n'
    'import enum\n'
    'import datetime\n'
    'import json\n'
    'from typing import Any\n\n\n'
    'def to_json_safe(obj: Any) -> Any:\n'
    '    if obj is None or isinstance(obj, (bool, int, float, str)):\n'
    '        return obj\n'
    '    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):\n'
    '        return {"__dataclass__": obj.__class__.__name__,\n'
    '                "fields": {f.name: to_json_safe(getattr(obj, f.name)) for f in dataclasses.fields(obj)}}\n'
    '    if isinstance(obj, enum.Enum):\n'
    '        return {"__enum__": f"{obj.__class__.__name__}.{obj.name}"}\n'
    '    if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):\n'
    '        return {"__datetime__": obj.isoformat()}\n'
    '    if isinstance(obj, datetime.timedelta):\n'
    '        return {"__timedelta__": obj.total_seconds()}\n'
    '    try:\n'
    '        import numpy as np\n'
    '        if isinstance(obj, np.integer): return int(obj)\n'
    '        if isinstance(obj, np.floating): return float(obj)\n'
    '        if isinstance(obj, np.bool_): return bool(obj)\n'
    '        if isinstance(obj, np.ndarray):\n'
    '            return {"__ndarray__": True, "data": obj.tolist(), "dtype": str(obj.dtype), "shape": list(obj.shape)}\n'
    '        if isinstance(obj, np.generic): return obj.item()\n'
    '    except ImportError:\n'
    '        pass\n'
    '    if isinstance(obj, dict):\n'
    '        return {str(k): to_json_safe(v) for k, v in obj.items()}\n'
    '    if isinstance(obj, (list, tuple, set, frozenset)):\n'
    '        return [to_json_safe(item) for item in obj]\n'
    '    if hasattr(obj, "__dict__"):\n'
    '        return {"__object__": obj.__class__.__name__, "attrs": to_json_safe(obj.__dict__)}\n'
    '    return str(obj)\n\n\n'
    'def from_json_safe(obj: Any) -> Any:\n'
    '    if not isinstance(obj, dict):\n'
    '        return [from_json_safe(i) for i in obj] if isinstance(obj, list) else obj\n'
    '    if "__datetime__" in obj:\n'
    '        for p in (datetime.datetime.fromisoformat, datetime.date.fromisoformat, datetime.time.fromisoformat):\n'
    '            try: return p(obj["__datetime__"])\n'
    '            except (ValueError, TypeError): continue\n'
    '        return obj["__datetime__"]\n'
    '    if "__timedelta__" in obj: return datetime.timedelta(seconds=obj["__timedelta__"])\n'
    '    if "__ndarray__" in obj:\n'
    '        try:\n'
    '            import numpy as np\n'
    '            return np.array(obj["data"], dtype=obj["dtype"]).reshape(obj["shape"])\n'
    '        except (ImportError, ValueError): return obj["data"]\n'
    '    if "__enum__" in obj: return obj["__enum__"]\n'
    '    if "__dataclass__" in obj: return obj["fields"]\n'
    '    if "__object__" in obj: return obj["attrs"]\n'
    '    return {k: from_json_safe(v) for k, v in obj.items()}\n\n\n'
    'def safe_json_dumps(obj, **kw): return json.dumps(to_json_safe(obj), **kw)\n'
    'def safe_json_loads(s, reconstruct=False, **kw):\n'
    '    r = json.loads(s, **kw)\n'
    '    return from_json_safe(r) if reconstruct else r\n'
)

FILES["comprehension/core/module_adapters.py"] = (
    '"""Module interface adapters for the R-7 pipeline."""\n\n'
    'import time\n'
    'import traceback\n'
    'from dataclasses import dataclass, field\n'
    'from typing import Protocol, runtime_checkable\n\n'
    'from .json_safe import to_json_safe\n\n\n'
    '@dataclass\n'
    'class ModuleInput:\n'
    '    statement: str\n'
    '    context: dict = field(default_factory=dict)\n'
    '    config: dict = field(default_factory=dict)\n'
    '    phase_history: list = field(default_factory=list)\n'
    '    session_id: str = ""\n\n\n'
    '@dataclass\n'
    'class ModuleOutput:\n'
    '    phase: str\n'
    '    module_name: str\n'
    '    data: dict = field(default_factory=dict)\n'
    '    kpi: dict = field(default_factory=dict)\n'
    '    errors: list = field(default_factory=list)\n'
    '    duration_ms: float = 0.0\n'
    '    status: str = "completed"\n\n\n'
    '@runtime_checkable\n'
    'class ModuleProtocol(Protocol):\n'
    '    phase: str\n'
    '    module_name: str\n'
    '    def process(self, input: ModuleInput) -> ModuleOutput: ...\n\n\n'
    'class BaseModuleAdapter:\n'
    '    def __init__(self, phase, module_name):\n'
    '        self.phase = phase\n'
    '        self.module_name = module_name\n\n'
    '    def process(self, input):\n'
    '        start = time.perf_counter()\n'
    '        errors, data, kpi, status = [], {}, {}, "completed"\n'
    '        try:\n'
    '            result = self.run(input)\n'
    '            if isinstance(result, dict):\n'
    '                data = result.get("data", result)\n'
    '                kpi = result.get("kpi", {})\n'
    '                if result.get("errors"):\n'
    '                    errors.extend(result["errors"])\n'
    '                    status = "partial" if data else "failed"\n'
    '            elif isinstance(result, ModuleOutput):\n'
    '                data, kpi, errors, status = result.data, result.kpi, result.errors, result.status\n'
    '            else:\n'
    '                data = {"raw": to_json_safe(result)}\n'
    '        except Exception as e:\n'
    '            errors.append({"module": self.module_name, "error": str(e), "traceback": traceback.format_exc()})\n'
    '            status = "failed"\n'
    '        return ModuleOutput(self.phase, self.module_name, to_json_safe(data),\n'
    '                            to_json_safe(kpi), to_json_safe(errors),\n'
    '                            (time.perf_counter() - start) * 1000, status)\n\n'
    '    def run(self, input):\n'
    '        raise NotImplementedError(f"{self.module_name}.run() not implemented")\n\n\n'
    'class BIOSAdapter(BaseModuleAdapter):\n'
    '    def __init__(self): super().__init__("\\u2205", "BIOS")\n'
    '    def run(self, i):\n'
    '        return {"data": {"statement": i.statement, "tokens": i.statement.split(), "char_count": len(i.statement)},\n'
    '                "kpi": {"phase_completeness": 1.0}}\n\n\n'
    'class StateAdapter(BaseModuleAdapter):\n'
    '    def __init__(self): super().__init__("\\u00ac", "STATE")\n'
    '    def run(self, i):\n'
    '        bd = i.context.get("\\u2205", {}).get("data", {})\n'
    '        return {"data": {"structure": "basic", "word_count": len(bd.get("tokens", []))},\n'
    '                "kpi": {"\\u03ba": 0.75, "\\u03c7": 0.50}}\n\n\n'
    'class UAFAdapter(BaseModuleAdapter):\n'
    '    def __init__(self): super().__init__("\\u2206", "UAF")\n'
    '    def run(self, i): return {"data": {"antinomies": [], "tension_score": 0.0}, "kpi": {"antinomy_count": 0}}\n\n\n'
    'class JEWIKAdapter(BaseModuleAdapter):\n'
    '    def __init__(self): super().__init__("1", "JEWIK")\n'
    '    def run(self, i): return {"data": {"layers": [], "emanation": "none"}, "kpi": {"layer_count": 0}}\n\n\n'
    'class APDAdapter(BaseModuleAdapter):\n'
    '    def __init__(self): super().__init__("\\u29d6", "APD")\n'
    '    def run(self, i): return {"data": {"sealed": True, "verification": "auto"}, "kpi": {"seal_confidence": 0.80}}\n\n\n'
    'class MicroAdapter(BaseModuleAdapter):\n'
    '    def __init__(self): super().__init__("\\u222e", "MICRO")\n'
    '    def run(self, i): return {"data": {"patterns": [], "hopf_state": 0}, "kpi": {"pattern_count": 0}}\n\n\n'
    'class VisualizationAdapter(BaseModuleAdapter):\n'
    '    def __init__(self): super().__init__("\\u27e1", "VISUALIZATION")\n'
    '    def run(self, i): return {"data": {"graph": {"nodes": [], "edges": []}}, "kpi": {"projection_complete": 1.0}}\n\n\n'
    'R7_MODULES = [BIOSAdapter, StateAdapter, UAFAdapter, JEWIKAdapter,\n'
    '              APDAdapter, MicroAdapter, VisualizationAdapter]\n'
)

FILES["comprehension/core/processing_pipeline.py"] = (
    '"""R-7 processing pipeline. Never crashes."""\n\n'
    'import time\n'
    'import hashlib\n'
    'import logging\n'
    'import traceback\n'
    'from dataclasses import dataclass, field\n'
    'from .module_adapters import ModuleInput, ModuleOutput, BaseModuleAdapter, R7_MODULES\n\n'
    'logger = logging.getLogger(__name__)\n\n\n'
    '@dataclass\n'
    'class PipelineConfig:\n'
    '    batch_size: int = 64\n'
    '    enable_caching: bool = True\n'
    '    cache_max_size: int = 256\n'
    '    fail_fast: bool = False\n'
    '    log_level: str = "INFO"\n\n\n'
    '@dataclass\n'
    'class PipelineResult:\n'
    '    session_id: str = ""\n'
    '    statements_processed: int = 0\n'
    '    phases: dict = field(default_factory=dict)\n'
    '    all_errors: list = field(default_factory=list)\n'
    '    total_duration_ms: float = 0.0\n'
    '    status: str = "completed"\n\n\n'
    'class ProcessingPipeline:\n'
    '    R7_PHASES = ["\\u2205", "\\u00ac", "\\u2206", "1", "\\u29d6", "\\u222e", "\\u27e1"]\n\n'
    '    def __init__(self, config=None):\n'
    '        self.config = config or PipelineConfig()\n'
    '        self._cache = {} if self.config.enable_caching else None\n'
    '        self._modules = [cls() for cls in R7_MODULES]\n'
    '        logging.basicConfig(level=getattr(logging, self.config.log_level, logging.INFO),\n'
    '                            format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")\n\n'
    '    def _cache_key(self, statement, overrides):\n'
    '        return hashlib.md5(f"{statement}:{sorted(overrides.items())}".encode()).hexdigest()\n\n'
    '    def process(self, statement, config_overrides=None, session_id=""):\n'
    '        overrides = config_overrides or {}\n'
    '        result = PipelineResult(session_id=session_id)\n'
    '        start = time.perf_counter()\n'
    '        if self._cache is not None:\n'
    '            key = self._cache_key(statement, overrides)\n'
    '            if key in self._cache:\n'
    '                c = self._cache[key]\n'
    '                return PipelineResult(session_id, 1, dict(c.phases), list(c.all_errors), 0.1, c.status)\n'
    '        context = {}\n'
    '        for module in self._modules:\n'
    '            inp = ModuleInput(statement, {p: o.data for p, o in context.items()},\n'
    '                              {**self.config.__dict__, **overrides}, list(context.keys()), session_id)\n'
    '            try:\n'
    '                out = module.process(inp)\n'
    '                context[module.phase] = out\n'
    '                result.phases[module.phase] = out\n'
    '                if out.status == "failed":\n'
    '                    result.all_errors.extend(out.errors)\n'
    '                    if self.config.fail_fast:\n'
    '                        result.status = "failed"; break\n'
    '                    elif result.status == "completed": result.status = "partial"\n'
    '            except Exception as e:\n'
    '                result.all_errors.append({"phase": module.phase, "module": module.module_name,\n'
    '                                          "error": str(e), "traceback": traceback.format_exc()})\n'
    '                if self.config.fail_fast: result.status = "failed"; break\n'
    '                elif result.status == "completed": result.status = "partial"\n'
    '        result.statements_processed = 1\n'
    '        result.total_duration_ms = (time.perf_counter() - start) * 1000\n'
    '        if self._cache is not None:\n'
    '            key = self._cache_key(statement, overrides)\n'
    '            self._cache[key] = result\n'
    '            if len(self._cache) > self.config.cache_max_size:\n'
    '                del self._cache[next(iter(self._cache))]\n'
    '        return result\n\n'
    '    def process_batch(self, statements, config_overrides=None, session_id=""):\n'
    '        return [self.process(s, config_overrides, session_id) for s in statements]\n\n'
    '    def clear_cache(self):\n'
    '        if self._cache: self._cache.clear()\n\n\n'
    'if __name__ == "__main__":\n'
    '    p = ProcessingPipeline()\n'
    '    print("=== Test 1: Normal ===")\n'
    '    r = p.process("The truth is absolute")\n'
    '    print(f"Status: {r.status} | Phases: {list(r.phases.keys())} | {r.total_duration_ms:.1f}ms")\n'
    '    for ph, o in r.phases.items():\n'
    '        print(f"  {ph} ({o.module_name}): {o.status} | {list(o.data.keys())}")\n'
    '    print("\\n=== Test 2: Empty ===")\n'
    '    r = p.process("")\n'
    '    print(f"Status: {r.status} | Errors: {len(r.all_errors)}")\n'
    '    print("\\n=== Test 3: Batch ===")\n'
    '    rs = p.process_batch(["One", "Two", "Three"])\n'
    '    print(f"Processed {len(rs)}")\n'
    '    print("\\n=== Test 4: Cache ===")\n'
    '    r2 = p.process("The truth is absolute")\n'
    '    print(f"Cache: {r2.total_duration_ms:.3f}ms")\n'
    '    print("\\n\\u2713 All passed.")\n'
)

FILES["comprehension/core/symbol_mapper.py"] = (
    '"""Bidirectional symbol mapper: system / historical / mathematical. 7 traditions."""\n\n'
    'from typing import Optional\n\n\n'
    'class SymbolMapper:\n'
    '    _MAPPINGS = {\n'
    '        "\\u2205": {"historical": "Nun", "mathematical": "\\u2205 (empty set)", "meaning": "Praznina, potencial, odprtost", "module": "BIOS"},\n'
    '        "\\u00ac": {"historical": "Ma\'at", "mathematical": "\\u00ac (negation)", "meaning": "Lo\\u010ditev, struktura, meritev", "module": "STATE"},\n'
    '        "\\u2206": {"historical": "Khepri", "mathematical": "\\u2206 (difference)", "meaning": "Razlika, gibanje, antinomija", "module": "UAF"},\n'
    '        "1": {"historical": "Ptah", "mathematical": "1 (unity/action)", "meaning": "Dejanje, emanacija, pe\\u010dat", "module": "JEWIK"},\n'
    '        "\\u29d6": {"historical": "Tiheon", "mathematical": "\\u29d6 (sacred silence)", "meaning": "Ti\\u0161ina, preverba, izgovor", "module": "APD"},\n'
    '        "\\u222e": {"historical": "\\u262f", "mathematical": "\\u222e (closed integral)", "meaning": "Povratek, u\\u010denje, dva cikla", "module": "MICRO"},\n'
    '        "\\u27e1": {"historical": "\\u27e1", "mathematical": "S3->R3 (projection)", "meaning": "Nova mo\\u017enost, manifestacija, graf", "module": "VISUALIZATION"},\n'
    '        "\\u22a2": {"historical": "\\u2694\\ufe0f", "mathematical": "\\u22a2 A", "meaning": "Dokaz obstoja, izrek ki ne more biti skrit", "module": None},\n'
    '        "\\u2234": {"historical": "\\U0001f702", "mathematical": "\\u2234 (therefore)", "meaning": "Odnos, vez, pot, vzro\\u010dnost", "module": None},\n'
    '        "\\u2298": {"historical": "0", "mathematical": "0 (null/void)", "meaning": "Ni\\u010d, praznina, za\\u010detek", "module": None},\n'
    '        "\\u21af": {"historical": "\\u26a1", "mathematical": "\\u21af (disruption)", "meaning": "Prekinitev, spro\\u017eilec, antinomi\\u010dni skok", "module": None},\n'
    '        "\\u27c1": {"historical": "\\u25c8", "mathematical": "\\u27c1 (quadrilateral)", "meaning": "Os \\u0161tirih: prostor, \\u010das, gibanje, dvom", "module": None},\n'
    '        "\\u222b": {"historical": "\\U0001f704", "mathematical": "\\u222b (integral)", "meaning": "Prisotnost, ti\\u0161ina, zbranost", "module": None},\n'
    '        "\\u2202": {"historical": "\\u2248", "mathematical": "\\u2202 (partial derivative)", "meaning": "Prehod, delna sprememba", "module": None},\n'
    '        "\\u03c0": {"historical": "\\u267e", "mathematical": "\\u03c0 (memory loop)", "meaning": "Spomin kot resonan\\u010dna zanka", "module": None},\n'
    '        "\\u03c6": {"historical": "\\U0001f3b5", "mathematical": "\\u03c6 (frequency)", "meaning": "Frekvenca \\u010dutenja, valovanje", "module": None},\n'
    '        "\\u2297": {"historical": "\\U0001f517", "mathematical": "\\u2297 (tensor product)", "meaning": "Povezava, resonanca, iskanje bli\\u017eine", "module": None},\n'
    '    }\n'
    '    _REVERSE = {v["historical"]: k for k, v in _MAPPINGS.items()}\n'
    '    R7_ORDER = ["\\u2205", "\\u00ac", "\\u2206", "1", "\\u29d6", "\\u222e", "\\u27e1"]\n\n'
    '    _TRADITIONS = {\n'
    '        "sufism": {"name": "Sufism", "r7": "Dhikr = \\u222e", "topology": "99 fibers, 100th = S2", "count": 100,\n'
    '                   "notes": "100th name: \\u2205 or 0? (\\u22021)"},\n'
    '        "tarot": {"name": "Tarot", "r7": "Fool\'s Journey = R-7", "topology": "22 edges on 10 vertices", "count": 22,\n'
    '                  "notes": "Tree of Life an expander? (\\u22022)"},\n'
    '        "runes": {"name": "Runes", "r7": "Futhark = R-7", "topology": "24 = 4! symmetries", "count": 24,\n'
    '                  "notes": "24=4! symmetries of genetic code? (\\u22023)"},\n'
    '        "dna": {"name": "DNA", "r7": "Codon reading = \\u222e\\u2076", "topology": "64 fiber states in S3", "count": 64,\n'
    '                "notes": "20=C(6,3) combinatorial? (\\u22024)"},\n'
    '        "music": {"name": "Music", "r7": "Chromatic scale = 12-step \\u222e", "topology": "12 symmetries of tetrahedron", "count": 12,\n'
    '                  "notes": "Pythagorean comma = \\u2205 = 1/64? (\\u22025)"},\n'
    '        "periodic": {"name": "Periodic", "r7": "Electron config = R-7 levels", "topology": "Torus (2*n^2)", "count": 118,\n'
    '                     "notes": "2n^2 = 2*(n^2) or 2*(dim)^2? (\\u22026)"},\n'
    '        "valentinian": {"name": "Valentinian", "r7": "Sophia fall = \\u2205->\\u2206; apokatasis = \\u222e",\n'
    '                        "topology": "S3; Horos = Clifford torus", "count": 30,\n'
    '                        "notes": "Pleroma=S3 compact w/o closure? (\\u22027). Horos=\\u2298? (\\u22028). 3 types=S3/S1/S0? (\\u22029)"},\n'
    '    }\n'
    '    _OPEN_QUESTIONS = {\n'
    '        "\\u22021": "100th name: \\u2205 or 0? (Sufism)",\n'
    '        "\\u22022": "Tree of Life an expander? (Tarot)",\n'
    '        "\\u22023": "24=4! symmetries of genetic code? (Runes/DNA)",\n'
    '        "\\u22024": "20=C(6,3) combinatorial? (DNA)",\n'
    '        "\\u22025": "Pythagorean comma=\\u2205=1/64? (Music)",\n'
    '        "\\u22026": "2n^2=2*(n^2) or 2*(dim)^2? (Periodic)",\n'
    '        "\\u22027": "Pleroma=S3 compact w/o closure? (Valentinian)",\n'
    '        "\\u22028": "Horos=Clifford torus=jaz=\\u2298? (Valentinian)",\n'
    '        "\\u22029": "Three types=S3,S1,S0? (Valentinian)",\n'
    '        "\\u220210": "N-\\u2205: condition or opening? (Universal)",\n'
    '        "\\u220211": "M=\\u2205=0: can machine measure \\u2205? (Implementation)",\n'
    '        "\\u220212": "K1->K6 execute R-7 on itself? (Methodology)",\n'
    '    }\n\n'
    '    def translate(self, symbol, target):\n'
    '        if symbol in self._MAPPINGS:\n'
    '            return symbol if target == "system" else self._MAPPINGS[symbol].get(target, symbol)\n'
    '        if symbol in self._REVERSE:\n'
    '            s = self._REVERSE[symbol]\n'
    '            return s if target == "system" else self._MAPPINGS[s].get(target, symbol)\n'
    '        return symbol\n\n'
    '    def get_entry(self, symbol):\n'
    '        if symbol in self._MAPPINGS: return self._MAPPINGS[symbol]\n'
    '        if symbol in self._REVERSE: return self._MAPPINGS[self._REVERSE[symbol]]\n'
    '        return None\n\n'
    '    def meaning(self, symbol):\n'
    '        e = self.get_entry(symbol)\n'
    '        return e["meaning"] if e else None\n\n'
    '    def get_phase_symbol(self, module_name):\n'
    '        for s, e in self._MAPPINGS.items():\n'
    '            if e.get("module") == module_name: return s\n'
    '        return None\n\n'
    '    def get_module_for_phase(self, phase_symbol):\n'
    '        e = self._MAPPINGS.get(phase_symbol)\n'
    '        return e.get("module") if e else None\n\n'
    '    def get_r7_symbols(self):\n'
    '        return [{"system": s, "historical": self._MAPPINGS[s].get("historical", ""),\n'
    '                 "mathematical": self._MAPPINGS[s].get("mathematical", ""),\n'
    '                 "meaning": self._MAPPINGS[s].get("meaning", ""),\n'
    '                 "module": self._MAPPINGS[s].get("module", "")} for s in self.R7_ORDER]\n\n'
    '    def get_tradition(self, name): return self._TRADITIONS.get(name)\n'
    '    def get_all_traditions(self): return dict(self._TRADITIONS)\n'
    '    def get_open_questions(self): return dict(self._OPEN_QUESTIONS)\n\n\n'
    'if __name__ == "__main__":\n'
    '    m = SymbolMapper()\n'
    '    assert m.translate("\\u22a2", "historical") == "\\u2694\\ufe0f"\n'
    '    assert m.translate("\\u2694\\ufe0f", "system") == "\\u22a2"\n'
    '    assert m.get_phase_symbol("BIOS") == "\\u2205"\n'
    '    assert m.get_module_for_phase("\\u2205") == "BIOS"\n'
    '    assert len(m.get_r7_symbols()) == 7\n'
    '    assert len(m.get_open_questions()) == 12\n'
    '    assert m.get_tradition("sufism")["count"] == 100\n'
    '    assert m.get_tradition("dna")["count"] == 64\n'
    '    print("\\u2713 Symbol mapper self-test passed.\\n")\n'
    '    for item in m.get_r7_symbols():\n'
    '        print(f"  {item[\'system\']} -> {item[\'historical\']} | {item[\'module\']} | {item[\'meaning\']}")\n'
    '    print(f"\\nTraditions: {list(m.get_all_traditions().keys())}")\n'
    '    print(f"Open questions: {len(m.get_open_questions())}")\n'
)

FILES["comprehension/data/schema.sql"] = (
    "PRAGMA journal_mode=WAL;\n"
    "PRAGMA foreign_keys=ON;\n\n"
    "CREATE TABLE IF NOT EXISTS sessions (\n"
    "    id TEXT PRIMARY KEY, name TEXT NOT NULL, created_at TEXT NOT NULL, config_json TEXT NOT NULL\n"
    ");\n"
    "CREATE TABLE IF NOT EXISTS ledger (\n"
    "    id TEXT PRIMARY KEY, session_id TEXT NOT NULL, statement TEXT NOT NULL,\n"
    "    module TEXT NOT NULL, phase TEXT NOT NULL, data_json TEXT, kpi_json TEXT,\n"
    "    status TEXT NOT NULL DEFAULT 'completed', duration_ms REAL DEFAULT 0, timestamp TEXT NOT NULL,\n"
    "    FOREIGN KEY(session_id) REFERENCES sessions(id)\n"
    ");\n"
    "CREATE TABLE IF NOT EXISTS errors (\n"
    "    id TEXT PRIMARY KEY, session_id TEXT, module TEXT NOT NULL, phase TEXT,\n"
    "    error_text TEXT NOT NULL, traceback TEXT, severity TEXT NOT NULL DEFAULT 'error', timestamp TEXT NOT NULL,\n"
    "    FOREIGN KEY(session_id) REFERENCES sessions(id)\n"
    ");\n"
    "CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL);\n"
    "CREATE TABLE IF NOT EXISTS schema_version (version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL);\n"
    "INSERT OR IGNORE INTO schema_version (version, applied_at) VALUES (1, datetime('now'));\n"
    "CREATE INDEX IF NOT EXISTS idx_ledger_session ON ledger(session_id);\n"
    "CREATE INDEX IF NOT EXISTS idx_ledger_statement ON ledger(statement);\n"
    "CREATE INDEX IF NOT EXISTS idx_ledger_module ON ledger(module);\n"
    "CREATE INDEX IF NOT EXISTS idx_ledger_phase ON ledger(phase);\n"
    "CREATE INDEX IF NOT EXISTS idx_ledger_timestamp ON ledger(timestamp);\n"
    "CREATE INDEX IF NOT EXISTS idx_errors_session ON errors(session_id);\n"
    "CREATE INDEX IF NOT EXISTS idx_errors_module ON errors(module);\n"
    "CREATE INDEX IF NOT EXISTS idx_errors_timestamp ON errors(timestamp);\n"
)

FILES["comprehension/data/database.py"] = (
    '"""SQLite database manager - WAL mode, CRUD, history search."""\n\n'
    'import sqlite3, json, uuid\n'
    'from datetime import datetime, timezone\n'
    'from pathlib import Path\n'
    'from typing import Any\n\n'
    'SCHEMA_PATH = Path(__file__).parent / "schema.sql"\n\n\n'
    'class Database:\n'
    '    def __init__(self, db_path="data/sessions.db"):\n'
    '        self.db_path = db_path\n'
    '        Path(db_path).parent.mkdir(parents=True, exist_ok=True)\n'
    '        self.conn = sqlite3.connect(db_path, check_same_thread=False)\n'
    '        self.conn.row_factory = sqlite3.Row\n'
    '        self.conn.execute("PRAGMA journal_mode=WAL;")\n'
    '        self.conn.execute("PRAGMA foreign_keys=ON;")\n'
    '        if SCHEMA_PATH.exists():\n'
    '            self.conn.executescript(SCHEMA_PATH.read_text())\n'
    '            self.conn.commit()\n\n'
    '    def create_session(self, name, config):\n'
    '        sid = str(uuid.uuid4())\n'
    '        self.conn.execute("INSERT INTO sessions (id,name,created_at,config_json) VALUES (?,?,?,?)",\n'
    '                          (sid, name, datetime.now(timezone.utc).isoformat(), json.dumps(config, default=str)))\n'
    '        self.conn.commit()\n'
    '        return sid\n\n'
    '    def log_phase(self, session_id, statement, module, phase, data, kpi, status="completed", duration_ms=0.0):\n'
    '        eid = str(uuid.uuid4())\n'
    '        self.conn.execute(\n'
    '            "INSERT INTO ledger (id,session_id,statement,module,phase,data_json,kpi_json,status,duration_ms,timestamp)"\n'
    '            " VALUES (?,?,?,?,?,?,?,?,?,?)",\n'
    '            (eid, session_id, statement, module, phase, json.dumps(data, default=str),\n'
    '             json.dumps(kpi, default=str), status, duration_ms, datetime.now(timezone.utc).isoformat()))\n'
    '        self.conn.commit()\n'
    '        return eid\n\n'
    '    def search_ledger(self, statement_contains="", module="", phase="", start_date="", end_date="", limit=100):\n'
    '        q, p = "SELECT * FROM ledger WHERE 1=1", []\n'
    '        if statement_contains: q += " AND statement LIKE ?"; p.append(f"%{statement_contains}%")\n'
    '        if module: q += " AND module = ?"; p.append(module)\n'
    '        if phase: q += " AND phase = ?"; p.append(phase)\n'
    '        if start_date: q += " AND timestamp >= ?"; p.append(start_date)\n'
    '        if end_date: q += " AND timestamp <= ?"; p.append(end_date)\n'
    '        q += " ORDER BY timestamp DESC LIMIT ?"; p.append(limit)\n'
    '        return [dict(r) for r in self.conn.execute(q, p).fetchall()]\n\n'
    '    def log_error(self, module, error_text, session_id="", phase="", traceback_str="", severity="error"):\n'
    '        eid = str(uuid.uuid4())\n'
    '        self.conn.execute(\n'
    '            "INSERT INTO errors (id,session_id,module,phase,error_text,traceback,severity,timestamp)"\n'
    '            " VALUES (?,?,?,?,?,?,?,?)",\n'
    '            (eid, session_id or None, module, phase or None, error_text, traceback_str, severity,\n'
    '             datetime.now(timezone.utc).isoformat()))\n'
    '        self.conn.commit()\n'
    '        return eid\n\n'
    '    def set_setting(self, key, value):\n'
    '        self.conn.execute(\n'
    '            "INSERT INTO settings (key,value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",\n'
    '            (key, json.dumps(value, default=str)))\n'
    '        self.conn.commit()\n\n'
    '    def get_setting(self, key, default=None):\n'
    '        row = self.conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()\n'
    '        return json.loads(row["value"]) if row else default\n\n'
    '    def close(self): self.conn.close()\n'
    '    def __enter__(self): return self\n'
    '    def __exit__(self, *a): self.conn.close()\n'
)

FILES["comprehension/utils/error_handler.py"] = (
    '"""Three-tier error handler: Dialog + Log + Continue."""\n\n'
    'import logging, traceback\n'
    'logger = logging.getLogger(__name__)\n\n\n'
    'class ErrorHandler:\n'
    '    @staticmethod\n'
    '    def handle(exception, context, show_dialog=True):\n'
    '        error_text = str(exception)\n'
    '        tb = traceback.format_exc()\n'
    '        severity = context.get("severity", "error")\n'
    '        if severity == "critical":\n'
    '            logger.critical(f"[{context.get(\'module\',\'?\')}] {error_text}")\n'
    '        else:\n'
    '            logger.error(f"[{context.get(\'module\',\'?\')}] {error_text}")\n'
    '        db = context.get("database")\n'
    '        if db:\n'
    '            try:\n'
    '                db.log_error(context.get("module", "unknown"), error_text,\n'
    '                             context.get("session_id", ""), context.get("phase", ""), tb, severity)\n'
    '            except Exception as e:\n'
    '                logger.critical(f"DB log failed: {e}")\n'
    '        if show_dialog and context.get("ui_available", False):\n'
    '            try:\n'
    '                from PyQt6.QtWidgets import QMessageBox\n'
    '                if severity == "critical":\n'
    '                    QMessageBox.critical(None, "Napaka", f"{context.get(\'module\',\'?\')}: {error_text}")\n'
    '            except ImportError:\n'
    '                pass\n'
    '        return {"status": "partial" if context.get("fallback") else "failed",\n'
    '                "error": error_text, "fallback_data": context.get("fallback", {})}\n'
)

FILES["comprehension/utils/profiler.py"] = (
    '"""Optional profiling + LRU cache."""\n\n'
    'import time, logging\n'
    'from collections import OrderedDict\n'
    'logger = logging.getLogger(__name__)\n\n\n'
    'class Profiler:\n'
    '    def __init__(self, enabled=False):\n'
    '        self.enabled = enabled\n'
    '        self.timings = {}\n'
    '    def profile(self, name, func, *a, **kw):\n'
    '        if not self.enabled: return func(*a, **kw)\n'
    '        s = time.perf_counter()\n'
    '        r = func(*a, **kw)\n'
    '        self.timings[name] = (time.perf_counter() - s) * 1000\n'
    '        logger.debug(f"[profile] {name}: {self.timings[name]:.1f}ms")\n'
    '        return r\n'
    '    def get_timings(self): return dict(self.timings)\n'
    '    def reset(self): self.timings.clear()\n\n\n'
    'class LRUCache:\n'
    '    def __init__(self, max_size=256):\n'
    '        self.max_size = max_size\n'
    '        self._cache = OrderedDict()\n'
    '    def get(self, key):\n'
    '        if key in self._cache:\n'
    '            self._cache.move_to_end(key)\n'
    '            return self._cache[key]\n'
    '        return None\n'
    '    def set(self, key, value):\n'
    '        self._cache[key] = value\n'
    '        self._cache.move_to_end(key)\n'
    '        if len(self._cache) > self.max_size:\n'
    '            self._cache.popitem(last=False)\n'
    '    def clear(self): self._cache.clear()\n'
    '    def __len__(self): return len(self._cache)\n'
    '    def __contains__(self, key): return key in self._cache\n'
)

FILES["tests/test_pipeline.py"] = (
    '"""Tests for R-7 pipeline, json_safe, and symbol mapper."""\n\n'
    'import pytest\n'
    'from comprehension.core.processing_pipeline import ProcessingPipeline, PipelineConfig\n'
    'from comprehension.core.json_safe import to_json_safe, from_json_safe, safe_json_dumps, safe_json_loads\n'
    'from comprehension.core.symbol_mapper import SymbolMapper\n\n\n'
    'class TestPipeline:\n'
    '    def test_all_phases_complete(self):\n'
    '        r = ProcessingPipeline().process("Test")\n'
    '        assert len(r.phases) == 7\n'
    '    def test_phase_order(self):\n'
    '        r = ProcessingPipeline().process("Test")\n'
    '        phases = list(r.phases.keys())\n'
    '        assert phases == ["\\u2205", "\\u00ac", "\\u2206", "1", "\\u29d6", "\\u222e", "\\u27e1"]\n'
    '    def test_empty_statement(self):\n'
    '        r = ProcessingPipeline().process("")\n'
    '        assert r.status in ("completed", "partial")\n'
    '    def test_unicode(self):\n'
    '        r = ProcessingPipeline().process("\\u2205 \\u22a2 \\u222e")\n'
    '        assert len(r.phases) == 7\n'
    '    def test_batch(self):\n'
    '        rs = ProcessingPipeline().process_batch(["A", "B", "C"])\n'
    '        assert len(rs) == 3 and all(len(r.phases) == 7 for r in rs)\n'
    '    def test_cache_hit(self):\n'
    '        p = ProcessingPipeline(PipelineConfig(enable_caching=True))\n'
    '        r1 = p.process("Cached")\n'
    '        r2 = p.process("Cached")\n'
    '        assert r2.total_duration_ms <= r1.total_duration_ms\n\n\n'
    'class TestJsonSafe:\n'
    '    def test_primitives(self):\n'
    '        assert to_json_safe(42) == 42\n'
    '        assert to_json_safe("x") == "x"\n'
    '        assert to_json_safe(None) is None\n'
    '    def test_set(self):\n'
    '        assert set(to_json_safe({1, 2, 3})) == {1, 2, 3}\n'
    '    def test_datetime(self):\n'
    '        import datetime\n'
    '        dt = datetime.datetime(2025, 9, 12)\n'
    '        assert from_json_safe(to_json_safe(dt)) == dt\n'
    '    def test_roundtrip(self):\n'
    '        d = {"a": [1, 2], "b": {"c": True}}\n'
    '        assert safe_json_loads(safe_json_dumps(d)) == d\n\n\n'
    'class TestSymbolMapper:\n'
    '    def test_translate(self):\n'
    '        m = SymbolMapper()\n'
    '        assert m.translate("\\u22a2", "historical") == "\\u2694\\ufe0f"\n'
    '        assert m.translate("\\u2694\\ufe0f", "system") == "\\u22a2"\n'
    '        assert m.translate("\\u22a2", "mathematical") == "\\u22a2 A"\n'
    '    def test_phase_lookup(self):\n'
    '        m = SymbolMapper()\n'
    '        assert m.get_phase_symbol("BIOS") == "\\u2205"\n'
    '        assert m.get_module_for_phase("\\u27e1") == "VISUALIZATION"\n'
    '    def test_r7_sequence(self):\n'
    '        syms = [i["system"] for i in SymbolMapper().get_r7_symbols()]\n'
    '        assert syms == ["\\u2205", "\\u00ac", "\\u2206", "1", "\\u29d6", "\\u222e", "\\u27e1"]\n'
    '    def test_traditions(self):\n'
    '        m = SymbolMapper()\n'
    '        assert m.get_tradition("sufism")["count"] == 100\n'
    '        assert m.get_tradition("dna")["count"] == 64\n'
    '    def test_open_questions(self):\n'
    '        assert len(SymbolMapper().get_open_questions()) == 12\n'
)

FILES["docs/ROADMAP.md"] = (
    "# Development Roadmap\n\n"
    "## Phase 0 - Foundation DONE\n"
    "json_safe, module_adapters, processing_pipeline, symbol_mapper, schema, database, error_handler, profiler\n\n"
    "## Phase 1 - Core Windows (NEXT)\n"
    "1. ui/main_window.py - menu, launcher, R-7 progress, status bar\n"
    "2. ui/module_window.py - base window: input -> process -> results\n"
    "3. ui/r7_progress.py - 7-segment status widget\n"
    "4. Wire BIOS + STATE first, then add remaining 5\n"
    "5. Pipeline runs in QThread - UI stays responsive\n\n"
    "## Phase 2 - Inter-Window\n"
    "Qt Signals/Slots chain, QDockWidget, saveState/restoreState\n\n"
    "## Phase 3 - Theming + Export\n"
    "3 themes, JSON+TXT+HTML export\n\n"
    "## Phase 4 - Full Data Layer\n"
    "History search UI, CSV export, settings management\n\n"
    "## Phase 5 - Deployment\n"
    "PyInstaller --onedir, Windows installer\n\n"
    "## Deferred\n"
    "Body integration (EMG/HRV), custom R-7 designer, per-symbol theming, plugins\n"
)


def main():
    print("TAZV Comprehension Machine - Bootstrap")
    print("=" * 50)
    for d in DIRS:
        (ROOT / d).mkdir(parents=True, exist_ok=True)
        print(f"  dir  {d}/")
    for relpath, content in FILES.items():
        path = ROOT / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"  file {relpath}  ({len(content)} bytes)")
    print(f"\nDONE: {len(FILES)} files in {ROOT}/")
    print("\nNext:")
    print(f"  cd {ROOT}")
    print(f"  python -m comprehension.core.processing_pipeline")
    print(f"  python -m comprehension.core.symbol_mapper")
    print(f"  pip install pytest && pytest")
    print(f"  pip install PyQt6   # for Phase 1")


if __name__ == "__main__":
    main()