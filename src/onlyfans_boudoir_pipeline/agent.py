"""Agente interativo para seleção e geração de conteúdo."""

from dataclasses import dataclass
from typing import List, Optional

from .models import ModelProfile, ModelStyle, get_model_by_id, list_models


@dataclass(frozen=True)
class ContentRequest:
    """Solicitação de geração de conteúdo."""

    model_id: str
    theme: str
    mood: str
    extras: List[str]


class InteractiveAgent:
    """Agente que ajuda a escolher modelos e montar prompts de conteúdo."""

    def __init__(self) -> None:
        self._models = list_models()

    def available_models(self) -> List[ModelProfile]:
        """Retorna todos os modelos disponíveis."""
        return self._models

    def suggest_models(self, style: Optional[ModelStyle] = None) -> List[ModelProfile]:
        """Sugere modelos, opcionalmente filtrados por estilo."""
        if style is None:
            return self._models
        return [m for m in self._models if m.style == style]

    def build_prompt(self, request: ContentRequest) -> str:
        """Monta um prompt a partir de uma solicitação de conteúdo.

        Args:
            request: Dados da solicitação.

        Returns:
            String contendo o prompt final.

        Raises:
            ValueError: Se o modelo informado não existir.
        """
        model = get_model_by_id(request.model_id)
        parts = [
            model.prompt_prefix,
            f"theme: {request.theme}",
            f"mood: {request.mood}",
        ]
        if request.extras:
            parts.append(", ".join(request.extras))
        return ", ".join(parts)
