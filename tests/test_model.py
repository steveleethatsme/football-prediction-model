import numpy as np
import pytest
from scipy.stats import poisson, skellam

from fpm.model import outcome_probs


def test_probs_sum_to_one():
    assert outcome_probs(1.5, 1.1).sum() == pytest.approx(1.0)


def test_symmetric_rates_give_equal_win_probs():
    p = outcome_probs(1.3, 1.3)
    assert p[0] == pytest.approx(p[2])


def test_stronger_home_rate_favors_home():
    p = outcome_probs(2.2, 0.8)
    assert p[0] > p[2]


def test_matches_skellam_difference():
    # X - Y for independent Poissons is Skellam-distributed, giving an exact check.
    lh, la = 1.6, 1.1
    p = outcome_probs(lh, la, max_goals=15)
    assert p[1] == pytest.approx(skellam.pmf(0, lh, la), abs=1e-8)
    assert p[0] == pytest.approx(skellam.sf(0, lh, la), abs=1e-8)


def test_truncation_mass_is_negligible():
    goals = np.arange(11)
    assert 1 - poisson.pmf(goals, 3.0).sum() < 1e-3
