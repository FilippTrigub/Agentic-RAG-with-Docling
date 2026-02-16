#!/usr/bin/env python3
"""
Dummy script for RAG MVP project.
Demonstrates basic operations like loading config, printing status, and basic logging.
"""

import sys
import json
from pathlib import Path


def main():
    """Main entry point for the dummy script."""
    print("=" * 60)
    print("RAG MVP - Dummy Script")
    print("=" * 60)
    print()

    # Check if .env file exists
    env_file = Path(".env")
    if env_file.exists():
        print("✓ .env file found")
    else:
        print("✗ .env file not found (copy from .env.example)")

    # Check data directory structure
    print("\nChecking data directory structure...")
    data_dir = Path("data")
    if data_dir.exists():
        print(f"✓ data/ directory exists")

        processed_dir = data_dir / "processed"
        if processed_dir.exists():
            json_files = list(processed_dir.glob("*.json"))
            print(f"  ✓ data/processed/ has {len(json_files)} JSON files")
        else:
            print("  ✗ data/processed/ not found")

        index_dir = data_dir / "index"
        if index_dir.exists():
            print(f"  ✓ data/index/ directory exists")
        else:
            print("  ✗ data/index/ not found")
    else:
        print("✗ data/ directory not found")

    # Check project modules
    print("\nChecking project modules...")
    rag_mvp_dir = Path("rag_mvp")
    if rag_mvp_dir.exists():
        print(f"✓ rag_mvp/ module directory exists")
        modules = [f.stem for f in rag_mvp_dir.glob("*.py") if f.name != "__pycache__"]
        for module in sorted(modules):
            print(f"  - {module}.py")
    else:
        print("✗ rag_mvp/ module directory not found")

    # Summary
    print("\n" + "=" * 60)
    print("Dummy script completed successfully!")
    print("Next steps:")
    print("  1. Configure .env with API keys")
    print("  2. Place JSON files in data/processed/")
    print("  3. Build index: uv run python -m rag_mvp.index_json ...")
    print("  4. Run agent: uv run python -m rag_mvp.agent chat ...")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)
