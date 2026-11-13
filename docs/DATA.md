# Data Notes

## Primary source: football-data.co.uk

- Free CSVs of historical results, match statistics, and betting odds.
- Loaded through `soccerdata.MatchHistory`, which provides DataFrames from the football-data.co.uk CSVs and caches them locally under `~/soccerdata/data/MatchHistory`.
- Column definitions: <https://www.football-data.co.uk/notes.txt>. That's the authoritative reference; check it whenever a column's meaning is unclear.

### Columns this project uses

| Purpose | Columns | Notes |
|---|---|---|
| Match ID | `Date`, `HomeTeam`, `AwayTeam` | `soccerdata` may rename or index these; check after loading |
| Outcome | `FTHG`, `FTAG`, `FTR` | Full-time home goals, away goals, result (H/D/A) |
| Shots (optional features) | `HS`, `AS`, `HST`, `AST` | Shots and shots on target |
| Pre-match odds | e.g. `B365H/D/A`, `PSH/D/A`, `AvgH/D/A` | Bet365, Pinnacle, market average |
| **Closing odds** | e.g. `B365CH/CD/CA`, `PSCH/CD/CA`, `AvgCH/CD/CA`, `MaxCH/CD/CA` | Per the notes file, closing odds are the last odds before the match starts, marked by an extra "C" after the bookmaker/Max/Avg abbreviation |

### To verify after the first download (M1)

These are **not yet confirmed** and need checking against the real files:

- [ ] Which seasons actually include the closing-odds columns. Sources I found disagree, so check empirically: `df.filter(like="CH").notna().mean()` per season.
- [ ] Whether older seasons use different names for the market average (the loader should fail loudly if expected columns are missing)
- [ ] How `soccerdata` labels seasons (e.g. `"2324"` vs `2023`) and what the index looks like
- [ ] Any missing odds rows; decide whether to drop them (same matches dropped for model *and* market)

## Optional source: StatsBomb Open Data (xG stretch goal)

- Free event data on GitHub: <https://github.com/statsbomb/open-data>
- Using it means agreeing to StatsBomb's user agreement. Published analysis should name StatsBomb as the data source and use their logo (from their Media Pack).
- Premier League coverage I could confirm is the **2015/16 full season** (competition_id = 2, season_id = 27), released as part of their free "Big 5 Leagues" data release.
- **Caveat that affects the design:** if 2015/16 is the only full EPL season in the open data, an xG feature can't cover the same recent seasons as the main model. Options: (a) run the xG experiment as a separate 2015/16 study, (b) use xG from a different source, or (c) skip it. Check `competitions.json` before deciding.

## Data handling rules

- Raw CSVs live in `data/raw/` and are **git-ignored**. The repo ships a download script, not the data.
- Every row is keyed by kickoff date. Any feature for a match must be computed from matches with an **earlier** date (see `docs/METHODOLOGY.md`).
