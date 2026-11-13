"""Date-based splitting. Nothing from the future may reach a prediction."""

from __future__ import annotations

from collections.abc import Iterator

import pandas as pd


def split_by_date(df: pd.DataFrame, cutoff: str | pd.Timestamp, date_col: str = "date"):
    """Train = matches strictly before `cutoff`; test = matches on/after `cutoff`."""
    cutoff = pd.Timestamp(cutoff)
    dates = pd.to_datetime(df[date_col])
    train = df[dates < cutoff]
    test = df[dates >= cutoff]
    return train, test


def walk_forward_windows(
    df: pd.DataFrame,
    test_start: str | pd.Timestamp,
    freq: str = "7D",
    date_col: str = "date",
) -> Iterator[tuple[pd.DataFrame, pd.DataFrame]]:
    """Yield (history, chunk) pairs for walk-forward evaluation.

    For each chunk of the test period (default: 7-day windows), `history` contains every
    match strictly before the chunk's first day. Refit on `history`, predict `chunk`.
    """
    dates = pd.to_datetime(df[date_col])
    step = pd.Timedelta(freq)
    lo = pd.Timestamp(test_start)
    end = dates.max()

    while lo <= end:
        hi = lo + step
        chunk = df[(dates >= lo) & (dates < hi)]
        if not chunk.empty:
            yield df[dates < lo], chunk
        lo = hi
