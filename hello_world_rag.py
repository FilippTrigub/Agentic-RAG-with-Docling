#!/usr/bin/env python3
"""
Hello World script demonstrating basic RAG (Retrieval-Augmented Generation) concepts.
"""


class SimpleDocumentStore:
    """A simple in-memory document store to demonstrate RAG concepts."""
    
    def __init__(self):
        self.documents = [
            {
                "id": "doc1",
                "content": "Hello, World! This is the first document about greetings.",
                "metadata": {"topic": "greetings", "language": "English"}
            },
            {
                "id": "doc2",
                "content": "RAG systems combine retrieval and generation for better answers.",
                "metadata": {"topic": "RAG", "language": "English"}
            },
            {
                "id": "doc3",
                "content": "Chroma is a vector database for storing embeddings.",
                "metadata": {"topic": "databases", "language": "English"}
            },
            {
                "id": "doc4",
                "content": "LangChain helps build applications with language models.",
                "metadata": {"topic": "frameworks", "language": "English"}
            },
        ]
    
    def search(self, query: str, top_k: int = 2) -> list[dict]:
        """Simple keyword-based search (not using embeddings for this demo)."""
        query_lower = query.lower()
        
        # Score documents based on keyword matches
        scored_docs = []
        for doc in self.documents:
            score = sum(
                word in doc["content"].lower() 
                for word in query_lower.split()
            )
            if score > 0:
                scored_docs.append((score, doc))
        
        # Sort by score and return top_k
        scored_docs.sort(reverse=True, key=lambda x: x[0])
        return [doc for _, doc in scored_docs[:top_k]]


def demonstrate_rag_pipeline():
    """Demonstrate a simple RAG pipeline."""
    print("=== Simple RAG Pipeline Demo ===\n")
    
    # Initialize document store
    store = SimpleDocumentStore()
    print(f"✓ Document store initialized with {len(store.documents)} documents\n")
    
    # User query
    query = "What is RAG?"
    print(f"Query: {query}\n")
    
    # Step 1: Retrieval
    print("Step 1: Retrieving relevant documents...")
    retrieved_docs = store.search(query, top_k=2)
    
    print(f"Retrieved {len(retrieved_docs)} documents:")
    for i, doc in enumerate(retrieved_docs, 1):
        print(f"  [{i}] {doc['id']}: {doc['content'][:60]}...")
    
    # Step 2: Context preparation
    print("\nStep 2: Preparing context from retrieved documents...")
    context = "\n".join([doc["content"] for doc in retrieved_docs])
    print(f"Context prepared ({len(context)} characters)")
    
    # Step 3: Generation (simulated)
    print("\nStep 3: Generating answer (simulated)...")
    answer = (
        f"Based on the retrieved documents, {query} "
        f"RAG systems combine retrieval and generation to provide "
        f"better, context-aware answers by first finding relevant "
        f"information and then using it to generate responses."
    )
    print(f"\nAnswer: {answer}")
    
    # Show citations
    print("\nCitations:")
    for i, doc in enumerate(retrieved_docs, 1):
        print(f"  [{i}] {doc['id']} - Topic: {doc['metadata']['topic']}")


def main():
    """Run RAG demonstration."""
    print("Hello from the RAG System!\n")
    print("This demonstrates the basic concept of Retrieval-Augmented Generation.\n")
    
    demonstrate_rag_pipeline()
    
    print("\n" + "="*70)
    print("RAG Hello World completed!")
    print("In a real system, this would use:")
    print("  - Docling for document parsing")
    print("  - Google Generative AI for embeddings")
    print("  - Chroma for vector storage")
    print("  - LangChain for agent orchestration")
    print("="*70)


if __name__ == "__main__":
    main()
