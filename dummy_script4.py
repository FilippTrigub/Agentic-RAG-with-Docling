#!/usr/bin/env python3


def main() -> None:
    # Simple list operations
    fruits = ["apple", "banana", "cherry", "date", "elderberry"]
    
    print("Original list:", fruits)
    print("First item:", fruits[0])
    print("Last item:", fruits[-1])
    print("Sorted:", sorted(fruits))
    print("Reversed:", fruits[::-1])
    
    # Simple calculations
    numbers = [10, 20, 30, 40, 50]
    average = sum(numbers) / len(numbers)
    
    print(f"\nNumbers: {numbers}")
    print(f"Average: {average}")
    print(f"Total: {sum(numbers)}")


if __name__ == "__main__":
    main()
