from __future__ import annotations

from cms.domain.tags.entities import Tag
from cms.domain.tags.repositories import TagRepository


async def create_tag(repo: TagRepository, slug: str, name: str) -> dict[str, str]:
    existing: Tag | None = await repo.get_by_slug(slug)
    if existing is not None:
        raise ValueError("Tag already exists")

    tag = Tag(id=None, slug=slug, name=name)
    await repo.add(tag)
    return {"slug": tag.slug, "name": tag.name}


async def delete_tag(repo: TagRepository, slug: str) -> bool:
    tag: Tag | None = await repo.get_by_slug(slug)
    if tag is None:
        return False

    usage_count: int = await repo.count_usage(tag.id)

    if usage_count > 0:
        raise ValueError("Tag is still in use and cannot be deleted")

    await repo.delete(tag)
    return True
