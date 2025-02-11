"""Main model for the application."""

from typing import Protocol

import pandas as pd

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
        self.raw_data = None

    def read_data(self, filepath: str, *args, **kwargs) -> pd.DataFrame:
        """Read a file."""
        filetype = filepath.split(".")[-1]
        return READ_FUNCTIONS.get(filetype)(filepath, *args, **kwargs)
