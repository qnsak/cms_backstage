from __future__ import annotations

import re
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


FRONTEND_SLUG_PATTERN: re.Pattern[str] = re.compile(r"^[a-z0-9_]+$")


async def build_article_slug(session: AsyncSession, frontend_slug: str) -> str:
    """
    frontend_slug: hello_fastapi
    result:       20260127_0001_hello_fastapi
    """
    if not FRONTEND_SLUG_PATTERN.match(frontend_slug):
        raise ValueError("slug must contain only a-z, 0-9, underscore")

    today: str = datetime.utcnow().strftime("%Y%m%d")
    prefix: str = f"{today}_"

    sql = text(
        """
        SELECT slug
        FROM articles
        WHERE slug LIKE :p
        ORDER BY slug DESC
        LIMIT 1
        """
    )

    result = await session.execute(sql, {"p": f"{prefix}%"})
    row: tuple[str] | None = result.fetchone()

    if row is None:
        seq: int = 1
    else:
        last_slug: str = row[0]
        last_seq: int = int(last_slug.split("_")[1])
        seq = last_seq + 1

    return f"{today}_{seq:04d}_{frontend_slug}"
