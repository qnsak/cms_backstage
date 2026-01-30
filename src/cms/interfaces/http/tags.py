from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from cms.interfaces.http.articles import get_session
from cms.infrastructure.repositories.tag_repo import SQLAlchemyTagRepository
from cms.application.tags.list_all import list_tags
from cms.application.tags.create import create_tag
from cms.application.tags.delete import delete_tag

router = APIRouter()


class RequestModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CreateTagRequest(RequestModel):
    slug: str
    name: str


@router.get("/api/admin/tags")
async def admin_list_tags_api(
    session: AsyncSession = Depends(get_session),
) -> list[dict[str, str]]:
    repo = SQLAlchemyTagRepository(session)
    return await list_tags(repo)


@router.post("/api/admin/tags")
async def admin_create_tag_api(
    req: CreateTagRequest,
    session: AsyncSession = Depends(get_session),
) -> dict[str, str]:
    repo = SQLAlchemyTagRepository(session)
    try:
        return await create_tag(repo, req.slug, req.name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/api/admin/tags/{slug}")
async def admin_delete_tag_api(
    slug: str,
    session: AsyncSession = Depends(get_session),
) -> dict[str, str]:
    repo = SQLAlchemyTagRepository(session)
    try:
        ok = await delete_tag(repo, slug)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not ok:
        raise HTTPException(status_code=404, detail="Tag not found")

    return {"message": "deleted", "slug": slug}
