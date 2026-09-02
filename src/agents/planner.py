"""Planner Agent: Decomposes a research topic into targeted sub-queries."""

import logging
from langchain_core.prompts import ChatPromptTemplate
from src.agents.llm import get_llm
from src.state import SubQueryPlan

logger = logging.getLogger(__name__)

PLANNER_SYSTEM_PROMPT = """You are a Principal AI Research Architect and Information Strategist.
Your mission is to break down a research topic into 3 distinct, high-impact search queries.

Each query must target a specific angle:
1. Foundational Architecture & Core Mechanisms
2. State-of-the-Art (SOTA) Breakthroughs & Recent Developments (2024-2026)
3. Technical Limitations, Production Challenges, Benchmarks & Future Trajectory

Make the search queries precise, keyword-rich, and optimized for search engines (avoid generic single-word queries)."""

planner_prompt = ChatPromptTemplate.from_messages([
    ("system", PLANNER_SYSTEM_PROMPT),
    ("human", "Decompose this research topic into 3 strategic search queries:\n\nTopic: {topic}")
])


def plan_sub_queries(topic: str) -> SubQueryPlan:
    """Generate structured sub-queries for research topic."""
    llm = get_llm(temperature=0.2)
    structured_llm = llm.with_structured_output(SubQueryPlan)
    chain = planner_prompt | structured_llm

    try:
        plan: SubQueryPlan = chain.invoke({"topic": topic})
        return plan
    except Exception as e:
        logger.warning("Structured output failed in planner, using fallback: %s", e)
        # Resilient fallback
        return SubQueryPlan(
            sub_queries=[
                f"{topic} architecture foundations overview",
                f"{topic} recent breakthroughs 2025 2026",
                f"{topic} challenges benchmarks limitations",
            ],
            rationale="Fallback decomposition covering foundations, recent progress, and challenges."
        )

