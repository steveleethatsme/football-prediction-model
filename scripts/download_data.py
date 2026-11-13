"""Download Premier League seasons from football-data.co.uk and save a cleaned CSV.

Usage:
    python scripts/download_data.py --seasons 1920 2021 2122 2223 2324 2425
"""

from __future__ import annotations

import argparse
from pathlib import Path

from fpm.data import clean, closing_coverage, load_raw

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seasons", nargs="+", default=["1920", "2021", "2122", "2223", "2324", "2425"])
    ap.add_argument("--out", default=str(ROOT / "data" / "processed" / "matches.csv"))
    args = ap.parse_args()

    raw = load_raw(args.seasons)
    raw.to_csv(ROOT / "data" / "raw" / "matches_raw.csv", index=False)
    print(f"Raw rows: {len(raw)}; columns: {len(raw.columns)}")

    df = clean(raw)
    df.to_csv(args.out, index=False)
    print(f"Saved {len(df)} cleaned rows to {args.out}")
    print("Closing-odds coverage (Pinnacle) by season:")
    print(closing_coverage(df, "PS"))


if __name__ == "__main__":
    main()
