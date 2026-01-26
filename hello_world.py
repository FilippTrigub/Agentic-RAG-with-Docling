#!/usr/bin/env python3
"""
Basic Hello World script for Python
"""


def main():
    """Print a simple hello world message"""
    print("Hello, World!")
    print("Welcome to the RAG MVP project!")
    
    # Show Python version
    import sys
    print(f"\nRunning Python {sys.version}")
    
    # Show project info
    print("\nThis is an Agentic RAG MVP using:")
    print("  - Docling for document parsing")
    print("  - LangChain for agent orchestration")
    print("  - Chroma for vector storage")
    print("  - Google Generative AI for embeddings")


if __name__ == "__main__":
    main()
