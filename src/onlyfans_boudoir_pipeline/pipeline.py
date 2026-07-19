"""Orquestração do pipeline de produção de conteúdo."""

from dataclasses import dataclass
from typing import List

from .agent import ContentRequest, InteractiveAgent


@dataclass(frozen=True)
class ContentPiece:
    """Peça de conteúdo gerada pelo pipeline."""

    model_id: str
    theme: str
    prompt: str


class BoudoirPipeline:
    """Pipeline autônomo de produção de conteúdo boudoir."""

    def __init__(self, agent: InteractiveAgent) -> None:
        self._agent = agent

    def generate_batch(
        self, requests: List[ContentRequest]
    ) -> List[ContentPiece]:
        """Gera um lote de peças de conteúdo.

        Args:
            requests: Lista de solicitações de conteúdo.

        Returns:
            Lista de peças de conteúdo geradas.
        """
        pieces: List[ContentPiece] = []
        for request in requests:
            prompt = self._agent.build_prompt(request)
            pieces.append(
                ContentPiece(
                    model_id=request.model_id,
                    theme=request.theme,
                    prompt=prompt,
                )
            )
        return pieces

    def generate_for_all_models(self, theme: str, mood: str) -> List[ContentPiece]:
        """Gera uma peça de conteúdo para cada modelo disponível.

        Args:
            theme: Tema da sessão.
            mood: Tom emocional desejado.

        Returns:
            Lista de peças de conteúdo, uma por modelo.
        """
        requests = [
            ContentRequest(
                model_id=model.id,
                theme=theme,
                mood=mood,
                extras=[],
            )
            for model in self._agent.available_models()
        ]
        return self.generate_batch(requests)
