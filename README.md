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

## License
MIT
