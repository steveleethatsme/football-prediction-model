import pandas as pd

from fpm.split import split_by_date, walk_forward_windows


def _matches():
    dates = pd.date_range("2024-08-01", periods=40, freq="3D")
    return pd.DataFrame({"date": dates, "x": range(40)})


def test_split_has_no_overlap_and_respects_cutoff():
    df = _matches()
    train, test = split_by_date(df, "2024-09-15")
    assert train["date"].max() < pd.Timestamp("2024-09-15") <= test["date"].min()
    assert len(train) + len(test) == len(df)


def test_walk_forward_history_is_strictly_before_chunk():
    df = _matches()
    seen = 0
    for history, chunk in walk_forward_windows(df, "2024-09-15", freq="7D"):
        assert history["date"].max() < chunk["date"].min()
        seen += len(chunk)
    _, test = split_by_date(df, "2024-09-15")
    assert seen == len(test)  # every test match predicted exactly once
