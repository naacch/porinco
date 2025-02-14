"""Main model for the application."""

from typing import Protocol

import pandas as pd

from . import _norm

READ_FUNCTIONS = {
    "csv": pd.read_csv,
    "parquet": pd.read_parquet,
    "pkl": pd.read_pickle,
    "xls": pd.read_excel,
    "xlsx": pd.read_excel,
}


class Presenter(Protocol):
    """Presenter protocol."""


class MainModel:
    """Model for the main window."""

    def __init__(self) -> None:
        """Create the main model."""
        self.raw_data = pd.DataFrame()
        self.norm_data = pd.DataFrame()

    def read_data(self, filepath: str, *args, **kwargs) -> pd.DataFrame:
        """Read a file."""
        filetype = filepath.split(".")[-1]
        self.raw_data = READ_FUNCTIONS.get(filetype)(filepath, *args, **kwargs)
        return self.raw_data

    @staticmethod
    def _change_range(data: pd.DataFrame, new_range: _norm.Range) -> pd.DataFrame:
        """d"""
        return (
            data * (new_range.max_value - new_range.min_value) / 2
            + (new_range.max_value + new_range.min_value) / 2
        )

    # FIXME: cambiar
    def apply_norm(
        self,
        norm: _norm.Norm,
        neg_vars: list[str] | None = None,
        new_range: _norm.Range | None = None,
    ) -> pd.DataFrame:
        """d"""
        if self.raw_data.empty:
            raise ValueError("No data to normalize.")

        norm.fit()
        self.norm_data = norm.transform()

        if neg_vars:
            # FIXME: esto es una mierda, se invierte todo el dataframe
            # y despues se filtra, deberia ser al reves
            self.norm_data[neg_vars] = norm.inverse_transform()[neg_vars]

        if new_range:
            self.norm_data = self._change_range(self.norm_data, new_range)

        return self.norm_data
