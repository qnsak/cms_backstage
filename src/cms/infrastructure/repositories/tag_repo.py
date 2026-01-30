from __future__ import annotations

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from cms.domain.tags.entities import Tag as DomainTag
from cms.domain.tags.repositories import TagRepository
from cms.infrastructure.db.models import Tag, ArticleTag


class SQLAlchemyTagRepository(TagRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def _to_domain(self, model: Tag) -> DomainTag:
        return DomainTag(id=model.id, slug=model.slug, name=model.name)

    async def _commit(self) -> None:
        await self.session.commit()

    async def _commit_and_refresh(self, model: Tag) -> None:
        await self.session.commit()
        await self.session.refresh(model)

    async def list_all(self) -> list[DomainTag]:
        result = await self.session.scalars(select(Tag))
        return [self._to_domain(tag) for tag in result]

    async def get_by_slug(self, slug: str) -> DomainTag | None:
        tag = await self.session.scalar(select(Tag).where(Tag.slug == slug))
        if tag is None:
            return None
        return self._to_domain(tag)

    async def add(self, tag: DomainTag) -> None:
        model = Tag(slug=tag.slug, name=tag.name)
        self.session.add(model)
        await self._commit_and_refresh(model)
        tag.id = model.id

    async def delete(self, tag: DomainTag) -> None:
        model = None
        if tag.id is not None:
            model = await self.session.get(Tag, tag.id)
        if model is None:
            model = await self.session.scalar(select(Tag).where(Tag.slug == tag.slug))
        if model is None:
            return

        await self.session.delete(model)
        await self._commit()

    async def count_usage(self, tag_id: int) -> int:
        return (
            await self.session.scalar(
                select(func.count()).select_from(ArticleTag).where(ArticleTag.tag_id == tag_id)
            )
            or 0
        )
