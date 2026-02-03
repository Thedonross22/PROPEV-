from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Iterable

from ev_tool.clients.odds_api import OddsApiClient
from ev_tool.clients.props_made_easy import PropsMadeEasyClient
from ev_tool.config import Config
from ev_tool.ev import build_ev_play
from ev_tool.models import BookOdds, EVPlay, PlayerProjection


LINE_TOLERANCE = 0.5


def load_cache(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def save_cache(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))


def group_projections(projections: Iterable[PlayerProjection]) -> dict[tuple[str, str], list[PlayerProjection]]:
    grouped: dict[tuple[str, str], list[PlayerProjection]] = {}
    for projection in projections:
        key = (projection.player, projection.market)
        grouped.setdefault(key, []).append(projection)
    return grouped


def find_projection(
    projection_groups: dict[tuple[str, str], list[PlayerProjection]],
    odds: BookOdds,
) -> PlayerProjection | None:
    candidates = projection_groups.get((odds.player, odds.market), [])
    if not candidates:
        return None
    best = min(candidates, key=lambda projection: abs(projection.line - odds.line))
    if abs(best.line - odds.line) > LINE_TOLERANCE:
        return None
    return best


def compute_ev(
    projections: Iterable[PlayerProjection],
    odds_list: Iterable[BookOdds],
) -> list[EVPlay]:
    projection_groups = group_projections(projections)
    plays: list[EVPlay] = []
    for odds in odds_list:
        projection = find_projection(projection_groups, odds)
        if not projection:
            continue
        plays.append(build_ev_play(projection, odds))
    return sorted(plays, key=lambda play: play.expected_value, reverse=True)


def load_sample_data() -> dict:
    sample_path = Path(__file__).resolve().parent / "sample_data.json"
    return json.loads(sample_path.read_text())


def refresh_data(config: Config, use_sample: bool) -> dict:
    if use_sample:
        return load_sample_data()
    odds_client = OddsApiClient(config.odds_api_key, config.odds_api_base_url)
    props_client = PropsMadeEasyClient(
        api_key=config.props_made_easy_key,
        base_url=config.props_made_easy_base_url,
        login_url=config.props_made_easy_login_url,
        email=config.props_made_easy_email,
        password=config.props_made_easy_password,
    )
    projections = list(props_client.fetch_nba_projections())
    odds_list = list(odds_client.fetch_nba_player_props())
    return {
        "projections": [asdict(item) for item in projections],
        "odds": [asdict(item) for item in odds_list],
    }


def load_models(payload: dict) -> tuple[list[PlayerProjection], list[BookOdds]]:
    projections = [PlayerProjection(**item) for item in payload.get("projections", [])]
    odds_list = [BookOdds(**item) for item in payload.get("odds", [])]
    return projections, odds_list


def command_refresh(config: Config, use_sample: bool) -> None:
    cache_path = Path(config.cache_path)
    payload = refresh_data(config, use_sample)
    save_cache(cache_path, payload)
    print(f"Refreshed data and saved to {cache_path}.")


def format_play(play: EVPlay) -> str:
    ev_percent = play.expected_value * 100
    return (
        f"{play.player} {play.market} {play.side} {play.line} "
        f"@ {play.odds} ({play.bookmaker}) | EV {ev_percent:.1f}% "
        f"Model {play.model_prob:.1%} Implied {play.implied_prob:.1%}"
    )


def command_top(config: Config, limit: int, use_sample: bool) -> None:
    cache_path = Path(config.cache_path)
    payload = load_cache(cache_path)
    if not payload and use_sample:
        payload = load_sample_data()
    if not payload:
        raise RuntimeError("Cache is empty. Run refresh first.")
    projections, odds_list = load_models(payload)
    plays = compute_ev(projections, odds_list)
    for play in plays[:limit]:
        print(format_play(play))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="EV+ NBA player props tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    refresh_parser = subparsers.add_parser("refresh", help="Refresh odds and projections")
    refresh_parser.add_argument(
        "--use-sample",
        action="store_true",
        help="Use bundled sample data instead of API calls.",
    )
    refresh_parser.set_defaults(
        handler=lambda args: command_refresh(args.config, args.use_sample)
    )

    top_parser = subparsers.add_parser("top", help="Show top EV plays")
    top_parser.add_argument("--limit", type=int, default=20)
    top_parser.add_argument(
        "--use-sample",
        action="store_true",
        help="Use bundled sample data if cache is empty.",
    )
    top_parser.set_defaults(
        handler=lambda args: command_top(args.config, args.limit, args.use_sample)
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.config = Config.from_env()
    args.handler(args)


if __name__ == "__main__":
    main()
