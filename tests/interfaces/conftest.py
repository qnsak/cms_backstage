from __future__ import annotations

from collections.abc import Awaitable, Callable

import pytest
from httpx import AsyncClient, Response


@pytest.fixture
def create_tag(
    client: AsyncClient,
    admin_auth_header: dict[str, str],
) -> Callable[[str, str], Awaitable[Response]]:
    async def _create(slug: str = "python", name: str = "Python") -> Response:
        return await client.post(
            "/api/admin/tags",
            json={"slug": slug, "name": name},
            headers=admin_auth_header,
        )

    return _create


@pytest.fixture
def delete_tag(
    client: AsyncClient,
    admin_auth_header: dict[str, str],
) -> Callable[[str], Awaitable[Response]]:
    async def _delete(slug: str) -> Response:
        return await client.delete(
            f"/api/admin/tags/{slug}",
            headers=admin_auth_header,
        )

    return _delete


@pytest.fixture
def list_admin_tags(
    client: AsyncClient,
    admin_auth_header: dict[str, str],
) -> Callable[[], Awaitable[Response]]:
    async def _list() -> Response:
        return await client.get("/api/admin/tags", headers=admin_auth_header)

    return _list


@pytest.fixture
def create_article(client: AsyncClient) -> Callable[..., Awaitable[Response]]:
    async def _create(
        slug: str = "hello_fastapi",
        title: str = "Draft Post",
        body_md: str = "# Draft",
        tags: list[str] | None = None,
    ) -> Response:
        return await client.post(
            "/api/articles",
            json={
                "slug": slug,
                "title": title,
                "body_md": body_md,
                "tags": tags or [],
            },
        )

    return _create


@pytest.fixture
def publish_article(client: AsyncClient) -> Callable[[str], Awaitable[Response]]:
    async def _publish(slug: str) -> Response:
        return await client.post(f"/api/articles/{slug}/publish")

    return _publish


@pytest.fixture
def get_admin_article(
    client: AsyncClient,
    admin_auth_header: dict[str, str],
) -> Callable[[str], Awaitable[Response]]:
    async def _get(slug: str) -> Response:
        return await client.get(
            f"/api/admin/articles/{slug}",
            headers=admin_auth_header,
        )

    return _get


@pytest.fixture
def list_contents(client: AsyncClient) -> Callable[[], Awaitable[Response]]:
    async def _list() -> Response:
        return await client.get("/api/contents")

    return _list


@pytest.fixture
def list_admin_articles(
    client: AsyncClient,
    admin_auth_header: dict[str, str],
) -> Callable[[], Awaitable[Response]]:
    async def _list() -> Response:
        return await client.get("/api/admin/articles", headers=admin_auth_header)

    return _list
