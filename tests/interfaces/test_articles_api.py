from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_full_article_flow(client) -> None:
    # 1) Create draft
    res = await client.post(
        "/api/articles",
        json={
            "slug": "hello_fastapi",
            "title": "Draft Post",
            "body_md": "# Draft",
            "tags": ["python"],
        },
    )
    assert res.status_code == 200
    created = res.json()
    assert created["published_at"] is None
    article_slug = created["slug"]

    # 2) Admin preview should work for draft
    res = await client.get(f"/api/admin/articles/{article_slug}")
    assert res.status_code == 200

    # 3) Publish
    res = await client.post(f"/api/articles/{article_slug}/publish")
    assert res.status_code == 200

    # 4) Public list should include it
    res = await client.get("/api/contents")
    assert res.status_code == 200
    items = res.json()
    assert any(a["slug"] == article_slug for a in items)
