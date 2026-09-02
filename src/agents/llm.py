"""LLM factory initializing LangChain chat models with structured outputs."""

import os
from langchain_mistralai import ChatMistralAI
from src.config import settings


def get_llm(temperature: float = None) -> ChatMistralAI:
    """Return a configured ChatMistralAI instance."""
    api_key = settings.mistral_api_key or os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY is not configured in environment or .env file.")

    temp = temperature if temperature is not None else settings.temperature
    return ChatMistralAI(
        model=settings.model_name,
        api_key=api_key,
        temperature=temp,
    )

