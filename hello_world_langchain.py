#!/usr/bin/env python3
"""
Hello World script demonstrating basic LangChain usage.
"""
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate


def demonstrate_prompt_template():
    """Show basic LangChain prompt template usage."""
    print("=== LangChain Prompt Template Demo ===\n")
    
    # Create a simple prompt template
    template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant for a RAG system."),
        ("human", "Say hello to {name} and explain what you do in one sentence."),
    ])
    
    # Format the prompt
    messages = template.format_messages(name="World")
    
    print("Generated prompt messages:")
    for msg in messages:
        print(f"  {msg.__class__.__name__}: {msg.content}")
    
    print("\n✓ LangChain prompt template created successfully!")


def demonstrate_messages():
    """Show basic LangChain message types."""
    print("\n=== LangChain Message Types Demo ===\n")
    
    system_msg = SystemMessage(content="You are a RAG assistant.")
    human_msg = HumanMessage(content="Hello, World!")
    
    print(f"System Message: {system_msg.content}")
    print(f"Human Message: {human_msg.content}")
    
    print("\n✓ LangChain messages created successfully!")


def main():
    """Run LangChain demonstrations."""
    print("Hello from LangChain!\n")
    
    demonstrate_prompt_template()
    demonstrate_messages()
    
    print("\n" + "="*50)
    print("LangChain Hello World completed!")
    print("This project uses LangChain for agent orchestration.")
    print("="*50)


if __name__ == "__main__":
    main()
