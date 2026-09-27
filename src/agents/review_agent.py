from src.llm.base import BaseLLM
from src.llm.factory import LLMFactory

from src.models.post_data import PostData
class ReviewAgent:

    def __init__(self) -> None:
        self.llm: BaseLLM = LLMFactory.create()
        self.system_prompt = """
Consider yourself as a reviewer agent who will review the number of gold and silver rate provided by user

Gold Rate & Silver Rate should be a postive number
Difference should be any type of number like positive, negative or zero
respond only with true or false
"""

    def run(self, post_data: PostData):
        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role":"user",
                "content": post_data.model_dump_json()
            }
        ]

        reponse = self.llm.chat(messages=messages, tools=[])

        return reponse.choices[0].message.content