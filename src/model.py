from __future__ import annotations

from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import settings



def build_llm() -> ChatGoogleGenerativeAI:
    if not settings.google_api_key:
        raise ValueError("GOOGLE_API_KEY is missing. Add it in your .env file.")

    return ChatGoogleGenerativeAI(
        model=settings.model_name,
        google_api_key=settings.google_api_key,
        temperature=0.1,
    )
