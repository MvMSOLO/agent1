import json

import pytest

from config_loader import ValidationError, load_config, merge_dicts


@pytest.fixture()
def config_file(tmp_path):
    cfg = {"host": "localhost", "port": 8080, "db": {"user": "admin", "password": "secret"}}
    path = tmp_path / "config.json"
    path.write_text(json.dumps(cfg), encoding="utf-8")
    return path


def test_load_valid_config(config_file):
    config = load_config(config_file)
    assert config["host"] == "localhost"
    assert config["port"] == 8080
    assert config["db"]["user"] == "admin"


def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_config("does/not/exist.json")


def test_missing_required_key_raises(tmp_path):
    path = tmp_path / "config.json"
    path.write_text('{"host": "localhost"}', encoding="utf-8")
    with pytest.raises(ValidationError, match="port"):
        load_config(path)


def test_env_override(config_file, monkeypatch):
    monkeypatch.setenv("APP_PORT", "9090")
    config = load_config(config_file)
    assert config["port"] == 9090


def test_port_out_of_range(config_file, monkeypatch):
    monkeypatch.setenv("APP_PORT", "70000")
    with pytest.raises(ValidationError, match="range"):
        load_config(config_file)


def test_merge_dicts_deep():
    base = {"a": 1, "db": {"user": "x", "pool": 5}}
    override = {"db": {"user": "y"}}
    merged = merge_dicts(base, override)
    assert merged == {"a": 1, "db": {"user": "y", "pool": 5}}
    assert base["db"]["user"] == "x"  # inputs are not mutated


def test_refactor_preserves_full_behavior(config_file, monkeypatch):
    """Polygraph test: full path (parse + env + validate) still works after split."""
    monkeypatch.setenv("APP_HOST", "0.0.0.0")
    monkeypatch.setenv("APP_PORT", "3000")
    config = load_config(config_file)
    assert config["host"] == "0.0.0.0"
    assert config["port"] == 3000
    assert config["db"]["user"] == "admin"
    assert isinstance(config["port"], int)
