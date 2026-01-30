from __future__ import annotations

from cms.domain.articles.repositories import ArticleRepository
from cms.application.articles.dto import ArticleDetailDTO


async def admin_get_article_by_slug(
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
        tags=article.tag_slugs,
    )
