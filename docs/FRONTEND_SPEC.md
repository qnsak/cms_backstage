# Frontend Spec (Auth + Admin Protection)

## Goal
Add a minimal admin UI auth flow that integrates with the new Access/Refresh token system:
- Access token (JWT) is returned by `/api/auth/login` and used in `Authorization: Bearer ...`.
- Refresh token is stored in HttpOnly cookie and used implicitly by `/api/auth/refresh`.
- Only `/api/admin/*` endpoints require auth.

## User Flows
1. **Login**
   - Screen: email + password form.
   - On submit:
     - `POST /api/auth/login` with JSON body `{ email, password }`.
     - On success, receive `{ access_token, token_type }`.
     - Store `access_token` in memory (preferred) or sessionStorage.
     - Redirect to admin landing page.
   - On failure: show inline error (`Invalid credentials`).

2. **Access Protected Admin**
   - Any admin view request uses `Authorization: Bearer <access_token>`.
   - If `401` (missing/expired): call refresh flow.
   - If `403`: show “Forbidden”.

3. **Refresh Access Token**
   - Trigger:
     - On `401` from `/api/admin/*`.
     - Or proactively when token is near expiry (optional).
   - `POST /api/auth/refresh`.
   - Server uses HttpOnly refresh cookie to validate.
   - On success:
     - Update in-memory access token.
     - Retry the original request once.
   - On failure:
     - Clear access token and redirect to login.

4. **Logout**
   - `POST /api/auth/logout`.
   - Clear in-memory access token.
   - Redirect to login.

## API Integration
- Login: `POST /api/auth/login`
- Refresh: `POST /api/auth/refresh`
- Logout: `POST /api/auth/logout`
- Admin routes: `/api/admin/*`
- Public routes remain unchanged.

## Token Handling
- Access token:
  - Stored in memory (default).
  - Optional: store in `sessionStorage` to survive reloads.
  - Never store refresh token in JS-accessible storage.
- Refresh token:
  - HttpOnly cookie; not accessible to JS.

## Error Handling
- `401` on admin endpoints → attempt refresh once.
- `401` on refresh or login → show login screen.
- `403` → show forbidden page.
- Network errors → show retry UI.

## UI Screens (Minimal)
1. **Login page**
   - Email + password inputs.
   - Submit button.
   - Error message area.

2. **Admin layout**
   - Top bar with “Logout”.
   - Standard admin list/detail UI (existing or to be added later).

3. **Forbidden page**
   - Message + “Back to login”.

## Client Architecture (Suggested)
- `AuthService` module:
  - `login(email, password)` → returns access token.
  - `refresh()` → returns new access token.
  - `logout()` → void.
- `ApiClient` wrapper:
  - Injects `Authorization` header.
  - Handles `401` → refresh → retry once.

## Security Notes
- Use HTTPS in production so `Secure` cookie works.
- Avoid storing access token in `localStorage`.
- Ensure CORS allows credentials if frontend is on a different origin.

## Non-Goals
- User management screens (create users, reset password).
- Role management beyond admin vs non-admin.
