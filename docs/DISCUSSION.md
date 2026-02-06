# Discussion Log

## 2026-02-05 - Auth Strategy (Access/Refresh)

Context:
- Added token-based auth with access + refresh tokens.
- Scope: only protect `/api/admin/*`.
- Refresh token stored in HttpOnly cookie.
- Password hashing uses Argon2.

Decisions:
- Access token: JWT, short-lived, returned in JSON response.
- Refresh token: long-lived, HttpOnly cookie, stored hashed in DB.
- Refresh is rotated on each use; old token revoked.
- Refresh concurrency: single-use; concurrent refresh attempts result in one success and others failing.
- Admin endpoints require `Authorization: Bearer <access_token>`.

Open items:
- Add user management endpoints (optional, not part of initial scope).
- Decide on production cookie settings (SameSite/Domain/Secure).
