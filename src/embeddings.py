from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from config import ModelConfig


def create_embeddings(config: ModelConfig):
    if config.provider == "openai":
        return OpenAIEmbeddings(model=config.embedding_model)

    if config.provider == "gemini":
        return GoogleGenerativeAIEmbeddings(model=config.embedding_model)

    if config.provider == "ollama":
        return GoogleGenerativeAIEmbeddings(model=config.embedding_model)

    raise ValueError(f"Unsupported provider: {config.provider}")