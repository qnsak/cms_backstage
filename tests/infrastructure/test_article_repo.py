from __future__ import annotations

import pytest

from cms.infrastructure.db.models import Article
from cms.infrastructure.repositories.article_repo import SQLAlchemyArticleRepository


@pytest.mark.asyncio
async def test_article_repo_add_and_get(async_session) -> None:
    article = Article(
        slug="20260127_0001_hello_fastapi",
        title="Hello",
        body_md="# Hello",
        published_at="2026-01-27T10:00:00Z",
    )

    async_session.add(article)
    await async_session.commit()

    repo = SQLAlchemyArticleRepository(async_session)
    loaded = await repo.get_by_slug(article.slug)

    assert loaded is not None
    assert loaded.title == "Hello"


@pytest.mark.asyncio
async def test_article_repo_list_only_published(async_session) -> None:
    draft = Article(
        slug="20260127_0001_draft",
        title="Draft",
        body_md="draft",
        published_at=None,
    )
    published = Article(
        slug="20260127_0002_pub",
        title="Published",
        body_md="pub",
        published_at="2026-01-27T10:00:00Z",
    )

    async_session.add_all([draft, published])
    await async_session.commit()

    repo = SQLAlchemyArticleRepository(async_session)
    items = await repo.list_published(page=1, page_size=10)

    assert len(items) == 1
    assert items[0].slug == "20260127_0002_pub"
