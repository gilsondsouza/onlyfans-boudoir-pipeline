"""Carregamento e acesso aos perfis de modelos."""

from __future__ import annotations

from src.config import get_models
from src.models.base_model import ModelProfile


def load_all_profiles() -> dict[str, ModelProfile]:
    """Carrega todos os perfis de modelos habilitados da configuração."""
    raw = get_models()
    return {name: ModelProfile.from_dict(name, data) for name, data in raw.items()}


def get_profile(name: str) -> ModelProfile:
    """Retorna o perfil de um modelo específico pelo nome."""
    profiles = load_all_profiles()
    if name not in profiles:
        available = ", ".join(profiles.keys())
        raise KeyError(f"Modelo '{name}' não encontrado. Disponíveis: {available}")
    return profiles[name]
