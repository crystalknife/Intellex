"""
Standalone ingestion entrypoint.

Runs a single ingestion cycle (collect -> process -> persist -> cluster)
and prints a summary. Useful for local debugging without spinning up the
API server. The API server itself runs this on a schedule automatically
(see app/scheduler/scheduler.py) -- this script is not required for the
API to have data.

Phase B: ingestion is private per organization, so this script needs an
organization to run against. It defaults to the first organization that
exists (fine for local dev, where there's usually exactly one); pass an
explicit --org-id to target a specific one.
"""

import argparse
import asyncio

from backend.app.db.session import SessionLocal, init_db
from backend.app.repositories.organization_repository import (
    OrganizationRepository,
)
from backend.app.services.ingestion_service import ingestion_service


async def main(organization_id: str | None):

    init_db()

    if organization_id is None:
        db = SessionLocal()
        try:
            organizations = OrganizationRepository(db).list_all()
        finally:
            db.close()

        if not organizations:
            print(
                "No organizations exist yet -- sign up through the API "
                "first (POST /auth/signup), then re-run this script."
            )
            return

        organization_id = organizations[0].id
        print(f"No --org-id given, defaulting to: {organizations[0].name}")

    result = await ingestion_service.run_cycle(organization_id=organization_id)

    print("=" * 60)
    print("Intellex")
    print("=" * 60)

    print(f"Fetched:            {result.get('fetched')}")
    print(f"Unique this cycle:  {result.get('unique')}")
    print(f"Total documents:    {result.get('total_documents')}")
    print(f"Total events:       {result.get('total_events')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--org-id", dest="organization_id", default=None)
    args = parser.parse_args()

    asyncio.run(main(args.organization_id))
