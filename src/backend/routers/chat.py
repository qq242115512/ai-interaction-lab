from fastapi import APIRouter, HTTPException
from models.schemas import ChatRequest, ChatResponse
from services.deepseek_client import chat_reply
from services.utils import sanitize_error, logger

router = APIRouter()

sessions: dict[str, dict] = {}

MAX_MESSAGE_LENGTH = 500


@router.post("/chat", response_model=ChatResponse)
async def chat_followup(req: ChatRequest):
    # Validate message length
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="消息不能为空。")

    if len(req.message) > MAX_MESSAGE_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"消息过长，请控制在 {MAX_MESSAGE_LENGTH} 字以内。",
        )

    session = sessions.get(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在或已过期，请重新上传设计稿进行评审。")

    context = {
        "review": session.get("review", {}),
        "chat_history": session.get("chat_history", []),
    }

    try:
        result = await chat_reply(context, req.message.strip())
    except Exception as e:
        logger.error(f"Chat reply failed: {e}")
        raise HTTPException(status_code=502, detail=f"AI 回复失败，请稍后重试。")

    # Update chat history
    session["chat_history"].append({"role": "user", "content": req.message.strip()})
    session["chat_history"].append({"role": "assistant", "content": result.get("reply", "")})

    return ChatResponse(
        reply=result.get("reply", ""),
        references=result.get("references", []),
    )
