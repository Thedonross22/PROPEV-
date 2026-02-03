from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from ev_tool.models import PlayerProjection


@dataclass(frozen=True)
class PropsMadeEasyClient:
    api_key: str
    base_url: str
    login_url: str
    email: str
    password: str

    def fetch_nba_projections(self) -> Iterable[PlayerProjection]:
        url = f"{self.base_url}/v1/nba/projections"
        headers = {"Authorization": f"Bearer {self._get_token()}"}
        import requests

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return list(self._parse_response(response.json()))

    def _get_token(self) -> str:
        if self.api_key:
            return self.api_key
        if not self.email or not self.password:
            raise RuntimeError(
                "Props Made Easy credentials are missing. Set PROPS_MADE_EASY_KEY or "
                "PROPS_MADE_EASY_EMAIL/PROPS_MADE_EASY_PASSWORD."
            )
        import requests

        response = requests.post(
            self.login_url,
            json={"email": self.email, "password": self.password},
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
        token = payload.get("access_token") or payload.get("token") or payload.get("data", {}).get("token")
        if not token:
            raise RuntimeError("Unable to parse Props Made Easy token response.")
        return token

    def _parse_response(self, payload: dict) -> Iterable[PlayerProjection]:
        for item in payload.get("data", []):
            yield PlayerProjection(
                player=item.get("player", ""),
                team=item.get("team", ""),
                market=item.get("market", ""),
                line=float(item.get("line", 0)),
                mean=float(item.get("mean", 0)),
                std_dev=float(item.get("std_dev", 0)) or 1.0,
            )
