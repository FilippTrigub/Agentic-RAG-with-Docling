from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from rag_mvp.index_json import build_index
from rag_mvp.agent import run_chat
from rag_mvp.web import run_web_server


def cmd_index(processed: Path, index_dir: Path, collection: str) -> None:
    n = build_index(processed, index_dir, collection)
    print(f"Indexed {n} documents from {processed} into {index_dir} ({collection})")


def cmd_chat(index_dir: Path, collection: str) -> None:
    run_chat(index_dir=str(index_dir), collection=collection)


def cmd_web(host: str, port: int, debug: bool) -> None:
    run_web_server(host=host, port=port, debug=debug)


def main(argv: Optional[list[str]] = None) -> None:
    load_dotenv()  # load .env if present

    parser = argparse.ArgumentParser(description="RAG MVP CLI")
    sub = parser.add_subparsers(dest="cmd")

    p_index = sub.add_parser("index", help="Build Chroma index from processed JSON")
    p_index.add_argument("--processed-dir", type=Path, default=Path("data/processed"))
    p_index.add_argument("--index-dir", type=Path, default=Path("data/index/chroma"))
    p_index.add_argument("--collection", type=str, default="rag_mvp")

    p_chat = sub.add_parser("chat", help="Start chat agent")
    p_chat.add_argument("--index-dir", type=Path, default=Path("data/index/chroma"))
    p_chat.add_argument("--collection", type=str, default="rag_mvp")

    p_web = sub.add_parser("web", help="Start web server")
    p_web.add_argument("--host", type=str, default="0.0.0.0")
    p_web.add_argument("--port", type=int, default=5000)
    p_web.add_argument("--debug", action="store_true", default=False)

    p_run = sub.add_parser("run", help="Index then start chat")
    p_run.add_argument("--processed-dir", type=Path, default=Path("data/processed"))
    p_run.add_argument("--index-dir", type=Path, default=Path("data/index/chroma"))
    p_run.add_argument("--collection", type=str, default="rag_mvp")

    args = parser.parse_args(argv)

    # If no subcommand provided, default to 'run' with standard paths
    if getattr(args, "cmd", None) is None:
        args.cmd = "run"
        setattr(args, "processed_dir", Path("data/processed"))
        setattr(args, "index_dir", Path("data/index/chroma"))
        setattr(args, "collection", "rag_mvp")

    try:
        if args.cmd == "index":
            cmd_index(args.processed_dir, args.index_dir, args.collection)
        elif args.cmd == "chat":
            cmd_chat(args.index_dir, args.collection)
        elif args.cmd == "web":
            cmd_web(args.host, args.port, args.debug)
        elif args.cmd == "run":
            cmd_index(args.processed_dir, args.index_dir, args.collection)
            cmd_chat(args.index_dir, args.collection)
        else:
            parser.error(f"Unknown command: {args.cmd}")
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")


if __name__ == "__main__":
    main()
