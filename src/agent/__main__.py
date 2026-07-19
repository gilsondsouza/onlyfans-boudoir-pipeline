"""
Ponto de entrada do agente interativo.
Executar com: python -m src.agent
"""

from __future__ import annotations

import sys

import click

from src.agent.chat import ChatAgent, build_backend


@click.command()
@click.option(
    "--provider",
    default=None,
    help="Backend de LLM: openai, anthropic ou demo (padrão).",
)
def main(provider: str | None) -> None:
    """Inicia o agente interativo do Boudoir Pipeline."""
    try:
        from rich.console import Console
        from rich.panel import Panel

        console = Console()
        use_rich = True
    except ImportError:
        use_rich = False

    backend = build_backend(provider)
    agent = ChatAgent(backend=backend)

    if use_rich:
        console.print(
            Panel(
                "[bold cyan]🤖 Boudoir Pipeline Agent[/bold cyan]\n"
                "Digite sua mensagem ou [bold]'sair'[/bold] para encerrar.",
                border_style="cyan",
            )
        )
    else:
        print("=== Boudoir Pipeline Agent ===")
        print("Digite sua mensagem ou 'sair' para encerrar.\n")

    while True:
        try:
            user_input = input("Você: ").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if not user_input:
            continue
        if user_input.lower() in {"sair", "exit", "quit"}:
            break

        response = agent.chat(user_input)

        if use_rich:
            console.print(f"\n[bold green]Agente:[/bold green] {response}\n")
        else:
            print(f"\nAgente: {response}\n")

    if use_rich:
        console.print("[dim]Encerrando agente.[/dim]")
    else:
        print("Encerrando agente.")


if __name__ == "__main__":
    main()
