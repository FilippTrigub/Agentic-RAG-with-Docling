# RAG MVP: Docling + LangChain + Chroma

Minimal retrieval-augmented generation (RAG) app. Documents are parsed to JSON (handled separately), embedded with Google Generative AI embeddings, stored locally in Chroma, and queried by a simple chat agent that always retrieves context before answering.

## Prerequisites
- Python 3.13 (repo uses `uv` for dependency management)
- Accounts/keys: Google Generative AI, Cerebras

## Setup
1) Install deps
   - `uv sync`
   - Or: `uv add langchain langchain-core langchain-community chromadb langchain-google-genai cerebras-cloud-sdk python-dotenv`
2) Configure environment
   - Copy `.env.example` to `.env` and fill values
   - Ensure processed JSON files exist in `data/processed/`
   - To reprocess files, place PDFs in `documents/` and run ingest.py

## Data Format (processed JSON)
Each file in `data/processed/` contains:
```json
{
  "source": "string",
  "content": "string",
  "Product features and benefits": [
    "feature 1",
    "feature 2"
  ],
  "Areas of application": [
    "area 1",
    "area 2"
  ],
  "General Product Information": {
    "Product number (Americas)": "",
    "Product name (Americas)": "",
    "Family brand": "",
    "ANSI code": ""
  },
  "Electrical Data": {
    "Nominal wattage": ""
  },
  "Photometric Data": {
    "Nominal luminous flux": "",
    "Useful luminous flux ( Φ use)": "",
    "Φ use value refers to luminous flux": "",
    "Illuminated field": "",
    "Color temperature": "",
    "Correlated color temperature CCT": "",
    "Chromaticity coordinate x": "",
    "Chromaticity coordinate y": "",
    "Color rendering index Ra": ""
  },
  "Physical Attributes & Dimensions": {
    "Lamp base": ""
  },
  "Product datasheet": {
    "Diameter": "",
    "Length": ""
  },
  "Operating Conditions": {
    "Burning position": ""
  },
  "Environmental & Regulatory Information": {
    "Primary article identifier": "",
    "Energy efficiency class": "",
    "Declaration no. in SCIP database": ""
  }
}
```
The indexer will also add `doc_id` from the filename.

## Build the Index
- `uv run python -m rag_mvp.index_json --processed-dir data/processed --index-dir data/index/chroma`
- Output persists to `data/index/chroma`.
- The document metadata transforms all maps into lists of strings containing the values as concatenated strings 

## Run the Chat Agent
- `uv run python -m rag_mvp.agent chat --index-dir data/index/chroma`
- Type a question; the agent retrieves top-k chunks and answers with brief citations like `[1]`.
- The agent is capable of using the rag iteratively.
- The agent can use the rag tool to filter the search via substrings.

## Project Layout
- `main.py` — ingestion from PDFs to JSON (Docling)
- `rag_mvp/index_json.py` — build Chroma index from processed JSON
- `rag_mvp/tools.py` — retrieval helper + context formatting
- `rag_mvp/agent.py` — minimal chat agent with memory
- `data/processed/` — input JSONs
- `data/index/chroma/` — Chroma persistence

## Troubleshooting
- Missing embeddings: ensure `GOOGLE_API_KEY` is set
- Cerebras auth: ensure `CEREBRAS_API_KEY` is set
- No results: confirm `data/processed/` has JSON with non-empty `content`
