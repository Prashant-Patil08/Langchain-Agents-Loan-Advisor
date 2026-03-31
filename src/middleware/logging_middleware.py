from __future__ import annotations

from typing import Callable

from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponse
from langchain.messages import ToolMessage
from langchain.tools.tool_node import ToolCallRequest
from langgraph.types import Command


class ConsoleLoggingMiddleware(AgentMiddleware):
    """Simple middleware for learning: logs model and tool activity to the terminal."""

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        print(f"\n[MIDDLEWARE] Model call | messages={len(request.messages)} | tools={len(request.tools)}")
        return handler(request)

    def wrap_tool_call(
        self,
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], ToolMessage | Command],
    ) -> ToolMessage | Command:
        print(f"[MIDDLEWARE] Tool call -> {request.tool_call['name']} | args={request.tool_call['args']}")
        return handler(request)
