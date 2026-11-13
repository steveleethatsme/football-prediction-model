"""Goals-based baseline: home and away goals as independent Poisson random variables.

    log λ_home = μ + h + attack[home] − defense[away]
    log λ_away = μ + attack[away] − defense[home]

See docs/METHODOLOGY.md §3.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from scipy.stats import poisson


def outcome_probs(lam_home: float, lam_away: float, max_goals: int = 10) -> np.ndarray:
    """P(H), P(D), P(A) from two independent Poisson goal counts.

    Builds the joint score matrix P(X=i, Y=j) = P(X=i) P(Y=j) for i, j <= max_goals,
    sums below / on / above the diagonal, and renormalizes for the truncated tail.
    """
    goals = np.arange(max_goals + 1)
    px = poisson.pmf(goals, lam_home)
    py = poisson.pmf(goals, lam_away)
    joint = np.outer(px, py)  # rows = home goals i, cols = away goals j
    p_home = np.tril(joint, k=-1).sum()  # i > j
    p_draw = np.trace(joint)  # i == j
    p_away = np.triu(joint, k=1).sum()  # i < j
    p = np.array([p_home, p_draw, p_away])
    return p / p.sum()


@dataclass
class PoissonModel:
    """Attack/defense/home-advantage Poisson model, fit by maximum likelihood.

    TODO (M3): implement `fit` and `predict_rates`. Suggested approach:
      1. Map team names to integer ids.
      2. Parameter vector θ = [μ, h, attack (n_teams), defense (n_teams)].
      3. Negative log-likelihood = -Σ [log Poisson(FTHG | λ_home) + log Poisson(FTAG | λ_away)]
         (optionally weighted by a time-decay factor per match).
      4. Enforce identifiability, e.g. fix Σ attack = 0 and Σ defense = 0
         (reparameterize, or add a penalty).
      5. Minimize with scipy.optimize.minimize.
      6. Decide what to do with teams not seen in training (promoted sides).
    """

    max_goals: int = 10
    params_: dict = field(default_factory=dict)

    def fit(self, matches: pd.DataFrame) -> "PoissonModel":
        raise NotImplementedError("M3: implement maximum likelihood fit")

    def predict_rates(self, matches: pd.DataFrame) -> np.ndarray:
        """Return an (n, 2) array of (λ_home, λ_away) for each match."""
        raise NotImplementedError("M3: implement after fit")

    def predict_proba(self, matches: pd.DataFrame) -> np.ndarray:
        """Return an (n, 3) array of (P(H), P(D), P(A))."""
        rates = self.predict_rates(matches)
        return np.vstack([outcome_probs(lh, la, self.max_goals) for lh, la in rates])
