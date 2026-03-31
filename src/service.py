from __future__ import annotations

from typing import Any

from src.agent import build_agent

agent = build_agent()


def run_agent(user_input: str, thread_id: str) -> dict[str, Any]:
    result = agent.invoke(
        {"messages": [{"role": "user", "content": user_input}]},
        {"configurable": {"thread_id": thread_id}},
    )

    structured = result.get("structured_response")
    return {
        "raw": result,
        "structured": structured,
    }
