"""Unit tests for LangGraph compilation and conditional routing logic."""

import pytest
from unittest.mock import patch, MagicMock
from src.graph import build_research_graph, should_revise
from src.state import ResearchState


def test_graph_compilation():
    """Verify that the StateGraph compiles cleanly without dangling edges."""
    app = build_research_graph()
    assert app is not None
    # Verify nodes exist in the compiled graph
    assert "plan_queries" in app.nodes
    assert "research" in app.nodes
    assert "curate_content" in app.nodes
    assert "write_report" in app.nodes
    assert "critique_report" in app.nodes


def test_should_revise_passes():
    """If review score passes threshold, routing should terminate at 'end'."""
    state: ResearchState = {
        "topic": "Testing",
        "critic_review": {"passed": True, "score": 9},
        "revision_count": 1,
    }
    decision = should_revise(state)
    assert decision == "end"


def test_should_revise_triggers_revision():
    """If review fails and revisions < max_revisions, route back to 'write_report'."""
    state: ResearchState = {
        "topic": "Testing",
        "critic_review": {"passed": False, "score": 5},
        "revision_count": 0,
    }
    decision = should_revise(state)
    assert decision == "write_report"


def test_should_revise_respects_max_revisions():
    """If review fails but max_revisions reached, route to 'end' to prevent infinite loop."""
    state: ResearchState = {
        "topic": "Testing",
        "critic_review": {"passed": False, "score": 6},
        "revision_count": 2,  # equals settings.max_revisions (2)
    }
    decision = should_revise(state)
    assert decision == "end"

