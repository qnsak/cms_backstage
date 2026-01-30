from __future__ import annotations

from cms.domain.articles.repositories import ArticleRepository
from cms.application.articles.dto import ArticleListItemDTO


async def list_published_articles(
    repo: ArticleRepository,
    page: int,
    page_size: int,
) -> list[ArticleListItemDTO]:
    articles = await repo.list_published(page, page_size)
    return [
        ArticleListItemDTO(
            slug=a.slug,
            title=a.title,
            published_at=a.published_at,
            tags=a.tag_slugs,
        )
        for a in articles
    ]
