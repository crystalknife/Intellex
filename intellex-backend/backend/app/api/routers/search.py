from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.api.schemas import DocumentListResponse
from backend.app.db.session import get_db
from backend.app.repositories.document_repository import DocumentRepository

router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


@router.get("/", response_model=DocumentListResponse)
async def search(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    repo = DocumentRepository(db)

    results, total = repo.search(q, limit=limit)

    return DocumentListResponse(
        items=results,
        total=total,
        limit=limit,
        offset=0,
    )
