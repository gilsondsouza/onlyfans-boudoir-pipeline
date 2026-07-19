"""
Ponto de entrada da CLI do pipeline.
Executar com: python -m src.pipeline run [--model NOME] [--dry-run]
"""

from __future__ import annotations

import logging

import click

from src.models.loader import load_all_profiles
from src.pipeline.runner import run_pipeline


def _configure_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
        level=level,
    )


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Ativa logs detalhados.")
@click.pass_context
def main(ctx: click.Context, verbose: bool) -> None:
    """🎨 Boudoir Pipeline — gerenciamento de conteúdo para OnlyFans."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    _configure_logging(verbose)


@main.command()
@click.option(
    "--model",
    "-m",
    default=None,
    help="Nome do modelo a processar. Omita para processar todos.",
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Simula a execução sem efetuar uploads reais.",
)
@click.pass_context
def run(ctx: click.Context, model: str | None, dry_run: bool) -> None:
    """Executa o pipeline de produção de conteúdo."""
    profiles = load_all_profiles()

    if model:
        if model not in profiles:
            available = ", ".join(profiles)
            raise click.BadParameter(
                f"Modelo '{model}' não encontrado. Disponíveis: {available}",
                param_hint="--model",
            )
        targets = {model: profiles[model]}
    else:
        targets = profiles

    if dry_run:
        click.echo("⚠️  Modo dry-run ativado — nenhum upload será realizado.\n")

    any_failed = False
    for model_name in targets:
        click.echo(f"▶ {model_name}")
        pipeline_run = run_pipeline(model_name, dry_run=dry_run)
        click.echo(pipeline_run.summary)
        click.echo()
        if not pipeline_run.success:
            any_failed = True

    if any_failed:
        raise SystemExit(1)


@main.command()
def list_models() -> None:
    """Lista todos os modelos configurados e seus status."""
    profiles = load_all_profiles()
    click.echo(f"{'Modelo':<15} {'Display':<15} {'Assinatura':>12}  Horários de pico")
    click.echo("-" * 60)
    for name, p in profiles.items():
        hours = ", ".join(str(h) + "h" for h in p.posting.peak_hours)
        click.echo(
            f"{name:<15} {p.display_name:<15} "
            f"USD {p.pricing.subscription_usd:>6.2f}   {hours}"
        )


if __name__ == "__main__":
    main()
