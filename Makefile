.PHONY: help install install-dev lint format typecheck test test-cov run-agent run-pipeline clean

# Detecta o Python disponível
PYTHON ?= python3
PIP    ?= pip

help: ## Mostra esta ajuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instala as dependências mínimas de runtime
	$(PIP) install pyyaml python-dotenv click rich loguru

install-dev: ## Instala todas as dependências (runtime + dev)
	$(PIP) install -r requirements.txt

lint: ## Verifica estilo e erros com ruff
	ruff check src/ tests/

format: ## Formata o código com ruff
	ruff format src/ tests/

typecheck: ## Verifica tipos com mypy
	mypy src/

test: ## Executa a suíte de testes
	$(PYTHON) -m pytest tests/ -v

test-cov: ## Executa testes com relatório de cobertura
	$(PYTHON) -m pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html

run-agent: ## Inicia o agente interativo (modo demo sem LLM real)
	$(PYTHON) -m src.agent

run-pipeline: ## Executa o pipeline completo (dry-run)
	$(PYTHON) -m src.pipeline run --dry-run

clean: ## Remove arquivos temporários e de build
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
