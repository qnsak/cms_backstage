from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from cms.interfaces.http.articles import router as article_router
from cms.interfaces.http.tags import router as tag_router
from cms.interfaces.http.rate_limit import RateLimiterMiddleware

app = FastAPI(title="Async DDD CMS")

if os.getenv("RATE_LIMIT_ENABLED", "false").lower() == "true":
    requests_per_window = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    window_seconds = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))
    app.add_middleware(
        RateLimiterMiddleware,
        requests_per_window=requests_per_window,
        window_seconds=window_seconds,
    )

app.include_router(article_router)
app.include_router(tag_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
