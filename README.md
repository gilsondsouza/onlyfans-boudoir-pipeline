# onlyfans-boudoir-pipeline
Autonomous artistic boudoir content production pipeline for OnlyFans - 7 models + interactive agent

## Structure

- `src/onlyfans_boudoir_pipeline/models.py` — profiles for 7 models with distinct photographic styles.
- `src/onlyfans_boudoir_pipeline/agent.py` — interactive agent that suggests models and builds prompts.
- `src/onlyfans_boudoir_pipeline/pipeline.py` — orchestration for content generation pipeline.
- `tests/` — automated tests with `pytest`.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Tests

```bash
pytest -v
```

## Quick start

```python
from onlyfans_boudoir_pipeline.agent import InteractiveAgent
from onlyfans_boudoir_pipeline.pipeline import BoudoirPipeline

agent = InteractiveAgent()
pipeline = BoudoirPipeline(agent)
pieces = pipeline.generate_for_all_models("golden hour", "intimate")
for p in pieces:
    print(p.prompt)
```
