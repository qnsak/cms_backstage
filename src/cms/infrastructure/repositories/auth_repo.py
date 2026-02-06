from __future__ import annotations

from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from cms.domain.auth.entities import User, RefreshToken
from cms.domain.auth.repositories import UserRepository, RefreshTokenRepository
from cms.infrastructure.db.models import User as UserModel, RefreshToken as RefreshTokenModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def _to_domain(self, model: UserModel) -> User:
        return User(
            id=model.id,
            email=model.email,
            password_hash=model.password_hash,
            is_active=model.is_active,
            is_admin=model.is_admin,
            created_at=model.created_at,
        )

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email),
        )
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._to_domain(model)

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id),
        )
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._to_domain(model)

    async def add(
        self,
        email: str,
        password_hash: str,
        is_active: bool,
        is_admin: bool,
        created_at: datetime,
    ) -> User:
        model = UserModel(
            email=email,
            password_hash=password_hash,
            is_active=is_active,
            is_admin=is_admin,
            created_at=created_at,
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)


class SQLAlchemyRefreshTokenRepository(RefreshTokenRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def _to_domain(self, model: RefreshTokenModel) -> RefreshToken:
        return RefreshToken(
            id=model.id,
            user_id=model.user_id,
            token_hash=model.token_hash,
            expires_at=model.expires_at,
            revoked_at=model.revoked_at,
            created_at=model.created_at,
            last_used_at=model.last_used_at,
        )

    async def create(
        self,
        user_id: int,
        token_hash: str,
        expires_at: datetime,
        created_at: datetime,
    ) -> RefreshToken:
        model = RefreshTokenModel(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            revoked_at=None,
            created_at=created_at,
            last_used_at=None,
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def revoke(self, token_hash: str, revoked_at: datetime) -> bool:
        result = await self.session.execute(
            update(RefreshTokenModel)
            .where(
                RefreshTokenModel.token_hash == token_hash,
                RefreshTokenModel.revoked_at.is_(None),
            )
            .values(revoked_at=revoked_at),
        )
        await self.session.commit()
        return (result.rowcount or 0) > 0

    async def use_and_rotate(
        self,
        token_hash: str,
        new_token_hash: str,
        new_expires_at: datetime,
        now: datetime,
    ) -> int | None:
        async with self.session.begin():
            result = await self.session.execute(
                select(RefreshTokenModel).where(
                    RefreshTokenModel.token_hash == token_hash,
                    RefreshTokenModel.revoked_at.is_(None),
                    RefreshTokenModel.expires_at > now,
                )
            )
            model = result.scalar_one_or_none()
            if model is None:
                return None

            update_result = await self.session.execute(
                update(RefreshTokenModel)
                .where(
                    RefreshTokenModel.id == model.id,
                    RefreshTokenModel.revoked_at.is_(None),
                )
                .values(revoked_at=now, last_used_at=now),
            )
            if (update_result.rowcount or 0) != 1:
                return None

            new_model = RefreshTokenModel(
                user_id=model.user_id,
                token_hash=new_token_hash,
                expires_at=new_expires_at,
                revoked_at=None,
                created_at=now,
                last_used_at=None,
            )
            self.session.add(new_model)
            return model.user_id
