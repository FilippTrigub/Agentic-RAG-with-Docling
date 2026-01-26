#!/usr/bin/env python3
"""
Hello World for Embeddings and Vector Search
Demonstrates embedding concepts without requiring external APIs
"""

import math


def simple_embedding(text: str) -> list[float]:
    """
    Create a simple embedding based on text characteristics
    (This is a toy example - real embeddings use neural networks)
    """
    # Simple features: length, vowel count, unique chars
    length = len(text)
    vowels = sum(1 for c in text.lower() if c in 'aeiou')
    unique_chars = len(set(text.lower()))
    
    # Normalize to create a simple 3D vector
    return [length / 100.0, vowels / 50.0, unique_chars / 50.0]


def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """Calculate cosine similarity between two vectors"""
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(b * b for b in vec2))
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)


def main():
    """Demonstrate embedding and similarity concepts"""
    print("=" * 60)
    print("Hello from Vector Embeddings!")
    print("=" * 60)
    
    # Sample documents
    documents = [
        "Python is a programming language",
        "Machine learning uses neural networks",
        "Vector databases store embeddings",
        "RAG combines retrieval and generation",
        "Semantic search finds similar meanings",
    ]
    
    print("\n📄 Documents:")
    for i, doc in enumerate(documents, 1):
        print(f"  {i}. {doc}")
    
    # Create embeddings
    print("\n🔢 Creating embeddings (simplified)...")
    embeddings = [simple_embedding(doc) for doc in documents]
    
    print("\n📊 Document Embeddings:")
    for i, (doc, emb) in enumerate(zip(documents, embeddings), 1):
        print(f"  {i}. [{emb[0]:.3f}, {emb[1]:.3f}, {emb[2]:.3f}] - {doc[:40]}...")
    
    # Query
    query = "What is semantic search?"
    query_embedding = simple_embedding(query)
    
    print(f"\n🔍 Query: '{query}'")
    print(f"   Embedding: [{query_embedding[0]:.3f}, {query_embedding[1]:.3f}, {query_embedding[2]:.3f}]")
    
    # Calculate similarities
    print("\n📏 Similarity Scores:")
    similarities = []
    for i, (doc, doc_emb) in enumerate(zip(documents, embeddings), 1):
        similarity = cosine_similarity(query_embedding, doc_emb)
        similarities.append((similarity, i, doc))
        print(f"  {i}. {similarity:.4f} - {doc}")
    
    # Find most similar
    similarities.sort(reverse=True)
    best_match = similarities[0]
    
    print(f"\n✨ Most Similar Document:")
    print(f"   Score: {best_match[0]:.4f}")
    print(f"   Document: {best_match[2]}")
    
    print("\n" + "=" * 60)
    print("Key Concepts:")
    print("  • Embeddings convert text to numerical vectors")
    print("  • Similar meanings → Similar vectors")
    print("  • Cosine similarity measures vector closeness")
    print("  • Vector databases enable fast similarity search")
    print("\nThis project uses:")
    print("  ✓ Google Generative AI for real embeddings")
    print("  ✓ Chroma for vector storage and retrieval")
    print("=" * 60)


if __name__ == "__main__":
    main()
