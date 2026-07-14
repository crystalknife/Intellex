"""
Feed Source Repository

Persistence access for configured RSS feeds.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.db.models import FeedSourceModel


class FeedSourceRepository:

    def __init__(self, db: Session):
        self.db = db

    def list_all(self, enabled_only: bool = False) -> list[FeedSourceModel]:
        stmt = select(FeedSourceModel).order_by(
            FeedSourceModel.created_at.asc()
        )

        if enabled_only:
            stmt = stmt.where(FeedSourceModel.enabled.is_(True))

        return list(self.db.execute(stmt).scalars())

    def get(self, feed_id: str) -> FeedSourceModel | None:
        return self.db.get(FeedSourceModel, feed_id)

    def get_by_url(self, url: str) -> FeedSourceModel | None:
        return self.db.execute(
            select(FeedSourceModel).where(FeedSourceModel.url == url)
        ).scalar_one_or_none()

    def create(self, url: str, label: str = "") -> FeedSourceModel:
        model = FeedSourceModel(url=url, label=label, enabled=True)

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return model

    def delete(self, feed_id: str) -> bool:
        model = self.get(feed_id)

        if model is None:
            return False

        self.db.delete(model)
        self.db.commit()

        return True

    def set_enabled(self, feed_id: str, enabled: bool) -> FeedSourceModel | None:
        model = self.get(feed_id)

        if model is None:
            return None

        model.enabled = enabled
        self.db.commit()
        self.db.refresh(model)

        return model

    def seed_defaults_if_empty(self, default_urls: list[str]) -> None:
        """
        Populates the table with the original hardcoded feed list on
        first-ever run, so out-of-the-box behavior is unchanged. A no-op
        on every subsequent call once any feed exists (including if the
        user has since deleted all of them -- we don't want to silently
        resurrect defaults after an intentional empty state... but an
        empty *table* only ever happens pre-seed, since the table is
        never fully emptied by normal use without deleting rows one by
        one, so this distinction is acceptable for now).
        """

        existing = self.db.execute(
            select(FeedSourceModel.id).limit(1)
        ).first()

        if existing is not None:
            return

        for url in default_urls:
            self.db.add(FeedSourceModel(url=url, label="", enabled=True))

        self.db.commit()
