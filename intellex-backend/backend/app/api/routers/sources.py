from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.api.deps import get_current_membership
from backend.app.api.schemas import SourceListResponse, SourceStats
from backend.app.db.models import OrganizationMemberModel
from backend.app.db.session import get_db
from backend.app.repositories.document_repository import DocumentRepository

router = APIRouter(
    prefix="/sources",
    tags=["Sources"],
)


@router.get("/", response_model=SourceListResponse)
async def get_sources(
    db: Session = Depends(get_db),
    membership: OrganizationMemberModel = Depends(get_current_membership),
):
    repo = DocumentRepository(db)

    counts = dict(repo.counts_by_source(membership.organization_id))
    last_collected = repo.most_recent_by_source(membership.organization_id)

    items = [
        SourceStats(
            name=source,
            document_count=count,
            last_collected_at=last_collected.get(source),
        )
        for source, count in sorted(
            counts.items(), key=lambda kv: -kv[1]
        )
    ]

    return SourceListResponse(items=items)
