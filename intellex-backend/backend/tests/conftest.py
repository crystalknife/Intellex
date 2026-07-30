"""
Pytest configuration and shared fixtures.

DATABASE_URL/JWT_SECRET/etc. must be set before backend.app is imported
anywhere -- Settings() reads them from the environment exactly once, at
import time (see config/settings.py), and every test module importing
anything under backend.app shares that one cached import. Since pytest
always imports conftest.py before collecting any test module, setting
them here at module level (not inside a fixture function) guarantees
they're in place before that first import happens, however pytest
happens to order test collection.

Test isolation strategy: one shared SQLite file for the whole test
session (fresh at session start), with each test that needs an
authenticated context signing up its own uniquely-emailed organization
via the `signed_up_org`/`two_orgs` fixtures below. This avoids the
complexity/fragility of reloading Settings-derived singletons
(engine, SessionLocal, the FastAPI app itself) per test, while still
keeping tests independent of each other -- nothing here relies on
tests running in any particular order.
"""

import os
import uuid

os.environ.setdefault(
    "DATABASE_URL", "sqlite:////tmp/intellex_pytest.db"
)
os.environ.setdefault("JWT_SECRET", "test-secret-not-for-production")
os.environ.setdefault("RUN_INGESTION_ON_STARTUP", "false")
os.environ.setdefault("OPENROUTER_API_KEY", "test-key-not-real")
os.environ.setdefault(
    "OPENROUTER_MODELS", "test-model-a:free,test-model-b:free"
)

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="session", autouse=True)
def _fresh_test_database():
    """Every full test run starts from a brand-new, empty database file."""

    db_path = os.environ["DATABASE_URL"].removeprefix("sqlite:///")

    try:
        os.remove(db_path)
    except FileNotFoundError:
        pass

    yield


@pytest.fixture()
def client():
    from backend.app.api.app import app

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def unique_email() -> str:
    return f"user-{uuid.uuid4().hex[:12]}@example.com"


def _signup(client: TestClient, email: str | None = None) -> dict:
    email = email or f"user-{uuid.uuid4().hex[:12]}@example.com"
    org_name = f"Test Org {uuid.uuid4().hex[:8]}"

    response = client.post(
        "/auth/signup",
        json={
            "email": email,
            "password": "password12345",
            "full_name": "Test User",
            "organization_name": org_name,
        },
    )
    assert response.status_code == 201, response.text
    body = response.json()

    return {
        "headers": {"Authorization": f"Bearer {body['access_token']}"},
        "token": body["access_token"],
        "org_name": org_name,
        "org_id": body["organization"]["id"],
        "user_email": email,
    }


@pytest.fixture()
def signed_up_org(client) -> dict:
    """A single freshly signed-up user + organization."""

    return _signup(client)


@pytest.fixture()
def two_orgs(client) -> tuple[dict, dict]:
    """Two independent, freshly signed-up organizations -- for isolation tests."""

    return _signup(client), _signup(client)
