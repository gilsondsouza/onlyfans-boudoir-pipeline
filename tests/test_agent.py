"""
Testes para o agente interativo (src/agent/chat.py).
"""

from __future__ import annotations

import pytest

from src.agent.chat import ChatAgent, DemoBackend, build_backend


# ---------------------------------------------------------------------------
# Testes do DemoBackend
# ---------------------------------------------------------------------------


class TestDemoBackend:
    def test_returns_string(self):
        backend = DemoBackend()
        result = backend.complete([{"role": "user", "content": "olá"}])
        assert isinstance(result, str)
        assert len(result) > 0

    def test_rotates_responses(self):
        backend = DemoBackend()
        responses = {backend.complete([]) for _ in range(6)}
        # Deve ter pelo menos 2 respostas distintas em 6 chamadas (ciclo de 3)
        assert len(responses) >= 2


# ---------------------------------------------------------------------------
# Testes do ChatAgent
# ---------------------------------------------------------------------------


class TestChatAgent:
    def _make_agent(self) -> ChatAgent:
        return ChatAgent(backend=DemoBackend())

    def test_chat_returns_string(self):
        agent = self._make_agent()
        response = agent.chat("Olá!")
        assert isinstance(response, str)
        assert len(response) > 0

    def test_chat_appends_to_history(self):
        agent = self._make_agent()
        agent.chat("Mensagem 1")
        assert len(agent.history) == 2  # user + assistant

    def test_chat_multiple_turns_grow_history(self):
        agent = self._make_agent()
        agent.chat("Turno 1")
        agent.chat("Turno 2")
        assert len(agent.history) == 4  # 2 turnos × (user + assistant)

    def test_reset_clears_history(self):
        agent = self._make_agent()
        agent.chat("Mensagem")
        agent.reset()
        assert agent.history == []

    def test_history_contains_user_message(self):
        agent = self._make_agent()
        agent.chat("teste de histórico")
        user_msgs = [m for m in agent.history if m["role"] == "user"]
        assert any("teste de histórico" in m["content"] for m in user_msgs)

    def test_history_contains_assistant_response(self):
        agent = self._make_agent()
        agent.chat("qualquer coisa")
        assistant_msgs = [m for m in agent.history if m["role"] == "assistant"]
        assert len(assistant_msgs) == 1


# ---------------------------------------------------------------------------
# Testes do build_backend
# ---------------------------------------------------------------------------


class TestBuildBackend:
    def test_demo_provider_returns_demo_backend(self):
        backend = build_backend("demo")
        assert isinstance(backend, DemoBackend)

    def test_none_provider_falls_back_to_demo(self, monkeypatch):
        monkeypatch.delenv("LLM_PROVIDER", raising=False)
        backend = build_backend(None)
        assert isinstance(backend, DemoBackend)

    def test_env_var_demo_returns_demo_backend(self, monkeypatch):
        monkeypatch.setenv("LLM_PROVIDER", "demo")
        backend = build_backend(None)
        assert isinstance(backend, DemoBackend)

    def test_openai_without_package_raises_import_error(self, monkeypatch):
        import sys
        monkeypatch.setitem(sys.modules, "openai", None)  # type: ignore[arg-type]
        with pytest.raises(ImportError, match="openai"):
            build_backend("openai")

    def test_anthropic_without_package_raises_import_error(self, monkeypatch):
        import sys
        monkeypatch.setitem(sys.modules, "anthropic", None)  # type: ignore[arg-type]
        with pytest.raises(ImportError, match="anthropic"):
            build_backend("anthropic")
