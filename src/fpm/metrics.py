"""Scoring rules and calibration for 3-way (H/D/A) probability forecasts.

Conventions: `probs` is shape (n, 3) in order (H, D, A); `outcomes` is length n with
values in {"H", "D", "A"} or integer indices {0, 1, 2}.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from fpm import OUTCOMES

_EPS = 1e-15


def outcome_index(outcomes) -> np.ndarray:
    arr = np.asarray(outcomes)
    if arr.dtype.kind in "iu":
        return arr.astype(int)
    lookup = {k: i for i, k in enumerate(OUTCOMES)}
    return np.array([lookup[o] for o in arr], dtype=int)


def one_hot(outcomes) -> np.ndarray:
    idx = outcome_index(outcomes)
    out = np.zeros((len(idx), 3))
    out[np.arange(len(idx)), idx] = 1.0
    return out


def log_loss(probs, outcomes) -> float:
    """Mean of -log p(actual outcome). Uniform (1/3 each) scores ln 3 ~= 1.0986."""
    p = np.asarray(probs, dtype=float)
    idx = outcome_index(outcomes)
    p_actual = np.clip(p[np.arange(len(idx)), idx], _EPS, 1.0)
    return float(-np.mean(np.log(p_actual)))


def brier_score(probs, outcomes) -> float:
    """Mean over matches of sum_k (p_k - o_k)^2. Multi-class version, range [0, 2]."""
    p = np.asarray(probs, dtype=float)
    return float(np.mean(np.sum((p - one_hot(outcomes)) ** 2, axis=1)))


def calibration_table(probs, outcomes, outcome: str = "H", n_bins: int = 10) -> pd.DataFrame:
    """Equal-width bins of predicted P(outcome); mean predicted vs. observed frequency."""
    k = OUTCOMES.index(outcome)
    p = np.asarray(probs, dtype=float)[:, k]
    hit = (outcome_index(outcomes) == k).astype(float)
    edges = np.linspace(0.0, 1.0, n_bins + 1)
    bins = np.clip(np.digitize(p, edges[1:-1]), 0, n_bins - 1)
    df = pd.DataFrame({"bin": bins, "pred": p, "hit": hit})
    table = df.groupby("bin").agg(mean_pred=("pred", "mean"), observed=("hit", "mean"), count=("hit", "size"))
    table["bin_lo"] = edges[table.index]
    table["bin_hi"] = edges[table.index + 1]
    return table.reset_index(drop=True)[["bin_lo", "bin_hi", "mean_pred", "observed", "count"]]


def bootstrap_logloss_diff(probs_a, probs_b, outcomes, n_boot: int = 2000, seed: int = 0):
    """Bootstrap the difference log_loss(a) - log_loss(b) over matches.

    Returns (point_estimate, (lo, hi)) with a 95% percentile interval. Negative = a is better.
    """
    rng = np.random.default_rng(seed)
    idx = outcome_index(outcomes)
    n = len(idx)
    rows = np.arange(n)
    la = -np.log(np.clip(np.asarray(probs_a, float)[rows, idx], _EPS, 1.0))
    lb = -np.log(np.clip(np.asarray(probs_b, float)[rows, idx], _EPS, 1.0))
    d = la - lb
    samples = rng.integers(0, n, size=(n_boot, n))
    boots = d[samples].mean(axis=1)
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return float(d.mean()), (float(lo), float(hi))
