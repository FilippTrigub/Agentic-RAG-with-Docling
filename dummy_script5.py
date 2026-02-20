#!/usr/bin/env python3


def main() -> None:
    scores = {"Alice": 88, "Bob": 95, "Charlie": 72, "Diana": 91}

    print("Student Scores")
    print("-" * 25)
    for name, score in scores.items():
        status = "Pass" if score >= 75 else "Fail"
        print(f"  {name:<10} {score:>3}  {status}")

    avg = sum(scores.values()) / len(scores)
    top = max(scores, key=scores.get)  # type: ignore[arg-type]
    print(f"\nAverage: {avg:.1f}")
    print(f"Top scorer: {top}")


if __name__ == "__main__":
    main()
