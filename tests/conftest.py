from __future__ import annotations

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import event

from cms.main import app
from cms.infrastructure.db.models import Base
from cms.interfaces.http.articles import get_session as prod_get_session


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

    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c

    app.dependency_overrides.clear()
