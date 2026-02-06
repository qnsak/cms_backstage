from __future__ import annotations

from datetime import datetime, timedelta, timezone
import hashlib
import secrets

import jwt
from jwt import InvalidTokenError

from cms.infrastructure.auth.settings import JWT_SECRET, ACCESS_TOKEN_TTL_MIN


class TokenError(ValueError):
    pass


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def create_access_token(user_id: int) -> str:
    exp = _utcnow() + timedelta(minutes=ACCESS_TOKEN_TTL_MIN)
    payload = {"sub": str(user_id), "type": "access", "exp": exp}
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except InvalidTokenError as exc:
        raise TokenError("Invalid token") from exc

    if payload.get("type") != "access":
        raise TokenError("Invalid token type")
    return payload


def generate_refresh_token() -> str:
    return secrets.token_urlsafe(48)


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
