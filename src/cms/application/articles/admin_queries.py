from __future__ import annotations

from cms.domain.articles.repositories import ArticleRepository
from cms.application.articles.dto import ArticleListItemDTO


async def list_admin_articles(
    repo: ArticleRepository,
    mode: str,
    page: int,
    page_size: int,
) -> list[ArticleListItemDTO]:
    if mode == "drafts":
        articles = await repo.list_drafts(page, page_size)
    elif mode == "published":
        articles = await repo.list_published(page, page_size)
    else:
        articles = await repo.list_all(page, page_size)

    return [
        ArticleListItemDTO(
            slug=a.slug,
            title=a.title,
            published_at=a.published_at,
            tags=a.tag_slugs,
        )
        for a in articles
    ]
