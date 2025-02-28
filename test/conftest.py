"""Configuration for pytest."""

import os
import sys

import pandas as pd
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))


@pytest.fixture
def sample_data():
    """Return sample data."""
    path = os.path.join(os.path.dirname(__file__), "datasets", "data.xlsx")
    return pd.read_excel(path, index_col=0, nrows=5, usecols=range(5), header=0)
