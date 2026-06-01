import uuid
import time
from fastapi import APIRouter, HTTPException
from models.schemas import ClarifyRequest, ClarifyResponse, ClarifyQuestion
from models.schemas import ConfirmRequest, ConfirmResponse, ExecuteRequest, ExecuteResponse
from models.schemas import RefineRequest, RefineResponse
from services.deepseek_client import _call_deepseek
from services.prompts import CLARIFY_PROMPT, CONFIRM_PROMPT, REFINE_PROMPT
from services.utils import parse_json_response, logger

router = APIRouter()

MAX_DESC_LENGTH = 500
MAX_CONTEXT_LENGTH = 1000
PENDING_CONFIRMATIONS: dict[str, dict] = {}
CONFIRMATION_TTL = 600  # 10 minutes


def _cleanup_confirmations():
    now = time.time()
    expired = [aid for aid, c in PENDING_CONFIRMATIONS.items()
               if now - c.get("_created_at", 0) > CONFIRMATION_TTL]
    for aid in expired:
        del PENDING_CONFIRMATIONS[aid]


@router.post("/clarify", response_model=ClarifyResponse)
async def clarify(req: ClarifyRequest):
    desc = req.description.strip()
    if not desc:
        raise HTTPException(status_code=400, detail="描述不能为空。")
    if len(desc) > MAX_DESC_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"描述过长，请控制在 {MAX_DESC_LENGTH} 字以内。",
        )

    messages = [
        {"role": "system", "content": CLARIFY_PROMPT},
        {"role": "user", "content": f"学生的描述：{desc}"},
    ]

    try:
        content = await _call_deepseek(messages, max_tokens=1024, temperature=0.7, timeout=60.0)
        data = parse_json_response(content)
    except Exception as e:
        logger.error(f"Clarify failed: {e}")
        raise HTTPException(status_code=502, detail="AI 澄清提问生成失败，请稍后重试。")

    questions = [ClarifyQuestion(id=q["id"], question=q["question"]) for q in data.get("questions", [])]
    return ClarifyResponse(questions=questions, summary=data.get("summary", ""))


@router.post("/clarify/refine", response_model=RefineResponse)
async def refine_after_clarify(req: RefineRequest):
    if not req.original_description.strip():
        raise HTTPException(status_code=400, detail="原始描述不能为空。")
    if not req.qa_pairs:
        raise HTTPException(status_code=400, detail="请至少回答一个澄清问题。")

    qa_text = "\n".join([f"Q: {qa.question}\nA: {qa.answer}" for qa in req.qa_pairs])
    messages = [
        {"role": "system", "content": REFINE_PROMPT},
        {"role": "user", "content": f"原始模糊描述：{req.original_description}\n\n澄清问答：\n{qa_text}"},
    ]

    try:
        content = await _call_deepseek(messages, max_tokens=1024, temperature=0.7, timeout=60.0)
        data = parse_json_response(content)
    except Exception as e:
        logger.error(f"Refine failed: {e}")
        raise HTTPException(status_code=502, detail="AI 精准分析生成失败，请稍后重试。")

    return RefineResponse(
        refined_analysis=data.get("refined_analysis", ""),
        without_clarify=data.get("without_clarify", ""),
    )


@router.post("/confirm", response_model=ConfirmResponse)
async def request_confirmation(req: ConfirmRequest):
    action = req.action_type.strip()
    context = req.context.strip()
    if not action or not context:
        raise HTTPException(status_code=400, detail="操作类型和上下文不能为空。")
    if len(context) > MAX_CONTEXT_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"上下文过长，请控制在 {MAX_CONTEXT_LENGTH} 字以内。",
        )

    messages = [
        {"role": "system", "content": CONFIRM_PROMPT},
        {"role": "user", "content": f"操作类型：{action}\n上下文：{context}"},
    ]

    try:
        content = await _call_deepseek(messages, max_tokens=512, temperature=0.5, timeout=30.0)
        data = parse_json_response(content)
    except Exception as e:
        logger.error(f"Confirm generation failed: {e}")
        raise HTTPException(status_code=502, detail="确认请求生成失败，请稍后重试。")

    _cleanup_confirmations()
    action_id = str(uuid.uuid4())
    PENDING_CONFIRMATIONS[action_id] = {
        "action_type": action,
        "context": context,
        "proposal": data.get("proposal", ""),
        "_created_at": time.time(),
    }

    return ConfirmResponse(
        action_id=action_id,
        proposal=data.get("proposal", ""),
        impact=data.get("impact", ""),
        reversible=data.get("reversible", False),
    )


@router.post("/execute", response_model=ExecuteResponse)
async def execute_action(req: ExecuteRequest):
    pending = PENDING_CONFIRMATIONS.get(req.action_id)
    if not pending:
        raise HTTPException(status_code=404, detail="该操作已过期或不存在，请重新发起确认。")

    if not req.confirmed:
        del PENDING_CONFIRMATIONS[req.action_id]
        return ExecuteResponse(result="操作已取消。", status="cancelled")

    action_type = pending["action_type"]
    context = pending["context"]
    proposal = pending["proposal"]

    del PENDING_CONFIRMATIONS[req.action_id]

    # Simulate execution — for demo purposes, generate a result description
    result = f"已执行「{proposal}」。\n操作类型：{action_type}\n处理上下文：{context[:80]}..."
    return ExecuteResponse(result=result, status="executed")
