from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Header, HTTPException, Response, Cookie
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from cms.application.auth.authenticate import authenticate_user
from cms.application.auth.issue_tokens import issue_tokens
from cms.application.auth.refresh import rotate_refresh_token
from cms.infrastructure.auth.passwords import verify_password
from cms.infrastructure.auth.tokens import (
    create_access_token,
    decode_access_token,
    hash_refresh_token,
    generate_refresh_token,
    TokenError,
)
from cms.infrastructure.auth.settings import (
    AUTH_COOKIE_SECURE,
    AUTH_COOKIE_SAMESITE,
    REFRESH_TOKEN_TTL_DAYS,
)
from cms.infrastructure.repositories.auth_repo import (
    SQLAlchemyUserRepository,
    SQLAlchemyRefreshTokenRepository,
)
from cms.interfaces.http.deps import get_session

router = APIRouter()


class RequestModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class LoginRequest(RequestModel):
    email: str
    password: str


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _set_refresh_cookie(response: Response, refresh_token: str) -> None:
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=AUTH_COOKIE_SECURE,
        samesite=AUTH_COOKIE_SAMESITE,
        path="/api/auth",
        max_age=REFRESH_TOKEN_TTL_DAYS * 24 * 60 * 60,
    )


def _clear_refresh_cookie(response: Response) -> None:
    response.delete_cookie(key="refresh_token", path="/api/auth")


@router.post("/api/auth/login")
async def login(
    req: LoginRequest,
    response: Response,
    session: AsyncSession = Depends(get_session),
) -> dict[str, str]:
    user_repo = SQLAlchemyUserRepository(session)
    refresh_repo = SQLAlchemyRefreshTokenRepository(session)

    user = await authenticate_user(
        user_repo=user_repo,
        email=req.email,
        password=req.password,
        verify_password=verify_password,
    )
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token, refresh_token = await issue_tokens(
        user=user,
        refresh_repo=refresh_repo,
        now=_now(),
        refresh_ttl_days=REFRESH_TOKEN_TTL_DAYS,
        create_access_token=create_access_token,
        generate_refresh_token=generate_refresh_token,
        hash_refresh_token=hash_refresh_token,
    )

    _set_refresh_cookie(response, refresh_token)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/api/auth/refresh")
async def refresh(
    response: Response,
    refresh_token: str | None = Cookie(None),
    session: AsyncSession = Depends(get_session),
) -> dict[str, str]:
    token = refresh_token
    if token is None:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    refresh_repo = SQLAlchemyRefreshTokenRepository(session)
    try:
        user_id, new_refresh = await rotate_refresh_token(
            refresh_repo=refresh_repo,
            token_hash=hash_refresh_token(token),
            now=_now(),
            refresh_ttl_days=REFRESH_TOKEN_TTL_DAYS,
            generate_refresh_token=generate_refresh_token,
            hash_refresh_token=hash_refresh_token,
        )
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access_token = create_access_token(user_id)
    _set_refresh_cookie(response, new_refresh)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/api/auth/logout")
async def logout(
    response: Response,
    refresh_token: str | None = Cookie(None),
    session: AsyncSession = Depends(get_session),
) -> dict[str, str]:
    if refresh_token:
        refresh_repo = SQLAlchemyRefreshTokenRepository(session)
        await refresh_repo.revoke(hash_refresh_token(refresh_token), _now())

    _clear_refresh_cookie(response)
    return {"message": "logged_out"}


async def get_current_admin_user(
    authorization: str | None = Header(None),
    session: AsyncSession = Depends(get_session),
) -> int:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing access token")

    token = authorization.split(" ", 1)[1]
    try:
        payload = decode_access_token(token)
    except TokenError:
        raise HTTPException(status_code=401, detail="Invalid access token")

    sub = payload.get("sub")
    if sub is None:
        raise HTTPException(status_code=401, detail="Invalid access token")

    try:
        user_id = int(sub)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid access token")

    user_repo = SQLAlchemyUserRepository(session)
    user = await user_repo.get_by_id(user_id)
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid access token")
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")

    return user_id
