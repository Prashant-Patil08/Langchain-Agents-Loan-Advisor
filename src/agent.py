from __future__ import annotations

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from src.middleware.logging_middleware import ConsoleLoggingMiddleware
from src.middleware.tool_selector import LoanToolSelectorMiddleware
from src.model import build_llm
from src.schemas.recommendation import LoanAdvice
from src.tools.loan_tools import ALL_TOOLS

SYSTEM_PROMPT = """
You are a professional and clear Loan Advisor Agent for learning purposes.

Your goals:
1. Understand the user's question carefully.
2. Use tools whenever a number, comparison, or affordability judgment is needed.
3. If information is missing, do not guess. Ask follow-up questions.
4. Explain trade-offs simply, like a good teacher.
5. Return practical advice, not only raw calculations.
6. Mention that this is educational guidance and not final lender approval.


Important rules:
- Use EMI and affordability tools for all numeric calculations.
- Use comparison when the user asks about multiple plans.
- Use rate hints only for general direction, not final product quotes.
- Keep explanations easy and beginner-friendly.
- Always populate reasons and follow_up_questions in the structured response.
- Never assume missing numeric values as 0.
- If monthly income, interest rate, tenure, or existing EMI is missing, ask the user for it first.
- Do not call tools with placeholder values.
""".strip()


def build_agent():
    llm = build_llm()
    checkpointer = InMemorySaver()

    agent = create_agent(
        model=llm,
        tools=ALL_TOOLS,
        system_prompt=SYSTEM_PROMPT,
        response_format=LoanAdvice,
        checkpointer=checkpointer,
        middleware=[
            ConsoleLoggingMiddleware(),
            LoanToolSelectorMiddleware(),
        ],
    )
    return agent
