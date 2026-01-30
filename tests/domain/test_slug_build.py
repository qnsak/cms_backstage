from __future__ import annotations

import re
from datetime import datetime, timezone

import pytest

from cms.domain.articles.services import build_article_slug


class FakeArticleRepo:
    def __init__(self) -> None:
        self._slugs: list[str] = []

    async def get_latest_slug_by_prefix(self, prefix: str) -> str | None:
        candidates = [slug for slug in self._slugs if slug.startswith(prefix)]
        return max(candidates) if candidates else None

    def add_slug(self, slug: str) -> None:
        self._slugs.append(slug)


@pytest.mark.asyncio
async def test_build_article_slug_formats_and_increments_sequence() -> None:
    repo = FakeArticleRepo()
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    pattern = re.compile(rf"^{today}_\d{{4}}_hello_fastapi$")

    first = await build_article_slug(repo, "hello_fastapi")
    assert pattern.match(first)

    # Simulate persistence of the first slug.
    repo.add_slug(first)

    second = await build_article_slug(repo, "hello_fastapi")
    assert pattern.match(second)
    assert second != first


@pytest.mark.asyncio
async def test_build_article_slug_rejects_invalid_frontend_slug() -> None:
    repo = FakeArticleRepo()
    with pytest.raises(ValueError):
        await build_article_slug(repo, "hello-fastapi")
