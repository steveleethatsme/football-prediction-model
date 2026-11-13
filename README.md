# Football Prediction Model vs. the Betting Market

A goals-based model that predicts home / draw / away probabilities for Premier League matches, evaluated honestly against bookmakers' closing odds.

**The question:** how close can a simple, well-calibrated statistical model get to the betting market? The goal isn't to beat the bookmakers. Closing odds are a very strong benchmark, and results get reported as they come out, even if the model loses.

> **Status:** 🚧 In progress. Results, charts, and the write-up will be added as the project develops. See [`docs/PLAN.md`](docs/PLAN.md).

## What this project does

1. **Loads historical match data** from [football-data.co.uk](https://www.football-data.co.uk/): results, shot stats, and pre-match and closing odds. It uses the [`soccerdata`](https://soccerdata.readthedocs.io/) library's `MatchHistory` reader.
2. **Fits a goals-based baseline model** that turns each match into P(home win), P(draw), P(away win), using only information available before kickoff.
3. **Splits by date.** The model is trained on earlier matches and tested on later ones, so no future data leaks into a prediction.
4. **Builds a market benchmark.** Closing odds become implied probabilities, with the bookmaker's margin (overround) removed.
5. **Compares model vs. market** on the same test matches using log loss, Brier score, and calibration plots.
6. **Analyzes disagreements.** Where does the model differ most from the market, and why?
7. *(Optional)* **Adds an expected-goals (xG) feature** from [StatsBomb open data](https://github.com/statsbomb/open-data).

## Results

_To be filled in once the evaluation runs._

| Predictor | Log loss ↓ | Brier score ↓ | Test matches |
|---|---|---|---|
| Uniform (1/3 each) | — | — | — |
| Model | — | — | — |
| Market (closing, margin removed) | — | — | — |

The full write-up is in [`docs/WRITEUP.md`](docs/WRITEUP.md).

## Repo layout

```
├── src/fpm/            # Project code (importable package)
│   ├── data.py         # Load + clean football-data.co.uk matches
│   ├── split.py        # Date-based train/test split (no leakage)
│   ├── market.py       # Odds → implied probabilities, margin removal
│   ├── model.py        # Goals-based baseline model
│   └── metrics.py      # Log loss, Brier score, calibration bins
├── scripts/            # Command-line entry points (download data, run eval)
├── notebooks/          # Exploration and chart notebooks
├── tests/              # Unit tests (pytest)
├── data/raw/           # Downloaded CSVs (not committed)
├── data/processed/     # Cleaned tables (not committed)
├── figures/            # Charts used in the write-up
└── docs/               # Plan, methodology, data notes, write-up
```

## Getting started

```bash
git clone https://github.com/<your-username>/football-prediction-model.git
cd football-prediction-model
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

pytest                                  # run the unit tests
python scripts/download_data.py         # fetch Premier League seasons (needs internet)
```

## Docs

- [`docs/PLAN.md`](docs/PLAN.md): milestones and timeline
- [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md): model, split, margin removal, metrics
- [`docs/DATA.md`](docs/DATA.md): data sources, columns used, known caveats
- [`docs/WRITEUP.md`](docs/WRITEUP.md): the ~1,000-word write-up (draft)

## Data sources & attribution

- Match results, statistics, and odds: [football-data.co.uk](https://www.football-data.co.uk/). Raw data is not redistributed in this repo; the download script fetches it.
- Optional xG work: [StatsBomb Open Data](https://github.com/statsbomb/open-data). Use is subject to StatsBomb's user agreement, and published work based on it should credit StatsBomb as the data source.

## License

Code is released under the MIT License (see [`LICENSE`](LICENSE)). Data belongs to its respective providers.
