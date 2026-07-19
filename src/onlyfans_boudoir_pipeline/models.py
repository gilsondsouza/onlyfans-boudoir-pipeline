"""Character models for the boudoir pipeline."""

from dataclasses import dataclass
from enum import Enum
from typing import List


class ModelStyle(str, Enum):
    """Supported photographic styles."""

    ROMANTIC = "romantic"
    EDITORIAL = "editorial"
    MOODY = "moody"
    VINTAGE = "vintage"
    MINIMALIST = "minimalist"
    GLAMOUR = "glamour"
    ARTISTIC = "artistic"


@dataclass(frozen=True)
class ModelProfile:
    """Model profile for the pipeline."""

    id: str
    name: str
    style: ModelStyle
    traits: List[str]
    prompt_prefix: str


MODELS: tuple[ModelProfile, ...] = (
    ModelProfile(
        id="aurora",
        name="Aurora",
        style=ModelStyle.ROMANTIC,
        traits=["soft light", "pastel tones", "intimate"],
        prompt_prefix="romantic boudoir portrait, soft natural light",
    ),
    ModelProfile(
        id="luna",
        name="Luna",
        style=ModelStyle.MOODY,
        traits=["dramatic shadows", "film grain", "mysterious"],
        prompt_prefix="moody boudoir portrait, dramatic shadows",
    ),
    ModelProfile(
        id="stella",
        name="Stella",
        style=ModelStyle.EDITORIAL,
        traits=["high fashion", "clean lines", "confident"],
        prompt_prefix="editorial boudoir portrait, high fashion lighting",
    ),
    ModelProfile(
        id="ruby",
        name="Ruby",
        style=ModelStyle.VINTAGE,
        traits=["retro colors", "classic poses", "timeless"],
        prompt_prefix="vintage boudoir portrait, retro color palette",
    ),
    ModelProfile(
        id="ivy",
        name="Ivy",
        style=ModelStyle.MINIMALIST,
        traits=["negative space", "neutral tones", "serene"],
        prompt_prefix="minimalist boudoir portrait, neutral tones",
    ),
    ModelProfile(
        id="sable",
        name="Sable",
        style=ModelStyle.GLAMOUR,
        traits=["luxury setting", "polished finish", "bold"],
        prompt_prefix="glamour boudoir portrait, luxury setting",
    ),
    ModelProfile(
        id="iris",
        name="Iris",
        style=ModelStyle.ARTISTIC,
        traits=["experimental angles", "painterly", "expressive"],
        prompt_prefix="artistic boudoir portrait, experimental composition",
    ),
)


def get_model_by_id(model_id: str) -> ModelProfile:
    """Returns a model by identifier.

    Args:
        model_id: Unique model identifier.

    Raises:
        ValueError: If no model is found with the provided ID.
    """
    for model in MODELS:
        if model.id == model_id:
            return model
    raise ValueError(f"Model with ID '{model_id}' not found")


def list_models() -> List[ModelProfile]:
    """Lists all available model profiles."""
    return list(MODELS)
