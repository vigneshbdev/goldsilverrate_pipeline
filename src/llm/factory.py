from src.llm.base import BaseLLM
from src.llm.config import LLMConfig
from src.llm.providers.openai_provider import OpenAICompatibleProvider


class LLMFactory:

    @staticmethod
    def create() -> BaseLLM:

        config = LLMConfig.get_provider_config()

        return OpenAICompatibleProvider(
            base_url=config["base_url"],
            api_key=config["api_key"],
            model=config["model"],
        )