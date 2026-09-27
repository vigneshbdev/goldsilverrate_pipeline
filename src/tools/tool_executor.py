from src.tools.gold_rate_tool import get_latest_gold_and_silver_rates


TOOL_REGISTRY = {
    "get_latest_gold_and_silver_rates": get_latest_gold_and_silver_rates
}

def execute_tool(tool_name: str, arguments: dict):
    if tool_name not in TOOL_REGISTRY:
        raise ValueError(
            f"Unknown tool: {tool_name}"
        )

    tool = TOOL_REGISTRY[tool_name]

    return tool(**arguments)