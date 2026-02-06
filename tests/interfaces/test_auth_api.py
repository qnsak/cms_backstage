from __future__ import annotations

import pytest
from httpx import AsyncClient, Response


@pytest.mark.asyncio
async def test_login_sets_refresh_cookie(
    client: AsyncClient,
    admin_user,
    admin_credentials,
) -> None:
    email, password = admin_credentials
    res: Response = await client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    assert res.status_code == 200
    payload = res.json()
    assert "access_token" in payload
    assert res.cookies.get("refresh_token") is not None
    assert "HttpOnly" in res.headers.get("set-cookie", "")


@pytest.mark.asyncio
async def test_refresh_rotates_token(
    client: AsyncClient,
    admin_user,
    admin_credentials,
) -> None:
    email, password = admin_credentials
    res: Response = await client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    old_refresh = res.cookies.get("refresh_token")
    assert old_refresh is not None

    res = await client.post("/api/auth/refresh")
    assert res.status_code == 200
    payload = res.json()
    assert "access_token" in payload
    new_refresh = res.cookies.get("refresh_token")
    assert new_refresh is not None
    assert new_refresh != old_refresh


@pytest.mark.asyncio
async def test_logout_revokes_refresh(
    client: AsyncClient,
    admin_user,
    admin_credentials,
) -> None:
    email, password = admin_credentials
    res: Response = await client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    refresh = res.cookies.get("refresh_token")
    assert refresh is not None

    res = await client.post("/api/auth/logout")
    assert res.status_code == 200

    client.cookies.set("refresh_token", refresh, path="/api/auth")
    res = await client.post("/api/auth/refresh")
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_admin_requires_auth(client: AsyncClient) -> None:
    res = await client.get("/api/admin/tags")
    assert res.status_code == 401
