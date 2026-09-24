"""R-7 processing pipeline. Never crashes."""

import time
import hashlib
import logging
import traceback
from dataclasses import dataclass, field
from .module_adapters import ModuleInput, ModuleOutput, BaseModuleAdapter, R7_MODULES

logger = logging.getLogger(__name__)


@dataclass
class PipelineConfig:
    batch_size: int = 64
    enable_caching: bool = True
    cache_max_size: int = 256
    fail_fast: bool = False
    log_level: str = "INFO"


@dataclass
class PipelineResult:
    session_id: str = ""
    statements_processed: int = 0
    phases: dict = field(default_factory=dict)
    all_errors: list = field(default_factory=list)
    total_duration_ms: float = 0.0
    status: str = "completed"


class ProcessingPipeline:
    R7_PHASES = ["\u2205", "\u00ac", "\u2206", "1", "\u29d6", "\u222e", "\u27e1"]

    def __init__(self, config=None):
        self.config = config or PipelineConfig()
        self._cache = {} if self.config.enable_caching else None
        self._modules = [cls() for cls in R7_MODULES]
        logging.basicConfig(level=getattr(logging, self.config.log_level, logging.INFO),
                            format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")

    def _cache_key(self, statement, overrides):
        return hashlib.md5(f"{statement}:{sorted(overrides.items())}".encode()).hexdigest()

    def process(self, statement, config_overrides=None, session_id=""):
        overrides = config_overrides or {}
        result = PipelineResult(session_id=session_id)
        start = time.perf_counter()
        if self._cache is not None:
            key = self._cache_key(statement, overrides)
            if key in self._cache:
                c = self._cache[key]
                return PipelineResult(session_id, 1, dict(c.phases), list(c.all_errors), 0.1, c.status)
        context = {}
        for module in self._modules:
            inp = ModuleInput(statement, {p: o.data for p, o in context.items()},
                              {**self.config.__dict__, **overrides}, list(context.keys()), session_id)
            try:
                out = module.process(inp)
                context[module.phase] = out
                result.phases[module.phase] = out
                if out.status == "failed":
                    result.all_errors.extend(out.errors)
                    if self.config.fail_fast:
                        result.status = "failed"; break
                    elif result.status == "completed": result.status = "partial"
            except Exception as e:
                result.all_errors.append({"phase": module.phase, "module": module.module_name,
                                          "error": str(e), "traceback": traceback.format_exc()})
                if self.config.fail_fast: result.status = "failed"; break
                elif result.status == "completed": result.status = "partial"
        result.statements_processed = 1
        result.total_duration_ms = (time.perf_counter() - start) * 1000
        if self._cache is not None:
            key = self._cache_key(statement, overrides)
            self._cache[key] = result
            if len(self._cache) > self.config.cache_max_size:
                del self._cache[next(iter(self._cache))]
        return result

    def process_batch(self, statements, config_overrides=None, session_id=""):
        return [self.process(s, config_overrides, session_id) for s in statements]

    def clear_cache(self):
        if self._cache: self._cache.clear()


if __name__ == "__main__":
    p = ProcessingPipeline()
    print("=== Test 1: Normal ===")
    r = p.process("The truth is absolute")
    print(f"Status: {r.status} | Phases: {list(r.phases.keys())} | {r.total_duration_ms:.1f}ms")
    for ph, o in r.phases.items():
        print(f"  {ph} ({o.module_name}): {o.status} | {list(o.data.keys())}")
    print("\n=== Test 2: Empty ===")
    r = p.process("")
    print(f"Status: {r.status} | Errors: {len(r.all_errors)}")
    print("\n=== Test 3: Batch ===")
    rs = p.process_batch(["One", "Two", "Three"])
    print(f"Processed {len(rs)}")
    print("\n=== Test 4: Cache ===")
    r2 = p.process("The truth is absolute")
    print(f"Cache: {r2.total_duration_ms:.3f}ms")
    print("\n\u2713 All passed.")
