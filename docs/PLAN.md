# Project Plan

**Deadline:** end of UW winter break, **Sun Jan 3, 2027** (Winter 2027 instruction begins Mon Jan 4).
**Constraint:** Autumn finals run Dec 12–18, so most of the build happens Nov 13 → Dec 11 (light) and Dec 19 → Jan 3 (heavy).

## Definition of done

- [ ] Public GitHub repo (portfolio piece), clean history, passing tests
- [ ] README with a results table and a how-to-run section
- [ ] ~1,000-word write-up (`docs/WRITEUP.md`) with 3–4 charts
- [ ] All results reported truthfully, including if the model loses to the market
- [ ] Every step explainable at a CSE 312 level (interview-ready)

## Milestones

### M0: Setup (Nov 13–16)
- [x] Repo scaffold, package layout, docs skeletons
- [x] Unit tests for margin removal, metrics, date split
- [ ] Push to a public GitHub repo; pin it on the GitHub profile
- [ ] Run `scripts/download_data.py` locally and confirm the columns exist (see `docs/DATA.md`)

### M1: Data (Nov 17–30)
- [ ] Pick the league (default: Premier League) and seasons
- [ ] Confirm which seasons have closing-odds columns, then lock the season range
- [ ] Clean table: date, teams, goals, result, shots, pre-match and closing odds
- [ ] Notebook: basic EDA (home win rate, goals per game, draw rate)

### M2: Market benchmark (Dec 1–11)
- [ ] Implied probabilities from closing odds; check the overround distribution
- [ ] Choose which bookmaker or average to use as "the market" (see `docs/METHODOLOGY.md`)
- [ ] Baselines: uniform (1/3) and "historical base rates"

### ⏸ Finals week (Dec 12–18): no project work planned

### M3: Model (Dec 19–25)
- [ ] Implement the goals-based model fit (`src/fpm/model.py`)
- [ ] Walk-forward predictions on the test period
- [ ] Sanity checks: predicted goal totals vs. actual, home advantage estimate

### M4: Evaluation + analysis (Dec 26–30)
- [ ] Log loss and Brier for uniform / base rates / model / market
- [ ] Calibration plots (model and market)
- [ ] Disagreement analysis: biggest model-vs-market gaps; who was right; patterns
- [ ] Bootstrap confidence interval for the log-loss difference

### M5: Write-up + polish (Dec 31 – Jan 3)
- [ ] Final charts in `figures/`
- [ ] Write-up draft → edit to ~1,000 words
- [ ] README results table filled in
- [ ] Fresh-clone test: install, run tests, reproduce numbers

### Stretch (only if M0–M5 are done)
- [ ] xG feature from StatsBomb open data (see the caveat in `docs/DATA.md`)

## Decisions log

| Date | Decision | Why |
|---|---|---|
| 2026-11-13 | Repo name `football-prediction-model`, Python package `fpm` | Matches project name |
| 2026-11-13 | MIT license for code | Common permissive default; can change before going public |
| | | |
