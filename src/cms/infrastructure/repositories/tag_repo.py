from __future__ import annotations

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from cms.domain.tags.repositories import TagRepository
from cms.infrastructure.db.models import Tag, ArticleTag


class SQLAlchemyTagRepository(TagRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_all(self) -> list[Tag]:
        result = await self.session.scalars(select(Tag))
        return list(result)

    async def get_by_slug(self, slug: str) -> Tag | None:
        return await self.session.scalar(select(Tag).where(Tag.slug == slug))

    async def add(self, tag: Tag) -> None:
        self.session.add(tag)
        await self.session.commit()
        await self.session.refresh(tag)

    async def delete(self, tag: Tag) -> None:
        await self.session.delete(tag)
        await self.session.commit()

    async def count_usage(self, tag_id: int) -> int:
        return (
            await self.session.scalar(
                select(func.count()).select_from(ArticleTag).where(ArticleTag.tag_id == tag_id)
            )
            or 0
        )
