# Agentic RAG MVP: Docling + LangChain + Chroma

A production-ready retrieval-augmented generation (RAG) system that intelligently searches and queries structured product documentation.

## Overview

This MVP demonstrates an agentic RAG pipeline that:

1. **Parses documents** - Extracts structured data from PDFs using Docling (tables, sections, metadata)
2. **Embeds content** - Generates vector embeddings via Google Generative AI
3. **Stores searchably** - Persists embeddings and metadata in Chroma with filterable metadata
4. **Enables intelligent search** - Provides a chat agent with iterative RAG capabilities
5. **Filters precisely** - Supports exact `where` filters and substring `contains` post-retrieval filtering
6. **Maintains context** - Preserves conversation memory across interactions

### Key Features

- **Parallel document ingestion** with configurable worker processes
- **Structured metadata extraction** from product datasheets (technical specs, features, applications)
- **Hybrid search** combining vector similarity with metadata filtering
- **Agentic retrieval** that can iteratively refine searches
- **Source attribution** with inline citations

## Prerequisites

- **Python 3.13+** (dependency management via `uv`)
- **API Keys**:
  - Google Generative AI API key (for embeddings)
  - Cerebras API key (for chat model)

## Quick Start

### 1. Environment Setup

```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Install dependencies
uv sync
```

### 2. Configuration

```bash
# Copy environment template and add your API keys
cp .env.example .env
# Edit .env and add:
# GOOGLE_API_KEY=your_google_api_key
# CEREBRAS_API_KEY=your_cerebras_api_key
```

### 3. Prepare Data

The repository includes pre-processed JSON files in `data/processed/`. To process your own PDFs:

```bash
# Place PDFs in documents/ directory, then run:
uv run python ingest.py --input-dir documents --output-dir data/processed --workers 6
```

### 4. Run the Application

**Option A: All-in-one** (index + chat)
```bash
uv run python main.py run
```

**Option B: Step-by-step**
```bash
# Build the vector index
uv run python main.py index --processed-dir data/processed --index-dir data/index/chroma

# Start the chat agent
uv run python main.py chat --index-dir data/index/chroma
```

## Architecture

### Data Pipeline

```
PDFs → [Docling Parser] → Structured JSON → [Embeddings] → Chroma Vector Store → [Agent + Tools] → User
```

### Data Format

Processed JSON files (`data/processed/`) follow this structure:

```json
{
  "source": "documents/product.pdf",
  "content": "Full text content...",
  "Product features and benefits": ["feature 1", "feature 2"],
  "Areas of application": ["application 1", "application 2"],
  "General Product Information": {
    "ANSI code": "ABC123",
    "Product name (Americas)": "Product Name"
  },
  "Electrical Data": {
    "Nominal wattage": "500W",
    "Nominal voltage": "240 V"
  },
  "Photometric Data": {
    "Nominal luminous flux": "13500 lm",
    "Color temperature": "3200 K"
  },
  "Physical Attributes & Dimensions": {
    "Lamp base": "GY9.5",
    "Diameter": "18.0mm"
  },
  "Operating Conditions": {
    "Burning position": "Any",
    "Dimmable": "Yes"
  },
  "Environmental & Regulatory Information": {
    "Energy efficiency class": "G"
  }
}
```

During indexing, the system adds a `doc_id` (derived from filename) and flattens nested metadata for efficient filtering.

### Metadata Transformation

During indexing, nested structures are flattened into pipe-delimited strings for substring filtering:

```json
{
  "doc_id": "ZMP_1004795",
  "source": "documents\\ZMP_1004795.pdf",
  "areas_of_application": "Stage & Theatre | Studio, TV, & Film | Professional Photography | Club & Disco",
  "electrical_data": "Nominal wattage: 500W | Nominal voltage: 240 V",
  "photometric_data": "Nominal luminous flux: 13500 lm | Color temperature: 3200 K | ...",
  "product_features_and_benefits": "Robust construction | Consistent color | Dimmable to 0%",
  "physical_attributes_dimensions": "Lamp base: GY9.5 | Diameter: 18.0mm | Length: 80.0mm"
}
```

This enables efficient substring matching on metadata fields (e.g., searching for "GY9.5" in lamp base specifications).

## Usage Examples

### Interactive Chat

```bash
uv run python main.py chat --index-dir data/index/chroma
```

