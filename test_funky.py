#!/usr/bin/env python3
"""Test script to demonstrate the funky CLI features"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
import time

console = Console()

# Show the banner
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

console.print(BANNER, style="bold cyan")

# Demo 1: Indexing with progress bar
console.print("\n✨ [bold magenta]Demo 1: Indexing Process[/bold magenta]\n")

with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    console=console
) as progress:
    task = progress.add_task("📄 [cyan]Loading documents...", total=100)
    for i in range(100):
        time.sleep(0.01)
        progress.advance(task)

console.print("✨ [green]Loaded 42 documents[/green]")

with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    console=console
) as progress:
    task = progress.add_task("🔮 [cyan]Creating embeddings...", total=None)
    time.sleep(1)
    progress.update(task, description="💾 [cyan]Adding documents to vector store...")
    time.sleep(0.5)
    progress.update(task, description="💿 [cyan]Persisting index...")
    time.sleep(0.5)

# Demo 2: Success panel
success_text = Text()
success_text.append("🎉 Successfully indexed ", style="bold green")
success_text.append("42", style="bold yellow")
success_text.append(" documents!", style="bold green")

panel = Panel(
    success_text,
    title="[bold cyan]✅ Indexing Complete[/bold cyan]",
    border_style="green",
    padding=(1, 2)
)
console.print(panel)
console.print(f"📁 [cyan]Source:[/cyan] data/processed")
console.print(f"💾 [cyan]Index:[/cyan] data/index/chroma")
console.print(f"📦 [cyan]Collection:[/cyan] rag_mvp\n")

# Demo 3: Chat interface
console.print("\n✨ [bold magenta]Demo 2: Chat Interface[/bold magenta]\n")

welcome_panel = Panel(
    "[bold green]Welcome to the Funky RAG Chat! 🎉[/bold green]\n\n"
    "💡 Ask me anything about your product specs!\n"
    "🔍 I'll search through the documents to find answers\n"
    "✨ Type [bold yellow]'exit'[/bold yellow] or [bold yellow]'quit'[/bold yellow] to leave\n",
    title="[bold cyan]🤖 Chat Agent Ready[/bold cyan]",
    border_style="cyan",
    padding=(1, 2)
)
console.print(welcome_panel)

# Simulate a query
console.print("\n[bold magenta]You[/bold magenta] 💬 What products have a color temperature of 3200K?")
console.print("\n🔎 [dim]Searching documents...[/dim]\n")

time.sleep(0.5)

# Simulate answer
answer = """Based on the search results, I found several products with a color temperature of 3200K:

1. **Product ZMP_1004795** - This is a halogen lamp with:
   - Color temperature: 3200K
   - Nominal wattage: 500W
   - Lamp base: GY9.5
   - Applications: Stage & Theatre, Studio/TV/Film

2. **Product ZMP_1006242** - Another 3200K option with similar specifications

These products are designed for professional lighting applications where accurate color rendering is critical. [1][2]"""

answer_panel = Panel(
    answer,
    title=f"[bold green]🤖 Assistant[/bold green] [dim](Found 5 relevant docs)[/dim]",
    border_style="green",
    padding=(1, 2)
)
console.print(answer_panel)

# Demo 4: Sources table
sources_table = Table(
    title="📚 Sources",
    show_header=True,
    header_style="bold cyan",
    border_style="blue"
)
sources_table.add_column("#", style="yellow", width=4)
sources_table.add_column("Document", style="cyan")

sources_table.add_row("[1]", "documents/ZMP_1004795.pdf")
sources_table.add_row("[2]", "documents/ZMP_1006242.pdf")
sources_table.add_row("[3]", "documents/ZMP_1006707.pdf")
sources_table.add_row("[4]", "documents/ZMP_1006708.pdf")
sources_table.add_row("[5]", "documents/ZMP_1006710.pdf")

console.print(sources_table)

# Final message
console.print("\n\n👋 [bold yellow]Demo complete! Your RAG MVP is now FUNKY! ✨[/bold yellow]\n")
