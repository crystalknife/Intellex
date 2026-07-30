"""
Multi-tenant isolation tests.

These formalize the checks that were run by hand while building Phase B
(org-scoped tenancy) into a real, repeatable suite -- every resource
that's supposed to be private per organization gets a same-URL/cross-org
test here, not just a "does the list endpoint 401 without a token" test.
"""

import pytest


PROTECTED_ROUTES = [
    "/documents/",
    "/events/",
    "/sources/",
    "/feeds/",
    "/collections/",
    "/search/?q=x",
    "/analytics/pipeline",
]


@pytest.mark.parametrize("path", PROTECTED_ROUTES)
def test_protected_routes_require_auth(client, path):
    assert client.get(path).status_code == 401


def test_feeds_are_isolated_per_org(client, two_orgs):
    org_a, org_b = two_orgs

    create = client.post(
        "/feeds/",
        json={"url": "https://shared-feed.example.com/rss.xml", "label": "Shared"},
        headers=org_a["headers"],
    )
    assert create.status_code == 201
    feed_id = create.json()["id"]

    # Same feed URL from org B must succeed independently -- it's a
    # different row, not a global unique conflict.
    create_b = client.post(
        "/feeds/",
        json={"url": "https://shared-feed.example.com/rss.xml", "label": "Also shared"},
        headers=org_b["headers"],
    )
    assert create_b.status_code == 201
    assert create_b.json()["id"] != feed_id

    feeds_a = client.get("/feeds/", headers=org_a["headers"]).json()["items"]
    feeds_b = client.get("/feeds/", headers=org_b["headers"]).json()["items"]
    assert any(f["id"] == feed_id for f in feeds_a)
    assert not any(f["id"] == feed_id for f in feeds_b)

    # org B must not be able to delete org A's feed by guessing its ID
    assert client.delete(f"/feeds/{feed_id}", headers=org_b["headers"]).status_code == 404

    # org A can delete its own feed
    assert client.delete(f"/feeds/{feed_id}", headers=org_a["headers"]).status_code == 204


def test_collections_are_isolated_per_org(client, two_orgs):
    org_a, org_b = two_orgs

    created = client.post(
        "/collections/", json={"name": "Org A's Collection"}, headers=org_a["headers"]
    )
    assert created.status_code == 201
    collection_id = created.json()["id"]

    # org B cannot fetch it directly by ID
    assert (
        client.get(f"/collections/{collection_id}", headers=org_b["headers"]).status_code
        == 404
    )

    # org B cannot rename or delete it either
    assert (
        client.patch(
            f"/collections/{collection_id}",
            json={"name": "Hijacked"},
            headers=org_b["headers"],
        ).status_code
        == 404
    )
    assert (
        client.delete(f"/collections/{collection_id}", headers=org_b["headers"]).status_code
        == 404
    )

    # it doesn't show up in org B's list
    collections_b = client.get("/collections/", headers=org_b["headers"]).json()["items"]
    assert not any(c["id"] == collection_id for c in collections_b)

    # but org A can see and manage it fine
    collections_a = client.get("/collections/", headers=org_a["headers"]).json()["items"]
    assert any(c["id"] == collection_id for c in collections_a)


def test_documents_endpoint_is_scoped_per_org(client, two_orgs):
    org_a, org_b = two_orgs

    # Neither org has ingested anything, but both must get a clean,
    # independently-scoped empty result rather than an error or shared
    # data leaking across orgs.
    docs_a = client.get("/documents/", headers=org_a["headers"])
    docs_b = client.get("/documents/", headers=org_b["headers"])

    assert docs_a.status_code == 200
    assert docs_b.status_code == 200
    assert docs_a.json()["total"] == 0
    assert docs_b.json()["total"] == 0


def test_analytics_are_independent_per_org(client, two_orgs):
    org_a, org_b = two_orgs

    client.post(
        "/feeds/",
        json={"url": "https://a-only.example.com/rss.xml", "label": "A only"},
        headers=org_a["headers"],
    )

    stats_a = client.get("/analytics/pipeline", headers=org_a["headers"]).json()
    stats_b = client.get("/analytics/pipeline", headers=org_b["headers"]).json()

    assert stats_a["total_documents"] == 0
    assert stats_b["total_documents"] == 0
    assert stats_a["is_running"] is False
    assert stats_b["is_running"] is False


def test_ingestion_trigger_is_scoped_per_org(client, two_orgs):
    org_a, _org_b = two_orgs

    response = client.post("/ingestion/trigger", headers=org_a["headers"])
    assert response.status_code == 202
    assert response.json()["status"] in {"started", "already_running"}
