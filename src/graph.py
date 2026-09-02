"""LangGraph Multi-Agent Workflow Engine with Conditional Reflection Loops."""

import time
import logging
from typing import Literal, Dict, Any
from langgraph.graph import StateGraph, START, END
from src.state import ResearchState, TimelineEvent
from src.config import settings
from src.agents.planner import plan_sub_queries
from src.agents.researcher import execute_research_plan
from src.agents.curator import curate_and_scrape
from src.agents.writer import write_research_report
from src.agents.critic import review_research_report

logger = logging.getLogger(__name__)


def plan_node(state: ResearchState) -> Dict[str, Any]:
    """Execute Planner Agent node to decompose research topic."""
    start_time = time.time()
    topic = state.get("topic", "")
    logger.info("[Node: Planner] Generating search angles for: %s", topic)

    plan = plan_sub_queries(topic)
    duration = time.time() - start_time

    event = TimelineEvent(
        node="planner",
        stage="Query Planning",
        timestamp=start_time,
        duration_seconds=round(duration, 2),
        details=f"Generated {len(plan.sub_queries)} strategic queries: {', '.join(plan.sub_queries)}"
    ).model_dump()

    timeline = list(state.get("timeline", []))
    timeline.append(event)

    return {
        "sub_queries": plan.sub_queries,
        "current_node": "planner",
        "timeline": timeline,
    }


def research_node(state: ResearchState) -> Dict[str, Any]:
    """Execute Researcher Agent node to query Tavily."""
    start_time = time.time()
    sub_queries = state.get("sub_queries", [state.get("topic", "")])
    logger.info("[Node: Researcher] Executing search across %d queries", len(sub_queries))

    results = execute_research_plan(sub_queries)
    duration = time.time() - start_time

    event = TimelineEvent(
        node="researcher",
        stage="Multi-Query Search",
        timestamp=start_time,
        duration_seconds=round(duration, 2),
        details=f"Retrieved {len(results)} verified source snippets across web search"
    ).model_dump()

    timeline = list(state.get("timeline", []))
    timeline.append(event)

    return {
        "search_results": results,
        "current_node": "researcher",
        "timeline": timeline,
    }


def curate_node(state: ResearchState) -> Dict[str, Any]:
    """Execute Curator Agent node to scrape top authority resources."""
    start_time = time.time()
    search_results = state.get("search_results", [])
    logger.info("[Node: Curator] Curating and scraping top resources")

    scraped = curate_and_scrape(search_results, max_urls=2)
    duration = time.time() - start_time

    event = TimelineEvent(
        node="curator",
        stage="Deep Content Extraction",
        timestamp=start_time,
        duration_seconds=round(duration, 2),
        details=f"Extracted full body text from {len(scraped)} authority domains"
    ).model_dump()

    timeline = list(state.get("timeline", []))
    timeline.append(event)

    return {
        "scraped_sources": scraped,
        "current_node": "curator",
        "timeline": timeline,
    }


def write_node(state: ResearchState) -> Dict[str, Any]:
    """Execute Writer Agent node to synthesize or revise research report."""
    start_time = time.time()
    topic = state.get("topic", "")
    search_results = state.get("search_results", [])
    scraped_sources = state.get("scraped_sources", [])
    revision_count = state.get("revision_count", 0)
    revision_notes = state.get("revision_notes", [])

    logger.info("[Node: Writer] Synthesizing report (Revision #%d)", revision_count)
    report = write_research_report(
        topic=topic,
        search_results=search_results,
        scraped_sources=scraped_sources,
        revision_count=revision_count,
        critic_notes=revision_notes,
    )
    duration = time.time() - start_time

    event = TimelineEvent(
        node="writer",
        stage=f"Report Synthesis (Draft #{revision_count + 1})",
        timestamp=start_time,
        duration_seconds=round(duration, 2),
        details=f"Authored {len(report.split())} words with citations and structured sections"
    ).model_dump()

    timeline = list(state.get("timeline", []))
    timeline.append(event)

    return {
        "draft_report": report,
        "current_node": "writer",
        "timeline": timeline,
    }


def critique_node(state: ResearchState) -> Dict[str, Any]:
    """Execute Critic Agent node to evaluate draft using structured Pydantic schema."""
    start_time = time.time()
    topic = state.get("topic", "")
    report = state.get("draft_report", "")
    current_revisions = state.get("revision_count", 0)

    logger.info("[Node: Critic] Evaluating report quality and factual depth")
    review = review_research_report(topic=topic, report=report)
    duration = time.time() - start_time

    review_dict = review.model_dump()
    new_revision_count = current_revisions + 1

    event = TimelineEvent(
        node="critic",
        stage=f"Quality Audit (Score: {review.score}/10)",
        timestamp=start_time,
        duration_seconds=round(duration, 2),
        details=f"Passed: {review.passed}. Score: {review.score}/10. {review.verdict}"
    ).model_dump()

    timeline = list(state.get("timeline", []))
    timeline.append(event)

    return {
        "critic_review": review_dict,
        "revision_count": new_revision_count,
        "revision_notes": review.actionable_recommendations,
        "current_node": "critic",
        "timeline": timeline,
    }


def should_revise(state: ResearchState) -> Literal["write_report", "end"]:
    """Conditional Edge: Determines if report requires reflection and revision."""
    review = state.get("critic_review") or {}
    passed = review.get("passed", False)
    score = review.get("score", 0)
    rev_count = state.get("revision_count", 0)

    logger.info("Conditional evaluation: score=%d, passed=%s, revisions=%d/%d",
                score, passed, rev_count, settings.max_revisions)

    # If it passes quality threshold or reached maximum allowed revisions, conclude
    if passed or rev_count >= settings.max_revisions:
        logger.info("Report approved or max revisions reached. Exiting workflow.")
        return "end"

    # Otherwise route back to writer for targeted revision
    logger.info("Quality criteria not met (score %d < %d). Triggering revision loop.",
                score, settings.pass_score_threshold)
    return "write_report"


def build_research_graph() -> Any:
    """Build and compile the LangGraph StateGraph."""
    workflow = StateGraph(ResearchState)

    # Register nodes
    workflow.add_node("plan_queries", plan_node)
    workflow.add_node("research", research_node)
    workflow.add_node("curate_content", curate_node)
    workflow.add_node("write_report", write_node)
    workflow.add_node("critique_report", critique_node)

    # Wire edges
    workflow.add_edge(START, "plan_queries")
    workflow.add_edge("plan_queries", "research")
    workflow.add_edge("research", "curate_content")
    workflow.add_edge("curate_content", "write_report")
    workflow.add_edge("write_report", "critique_report")

    # Conditional reflection edge
    workflow.add_conditional_edges(
        "critique_report",
        should_revise,
        {
            "write_report": "write_report",
            "end": END,
        }
    )

    return workflow.compile()


# Singleton compiled graph
research_app = build_research_graph()

