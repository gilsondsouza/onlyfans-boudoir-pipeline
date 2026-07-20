"""Testes da API do dashboard web."""

from __future__ import annotations

from fastapi.testclient import TestClient

from src.web.app import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_models() -> None:
    response = client.get("/api/models")
    assert response.status_code == 200
    models = response.json()
    assert len(models) == 7
    assert {m["name"] for m in models} >= {"aurora", "valentina", "marina"}


def test_pipeline_run_dry() -> None:
    response = client.post(
        "/api/pipeline/run",
        json={"model_name": "aurora", "dry_run": True},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["dry_run"] is True
    assert len(body["steps"]) == 5


def test_agent_chat_and_reset() -> None:
    chat = client.post(
        "/api/agent/chat",
        json={"message": "Olá", "session_id": "test-web"},
    )
    assert chat.status_code == 200
    assert "reply" in chat.json()

    reset = client.post("/api/agent/reset", json={"session_id": "test-web"})
    assert reset.status_code == 200
    assert reset.json()["status"] == "reset"


def test_index_serves_html() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Boudoir" in response.text
