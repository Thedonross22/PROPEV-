from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


MarketSide = Literal["over", "under"]


@dataclass(frozen=True)
class PlayerProjection:
    player: str
    team: str
    market: str
    line: float
    mean: float
    std_dev: float


@dataclass(frozen=True)
class BookOdds:
    bookmaker: str
    player: str
    market: str
    side: MarketSide
    odds: int
    line: float


@dataclass(frozen=True)
class EVPlay:
    player: str
    team: str
    market: str
    side: MarketSide
    line: float
    odds: int
    implied_prob: float
    model_prob: float
    expected_value: float
    bookmaker: str
