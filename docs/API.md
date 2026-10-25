# API Reference — config-loader

All public names are exported from the top-level package:

```python
from config_loader import ValidationError, load_config, merge_dicts
```

---

## `load_config(path, *, env_prefix="APP_")`

Load a JSON config file, apply environment overrides, and validate the result.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `path` | `str \| Path` | required | Path to a JSON file |
| `env_prefix` | `str` | `"APP_"` | Prefix that marks environment variables as overrides |

**Returns** `dict` — the merged and validated configuration.

**Raises**

- `FileNotFoundError` — the file does not exist
- `ValidationError` — invalid JSON, non-object top level, missing required keys (`host`, `port`), or `port` outside 1–65535

### Example 1 — basic load

```python
from config_loader import load_config

config = load_config("config.json")
print(config["host"])   # localhost
print(config["port"])   # 8080
```

### Example 2 — environment override

```bash
export APP_PORT=9090
```

```python
from config_loader import load_config

config = load_config("config.json")
print(config["port"])   # 9090 — env var won
```

### Example 3 — handling validation errors

```python
from config_loader import ValidationError, load_config

try:
    load_config("broken.json")
except ValidationError as exc:
    print(f"Bad config: {exc}")
    # e.g. Bad config: missing required keys: port
```

---

## `merge_dicts(base, override)`

Recursively merge two dicts and return a **new** dict. Nested dicts merge
key by key; any other type in `override` replaces the `base` value.
Inputs are never mutated.

```python
from config_loader import merge_dicts

merged = merge_dicts(
    {"db": {"user": "x", "pool": 5}},
    {"db": {"user": "y"}},
)
# {"db": {"user": "y", "pool": 5}}
```

---

## `ValidationError`

Subclass of `ValueError`. Raised by `load_config` for every configuration
problem, so one `except` clause covers all validation failures.
