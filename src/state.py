"""State definitions and Pydantic schemas for the Multi-Agent System."""

from typing import Dict, List, Optional, Any
from typing_extensions import TypedDict
from pydantic import BaseModel, Field


class SubQueryPlan(BaseModel):
    """Pydantic schema for query decomposition by the Planner Agent."""

    sub_queries: List[str] = Field(
        ...,
        min_length=2,
        max_length=4,
        description="List of 2-4 distinct, targeted search queries covering different facets of the topic."
    )
    rationale: str = Field(
        ...,
        description="Brief explanation of why these queries provide comprehensive coverage."
    )


class CriticReview(BaseModel):
    """Structured Pydantic review produced by the Critic Agent."""

    score: int = Field(
        ...,
        ge=1,
        le=10,
        description="Overall research report quality score from 1 to 10."
    )
    factual_accuracy: int = Field(
        ...,
        ge=1,
        le=10,
        description="Factual consistency and reliability score."
    )
    depth_and_coverage: int = Field(
        ...,
        ge=1,
        le=10,
        description="Depth of explanation and comprehensive coverage score."
    )
    structure_and_clarity: int = Field(
        ...,
        ge=1,
        le=10,
        description="Logical flow, markdown formatting, and readability score."
    )
    citation_quality: int = Field(
        ...,
        ge=1,
        le=10,
        description="Relevance and attribution of source URLs score."
    )
    strengths: List[str] = Field(
        default_factory=list,
        description="Key strengths and high-quality sections identified."
    )
    weaknesses: List[str] = Field(
        default_factory=list,
        description="Gaps, unclear points, or missing evidence in the report."
    )
    actionable_recommendations: List[str] = Field(
        default_factory=list,
        description="Concrete instructions for the Writer to improve the report in revision."
    )
    passed: bool = Field(
        ...,
        description="True if score >= 8 and meets publication standard; False if revision is needed."
    )
    verdict: str = Field(
        ...,
        description="Executive one-line summary verdict."
    )


class TimelineEvent(BaseModel):
    """Event logged in the execution timeline for telemetry and UI visualization."""

    node: str
    stage: str
    timestamp: float
    duration_seconds: float = 0.0
    status: str = "completed"
    details: Optional[str] = None


class ResearchState(TypedDict, total=False):
    """LangGraph execution state passed across agents."""

    topic: str
    sub_queries: List[str]
    search_results: List[Dict[str, Any]]
    scraped_sources: List[Dict[str, Any]]
    draft_report: str
    critic_review: Optional[Dict[str, Any]]
    revision_count: int
    revision_notes: List[str]
    current_node: str
    timeline: List[Dict[str, Any]]
    error: Optional[str]

