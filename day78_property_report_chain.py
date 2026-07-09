"""
Day 78 – LangChain Basics: LLM chains, prompt templates, LCEL pipe syntax.
Includes python-dotenv for API key hygiene — never commit .env to GitHub.
PCPP1 standard: type hints, docstrings, private attributes, PEP 8, British English.
Requires: pip install langchain langchain-anthropic python-dotenv

.env file (add to .gitignore):
    ANTHROPIC_API_KEY=sk-ant-...
"""

import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable

load_dotenv()


class PropertyReportChain:
    """LangChain pipeline for generating property investment reports."""

    _SYSTEM_PROMPT: str = (
        "You are a RICS-qualified property investment analyst with 10 years of "
        "experience in UK commercial real estate. Respond concisely in British English."
    )

    def __init__(self, model: str = "claude-sonnet-4-6") -> None:
        """Initialise the chain with an Anthropic LLM.

        Args:
            model: Anthropic model string; defaults to claude-sonnet-4-6.

        Raises:
            EnvironmentError: If ANTHROPIC_API_KEY is not set.
        """
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "ANTHROPIC_API_KEY not set. Add it to your .env file."
            )
        self._llm: ChatAnthropic = ChatAnthropic(model=model)
        self._parser: StrOutputParser = StrOutputParser()

    def _build_chain(self, human_template: str) -> Runnable:
        """Build an LCEL chain from a human message template.

        Args:
            human_template: Template string with {property_details} placeholder.

        Returns:
            A composable Runnable LCEL chain.
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", self._SYSTEM_PROMPT),
            ("human", human_template),
        ])
        return prompt | self._llm | self._parser

    def investment_summary(self, property_details: str) -> str:
        """Generate an investment summary for a property.

        Args:
            property_details: Free-text description of the property.

        Returns:
            Investment summary as a string.
        """
        chain = self._build_chain(
            "Write a concise investment summary for: {property_details}"
        )
        return chain.invoke({"property_details": property_details})

    def risk_analysis(self, property_details: str) -> str:
        """Generate a risk analysis for a property.

        Args:
            property_details: Free-text description of the property.

        Returns:
            Risk analysis as a string.
        """
        chain = self._build_chain(
            "List the key investment risks for: {property_details}"
        )
        return chain.invoke({"property_details": property_details})

    def batch_summaries(self, details_list: list[str]) -> list[str]:
        """Generate investment summaries for multiple properties.

        Args:
            details_list: List of property description strings.

        Returns:
            List of investment summaries.
        """
        chain = self._build_chain(
            "Write a concise investment summary for: {property_details}"
        )
        inputs = [{"property_details": d} for d in details_list]
        return chain.batch(inputs)

    def stream_summary(self, property_details: str) -> None:
        """Stream an investment summary token by token to stdout.

        Args:
            property_details: Free-text description of the property.
        """
        chain = self._build_chain(
            "Write a concise investment summary for: {property_details}"
        )
        for chunk in chain.stream({"property_details": property_details}):
            print(chunk, end="", flush=True)
        print()

    def __repr__(self) -> str:
        """Return an unambiguous string representation.

        Returns:
            Developer-facing string for this chain.
        """
        return f"PropertyReportChain(model='{self._llm.model}')"


if __name__ == "__main__":
    chain = PropertyReportChain()

    print("=== Investment Summary ===")
    result = chain.investment_summary(
        "EC2 office tower, 50,000 sq ft NIA, £100 psf passing rent, 5% NIY, "
        "single tenant, lease expiry 5 years, Grade A specification."
    )
    print(result)

    print("\n=== Risk Analysis ===")
    risks = chain.risk_analysis(
        "Retail warehouse in Birmingham, £2.5m, 7% NIY, short WAULT of 2 years."
    )
    print(risks)

    print(repr(chain))