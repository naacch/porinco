import pandas as pd
import pytest


@pytest.fixture
def df():
    return pd.DataFrame({"foo": [1, 2, 3], "bar": [10, 20, 70]})


@pytest.fixture
def zero_df():
    return pd.DataFrame({"foo": [0, 0, 0], "bar": [0, 0, 0]})
