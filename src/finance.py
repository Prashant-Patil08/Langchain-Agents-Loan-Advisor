from __future__ import annotations

import math
from typing import Any


def calculate_emi_values(principal: float, annual_rate: float, tenure_years: int) -> dict[str, Any]:
    if principal <= 0:
        raise ValueError("principal must be greater than 0")
    if annual_rate < 0:
        raise ValueError("annual_rate cannot be negative")
    if tenure_years <= 0:
        raise ValueError("tenure_years must be greater than 0")

    monthly_rate = annual_rate / 12 / 100
    total_months = tenure_years * 12

    if monthly_rate == 0:
        emi = principal / total_months
    else:
        emi = principal * monthly_rate * math.pow(1 + monthly_rate, total_months) / (
            math.pow(1 + monthly_rate, total_months) - 1
        )

    total_repayment = emi * total_months
    total_interest = total_repayment - principal

    return {
        "principal": round(principal, 2),
        "annual_rate": round(annual_rate, 4),
        "tenure_years": tenure_years,
        "monthly_emi": round(emi, 2),
        "total_interest": round(total_interest, 2),
        "total_repayment": round(total_repayment, 2),
    }


def assess_affordability(
    monthly_income: float,
    existing_emi: float,
    proposed_emi: float,
    foir_limit: float,
) -> dict[str, Any]:
    if monthly_income <= 0:
        raise ValueError("monthly_income must be greater than 0")
    if existing_emi < 0 or proposed_emi < 0:
        raise ValueError("EMI values cannot be negative")

    total_obligations = existing_emi + proposed_emi
    foir = total_obligations / monthly_income
    disposable_income = monthly_income - total_obligations

    if foir <= foir_limit * 0.75:
        affordability = "affordable"
        risk_level = "low"
    elif foir <= foir_limit:
        affordability = "borderline"
        risk_level = "medium"
    else:
        affordability = "not_affordable"
        risk_level = "high"

    return {
        "monthly_income": round(monthly_income, 2),
        "existing_emi": round(existing_emi, 2),
        "proposed_emi": round(proposed_emi, 2),
        "total_obligations": round(total_obligations, 2),
        "foir": round(foir, 4),
        "foir_limit": foir_limit,
        "affordability_status": affordability,
        "risk_level": risk_level,
        "disposable_income": round(disposable_income, 2),
    }


def max_affordable_loan(
    monthly_income: float,
    existing_emi: float,
    annual_rate: float,
    tenure_years: int,
    foir_limit: float,
) -> dict[str, Any]:
    if monthly_income <= 0:
        return {
            "error": "monthly_income must be greater than 0",
            "status": "invalid_input"
        }
    if existing_emi < 0:
        raise ValueError("existing_emi cannot be negative")

    max_total_emi = monthly_income * foir_limit
    max_new_emi = max_total_emi - existing_emi

    if max_new_emi <= 0:
        return {
            "maximum_safe_monthly_emi": 0.0,
            "maximum_safe_principal": 0.0,
            "note": "Current obligations already exceed the selected FOIR threshold.",
        }

    monthly_rate = annual_rate / 12 / 100
    total_months = tenure_years * 12

    if monthly_rate == 0:
        principal = max_new_emi * total_months
    else:
        principal = max_new_emi * ((math.pow(1 + monthly_rate, total_months) - 1) / (
            monthly_rate * math.pow(1 + monthly_rate, total_months)
        ))

    return {
        "maximum_safe_monthly_emi": round(max_new_emi, 2),
        "maximum_safe_principal": round(principal, 2),
        "assumptions": {
            "monthly_income": round(monthly_income, 2),
            "existing_emi": round(existing_emi, 2),
            "annual_rate": round(annual_rate, 4),
            "tenure_years": tenure_years,
            "foir_limit": foir_limit,
        },
    }


def compare_plans(plans: list[dict[str, Any]]) -> dict[str, Any]:
    if len(plans) < 2:
        raise ValueError("Provide at least 2 plans to compare")

    enriched = []
    for idx, plan in enumerate(plans, start=1):
        label = plan.get("label") or f"Plan {idx}"
        result = calculate_emi_values(
            principal=float(plan["principal"]),
            annual_rate=float(plan["annual_rate"]),
            tenure_years=int(plan["tenure_years"]),
        )
        result["label"] = label
        enriched.append(result)

    lowest_emi = min(enriched, key=lambda x: x["monthly_emi"])
    lowest_repayment = min(enriched, key=lambda x: x["total_repayment"])

    return {
        "plans": enriched,
        "lowest_emi_plan": lowest_emi["label"],
        "lowest_total_repayment_plan": lowest_repayment["label"],
        "learning_note": "Longer tenure usually lowers EMI but increases total repayment.",
    }
