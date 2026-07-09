"""
Day 80 – AI Agent Building: tool use, ReAct loop, Anthropic tool_use API.
PCPP1 standard: type hints, docstrings, private attributes, PEP 8, British English.
Requires: pip install anthropic python-dotenv

.env file (add to .gitignore):
    ANTHROPIC_API_KEY=sk-ant-...
"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic
from anthropic.types import ToolUseBlock, TextBlock, MessageParam

load_dotenv()


class PropertyAgent:
    """
    AI agent with tool use for property investment analysis.
    Uses the Anthropic tool_use API with an autonomous ReAct loop.

    Note on production patterns (mid-2026):
        This implementation uses the Anthropic tool_use API directly with a
        hand-rolled ReAct loop, which is the correct approach for the Anthropic
        SDK. For multi-agent orchestration, stateful workflows, and complex
        agent graphs, LangGraph (langgraph package) is the current production
        standard, superseding the deprecated LangChain AgentExecutor. LangGraph
        uses a StateGraph model with nodes and edges to define agent behaviour.
        See Day 92 for a LangGraph implementation.
    """

    _SYSTEM_PROMPT: str = (
        "You are a RICS-qualified property investment analyst. "
        "Use the available tools to answer questions about property yields and valuations. "
        "Respond in British English."
    )

    def __init__(self, model: str = "claude-sonnet-4-6") -> None:
        """Initialise the agent with the Anthropic client and tool definitions.

        Args:
            model: Anthropic model string.

        Raises:
            EnvironmentError: If ANTHROPIC_API_KEY is not set.
        """
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "ANTHROPIC_API_KEY not set. Add it to your .env file."
            )
        self._client: Anthropic = Anthropic()
        self._model: str = model
        self._tools: list[dict] = self._define_tools()

    def _define_tools(self) -> list[dict]:
        """Define the tool schemas available to the agent.

        Returns:
            List of tool definition dictionaries.
        """
        return [
            {
                "name": "get_yield",
                "description": (
                    "Returns the current market net initial yield for a given property sector."
                ),
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "sector": {
                            "type": "string",
                            "description": "Property sector: Office, Retail, or Industrial.",
                        }
                    },
                    "required": ["sector"],
                },
            },
            {
                "name": "calculate_value",
                "description": (
                    "Calculates the capital value of a property using direct capitalisation: "
                    "Value = NOI / (yield_pct / 100)."
                ),
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "noi": {
                            "type": "number",
                            "description": "Net operating income in £.",
                        },
                        "yield_pct": {
                            "type": "number",
                            "description": "Net initial yield as a percentage (e.g. 4.5).",
                        },
                    },
                    "required": ["noi", "yield_pct"],
                },
            },
        ]

    def _execute_tool(self, name: str, inputs: dict) -> str:
        """Execute a tool by name and return its result as a string.

        Args:
            name:   Tool name matching a defined schema.
            inputs: Dictionary of input parameters from the model.

        Returns:
            Tool result as a string.
        """
        if name == "get_yield":
            yields: dict[str, float] = {
                "Office": 4.5,
                "Retail": 5.5,
                "Industrial": 5.0,
            }
            return f"{yields.get(inputs['sector'], 5.0)}%"

        if name == "calculate_value":
            value = inputs["noi"] / (inputs["yield_pct"] / 100)
            return f"£{value:,.0f}"

        return f"Unknown tool: {name}"

    def run(self, query: str) -> str:
        """Run the agent ReAct loop until the model produces a final answer.

        Args:
            query: User question string.

        Returns:
            Final text response from the agent.
        """
        messages: list[MessageParam] = [{"role": "user", "content": query}]

        while True:
            response = self._client.messages.create(
                model=self._model,
                max_tokens=1000,
                system=self._SYSTEM_PROMPT,
                tools=self._tools,
                messages=messages,
            )

            if response.stop_reason == "end_turn":
                text_blocks = [b for b in response.content if isinstance(b, TextBlock)]
                return text_blocks[0].text if text_blocks else ""

            tool_uses = [b for b in response.content if isinstance(b, ToolUseBlock)]
            if not tool_uses:
                text_blocks = [b for b in response.content if isinstance(b, TextBlock)]
                return text_blocks[0].text if text_blocks else ""

            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for tool_use in tool_uses:
                result = self._execute_tool(tool_use.name, tool_use.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": result,
                })
            messages.append({"role": "user", "content": tool_results})

    def calculate_value(self, noi: float, yield_pct: float) -> float:
        """Calculate capital value via direct capitalisation.

        Args:
            noi:       Net operating income in £.
            yield_pct: Net initial yield as a percentage.

        Returns:
            Capital value in £.
        """
        return noi / (yield_pct / 100)

    def list_tools(self) -> list[str]:
        """Return a list of available tool names.

        Returns:
            List of tool name strings.
        """
        return [t["name"] for t in self._tools]

    def __len__(self) -> int:
        """Return the number of tools available to the agent.

        Returns:
            Integer count of tools.
        """
        return len(self._tools)

    def __repr__(self) -> str:
        """Return an unambiguous string representation.

        Returns:
            Developer-facing string for this agent.
        """
        return f"PropertyAgent(model='{self._model}', tools={self.list_tools()})"

    def __str__(self) -> str:
        """Return a human-readable string representation.

        Returns:
            User-facing string for this agent.
        """
        return f"PropertyAgent | tools={len(self)} | {self.list_tools()}"


if __name__ == "__main__":
    agent = PropertyAgent()
    print(repr(agent))
    print(str(agent))
    print(f"Tool count: {len(agent)}")
    print(f"CV (manual): £{agent.calculate_value(100_000, 4.5):,.0f}")
    print("\nRunning agent...")
    answer = agent.run(
        "What is the capital value of an Office property with £200,000 NOI? "
        "Use the market yield for that sector."
    )
    print(answer)