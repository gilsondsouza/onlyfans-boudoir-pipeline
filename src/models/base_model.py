"""
Perfil base de modelo.
Define a estrutura e validação de cada um dos 7 perfis.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PostingConfig:
    frequency: str = "1/day"
    peak_hours: list[int] = field(default_factory=lambda: [18, 20])
    timezone: str = "America/Sao_Paulo"
    content_types: dict[str, float] = field(
        default_factory=lambda: {"photos": 0.70, "videos": 0.20, "stories": 0.10}
    )


@dataclass
class PricingConfig:
    subscription_usd: float = 9.99
    ppv_enabled: bool = False
    ppv_price_range: tuple[float, float] = (5.0, 25.0)


@dataclass
class StyleConfig:
    color_palette: list[str] = field(default_factory=list)
    mood: list[str] = field(default_factory=list)


@dataclass
class PersonaConfig:
    description: str = ""
    aesthetic: str = ""
    tone_of_voice: str = ""
    language: str = "pt-BR"


@dataclass
class ModelProfile:
    """Representação completa do perfil de um modelo."""

    name: str
    display_name: str
    enabled: bool = True
    persona: PersonaConfig = field(default_factory=PersonaConfig)
    style: StyleConfig = field(default_factory=StyleConfig)
    posting: PostingConfig = field(default_factory=PostingConfig)
    pricing: PricingConfig = field(default_factory=PricingConfig)

    @classmethod
    def from_dict(cls, name: str, data: dict) -> "ModelProfile":
        """Cria um ModelProfile a partir de um dicionário de configuração."""
        persona_data = data.get("persona", {})
        style_data = data.get("style", {})
        posting_data = data.get("posting", {})
        pricing_data = data.get("pricing", {})

        ppv_range = pricing_data.get("ppv_price_range", [5, 25])

        return cls(
            name=name,
            display_name=data.get("display_name", name.capitalize()),
            enabled=data.get("enabled", True),
            persona=PersonaConfig(
                description=persona_data.get("description", ""),
                aesthetic=persona_data.get("aesthetic", ""),
                tone_of_voice=persona_data.get("tone_of_voice", ""),
                language=persona_data.get("language", "pt-BR"),
            ),
            style=StyleConfig(
                color_palette=style_data.get("color_palette", []),
                mood=style_data.get("mood", []),
            ),
            posting=PostingConfig(
                frequency=posting_data.get("frequency", "1/day"),
                peak_hours=posting_data.get("peak_hours", [18, 20]),
                timezone=posting_data.get("timezone", "America/Sao_Paulo"),
                content_types=posting_data.get(
                    "content_types",
                    {"photos": 0.70, "videos": 0.20, "stories": 0.10},
                ),
            ),
            pricing=PricingConfig(
                subscription_usd=pricing_data.get("subscription_usd", 9.99),
                ppv_enabled=pricing_data.get("ppv_enabled", False),
                ppv_price_range=(ppv_range[0], ppv_range[1]),
            ),
        )

    def __repr__(self) -> str:
        return (
            f"ModelProfile(name={self.name!r}, "
            f"display_name={self.display_name!r}, "
            f"aesthetic={self.persona.aesthetic!r})"
        )
