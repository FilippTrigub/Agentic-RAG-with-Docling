# Agentic RAG MVP

An end-to-end retrieval-augmented generation workflow that converts product specification PDFs into structured JSON with Docling, indexes them in a local Chroma vector store using Google Generative AI embeddings, and exposes an agentic chat interface powered by Cerebras for iterative search.

## Key Capabilities
- Parse PDFs into normalized JSON content and metadata via Docling (`ingest.py`).
- Flatten metadata for substring-friendly retrieval and persist vectors in Chroma (`rag_mvp/index_json.py`).
- Expose a LangChain-based agent that must call the retrieval tool, can iterate on queries, and surfaces citations (`rag_mvp/agent.py` + `rag_mvp/tools.py`).
- Support metadata-aware filtering with exact filters, content substring filters (`where`), and post-retrieval substring filters (`contains`).
- Run the entire pipeline (`main.py`) from ingestion through interactive chat.

> Note: No HTML assets are bundled in this repository—the processed corpus in `data/processed/` already contains the Docling JSON output derived from PDFs.

## Prerequisites
- Python 3.13 with [`uv`](https://docs.astral.sh/uv) installed (used for dependency management and execution).
- Google Generative AI credentials (`GOOGLE_API_KEY`) for embeddings.
- Cerebras Cloud credentials (`CEREBRAS_API_KEY`) for chat.
- Optional: Source PDFs placed under `documents/` if you need to regenerate JSON.

## Setup
1. Create and activate a virtual environment (optional but recommended):
   ```bash
   uv venv
   source .venv/bin/activate      # Windows: .venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   uv sync
   ```
3. Configure environment variables:
   - Copy `.env.example` to `.env`.
   - Populate `GOOGLE_API_KEY` and `CEREBRAS_API_KEY`.
   - Verify JSON inputs exist in `data/processed/` (or run the ingestion step below).

## Workflow
### 1. Ingest PDFs → JSON
```bash
uv run python ingest.py --input-dir documents --output-dir data/processed --workers 6
```
- Uses Docling with optional multi-process parallelism (`--workers`).
- Produces one JSON file per PDF containing the document content plus structured metadata.

### 2. Build or Refresh the Vector Index
```bash
uv run python main.py index --processed-dir data/processed --index-dir data/index/chroma --collection rag_mvp
```
- Generates Google embeddings and persists them locally.
- Metadata is flattened into pipe-delimited strings to simplify substring filtering.

### 3. Chat with the Agent
```bash
uv run python main.py chat --index-dir data/index/chroma --collection rag_mvp
```
- The agent always calls the `retrieve_context` tool before responding and will iterate if the first attempt is weak.
- Supports `filters`, `where` (substring in document text), and `contains` (substring in flattened metadata) arguments.
- Responses cite sources with `[n]` markers that map back to `doc_id` / `source`.

### 4. One-Shot Run (index + chat)
```bash
uv run python main.py run
```
- Rebuilds the index from `data/processed/` and immediately launches the chat loop.

## Data Model & Metadata Flattening
- Base JSON structure (see `data/processed/*.json`) includes:
  - `source`: original PDF path.
  - `content`: concatenated textual content.
  - Section fields like `Product features and benefits`, `Areas of application`, and nested maps for detailed specs.
- During indexing each section key is normalized to `snake_case` and flattened:
  - Lists → `"item1 | item2 | ..."`
  - Dicts → `"key: value | key: value"`
  - Scalars → direct string values.
- Resulting metadata keys include `product_features_and_benefits`, `areas_of_application`, `general_product_information`, `electrical_data`, `photometric_data`, `physical_attributes_dimensions`, `operating_conditions`, `product_datasheet`, and `environmental_regulatory_information`.

## Configuration & Environment
- `main.py` exposes `index`, `chat`, and `run` subcommands; default paths align with the repo layout.
- `.env` (loaded via `dotenv`) supplies API keys.
- Vector store persists under `data/index/chroma/`; delete the directory to force a clean rebuild.

## Development Notes
- Codebase targets Python 3.13 and follows PEP 8, using type hints throughout.
- Add new dependencies with `uv add <package>`; both `pyproject.toml` and `uv.lock` are maintained automatically.
- Suggested tests (pytest not yet included):
  - Metadata flattening produces expected pipe-delimited strings.
  - `retrieve_context` respects `contains` filters.
  - Agent invokes the retrieval tool before answering.
- When extending the agent, avoid introducing additional global state; favor passing configuration objects.

## Troubleshooting
- **Missing embeddings**: ensure `GOOGLE_API_KEY` is present and valid.
- **Cerebras authentication errors**: confirm `CEREBRAS_API_KEY` and network access.
- **Empty chat responses**: check that `data/index/chroma/` exists and contains vectors (rerun the `index` command).
- **Docling ingestion warnings**: verify PDFs are readable; tables with more than two columns are skipped by design.

## Repository Structure
- `main.py` – CLI entry point with `index`, `chat`, and `run`.
- `ingest.py` – Docling-powered PDF→JSON ingestion (supports parallel workers).
- `rag_mvp/index_json.py` – vector store builder and metadata flattener.
- `rag_mvp/tools.py` – retrieval utilities and formatting helpers.
- `rag_mvp/agent.py` – Cerebras-backed chat agent with memory and tool-calling.
- `data/processed/` – processed JSON corpus (supplied).
- `data/index/chroma/` – Chroma persistence directory (created on first index build).
