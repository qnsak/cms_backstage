from __future__ import annotations

from cms.domain.articles.repositories import ArticleRepository
from cms.application.articles.dto import ArticleListItemDTO, ArticleDetailDTO


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
            tags=[t.slug for t in a.tags],
        )
        for a in articles
    ]


async def get_article_by_slug(
    repo: ArticleRepository,
    slug: str,
) -> ArticleDetailDTO | None:
    article = await repo.get_by_slug(slug)
    if article is None:
        return None

    return ArticleDetailDTO(
        slug=article.slug,
        title=article.title,
        body_md=article.body_md,
        published_at=article.published_at,
        tags=[t.slug for t in article.tags],
    )
