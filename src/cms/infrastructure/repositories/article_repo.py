from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from cms.domain.articles.entities import Article as DomainArticle
from cms.domain.tags.entities import Tag as DomainTag
from cms.infrastructure.db.models import Article, ArticleTag, Tag
from cms.domain.articles.repositories import ArticleRepository


class SQLAlchemyArticleRepository(ArticleRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def _to_domain(self, model: Article) -> DomainArticle:
        return DomainArticle(
            id=model.id,
            slug=model.slug,
            title=model.title,
            body_md=model.body_md,
            published_at=model.published_at,
            tag_slugs=[t.slug for t in model.tags],
        )

    async def _load_tags(self, tags: list[DomainTag]) -> list[Tag]:
        slugs = [tag.slug for tag in tags]
        if not slugs:
            return []

        result = await self.session.scalars(select(Tag).where(Tag.slug.in_(slugs)))
        existing = {tag.slug: tag for tag in result}

        for slug in slugs:
            if slug not in existing:
                tag = Tag(slug=slug, name=slug)
                self.session.add(tag)
                existing[slug] = tag

        return [existing[slug] for slug in slugs]

    async def list_published(self, page: int, page_size: int) -> list[DomainArticle]:
        offset = (page - 1) * page_size
        stmt = (
            select(Article)
            .options(selectinload(Article.tags))
            .where(Article.published_at.is_not(None))
            .offset(offset)
            .limit(page_size)
        )
        result = await self.session.scalars(stmt)
        return [self._to_domain(article) for article in result]

    async def list_all(self, page: int, page_size: int) -> list[DomainArticle]:
        offset = (page - 1) * page_size
        stmt = (
            select(Article)
            .options(selectinload(Article.tags))
            .offset(offset)
            .limit(page_size)
        )
        result = await self.session.scalars(stmt)
        return [self._to_domain(article) for article in result]

    async def list_drafts(self, page: int, page_size: int) -> list[DomainArticle]:
        offset = (page - 1) * page_size
        stmt = (
            select(Article)
            .options(selectinload(Article.tags))
            .where(Article.published_at.is_(None))
            .offset(offset)
            .limit(page_size)
        )
        result = await self.session.scalars(stmt)
        return [self._to_domain(article) for article in result]

    async def get_by_slug(self, slug: str) -> DomainArticle | None:
        stmt = (
            select(Article)
            .options(selectinload(Article.tags))
            .where(Article.slug == slug)
        )
        article = await self.session.scalar(stmt)
        if article is None:
            return None
        return self._to_domain(article)

    async def get_latest_slug_by_prefix(self, prefix: str) -> str | None:
        stmt = (
            select(Article.slug)
            .where(Article.slug.like(f"{prefix}%"))
            .order_by(Article.slug.desc())
            .limit(1)
        )
        return await self.session.scalar(stmt)

    async def create(
        self,
        slug: str,
        title: str,
        body_md: str,
        tags: list[DomainTag],
    ) -> DomainArticle:
        tag_models = await self._load_tags(tags)
        article = Article(
            slug=slug,
            title=title,
            body_md=body_md,
            published_at=None,
            tags=tag_models,
        )
        self.session.add(article)
        await self.session.commit()
        await self.session.refresh(article)
        return self._to_domain(article)

    async def update(
        self,
        slug: str,
        title: str,
        body_md: str,
        tags: list[DomainTag],
    ) -> DomainArticle | None:
        stmt = (
            select(Article)
            .options(selectinload(Article.tags))
            .where(Article.slug == slug)
        )
        article = await self.session.scalar(stmt)
        if article is None:
            return None

        article.title = title
        article.body_md = body_md
        article.tags = await self._load_tags(tags)
        await self.session.commit()
        await self.session.refresh(article)
        return self._to_domain(article)

    async def publish(self, slug: str, published_at: str) -> DomainArticle | None:
        stmt = (
            select(Article)
            .options(selectinload(Article.tags))
            .where(Article.slug == slug)
        )
        article = await self.session.scalar(stmt)
        if article is None:
            return None

        if article.published_at is None:
            article.published_at = published_at

        await self.session.commit()
        await self.session.refresh(article)
        return self._to_domain(article)

    async def delete(self, slug: str) -> bool:
        article = await self.session.scalar(select(Article).where(Article.slug == slug))
        if article is None:
            return False

        await self.session.execute(
            ArticleTag.__table__.delete().where(ArticleTag.article_id == article.id)
        )
        await self.session.delete(article)
        await self.session.commit()
        return True
