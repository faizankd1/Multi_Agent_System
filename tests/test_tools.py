"""Unit tests for search and scraping tools."""

import pytest
from unittest.mock import patch, MagicMock
from src.tools.scraper import extract_web_content
from src.tools.search import search_tavily


def test_extract_web_content_success():
    """Verify HTML cleaning, title extraction, and script stripping."""
    html_sample = """
    <html>
        <head><title>Quantum Computing Breakthrough</title></head>
        <body>
            <nav><a href="/home">Nav Link</a></nav>
            <script>console.log("ads");</script>
            <main>
                <h1>Quantum Supremacy</h1>
                <p>Researchers have developed a new 100-qubit processor with high coherence.</p>
            </main>
            <footer>Copyright 2025</footer>
        </body>
    </html>
    """

    mock_resp = MagicMock()
    mock_resp.text = html_sample
    mock_resp.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_resp):
        result = extract_web_content("https://example.com/quantum", max_chars=1000)

    assert result["url"] == "https://example.com/quantum"
    assert result["title"] == "Quantum Computing Breakthrough"
    assert "Nav Link" not in result["content"]
    assert "console.log" not in result["content"]
    assert "100-qubit processor" in result["content"]


def test_extract_web_content_failure():
    """Verify graceful error degradation on HTTP error."""
    import requests
    with patch("requests.get", side_effect=requests.exceptions.RequestException("Connection timed out")):
        result = extract_web_content("https://broken-link.org")

    assert result["title"] == "Fetch Failed"
    assert "Connection timed out" in result["content"]


def test_search_tavily_deduplication():
    """Verify search deduplicates identical URLs and formats correctly."""
    mock_client = MagicMock()
    mock_client.search.return_value = {
        "results": [
            {"title": "Doc 1", "url": "https://ai.org/paper1", "content": "Intro to agents", "score": 0.95},
            {"title": "Doc 1 Duplicate", "url": "https://ai.org/paper1", "content": "Duplicate", "score": 0.90},
            {"title": "Doc 2", "url": "https://ai.org/paper2", "content": "LangGraph guide", "score": 0.88},
        ]
    }

    with patch("src.tools.search.get_tavily_client", return_value=mock_client):
        results = search_tavily("agents", max_results=5)

    assert len(results) == 2
    assert results[0]["url"] == "https://ai.org/paper1"
    assert results[1]["url"] == "https://ai.org/paper2"
