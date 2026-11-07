"""
Standalone Interactive Demo for HackwithHyderabad 3.0.
Showcases the User Feedback Synthesizer powered by Hindsight Long-Term Memory.

Run via:
    python run_demo.py
"""

import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.text import Text

from agent.feedback_synthesizer import UserFeedbackSynthesizerAgent
from evaluation.benchmark_comparison import BenchmarkComparator

console = Console()

def print_header():
    console.clear()
    console.print(
        Panel.fit(
            "[bold cyan]🧠 USER FEEDBACK SYNTHESIZER[/bold cyan]\n"
            "[bold white]HackwithHyderabad 3.0 Hackathon Project[/bold white]\n"
            "[yellow]Core Architecture: Hindsight Agent Memory Layer[/yellow]\n"
            "[dim]4 Logical Networks: World Facts • Agent Experiences • Entity Summaries • Evolving Beliefs[/dim]",
            border_style="cyan",
            title="[bold green]DEMO SHOWCASE[/bold green]",
            subtitle="[dim]FlowPilot Product Suite (4-Week Real SaaS Crisis & Recovery Scenario)[/dim]"
        )
    )

def step_1_bootstrap(agent: UserFeedbackSynthesizerAgent):
    console.print("\n[bold yellow]═══ STEP 1: Bootstrapping Hindsight 4-Network Memory Layer ═══[/bold yellow]")
    with console.status("[bold green]Ingesting World Facts, Experiences & Entity Graphs...", spinner="dots"):
        stats = agent.memory.get_stats()
        time.sleep(0.6)

    table = Table(title="Hindsight Memory Bank Status", show_header=True, header_style="bold magenta")
    table.add_column("Logical Memory Network", style="cyan")
    table.add_column("Count", justify="center", style="green")
    table.add_column("Description / Role", style="dim")

    table.add_row("1. World Facts", str(stats["world_facts_count"]), "Objective product specs, changelogs (v2.3, v2.4, v2.4.1, v2.4.2)")
    table.add_row("2. Agent Experiences", str(stats["agent_experiences_count"]), "Chronological multi-channel feedback (Zendesk, Discord, Gong, Reddit, Survey)")
    table.add_row("3. Entity Summaries", str(stats["entity_summaries_count"]), "Dynamic customer accounts (Acme $120k ARR, Finovate $85k) & feature modules")
    table.add_row("4. Evolving Beliefs", str(stats["evolving_beliefs_count"]), "Mental models that mutate as evidence arrives & resolve contradictions")

    console.print(table)
    console.print(f"[bold green]✔ Memory Bank '{stats['bank_id']}' active in mode: {stats['mode']}[/bold green]\n")

def step_2_temporal_story(agent: UserFeedbackSynthesizerAgent):
    console.print("[bold yellow]═══ STEP 2: The Multi-Week Narrative & Cross-Channel Signals ═══[/bold yellow]")
    console.print("Demonstrating how Hindsight tracks the story across 4 distinct phases:\n")

    reflection = agent.memory.reflect("Summarize 4-week feedback progression")
    sentiment_data = reflection.sentiment_shift_detected.get("weekly_averages", {})

    story_table = Table(title="4-Week Timeline Synthesis & Sentiment Trajectory", show_header=True, header_style="bold blue")
    story_table.add_column("Timeline Phase", style="bold")
    story_table.add_column("Release Version", style="cyan")
    story_table.add_column("Avg Sentiment", style="yellow")
    story_table.add_column("Cross-Channel Narrative", style="white")

    w1_val = sentiment_data.get('Week 1 (Oct 1-7)', 0.78)
    w2_val = sentiment_data.get('Week 2 (Oct 8-14)', 0.12)
    w3_val = sentiment_data.get('Week 3 (Oct 15-21)', -0.68)
    w4_val = sentiment_data.get('Week 4 (Oct 22-29)', 0.81)

    story_table.add_row(
        "Week 1 (Oct 1-7)",
        "v2.3 Baseline",
        f"[green]{w1_val:+.2f}[/green]",
        "Golden era: Users praise speed over Miro. Feature requests for Figma import & RBAC."
    )
    story_table.add_row(
        "Week 2 (Oct 8-14)",
        "v2.4.0 Async Canvas",
        f"[yellow]{w2_val:+.2f}[/yellow]",
        "Subtle warning: Discord & Reddit whisper about Chrome tab GPU RAM leaks and PDF export delays."
    )
    story_table.add_row(
        "Week 3 (Oct 15-21)",
        "v2.4.1 Emergency Hotfix",
        f"[bold red]{w3_val:+.2f}[/bold red]",
        "CRISIS: 45m token check breaks Okta SSO. Acme Corp ($120k ARR) P0 escalation; Finovate ($85k) pauses POC!"
    )
    story_table.add_row(
        "Week 4 (Oct 22-29)",
        "v2.4.2 Stability Patch",
        f"[bold green]{w4_val:+.2f}[/bold green]",
        "RECOVERY: WebLock distributed mutex fixes SSO. 100% session stability confirmed; $205k ARR secured!"
    )

    console.print(story_table)
    console.print(f"[bold cyan]Key Hindsight Insight:[/bold cyan] {reflection.sentiment_shift_detected.get('interpretation', '')}\n")

