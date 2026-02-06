from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timedelta

from cms.domain.auth.repositories import RefreshTokenRepository


async def rotate_refresh_token(
    refresh_repo: RefreshTokenRepository,
    token_hash: str,
    now: datetime,
    refresh_ttl_days: int,
    generate_refresh_token: Callable[[], str],
    hash_refresh_token: Callable[[str], str],
) -> tuple[int, str]:
    new_token = generate_refresh_token()
    new_hash = hash_refresh_token(new_token)
    new_expires = now + timedelta(days=refresh_ttl_days)
    user_id = await refresh_repo.use_and_rotate(
        token_hash=token_hash,
        new_token_hash=new_hash,
        new_expires_at=new_expires,
        now=now,
    )
    if user_id is None:
        raise ValueError("invalid_refresh_token")
    return user_id, new_token
