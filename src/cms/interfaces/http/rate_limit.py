from __future__ import annotations

import asyncio
import time
from collections.abc import Callable, Awaitable

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        requests_per_window: int,
        window_seconds: int,
    ) -> None:
        super().__init__(app)
        self.requests_per_window = requests_per_window
        self.window_seconds = window_seconds
        self._lock = asyncio.Lock()
        self._buckets: dict[str, tuple[float, int]] = {}

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable],
    ):
        client_host = request.client.host if request.client else "unknown"
        now = time.monotonic()

        async with self._lock:
            window_start, count = self._buckets.get(client_host, (now, 0))
            if now - window_start >= self.window_seconds:
                window_start = now
                count = 0

            if count >= self.requests_per_window:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Rate limit exceeded"},
                )

            self._buckets[client_host] = (window_start, count + 1)

        return await call_next(request)
