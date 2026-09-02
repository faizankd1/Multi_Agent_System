"""Researcher Agent: Executes sub-queries across Tavily and aggregates verified sources."""

import logging
from typing import List, Dict, Any
from src.tools.search import search_tavily

logger = logging.getLogger(__name__)


def execute_research_plan(sub_queries: List[str]) -> List[Dict[str, Any]]:
    """Execute search across all planned sub-queries and deduplicate results."""
    aggregated_results: List[Dict[str, Any]] = []
    seen_urls = set()

    for query in sub_queries:
        logger.info("Executing search query: %s", query)
        results = search_tavily(query, max_results=3)

        for item in results:
            url = item.get("url")
            if url and url not in seen_urls:
                seen_urls.add(url)
                aggregated_results.append({
                    "query": query,
                    "title": item.get("title", ""),
                    "url": url,
                    "content": item.get("content", ""),
                    "score": item.get("score", 0.0),
                })

    logger.info("Aggregated %d unique search sources across %d queries", len(aggregated_results), len(sub_queries))
    return aggregated_results

