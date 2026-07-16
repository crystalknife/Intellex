from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.api.deps import get_current_membership
from backend.app.api.schemas import (
    AddCollectionItemRequest,
    CollectionDetailResponse,
    CollectionItemResponse,
    CollectionListResponse,
    CollectionResponse,
    CreateCollectionRequest,
    RenameCollectionRequest,
)
from backend.app.db.models import OrganizationMemberModel
from backend.app.db.session import get_db
from backend.app.repositories.collection_repository import (
    CollectionRepository,
    CrossOrganizationReferenceError,
    DuplicateItemError,
)
from backend.app.repositories.document_repository import DocumentRepository
from backend.app.repositories.event_repository import EventRepository

router = APIRouter(
    prefix="/collections",
    tags=["Collections"],
)


@router.get("/", response_model=CollectionListResponse)
async def get_collections(
    db: Session = Depends(get_db),
    membership: OrganizationMemberModel = Depends(get_current_membership),
):
    repo = CollectionRepository(db)

    return CollectionListResponse.build(repo.list_all(membership.organization_id))


@router.post("/", response_model=CollectionResponse, status_code=201)
async def create_collection(
    payload: CreateCollectionRequest,
    db: Session = Depends(get_db),
    membership: OrganizationMemberModel = Depends(get_current_membership),
):
    if not payload.name.strip():
        raise HTTPException(
            status_code=422, detail="Collection name cannot be empty"
        )

    repo = CollectionRepository(db)
    model = repo.create(payload.name.strip(), membership.organization_id)

    return CollectionResponse.from_model(model)


@router.get("/{collection_id}", response_model=CollectionDetailResponse)
async def get_collection(
    collection_id: str,
    db: Session = Depends(get_db),
    membership: OrganizationMemberModel = Depends(get_current_membership),
):
    repo = CollectionRepository(db)
    model = repo.get(collection_id, membership.organization_id)

    if model is None:
        raise HTTPException(status_code=404, detail="Collection not found")

    return CollectionDetailResponse.from_model(model)


@router.patch("/{collection_id}", response_model=CollectionResponse)
async def rename_collection(
    collection_id: str,
    payload: RenameCollectionRequest,
    db: Session = Depends(get_db),
    membership: OrganizationMemberModel = Depends(get_current_membership),
):
    if not payload.name.strip():
        raise HTTPException(
            status_code=422, detail="Collection name cannot be empty"
        )

    repo = CollectionRepository(db)
    model = repo.rename(
        collection_id, membership.organization_id, payload.name.strip()
    )

    if model is None:
        raise HTTPException(status_code=404, detail="Collection not found")

    return CollectionResponse.from_model(model)


@router.delete("/{collection_id}", status_code=204)
async def delete_collection(
    collection_id: str,
    db: Session = Depends(get_db),
    membership: OrganizationMemberModel = Depends(get_current_membership),
):
    repo = CollectionRepository(db)

    if not repo.delete(collection_id, membership.organization_id):
        raise HTTPException(status_code=404, detail="Collection not found")


@router.post(
    "/{collection_id}/items",
    response_model=CollectionItemResponse,
    status_code=201,
)
async def add_collection_item(
    collection_id: str,
    payload: AddCollectionItemRequest,
    db: Session = Depends(get_db),
    membership: OrganizationMemberModel = Depends(get_current_membership),
):
    org_id = membership.organization_id
    collection_repo = CollectionRepository(db)

    if collection_repo.get(collection_id, org_id) is None:
        raise HTTPException(status_code=404, detail="Collection not found")

    if payload.type == "document":
        if DocumentRepository(db).get(payload.id, org_id) is None:
            raise HTTPException(status_code=404, detail="Document not found")

        try:
            item = collection_repo.add_document(collection_id, payload.id, org_id)
        except DuplicateItemError:
            raise HTTPException(
                status_code=409,
                detail="This document is already saved to this collection",
            )
        except CrossOrganizationReferenceError:
            raise HTTPException(status_code=404, detail="Document not found")
    else:
        if EventRepository(db).get(payload.id, org_id) is None:
            raise HTTPException(status_code=404, detail="Event not found")

        try:
            item = collection_repo.add_event(collection_id, payload.id, org_id)
        except DuplicateItemError:
            raise HTTPException(
                status_code=409,
                detail="This event is already saved to this collection",
            )
        except CrossOrganizationReferenceError:
            raise HTTPException(status_code=404, detail="Event not found")

    db.refresh(item)

    return CollectionItemResponse.from_model(item)


@router.delete("/{collection_id}/items/{item_id}", status_code=204)
async def remove_collection_item(
    collection_id: str,
    item_id: str,
    db: Session = Depends(get_db),
    membership: OrganizationMemberModel = Depends(get_current_membership),
):
    repo = CollectionRepository(db)

    if not repo.remove_item(collection_id, item_id, membership.organization_id):
        raise HTTPException(status_code=404, detail="Item not found")
