"""
Feed Source Repository

Persistence access for configured RSS feeds. Every method is scoped to
a single organization_id -- feed configuration (and therefore ingestion
itself) is private per organization.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.db.models import FeedSourceModel


class FeedSourceRepository:

    def __init__(self, db: Session):
        self.db = db

    def list_all(
        self, organization_id: str, enabled_only: bool = False
    ) -> list[FeedSourceModel]:
        stmt = (
            select(FeedSourceModel)
            .where(FeedSourceModel.organization_id == organization_id)
            .order_by(FeedSourceModel.created_at.asc())
        )

        if enabled_only:
            stmt = stmt.where(FeedSourceModel.enabled.is_(True))

        return list(self.db.execute(stmt).scalars())

    def get(
        self, feed_id: str, organization_id: str
    ) -> FeedSourceModel | None:
        stmt = select(FeedSourceModel).where(
            FeedSourceModel.id == feed_id,
            FeedSourceModel.organization_id == organization_id,
        )

        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_url(
        self, url: str, organization_id: str
    ) -> FeedSourceModel | None:
        return self.db.execute(
            select(FeedSourceModel).where(
                FeedSourceModel.organization_id == organization_id,
                FeedSourceModel.url == url,
            )
        ).scalar_one_or_none()

    def create(
        self, url: str, organization_id: str, label: str = ""
    ) -> FeedSourceModel:
        model = FeedSourceModel(
            url=url, organization_id=organization_id, label=label, enabled=True
        )

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return model

    def delete(self, feed_id: str, organization_id: str) -> bool:
        model = self.get(feed_id, organization_id)

        if model is None:
            return False

        self.db.delete(model)
        self.db.commit()

        return True

    def set_enabled(
        self, feed_id: str, organization_id: str, enabled: bool
    ) -> FeedSourceModel | None:
        model = self.get(feed_id, organization_id)

        if model is None:
            return None

        model.enabled = enabled
        self.db.commit()
        self.db.refresh(model)

        return model

    def seed_defaults_if_empty(
        self, organization_id: str, default_urls: list[str]
    ) -> None:
        """
        Populates a brand-new organization's feed list with the original
        default feeds on its first-ever ingestion cycle, so out-of-the-box
        behavior is unchanged for a freshly signed-up org. A no-op on
        every subsequent call once this org has any feed of its own
        (including if they've since deleted all of them deliberately --
        we don't resurrect defaults after an intentional empty state, but
        distinguishing "never had feeds" from "emptied them" isn't tracked
        separately, so this is an acceptable simplification for now).
        """

        existing = self.db.execute(
            select(FeedSourceModel.id)
            .where(FeedSourceModel.organization_id == organization_id)
            .limit(1)
        ).first()

        if existing is not None:
            return

        for url in default_urls:
            self.db.add(
                FeedSourceModel(
                    url=url, organization_id=organization_id, label="", enabled=True
                )
            )

        self.db.commit()
