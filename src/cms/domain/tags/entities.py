from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Tag:
    slug: str
    name: str
    id: int | None = None
