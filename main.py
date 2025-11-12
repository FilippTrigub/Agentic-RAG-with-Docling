from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from rag_mvp.index_json import build_index
from rag_mvp.agent import run_chat

console = Console()

BANNER = """
╔═══════════════════════════════════════════════════════════╗
║  ██████╗  █████╗  ██████╗     ███╗   ███╗██╗   ██╗██████╗ ║
║  ██╔══██╗██╔══██╗██╔════╝     ████╗ ████║██║   ██║██╔══██╗║
║  ██████╔╝███████║██║  ███╗    ██╔████╔██║██║   ██║██████╔╝║
║  ██╔══██╗██╔══██║██║   ██║    ██║╚██╔╝██║╚██╗ ██╔╝██╔═══╝ ║
║  ██║  ██║██║  ██║╚██████╔╝    ██║ ╚═╝ ██║ ╚████╔╝ ██║     ║
║  ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝     ╚═╝     ╚═╝  ╚═══╝  ╚═╝     ║
╚═══════════════════════════════════════════════════════════╝
    🚀 Agentic RAG with Docling + LangChain + Chroma 🚀
"""


def show_banner() -> None:
    console.print(BANNER, style="bold cyan")


def cmd_index(processed: Path, index_dir: Path, collection: str) -> None:
    console.print("\n✨ [bold magenta]Starting indexing process...[/bold magenta]\n")
    n = build_index(processed, index_dir, collection)
    
    success_text = Text()
    success_text.append("🎉 Successfully indexed ", style="bold green")
    success_text.append(f"{n}", style="bold yellow")
    success_text.append(" documents!", style="bold green")
    
    panel = Panel(
        success_text,
        title="[bold cyan]✅ Indexing Complete[/bold cyan]",
        border_style="green",
        padding=(1, 2)
    )
    console.print(panel)
    console.print(f"📁 [cyan]Source:[/cyan] {processed}")
    console.print(f"💾 [cyan]Index:[/cyan] {index_dir}")
    console.print(f"📦 [cyan]Collection:[/cyan] {collection}\n")


def cmd_chat(index_dir: Path, collection: str) -> None:
    console.print("\n🤖 [bold magenta]Initializing chat agent...[/bold magenta]\n")
    run_chat(index_dir=str(index_dir), collection=collection)


def main(argv: Optional[list[str]] = None) -> None:
    load_dotenv()  # load .env if present
    show_banner()

    parser = argparse.ArgumentParser(
        description="🎨 Funky RAG MVP CLI - Your AI-powered document assistant!",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="cmd")

    p_index = sub.add_parser("index", help="📚 Build Chroma index from processed JSON")
    p_index.add_argument("--processed-dir", type=Path, default=Path("data/processed"))
    p_index.add_argument("--index-dir", type=Path, default=Path("data/index/chroma"))
    p_index.add_argument("--collection", type=str, default="rag_mvp")

    p_chat = sub.add_parser("chat", help="💬 Start chat agent")
    p_chat.add_argument("--index-dir", type=Path, default=Path("data/index/chroma"))
    p_chat.add_argument("--collection", type=str, default="rag_mvp")

    p_run = sub.add_parser("run", help="🚀 Index then start chat")
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
        elif args.cmd == "run":
            cmd_index(args.processed_dir, args.index_dir, args.collection)
            cmd_chat(args.index_dir, args.collection)
        else:
            parser.error(f"Unknown command: {args.cmd}")
    except KeyboardInterrupt:
        console.print("\n\n👋 [bold yellow]Interrupted. See you later![/bold yellow] ✨\n")
    except Exception as e:
        console.print(f"\n❌ [bold red]Error:[/bold red] {e}\n", style="red")
        raise


if __name__ == "__main__":
    main()
