"""Tiny, dependency-free JSON configuration loader.

Loads a JSON configuration file, applies environment-variable overrides,
and validates required keys. Designed to be small, explicit, and easy
to extend by the rest of the team.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

__all__ = ["ValidationError", "load_config", "merge_dicts"]

REQUIRED_KEYS = ("host", "port")


class ValidationError(ValueError):
    """Raised when a configuration file is missing required keys or has invalid values."""


def merge_dicts(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively merge override into base and return a new dict.

    Nested dicts are merged key by key; every other type in override
    replaces the value from base. Neither input dict is mutated.
    """
    result: Dict[str, Any] = dict(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result


def _parse_json(path: str | Path) -> Dict[str, Any]:
    """Read and parse a JSON config file. Raises FileNotFoundError or ValidationError."""
    config_path = Path(path)
    if not config_path.is_file():
        raise FileNotFoundError(f"config file not found: {config_path}")

    try:
        raw: Dict[str, Any] = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValidationError(f"invalid JSON in {config_path}: {exc}") from exc

    if not isinstance(raw, dict):
        raise ValidationError(f"top-level JSON value in {config_path} must be an object")

    return raw


def _apply_env_overrides(raw: Dict[str, Any], env_prefix: str = "APP_") -> Dict[str, Any]:
    """Merge environment-variable overrides into the raw config."""
    env_overrides = {
        key[len(env_prefix):].lower(): os.environ[key]
        for key in os.environ
        if key.startswith(env_prefix)
    }
    return merge_dicts(raw, env_overrides)


def _validate(config: Dict[str, Any]) -> Dict[str, Any]:
    """Validate required keys and coerce/check port. Returns the (possibly mutated) config."""
    missing = [k for k in REQUIRED_KEYS if k not in config]
    if missing:
        raise ValidationError(f"missing required keys: {', '.join(sorted(missing))}")

    try:
        config["port"] = int(config["port"])
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"port must be an integer, got {config['port']!r}") from exc
    if not 1 <= config["port"] <= 65535:
        raise ValidationError(f"port out of range 1-65535: {config['port']}")

    return config


def load_config(path: str | Path, *, env_prefix: str = "APP_") -> Dict[str, Any]:
    """Load a JSON config file and apply environment overrides.

    Rules:
      * path must point to an existing, readable JSON file.
      * Any environment variable APP_<KEY> overrides the lower-cased
        config key, e.g. APP_PORT -> port.
      * The result must contain all keys in REQUIRED_KEYS;
        port must be an integer in the range 1-65535.

    Raises:
        FileNotFoundError: if path does not exist.
        ValidationError: if JSON is invalid or required keys are missing/invalid.
    """
    raw = _parse_json(path)
    config = _apply_env_overrides(raw, env_prefix=env_prefix)
    return _validate(config)
