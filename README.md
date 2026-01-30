# Async DDD Headless Markdown CMS

📘 Language:
- English (README.md)
- 台灣繁體中文 (README.zh-TW.md)

A minimal, professional **Headless CMS starter kit** built with:

- FastAPI (Async)
- SQLAlchemy Async ORM
- SQLite (dev) + PostgreSQL-ready design
- DDD architecture (Domain / Application / Infrastructure / Interfaces)
- Alembic migrations
- Draft → Publish lifecycle
- Tag management (safe delete: cannot remove tags in use)
- Fully typed Python (3.12)

## Quick Start (Docker)

```bash
make up
make migrate
make seed
```

Open API docs:
- http://localhost:8000/docs

## Commands

```bash
make
```

## Testing Plan

This repo uses a layered test strategy aligned with DDD boundaries:

- Domain: fast unit tests, including DB-free checks (pure logic like slug validation).
- Interfaces: API flow tests (fixture-driven) plus contract tests for response shape.
- Infrastructure: integration-style tests for repo/db behavior when needed.

Common commands:

```bash
make test
make test-report
make test-report-local
```

Test reports are written to `reports/`:
- `reports/junit.xml`
- `reports/pytest.html`
- `reports/coverage.xml`
- `reports/coverage-html/`

See `docs/TESTING.md` for a detailed testing guide.

## License
MIT
