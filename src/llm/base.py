from abc import abstractmethod, ABC
from typing import Type
from pydantic import BaseModel

class BaseLLM(ABC):

    @abstractmethod
    def chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None
    ):
        pass

    @abstractmethod
    def parse(
        self,
        messages: list[dict],
        response_format: Type[BaseModel],
        tools: list[dict] | None = None
    ):
        pass