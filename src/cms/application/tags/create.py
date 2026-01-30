from __future__ import annotations

from cms.domain.tags.entities import Tag
from cms.domain.tags.repositories import TagRepository


async def create_tag(repo: TagRepository, slug: str, name: str) -> dict[str, str]:
    existing: Tag | None = await repo.get_by_slug(slug)
    if existing is not None:
        raise ValueError("Tag already exists")

    tag = Tag(slug=slug, name=name)
    await repo.add(tag)
    return {"slug": tag.slug, "name": tag.name}
