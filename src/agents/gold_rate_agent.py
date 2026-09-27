from src.llm.base import BaseLLM
from src.llm.factory import LLMFactory

from src.tools.tool_definitions import GOLD_RATE_TOOL
from src.tools.tool_executor import execute_tool
from src.models.gold_silver_rate import GoldSilverRate

class GoldRateAgent:

    def __init__(self):
        self.llm: BaseLLM = LLMFactory.create()
        self.system_prompt = """
You are a Gold Rate Social Media Agent.

Your job is to help create accurate gold and silver
rate posts for Instagram.

Important rules:

1. Never invent gold or silver rates.
2. If current rates are required, you must use the
   available gold-rate tool.
3. Do not assume that your training data contains
   today's rates.
4. Accuracy is more important than completing the post.
        """

    def run(self, user_request:str) -> GoldSilverRate:
        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": user_request
            }
        ]

        response = self.llm.chat(messages=messages, tools=[GOLD_RATE_TOOL])

        assistant_message = response.choices[0].message

        messages.append(
            assistant_message.model_dump(exclude_none=True)
        )

        if assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                import json

                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                tool_result = execute_tool(tool_name=tool_name, arguments=arguments)

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result.model_dump_json()
                    }
                )

            final_response = self.llm.parse(
                messages=messages,
                response_format=GoldSilverRate
            )

            return final_response.choices[0].message.parsed
        
        return response