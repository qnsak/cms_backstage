from __future__ import annotations

import pytest

from httpx import AsyncClient, Response


def _assert_article_list_item(item: dict) -> None:
    assert set(item.keys()) == {"slug", "title", "published_at", "tags"}
    assert isinstance(item["slug"], str)
    assert isinstance(item["title"], str)
    assert isinstance(item["tags"], list)
    assert all(isinstance(t, str) for t in item["tags"])
    assert item["published_at"] is None or isinstance(item["published_at"], str)


def _assert_article_detail_item(item: dict) -> None:
    assert set(item.keys()) == {"slug", "title", "body_md", "published_at", "tags"}
    assert isinstance(item["slug"], str)
    assert isinstance(item["title"], str)
    assert isinstance(item["body_md"], str)
    assert isinstance(item["tags"], list)
    assert all(isinstance(t, str) for t in item["tags"])
    assert item["published_at"] is None or isinstance(item["published_at"], str)


@pytest.mark.asyncio
async def test_health_contract(client: AsyncClient) -> None:
    res = await client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_article_create_contract(create_article) -> None:
    res: Response = await create_article(tags=["python"])
    assert res.status_code == 200
    payload = res.json()
    assert set(payload.keys()) == {"slug", "title", "published_at", "tags"}
    assert payload["published_at"] is None
    assert isinstance(payload["slug"], str)
    assert isinstance(payload["title"], str)
    assert payload["tags"] == ["python"]


@pytest.mark.asyncio
async def test_article_publish_contract(
    create_article,
    publish_article,
) -> None:
    res: Response = await create_article()
    article_slug = res.json()["slug"]

    res = await publish_article(article_slug)
    assert res.status_code == 200
    payload = res.json()
    assert set(payload.keys()) == {"slug", "published_at", "message"}
    assert payload["slug"] == article_slug
    assert payload["message"] == "published"
    assert isinstance(payload["published_at"], str)


@pytest.mark.asyncio
async def test_article_list_contract(
    create_article,
    publish_article,
    list_contents,
) -> None:
    res: Response = await create_article()
    article_slug = res.json()["slug"]
    await publish_article(article_slug)

    res = await list_contents()
    assert res.status_code == 200
    items = res.json()
    assert isinstance(items, list)
    assert any(item["slug"] == article_slug for item in items)
    for item in items:
        _assert_article_list_item(item)


@pytest.mark.asyncio
async def test_article_detail_contract(
    create_article,
    get_admin_article,
) -> None:
    res: Response = await create_article()
    article_slug = res.json()["slug"]

    res = await get_admin_article(article_slug)
    assert res.status_code == 200
    _assert_article_detail_item(res.json())


@pytest.mark.asyncio
async def test_article_not_found_contract(client: AsyncClient) -> None:
    res = await client.get("/api/contents/missing_slug")
    assert res.status_code == 404
    payload = res.json()
    assert set(payload.keys()) == {"detail"}
    assert isinstance(payload["detail"], str)


@pytest.mark.asyncio
async def test_article_update_not_found_contract(client: AsyncClient) -> None:
    res = await client.put(
        "/api/articles/missing_slug",
        json={
            "title": "Missing",
            "body_md": "Missing",
            "tags": [],
        },
    )
    assert res.status_code == 404
    payload = res.json()
    assert set(payload.keys()) == {"detail"}


@pytest.mark.asyncio
async def test_article_publish_not_found_contract(client: AsyncClient) -> None:
    res = await client.post("/api/articles/missing_slug/publish")
    assert res.status_code == 404
    payload = res.json()
    assert set(payload.keys()) == {"detail"}


@pytest.mark.asyncio
async def test_article_delete_not_found_contract(client: AsyncClient) -> None:
    res = await client.delete("/api/articles/missing_slug")
    assert res.status_code == 404
    payload = res.json()
    assert set(payload.keys()) == {"detail"}


@pytest.mark.asyncio
async def test_article_create_validation_error_contract(client: AsyncClient) -> None:
    res = await client.post("/api/articles", json={"slug": "only_slug"})
    assert res.status_code == 422
    payload = res.json()
    assert set(payload.keys()) == {"detail"}
    assert isinstance(payload["detail"], list)


@pytest.mark.asyncio
async def test_tag_create_validation_error_contract(
    client: AsyncClient,
    admin_auth_header: dict[str, str],
) -> None:
    res = await client.post(
        "/api/admin/tags",
        json={"slug": "python"},
        headers=admin_auth_header,
    )
    assert res.status_code == 422
    payload = res.json()
    assert set(payload.keys()) == {"detail"}
    assert isinstance(payload["detail"], list)


@pytest.mark.asyncio
async def test_tag_contracts(create_tag, list_admin_tags, delete_tag) -> None:
    res: Response = await create_tag()
    assert res.status_code == 200
    payload = res.json()
    assert set(payload.keys()) == {"slug", "name"}
    assert payload["slug"] == "python"
    assert payload["name"] == "Python"

    res = await list_admin_tags()
    assert res.status_code == 200
    items = res.json()
    assert isinstance(items, list)
    for item in items:
        assert set(item.keys()) == {"slug", "name"}
        assert isinstance(item["slug"], str)
        assert isinstance(item["name"], str)

    res = await delete_tag("python")
    assert res.status_code == 200
    payload = res.json()
    assert set(payload.keys()) == {"message", "slug"}


@pytest.mark.asyncio
async def test_tag_duplicate_and_missing_contracts(
    create_tag,
    delete_tag,
) -> None:
    res: Response = await create_tag()
    assert res.status_code == 200

    res = await create_tag()
    assert res.status_code == 400
    payload = res.json()
    assert set(payload.keys()) == {"detail"}
    assert isinstance(payload["detail"], str)

    res = await delete_tag("missing_tag")
    assert res.status_code == 404
    payload = res.json()
    assert set(payload.keys()) == {"detail"}
