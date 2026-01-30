from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Article:
    id: int | None
    slug: str
    title: str
    body_md: str
    published_at: str | None
    tag_slugs: list[str] = field(default_factory=list)
