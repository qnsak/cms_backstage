from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from cms.infrastructure.db.models import Article, ArticleTag


async def delete_article(session: AsyncSession, slug: str) -> bool:
    article: Article | None = await session.scalar(select(Article).where(Article.slug == slug))
    if article is None:
        return False

    # Remove associations explicitly (safe for SQLite FK constraints)
    await session.execute(
        ArticleTag.__table__.delete().where(ArticleTag.article_id == article.id)
    )

    await session.delete(article)
    await session.commit()
    return True
