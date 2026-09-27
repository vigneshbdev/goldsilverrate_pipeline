GOLD_RATE_TOOL = {
    "type": "function",
    "function": {
        "name" : "get_latest_gold_and_silver_rates",
        "description": (
            "Fetch the latest gold and silver rates from LiveChennai. "
            "Use this tool whenever current gold or silver rates are required. "
            "Do not guess or invent current rates."
        ),
        "paramaters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
}