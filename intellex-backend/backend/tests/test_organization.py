"""Tests for /organization/* and invite-based signup."""

import pytest


def test_signup_without_invite_or_org_name_fails(client, unique_email):
    response = client.post(
        "/auth/signup",
        json={"email": unique_email, "password": "password12345"},
    )
    assert response.status_code == 422


def test_owner_can_create_and_list_invite(client, signed_up_org, unique_email):
    response = client.post(
        "/organization/invites",
        json={"email": unique_email, "role": "member"},
        headers=signed_up_org["headers"],
    )
    assert response.status_code == 201
    assert "token" in response.json()

    invites = client.get(
        "/organization/invites", headers=signed_up_org["headers"]
    ).json()
    assert len(invites["items"]) == 1


def test_invite_is_not_visible_to_other_orgs(client, two_orgs, unique_email):
    org_a, org_b = two_orgs

    client.post(
        "/organization/invites",
        json={"email": unique_email},
        headers=org_a["headers"],
    )

    invites_b = client.get(
        "/organization/invites", headers=org_b["headers"]
    ).json()
    assert len(invites_b["items"]) == 0


def test_non_owner_cannot_create_invite(client, signed_up_org, unique_email):
    invite = client.post(
        "/organization/invites",
        json={"email": unique_email},
        headers=signed_up_org["headers"],
    )
    token = invite.json()["token"]

    join = client.post(
        "/auth/signup",
        json={
            "email": unique_email,
            "password": "password12345",
            "invite_token": token,
        },
    )
    member_headers = {
        "Authorization": f"Bearer {join.json()['access_token']}"
    }

    response = client.post(
        "/organization/invites",
        json={"email": "someone@else.com"},
        headers=member_headers,
    )
    assert response.status_code == 403


def test_signup_with_invite_token_joins_existing_org(
    client, signed_up_org, unique_email
):
    invite = client.post(
        "/organization/invites",
        json={"email": unique_email, "role": "admin"},
        headers=signed_up_org["headers"],
    )
    token = invite.json()["token"]

    response = client.post(
        "/auth/signup",
        json={
            "email": unique_email,
            "password": "password12345",
            "invite_token": token,
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["organization"]["id"] == signed_up_org["org_id"]
    assert body["role"] == "admin"


def test_invite_cannot_be_reused(client, signed_up_org, unique_email):
    invite = client.post(
        "/organization/invites",
        json={"email": unique_email},
        headers=signed_up_org["headers"],
    )
    token = invite.json()["token"]

    client.post(
        "/auth/signup",
        json={
            "email": unique_email,
            "password": "password12345",
            "invite_token": token,
        },
    )

    second = client.post(
        "/auth/signup",
        json={
            "email": f"other-{unique_email}",
            "password": "password12345",
            "invite_token": token,
        },
    )
    assert second.status_code == 400


def test_invite_rejects_mismatched_email(client, signed_up_org, unique_email):
    invite = client.post(
        "/organization/invites",
        json={"email": unique_email},
        headers=signed_up_org["headers"],
    )
    token = invite.json()["token"]

    response = client.post(
        "/auth/signup",
        json={
            "email": f"not-{unique_email}",
            "password": "password12345",
            "invite_token": token,
        },
    )
    assert response.status_code == 400


def test_cannot_invite_user_with_existing_org(client, two_orgs):
    org_a, org_b = two_orgs

    response = client.post(
        "/organization/invites",
        json={"email": org_b["user_email"]},
        headers=org_a["headers"],
    )
    assert response.status_code == 409


def test_revoke_invite(client, signed_up_org, unique_email):
    invite = client.post(
        "/organization/invites",
        json={"email": unique_email},
        headers=signed_up_org["headers"],
    )
    invite_id = invite.json()["id"]

    revoke = client.delete(
        f"/organization/invites/{invite_id}", headers=signed_up_org["headers"]
    )
    assert revoke.status_code == 204

    remaining = client.get(
        "/organization/invites", headers=signed_up_org["headers"]
    ).json()
    assert len(remaining["items"]) == 0


@pytest.fixture()
def org_with_member(client, signed_up_org, unique_email):
    """An org with its original owner plus one invited member."""

    invite = client.post(
        "/organization/invites",
        json={"email": unique_email, "role": "member"},
        headers=signed_up_org["headers"],
    )
    token = invite.json()["token"]

    join = client.post(
        "/auth/signup",
        json={
            "email": unique_email,
            "password": "password12345",
            "invite_token": token,
        },
    )
    member_headers = {
        "Authorization": f"Bearer {join.json()['access_token']}"
    }

    members = client.get(
        "/organization/members", headers=signed_up_org["headers"]
    ).json()["items"]
    owner_id = next(
        m["user_id"]
        for m in members
        if m["email"] == signed_up_org["user_email"]
    )
    member_id = next(
        m["user_id"] for m in members if m["email"] == unique_email
    )

    return {
        **signed_up_org,
        "member_headers": member_headers,
        "owner_id": owner_id,
        "member_id": member_id,
    }


def test_non_owner_cannot_change_roles(client, org_with_member):
    response = client.patch(
        f"/organization/members/{org_with_member['owner_id']}",
        json={"role": "member"},
        headers=org_with_member["member_headers"],
    )
    assert response.status_code == 403


def test_cannot_demote_last_owner(client, org_with_member):
    response = client.patch(
        f"/organization/members/{org_with_member['owner_id']}",
        json={"role": "member"},
        headers=org_with_member["headers"],
    )
    assert response.status_code == 409


def test_cannot_remove_last_owner(client, org_with_member):
    response = client.delete(
        f"/organization/members/{org_with_member['owner_id']}",
        headers=org_with_member["headers"],
    )
    assert response.status_code == 409


def test_owner_can_promote_and_remove_member(client, org_with_member):
    promote = client.patch(
        f"/organization/members/{org_with_member['member_id']}",
        json={"role": "admin"},
        headers=org_with_member["headers"],
    )
    assert promote.status_code == 200
    assert promote.json()["role"] == "admin"

    remove = client.delete(
        f"/organization/members/{org_with_member['member_id']}",
        headers=org_with_member["headers"],
    )
    assert remove.status_code == 204

    remaining = client.get(
        "/organization/members", headers=org_with_member["headers"]
    ).json()["items"]
    assert len(remaining) == 1
