from __future__ import annotations

import pytest

from cms.domain.articles.services import is_valid_frontend_slug


@pytest.mark.parametrize(
    "slug",
    [
        "hello_fastapi",
        "a",
        "a1_b2",
        "abc123",
        "with_underscores_and_123",
    ],
)
def test_is_valid_frontend_slug_accepts_valid(slug: str) -> None:
    assert is_valid_frontend_slug(slug) is True


@pytest.mark.parametrize(
    "slug",
    [
        "hello-fastapi",
        "Hello",
        "with space",
        "with.dot",
        "with/slash",
        "with:colon",
        "",
    ],
)
def test_is_valid_frontend_slug_rejects_invalid(slug: str) -> None:
    assert is_valid_frontend_slug(slug) is False
