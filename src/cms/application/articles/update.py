from __future__ import annotations

from cms.domain.articles.entities import Article
from cms.domain.articles.repositories import ArticleRepository
from cms.domain.tags.entities import Tag
from cms.domain.tags.repositories import TagRepository


async def update_article(
    article_repo: ArticleRepository,
    tag_repo: TagRepository,
    slug: str,
    title: str,
    body_md: str,
    tag_slugs: list[str],
) -> Article | None:
    tags: list[Tag] = []
    for t_slug in tag_slugs:
        tag: Tag | None = await tag_repo.get_by_slug(t_slug)
        if tag is None:
            tag = Tag(slug=t_slug, name=t_slug)
            await tag_repo.add(tag)
        tags.append(tag)

    return await article_repo.update(
        slug=slug,
        title=title,
        body_md=body_md,
        tags=tags,
    )
