"""JSON-safe serialization for dataclasses, Enums, numpy, datetime, sets."""

import dataclasses
import enum
import datetime
import json
from typing import Any


def to_json_safe(obj: Any) -> Any:
    if obj is None or isinstance(obj, (bool, int, float, str)):
        return obj
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return {"__dataclass__": obj.__class__.__name__,
                "fields": {f.name: to_json_safe(getattr(obj, f.name)) for f in dataclasses.fields(obj)}}
    if isinstance(obj, enum.Enum):
        return {"__enum__": f"{obj.__class__.__name__}.{obj.name}"}
    if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
        return {"__datetime__": obj.isoformat()}
    if isinstance(obj, datetime.timedelta):
        return {"__timedelta__": obj.total_seconds()}
    try:
        import numpy as np
        if isinstance(obj, np.integer): return int(obj)
        if isinstance(obj, np.floating): return float(obj)
        if isinstance(obj, np.bool_): return bool(obj)
        if isinstance(obj, np.ndarray):
            return {"__ndarray__": True, "data": obj.tolist(), "dtype": str(obj.dtype), "shape": list(obj.shape)}
        if isinstance(obj, np.generic): return obj.item()
    except ImportError:
        pass
    if isinstance(obj, dict):
        return {str(k): to_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set, frozenset)):
        return [to_json_safe(item) for item in obj]
    if hasattr(obj, "__dict__"):
        return {"__object__": obj.__class__.__name__, "attrs": to_json_safe(obj.__dict__)}
    return str(obj)


def from_json_safe(obj: Any) -> Any:
    if not isinstance(obj, dict):
        return [from_json_safe(i) for i in obj] if isinstance(obj, list) else obj
    if "__datetime__" in obj:
        for p in (datetime.datetime.fromisoformat, datetime.date.fromisoformat, datetime.time.fromisoformat):
            try: return p(obj["__datetime__"])
            except (ValueError, TypeError): continue
        return obj["__datetime__"]
    if "__timedelta__" in obj: return datetime.timedelta(seconds=obj["__timedelta__"])
    if "__ndarray__" in obj:
        try:
            import numpy as np
            return np.array(obj["data"], dtype=obj["dtype"]).reshape(obj["shape"])
        except (ImportError, ValueError): return obj["data"]
    if "__enum__" in obj: return obj["__enum__"]
    if "__dataclass__" in obj: return obj["fields"]
    if "__object__" in obj: return obj["attrs"]
    return {k: from_json_safe(v) for k, v in obj.items()}


def safe_json_dumps(obj, **kw): return json.dumps(to_json_safe(obj), **kw)
def safe_json_loads(s, reconstruct=False, **kw):
    r = json.loads(s, **kw)
    return from_json_safe(r) if reconstruct else r
