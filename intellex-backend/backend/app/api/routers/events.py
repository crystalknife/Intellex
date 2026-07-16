from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app.api.deps import get_current_membership
from backend.app.api.schemas import EventDetailResponse, EventListResponse
from backend.app.db.models import OrganizationMemberModel
from backend.app.db.session import get_db
from backend.app.repositories.event_repository import EventRepository

router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


@router.get("/", response_model=EventListResponse)
async def get_events(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    membership: OrganizationMemberModel = Depends(get_current_membership),
):
    repo = EventRepository(db)

    results, total = repo.list_events(
        membership.organization_id, limit=limit, offset=offset
    )

    return EventListResponse.build(
        results, total=total, limit=limit, offset=offset
    )


@router.get("/{event_id}", response_model=EventDetailResponse)
async def get_event(
    event_id: str,
    db: Session = Depends(get_db),
    membership: OrganizationMemberModel = Depends(get_current_membership),
):
    repo = EventRepository(db)

    event = repo.get(event_id, membership.organization_id)

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    return EventDetailResponse.from_model(event)
