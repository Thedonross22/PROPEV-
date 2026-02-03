from __future__ import annotations

import math
from dataclasses import dataclass

from ev_tool.models import BookOdds, EVPlay, PlayerProjection


@dataclass(frozen=True)
class EVResult:
    play: EVPlay


def american_to_implied_prob(odds: int) -> float:
    if odds > 0:
        return 100 / (odds + 100)
    return -odds / (-odds + 100)


def normal_cdf(x: float, mean: float, std_dev: float) -> float:
    if std_dev <= 0:
        return 0.5
    z = (x - mean) / (std_dev * math.sqrt(2))
    return 0.5 * (1 + math.erf(z))


def estimate_prob_over(projection: PlayerProjection) -> float:
    return 1 - normal_cdf(projection.line, projection.mean, projection.std_dev)


def estimate_prob_under(projection: PlayerProjection) -> float:
    return normal_cdf(projection.line, projection.mean, projection.std_dev)


def expected_value(prob: float, odds: int, stake: float = 1.0) -> float:
    if odds > 0:
        payout = stake * (odds / 100)
    else:
        payout = stake * (100 / abs(odds))
    return prob * payout - (1 - prob) * stake


def build_ev_play(
    projection: PlayerProjection,
    odds: BookOdds,
) -> EVPlay:
    implied = american_to_implied_prob(odds.odds)
    if odds.side == "over":
        model_prob = estimate_prob_over(projection)
    else:
        model_prob = estimate_prob_under(projection)
    ev = expected_value(model_prob, odds.odds)
    return EVPlay(
        player=projection.player,
        team=projection.team,
        market=projection.market,
        side=odds.side,
        line=odds.line,
        odds=odds.odds,
        implied_prob=implied,
        model_prob=model_prob,
        expected_value=ev,
        bookmaker=odds.bookmaker,
    )
