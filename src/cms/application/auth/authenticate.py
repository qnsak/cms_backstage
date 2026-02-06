from __future__ import annotations

from collections.abc import Callable

from cms.domain.auth.entities import User
from cms.domain.auth.repositories import UserRepository


async def authenticate_user(
    user_repo: UserRepository,
    email: str,
    password: str,
    verify_password: Callable[[str, str], bool],
) -> User | None:
    user = await user_repo.get_by_email(email)
    if user is None or not user.is_active:
        return None
    if not verify_password(user.password_hash, password):
        return None
    return user
