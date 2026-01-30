from __future__ import annotations

import pytest

from httpx import Response


@pytest.mark.asyncio
async def test_full_article_flow(
    create_article,
    get_admin_article,
    publish_article,
    list_contents,
) -> None:
    # 1) Create draft
    res: Response = await create_article(tags=["python"])
    assert res.status_code == 200
    created = res.json()
    assert created["published_at"] is None
    article_slug = created["slug"]

    # 2) Admin preview should work for draft
    res = await get_admin_article(article_slug)
    assert res.status_code == 200

    # 3) Publish
    res = await publish_article(article_slug)
    assert res.status_code == 200

    # 4) Public list should include it
    res = await list_contents()
    assert res.status_code == 200
    items = res.json()
    assert any(a["slug"] == article_slug for a in items)
