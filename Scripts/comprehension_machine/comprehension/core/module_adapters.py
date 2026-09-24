"""Module interface adapters for the R-7 pipeline."""

import time
import traceback
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

from .json_safe import to_json_safe


@dataclass
class ModuleInput:
    statement: str
    context: dict = field(default_factory=dict)
    config: dict = field(default_factory=dict)
    phase_history: list = field(default_factory=list)
    session_id: str = ""


@dataclass
class ModuleOutput:
    phase: str
    module_name: str
    data: dict = field(default_factory=dict)
    kpi: dict = field(default_factory=dict)
    errors: list = field(default_factory=list)
    duration_ms: float = 0.0
    status: str = "completed"


@runtime_checkable
class ModuleProtocol(Protocol):
    phase: str
    module_name: str
    def process(self, input: ModuleInput) -> ModuleOutput: ...


class BaseModuleAdapter:
    def __init__(self, phase, module_name):
        self.phase = phase
        self.module_name = module_name

    def process(self, input):
        start = time.perf_counter()
        errors, data, kpi, status = [], {}, {}, "completed"
        try:
            result = self.run(input)
            if isinstance(result, dict):
                data = result.get("data", result)
                kpi = result.get("kpi", {})
                if result.get("errors"):
                    errors.extend(result["errors"])
                    status = "partial" if data else "failed"
            elif isinstance(result, ModuleOutput):
                data, kpi, errors, status = result.data, result.kpi, result.errors, result.status
            else:
                data = {"raw": to_json_safe(result)}
        except Exception as e:
            errors.append({"module": self.module_name, "error": str(e), "traceback": traceback.format_exc()})
            status = "failed"
        return ModuleOutput(self.phase, self.module_name, to_json_safe(data),
                            to_json_safe(kpi), to_json_safe(errors),
                            (time.perf_counter() - start) * 1000, status)

    def run(self, input):
        raise NotImplementedError(f"{self.module_name}.run() not implemented")


class BIOSAdapter(BaseModuleAdapter):
    def __init__(self): super().__init__("\u2205", "BIOS")
    def run(self, i):
        return {"data": {"statement": i.statement, "tokens": i.statement.split(), "char_count": len(i.statement)},
                "kpi": {"phase_completeness": 1.0}}


class StateAdapter(BaseModuleAdapter):
    def __init__(self): super().__init__("\u00ac", "STATE")
    def run(self, i):
        bd = i.context.get("\u2205", {}).get("data", {})
        return {"data": {"structure": "basic", "word_count": len(bd.get("tokens", []))},
                "kpi": {"\u03ba": 0.75, "\u03c7": 0.50}}


class UAFAdapter(BaseModuleAdapter):
    def __init__(self): super().__init__("\u2206", "UAF")
    def run(self, i): return {"data": {"antinomies": [], "tension_score": 0.0}, "kpi": {"antinomy_count": 0}}


class JEWIKAdapter(BaseModuleAdapter):
    def __init__(self): super().__init__("1", "JEWIK")
    def run(self, i): return {"data": {"layers": [], "emanation": "none"}, "kpi": {"layer_count": 0}}


class APDAdapter(BaseModuleAdapter):
    def __init__(self): super().__init__("\u29d6", "APD")
    def run(self, i): return {"data": {"sealed": True, "verification": "auto"}, "kpi": {"seal_confidence": 0.80}}


class MicroAdapter(BaseModuleAdapter):
    def __init__(self): super().__init__("\u222e", "MICRO")
    def run(self, i): return {"data": {"patterns": [], "hopf_state": 0}, "kpi": {"pattern_count": 0}}


class VisualizationAdapter(BaseModuleAdapter):
    def __init__(self): super().__init__("\u27e1", "VISUALIZATION")
    def run(self, i): return {"data": {"graph": {"nodes": [], "edges": []}}, "kpi": {"projection_complete": 1.0}}


R7_MODULES = [BIOSAdapter, StateAdapter, UAFAdapter, JEWIKAdapter,
              APDAdapter, MicroAdapter, VisualizationAdapter]
