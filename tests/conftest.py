from __future__ import annotations

from datetime import datetime, timezone

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import event

from cms.main import app
from cms.infrastructure.db.models import Base
from cms.interfaces.http.deps import get_session as prod_get_session
from cms.infrastructure.repositories.auth_repo import SQLAlchemyUserRepository
from cms.infrastructure.auth.passwords import hash_password
from cms.infrastructure.auth.tokens import create_access_token


@pytest.fixture(scope="function")
async def test_engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

    @event.listens_for(engine.sync_engine, "connect")
    def _fk_pragma(dbapi_connection, connection_record) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    try:
        yield engine
    finally:
        await engine.dispose()


@pytest.fixture(scope="function")
async def session_maker(test_engine):
    return async_sessionmaker(test_engine, expire_on_commit=False)


@pytest.fixture(scope="function")
async def async_session(session_maker):
    async with session_maker() as session:  # type: AsyncSession
        yield session
        await session.rollback()


@pytest.fixture(scope="function")
async def client(session_maker):
    async def override_get_session():
        async with session_maker() as session:  # type: AsyncSession
            yield session

    app.dependency_overrides[prod_get_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
def admin_credentials() -> tuple[str, str]:
    return ("admin@example.com", "admin-pass")


@pytest.fixture
async def admin_user(session_maker, admin_credentials):
    email, password = admin_credentials
    async with session_maker() as session:  # type: AsyncSession
        repo = SQLAlchemyUserRepository(session)
        return await repo.add(
            email=email,
            password_hash=hash_password(password),
            is_active=True,
            is_admin=True,
            created_at=datetime.now(timezone.utc),
        )


@pytest.fixture
async def admin_auth_header(admin_user) -> dict[str, str]:
    assert admin_user.id is not None
    token = create_access_token(admin_user.id)
    return {"Authorization": f"Bearer {token}"}
