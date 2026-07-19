"""
Módulo de configuração do pipeline.
Carrega e valida settings.yaml, models.yaml e schedule.yaml.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env (se existir)
load_dotenv()

CONFIG_DIR = Path(__file__).parent.parent / "config"


def _expand_env(value: Any) -> Any:
    """Substitui referências a variáveis de ambiente no formato ${VAR:default}."""
    if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
        inner = value[2:-1]
        if ":" in inner:
            var_name, default = inner.split(":", 1)
        else:
            var_name, default = inner, ""
        return os.environ.get(var_name, default)
    if isinstance(value, dict):
        return {k: _expand_env(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_expand_env(item) for item in value]
    return value


def load_yaml(filename: str) -> dict:
    """Carrega um arquivo YAML da pasta config/ e expande variáveis de ambiente."""
    path = CONFIG_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Arquivo de configuração não encontrado: {path}")
    with open(path, encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return _expand_env(raw)


def get_settings() -> dict:
    """Retorna as configurações globais do pipeline."""
    return load_yaml("settings.yaml")


def get_models() -> dict:
    """Retorna os perfis de todos os modelos configurados."""
    data = load_yaml("models.yaml")
    return {
        name: profile
        for name, profile in data.get("models", {}).items()
        if profile.get("enabled", True)
    }


def get_schedule() -> dict:
    """Retorna as regras de agendamento."""
    return load_yaml("schedule.yaml")
