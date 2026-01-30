from __future__ import annotations

from typing import AsyncGenerator, Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from cms.infrastructure.db.session import AsyncSessionLocal
from cms.infrastructure.repositories.article_repo import SQLAlchemyArticleRepository

from cms.application.articles.queries import list_published_articles, get_article_by_slug
from cms.application.articles.admin_queries import list_admin_articles
from cms.application.articles.admin_detail import admin_get_article_by_slug
from cms.application.articles.commands import create_article, update_article, publish_article
from cms.application.articles.delete import delete_article

router = APIRouter()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


class CreateArticleRequest(BaseModel):
    slug: str
    title: str
    body_md: str
    tags: list[str] = []


class UpdateArticleRequest(BaseModel):
    title: str
    body_md: str
    tags: list[str] = []


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/api/contents")
async def list_contents(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, le=50),
    session: AsyncSession = Depends(get_session),
) -> list[dict]:
    repo = SQLAlchemyArticleRepository(session)
    items = await list_published_articles(repo, page, page_size)
    return [i.model_dump() for i in items]


@router.get("/api/contents/{slug}")
async def get_content(
    slug: str,
    session: AsyncSession = Depends(get_session),
) -> dict:
    repo = SQLAlchemyArticleRepository(session)
    article = await get_article_by_slug(repo, slug)
    if article is None:
        raise HTTPException(status_code=404, detail="Not found")
    return article.model_dump()


@router.post("/api/articles")
async def create_article_api(
    req: CreateArticleRequest,
    session: AsyncSession = Depends(get_session),
) -> dict:
    article = await create_article(
        session=session,
        frontend_slug=req.slug,
        title=req.title,
        body_md=req.body_md,
        tag_slugs=req.tags,
    )
    return {
        "slug": article.slug,
        "title": article.title,
        "published_at": article.published_at,
        "tags": [t.slug for t in article.tags],
    }


@router.put("/api/articles/{slug}")
async def update_article_api(
    slug: str,
    req: UpdateArticleRequest,
    session: AsyncSession = Depends(get_session),
) -> dict:
    article = await update_article(
        session=session,
        slug=slug,
        title=req.title,
        body_md=req.body_md,
        tag_slugs=req.tags,
    )
    if article is None:
        raise HTTPException(status_code=404, detail="Not found")

    return {
        "slug": article.slug,
        "title": article.title,
        "published_at": article.published_at,
        "tags": [t.slug for t in article.tags],
    }


@router.post("/api/articles/{slug}/publish")
async def publish_article_api(
    slug: str,
    session: AsyncSession = Depends(get_session),
) -> dict:
    article = await publish_article(session=session, slug=slug)
    if article is None:
        raise HTTPException(status_code=404, detail="Not found")
    return {"slug": article.slug, "published_at": article.published_at, "message": "published"}


@router.delete("/api/articles/{slug}")
async def delete_article_api(
    slug: str,
    session: AsyncSession = Depends(get_session),
) -> dict[str, str]:
    ok = await delete_article(session, slug)
    if not ok:
        raise HTTPException(status_code=404, detail="Not found")
    return {"message": "deleted", "slug": slug}


AdminMode = Literal["all", "drafts", "published"]


@router.get("/api/admin/articles")
async def admin_list_articles_api(
    mode: AdminMode = Query("all"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, le=50),
    session: AsyncSession = Depends(get_session),
) -> list[dict]:
    repo = SQLAlchemyArticleRepository(session)
    items = await list_admin_articles(repo=repo, mode=mode, page=page, page_size=page_size)
    return [i.model_dump() for i in items]


@router.get("/api/admin/articles/{slug}")
async def admin_get_article_api(
    slug: str,
    session: AsyncSession = Depends(get_session),
) -> dict:
    repo = SQLAlchemyArticleRepository(session)
    article = await admin_get_article_by_slug(repo, slug)
    if article is None:
        raise HTTPException(status_code=404, detail="Not found")
    return article.model_dump()
