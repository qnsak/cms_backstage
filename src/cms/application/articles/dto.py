from __future__ import annotations

from pydantic import BaseModel


class ArticleListItemDTO(BaseModel):
    slug: str
    title: str
    published_at: str | None
    tags: list[str]


class ArticleDetailDTO(BaseModel):
    slug: str
    title: str
    body_md: str
    published_at: str | None
    tags: list[str]
