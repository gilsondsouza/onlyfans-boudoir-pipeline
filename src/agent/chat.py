"""
Agente interativo de IA para gestão do pipeline de conteúdo boudoir.

Permite ao operador conversar em linguagem natural para:
- Consultar métricas de todos os perfis
- Solicitar sugestões de conteúdo
- Ajustar o calendário editorial
- Receber alertas e relatórios
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable


@runtime_checkable
class LLMBackend(Protocol):
    """Interface que qualquer backend de LLM deve implementar."""

    def complete(self, messages: list[dict]) -> str:
        """Envia uma lista de mensagens e retorna a resposta do modelo."""
        ...


# ---------------------------------------------------------------------------
# Backend de demonstração (sem LLM real — útil para testes e demo)
# ---------------------------------------------------------------------------

_DEMO_RESPONSES: list[str] = [
    "Olá! Sou o agente do pipeline boudoir. Esta é uma resposta de demonstração. "
    "Configure LLM_PROVIDER e LLM_API_KEY no .env para ativar respostas reais.",
    "Em modo demo, não consigo consultar métricas ao vivo. "
    "Conecte um provedor de LLM real para análises completas.",
    "Dica: defina LLM_PROVIDER=openai e LLM_API_KEY=<sua-chave> no arquivo .env.",
]


class DemoBackend:
    """Backend de demonstração que retorna respostas fixas sem chamar nenhuma API."""

    def __init__(self) -> None:
        self._turn = 0

    def complete(self, messages: list[dict]) -> str:
        response = _DEMO_RESPONSES[self._turn % len(_DEMO_RESPONSES)]
        self._turn += 1
        return response


# ---------------------------------------------------------------------------
# Fábrica de backend
# ---------------------------------------------------------------------------


def build_backend(provider: str | None = None) -> LLMBackend:
    """
    Cria e retorna o backend de LLM configurado.

    Suporta:
    - ``openai``   — usa openai.OpenAI (requer LLM_API_KEY)
    - ``anthropic`` — usa anthropic.Anthropic (requer LLM_API_KEY)
    - ``demo``     — respostas fixas, sem API (padrão quando nenhuma chave está presente)
    """
    provider = provider or os.environ.get("LLM_PROVIDER", "demo")

    if provider == "openai":
        return _build_openai_backend()
    if provider == "anthropic":
        return _build_anthropic_backend()

    return DemoBackend()


def _build_openai_backend() -> LLMBackend:
    try:
        import openai  # type: ignore[import]
    except ImportError as exc:
        raise ImportError(
            "O pacote 'openai' não está instalado. "
            "Execute: pip install openai"
        ) from exc

    api_key = os.environ.get("LLM_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "Defina LLM_API_KEY (ou OPENAI_API_KEY) no arquivo .env para usar o backend OpenAI."
        )

    model = os.environ.get("LLM_MODEL", "gpt-4o")
    client = openai.OpenAI(api_key=api_key)

    class _OpenAIBackend:
        def complete(self, messages: list[dict]) -> str:
            response = client.chat.completions.create(model=model, messages=messages)
            return response.choices[0].message.content or ""

    return _OpenAIBackend()


def _build_anthropic_backend() -> LLMBackend:
    try:
        import anthropic as ant  # type: ignore[import]
    except ImportError as exc:
        raise ImportError(
            "O pacote 'anthropic' não está instalado. "
            "Execute: pip install anthropic"
        ) from exc

    api_key = os.environ.get("LLM_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "Defina LLM_API_KEY (ou ANTHROPIC_API_KEY) no arquivo .env para usar o backend Anthropic."
        )

    model = os.environ.get("LLM_MODEL", "claude-3-5-sonnet-20241022")
    client = ant.Anthropic(api_key=api_key)

    class _AnthropicBackend:
        def complete(self, messages: list[dict]) -> str:
            # Separa a mensagem de sistema das mensagens de conversa
            system = next((m["content"] for m in messages if m["role"] == "system"), "")
            conv = [m for m in messages if m["role"] != "system"]
            response = client.messages.create(
                model=model,
                max_tokens=4096,
                system=system,
                messages=conv,
            )
            return response.content[0].text

    return _AnthropicBackend()


# ---------------------------------------------------------------------------
# Agente principal
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = """Você é o agente do OnlyFans Boudoir Pipeline — um assistente especializado
em gestão de conteúdo para 7 perfis de modelos (Aurora, Valentina, Sofia, Luna, Bianca,
Isabelle e Marina). Seu papel é:
- Analisar métricas de engajamento e receita
- Sugerir pautas e calendários editoriais
- Alertar sobre anomalias (quedas de subscritores, falhas de upload)
- Responder perguntas do operador de forma objetiva e orientada a dados
Responda sempre em português do Brasil."""


@dataclass
class ChatAgent:
    """
    Agente conversacional que mantém histórico de mensagens e se comunica
    com um backend de LLM configurável.
    """

    backend: LLMBackend
    system_prompt: str = _SYSTEM_PROMPT
    history: list[dict] = field(default_factory=list)

    def chat(self, user_message: str) -> str:
        """Envia uma mensagem do operador e retorna a resposta do agente."""
        self.history.append({"role": "user", "content": user_message})

        messages = [{"role": "system", "content": self.system_prompt}] + self.history

        response = self.backend.complete(messages)

        self.history.append({"role": "assistant", "content": response})
        return response

    def reset(self) -> None:
        """Limpa o histórico da conversa."""
        self.history.clear()
