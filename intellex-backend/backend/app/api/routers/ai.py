from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.ai.client import AINotConfiguredError, is_configured
from backend.app.ai.service import AIRequestError, AIService
from backend.app.api.deps import get_current_membership
from backend.app.api.schemas import AIChatRequest, AIChatResponse, AIStatusResponse
from backend.app.config import settings
from backend.app.db.models import OrganizationMemberModel
from backend.app.db.session import get_db

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.get("/status", response_model=AIStatusResponse)
async def get_ai_status():
    models = settings.openrouter_models_list

    return AIStatusResponse(
        configured=is_configured(),
        # "Primary" model shown to the frontend -- the actual model
        # that serves any given request can differ (see AIService's
        # fallback loop) and is reported per-response in
        # AIChatResponse.model instead. This is just the first entry
        # in the configured list, i.e. the one normally tried first.
        model=models[0] if models else "not configured",
    )


@router.post("/chat", response_model=AIChatResponse)
async def chat(
    payload: AIChatRequest,
    db: Session = Depends(get_db),
    membership: OrganizationMemberModel = Depends(get_current_membership),
):
    if not payload.question.strip():
        raise HTTPException(status_code=422, detail="Question cannot be empty")

    try:
        result = await AIService.answer_question(
            question=payload.question,
            history=[turn.model_dump() for turn in payload.history],
            db=db,
            organization_id=membership.organization_id,
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
