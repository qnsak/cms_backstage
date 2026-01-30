from __future__ import annotations

from abc import ABC, abstractmethod
from cms.infrastructure.db.models import Article


class ArticleRepository(ABC):

    @abstractmethod
    async def list_published(self, page: int, page_size: int) -> list[Article]:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self, page: int, page_size: int) -> list[Article]:
        raise NotImplementedError

    @abstractmethod
    async def list_drafts(self, page: int, page_size: int) -> list[Article]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_slug(self, slug: str) -> Article | None:
        raise NotImplementedError
