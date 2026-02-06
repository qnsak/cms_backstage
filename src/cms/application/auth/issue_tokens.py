from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timedelta

from cms.domain.auth.entities import User
from cms.domain.auth.repositories import RefreshTokenRepository


async def issue_tokens(
    user: User,
    refresh_repo: RefreshTokenRepository,
    now: datetime,
    refresh_ttl_days: int,
    create_access_token: Callable[[int], str],
    generate_refresh_token: Callable[[], str],
    hash_refresh_token: Callable[[str], str],
) -> tuple[str, str]:
    if user.id is None:
        raise ValueError("user_id_required")

    access_token = create_access_token(user.id)
    refresh_token = generate_refresh_token()
    refresh_hash = hash_refresh_token(refresh_token)
    expires_at = now + timedelta(days=refresh_ttl_days)
    await refresh_repo.create(
        user_id=user.id,
        token_hash=refresh_hash,
        expires_at=expires_at,
        created_at=now,
    )
    return access_token, refresh_token
