#!/usr/bin/env python3
"""
Hello World for LangChain concepts
Demonstrates basic LangChain patterns without requiring API keys
"""


def main():
    """Demonstrate basic LangChain concepts"""
    print("=" * 60)
    print("Hello from LangChain!")
    print("=" * 60)
    
    print("\n🔗 LangChain is a framework for building LLM applications")
    print("\nCore Concepts:")
    
    # 1. Chains
    print("\n1️⃣  Chains - Sequential operations")
    print("   Example: Input → Process → Output")
    steps = ["Receive user query", "Retrieve context", "Generate response"]
    for i, step in enumerate(steps, 1):
        print(f"      Step {i}: {step}")
    
    # 2. Agents
    print("\n2️⃣  Agents - Dynamic decision making")
    print("   Agents can choose which tools to use based on the task")
    tools = ["RAG Tool", "Calculator", "Web Search"]
    print(f"   Available tools: {', '.join(tools)}")
    
    # 3. Memory
    print("\n3️⃣  Memory - Conversation context")
    conversation = [
        {"role": "user", "content": "What is RAG?"},
        {"role": "assistant", "content": "RAG is Retrieval-Augmented Generation..."},
        {"role": "user", "content": "How does it work?"},
    ]
    print("   Conversation history:")
    for msg in conversation:
        print(f"      {msg['role']}: {msg['content']}")
    
    # 4. Tools
    print("\n4️⃣  Tools - External capabilities")
    print("   Tools extend agent capabilities:")
    print("      - Vector store retrieval")
    print("      - API calls")
    print("      - File operations")
    print("      - Custom functions")
    
    # 5. Prompts
    print("\n5️⃣  Prompts - Structured instructions")
    prompt_template = """
    Context: {context}
    Question: {question}
    Answer: """
    print(f"   Template: {prompt_template.strip()}")
    
    print("\n" + "=" * 60)
    print("This project uses LangChain for:")
    print("  ✓ Agent orchestration")
    print("  ✓ RAG tool integration")
    print("  ✓ Conversation memory")
    print("  ✓ Chroma vector store")
    print("=" * 60)


if __name__ == "__main__":
    main()
