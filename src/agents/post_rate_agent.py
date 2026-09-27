from src.llm.base import BaseLLM
from src.llm.factory import LLMFactory

from src.agents.gold_rate_agent import GoldRateAgent
from src.agents.caption_agent import CaptionAgent
import json

class PostRateAgent:

    def __init__(self) -> None:
        self.llm: BaseLLM = LLMFactory.create()
        self.rate_agent = GoldRateAgent()
        self.caption_agent = CaptionAgent()
        self.system_prompt = """
You are the orchestration agent for a Chennai gold and silver
Instagram content workflow.

Your job is to coordinate specialized agents.

Available agents:

1. run_rate_agent
   Gets and validates today's Chennai gold and silver rates.

2. run_caption_agent
   Generates an Instagram caption from validated rate data.

Workflow:

1. Always call run_rate_agent first when the user asks to create
   today's gold and silver content.
2. After receiving valid rate data, call run_caption_agent.
3. Do not invent or modify rate data.
4. Do not skip the rate agent.
5. Do not call the caption agent before the rate agent.
6. After both agents complete, provide a concise final response.

The rate agent owns rate retrieval.
The caption agent owns caption generation.
You own orchestration.
    """
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "run_rate_agent",
                    "description": (
                        "Get and validate today's Chennai gold and "
                        "silver rates."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "request": {
                                "type": "string",
                                "description": (
                                    "The user's request for the "
                                    "gold and silver rates."
                                ),
                            }
                        },
                        "required": ["request"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "run_caption_agent",
                    "description": (
                        "Generate an Instagram caption from "
                        "validated gold and silver rate data."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "rate_data": {
                                "type": "object",
                                "description": (
                                    "Validated gold and silver "
                                    "rate data."
                                ),
                            }
                        },
                        "required": ["rate_data"],
                    },
                },
            },
        ]

    def execute_tool(self, tool_name: str, arguments: dict):

        if tool_name == "run_rate_agent":

            print("\n🔧 Tool: run_rate_agent")

            result = self.rate_agent.run(
                arguments["request"]
            )

            print("📊 Rate Agent result:")
            print(result)

            return result.model_dump(mode="json")


        if tool_name == "run_caption_agent":

            print("\n🔧 Tool: run_caption_agent")

            rate_data = arguments["rate_data"]

            result = self.caption_agent.run(
                rate_data
            )

            print("✍️ Caption Agent result:")
            print(result)

            return {
                "caption": result
            }


        raise ValueError(
            f"Unknown tool: {tool_name}"
        )

    def run(self, user_request: str):

        messages = [
            {
                "role": "system",
                "content": self.system_prompt,
            },
            {
                "role": "user",
                "content": user_request,
            },
        ]

        while True:

            response = self.llm.chat(
                messages=messages,
                tools=self.tools,
            )

            assistant_message = response.choices[0].message

            messages.append(assistant_message)

            if not assistant_message.tool_calls:
                return assistant_message.content

            for tool_call in assistant_message.tool_calls:

                tool_name = tool_call.function.name

                arguments = json.loads(
                    tool_call.function.arguments
                )

                result = self.execute_tool(
                    tool_name,
                    arguments,
                )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result),
                    }
                )
