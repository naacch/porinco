"""Main window presenter."""

import tkinter as tk
from typing import Protocol

import pandas as pd

from . import _norm

FILETYPES = [
    ("CSV", "*.csv"),
    ("Excel", "*.xlsx"),  # TODO: add .xls
    ("Parquet", "*.parquet"),
    ("Pickle", "*.pkl"),
]


class Window(Protocol):
    """Window protocol."""


class Model(Protocol):
    """Model protocol."""

    def read_data(self, filepath: str, *args, **kwargs) -> pd.DataFrame: ...
    def apply_norm(self, norm: ..., neg_vars: ..., new_range: ...) -> pd.DataFrame: ...


class MainPresenter:
    """Presenter for the main window."""

    # TODO: typehints
    def __init__(
        self,
        main_window: Window,
        main_model: Model,
        normalizations: dict[str, _norm.Norm],  # TODO: typehints
    ) -> None:
        """Create the main window presenter."""
        self.main_window = main_window
        self.main_model = main_model
        self.normalizations = normalizations
        self.selected_norm = None

    def _get_filepath(self) -> str | None:
        """Get the path of the file."""
        path = tk.filedialog.askopenfilename(
            initialdir="/",
            title="Select file",
            filetypes=FILETYPES,
        )
        return path

    def open_file(self) -> None:
        """Open a file."""
        filepath = self._get_filepath()
        if not filepath:
            tk.messagebox.showerror("ERROR", "No file selected.")
            return
        data = self.main_model.read_data(filepath, index_col=0)
        self.main_window.treeview.display_data(data)

    def export_file(self) -> None:
        """Export a file."""

    def update_selected_norm(self, norm: str) -> None:
        """Update the selected normalization."""
        self.selected_norm = self.normalizations.get(norm)

    def apply_and_display_norm(self) -> None:
        """Apply and display the selected normalization."""
        if not self.selected_norm:
            tk.messagebox.showerror("ERROR", "No normalization selected.")
            return

        data = self.main_model.apply_norm(
            self.selected_norm(self.main_model.raw_data),
            neg_vars=[],  # FIXME: hardcodeado, falta range
        )
        self.main_window.treeview.display_data(data)
