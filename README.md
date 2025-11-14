# Agentic RAG MVP

A minimal retrieval-augmented generation (RAG) application built with Docling, LangChain, and Chroma.

## Overview

This project implements a simple RAG system for querying document collections:

1. **Document Processing**: PDFs are parsed using Docling to extract structured JSON data.
2. **Embedding & Indexing**: Content is embedded using Google Generative AI embeddings and stored in Chroma with metadata for searchable filters.
3. **Query Interface**: A chat agent allows users to query the indexed documents using a RAG tool.
4. **Iterative Search**: The agent can perform iterative searches with filters and post-retrieval processing.
5. **Memory**: Basic conversation memory is maintained for context.

## Prerequisites

- Python 3.13 (managed with `uv`)
- API keys for Google Generative AI and Cerebras

## Setup

1. **Create and activate virtual environment**:
   ```bash
   uv venv
   source .venv/bin/activate  # On Linux/macOS
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Configure environment**:
   - Copy `.env.example` to `.env` and fill in your API keys.
   - Ensure processed JSON files exist in `data/processed/`.
   - To reprocess PDFs: Place them in a `documents/` directory and run `ingest.py`.

## Data Format

Processed JSON files in `data/processed/` follow this structure:

```json
{
  "source": "string",
  "content": "string",
  "Product features and benefits": ["feature 1", "feature 2"],
  "Areas of application": ["area 1", "area 2"],
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
    "Useful luminous flux (Φ use)": "",
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

The indexer adds a `doc_id` field derived from the filename.

## Building the Index

Transform metadata into searchable strings and build the Chroma index:

```bash
uv run python -m rag_mvp.index_json --processed-dir data/processed --index-dir data/index/chroma
```

This persists the index to `data/index/chroma`. Metadata is flattened into concatenated strings, e.g.:

```json
{
  "areas_of_application": "Stage & Theatre | Studio, TV, & Film | Professional Photography | Club & Disco",
  "doc_id": "ZMP_1004795",
  "electrical_data": "Nominal wattage: 500W | Nominal voltage: 240 V",
  "environmental_regulatory_information": "Primary article identifier: 4008321099846 | 4052899015524 | Energy efficiency class: G | Declaration no. in SCIP database: No declarable substances contained",
  "general_product_information": "ANSI code: FRJ | LIF code: CP/82 | Global order reference: 64674",
  "operating_conditions": "Burning position: Any | Dimmable: Yes | Nominal lifetime: 200 hr",
  "photometric_data": "Nominal luminous flux: 13500 lm | Useful luminous flux (Φ use): 12240 lm | Φ use value refers to luminous flux: 360 | Luminous efficacy: 27 lm/W | Illuminated field: 8.0*18 mm² | Color temperature: 3200 K | Correlated color temperature CCT: 3193 K | Chromaticity coordinate x: 0.425 | Chromaticity coordinate y: 0.401 | Color rendering index Ra: 100 | Light center length (LCL): 46.5mm",
  "physical_attributes_dimensions": "Lamp base: GY9.5 | Diameter: 18.0mm | Length: 80.0mm | Product weight: 18.80 g",
  "product_features_and_benefits": "Robust construction for reliable, lasting performance | Consistent color over the life of the lamps | Instant on and nearly constant luminous flux over the life of the lamp | Broad product portfolio supporting the stage and studio markets | Dimmable to 0% with traditional amber shift",
  "source": "documents/ZMP_1004795.pdf"
}
```

## Running the Chat Agent

Start the interactive chat agent:

```bash
uv run python -m rag_mvp.agent chat --index-dir data/index/chroma
```

- Enter queries; the agent retrieves relevant chunks and provides answers with citations like `[1]`.
- Supports iterative RAG usage and substring-based filtering.

## Project Notes

Docling was chosen for metadata extraction from table fields, which works well despite some inconsistencies across documents (e.g., product identification numbers). A broad search approach using `where` conditions and post-processing was implemented.

### Known Issues & Future Improvements

- **Numerical Filtering**: Full numerical metadata evaluation is needed for advanced filtering. Requires enhanced parsing and data modeling.
- **Model Dependency**: Responses vary with temperature and model choice due to filter generation. Prompt engineering could help.
- **Global Variables**: Current implementation uses globals, unsuitable for API deployment.

## Scaling Considerations

To scale beyond local development:

- Migrate vector store to a hosted database like Qdrant.
- Implement async handling for concurrent API requests.
- Containerize and deploy with auto-scaling or serverless functions (e.g., AWS Lambda).

Additional challenges with large datasets:

- Exhaustive searches may exceed context limits and increase costs.
- Broad filters can return too many results; implement post-retrieval limits and refined tooling.

## Project Structure

- `main.py`: PDF ingestion to JSON using Docling
- `rag_mvp/index_json.py`: Chroma index construction from JSON
- `rag_mvp/tools.py`: Retrieval utilities and context formatting
- `rag_mvp/agent.py`: Chat agent with memory
- `data/processed/`: Processed JSON inputs
- `data/index/chroma/`: Chroma vector store

## Troubleshooting

- **Missing embeddings**: Verify `GOOGLE_API_KEY` is set in `.env`.
- **Authentication errors**: Ensure `CEREBRAS_API_KEY` is configured.
- **No search results**: Check that `data/processed/` contains JSON files with non-empty `content` fields.