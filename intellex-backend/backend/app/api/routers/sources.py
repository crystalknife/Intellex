from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.api.schemas import SourceListResponse, SourceStats
from backend.app.db.session import get_db
from backend.app.repositories.document_repository import DocumentRepository

router = APIRouter(
    prefix="/sources",
    tags=["Sources"],
)


@router.get("/", response_model=SourceListResponse)
async def get_sources(db: Session = Depends(get_db)):
    repo = DocumentRepository(db)

    counts = dict(repo.counts_by_source())
    last_collected = repo.most_recent_by_source()

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
