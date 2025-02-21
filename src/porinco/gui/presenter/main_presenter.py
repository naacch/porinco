"""Main window presenter."""

from __future__ import annotations

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

NORM_FIXED_RANGE = {"balanced": _norm.Range(70, 130)}
ICON_PATH = "src/porinco/gui/resources/icon.ico"


class MainWindow(Protocol):
    def create_ui(self, presenter: MainPresenter) -> None: ...
    def create_polarity_window(self, vars: list[str]) -> ...: ...
    def mainloop(self) -> None: ...
    def change_icon(self, icon_path: str) -> None: ...


class Model(Protocol):

    neg_vars: list[str]

    def read_data(self, filepath: str, *args, **kwargs) -> pd.DataFrame: ...
    def apply_norm(self, norm: ..., neg_vars: ..., new_range: ...) -> pd.DataFrame: ...


class MainPresenter:
    """Presenter for the main window."""

    # TODO: typehints
    def __init__(
        self,
        main_window: MainWindow,
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

    def open_polarity_window(self) -> None:
        """Open the polarity window."""
        vars = self.main_model.raw_data.columns.tolist()

        if not vars:
            tk.messagebox.showerror("ERROR", "No data to apply polarity.")
            return

        polarity_window = self.main_window.create_polarity_window(
            self.main_model.raw_data.columns.tolist()
        )
        polarity_window._create_widgets(self)
        polarity_window.grab_set()

    def update_selected_norm(self, norm: str) -> None:
        """Update the selected normalization."""
        self.selected_norm = norm

    def apply_and_display_norm(self) -> None:
        """Apply and display the selected normalization."""
        if not (norm := self.normalizations.get(self.selected_norm)):
            tk.messagebox.showerror("ERROR", "No normalization selected.")
            return

        data = self.main_model.apply_norm(
            norm(self.main_model.raw_data), NORM_FIXED_RANGE.get(self.selected_norm)
        )
        self.main_window.treeview.display_data(data)

    def update_negative_variables(self, neg_vars: list[str]) -> None:
        """Update the negative variables."""
        self.main_model.neg_vars = neg_vars

    def run(self) -> None:
        """Run the main window."""
        self.main_window.create_ui(self)
        self.main_window.change_icon(ICON_PATH)
        self.main_window.mainloop()
