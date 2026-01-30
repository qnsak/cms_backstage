from __future__ import annotations

from cms.domain.articles.services import FRONTEND_SLUG_PATTERN


def test_frontend_slug_allows_only_english_number_underscore() -> None:
    assert FRONTEND_SLUG_PATTERN.match("hello_fastapi")
    assert FRONTEND_SLUG_PATTERN.match("post_2026")

    assert not FRONTEND_SLUG_PATTERN.match("hello-fastapi")
    assert not FRONTEND_SLUG_PATTERN.match("中文")
    assert not FRONTEND_SLUG_PATTERN.match("hello fastapi")
