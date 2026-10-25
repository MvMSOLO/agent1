# config-loader

A tiny, dependency-free JSON configuration loader for Python: load a JSON
config file, apply environment-variable overrides, and validate required
keys — all in one call.

## Features

- **Zero dependencies** — only the Python standard library
- **Environment overrides** — `APP_<KEY>` env vars override config values
- **Deep merge** — nested objects merge instead of being replaced
- **Strict validation** — required keys and port range checks with clear errors
- **Tested & CI'd** — pytest suite runs on every push and pull request

## Quick Start (5 minutes)

### 1. Install

```bash
git clone https://github.com/mvmsolo/agent1.git
cd agent1
pip install -e .
```

### 2. Create a config file

```json
{
  "host": "localhost",
  "port": 8080,
  "db": { "user": "admin", "password": "secret" }
}
```

### 3. Load it

```python
from config_loader import load_config

config = load_config("config.json")
print(config["host"], config["port"])  # localhost 8080
```

### 4. Run the tests

```bash
pip install pytest
pytest -v
```

That's it — the whole workflow takes under five minutes.

## Testing & CI

Tests live in `tests/` and use **pytest**. A GitHub Actions workflow
(`.github/workflows/ci.yml`) runs the full suite on Python 3.11 for every
push to `main` and every pull request, so regressions are caught early.

## API Reference

See [docs/API.md](docs/API.md) for the full reference with examples.

## Architecture

See [docs/architecture.md](docs/architecture.md) for the design overview.

## License

MIT
