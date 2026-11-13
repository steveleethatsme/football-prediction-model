import numpy as np
import pytest

from fpm.market import implied_probs, overround, remove_margin_proportional


def test_fair_odds_have_zero_overround():
    odds = np.array([[3.0, 3.0, 3.0]])
    assert overround(odds)[0] == pytest.approx(0.0)
    assert remove_margin_proportional(odds)[0] == pytest.approx([1 / 3, 1 / 3, 1 / 3])


def test_margin_removed_rows_sum_to_one():
    odds = np.array([[1.90, 3.60, 4.20], [2.50, 3.30, 2.90]])
    p = remove_margin_proportional(odds)
    assert p.sum(axis=1) == pytest.approx([1.0, 1.0])
    assert np.all(overround(odds) > 0)


def test_proportional_keeps_ratios():
    odds = np.array([[2.0, 4.0, 4.0]])
    q = implied_probs(odds)[0]
    p = remove_margin_proportional(odds)[0]
    assert p[0] / p[1] == pytest.approx(q[0] / q[1])


def test_rejects_invalid_odds():
    with pytest.raises(ValueError):
        implied_probs([[1.0, 3.0, 3.0]])
