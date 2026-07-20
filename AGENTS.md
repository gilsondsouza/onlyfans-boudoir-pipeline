# AGENTS.md

## Cursor Cloud specific instructions

### What this repo is
`onlyfans-boudoir-pipeline` is a **single, self-contained Python CLI product** (no web server, no GUI, no database daemon required). It has two entry points:
- Content pipeline: `python -m src.pipeline` (subcommands `run`, `list-models`).
- Interactive LLM agent: `python -m src.agent`.

The pipeline steps and integrations (OnlyFans upload, media processing, storage, notifications) are currently **stubs**; the agent defaults to an offline `DemoBackend`. So the app runs end-to-end with **no external services, API keys, or network access**.

### Environment / dependencies
- Requires Python 3.11+ (VM has 3.12). Dependencies install to the **user site** (`pip` defaults to `--user` here; system is not PEP-668 externally-managed), so **no virtualenv is used**. `python3 -m venv` is intentionally avoided because `python3.12-venv` is not installed.
- The update script runs `pip3 install -e ".[dev]"` (core deps + `pytest`/`ruff`/`mypy`). Optional extras exist for real functionality and can be installed on demand: `pip3 install -e ".[llm]"`, `".[media]"`, `".[storage]"`, or `".[all]"`.
- Console scripts (`ruff`, `mypy`, `pytest`, `boudoir-pipeline`, `boudoir-agent`) install to `~/.local/bin`, which is added to `PATH` via `~/.bashrc`. If `PATH` isn't picked up, run tools as `python3 -m pytest` / `~/.local/bin/ruff`.

### Where the code lives (important)
The default/base branch (`enterprise`) contains **only `README.md`** — no source. The actual application code lives on branch `copilot/project-details` (this branch is based on it). If a future run starts on an empty branch, the update script guards on file existence and is a no-op, and there will be nothing to run/test until the code branch is present.

### Run / test / lint / build
Standard commands are in the `Makefile` and `pyproject.toml`; use those. Quick reference:
- Tests: `python3 -m pytest tests/ -v` (56 tests; `make test`). Coverage: `make test-cov`.
- Lint: `ruff check src/ tests/` (`make lint`). Typecheck: `mypy src/` (`make typecheck`).
- Run pipeline: `python3 -m src.pipeline run --dry-run` (`make run-pipeline`) or `--model <name>`; list profiles with `python3 -m src.pipeline list-models`.
- Run agent (offline demo): `python3 -m src.agent` (`make run-agent`); it reads stdin, so pipe input or type `sair` to exit.

### Non-obvious caveats
- `ruff check` and `mypy src/` currently **report pre-existing findings** in the source (the pinned lower-bound versions resolve to newer tools with additional rules). These are code-quality issues in the repo, **not** environment breakage — do not treat them as setup failures.
- Config in `config/*.yaml` is required at import time (`src/config.py` raises `FileNotFoundError` if missing) and supports `${VAR:default}` env expansion. `.env` is optional (`cp .env.example .env`); the app runs without it.
