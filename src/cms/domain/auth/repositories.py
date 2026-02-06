from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from cms.domain.auth.entities import User, RefreshToken


class UserRepository(ABC):

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def add(
        self,
        email: str,
        password_hash: str,
        is_active: bool,
        is_admin: bool,
        created_at: datetime,
    ) -> User:
        raise NotImplementedError


class RefreshTokenRepository(ABC):

    @abstractmethod
    async def create(
        self,
        user_id: int,
        token_hash: str,
        expires_at: datetime,
        created_at: datetime,
    ) -> RefreshToken:
        raise NotImplementedError

    @abstractmethod
    async def revoke(self, token_hash: str, revoked_at: datetime) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def use_and_rotate(
        self,
        token_hash: str,
        new_token_hash: str,
        new_expires_at: datetime,
        now: datetime,
    ) -> int | None:
        raise NotImplementedError
