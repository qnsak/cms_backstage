from __future__ import annotations

from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from cms.infrastructure.db.models import Article, Tag
from cms.domain.articles.services import build_article_slug


async def create_article(
    session: AsyncSession,
    frontend_slug: str,
    title: str,
    body_md: str,
    tag_slugs: list[str],
) -> Article:
    slug = await build_article_slug(session, frontend_slug)

    tags: list[Tag] = []
    for t_slug in tag_slugs:
        tag: Tag | None = await session.scalar(select(Tag).where(Tag.slug == t_slug))
        if tag is None:
            tag = Tag(slug=t_slug, name=t_slug)
            session.add(tag)
        tags.append(tag)

    article = Article(
        slug=slug,
        title=title,
        body_md=body_md,
        published_at=None,
        tags=tags,
    )

    session.add(article)
    await session.commit()
    await session.refresh(article)
    return article


async def update_article(
    session: AsyncSession,
    slug: str,
    title: str,
    body_md: str,
    tag_slugs: list[str],
) -> Article | None:
    article: Article | None = await session.scalar(select(Article).where(Article.slug == slug))
    if article is None:
        return None

    article.title = title
    article.body_md = body_md

    tags: list[Tag] = []
    for t_slug in tag_slugs:
        tag: Tag | None = await session.scalar(select(Tag).where(Tag.slug == t_slug))
        if tag is None:
            tag = Tag(slug=t_slug, name=t_slug)
            session.add(tag)
        tags.append(tag)

    article.tags = tags
    await session.commit()
    await session.refresh(article)
    return article


async def publish_article(session: AsyncSession, slug: str) -> Article | None:
    article: Article | None = await session.scalar(select(Article).where(Article.slug == slug))
    if article is None:
        return None

    if article.published_at is None:
        article.published_at = datetime.utcnow().isoformat()

    await session.commit()
    await session.refresh(article)
    return article
