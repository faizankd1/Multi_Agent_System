"""CLI Pipeline Runner powered by compiled LangGraph StateGraph."""

import sys
import time
from typing import Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

from src.graph import research_app
from src.state import ResearchState

console = Console()


def run_research_pipeline(topic: str) -> Dict[str, Any]:
    """Execute the full multi-agent research pipeline via LangGraph."""
    console.print(Panel(
        f"[bold cyan]Multi-Agent Research System (LangGraph)[/bold cyan]\n"
        f"[dim]Initiating autonomous research graph for:[/dim] [bold yellow]{topic}[/bold yellow]",
        border_style="cyan"
    ))

    initial_state: ResearchState = {
        "topic": topic,
        "sub_queries": [],
        "search_results": [],
        "scraped_sources": [],
        "draft_report": "",
        "critic_review": None,
        "revision_count": 0,
        "revision_notes": [],
        "current_node": "start",
        "timeline": [],
    }

    start_total = time.time()
    final_state = {}

    # Stream graph updates node-by-node
    for event in research_app.stream(initial_state, stream_mode="updates"):
        for node_name, node_state in event.items():
            final_state.update(node_state)

            if node_name == "plan_queries":
                queries = node_state.get("sub_queries", [])
                console.print("\n[bold magenta]📍 [Node: Planner][/bold magenta] Strategic Search Angles Generated:")
                for i, q in enumerate(queries, 1):
                    console.print(f"  [cyan]{i}.[/cyan] {q}")

            elif node_name == "research":
                results = node_state.get("search_results", [])
                console.print(f"\n[bold blue]🔍 [Node: Researcher][/bold blue] Retrieved [green]{len(results)}[/green] search sources.")

            elif node_name == "curate_content":
                sources = node_state.get("scraped_sources", [])
                console.print(f"\n[bold yellow]📄 [Node: Curator][/bold yellow] Scraped [green]{len(sources)}[/green] deep web resources:")
                for s in sources:
                    console.print(f"  • [underline]{s.get('title')}[/underline] ({s.get('url')})")

            elif node_name == "write_report":
                console.print("\n[bold green]✍️ [Node: Writer][/bold green] Synthesized comprehensive research report draft.")

            elif node_name == "critique_report":
                review = node_state.get("critic_review", {})
                score = review.get("score", 0)
                passed = review.get("passed", False)
                status_color = "green" if passed else "yellow"
                console.print(f"\n[bold {status_color}]🧐 [Node: Critic][/bold {status_color}] Audit Complete:")
                console.print(f"  • Overall Score: [bold {status_color}]{score}/10[/bold {status_color}] (Passed: {passed})")
                console.print(f"  • Verdict: {review.get('verdict')}")

                if not passed and node_state.get("revision_notes"):
                    console.print("  [yellow]⚡ Triggering Autonomous Revision Loop with feedback...[/yellow]")

    total_time = round(time.time() - start_total, 2)

    # Telemetry Summary Table
    table = Table(title=f"Research Execution Summary ({total_time}s)", border_style="dim")
    table.add_column("Stage / Agent", style="cyan")
    table.add_column("Duration (s)", justify="right", style="green")
    table.add_column("Details", style="dim")

    for event in final_state.get("timeline", []):
        table.add_row(
            event.get("stage", event.get("node", "Agent")),
            str(event.get("duration_seconds", 0.0)),
            event.get("details", "")[:80]
        )

    console.print("\n")
    console.print(table)

    # Print Final Report
    console.print("\n" + "=" * 60)
    console.print("[bold green]📝 FINAL RESEARCH REPORT[/bold green]")
    console.print("=" * 60 + "\n")
    console.print(final_state.get("draft_report", "No report generated."))

    return final_state


if __name__ == "__main__":
    if len(sys.argv) > 1:
        topic_input = " ".join(sys.argv[1:])
    else:
        topic_input = input("\nEnter a research topic: ").strip()

    if not topic_input:
        topic_input = "Agentic AI Architectures and Autonomous Multi-Agent Workflows 2025"

    run_research_pipeline(topic_input)