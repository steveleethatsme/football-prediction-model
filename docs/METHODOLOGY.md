# Methodology

Written so every step can be explained with CSE 312-level probability: random variables, the Poisson distribution, independence, maximum likelihood, expectation, and scoring rules.

## 1. Prediction target

For each match, predict a probability vector **p = (p_H, p_D, p_A)** with p_H + p_D + p_A = 1. The outcome is one of {H, D, A}.

## 2. No leakage: date-based evaluation

- Sort matches by kickoff date.
- **Train period:** earlier seasons. **Test period:** later season(s). Never shuffle.
- **Walk-forward (recommended):** step through the test period in chunks (e.g., one matchweek or one calendar week). Before each chunk, refit the model on *all matches strictly before that chunk*, then predict the chunk. This mimics what you'd actually know on the morning of each match.
- Closing odds are used **only** as the comparison benchmark, never as a model input.
- Open question: newly promoted teams have no Premier League history in the training data. Decide on a prior (e.g., give promoted teams the average rating of past promoted teams) and document it.

Implemented in `src/fpm/split.py` (`split_by_date`, `walk_forward_windows`).

## 3. Baseline model: goals as Poisson random variables

The simplest goals-based model: home goals X and away goals Y are independent Poisson random variables:

- X ~ Poisson(λ_home), Y ~ Poisson(λ_away)
- log λ_home = μ + h + attack[home] − defense[away]
- log λ_away = μ + attack[away] − defense[home]

where μ is a baseline scoring rate, h is home advantage, and each team has an attack and a defense rating. Add a constraint (e.g., ratings sum to 0) so the parameters are identifiable.

**Fitting:** maximum likelihood. The log-likelihood is a sum of Poisson log-PMFs over training matches; maximize it numerically (e.g., `scipy.optimize.minimize` on the negative log-likelihood).

**Optional:** weight recent matches more (e.g., exponential time decay), since team strength changes over time. Tune the decay rate on training data only.

**From goals to outcomes** (implemented in `fpm.model.outcome_probs`):

- P(X = i, Y = j) = P(X = i) · P(Y = j) (independence)
- p_H = Σ_{i > j} P(X = i, Y = j), p_D = Σ_i P(X = i, Y = i), p_A = Σ_{i < j} P(X = i, Y = j)
- Truncate at a maximum goal count (e.g., 10) and renormalize. The truncated mass is tiny, and the tests check this.

**Known limitation to discuss in the write-up:** independent Poisson tends to under-predict draws. Measure whether that happens here using the calibration plot for p_D.

## 4. Market benchmark: closing odds → probabilities

Decimal odds o_k for outcome k imply raw probability q_k = 1 / o_k.

- The **overround** is Σ_k q_k − 1 > 0. That's the bookmaker's margin.
- **Proportional margin removal:** p_k = q_k / Σ_j q_j. Simple, easy to explain, and the method used here. Other margin-removal methods exist; mention that in the write-up as a limitation, not a focus.
- Which odds count as "the market": decide in M2 between a single sharp-ish bookmaker (e.g., Pinnacle closing, `PSC*`) and the market average (`AvgC*`). Report which one and why. Check that the column coverage is complete for the test period.

Implemented in `src/fpm/market.py`.

## 5. Evaluation metrics

All metrics are computed on **the same set of test matches** for every predictor.

**Log loss** (lower is better): mean of −log p_{actual outcome}. A confident wrong prediction is punished heavily.
- Reference point: the uniform predictor (1/3 each) scores ln 3 ≈ 1.0986.

**Brier score** (lower is better): mean over matches of Σ_k (p_k − o_k)², where o is the one-hot actual outcome. This multi-class version ranges from 0 to 2. State this definition in the write-up, since some sources divide by the number of classes.

**Calibration:** for each outcome type (H, D, A), bin predictions by predicted probability (e.g., 10 equal-width bins). In each bin, compare the mean predicted probability with the observed frequency. A well-calibrated predictor lies near the diagonal. Show bin counts too, since sparse bins are noisy.

**Uncertainty:** report a bootstrap confidence interval for the *difference* in log loss (model − market), resampling test matches. Without it, a small difference could just be noise.

Implemented in `src/fpm/metrics.py`.

## 6. Baselines to report alongside model and market

1. Uniform: (1/3, 1/3, 1/3)
2. Base rates: training-period frequencies of H/D/A
3. Model
4. Market (closing, margin removed)

The model is "useful" if it clearly beats 1–2. How far it sits from 4 is the honest headline.

## 7. Disagreement analysis

- Per match, compute a disagreement measure, e.g., |p_H^model − p_H^market| or the KL divergence from market to model.
- Look at the top-N disagreements: who was closer on average? Is the disagreement concentrated in certain teams (promoted sides, teams that changed managers), certain times of the season (early-season, when the model has stale ratings), or certain outcome types (draws)?
- Be careful: on a small sample, "the model was right in these 20 games" is weak evidence. Use the log-loss comparison restricted to high-disagreement matches, with a bootstrap CI.
