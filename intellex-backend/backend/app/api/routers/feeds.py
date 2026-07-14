from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.api.schemas import (
    FeedSourceCreateRequest,
    FeedSourceListResponse,
    FeedSourceResponse,
    FeedSourceUpdateRequest,
)
from backend.app.collectors.rss import DEFAULT_FEEDS
from backend.app.db.session import get_db
from backend.app.repositories.feed_source_repository import (
    FeedSourceRepository,
)

router = APIRouter(
    prefix="/feeds",
    tags=["Feeds"],
)


@router.get("/", response_model=FeedSourceListResponse)
async def get_feeds(db: Session = Depends(get_db)):
    repo = FeedSourceRepository(db)
    repo.seed_defaults_if_empty(DEFAULT_FEEDS)

    return FeedSourceListResponse(items=repo.list_all())


@router.post("/", response_model=FeedSourceResponse, status_code=201)
async def create_feed(
    payload: FeedSourceCreateRequest, db: Session = Depends(get_db)
):
    repo = FeedSourceRepository(db)

    if repo.get_by_url(payload.url) is not None:
        raise HTTPException(
            status_code=409, detail="This feed URL is already configured"
        )

    try:
        return repo.create(payload.url, payload.label)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="This feed URL is already configured"
        )


@router.patch("/{feed_id}", response_model=FeedSourceResponse)
async def update_feed(
    feed_id: str,
    payload: FeedSourceUpdateRequest,
    db: Session = Depends(get_db),
):
    repo = FeedSourceRepository(db)

    model = repo.set_enabled(feed_id, payload.enabled)

    if model is None:
        raise HTTPException(status_code=404, detail="Feed not found")

    return model


@router.delete("/{feed_id}", status_code=204)
async def delete_feed(feed_id: str, db: Session = Depends(get_db)):
    repo = FeedSourceRepository(db)

    if not repo.delete(feed_id):
        raise HTTPException(status_code=404, detail="Feed not found")
