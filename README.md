# onlyfans-boudoir-pipeline
Pipeline autônomo de produção de conteúdo boudoir artístico para OnlyFans - 7 modelos + agente interativo

## Estrutura

- `src/onlyfans_boudoir_pipeline/models.py` — perfis de 7 modelos com estilos fotográficos distintos.
- `src/onlyfans_boudoir_pipeline/agent.py` — agente interativo que sugere modelos e monta prompts.
- `src/onlyfans_boudoir_pipeline/pipeline.py` — orquestração do pipeline de geração de conteúdo.
- `tests/` — testes automatizados com `pytest`.

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Testes

```bash
pytest -v
```

## Uso rápido

```python
from onlyfans_boudoir_pipeline.agent import InteractiveAgent
from onlyfans_boudoir_pipeline.pipeline import BoudoirPipeline

agent = InteractiveAgent()
pipeline = BoudoirPipeline(agent)
pieces = pipeline.generate_for_all_models("golden hour", "intimate")
for p in pieces:
    print(p.prompt)
```