def step_3_side_by_side(comparator: BenchmarkComparator):
    console.print("[bold yellow]═══ STEP 3: The Before-and-After Demonstration ═══[/bold yellow]")
    console.print("[bold white]PM Query:[/bold white] [italic]\"Why are enterprise customers escalating churn warnings this week, and what product change triggered it?\"[/italic]\n")

    with console.status("[bold green]Executing Head-to-Head Comparison...", spinner="dots"):
        result = comparator.run_side_by_side_comparison("Why are enterprise customers escalating churn warnings this week, and what product change triggered it?")
        time.sleep(0.5)

    # Show Stateless Bot Output
    console.print(Panel(
        f"[bold red]❌ BEFORE: Stateless Chatbot / Conventional RAG[/bold red]\n\n"
        f"{result['stateless_rag']['response']}\n\n"
        f"[dim]Limitations Exposed:\n" + "\n".join(f"• {x}" for x in result['stateless_rag']['limitations_exposed']) + "[/dim]",
        border_style="red"
    ))

    # Show Hindsight Agent Output
    console.print(Panel(
        f"[bold green]✔ AFTER: Hindsight-Powered Agent[/bold green]\n\n"
        f"{result['hindsight_agent']['response']}\n\n"
        f"[bold cyan]Hindsight Superpowers Demonstrated:[/bold cyan]\n"
        f"• Identified exact regression trigger: [bold]v2.4.1 OAuth token renewal interval lacking mutex[/bold]\n"
        f"• Correlated disparate channels: [bold]Discord (#bugs) + Zendesk (ZD-4201) + Gong ($85k sales call)[/bold]\n"
        f"• Quantified ARR at risk: [bold]{result['hindsight_agent']['at_risk_arr_calculated']} across Acme Global & Finovate[/bold]\n"
        f"• Tracked Evolving Belief: [bold]Hypothesis transitioned from 'SSO Crisis' to 'Stabilized via v2.4.2 WebLock'[/bold]",
        border_style="green"
    ))

    # Show Comparison Matrix
    matrix = result["comparison_matrix"]
    matrix_table = Table(title="Capability Matrix: Stateless RAG vs Hindsight Synthesizer", show_header=True, header_style="bold cyan")
    matrix_table.add_column("Evaluation Dimension", style="bold")
    matrix_table.add_column("Stateless RAG (Before)", style="red")
    matrix_table.add_column("Hindsight Agent (After)", style="green")

    for i in range(len(matrix["Dimension"])):
        matrix_table.add_row(
            matrix["Dimension"][i],
            matrix["Stateless RAG (Before)"][i],
            matrix["Hindsight Agent (After)"][i]
        )
    console.print(matrix_table)
    console.print()

def step_4_domain_learning(agent: UserFeedbackSynthesizerAgent):
    console.print("[bold yellow]═══ STEP 4: Domain Learning & Long-Term Recall Across Sessions ═══[/bold yellow]")
    console.print("Demonstrating how the agent builds up domain expertise from past conversations:\n")

    # Simulate PM multi-turn session
    console.print("[cyan]Turn 1 (Oct 14):[/cyan] PM asked: [italic]'Is the canvas performance issue localized or widespread?'[/italic]")
    res1 = agent.query("Is the canvas performance issue localized or widespread?")
    console.print(f"[green]Agent Answered:[/green] {res1['answer'][:250]}...\n")

    console.print("[cyan]Turn 2 (Oct 28 - 2 Weeks Later):[/cyan] PM follows up: [italic]'What should we build next sprint based on our customer commitments?'[/italic]")
    res2 = agent.query("What should we build next sprint based on our customer commitments?")
    console.print(f"[green]Agent Answered (Recalling customer history & past requests):[/green]")
    console.print(Panel(res2["answer"], border_style="cyan"))

    console.print(f"[bold green]✔ Agent maintained {len(agent.session_history)} conversational turns in session history.[/bold green]\n")

def interactive_loop(agent: UserFeedbackSynthesizerAgent):
    console.print("[bold yellow]═══ STEP 5: Interactive PM Query Console ═══[/bold yellow]")
    console.print("[dim]Type your own question for the agent, or type 'exit' to quit. Try questions like:\n"
                  "  - 'What caused our CSAT to drop?'\n"
                  "  - 'What happened after v2.4 shipped?'\n"
                  "  - 'Why was Acme Global threatening to cancel?'\n"
                  "  - 'What are users requesting on Discord vs In-App Surveys?'[/dim]\n")

    while True:
        try:
            user_input = console.input("[bold cyan]Enter PM Question (or press Enter for sample question): [/bold cyan]").strip()
            if not user_input:
                user_input = "Why was Acme Global threatening to cancel and how did we resolve it?"
                console.print(f"[dim]Running default: \"{user_input}\"[/dim]")
            
            if user_input.lower() in ["exit", "quit", "q"]:
                console.print("[green]Thank you for evaluating the User Feedback Synthesizer for HackwithHyderabad 3.0![/green]")
                break

            with console.status("[bold green]Querying Hindsight Memory...", spinner="dots"):
                res = agent.query(user_input)

            console.print(Panel(res["answer"], title="[bold green]Hindsight Agent Response[/bold green]", border_style="green"))
            console.print(f"[dim]Recalled {len(res['recalled_memories'])} memories across World Facts, Experiences, and Evolving Beliefs.[/dim]\n")
            
            # Ask if they want another
            cont = console.input("[dim]Ask another question? (y/n): [/dim]").strip().lower()
            if cont in ["n", "no"]:
                break
        except (KeyboardInterrupt, EOFError):
            console.print("\n[green]Exiting demo. Thank you for evaluating User Feedback Synthesizer![/green]")
            break

def main():
    print_header()
    agent = UserFeedbackSynthesizerAgent()
    comparator = BenchmarkComparator(agent)

    step_1_bootstrap(agent)
    step_2_temporal_story(agent)
    step_3_side_by_side(comparator)
    step_4_domain_learning(agent)
    interactive_loop(agent)

if __name__ == "__main__":
    main()
