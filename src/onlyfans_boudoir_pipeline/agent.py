"""Interactive agent for content selection and generation."""

from dataclasses import dataclass
from typing import List, Optional

from .models import ModelProfile, ModelStyle, get_model_by_id, list_models


@dataclass(frozen=True)
class ContentRequest:
    """Content generation request."""

    model_id: str
    theme: str
    mood: str
    extras: List[str]


class InteractiveAgent:
    """Agent that helps choose models and build content prompts."""

    def __init__(self) -> None:
        self._models = list_models()

    def available_models(self) -> List[ModelProfile]:
        """Returns all available models."""
        return self._models

    def suggest_models(self, style: Optional[ModelStyle] = None) -> List[ModelProfile]:
        """Suggests models, optionally filtered by style."""
        if style is None:
            return self._models
        return [m for m in self._models if m.style == style]

    def build_prompt(self, request: ContentRequest) -> str:
        """Builds a prompt from a content request.

        Args:
            request: Request data.

        Returns:
            String containing the final prompt.

        Raises:
            ValueError: If the specified model does not exist.
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
