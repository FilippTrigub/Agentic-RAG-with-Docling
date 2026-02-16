#!/usr/bin/env python3
"""
Another dummy script for testing purposes.
This script demonstrates basic Python functionality.
"""

def greet(name: str) -> str:
    """Return a greeting message."""
    return f"Hello, {name}!"

def add_numbers(a: int, b: int) -> int:
    """Return the sum of two numbers."""
    return a + b

def main():
    """Main function to demonstrate script functionality."""
    print(greet("World"))
    print(f"2 + 3 = {add_numbers(2, 3)}")
    print("This is another dummy script.")

if __name__ == "__main__":
    main()