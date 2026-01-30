from __future__ import annotations

import asyncio
import json
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from cms.infrastructure.db.session import AsyncSessionLocal, engine
from cms.infrastructure.db.models import Base
from cms.infrastructure.repositories.article_repo import SQLAlchemyArticleRepository
from cms.infrastructure.repositories.tag_repo import SQLAlchemyTagRepository
from cms.application.articles.commands import create_article
from cms.application.articles.commands import publish_article


async def main() -> None:
    # For demo convenience only (migrations remain the canonical way)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 載入 JSON 資料
    seed_file = Path(__file__).parent / "seed_data.json"
    with open(seed_file, "r", encoding="utf-8") as f:
        articles_data = json.load(f)

    async with AsyncSessionLocal() as session:  # type: AsyncSession
        article_repo = SQLAlchemyArticleRepository(session)
        tag_repo = SQLAlchemyTagRepository(session)
        for article_data in articles_data:
            article = await create_article(
                article_repo=article_repo,
                tag_repo=tag_repo,
                frontend_slug=article_data["slug"],
                title=article_data["title"],
                body_md=article_data["body_md"],
                tag_slugs=article_data["tag_slugs"],
            )
            await publish_article(article_repo=article_repo, slug=article.slug)
            print(f"✓ Created: {article.title}")

    print("Seed completed.")


if __name__ == "__main__":
    asyncio.run(main())
