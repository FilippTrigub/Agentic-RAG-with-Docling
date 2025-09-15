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
- The document metadata transforms all maps into lists of strings containing the values as concatenated strings, for example:
```json
{
  "areas_of_application": "Stage & Theatre | Studio, TV, & Film | Professional Photography | Club & Disco",
  "electrical_data": "Nominal wattage: 500W",
  "environmental_regulatory_information": "Primary article identifier: 4008321099846 | 4052899015524 | Energy efficiency class: G | Declaration no. in SCIP database: No declarable substances contained",
  "general_product_information": "ANSI code: FRJ | LIF code: CP/82",
  "operating_conditions": "Burning position: Any | Dimmable: Yes",
  "photometric_data": "Nominal luminous flux: 13500 lm | Useful luminous flux ( Φ use): 12240 lm | Φ use value refers to luminous flux: 360 | Luminous efficacy: 27 lm/W | Illuminated field: 8.0*18 mm² | Color temperature: 3200 K | Correlated color temperature CCT: 3193 K | Chromaticity coordinate x: 0.425 | Chromaticity coordinate y: 0.401 | Color rendering index Ra: 100",
  "physical_attributes_dimensions": "Lamp base: GY9.5 | Diameter: 18.0mm | Length: 80.0mm",
  "product_features_and_benefits": "Robust construction for reliable, lasting performance | Consistent color over the life of the lamps | Instant on and nearly constant luminous flux over the life of the lamp | Broad product portfolio supporting the stage and studio markets | Dimmable to 0% with traditional amber shift",
  "source": "documents\\ZMP_1004795.pdf"
}
```

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
