from __future__ import annotations

import json
from typing import List

from langchain.tools import tool

from src.config import settings
from src.finance import (
    assess_affordability,
    calculate_emi_values,
    compare_plans,
    max_affordable_loan,
)


@tool

def emi_calculator(principal: float, annual_rate: float, tenure_years: int) -> str:
    """Calculate EMI, total interest, and total repayment for a loan."""
    result = calculate_emi_values(principal, annual_rate, tenure_years)
    return json.dumps(result, indent=2)


@tool

def check_affordability(monthly_income: float, existing_emi: float, proposed_emi: float) -> str:
    """Check whether a proposed EMI is affordable using FOIR logic."""
    result = assess_affordability(
        monthly_income=monthly_income,
        existing_emi=existing_emi,
        proposed_emi=proposed_emi,
        foir_limit=settings.default_foir_limit,
    )
    return json.dumps(result, indent=2)


@tool

def compare_loan_options(plans_json: str) -> str:
    """Compare two or more loan plans. Input must be a JSON list with principal, annual_rate, tenure_years, and optional label."""
    plans: List[dict] = json.loads(plans_json)
    result = compare_plans(plans)
    return json.dumps(result, indent=2)


@tool

def estimate_max_safe_loan_amount(monthly_income: float, existing_emi: float, annual_rate: float, tenure_years: int) -> str:
    """Estimate the maximum safe loan amount for the user using monthly income, current EMI, rate, and tenure."""
    result = max_affordable_loan(
        monthly_income=monthly_income,
        existing_emi=existing_emi,
        annual_rate=annual_rate,
        tenure_years=tenure_years,
        foir_limit=settings.default_foir_limit,
    )
    return json.dumps(result, indent=2)


@tool

def get_interest_rate_hint(loan_type: str) -> str:
    """Return a sample interest-rate range for a loan type such as home, personal, car, or education."""
    return settings.default_rate_hints.get(
        loan_type.lower().strip(),
        "No sample rate hint available for that loan type.",
    )


ALL_TOOLS = [
    emi_calculator,
    check_affordability,
    compare_loan_options,
    estimate_max_safe_loan_amount,
    get_interest_rate_hint,
]
