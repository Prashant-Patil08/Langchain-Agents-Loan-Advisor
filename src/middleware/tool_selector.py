from __future__ import annotations

from typing import Callable

from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponse


class LoanToolSelectorMiddleware(AgentMiddleware):
    """Expose a smaller relevant tool subset to reduce confusion and teach context engineering."""

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        latest_text = " ".join(
            block.get("text", "")
            for message in request.messages[-2:]
            for block in getattr(message, "content_blocks", [])
            if isinstance(block, dict) and block.get("type") == "text"
        ).lower()

        selected = []
        for tool in request.tools:
            name = getattr(tool, "name", "")
            if any(word in latest_text for word in ["compare", "vs", "better"]):
                if name in {"compare_loan_options", "emi_calculator", "check_affordability"}:
                    selected.append(tool)
            elif any(word in latest_text for word in ["afford", "safe", "salary", "income", "foir"]):
                if name in {"check_affordability", "estimate_max_safe_loan_amount", "emi_calculator"}:
                    selected.append(tool)
            elif any(word in latest_text for word in ["rate", "interest"]):
                if name in {"get_interest_rate_hint", "emi_calculator", "compare_loan_options"}:
                    selected.append(tool)

        if not selected:
            selected = list(request.tools)

        return handler(request.override(tools=selected))
