from langchain_community.chat_models import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from config import ModelConfig


def create_llm(config: ModelConfig):
    if config.provider == "openai":
        return ChatOpenAI(model=config.llm_model, temperature=0.1)

    if config.provider == "gemini":
        return ChatGoogleGenerativeAI(
            model=config.llm_model,
            temperature=0.1,
            convert_system_message_to_human=True,
        )

    if config.provider == "ollama":
        return ChatOllama(model=config.llm_model, 
            temperature=0.1,
            convert_system_message_to_human=True,
        )

    raise ValueError(f"Unsupported provider: {config.provider}")
