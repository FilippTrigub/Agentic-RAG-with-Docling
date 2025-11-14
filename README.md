# Agentic RAG MVP: Docling + LangChain + Chroma

This project is a minimal Retrieval-Augmented Generation (RAG) application that demonstrates how to build a chat agent that can answer questions based on a knowledge base of documents.

## Features

-   **Document Processing:** Parses documents using Docling to extract content and metadata.
-   **Vector Embeddings:** Creates vector embeddings of the document content using Google Generative AI.
-   **Vector Store:** Stores the embedded documents in a local ChromaDB vector store.
-   **Chat Agent:** Provides a simple chat agent that uses a RAG tool to query the knowledge base.
-   **Iterative Search:** The agent can use the RAG tool to perform iterative searches and refine its answers.
-   **Metadata Filtering:** The agent can filter searches based on document metadata.
-   **Basic Memory:** The agent has basic memory to maintain context during a conversation.

## How it Works

The application follows a simple workflow:

```
┌───────────────────┐      ┌───────────────────┐      ┌───────────────────┐
│   PDF Documents   │ ───> │      Docling      │ ───> │  Processed JSON   │
└───────────────────┘      └───────────────────┘      └───────────────────┘
                                                            │
                                                            ▼
┌───────────────────┐      ┌───────────────────┐      ┌───────────────────┐
│   ChromaDB Index  │ <─── │ Google Generative │ <─── │      Content      │
└───────────────────┘      │        AI         │      └───────────────────┘
        │                  └───────────────────┘
        ▼
┌───────────────────┐      ┌───────────────────┐
│    Chat Agent     │ <─── │     RAG Tool      │
└───────────────────┘      └───────────────────┘
```

1.  **Ingestion:** PDF documents are placed in the `documents/` directory. The `ingest.py` script uses Docling to parse the PDFs and extract their content and metadata into JSON files in the `data/processed/` directory.
2.  **Indexing:** The `rag_mvp/index_json.py` script reads the processed JSON files, generates embeddings for the content using the Google Generative AI API, and stores the embeddings and metadata in a ChromaDB index located in the `data/index/chroma/` directory.
3.  **Chat:** The `rag_mvp/agent.py` script starts a chat agent that has access to a RAG tool. The agent can use this tool to search the ChromaDB index for relevant documents and use them to answer user questions.

## Prerequisites

-   Python 3.13 or higher
-   `uv` for dependency management
-   A Google Generative AI API key
-   A Cerebras API key

## Getting Started

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repository.git
    cd your-repository
    ```

2.  **Create a virtual environment and install dependencies:**

    ```bash
    uv venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    uv sync
    ```

3.  **Configure your environment:**

    -   Copy the `.env.example` file to `.env`:

        ```bash
        cp .env.example .env
        ```

    -   Open the `.env` file and add your Google Generative AI and Cerebras API keys:

        ```
        GOOGLE_API_KEY="your-google-api-key"
        CEREBRAS_API_KEY="your-cerebras-api-key"
        ```

4.  **Add your documents:**

    Place your PDF documents in the `documents/` directory.

5.  **Ingest the documents:**

    ```bash
    uv run python -m ingest
    ```

    This will create processed JSON files in the `data/processed/` directory.

6.  **Build the index:**

    ```bash
    uv run python main.py index
    ```

    This will create a ChromaDB index in the `data/index/chroma/` directory.

7.  **Start the chat agent:**

    ```bash
    uv run python main.py chat
    ```

    You can now start asking questions to the chat agent.

## Project Structure

-   `ingest.py`: Ingestion script to process PDFs with Docling.
-   `main.py`: Main entry point for the application, providing a CLI to build the index and run the chat agent.
-   `rag_mvp/index_json.py`: Script to build the ChromaDB index from processed JSON files.
-   `rag_mvp/tools.py`: Contains the RAG tool and other helper functions.
-   `rag_mvp/agent.py`: The chat agent implementation.
-   `data/processed/`: Directory for the processed JSON files.
-   `data/index/chroma/`: Directory for the ChromaDB index.
-   `documents/`: Directory for your PDF documents.

## Scaling and Future Work

### Scaling

-   **Vector Store:** For larger datasets, move the vector store to a self-hosted or cloud-hosted solution like Qdrant or Pinecone.
-   **API Deployment:** Deploy the application as an API to handle concurrent requests. This will require making the implementation asynchronous.
-   **Serverless:** For a more scalable and cost-effective solution, deploy the application as serverless functions (e.g., AWS Lambda).

### Future Work

-   **Numerical Metadata Filtering:** Extend the data model and parsing to enable numerical filtering on metadata.
-   **Prompt Optimization:** Optimize the prompts to improve the agent's ability to generate the correct filters.
-   **Refactor Global Variables:** Remove the use of global variables to make the code more modular and easier to deploy as an API.
-   **Advanced RAG Techniques:** Implement more advanced RAG techniques like post-retrieval processing and more refined tooling.

## Troubleshooting

-   **Missing Embeddings:** Ensure that your `GOOGLE_API_KEY` is set correctly in the `.env` file.
-   **Cerebras Authentication Errors:** Ensure that your `CEREBRAS_API_KEY` is set correctly in the `.env` file.
-   **No Results:** Make sure that you have run the ingestion and indexing steps and that the `data/processed/` directory contains JSON files with non-empty `content` fields.
