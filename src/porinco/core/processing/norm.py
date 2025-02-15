"""Normalization classes and functions."""

from abc import ABC, abstractmethod
from typing import NamedTuple

import pandas as pd


class Range(NamedTuple):
    """d"""

    min_value: float
    max_value: float


class Norm(ABC):
    """Abstract base class for normalization."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data.copy()
        self.params = {}

    def _validate_params(self, names: set[str]) -> None:
        """Checks if required parameters have been computed before transformation."""
        missing = names - self.params.keys()
        if missing:
            raise ValueError(
                f"Missing required parameters: {missing}. "
                "Call `fit` before `transform`."
            )

    @abstractmethod
    def fit(self) -> None:
        """Computes necessary values for normalization."""

    @abstractmethod
    def _transform(self) -> pd.DataFrame:
        """Applies normalization using precomputed values."""

    def transform(self) -> pd.DataFrame:
        """Validates parameters and applies transformation."""
        self._validate_params(self._required_params())
        return self._transform()

    @abstractmethod
    def _required_params(self) -> set[str]:
        """Defines the set of required parameters for validation."""

    @abstractmethod
    def inverse_transform(self) -> pd.DataFrame:
        """Applies inverse transformation."""


class LinealNorm(Norm):
    """Abstract base class for normalization with inverse transformation."""

    def inverse_transform(self) -> pd.DataFrame:
        """Applies inverse transformation."""
        return 1 - self._transform()


class Classic(LinealNorm):
    """Classic normalization."""

    def fit(self) -> None:
        """Computes mean and standard deviation for normalization."""
        self.params["mean"] = self.data.mean()
        self.params["std"] = self.data.std()

    def _required_params(self) -> set[str]:
        """d"""
        return {"mean", "std"}

    def _transform(self) -> pd.DataFrame:
        """d"""
        if any(self.params["std"] == 0):
            raise ZeroDivisionError("Standard deviation is zero.")

        return (self.data - self.params["mean"]) / self.params["std"]


class MinMaxNorm(LinealNorm):
    """Min-max normalization."""

    def fit(self) -> None:
        """Computes the minimum and maximum values for normalization."""
        self.params["min_value"] = self.data.min()
        self.params["max_value"] = self.data.max()

    def _transform(self) -> pd.DataFrame:
        """Applies min-max normalization."""

        is_zero = (self.params["max_value"] - self.params["min_value"]) == 0
        if any(is_zero):
            raise ZeroDivisionError("")  # TODO: add message

        return (self.data - self.params["min_value"]) / (
            self.params["max_value"] - self.params["min_value"]
        )

    def _required_params(self) -> set[str]:
        """Defines the required parameters for transformation."""
        return {"min_value", "max_value"}


class Balanced(Norm):
    """Balanced Normalization: Scales data between -1 and 1."""

    def fit(self) -> None:
        """Computes the median, minimum, and maximum values for normalization."""
        self.params["median"] = self.data.median()
        self.params["min_value"] = self.data.min()
        self.params["max_value"] = self.data.max()

    def _transform(self) -> pd.DataFrame:
        """Applies balanced normalization."""
        median = self.params["median"]
        min_value = self.params["min_value"]
        max_value = self.params["max_value"]

        # xd
        norm_data = (self.data - median) / (max_value - median)
        norm_data[self.data <= median] = (self.data[self.data <= median] - median) / (
            median - min_value
        )
        return norm_data

    def inverse_transform(self) -> pd.DataFrame:
        """Applies inverse transformation."""
        median = self.params["median"]
        min_value = self.params["min_value"]
        max_value = self.params["max_value"]

        # xd
        norm_data = (median - self.data) / (max_value - median)
        norm_data[self.data <= median] = (median - self.data[self.data <= median]) / (
            median - min_value
        )
        return norm_data

    def _required_params(self) -> set[str]:
        """Defines the required parameters for transformation."""
        return {"median", "min_value", "max_value"}


NORMALIZATIONS = {
    "classic": Classic,
    "min_max": MinMaxNorm,
    "balanced": Balanced,
}
