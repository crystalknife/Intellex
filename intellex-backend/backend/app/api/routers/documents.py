from fastapi import APIRouter, Depends, HTTPException, Query

from backend.app.api.deps import get_current_membership
from backend.app.api.schemas import DocumentListResponse, DocumentResponse
from backend.app.db.models import OrganizationMemberModel
from backend.app.db.session import get_db
from backend.app.repositories.document_repository import DocumentRepository
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.get("/", response_model=DocumentListResponse)
async def get_documents(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    source: str | None = None,
    category: str | None = None,
    db: Session = Depends(get_db),
    membership: OrganizationMemberModel = Depends(get_current_membership),
):
    repo = DocumentRepository(db)

    results, total = repo.list_documents(
        membership.organization_id,
        limit=limit,
        offset=offset,
        source=source,
        category=category,
    )

    return DocumentListResponse(
        items=results,
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    db: Session = Depends(get_db),
    membership: OrganizationMemberModel = Depends(get_current_membership),
):
    repo = DocumentRepository(db)

    document = repo.get(document_id, membership.organization_id)

    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    return document
