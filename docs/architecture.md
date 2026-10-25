# Architecture — config-loader

## Goals

1. **Small and explicit** — one responsibility (config loading), no dependencies
2. **Predictable precedence** — file < environment, always
3. **Fail fast** — invalid configs raise before they reach application code

## Module layout

```
src/config_loader/
  __init__.py    # public API re-exports (load_config, merge_dicts, ValidationError)
  loader.py      # implementation: parsing, env overrides, validation
tests/
  test_loader.py # pytest suite covering loader + merge behavior
```

## Design decisions

- **Package `src/` layout** — forces an installed import path, so tests run
  against the installed package exactly like end users see it.
- **Env overrides applied after parsing** — `APP_<KEY>` values are lower-cased
  and deep-merged into the parsed dict, so nested keys can be overridden
  individually without rewriting whole sections.
- **One exception type (`ValidationError`)`** — callers need a single
  `except` for every config failure, while `FileNotFoundError` stays a
  distinct, standard signal.
- **Validation in `load_config`, not in constructors** — there is exactly
  one entry point that can produce an invalid config, which keeps the
  invariant easy to reason about and to test.

## Extension points (planned)

- Additional required keys or per-key validators
- YAML support behind the same `load_config` signature
