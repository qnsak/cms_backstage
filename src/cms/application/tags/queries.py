from __future__ import annotations

from cms.domain.tags.repositories import TagRepository


async def list_tags(repo: TagRepository) -> list[dict[str, str]]:
    result = await repo.list_all()
    return [{"slug": t.slug, "name": t.name} for t in result]
