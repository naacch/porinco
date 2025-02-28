"""Test the norm module."""

import pandas as pd
import pytest

from porinco.core.processing import norm as n

NORM_CONFIG = [
    {
        "class": n.Balanced,
        "params": ["min_value", "max_value", "median"],
    },
    {
        "class": n.MinMax,
        "params": ["min_value", "max_value"],
    },
    {
        "class": n.Classic,
        "params": ["mean", "std"],
    },
]

# TODO: agregar test
