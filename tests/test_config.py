"""
Testes para carregamento de configurações YAML.
"""

import os
from pathlib import Path
import pytest
import yaml

from src.config import _expand_env, load_yaml


# ---------------------------------------------------------------------------
# Testes de expansão de variáveis de ambiente
# ---------------------------------------------------------------------------


class TestExpandEnv:
    def test_simple_string_unchanged(self):
        assert _expand_env("hello") == "hello"

    def test_env_var_without_default(self, monkeypatch):
        monkeypatch.setenv("MY_VAR", "secret_value")
        assert _expand_env("${MY_VAR}") == "secret_value"

    def test_env_var_with_default_uses_env(self, monkeypatch):
        monkeypatch.setenv("MY_VAR", "from_env")
        assert _expand_env("${MY_VAR:default_val}") == "from_env"

    def test_env_var_with_default_fallback(self, monkeypatch):
        monkeypatch.delenv("MISSING_VAR", raising=False)
        assert _expand_env("${MISSING_VAR:fallback}") == "fallback"

    def test_env_var_missing_no_default_returns_empty(self, monkeypatch):
        monkeypatch.delenv("MISSING_VAR", raising=False)
        assert _expand_env("${MISSING_VAR}") == ""

    def test_dict_values_expanded(self, monkeypatch):
        monkeypatch.setenv("DB_URL", "sqlite:///test.db")
        result = _expand_env({"url": "${DB_URL}"})
        assert result == {"url": "sqlite:///test.db"}

    def test_list_values_expanded(self, monkeypatch):
        monkeypatch.setenv("HOST", "localhost")
        result = _expand_env(["${HOST}", "plain"])
        assert result == ["localhost", "plain"]

    def test_integer_unchanged(self):
        assert _expand_env(42) == 42

    def test_boolean_unchanged(self):
        assert _expand_env(True) is True


# ---------------------------------------------------------------------------
# Testes de carregamento de YAML
# ---------------------------------------------------------------------------


class TestLoadYaml:
    def test_loads_settings_yaml(self):
        config = load_yaml("settings.yaml")
        assert "pipeline" in config
        assert config["pipeline"]["name"] == "onlyfans-boudoir-pipeline"

    def test_loads_models_yaml(self):
        config = load_yaml("models.yaml")
        assert "models" in config
        models = config["models"]
        assert len(models) == 7

    def test_models_yaml_has_all_seven(self):
        config = load_yaml("models.yaml")
        expected = {"aurora", "valentina", "sofia", "luna", "bianca", "isabelle", "marina"}
        assert set(config["models"].keys()) == expected

    def test_loads_schedule_yaml(self):
        config = load_yaml("schedule.yaml")
        assert "scheduler" in config

    def test_missing_file_raises_error(self):
        with pytest.raises(FileNotFoundError):
            load_yaml("nonexistent_file.yaml")
