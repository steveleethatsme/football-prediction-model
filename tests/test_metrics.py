import math

import numpy as np
import pytest

from fpm.metrics import bootstrap_logloss_diff, brier_score, calibration_table, log_loss


def test_uniform_log_loss_is_ln3():
    probs = np.full((4, 3), 1 / 3)
    assert log_loss(probs, ["H", "D", "A", "H"]) == pytest.approx(math.log(3))


def test_perfect_forecast_scores_zero():
    probs = np.array([[1.0, 0, 0], [0, 1.0, 0], [0, 0, 1.0]])
    outcomes = ["H", "D", "A"]
    assert log_loss(probs, outcomes) == pytest.approx(0.0, abs=1e-12)
    assert brier_score(probs, outcomes) == pytest.approx(0.0)


def test_brier_worst_case_is_two():
    probs = np.array([[0, 0, 1.0]])
    assert brier_score(probs, ["H"]) == pytest.approx(2.0)


def test_brier_uniform():
    # (1/3 - 1)^2 + 2 * (1/3)^2 = 4/9 + 2/9 = 2/3
    probs = np.full((1, 3), 1 / 3)
    assert brier_score(probs, ["D"]) == pytest.approx(2 / 3)


def test_integer_and_string_outcomes_agree():
    probs = np.array([[0.5, 0.3, 0.2], [0.2, 0.3, 0.5]])
    assert log_loss(probs, ["H", "A"]) == pytest.approx(log_loss(probs, np.array([0, 2])))


def test_calibration_on_calibrated_simulation():
    rng = np.random.default_rng(1)
    n = 20000
    p_home = rng.uniform(0.1, 0.8, n)
    rest = 1 - p_home
    probs = np.column_stack([p_home, rest / 2, rest / 2])
    u = rng.uniform(size=n)
    outcomes = np.where(u < probs[:, 0], 0, np.where(u < probs[:, 0] + probs[:, 1], 1, 2))
    table = calibration_table(probs, outcomes, "H", n_bins=10)
    assert table["count"].sum() == n
    assert np.max(np.abs(table["mean_pred"] - table["observed"])) < 0.03


def test_bootstrap_identical_predictors_gives_zero():
    probs = np.array([[0.5, 0.3, 0.2]] * 50)
    outcomes = ["H"] * 25 + ["A"] * 25
    est, (lo, hi) = bootstrap_logloss_diff(probs, probs, outcomes, n_boot=200)
    assert est == 0.0 and lo == 0.0 and hi == 0.0
