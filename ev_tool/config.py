from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    odds_api_key: str
    props_made_easy_key: str
    props_made_easy_email: str
    props_made_easy_password: str
    odds_api_base_url: str
    props_made_easy_base_url: str
    props_made_easy_login_url: str
    cache_path: str

    @classmethod
    def from_env(cls) -> "Config":
        props_base = os.getenv("PROPS_MADE_EASY_BASE_URL", "https://api.propsmadeeasy.com")
        return cls(
            odds_api_key=os.getenv("ODDS_API_KEY", ""),
            props_made_easy_key=os.getenv("PROPS_MADE_EASY_KEY", ""),
            props_made_easy_email=os.getenv("PROPS_MADE_EASY_EMAIL", ""),
            props_made_easy_password=os.getenv("PROPS_MADE_EASY_PASSWORD", ""),
            odds_api_base_url=os.getenv("ODDS_API_BASE_URL", "https://api.the-odds-api.com"),
            props_made_easy_base_url=props_base,
            props_made_easy_login_url=os.getenv(
                "PROPS_MADE_EASY_LOGIN_URL", f"{props_base}/v1/auth/login"
            ),
            cache_path=os.getenv("EV_CACHE_PATH", "data/cache.json"),
        )
