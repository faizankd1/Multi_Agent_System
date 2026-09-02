"""Tavily search tool integration with deduplication and error resilience."""

import logging
from typing import List, Dict, Any
from tavily import TavilyClient
from langchain.tools import tool
from src.config import settings

logger = logging.getLogger(__name__)


def get_tavily_client() -> TavilyClient:
    """Instantiate TavilyClient using configured API key."""
    api_key = settings.tavily_api_key
    if not api_key:
        raise ValueError("TAVILY_API_KEY is not set in environment or .env file.")
    return TavilyClient(api_key=api_key)


def search_tavily(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """Execute search query against Tavily API with structured return."""
    try:
        client = get_tavily_client()
        response = client.search(
            query=query,
            max_results=max_results,
            search_depth="advanced",
            include_answer=True,
        )
        raw_results = response.get("results", [])
        clean_results = []
        seen_urls = set()

        for item in raw_results:
            url = item.get("url", "")
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)
            clean_results.append({
                "title": item.get("title", "Untitled Source"),
                "url": url,
                "content": item.get("content", "")[:600],
                "score": item.get("score", 0.0),
            })

        return clean_results
    except Exception as e:
        logger.error("Tavily search failed for query '%s': %s", query, e)
        return []


@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information. Returns formatted titles, URLs, and snippets."""
    results = search_tavily(query, max_results=settings.max_search_results)
    if not results:
        return f"No search results found for: {query}"

    formatted = []
    for r in results:
        formatted.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content']}"
        )
    return "\n\n---\n\n".join(formatted)

