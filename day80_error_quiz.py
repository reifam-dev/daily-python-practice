# This file contains 3 deliberate bugs. Find and fix them.
import json
from anthropic import Anthropic


class PropertyAgent:

    def __init__(self) -> None:
        self._client = Anthropic()
        self._tools = self._define_tools()

    def _define_tools(self) -> list[dict]:
        return [
            {
                "name": "get_yield",
                "description": "Returns the current market yield for a property sector.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "sector": {"type": "string", "description": "Property sector e.g. Office, Retail"}
                    },
                    "required": ["sector"]
                }
            },
            {
                "name": "calculate_value",
                "description": "Calculates capital value from NOI and yield.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "noi": {"type": "number"},
                        "yield_pct": {"type": "number"}
                    },
                    "required": ["noi", "yield_pct"]
                }
            }
        ]

    def _execute_tool(self, name: str, inputs: dict) -> str:
        if name == "get_yield":
            yields = {"Office": 4.5, "Retail": 5.5, "Industrial": 5.0}
            return str(yields.get(inputs["sector"], 5.0))
        if name == "calculate_value":
            return str(inputs["noi"] / (inputs["yield_pct"] / 100))
        return "Unknown tool"

    def run(self, query: str) -> str:
        messages = [{"role": "user", "content": query}]
        while True:
            response = self._client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1000,
                tools=self._tools,
                messages=messages
            )
            if response.stop_reason == "end_turn":
                return response.content[0].text

            tool_uses = [b for b in response.content if b.type == "tool_use"]
            if not tool_uses:
                return response.content[0].text

            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            for tool_use in tool_uses:
                result = self._execute_tool(tool_use.name, tool_use.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": result
                })
            messages.append({"role": "user", "content": tool_results})  # Bug 1: role should be "user" — this is actually correct; real Bug 1: missing model param below

    def run_simple(self, query: str) -> str:
        response = self._client.messages.create(
            max_tokens=500,                     # Bug 1 (actual): missing model= parameter
            messages=[{"role": "user", "content": query}]
        )
        return response.content[0].text

    def calculate_value(self, noi: float, yield_pct: float) -> float:
        return noi + (yield_pct / 100)         # Bug 2: + should be / (capital value = NOI / yield)

    def summarise_tools(self) -> list[str]:
        return [t["name"] for t in self._tools]

    def __len__(self) -> int:
        return len(self._tools) * 2             # Bug 3: should not multiply by 2


if __name__ == "__main__":
    agent = PropertyAgent()
    print("Tools:", agent.summarise_tools())
    print("Tool count:", len(agent))
    print("CV:", agent.calculate_value(100_000, 5.0))