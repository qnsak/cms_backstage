from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from cms.infrastructure.db.models import Article
from cms.domain.articles.repositories import ArticleRepository


class SQLAlchemyArticleRepository(ArticleRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_published(self, page: int, page_size: int) -> list[Article]:
        offset = (page - 1) * page_size
        stmt = (
            select(Article)
            .options(selectinload(Article.tags))
            .where(Article.published_at.is_not(None))
            .offset(offset)
            .limit(page_size)
        )
        result = await self.session.scalars(stmt)
        return list(result)

    async def list_all(self, page: int, page_size: int) -> list[Article]:
        offset = (page - 1) * page_size
        stmt = (
            select(Article)
            .options(selectinload(Article.tags))
            .offset(offset)
            .limit(page_size)
        )
        result = await self.session.scalars(stmt)
        return list(result)

    async def list_drafts(self, page: int, page_size: int) -> list[Article]:
        offset = (page - 1) * page_size
        stmt = (
            select(Article)
            .options(selectinload(Article.tags))
            .where(Article.published_at.is_(None))
            .offset(offset)
            .limit(page_size)
        )
        result = await self.session.scalars(stmt)
        return list(result)

    async def get_by_slug(self, slug: str) -> Article | None:
        stmt = (
            select(Article)
            .options(selectinload(Article.tags))
            .where(Article.slug == slug)
        )
        return await self.session.scalar(stmt)
