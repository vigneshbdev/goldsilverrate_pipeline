from openai import OpenAI
from src.llm.base import BaseLLM


class OpenAICompatibleProvider(BaseLLM):

    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: str
    ):
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )
        self.model = model

    def chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None
    ):
        kwargs = {
            "model": self.model,
            "messages": messages,
        }

        if tools:
            kwargs["tools"] = tools

        return self.client.chat.completions.create(
            **kwargs
        )

    def parse(
        self,
        messages: list[dict],
        response_format,
        tools: list[dict] | None = None
    ):
        kwargs = {
            "model": self.model,
            "messages": messages,
            "response_format": response_format,
        }

        if tools:
            kwargs["tools"] = tools

        return self.client.chat.completions.parse(
            **kwargs
        )