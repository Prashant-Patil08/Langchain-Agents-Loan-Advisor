from __future__ import annotations

from typing import Any


def format_inr(value: float) -> str:
    return f"₹{value:,.2f}"


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default
