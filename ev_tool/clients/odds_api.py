from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from ev_tool.models import BookOdds, MarketSide


@dataclass(frozen=True)
class OddsApiClient:
    api_key: str
    base_url: str

    def fetch_nba_player_props(self) -> Iterable[BookOdds]:
        if not self.api_key:
            raise RuntimeError("ODDS_API_KEY is not set.")
        import requests

        url = f"{self.base_url}/v4/sports/basketball_nba/odds"
        params = {
            "apiKey": self.api_key,
            "regions": "us",
            "markets": "player_points,player_rebounds,player_assists,player_threes",
            "oddsFormat": "american",
        }
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return list(self._parse_response(response.json()))

    def _parse_response(self, payload: list[dict]) -> Iterable[BookOdds]:
        for event in payload:
            for bookmaker in event.get("bookmakers", []):
                book_key = bookmaker.get("key", "")
                for market in bookmaker.get("markets", []):
                    market_key = market.get("key", "")
                    for outcome in market.get("outcomes", []):
                        side = self._normalize_side(outcome.get("name", ""))
                        if side is None:
                            continue
                        yield BookOdds(
                            bookmaker=book_key,
                            player=outcome.get("description", ""),
                            market=market_key,
                            side=side,
                            odds=int(outcome.get("price", 0)),
                            line=float(outcome.get("point", 0)),
                        )

    @staticmethod
    def _normalize_side(name: str) -> MarketSide | None:
        lowered = name.lower()
        if lowered == "over":
            return "over"
        if lowered == "under":
            return "under"
        return None
