"""Web content extraction tool using BeautifulSoup with resilient filtering."""

import logging
from typing import Dict, Any
import requests
from bs4 import BeautifulSoup
from langchain.tools import tool
from src.config import settings

logger = logging.getLogger(__name__)


def extract_web_content(url: str, max_chars: int = 4000) -> Dict[str, str]:
    """Fetch and parse clean textual content from target URL."""
    headers = {"User-Agent": settings.user_agent}
    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=settings.request_timeout,
            allow_redirects=True,
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract title
        page_title = soup.title.string.strip() if soup.title and soup.title.string else url

        # Remove clutter, scripts, styles, navigation, footer, forms, ads
        unwanted_tags = [
            "script", "style", "nav", "footer", "header",
            "aside", "form", "noscript", "svg", "iframe",
        ]
        for tag in soup(unwanted_tags):
            tag.decompose()

        # Prioritize main article tags if available
        article = soup.find("article") or soup.find("main") or soup.body
        if not article:
            return {"url": url, "title": page_title, "content": "No readable content found."}

        text = article.get_text(separator=" ", strip=True)
        # Clean excessive whitespace
        cleaned_text = " ".join(text.split())

        return {
            "url": url,
            "title": page_title,
            "content": cleaned_text[:max_chars],
        }

    except requests.exceptions.RequestException as e:
        logger.warning("Failed to fetch %s: %s", url, e)
        return {"url": url, "title": "Fetch Failed", "content": f"Failed to retrieve URL: {str(e)}"}
    except Exception as e:
        logger.warning("Failed to parse %s: %s", url, e)
        return {"url": url, "title": "Parse Failed", "content": f"Parse error: {str(e)}"}


@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper analysis."""
    result = extract_web_content(url, max_chars=settings.max_scrape_length)
    return f"Source: {result['title']} ({result['url']})\nContent: {result['content']}"
