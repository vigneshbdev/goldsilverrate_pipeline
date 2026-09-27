import os
from dotenv import load_dotenv

load_dotenv()


class LLMConfig:

    @staticmethod
    def provider() -> str:
        return os.getenv("LLM_PROVIDER", "openrouter").lower()

    @staticmethod
    def model() -> str:
        return os.getenv("LLM_MODEL", "openrouter/free")

    @staticmethod
    def get_provider_config() -> dict:

        provider = LLMConfig.provider()

        if provider == "openrouter":
            return {
                "base_url": os.getenv("OPENROUTER_BASE_URL"),
                "api_key": os.getenv("OPENROUTER_API_KEY"),
                "model": LLMConfig.model(),
            }

        if provider == "openai":
            return {
                "base_url": os.getenv(
                    "OPENAI_BASE_URL",
                    "https://api.openai.com/v1"
                ),
                "api_key": os.getenv("OPENAI_API_KEY"),
                "model": LLMConfig.model(),
            }

        if provider == "ollama":
            return {
                "base_url": os.getenv(
                    "OLLAMA_BASE_URL",
                    "http://localhost:11434/v1"
                ),
                "api_key": os.getenv(
                    "OLLAMA_API_KEY",
                    "ollama"
                ),
                "model": LLMConfig.model(),
            }

        if provider == "groq":
            return {
                "base_url": os.getenv(
                    "GROQ_BASE_URL",
                    "https://api.groq.com/openai/v1"
                ),
                "api_key": os.getenv("GROQ_API_KEY"),
                "model": LLMConfig.model(),
            }

        if provider == "grok":
                return {
                        "base_url": os.getenv(
                            "GROK_BASE_URL",
                            "https://api.x.ai/v1/responses"
                        ),
                        "api_key": os.getenv("GROK_API_KEY"),
                        "model": LLMConfig.model(),
                    }

        raise ValueError(
            f"Unsupported LLM provider: {provider}"
        )