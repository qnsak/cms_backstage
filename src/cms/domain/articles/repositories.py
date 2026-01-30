from __future__ import annotations

from abc import ABC, abstractmethod

from cms.domain.articles.entities import Article
from cms.domain.tags.entities import Tag


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

    @abstractmethod
    async def get_latest_slug_by_prefix(self, prefix: str) -> str | None:
        raise NotImplementedError

    @abstractmethod
    async def create(
        self,
        slug: str,
        title: str,
        body_md: str,
        tags: list[Tag],
    ) -> Article:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        slug: str,
        title: str,
        body_md: str,
        tags: list[Tag],
    ) -> Article | None:
        raise NotImplementedError

    @abstractmethod
    async def publish(self, slug: str, published_at: str) -> Article | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, slug: str) -> bool:
        raise NotImplementedError
