from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    model_name: str = os.getenv("MODEL_NAME", "gemini-2.5-flash")
    app_title: str = os.getenv("APP_TITLE", "Loan Advisor Agent Learning Lab")
    default_foir_limit: float = 0.40
    default_rate_hints: dict[str, str] = None

    def __post_init__(self):
        if self.default_rate_hints is None:
            object.__setattr__(
                self,
                "default_rate_hints",
                {
                    "home": "Typical sample range: 8.25% to 9.50%",
                    "personal": "Typical sample range: 11.00% to 18.00%",
                    "car": "Typical sample range: 8.50% to 11.00%",
                    "education": "Typical sample range: 9.00% to 13.00%",
                },
            )


settings = Settings()
