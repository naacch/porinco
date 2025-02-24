"""Custom TreeView widget for displaying."""

from tkinter import ttk

import customtkinter as ctk
import pandas as pd

SCROLLBAR_FG_COLOR = ("#E0E0E0", "#363636")  # FIXME: hardocdeado


class CustomTreeview(ttk.Treeview):
    """Custom Treeview widget for displaying data."""

    # TODO: parent typehint
    def __init__(self, parent: ..., **kwargs) -> None:
        """Initializes the CustomTreeview object."""
        super().__init__(parent, **kwargs)
        self.x_scrollbar = None
        self.y_scrollbar = None

    def add_horizontal_scrollbar(self) -> None:
        """Add an horizontal scrollbar to the treeview."""
        self.x_scrollbar = ctk.CTkScrollbar(
            self,
            fg_color=SCROLLBAR_FG_COLOR,
            orientation="horizontal",
            command=self.xview,
        )
        self.configure(xscrollcommand=self.x_scrollbar.set)
        self.x_scrollbar.pack(side="bottom", fill="x")

    def add_vertical_scrollbar(self) -> None:
        """Add a vertical scrollbar to the treeview."""
        self.y_scrollbar = ctk.CTkScrollbar(
            self,
            fg_color=SCROLLBAR_FG_COLOR,
            orientation="vertical",
            command=self.yview,
        )
        self.configure(yscrollcommand=self.y_scrollbar.set)
        self.y_scrollbar.pack(side="right", fill="y")

    def _format_data(self, data: pd.DataFrame, show_idx: bool = True) -> pd.DataFrame:
        """Format the data to be displayed in the treeview."""
        if not data.index.name:
            data.index.name = "idx"  # TODO: cambia el nombre de la columna
        data = data.copy().round(3)
        return data.reset_index() if show_idx else data

    def _toggle_scrollbars(self) -> None:
        """d"""
        # TODO

    def display_data(self, data: pd.DataFrame, show_idx: bool = True) -> None:
        """Display data in the treeview."""

        self.delete_data()

        data = self._format_data(data, show_idx)

        self["columns"] = list(data.columns)
        self["show"] = "headings"

        for column in self["columns"]:
            self.heading(column, text=column)

        for row in data.itertuples(index=False, name=None):
            self.insert("", "end", values=row)

    def delete_data(self) -> None:
        """Delete all items in the treeview."""
        self.delete(*self.get_children())
