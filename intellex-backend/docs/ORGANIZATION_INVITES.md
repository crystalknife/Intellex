# Organization Invites & Member Management

## What this is

Every signup previously created a brand-new organization with that
user as its sole owner -- there was no way to bring a teammate into an
*existing* org. This adds that, plus member listing, role changes, and
removal.

## Endpoints

- `GET /organization/members` -- any member of the org
- `PATCH /organization/members/{user_id}` -- owner only
- `DELETE /organization/members/{user_id}` -- owner only
- `GET /organization/invites` -- owner only
- `POST /organization/invites` -- owner only
- `DELETE /organization/invites/{invite_id}` -- owner only

`POST /auth/signup` gained an optional `invite_token` field.

## Why invites instead of "add existing user by email"

The obvious first design -- an owner adds any existing Intellex user to
their org by email -- doesn't work with this project's data model:
every account already owns its own organization from signup, so
"add an existing user" would either need to support one user
belonging to multiple organizations (which needs an org-switcher, none
of which exists) or would just never succeed for anyone with an
account.

Instead: an owner creates an invite (email + role), gets back a token,
and shares it with the invitee themselves -- there's no email
infrastructure in this project, so nothing sends that invite
automatically. The invitee redeems the token via
`POST /auth/signup`'s `invite_token` field, which joins them directly
to the inviting org (with the invited role) instead of creating a new
org for them. This is fully backward compatible: signup without an
`invite_token` behaves exactly as before.

Invites expire after 7 days and can only be redeemed once. An invite
for an email that already has an Intellex account (and therefore
already belongs to its own org) is rejected up front, for the same
single-org-per-user reason.

## Role rules

- `owner`, `admin`, `member`.
- Only owners can manage members/invites -- no separate admin
  permission tier yet, kept simple until something needs more.
- An organization can never end up with zero owners: demoting or
  removing the last remaining owner is rejected with a clear error
  telling the caller to promote someone else first.
