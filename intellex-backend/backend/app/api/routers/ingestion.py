import asyncio

from fastapi import APIRouter, Depends

from backend.app.api.deps import get_current_membership
from backend.app.db.models import OrganizationMemberModel
from backend.app.services.ingestion_service import ingestion_service

router = APIRouter(
    prefix="/ingestion",
    tags=["Ingestion"],
)


@router.post("/trigger", status_code=202)
async def trigger_ingestion(
    membership: OrganizationMemberModel = Depends(get_current_membership),
):
    """
    Kick off an ingestion cycle for the caller's organization immediately
    instead of waiting for the next scheduled interval -- primarily so a
    newly added feed can be verified right away. Fires and returns
    immediately; poll /analytics/pipeline (isRunning / lastRunAt) for
    progress. Never affects any other organization's ingestion state.
    """

    org_id = membership.organization_id

    if ingestion_service.is_running(org_id):
        return {"status": "already_running"}

    asyncio.create_task(ingestion_service.run_cycle(organization_id=org_id))

    return {"status": "started"}
