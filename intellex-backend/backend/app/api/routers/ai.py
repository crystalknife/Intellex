from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.ai.client import AINotConfiguredError, is_configured
from backend.app.ai.service import AIRequestError, AIService
from backend.app.api.schemas import AIChatRequest, AIChatResponse, AIStatusResponse
from backend.app.config import settings
from backend.app.db.session import get_db

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.get("/status", response_model=AIStatusResponse)
async def get_ai_status():
    return AIStatusResponse(
        configured=is_configured(),
        model=settings.OPENROUTER_MODEL,
    )


@router.post("/chat", response_model=AIChatResponse)
async def chat(payload: AIChatRequest, db: Session = Depends(get_db)):
    if not payload.question.strip():
        raise HTTPException(status_code=422, detail="Question cannot be empty")

    try:
        result = await AIService.answer_question(
            question=payload.question,
            history=[turn.model_dump() for turn in payload.history],
            db=db,
        )
    except AINotConfiguredError:
        raise HTTPException(
            status_code=503,
            detail=(
                "AI Workspace isn't configured. Add OPENROUTER_API_KEY to "
                "backend/.env and restart the server."
            ),
        )
    except AIRequestError as e:
        raise HTTPException(
            status_code=502,
            detail=f"The AI model request failed: {e}",
        )

    return AIChatResponse(**result)
