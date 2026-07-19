"""
Testes para carregamento de perfis de modelos.
"""

import pytest
from src.models.base_model import ModelProfile, PersonaConfig, PostingConfig, PricingConfig


# ---------------------------------------------------------------------------
# Dados de teste
# ---------------------------------------------------------------------------

AURORA_DICT = {
    "display_name": "Aurora",
    "enabled": True,
    "persona": {
        "description": "Fotografia natural e minimalista",
        "aesthetic": "natural_minimalist",
        "tone_of_voice": "amigável, autêntica",
        "language": "pt-BR",
    },
    "style": {
        "color_palette": ["#F5E6D3", "#E8D5B7"],
        "mood": ["sereno", "natural"],
    },
    "posting": {
        "frequency": "2/day",
        "peak_hours": [18, 20, 22],
        "timezone": "America/Sao_Paulo",
        "content_types": {"photos": 0.70, "videos": 0.20, "stories": 0.10},
    },
    "pricing": {
        "subscription_usd": 9.99,
        "ppv_enabled": True,
        "ppv_price_range": [5, 25],
    },
}


# ---------------------------------------------------------------------------
# Testes de ModelProfile
# ---------------------------------------------------------------------------


class TestModelProfileFromDict:
    def test_creates_profile_with_correct_name(self):
        profile = ModelProfile.from_dict("aurora", AURORA_DICT)
        assert profile.name == "aurora"

    def test_creates_profile_with_correct_display_name(self):
        profile = ModelProfile.from_dict("aurora", AURORA_DICT)
        assert profile.display_name == "Aurora"

    def test_profile_is_enabled_by_default(self):
        profile = ModelProfile.from_dict("aurora", AURORA_DICT)
        assert profile.enabled is True

    def test_persona_fields_populated(self):
        profile = ModelProfile.from_dict("aurora", AURORA_DICT)
        assert profile.persona.aesthetic == "natural_minimalist"
        assert profile.persona.language == "pt-BR"
        assert "amigável" in profile.persona.tone_of_voice

    def test_posting_peak_hours(self):
        profile = ModelProfile.from_dict("aurora", AURORA_DICT)
        assert profile.posting.peak_hours == [18, 20, 22]

    def test_posting_frequency(self):
        profile = ModelProfile.from_dict("aurora", AURORA_DICT)
        assert profile.posting.frequency == "2/day"

    def test_pricing_subscription(self):
        profile = ModelProfile.from_dict("aurora", AURORA_DICT)
        assert profile.pricing.subscription_usd == 9.99

    def test_pricing_ppv_enabled(self):
        profile = ModelProfile.from_dict("aurora", AURORA_DICT)
        assert profile.pricing.ppv_enabled is True

    def test_pricing_ppv_range(self):
        profile = ModelProfile.from_dict("aurora", AURORA_DICT)
        assert profile.pricing.ppv_price_range == (5, 25)

    def test_style_color_palette(self):
        profile = ModelProfile.from_dict("aurora", AURORA_DICT)
        assert "#F5E6D3" in profile.style.color_palette

    def test_repr_contains_name(self):
        profile = ModelProfile.from_dict("aurora", AURORA_DICT)
        assert "aurora" in repr(profile)


class TestModelProfileDefaults:
    def test_empty_dict_uses_defaults(self):
        profile = ModelProfile.from_dict("test_model", {"display_name": "Test"})
        assert profile.enabled is True
        assert profile.posting.frequency == "1/day"
        assert profile.pricing.subscription_usd == 9.99
        assert profile.pricing.ppv_enabled is False

    def test_disabled_model(self):
        profile = ModelProfile.from_dict("ghost", {"display_name": "Ghost", "enabled": False})
        assert profile.enabled is False

    def test_display_name_falls_back_to_capitalized_name(self):
        profile = ModelProfile.from_dict("luna", {})
        assert profile.display_name == "Luna"
