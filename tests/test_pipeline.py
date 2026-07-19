"""Testes para o pipeline de produção de conteúdo."""

from onlyfans_boudoir_pipeline.agent import ContentRequest, InteractiveAgent
from onlyfans_boudoir_pipeline.pipeline import BoudoirPipeline


def test_pipeline_generate_batch():
    agent = InteractiveAgent()
    pipeline = BoudoirPipeline(agent)
    requests = [
        ContentRequest(
            model_id="stella",
            theme="hotel suite",
            mood="confident",
            extras=["gold accents"],
        )
    ]
    pieces = pipeline.generate_batch(requests)
    assert len(pieces) == 1
    assert pieces[0].model_id == "stella"
    assert pieces[0].theme == "hotel suite"
    assert "gold accents" in pieces[0].prompt


def test_pipeline_generate_for_all_models():
    agent = InteractiveAgent()
    pipeline = BoudoirPipeline(agent)
    pieces = pipeline.generate_for_all_models("summer evening", "relaxed")
    assert len(pieces) == 7
    model_ids = {p.model_id for p in pieces}
    assert len(model_ids) == 7
    assert all("summer evening" in p.prompt for p in pieces)
    assert all("relaxed" in p.prompt for p in pieces)
