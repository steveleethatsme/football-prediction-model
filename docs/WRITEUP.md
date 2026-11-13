# How Close Can a Simple Model Get to the Betting Market?

_Draft skeleton. Target ≈ 1,000 words, 3–4 charts. Word budgets are guides, not rules._

## 1. The question (~120 words)

- What's being predicted (H/D/A probabilities for Premier League matches)
- Why compare against closing odds: they're a strong, public benchmark
- The framing: not "beating the bookies," but how good a well-calibrated simple model can be

## 2. Data (~120 words)

- football-data.co.uk, seasons ____ to ____, N = ____ matches (train ____ / test ____)
- What was dropped and why (missing odds, etc.)

## 3. The model (~200 words)

- Goals as independent Poisson random variables; attack/defense/home advantage
- Maximum likelihood fit; walk-forward refitting so no future data leaks in
- How goal probabilities become H/D/A probabilities

## 4. Turning odds into probabilities (~120 words)

- 1/odds, the overround, proportional normalization
- Which bookmaker/average was used, and the typical margin observed: ____%

## 5. Results (~250 words)

**Chart 1: Results table / bar chart.** Log loss and Brier for uniform, base rates, model, market, with a bootstrap CI on model − market.

**Chart 2: Calibration plot.** Model vs. market, for home wins (and draws if interesting).

- Headline numbers, stated plainly
- Is the difference statistically meaningful?

## 6. Where the model and market disagree (~150 words)

**Chart 3: Disagreement scatter.** Model p_H vs. market p_H, colored by outcome.

- Patterns in the biggest disagreements (promoted teams, early season, draws…)
- Who tended to be right

## 7. Limitations and next steps (~80 words)

- Independence assumption / draw under-prediction
- No lineup/injury information; closing odds include it
- Possible extensions: xG features, time decay tuning, other margin-removal methods

**Optional Chart 4:** draw-rate calibration, or model log loss by matchweek.

---
_Data: football-data.co.uk. (If xG is used: StatsBomb Open Data, credited per their user agreement.)_
