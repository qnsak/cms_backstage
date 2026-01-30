## Testing Guide

This project uses a DDD-aligned test layout. Tests are grouped by layer and
use pytest with asyncio support.

## Suggested Reading Order

1) Start with layer overview: see `Folder Structure` below.
2) Read a simple unit test: `tests/domain/test_slug_validation.py`.
3) Read API contract tests: `tests/interfaces/test_api_contracts.py`.
4) Read API flow tests: `tests/interfaces/test_articles_api.py`.
5) Infrastructure tests (if present) last: `tests/infrastructure/`.

## Testing Lifecycle

1) Requirement or bug appears
   - Translate into testable behavior (inputs, outputs, state).
   - Decide the layer: Domain / Interfaces / Infrastructure.

2) Design before writing tests
   - Domain: define rules and edge cases.
   - Interfaces: define response shape (contract).
   - Infrastructure: define data integrity/transaction rules.

3) Write tests
   - Domain: pure logic, no DB.
   - Interfaces: contract tests first, then flow tests.
   - Infrastructure: repo/db behavior only when needed.

4) Run a minimal set locally
   - Example: `pytest -q tests/domain/test_slug_validation.py`

5) Run full suite after changes
   - `make test`
   - `make test-report` or `make test-report-local`

6) Review reports and coverage
   - `reports/pytest.html` for failures/timing.
   - `reports/coverage-html/` for gaps.

7) Regression and maintenance
   - Update contract and flow tests with requirements.
   - Add regression tests after bug fixes.
   - Refactor safely with tests as guardrails.

## Folder Structure

- `tests/domain/` — Fast unit tests for pure domain logic (no DB).
- `tests/infrastructure/` — Integration tests for repositories/database.
- `tests/interfaces/` — API flow tests and contract/response-shape checks.

## Naming Conventions

- Test files: `test_*.py`
- Test functions: `test_*`
- Keep tests near the layer they validate.

## Running Tests

```bash
make test
make test-report
make test-report-local
```

Reports are written to `reports/` when using report targets.

## Dependency Rule Check

Enforce Clean Architecture import rules:

```bash
make check-deps
```

## Adding a New Test Case (Example)

1) Pick the right layer:
   - Pure logic → `tests/domain/`
   - Repo/DB behavior → `tests/infrastructure/`
   - API behavior → `tests/interfaces/`

2) Create a new file or add to an existing one:

Example: add a domain test for slug validation.

```python
from cms.domain.articles.services import is_valid_frontend_slug


def test_is_valid_frontend_slug_rejects_spaces() -> None:
    assert is_valid_frontend_slug("has space") is False
```

3) Run tests:

```bash
pytest -q tests/domain/test_slug_validation.py
```

## API Test Tips

- Use fixtures from `tests/interfaces/conftest.py` for API calls.
- Contract tests should validate response shape and types.
