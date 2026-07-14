from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routers import (
    analytics,
    documents,
    events,
    feeds,
    ingestion,
    search,
    sources,
)
from backend.app.config import settings
from backend.app.core.logger import get_logger
from backend.app.db.session import init_db
from backend.app.scheduler import scheduler

logger = get_logger("App")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database")
    init_db()

    scheduler.start()

    yield

    scheduler.stop()


app = FastAPI(
    title="Intellex API",
    description="AI-powered News Intelligence Platform",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def root():
    return {
        "name": "Intellex",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health", tags=["Health"])
async def health():
    return {
        "status": "healthy"
    }


app.include_router(documents.router)
app.include_router(events.router)
app.include_router(search.router)
app.include_router(analytics.router)
app.include_router(sources.router)
app.include_router(feeds.router)
app.include_router(ingestion.router)