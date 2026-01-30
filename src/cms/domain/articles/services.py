from __future__ import annotations

import re
from datetime import datetime, timezone


from cms.domain.articles.repositories import ArticleRepository


FRONTEND_SLUG_PATTERN: re.Pattern[str] = re.compile(r"^[a-z0-9_]+$")


def is_valid_frontend_slug(frontend_slug: str) -> bool:
    return bool(FRONTEND_SLUG_PATTERN.fullmatch(frontend_slug))


async def build_article_slug(repo: ArticleRepository, frontend_slug: str) -> str:
    """
    frontend_slug: hello_fastapi
    result:       20260127_0001_hello_fastapi
    """
    if not is_valid_frontend_slug(frontend_slug):
        raise ValueError("slug must contain only a-z, 0-9, underscore")

    today: str = datetime.now(timezone.utc).strftime("%Y%m%d")
    prefix: str = f"{today}_"

    last_slug = await repo.get_latest_slug_by_prefix(prefix)

    if last_slug is None:
        seq: int = 1
    else:
        last_seq: int = int(last_slug.split("_")[1])
        seq = last_seq + 1

    return f"{today}_{seq:04d}_{frontend_slug}"
