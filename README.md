# EV+ NBA Props Tool

CLI utility to pull NBA player prop odds and projections, compute EV, and surface the best plays.

## Setup

```bash
pip install -r requirements.txt
```

Set your API credentials:

```bash
export ODDS_API_KEY="your_odds_api_key"
export PROPS_MADE_EASY_KEY="your_props_made_easy_key"
```

If Props Made Easy uses email/password login, set:

```bash
export PROPS_MADE_EASY_EMAIL="you@example.com"
export PROPS_MADE_EASY_PASSWORD="your_password"
```

Optional overrides:

```bash
export ODDS_API_BASE_URL="https://api.the-odds-api.com"
export PROPS_MADE_EASY_BASE_URL="https://api.propsmadeeasy.com"
export PROPS_MADE_EASY_LOGIN_URL="https://api.propsmadeeasy.com/v1/auth/login"
export EV_CACHE_PATH="data/cache.json"
```

## Usage

Refresh data and cache it:

```bash
python -m ev_tool.main refresh
```

Show the top EV plays:

```bash
python -m ev_tool.main top --limit 20
```

Run with bundled sample data (no API keys required):

```bash
python -m ev_tool.main refresh --use-sample
python -m ev_tool.main top --use-sample --limit 5
```

## Notes

- The tool expects props/projection data from Props Made Easy and odds from The Odds API.
- Lines are matched within a 0.5 tolerance to pair odds with projections.
