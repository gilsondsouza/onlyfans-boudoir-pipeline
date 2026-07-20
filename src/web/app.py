"""
API FastAPI + dashboard estático para o Boudoir Pipeline.

Expõe modelos, execução do pipeline e chat com o agente.
"""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from src.agent.chat import ChatAgent, build_backend
from src.config import get_schedule, get_settings
from src.models.loader import get_profile, load_all_profiles
from src.pipeline.runner import run_pipeline

STATIC_DIR = Path(__file__).resolve().parent / "static"

app = FastAPI(
    title="Boudoir Pipeline",
    description="Dashboard do OnlyFans Boudoir Pipeline",
    version="0.1.0",
)

_agents: dict[str, ChatAgent] = {}


def _profile_to_dict(profile: Any) -> dict[str, Any]:
    data = asdict(profile)
    # tuple → list for JSON
    ppv = data["pricing"]["ppv_price_range"]
    data["pricing"]["ppv_price_range"] = list(ppv)
    return data


def _get_agent(session_id: str) -> ChatAgent:
    if session_id not in _agents:
        _agents[session_id] = ChatAgent(backend=build_backend())
    return _agents[session_id]


class PipelineRunRequest(BaseModel):
    model_name: str = Field(..., min_length=1)
    dry_run: bool = True


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    session_id: str = "default"


class ResetRequest(BaseModel):
    session_id: str = "default"


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/models")
def list_models() -> list[dict[str, Any]]:
    profiles = load_all_profiles()
    return [_profile_to_dict(p) for p in profiles.values()]


@app.get("/api/models/{name}")
def model_detail(name: str) -> dict[str, Any]:
    try:
        return _profile_to_dict(get_profile(name))
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/settings")
def settings() -> dict[str, Any]:
    return get_settings()


@app.get("/api/schedule")
def schedule() -> dict[str, Any]:
    return get_schedule()


@app.post("/api/pipeline/run")
def pipeline_run(body: PipelineRunRequest) -> dict[str, Any]:
    try:
        get_profile(body.model_name)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    result = run_pipeline(body.model_name, dry_run=body.dry_run)
    return {
        "model_name": result.model_name,
        "dry_run": result.dry_run,
        "success": result.success,
        "summary": result.summary,
        "steps": [
            {
                "name": step.name,
                "status": step.status.value,
                "message": step.message,
                "items_processed": step.items_processed,
            }
            for step in result.steps
        ],
    }


@app.post("/api/agent/chat")
def agent_chat(body: ChatRequest) -> dict[str, str]:
    agent = _get_agent(body.session_id)
    reply = agent.chat(body.message)
    return {"reply": reply, "session_id": body.session_id}


@app.post("/api/agent/reset")
def agent_reset(body: ResetRequest) -> dict[str, str]:
    agent = _get_agent(body.session_id)
    agent.reset()
    return {"status": "reset", "session_id": body.session_id}


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
