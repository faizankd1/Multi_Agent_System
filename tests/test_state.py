"""Unit tests for state models and Pydantic validation schemas."""

import pytest
from pydantic import ValidationError
from src.state import SubQueryPlan, CriticReview


def test_sub_query_plan_valid():
    """Verify valid query plan construction."""
    plan = SubQueryPlan(
        sub_queries=[
            "agent architectures 2025",
            "langgraph stateful workflows",
            "self-correcting reflection loops"
        ],
        rationale="Covers architecture, workflow engine, and reflection patterns."
    )
    assert len(plan.sub_queries) == 3
    assert "agent" in plan.sub_queries[0]


def test_sub_query_plan_invalid_bounds():
    """Verify bounds enforcement on sub-queries count."""
    with pytest.raises(ValidationError):
        # Must have at least 2 queries
        SubQueryPlan(sub_queries=["only one query"], rationale="too short")


def test_critic_review_valid():
    """Verify structured critic review model constraints."""
    review = CriticReview(
        score=9,
        factual_accuracy=9,
        depth_and_coverage=8,
        structure_and_clarity=9,
        citation_quality=9,
        strengths=["Comprehensive citations", "Clear executive summary"],
        weaknesses=[],
        actionable_recommendations=[],
        passed=True,
        verdict="Exemplary report meeting publication standards."
    )
    assert review.score == 9
    assert review.passed is True


def test_critic_review_score_out_of_bounds():
    """Verify score is constrained between 1 and 10."""
    with pytest.raises(ValidationError):
        CriticReview(
            score=15,  # Invalid: > 10
            factual_accuracy=10,
            depth_and_coverage=10,
            structure_and_clarity=10,
            citation_quality=10,
            passed=True,
            verdict="Invalid score"
        )

