from __future__ import annotations

import pytest

from cms.domain.tags.entities import Tag
from cms.infrastructure.db.models import Article, Tag as TagModel, ArticleTag
from cms.infrastructure.repositories.tag_repo import SQLAlchemyTagRepository


@pytest.mark.asyncio
async def test_tag_repo_add_and_list(async_session) -> None:
    repo = SQLAlchemyTagRepository(async_session)

    await repo.add(Tag(slug="python", name="Python"))
    await repo.add(Tag(slug="fastapi", name="FastAPI"))

    tags = await repo.list_all()
    slugs = {t.slug for t in tags}
    assert {"python", "fastapi"} <= slugs


@pytest.mark.asyncio
async def test_tag_repo_count_usage(async_session) -> None:
    tag = TagModel(slug="python", name="Python")
    article = Article(
        slug="20260127_0001_hello_fastapi",
        title="Hello",
        body_md="# Hello",
        published_at=None,
    )
    async_session.add_all([tag, article])
    await async_session.flush()

    async_session.add(ArticleTag(article_id=article.id, tag_id=tag.id))
    await async_session.commit()

    repo = SQLAlchemyTagRepository(async_session)
    usage = await repo.count_usage(tag.id)
    assert usage == 1
