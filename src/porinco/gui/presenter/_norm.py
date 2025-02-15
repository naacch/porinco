"""Private module for normalization classes."""

import dataclasses
from typing import Protocol

import pandas as pd


class Norm(Protocol):
    """Protocol for normalization classes."""

    def fit(self) -> None: ...
    def transform(self) -> pd.DataFrame: ...
    def inverse_transform(self) -> pd.DataFrame: ...


@dataclasses.dataclass
class Range:
    """d"""

    min_value: float
    max_value: float
