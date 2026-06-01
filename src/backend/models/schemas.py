from pydantic import BaseModel
from typing import Optional


class ReviewRequest(BaseModel):
    dimensions: list[str]


class PrincipleInfo(BaseModel):
    name: str
    brief: str
    explanation: str
    application: str
    suggestion: str


class Finding(BaseModel):
    type: str  # "issue" | "strength"
    title: str
    description: str
    principle: PrincipleInfo


class DimensionResult(BaseModel):
    name: str
    score: float
    summary: str
    findings: list[Finding]


class ReviewResponse(BaseModel):
    session_id: str
    overall_score: float
    dimensions: list[DimensionResult]


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    reply: str
    references: list[str] = []


class HealthResponse(BaseModel):
    status: str
    version: str


class ClarifyRequest(BaseModel):
    description: str


class ClarifyQuestion(BaseModel):
    id: str
    question: str


class ClarifyResponse(BaseModel):
    questions: list[ClarifyQuestion]
    summary: str


class ConfirmRequest(BaseModel):
    action_type: str
    context: str


class ConfirmResponse(BaseModel):
    action_id: str
    proposal: str
    impact: str
    reversible: bool


class ExecuteRequest(BaseModel):
    action_id: str
    confirmed: bool


class ExecuteResponse(BaseModel):
    result: str
    status: str  # "executed" | "cancelled"


class QAPair(BaseModel):
    question: str
    answer: str


class RefineRequest(BaseModel):
    original_description: str
    qa_pairs: list[QAPair]


class RefineResponse(BaseModel):
    refined_analysis: str
    without_clarify: str  # What AI would have said without clarification
