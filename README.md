# EV+ NBA Props Tool

CLI utility to pull NBA player prop odds and projections, compute EV, and surface the best plays.

## Setup

### Step-by-step (from no project folder)

1) Open your terminal.
2) Make a folder for the project and enter it:

```bash
mkdir -p ~/PROPEV-
cd ~/PROPEV-
```

3) Create the project folders you need:

```bash
mkdir -p ev_tool/clients tests data
```

4) Copy the files from this repository into your new folder.
   - If you already downloaded the code, copy everything into `~/PROPEV-`.
   - If you are pasting by hand in Nano, open each file with Nano and paste.

Example (Nano):

```bash
nano README.md
```

Then paste the file contents, save with **Ctrl + O**, press **Enter**, and exit with **Ctrl + X**.

Repeat for each file listed in this repo (for example: `requirements.txt`, `ev_tool/main.py`, etc.).

5) Install Python requirements:

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
