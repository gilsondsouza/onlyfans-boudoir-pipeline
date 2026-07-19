"""Tests for the models module."""

import pytest

from onlyfans_boudoir_pipeline.models import (
    MODELS,
    ModelStyle,
    get_model_by_id,
    list_models,
)


def test_seven_models_defined():
    assert len(MODELS) == 7


def test_list_models_returns_all():
    assert len(list_models()) == 7


def test_get_model_by_id_success():
    model = get_model_by_id("aurora")
    assert model.name == "Aurora"
    assert model.style == ModelStyle.ROMANTIC


def test_get_model_by_id_failure():
    with pytest.raises(ValueError):
        get_model_by_id("not-a-model")


def test_all_styles_are_unique_groups():
    styles = {m.style for m in MODELS}
    assert len(styles) == 7
