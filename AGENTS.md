# AGENTS.md

## Cursor Cloud specific instructions

### What this repo is
`onlyfans-boudoir-pipeline` is a **single, self-contained Python CLI product** (no web server, no GUI, no database daemon required). It has two entry points:
- Content pipeline: `python3 -m src.pipeline` (subcommands `run`, `list-models`).
- Interactive LLM agent: `python3 -m src.agent`.

The pipeline steps and integrations (OnlyFans upload, media processing, storage, notifications) are currently **stubs**; the agent defaults to an offline `DemoBackend`. So the app runs end-to-end with **no external services, API keys, or network access**.

### Where the code lives (important)
The default/base branch (`enterprise`) contains **only `README.md`** — no source. The actual application code lives on branch `copilot/project-details` (this branch is based on it). If a future run starts on the empty `enterprise` branch, the startup/update script guards on file existence and is a no-op, and there is nothing to run/test until the code branch is checked out.

### Environment / dependencies
- Requires Python 3.11+ (VM has 3.12). `pip3` installs to the **user site** (`~/.local`), so **no virtualenv is used**.
- Install with `pip3 install -e ".[dev]"` (core deps + `pytest`/`ruff`/`mypy`). Optional extras exist for real functionality: `pip3 install -e ".[llm]"`, `".[media]"`, `".[storage]"`, or `".[all]"`.
- Console scripts (`ruff`, `mypy`, `pytest`, `boudoir-pipeline`, `boudoir-agent`) install to `~/.local/bin`. That directory is added to `PATH` via `~/.bashrc`; if a tool isn't found, invoke via module form (`python3 -m pytest`, `python3 -m mypy`) or the full path (`~/.local/bin/ruff`).

### Run / test / lint / build
Standard commands are in the `Makefile` and `pyproject.toml`; use those. Quick reference:
- Tests: `python3 -m pytest tests/ -v` (56 tests; `make test`). Coverage: `make test-cov`.
- Lint: `ruff check src/ tests/` (`make lint`). Typecheck: `mypy src/` (`make typecheck`).
- Run pipeline: `python3 -m src.pipeline run --dry-run` (`make run-pipeline`), optionally `--model <name>`; list profiles with `python3 -m src.pipeline list-models`.
- Run agent (offline demo): `python3 -m src.agent` (`make run-agent`); it reads stdin, so pipe input or type `sair` to exit.

### Non-obvious caveats
- `ruff check src/ tests/` and `mypy src/` currently **report pre-existing findings** in the source (newer tool versions add rules). These are code-quality issues in the repo, **not** environment breakage — do not treat them as setup failures.
- Config in `config/*.yaml` is required at import time (`src/config.py` raises `FileNotFoundError` if missing) and supports `${VAR:default}` env expansion. `.env` is optional (`cp .env.example .env`); the app runs without it.
