"""config_loader: a tiny JSON configuration loader."""

from .loader import ValidationError, load_config, merge_dicts

__all__ = ["ValidationError", "load_config", "merge_dicts"]
__version__ = "0.1.0"
