# Agentic RAG MVP (Python)

A minimal retrieval-augmented generation (RAG) prototype that demonstrates document ingestion, metadata extraction, vector indexing with Chroma, and a small chat agent that performs RAG-enabled question answering.

Key ideas
- Parse documents (PDFs) to structured JSON using Docling (see main.py / ingest.py).
- Convert document content and metadata into embeddings and persist a Chroma index (rag_mvp/index_json.py).
- Provide a chat agent that retrieves relevant chunks and composes answers with brief citations (rag_mvp/agent.py).

Important: This repository targets Linux / Python environments. The examples below assume a POSIX shell.

Prerequisites
- Python 3.13
- The repository uses `uv` for environment and dependency management (see pyproject.toml).
- API keys: set GOOGLE_API_KEY and optionally CEREBRAS_API_KEY in an .env file.

Quick setup
1. Create and activate a virtual environment (POSIX):

    uv venv
    source .venv/bin/activate

2. Install dependencies:

    uv sync

3. Configure environment variables:

    cp .env.example .env
    # Edit .env and add API keys and other required values

4. Prepare processed data:

    - Processed JSON files should be placed in `data/processed/` (these are produced by the ingestion step). If you need to reprocess, place source PDFs in `documents/` and run the ingestion script:

      python main.py   # or `python ingest.py` depending on your workflow

Data format (processed JSON)
Each processed file in data/processed/ is a JSON object with structured metadata and a `content` field (plain text). The indexer will also add a `doc_id` derived from the filename.

Example (simplified):

```json
{
  "doc_id": "ZMP_1004795",
  "source": "documents/ZMP_1004795.pdf",
  "content": "Long text content...",
  "product_features_and_benefits": ["Robust construction", "Consistent color"],
  "photometric_data": {"Nominal luminous flux": "13500 lm"}
}
```

Building the Chroma index

Run the indexer to build persistent Chroma data under data/index/chroma:

    uv run python -m rag_mvp.index_json --processed-dir data/processed --index-dir data/index/chroma

Running the chat agent

Start the simple RAG chat agent (it reads the index from the directory above):

    uv run python -m rag_mvp.agent chat --index-dir data/index/chroma

Then type questions; the agent will retrieve top-k chunks and answer with brief bracketed citations.

Troubleshooting
- No embeddings / errors contacting Google: verify GOOGLE_API_KEY is set and network is available.
- No results: make sure data/processed contains JSON files with non-empty `content` fields.
- If the `uv` commands fail: ensure `uv` (a project-specific tool) is installed or use your preferred venv and pip flow (python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt).

Scaling & next steps
- Move vector store to a hosted vector database (Qdrant, Milvus) for production-scale datasets.
- Parse numerical metadata into typed fields for numeric filters and range queries.
- Refactor global-state usage for proper API concurrency (make components async where applicable).

Project layout
- main.py / ingest.py — ingestion from PDFs to JSON
- rag_mvp/index_json.py — build Chroma index from processed JSON
- rag_mvp/tools.py — retrieval helpers and context formatting
- rag_mvp/agent.py — minimal chat agent with memory
- data/processed/ — processed JSON inputs
- data/index/chroma/ — Chroma persistence

License & notes
This is a small experimental project. Review code and configuration before deploying; avoid committing API keys or sensitive data.
