"""Curator Agent: Selects top authority sources and scrapes full content."""

import logging
from typing import List, Dict, Any
from src.tools.scraper import extract_web_content

logger = logging.getLogger(__name__)


def curate_and_scrape(search_results: List[Dict[str, Any]], max_urls: int = 2) -> List[Dict[str, Any]]:
    """Select the highest-quality distinct sources and scrape deep text content."""
    scraped_sources: List[Dict[str, Any]] = []

    # Pick up to max_urls distinct valid URLs
    candidate_urls = []
    seen = set()
    for item in search_results:
        url = item.get("url")
        if url and url.startswith("http") and url not in seen:
            seen.add(url)
            candidate_urls.append(item)
            if len(candidate_urls) >= max_urls:
                break

    for candidate in candidate_urls:
        url = candidate["url"]
        logger.info("Curator scraping deep content from: %s", url)
        data = extract_web_content(url, max_chars=3500)
        scraped_sources.append({
            "title": data.get("title") or candidate.get("title", "Web Source"),
            "url": url,
            "content": data.get("content", ""),
        })

    return scraped_sources

