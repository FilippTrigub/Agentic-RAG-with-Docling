#!/usr/bin/env python3
import random


def main() -> None:
    numbers = [random.randint(1, 100) for _ in range(5)]
    print(f"Random numbers: {numbers}")
    print(f"Sum: {sum(numbers)}")
    print(f"Max: {max(numbers)}")
    print(f"Min: {min(numbers)}")


if __name__ == "__main__":
    main()
