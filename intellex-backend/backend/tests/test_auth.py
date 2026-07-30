"""Tests for POST /auth/signup, POST /auth/login, GET /auth/me."""


def test_signup_creates_user_and_org_as_owner(client, unique_email):
    response = client.post(
        "/auth/signup",
        json={
            "email": unique_email,
            "password": "password12345",
            "full_name": "Ada Lovelace",
            "organization_name": "Analytical Engines Inc",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["role"] == "owner"
    assert body["organization"]["name"] == "Analytical Engines Inc"
    assert body["user"]["email"] == unique_email
    assert "access_token" in body and body["access_token"]


def test_signup_rejects_duplicate_email(client, unique_email):
    payload = {
        "email": unique_email,
        "password": "password12345",
        "organization_name": "First Org",
    }
    first = client.post("/auth/signup", json=payload)
    assert first.status_code == 201

    payload["organization_name"] = "Second Org"
    second = client.post("/auth/signup", json=payload)
    assert second.status_code == 409


def test_login_with_correct_password_succeeds(client, signed_up_org):
    response = client.post(
        "/auth/login",
        json={
            "email": signed_up_org["user_email"],
            "password": "password12345",
        },
    )

    assert response.status_code == 200
    assert response.json()["organization"]["name"] == signed_up_org["org_name"]


def test_login_with_wrong_password_fails(client, signed_up_org):
    response = client.post(
        "/auth/login",
        json={"email": signed_up_org["user_email"], "password": "wrong-password"},
    )

    assert response.status_code == 401


def test_login_with_unknown_email_fails(client):
    response = client.post(
        "/auth/login",
        json={"email": "nobody@nowhere.com", "password": "whatever12345"},
    )

    assert response.status_code == 401


def test_me_requires_a_token(client):
    assert client.get("/auth/me").status_code == 401


def test_me_rejects_garbage_token(client):
    response = client.get(
        "/auth/me", headers={"Authorization": "Bearer not-a-real-token"}
    )
    assert response.status_code == 401


def test_me_returns_correct_identity(client, signed_up_org):
    response = client.get("/auth/me", headers=signed_up_org["headers"])

    assert response.status_code == 200
    body = response.json()
    assert body["user"]["email"] == signed_up_org["user_email"]
    assert body["organization"]["name"] == signed_up_org["org_name"]
    assert body["role"] == "owner"
