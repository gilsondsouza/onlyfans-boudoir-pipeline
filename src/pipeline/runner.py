"""
Orquestrador do pipeline de produção de conteúdo.
Coordena ingestão → processamento → curadoria → agendamento → upload.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class StepStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class StepResult:
    name: str
    status: StepStatus
    message: str = ""
    items_processed: int = 0


@dataclass
class PipelineRun:
    """Resultado de uma execução completa do pipeline."""

    model_name: str
    dry_run: bool = False
    steps: list[StepResult] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return all(s.status in (StepStatus.SUCCESS, StepStatus.SKIPPED) for s in self.steps)

    @property
    def summary(self) -> str:
        lines = [f"Pipeline run — model: {self.model_name} | dry_run: {self.dry_run}"]
        for step in self.steps:
            icon = {"success": "✅", "failed": "❌", "skipped": "⏭️", "pending": "⏳", "running": "🔄"}.get(
                step.status.value, "❓"
            )
            lines.append(f"  {icon} {step.name}: {step.status.value} — {step.message}")
        return "\n".join(lines)


def run_pipeline(model_name: str, *, dry_run: bool = False) -> PipelineRun:
    """
    Executa o pipeline completo para um perfil de modelo.

    Em ``dry_run=True`` todos os passos são simulados sem efetuar uploads reais.
    """
    run = PipelineRun(model_name=model_name, dry_run=dry_run)

    steps = [
        ("ingest", _step_ingest),
        ("process", _step_process),
        ("curate", _step_curate),
        ("schedule", _step_schedule),
        ("upload", _step_upload),
    ]

    for step_name, step_fn in steps:
        logger.info("Iniciando etapa '%s' para modelo '%s'", step_name, model_name)
        result = step_fn(model_name=model_name, dry_run=dry_run)
        run.steps.append(result)
        if result.status == StepStatus.FAILED:
            logger.error("Etapa '%s' falhou: %s", step_name, result.message)
            break

    return run


# ---------------------------------------------------------------------------
# Implementações das etapas (stubs prontos para extensão)
# ---------------------------------------------------------------------------


def _step_ingest(*, model_name: str, dry_run: bool) -> StepResult:
    """Detecta novos arquivos de mídia para o modelo."""
    logger.debug("[%s] ingest: dry_run=%s", model_name, dry_run)
    return StepResult(
        name="ingest",
        status=StepStatus.SUCCESS,
        message="Nenhuma mídia nova encontrada (stub)",
        items_processed=0,
    )


def _step_process(*, model_name: str, dry_run: bool) -> StepResult:
    """Aplica marca d'água e redimensionamento."""
    logger.debug("[%s] process: dry_run=%s", model_name, dry_run)
    return StepResult(
        name="process",
        status=StepStatus.SKIPPED,
        message="Nenhum item para processar",
    )


def _step_curate(*, model_name: str, dry_run: bool) -> StepResult:
    """Curadoria assistida por IA — seleciona as melhores peças."""
    logger.debug("[%s] curate: dry_run=%s", model_name, dry_run)
    return StepResult(
        name="curate",
        status=StepStatus.SKIPPED,
        message="Nenhum item para curar",
    )


def _step_schedule(*, model_name: str, dry_run: bool) -> StepResult:
    """Determina o melhor horário de publicação."""
    logger.debug("[%s] schedule: dry_run=%s", model_name, dry_run)
    return StepResult(
        name="schedule",
        status=StepStatus.SKIPPED,
        message="Nenhum item para agendar",
    )


def _step_upload(*, model_name: str, dry_run: bool) -> StepResult:
    """Faz upload do conteúdo agendado para o OnlyFans."""
    if dry_run:
        return StepResult(
            name="upload",
            status=StepStatus.SKIPPED,
            message="dry_run=True — upload não realizado",
        )
    logger.debug("[%s] upload", model_name)
    return StepResult(
        name="upload",
        status=StepStatus.SKIPPED,
        message="Nenhum item na fila de upload",
    )
