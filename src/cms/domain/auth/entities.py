from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int | None
    email: str
    password_hash: str
    is_active: bool
    is_admin: bool
    created_at: datetime


@dataclass
class RefreshToken:
    id: int | None
    user_id: int
    token_hash: str
    expires_at: datetime
    revoked_at: datetime | None
    created_at: datetime
    last_used_at: datetime | None
