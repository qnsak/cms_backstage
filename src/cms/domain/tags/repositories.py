from __future__ import annotations

from abc import ABC, abstractmethod

from cms.infrastructure.db.models import Tag


class TagRepository(ABC):

    @abstractmethod
    async def list_all(self) -> list[Tag]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_slug(self, slug: str) -> Tag | None:
        raise NotImplementedError

    @abstractmethod
    async def add(self, tag: Tag) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, tag: Tag) -> None:
        raise NotImplementedError

    @abstractmethod
    async def count_usage(self, tag_id: int) -> int:
        raise NotImplementedError
