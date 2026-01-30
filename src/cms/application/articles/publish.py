from __future__ import annotations

from datetime import datetime, timezone

from cms.domain.articles.entities import Article
from cms.domain.articles.repositories import ArticleRepository


async def publish_article(
    article_repo: ArticleRepository,
    slug: str,
) -> Article | None:
    return await article_repo.publish(
        slug=slug,
        published_at=datetime.now(timezone.utc).isoformat(),
    )
