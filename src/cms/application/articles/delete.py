from __future__ import annotations

from cms.domain.articles.repositories import ArticleRepository


async def delete_article(repo: ArticleRepository, slug: str) -> bool:
    return await repo.delete(slug)
