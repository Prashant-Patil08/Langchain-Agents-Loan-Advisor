from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field


class LoanAdvice(BaseModel):
    summary: str = Field(description="Short final answer for the user")
    affordability_status: str = Field(description="affordable, borderline, or not_affordable")
    risk_level: str = Field(description="low, medium, or high")
    recommended_action: str = Field(description="Best next action for the user")
    reasons: List[str] = Field(description="Key reasons behind the recommendation")
    follow_up_questions: List[str] = Field(description="Questions to ask when key information is missing")
