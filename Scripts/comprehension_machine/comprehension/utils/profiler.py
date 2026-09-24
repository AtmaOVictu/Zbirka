"""Optional profiling + LRU cache."""

import time, logging
from collections import OrderedDict
logger = logging.getLogger(__name__)


class Profiler:
    def __init__(self, enabled=False):
        self.enabled = enabled
        self.timings = {}
    def profile(self, name, func, *a, **kw):
        if not self.enabled: return func(*a, **kw)
        s = time.perf_counter()
        r = func(*a, **kw)
        self.timings[name] = (time.perf_counter() - s) * 1000
        logger.debug(f"[profile] {name}: {self.timings[name]:.1f}ms")
        return r
    def get_timings(self): return dict(self.timings)
    def reset(self): self.timings.clear()


class LRUCache:
    def __init__(self, max_size=256):
        self.max_size = max_size
        self._cache = OrderedDict()
    def get(self, key):
        if key in self._cache:
            self._cache.move_to_end(key)
            return self._cache[key]
        return None
    def set(self, key, value):
        self._cache[key] = value
        self._cache.move_to_end(key)
        if len(self._cache) > self.max_size:
            self._cache.popitem(last=False)
    def clear(self): self._cache.clear()
    def __len__(self): return len(self._cache)
    def __contains__(self, key): return key in self._cache
