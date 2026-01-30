from __future__ import annotations

from fastapi import FastAPI

from cms.interfaces.http.articles import router as article_router
from cms.interfaces.http.tags import router as tag_router

app = FastAPI(title="Async DDD CMS")

app.include_router(article_router)
app.include_router(tag_router)
