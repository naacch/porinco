"""Main window presenter."""

from __future__ import annotations

import re
import tkinter as tk
from typing import Callable, Protocol

import pandas as pd

from . import _norm

WeightingFunc = Callable[[pd.DataFrame], pd.Series]

FILETYPES = [
    ("CSV", "*.csv"),
    ("Excel", "*.xlsx"),  # TODO: add .xls
    ("Parquet", "*.parquet"),
    ("Pickle", "*.pkl"),
]

NORM_FIXED_RANGE = {"balanced": _norm.Range(70, 130)}
ICON_PATH = "src/porinco/gui/resources/icon.ico"


class MainWindow(Protocol):
    treeview: ...
    min_value_entry: ...
    max_value_entry: ...
    taxonomy_cb: ...

    def create_ui(self, presenter: MainPresenter) -> None: ...
    def create_polarity_window(self, vars: list[str]) -> ...: ...
    def mainloop(self) -> None: ...
    def change_icon(self, icon_path: str) -> None: ...
    def create_weighting_window(self) -> None: ...


class Model(Protocol):

    norm_range: _norm.Range

    def read_data(self, filepath: str, *args, **kwargs) -> pd.DataFrame: ...
    def apply_norm(self, norm: ..., neg_vars: ...) -> pd.DataFrame: ...
    def calculate_weighting(self, weighting_func: WeightingFunc) -> pd.Series: ...
    def calculate_weighted_data(self) -> pd.DataFrame: ...


class MainPresenter:
    """Presenter for the main window."""

    # TODO: typehints
    def __init__(
        self,
        main_window: MainWindow,
        main_model: Model,
        normalizations: dict[str, _norm.Norm],
        weightings: dict[str, Callable],  # TODO: typehints
    ) -> None:
        """Create the main window presenter."""
        self.main_window = main_window
        self.main_model = main_model

        self.normalizations = normalizations
        self.weightings = weightings

        self.selected_norm = None
        self.weighting_func: WeightingFunc | None = None
        self.neg_vars = []

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

    def _update_weighting_func(self, weighting: str) -> None:
        """Update the weighting function."""
        self.weighting_func = self.weightings.get(weighting)

    def open_weighting_window(self) -> None:
        """Open the weighting window."""
        if not self.weighting_func:
            tk.messagebox.showerror("ERROR", "No weighting selected.")
            return

        weighting = self.main_model.calculate_weighting(self.weighting_func)

        weighting_window = self.main_window.create_weighting_window()
        weighting_window._create_widgets(self)
        weighting_window.display_data(pd.DataFrame(weighting).T)

    def norm_option_menu_func(self, norm: str) -> None:
        """Handles normalization option selection and updates range entries."""
        self.clear_entry_txt(self.main_window.min_value_entry)
        self.clear_entry_txt(self.main_window.max_value_entry)

        self._update_selected_norm(norm)

        if fixed_range := NORM_FIXED_RANGE.get(norm):
            self.set_and_lock_entry(
                self.main_window.min_value_entry, fixed_range.min_value
            )
            self.set_and_lock_entry(
                self.main_window.max_value_entry, fixed_range.max_value
            )
            self._update_norm_range(fixed_range)

    # TODO: typehint
    def set_and_lock_entry(self, entry: ..., value: str) -> None:
        """Sets a value to the entry widget and makes it read-only."""
        self.clear_entry_txt(entry)
        entry.insert(0, value)
        entry.configure(state="readonly")

    # TODO: typehint
    def clear_entry_txt(self, entry: ...) -> None:
        """Deletes the text of an entry widget."""
        entry.configure(state="normal")
        entry.delete(0, tk.END)

    def _update_selected_norm(self, norm: str) -> None:
        """Update the selected normalization."""
        self.selected_norm = norm

    def apply_and_display_norm(self) -> None:
        """Apply and display the selected normalization."""
        if not (norm := self.normalizations.get(self.selected_norm)):
            tk.messagebox.showerror("ERROR", "No normalization selected.")
            return

        data = (
            self.main_model.apply_norm(norm(self.main_model.raw_data))
            if self.is_taxonomy_selected()
            else self.main_model.apply_norm(
                norm(self.main_model.raw_data), self.neg_vars
            )
        )

        self.main_window.treeview.display_data(data)

    def _update_negative_variables(self, neg_vars: list[str]) -> None:
        """Update the negative variables."""
        self.neg_vars = neg_vars

    def _update_norm_range(self, norm_range: _norm.Range) -> None:
        """d"""
        self.main_model.norm_range = norm_range

    def is_num(self, s: str) -> bool:
        """d"""
        return bool(re.fullmatch(r"\d*\.?\d*", s))

    def get_new_norm_range(self) -> None:
        """d"""

        min_value = self.main_window.min_value_entry.get()
        max_value = self.main_window.max_value_entry.get()

        if not min_value or not max_value:
            tk.messagebox.showerror("ERROR", "Empty range.")
            return

        if (min_value := float(min_value)) >= (max_value := float(max_value)):
            tk.messagebox.showerror("ERROR", "Invalid range.")
            return

        self._update_norm_range(_norm.Range(min_value, max_value))

    def is_taxonomy_selected(self) -> bool:
        """Get the selected taxonomy value."""
        return bool(self.main_window.taxonomy_cb.get())

    def calculate_and_display_weighted_data(self) -> None:
        """Calculate and display the weighted data."""
        weighted_data = self.main_model.calculate_weighted_data()
        self.main_window.treeview.display_data(weighted_data)

    def run(self) -> None:
        """Run the main window."""
        self.main_window.create_ui(self)
        self.main_window.change_icon(ICON_PATH)
        self.main_window.mainloop()
