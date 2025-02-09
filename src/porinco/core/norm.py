"""Normalization classes and functions."""

from abc import ABC, abstractmethod
from typing import NamedTuple

import pandas as pd


class Range(NamedTuple):
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
        pass

    @abstractmethod
    def _transform(self) -> pd.DataFrame:
        """Applies normalization using precomputed values."""
        pass

    def transform(self) -> pd.DataFrame:
        """Validates parameters and applies transformation."""
        self._validate_params(self._required_params())
        return self._transform()

    @abstractmethod
    def _required_params(self) -> set[str]:
        """Defines the set of required parameters for validation."""
        pass

    @abstractmethod
    def inverse_transform(self) -> pd.DataFrame:
        """Applies inverse transformation."""
        pass


class LinealNorm(Norm):
    """Abstract base class for normalization with inverse transformation."""

    def inverse_transform(self) -> pd.DataFrame:
        """Applies inverse transformation."""
        return 1 - self._transform()


class Classic(LinealNorm):

    def __init__(self, data) -> None:
        super().__init__(data)

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

    def __init__(self, data) -> None:
        super().__init__(data)

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


class Balanced(LinealNorm):
    """Balanced Normalization: Scales data between -1 and 1."""

    def __init__(self, data) -> None:
        super().__init__(data)

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

    def _required_params(self) -> set[str]:
        """Defines the required parameters for transformation."""
        return {"median", "min_value", "max_value"}


def change_range(data: pd.DataFrame, new_range: Range) -> pd.DataFrame:
    """d"""

    return (
        data * (new_range.max_value - new_range.min_value) / 2
        + (new_range.max_value + new_range.min_value) / 2
    )


def apply_norm(
    norm: Norm, neg_vars: list[str] | None = None, new_range: Range | None = None
) -> pd.DataFrame:
    """d"""
    norm.fit()
    norm_data = norm.transform()
    if neg_vars:
        # FIXME: esto es una mierda, se invierte todo el dataframe y despues se filtra, deberia ser al reves
        norm_data[neg_vars] = norm.inverse_transform()[neg_vars]
    if new_range:
        norm_data = change_range(norm_data, new_range)
    return norm_data
