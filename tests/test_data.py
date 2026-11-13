import pandas as pd
import pytest

from fpm.data import clean, closing_coverage, odds_columns


def _raw():
    row = {"Date": "2024-08-17", "HomeTeam": "Arsenal", "AwayTeam": "Wolves",
           "FTHG": 2, "FTAG": 0, "FTR": "H", "HS": 18, "AS": 9, "HST": 6, "AST": 3}
    for p in ("PS", "Avg"):
        for c in odds_columns(p, False) + odds_columns(p, True):
            row[c] = 2.0
    later = dict(row, Date="2024-08-24")
    return pd.DataFrame([later, row])


def test_odds_column_names():
    assert odds_columns("PS", True) == ["PSCH", "PSCD", "PSCA"]
    assert odds_columns("Avg", False) == ["AvgH", "AvgD", "AvgA"]


def test_clean_sorts_by_date_and_renames():
    df = clean(_raw())
    assert list(df["date"]) == sorted(df["date"])
    assert {"home_team", "away_team"} <= set(df.columns)


def test_clean_fails_loudly_on_missing_columns():
    with pytest.raises(KeyError):
        clean(_raw().drop(columns=["PSCH"]))


def test_closing_coverage():
    df = clean(_raw())
    assert closing_coverage(df).iloc[0] == 1.0
