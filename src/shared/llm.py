import os
from functools import lru_cache

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama


@lru_cache(maxsize=None)
def get_google_llm(model: str = "gemini-1.5-pro", temperature: float = 0.0):
    return ChatGoogleGenerativeAI(
        model=model,
        temperature=temperature,
        google_api_key=os.environ["GOOGLE_API_KEY"],
    )


@lru_cache(maxsize=None)
def get_ollama_llm(model: str = "llama3.2:3b", temperature: float = 0.0):
    return ChatOllama(
        model=model,
        temperature=temperature,
        base_url=os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434"),
    )