**Example queries:**
- "Show me all lamps with color temperature 3200K"
- "What are the dimmable products suitable for stage and theatre?"
- "Find lamps with GY9.5 base and 500W power"

The agent:
- Retrieves relevant documents using vector similarity
- Applies metadata filters (exact `where` clauses or substring `contains` filters)
- Iteratively refines searches if needed
- Provides answers with inline citations like `[1]`, `[2]`

## Project Structure

```
.
├── main.py                    # CLI entry point (index, chat, run commands)
├── ingest.py                  # PDF→JSON ingestion with parallel processing
├── rag_mvp/
│   ├── index_json.py         # Chroma index builder
│   ├── tools.py              # Retrieval tool with metadata filtering
│   └── agent.py              # LangChain chat agent with RAG capabilities
├── data/
│   ├── processed/            # Parsed JSON files (input for indexing)
│   └── index/chroma/         # Chroma vector store persistence
├── pyproject.toml            # Project dependencies (managed by uv)
├── .env.example              # Environment variable template
└── README.md                 # This file
```

## Implementation Notes

### Design Decisions

**Docling for Extraction**: Chosen for its robust table parsing capabilities. While field consistency varies across documents (e.g., product identifiers), the broad search approach using `where` and `contains` filters handles this gracefully.

**Metadata Flattening**: Nested structures are flattened to pipe-delimited strings, enabling substring searches without complex query languages.

**Agentic Approach**: The LangChain agent can iteratively invoke the RAG tool, refining searches based on initial results.

### Known Limitations

- **Numerical filtering**: Metadata is stored as strings. Implementing range queries (e.g., "wattage > 100") requires parsing and structured numerical indexing.
- **Model sensitivity**: Filter generation depends on LLM interpretation. Prompt engineering and temperature tuning can improve consistency.
- **Global variables**: Current implementation uses globals for simplicity. Production deployment requires refactoring for concurrency.

### Scaling Considerations

**For production deployment:**

1. **Vector Store**: Migrate from local Chroma to hosted solutions (Qdrant, Pinecone, Weaviate)
2. **API Layer**: Implement async request handling with FastAPI or similar frameworks
3. **Deployment**: Containerize with Docker and deploy to Kubernetes, or use serverless (AWS Lambda, Cloud Run)
4. **Result Limiting**: Implement pagination and hard limits to prevent context window exhaustion
5. **Caching**: Add Redis/Memcached for frequently accessed queries
6. **Monitoring**: Integrate observability (OpenTelemetry, Langfuse) for latency and cost tracking

**At scale:**
- Exhaustive queries ("give me all products") become impractical due to context limits and cost
- Implement intelligent result summarization and progressive disclosure
- Consider hybrid architectures with traditional databases for structured queries

## Troubleshooting

### Common Issues

**No embeddings generated**
```bash
# Ensure GOOGLE_API_KEY is set
echo $GOOGLE_API_KEY  # Linux/Mac
echo %GOOGLE_API_KEY% # Windows
```

**Cerebras authentication fails**
```bash
# Verify CEREBRAS_API_KEY in .env
cat .env | grep CEREBRAS_API_KEY
```

**No search results**
- Confirm `data/processed/` contains JSON files with non-empty `content` fields
- Rebuild the index: `uv run python main.py index`
- Check that the index directory exists and has data: `ls -la data/index/chroma/`

**Module import errors**
```bash
# Reinstall dependencies
uv sync --force
```

**Parallel ingestion fails**
```bash
# Reduce worker count
uv run python ingest.py --workers 1
```

## Development

### Adding Dependencies

```bash
uv add package-name           # Add runtime dependency
uv add --dev package-name     # Add development dependency
```

### Testing

```bash
# Install pytest
uv add --dev pytest

# Run tests (when available)
uv run pytest
```

### Code Style

- Python 3.13+, PEP 8 style guidelines
- 4-space indentation
- Type hints preferred
- Docstrings for non-trivial functions

See `AGENTS.md` for detailed development guidelines.

## Contributing

1. Create a feature branch
2. Make focused, incremental changes
3. Update README if behavior changes
4. Use conventional commits (e.g., `feat:`, `fix:`, `docs:`)
5. Open a pull request with clear description

## License

[Specify your license here]

## Acknowledgments

- **Docling** - Document parsing and structure extraction
- **LangChain** - Agentic RAG framework
- **Chroma** - Vector database
- **Google Generative AI** - Embeddings
- **Cerebras** - Fast inference for chat model
