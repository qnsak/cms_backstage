# Repository Guidelines

## Project Structure & Module Organization
- `src/cms/` is the application package, organized by DDD layers: `domain/`, `application/`, `infrastructure/`, `interfaces/`, plus `main.py` for the FastAPI entrypoint.
- `tests/` mirrors the DDD boundaries with `domain/`, `infrastructure/`, and `interfaces/` test modules.
- `migrations/` holds Alembic migration scripts; `alembic.ini` configures migrations.
- `docker-compose.yml` and `Dockerfile` define the dev runtime; `app.db` is the local SQLite database.
- `src/cms/scripts/` includes operational scripts (for example, seeding demo data).

## Build, Test, and Development Commands
- `make up` builds and starts the Docker containers.
- `make down` stops containers; `make logs` tails backend logs.
- `make shell` opens a bash shell inside the backend container.
- `make migrate` runs Alembic migrations; `make revision m="message"` creates a new migration.
- `make seed` loads demo data into SQLite; `make test` runs `pytest -q` in the container.
- `make fmt` and `make lint` run Ruff formatting and linting.

## Coding Style & Naming Conventions
- Python 3.12 with full typing; keep boundaries between DDD layers.
- Formatting and linting are handled by Ruff (`line-length = 88`, double quotes).
- Use 4-space indentation for Python. Prefer descriptive, domain-oriented names (for example, `Article`, `Tag`, `PublishCommand`).

## Testing Guidelines
- Pytest with `pytest-asyncio` (`asyncio_mode = auto`); tests live under `tests/`.
- Name test files `test_*.py` and keep tests in the matching layer directory (for example, `tests/domain/`).
- Run tests via `make test`; add/extend tests for behavior changes.

## Commit & Pull Request Guidelines
- Git history is not available in this repository snapshot, so no commit-message convention is enforced here.
- Keep PRs focused, explain the change and motivation, and link related issues when applicable.
- Include tests for behavior changes and note any migration steps (for example, `make migrate`).

## Security & Configuration Tips
- Report security issues via the process described in `SECURITY.md`.
- Default dev DB is SQLite (`app.db`); the architecture is PostgreSQL-ready, so keep database-specific logic isolated in `infrastructure/`.
