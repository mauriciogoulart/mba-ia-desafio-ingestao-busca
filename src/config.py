from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class ModelConfig:
    provider: str
    embedding_model: str
    llm_model: str


class Settings:
    MODEL_PROVIDER: str = os.getenv("MODEL_PROVIDER", "openai").lower()
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    PG_VECTOR_COLLECTION_NAME: str = os.getenv("PG_VECTOR_COLLECTION_NAME", "documents")

    @staticmethod
    def model_config() -> ModelConfig:
        if Settings.MODEL_PROVIDER == "openai":
            return ModelConfig(
                provider="openai",
                embedding_model="text-embedding-3-small",
                llm_model="gpt-5-nano",
            )

        if Settings.MODEL_PROVIDER == "gemini":
            return ModelConfig(
                provider="gemini",
                embedding_model="models/embedding-001",
                llm_model="gemini-2.5-flash-lite",
            )

        if Settings.MODEL_PROVIDER == "ollama":
            return ModelConfig(
                provider="ollama",
                embedding_model="text-embedding-004",
                llm_model="llama3.2:3b",
            )

        raise ValueError(f"Unsupported MODEL_PROVIDER: {Settings.MODEL_PROVIDER}")