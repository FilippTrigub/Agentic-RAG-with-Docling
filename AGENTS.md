# Repository Guidelines

## Project Structure & Module Organization
- `main.py` — CLI/entry point for running the project.
- `pyproject.toml` — project metadata; managed with `uv`.
- `uv.lock` — locked dependency state.
- `README.md` — high-level notes (expand as features land).
- `tests/` — add pytest tests here (`tests/test_*.py`).

## Build, Test, and Development Commands
- Setup env: `uv sync` — creates `.venv` and installs deps.
- Run app: `uv run python main.py` — executes the entry point.
- Add a dependency: `uv add <package>` — updates `pyproject.toml` and `uv.lock`.
- Run tests: `uv run pytest -q` — runs test suite.
- Optional without uv: activate an existing `.venv` and run `python main.py`.

## Coding Style & Naming Conventions
- Python 3.13, 4-space indentation, PEP 8 style; prefer type hints.
- Names: modules/files `snake_case.py`, functions/vars `snake_case`, classes `PascalCase`.
- Keep functions small; avoid unnecessary globals; prefer explicit over implicit.
- Docstrings: use concise one-liners for simple functions; expand when behavior is non‑trivial.

## Testing Guidelines
- Framework: `pytest` (add to the project with `uv add pytest`).
- Layout: `tests/test_<module>.py`; one unit under test per test function where feasible.
- Use fixtures for setup; avoid network/IO in unit tests; mock external calls.
- Aim for meaningful coverage on new/changed code; add regression tests for bugs.

## Commit & Pull Request Guidelines
- Commits: keep them small and scoped; use Conventional Commits where possible, e.g. `feat: add retriever`, `fix: handle empty query`.
- PRs: include a clear description, rationale, and testing notes; link issues; attach logs or screenshots for user-facing changes.
- Keep PRs focused; update `README.md` when behavior or usage changes.

## Security & Configuration Tips
- Do not commit secrets; prefer environment variables. Provide `.env.example` when adding new config.
- Pin dependencies via `uv.lock`; use `uv up` cautiously and test before merging.
