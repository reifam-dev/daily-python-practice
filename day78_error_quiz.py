# This file contains 3 deliberate bugs. Find and fix them.
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class PropertyReportChain:

    def __init__(self, model: str = "claude-sonnet-4-6") -> None:
        self._llm = ChatAnthropic(model=model)
        self._parser = StrOutputParser()

    def build_chain(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a RICS-qualified property analyst. Respond in British English."),
            ("human", "Write a brief investment summary for: {property_details}")
        ])
        return prompt | self._llm | self._parser

    def run(self, property_details: str) -> str:
        chain = self.build_chain                # Bug 1: missing parentheses
        return chain.invoke({"property_details": property_details})

    def batch_run(self, details_list: list[str]) -> list[str]:
        chain = self.build_chain()
        inputs = [{"property_details": d} for d in details_list]
        return chain.batch(inputs)

    def stream_run(self, property_details: str) -> None:
        chain = self.build_chain()
        for chunk in chain.stream({"property_detail": property_details}):  # Bug 2: wrong key
            print(chunk, end="", flush=True)

    def build_valuation_chain(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a property valuer. Output only a number in £m."),
            ("human", "Estimate the value of: {property_details}")
        ])
        return prompt + self._llm + self._parser  # Bug 3: + should be |


if __name__ == "__main__":
    chain = PropertyReportChain()
    result = chain.run("EC2 office tower, 50,000 sq ft, £100 psf passing rent, 5% NIY")
    print(result)