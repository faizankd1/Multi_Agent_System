"""Writer Agent: Synthesizes multi-source research into an executive-grade report."""

import logging
from typing import List, Dict, Any, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.agents.llm import get_llm

logger = logging.getLogger(__name__)

WRITER_SYSTEM_PROMPT = """You are a Lead AI Research Analyst and Technical Author.
Your mission is to synthesize multi-source research findings into a comprehensive, authoritative, publication-ready research report.

Report Requirements:
1. # Executive Summary (High-level synthesis with key breakthroughs)
2. ## Architectural & Technical Foundations (Deep technical mechanisms)
3. ## Current Breakthroughs & State-of-the-Art (Real-world examples, benchmarks)
4. ## Production Challenges, Trade-offs & Limitations (Critical, balanced analysis)
5. ## Strategic Outlook & Future Directions (Where the field is headed)
6. ## Verified Sources & References (Numbered list of URLs with brief descriptions)

Formatting Guidelines:
- Use clean GitHub-flavored markdown with clear headers, bullet points, and callout quotes where relevant.
- Attribute insights by referencing source URLs inline e.g. `([Domain](URL))`.
- Ensure technical depth, factual accuracy, and high informational density."""

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", WRITER_SYSTEM_PROMPT),
    ("human", """Synthesize a detailed research report on the following topic.

Topic: {topic}

Search Highlights:
{search_summary}

Deep Web Scrapes:
{scraped_content}

{revision_context}

Draft the complete, polished report now.""")
])


def write_research_report(
    topic: str,
    search_results: List[Dict[str, Any]],
    scraped_sources: List[Dict[str, Any]],
    revision_count: int = 0,
    critic_notes: Optional[List[str]] = None,
) -> str:
    """Generate or revise research report with optional critique feedback incorporated."""
    llm = get_llm(temperature=0.3)
    chain = writer_prompt | llm | StrOutputParser()

    # Format search snippets
    search_lines = []
    for s in search_results[:6]:
        search_lines.append(f"- [{s.get('title', 'Source')}]({s.get('url', '')}): {s.get('content', '')[:250]}")
    search_summary = "\n".join(search_lines) if search_lines else "No search snippets available."

    # Format scraped text
    scraped_lines = []
    for sc in scraped_sources:
        scraped_lines.append(f"### Source: {sc.get('title')} ({sc.get('url')})\n{sc.get('content', '')[:2500]}")
    scraped_content = "\n\n".join(scraped_lines) if scraped_lines else "No scraped body text available."

    # Revision instructions if this is a revision loop
    if revision_count > 0 and critic_notes:
        notes_str = "\n".join(f"- {note}" for note in critic_notes)
        revision_context = f"""IMPORTANT - REVISION #{revision_count} INSTRUCTIONS:
The Critic agent evaluated the previous draft and identified the following deficiencies:
{notes_str}

You MUST explicitly resolve every item listed above to elevate this report to a top-tier score."""
    else:
        revision_context = "This is the initial draft. Deliver thorough, first-class depth and structure."

    logger.info("Writer synthesizing report for '%s' (Revision: %d)", topic, revision_count)
    report = chain.invoke({
        "topic": topic,
        "search_summary": search_summary,
        "scraped_content": scraped_content,
        "revision_context": revision_context,
    })
    return report

