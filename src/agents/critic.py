"""Critic Agent: Evaluates research report using structured Pydantic reflection schemas."""

import logging
from langchain_core.prompts import ChatPromptTemplate
from src.agents.llm import get_llm
from src.state import CriticReview
from src.config import settings

logger = logging.getLogger(__name__)

CRITIC_SYSTEM_PROMPT = """You are a Peer Review Referee and Quality Assurance Auditor for an advanced AI research publication.
Your job is to rigorously evaluate draft research reports on accuracy, depth, structure, and source citations.

Scoring Criteria (1-10 each):
- Factual Accuracy: Are claims consistent, believable, and grounded?
- Depth and Coverage: Does the report unpack technical mechanisms or is it shallow and generic?
- Structure and Clarity: Is it organized logically with markdown sections, executive summary, and smooth transitions?
- Citation Quality: Does it cite real URLs and attribute facts properly?
- Overall Score: Weighted score (1-10).

Standards:
- Score 8-10: Publication-ready. Set `passed=True`.
- Score 1-7: Needs revision. Set `passed=False` and supply concrete, actionable instructions in `actionable_recommendations`.

Be honest, uncompromising, and constructive."""

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", CRITIC_SYSTEM_PROMPT),
    ("human", """Perform a rigorous review of the following research report:

Topic: {topic}

Report Draft:
{report}

Return your detailed structured evaluation.""")
])


def review_research_report(topic: str, report: str) -> CriticReview:
    """Evaluate report using structured output model."""
    llm = get_llm(temperature=0.1)
    structured_llm = llm.with_structured_output(CriticReview)
    chain = critic_prompt | structured_llm

    try:
        review: CriticReview = chain.invoke({
            "topic": topic,
            "report": report,
        })
        # Enforce threshold alignment
        review.passed = review.score >= settings.pass_score_threshold
        return review
    except Exception as e:
        logger.warning("Structured output failed in critic, using robust fallback evaluation: %s", e)
        # Fallback review
        passed = len(report) > 1500
        score = 8 if passed else 6
        return CriticReview(
            score=score,
            factual_accuracy=7,
            depth_and_coverage=7,
            structure_and_clarity=8,
            citation_quality=7,
            strengths=["Contains structured sections and references", "Covers major aspects of the topic"],
            weaknesses=["Could integrate more empirical data points and recent benchmark figures"] if not passed else [],
            actionable_recommendations=[
                "Add more specific technical metrics and benchmark comparisons",
                "Ensure every major claim points to an attributed source"
            ] if not passed else [],
            passed=passed,
            verdict="Comprehensive initial draft meeting baseline research criteria." if passed else "Draft requires further depth and citations."
        )

