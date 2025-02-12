"""Main window presenter."""

import tkinter as tk
from typing import Protocol

import pandas as pd

FILETYPES = [
    ("CSV", "*.csv"),
    ("Excel", "*.xlsx"),  # TODO: add .xls
    ("Parquet", "*.parquet"),
    ("Pickle", "*.pkl"),
]


class MainWindow(Protocol):
    """View protocol."""


class Model(Protocol):
    """Model protocol."""

    def read_data(self, filepath: str, *args, **kwargs) -> pd.DataFrame:
        """Read data."""


class MainPresenter:
    """Presenter for the main window."""

    # TODO: typehints
    def __init__(self, main_window: ..., main_model: Model) -> None:
        """Create the main window presenter."""
        self.main_window = main_window
        self.main_model = main_model

    def _get_filepath(self) -> str | None:
        """Get the path of the file."""
        path = tk.filedialog.askopenfilename(
            initialdir="/",
            title="Select file",
            filetypes=FILETYPES,
        )
        return path

    def open_file(self) -> pd.DataFrame:
        """Open a file."""
        filepath = self._get_filepath()
        if not filepath:
            tk.messagebox.showerror("Error", "No file selected.")
            return
        self.main_model.raw_data = self.main_model.read_data(filepath, index_col=0)
        self.main_window.treeview.display_data(self.main_model.raw_data)

    def export_file(self) -> pd.DataFrame:
        """Export a file."""
