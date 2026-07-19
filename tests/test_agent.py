"""Testes para o agente interativo."""

import pytest

from onlyfans_boudoir_pipeline.agent import ContentRequest, InteractiveAgent
from onlyfans_boudoir_pipeline.models import ModelStyle


def test_agent_lists_all_models():
    agent = InteractiveAgent()
    assert len(agent.available_models()) == 7


def test_agent_suggests_by_style():
    agent = InteractiveAgent()
    romantic = agent.suggest_models(ModelStyle.ROMANTIC)
    assert len(romantic) == 1
    assert romantic[0].id == "aurora"


def test_agent_builds_prompt():
    agent = InteractiveAgent()
    request = ContentRequest(
        model_id="luna",
        theme="rainy window",
        mood="melancholic",
        extras=["cinematic framing"],
    )
    prompt = agent.build_prompt(request)
    assert "luna" not in prompt.lower()
    assert "moody boudoir portrait" in prompt
    assert "rainy window" in prompt
    assert "melancholic" in prompt
    assert "cinematic framing" in prompt


def test_agent_builds_prompt_unknown_model():
    agent = InteractiveAgent()
    request = ContentRequest(
        model_id="unknown",
        theme="test",
        mood="test",
        extras=[],
    )
    with pytest.raises(ValueError):
        agent.build_prompt(request)
