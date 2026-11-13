"""Turn bookmaker odds into probabilities with the margin removed."""

from __future__ import annotations

import numpy as np


def implied_probs(odds) -> np.ndarray:
    """Raw implied probabilities q_k = 1 / o_k for decimal odds. Shape (n, 3) -> (n, 3)."""
    odds = np.asarray(odds, dtype=float)
    if np.any(odds <= 1.0):
        raise ValueError("Decimal odds must be > 1.")
    return 1.0 / odds


def overround(odds) -> np.ndarray:
    """Bookmaker margin per match: sum_k (1 / o_k) - 1."""
    return implied_probs(odds).sum(axis=-1) - 1.0


def remove_margin_proportional(odds) -> np.ndarray:
    """Proportional normalization: p_k = q_k / sum_j q_j. Rows sum to 1."""
    q = implied_probs(odds)
    return q / q.sum(axis=-1, keepdims=True)
