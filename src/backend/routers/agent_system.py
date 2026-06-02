"""Agent system router — serves 15-role pipeline metadata from pre-generated JSON.

Run: python scripts/generate_agents_data.py
This reads all SKILL.md and LESSONS.md from ~/.claude/skills/agents/
and generates data/agents.json, which is deployed alongside the backend.
"""

import json
from pathlib import Path
from fastapi import APIRouter

router = APIRouter()

_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "agents.json"

try:
    _data = json.loads(_DATA_PATH.read_text(encoding="utf-8"))
except Exception:
    _data = {
        "agents": [], "pipeline": {"stages": [], "roles": []},
        "lessons": {"items": [], "summary": {}}, "summary": {},
    }


@router.get("/agent-system/status")
async def agent_status():
    return {"agents": _data["agents"]}


@router.get("/agent-system/pipeline")
async def agent_pipeline():
    return _data["pipeline"]


@router.get("/agent-system/lessons")
async def agent_lessons():
    return _data["lessons"]


@router.get("/agent-system/knowledge")
async def agent_knowledge():
    return {
        "status": "static",
        "note": "Pre-generated from local agent files during deployment.",
        "generated_at": _data.get("generated_at"),
        "summary": _data["summary"],
    }
