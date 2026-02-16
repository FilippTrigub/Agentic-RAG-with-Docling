#!/usr/bin/env python3
from datetime import datetime


def main() -> None:
    now = datetime.now()
    greeting = "Hello, World!"
    
    print(f"Current timestamp: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Message: {greeting}")
    print(f"Reversed: {greeting[::-1]}")
    print(f"Uppercase: {greeting.upper()}")
    print(f"Character count: {len(greeting)}")


if __name__ == "__main__":
    main()
