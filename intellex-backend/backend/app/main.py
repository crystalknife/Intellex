"""
Standalone ingestion entrypoint.

Runs a single ingestion cycle (collect -> process -> persist -> cluster)
and prints a summary. Useful for local debugging without spinning up the
API server. The API server itself runs this on a schedule automatically
(see app/scheduler/scheduler.py) -- this script is not required for the
API to have data.
"""

import asyncio

from backend.app.db.session import init_db
from backend.app.services.ingestion_service import ingestion_service


async def main():

    init_db()

    result = await ingestion_service.run_cycle()

    print("=" * 60)
    print("Intellex")
    print("=" * 60)

    print(f"Fetched:            {result.get('fetched')}")
    print(f"Unique this cycle:  {result.get('unique')}")
    print(f"Total documents:    {result.get('total_documents')}")
    print(f"Total events:       {result.get('total_events')}")


if __name__ == "__main__":
    asyncio.run(main())
