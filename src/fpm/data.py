"""Load and clean match data from football-data.co.uk (via soccerdata).

Column meanings: https://www.football-data.co.uk/notes.txt
Closing odds use an extra "C" after the bookmaker/Max/Avg code, e.g. PSCH, AvgCH.
"""

from __future__ import annotations

import pandas as pd

LEAGUE = "ENG-Premier League"

BASE_COLUMNS = ["date", "home_team", "away_team", "FTHG", "FTAG", "FTR"]
SHOT_COLUMNS = ["HS", "AS", "HST", "AST"]


def odds_columns(prefix: str, closing: bool) -> list[str]:
    """Column names for a bookmaker's 1X2 odds, e.g. ('PS', True) -> PSCH, PSCD, PSCA."""
    c = "C" if closing else ""
    return [f"{prefix}{c}{k}" for k in ("H", "D", "A")]


def load_raw(seasons: list[str], league: str = LEAGUE) -> pd.DataFrame:
    """Download (or read from cache) raw match rows using soccerdata.MatchHistory.

    `seasons` like ["2122", "2223", "2324"]. Verify soccerdata's season format on the
    first run (see docs/DATA.md).
    """
    import soccerdata as sd  # imported here so tests don't need the network or the package

    mh = sd.MatchHistory(leagues=league, seasons=seasons)
    return mh.read_games().reset_index()


def clean(raw: pd.DataFrame, market_prefixes: tuple[str, ...] = ("PS", "Avg")) -> pd.DataFrame:
    """Select and standardize the columns the project uses.

    Fails loudly if expected columns are missing, so a season with a different schema
    can't silently slip in.
    """
    df = raw.copy()

    # soccerdata may already rename these; accept either form.
    rename = {"Date": "date", "HomeTeam": "home_team", "AwayTeam": "away_team"}
    df = df.rename(columns={k: v for k, v in rename.items() if k in df.columns})

    wanted = BASE_COLUMNS + SHOT_COLUMNS
    for p in market_prefixes:
        wanted += odds_columns(p, closing=False) + odds_columns(p, closing=True)
    if "season" in df.columns:
        wanted = ["season"] + wanted

    missing = [c for c in wanted if c not in df.columns]
    if missing:
        raise KeyError(f"Missing expected columns: {missing}. Check docs/DATA.md.")

    df = df[wanted].copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date", kind="stable").reset_index(drop=True)
    return df


def closing_coverage(df: pd.DataFrame, prefix: str = "PS") -> pd.Series:
    """Fraction of rows with complete closing odds, per season (to pick the season range)."""
    cols = odds_columns(prefix, closing=True)
    complete = df[cols].notna().all(axis=1)
    key = df["season"] if "season" in df.columns else df["date"].dt.year
    return complete.groupby(key).mean()
