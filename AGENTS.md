# Repository Guidelines

## Project Structure & Module Organization
- `main.py` — unified CLI: `index`, `chat`, `run`.
- `ingest.py` — Docling PDF→JSON ingestion (parallel via `--workers`).
- `rag_mvp/` — MVP package:
  - `index_json.py` — build Chroma index from processed JSON.
  - `tools.py` — retrieval helper with metadata substring filtering.
  - `agent.py` — agentic RAG (LangChain tool-calling) with sources.
- `pyproject.toml` — project metadata; managed with `uv`.
- `README.md` — usage and quickstart.
- `data/processed/` — parsed JSON inputs; `data/index/chroma/` — vector store.

## Build, Test, and Development Commands
- Setup env: `uv sync` — creates `.venv` and installs deps.
- Ingest PDFs→JSON: `uv run python ingest.py --input-dir documents --output-dir data/processed --workers 6`.
- Build index: `uv run python main.py index --processed-dir data/processed --index-dir data/index/chroma`.
- Chat agent: `uv run python main.py chat --index-dir data/index/chroma`.
- One-shot run: `uv run python main.py run` (index then chat).
- Add a dependency: `uv add <package>` — updates `pyproject.toml` and `uv.lock`.

## Coding Style & Naming Conventions
- Python 3.13, 4-space indentation, PEP 8 style; prefer type hints.
- Names: modules/files `snake_case.py`, functions/vars `snake_case`, classes `PascalCase`.
- Keep functions small; avoid unnecessary globals; prefer explicit over implicit.
- Docstrings: use concise one-liners for simple functions; expand when behavior is non‑trivial.

## Testing Guidelines
- Framework: `pytest` (add with `uv add pytest`).
- Suggested tests: indexer flattens metadata correctly; retrieval `contains` filtering; agent invokes tool at least once.
- Layout: `tests/test_<module>.py`; focus on targeted unit tests.

## Commit & Pull Request Guidelines
- Commits: keep them small and scoped; use Conventional Commits where possible, e.g. `feat: add retriever`, `fix: handle empty query`.
- PRs: include a clear description, rationale, and testing notes; link issues; attach logs or screenshots for user-facing changes.
- Keep PRs focused; update `README.md` when behavior or usage changes.

## Security & Configuration Tips
- Env vars: `GOOGLE_API_KEY` (embeddings), `CEREBRAS_API_KEY` (chat model). Copy `.env.example`.
- Do not commit secrets; prefer environment variables.
- Pin dependencies via `uv.lock`; use `uv up` cautiously and test before merging.

## RAG Implementation Notes
- Embeddings: Google Generative AI (`models/embedding-001`) via `langchain-google-genai`.
- Vector store: Chroma persisted at `data/index/chroma`.
- Agent: LangChain tool-calling (Cerebras chat). The tool `retrieve_context` accepts `query`, `k`, optional exact `filters`, and substring `contains` filters.
- Metadata schema (flattened strings for simple substring search):
  - `product_features_and_benefits`: joined list string (`"item1 | item2 | ..."`).
  - `areas_of_application`: joined list string.
  - Section maps (e.g., `general_product_information`, `electrical_data`, `photometric_data`, `physical_attributes_dimensions`, `operating_conditions`, `product_datasheet`, `environmental_regulatory_information`) → single string of `"key: value"` pairs joined by `|`.
- Ingestion acceleration: `ingest.py` supports `--workers` with process-based parallelism and per-process Docling converter reuse.
