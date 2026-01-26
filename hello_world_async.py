#!/usr/bin/env python3
"""
Async Hello World script demonstrating async/await patterns.
"""
import asyncio


async def greet_async(name: str, delay: float = 0.5) -> str:
    """Asynchronously greet someone after a delay."""
    await asyncio.sleep(delay)
    return f"Hello, {name}!"


async def main():
    """Run multiple async greetings concurrently."""
    print("Starting async greetings...")
    
    # Create multiple greeting tasks
    tasks = [
        greet_async("World", 0.3),
        greet_async("RAG System", 0.2),
        greet_async("LangChain", 0.4),
        greet_async("Chroma DB", 0.1),
    ]
    
    # Run all tasks concurrently
    results = await asyncio.gather(*tasks)
    
    # Print results
    for result in results:
        print(result)
    
    print("\nAll async greetings completed!")


if __name__ == "__main__":
    asyncio.run(main())
