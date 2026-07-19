"""
Testes para o orquestrador do pipeline (src/pipeline/runner.py).
"""

from __future__ import annotations

import pytest

from src.pipeline.runner import (
    PipelineRun,
    StepResult,
    StepStatus,
    run_pipeline,
)


# ---------------------------------------------------------------------------
# Testes de StepResult
# ---------------------------------------------------------------------------


class TestStepResult:
    def test_default_message_is_empty(self):
        step = StepResult(name="ingest", status=StepStatus.SUCCESS)
        assert step.message == ""

    def test_default_items_processed_is_zero(self):
        step = StepResult(name="ingest", status=StepStatus.SUCCESS)
        assert step.items_processed == 0


# ---------------------------------------------------------------------------
# Testes de PipelineRun
# ---------------------------------------------------------------------------


class TestPipelineRun:
    def _make_run(self, statuses: list[StepStatus]) -> PipelineRun:
        run = PipelineRun(model_name="aurora")
        for i, status in enumerate(statuses):
            run.steps.append(StepResult(name=f"step_{i}", status=status))
        return run

    def test_success_when_all_steps_succeed(self):
        run = self._make_run([StepStatus.SUCCESS, StepStatus.SUCCESS])
        assert run.success is True

    def test_success_when_all_steps_skipped(self):
        run = self._make_run([StepStatus.SKIPPED, StepStatus.SKIPPED])
        assert run.success is True

    def test_success_mixed_success_and_skipped(self):
        run = self._make_run([StepStatus.SUCCESS, StepStatus.SKIPPED])
        assert run.success is True

    def test_failure_when_any_step_fails(self):
        run = self._make_run([StepStatus.SUCCESS, StepStatus.FAILED])
        assert run.success is False

    def test_summary_contains_model_name(self):
        run = PipelineRun(model_name="valentina")
        assert "valentina" in run.summary

    def test_summary_contains_step_names(self):
        run = self._make_run([StepStatus.SUCCESS])
        assert "step_0" in run.summary


# ---------------------------------------------------------------------------
# Testes de run_pipeline
# ---------------------------------------------------------------------------


class TestRunPipeline:
    def test_returns_pipeline_run_instance(self):
        result = run_pipeline("aurora", dry_run=True)
        assert isinstance(result, PipelineRun)

    def test_model_name_preserved(self):
        result = run_pipeline("luna", dry_run=True)
        assert result.model_name == "luna"

    def test_dry_run_flag_preserved(self):
        result = run_pipeline("sofia", dry_run=True)
        assert result.dry_run is True

    def test_has_five_steps(self):
        result = run_pipeline("bianca", dry_run=True)
        assert len(result.steps) == 5

    def test_step_names_match_expected(self):
        result = run_pipeline("marina", dry_run=True)
        names = [s.name for s in result.steps]
        assert names == ["ingest", "process", "curate", "schedule", "upload"]

    def test_dry_run_upload_is_skipped(self):
        result = run_pipeline("isabelle", dry_run=True)
        upload_step = next(s for s in result.steps if s.name == "upload")
        assert upload_step.status == StepStatus.SKIPPED

    def test_overall_success_in_dry_run(self):
        result = run_pipeline("aurora", dry_run=True)
        assert result.success is True
