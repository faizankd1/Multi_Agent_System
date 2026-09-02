"""Configuration module for Multi-Agent Research System."""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """System-wide configuration settings."""

    # API Keys
    mistral_api_key: str = os.getenv("MISTRAL_API_KEY", "")
    tavily_api_key: str = os.getenv("TAVILY_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

    # Model configuration
    model_name: str = os.getenv("MISTRAL_MODEL", "mistral-small-latest")
    temperature: float = 0.2

    # Graph Execution
    max_search_results: int = 5
    max_scrape_length: int = 4000
    max_revisions: int = 2
    pass_score_threshold: int = 8  # Out of 10

    # Scraper config
    request_timeout: int = 10
    user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )


settings = Settings()

