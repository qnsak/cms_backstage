from __future__ import annotations

import pytest

from httpx import Response


@pytest.mark.asyncio
async def test_tag_create_and_delete_flow(create_tag, delete_tag) -> None:
    res: Response = await create_tag()
    assert res.status_code == 200
    created = res.json()
    assert created["slug"] == "python"

    res = await delete_tag("python")
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_tag_delete_fails_when_in_use(
    create_tag,
    create_article,
    delete_tag,
) -> None:
    res: Response = await create_tag()
    assert res.status_code == 200

    res = await create_article(tags=["python"])
    assert res.status_code == 200

    res = await delete_tag("python")
    assert res.status_code == 400
