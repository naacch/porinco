"""Custom TreeView widget for displaying."""

from tkinter import ttk

import pandas as pd


class CustomTreeview(ttk.Treeview):
    """Custom Treeview widget for displaying data."""

    # TODO: parent typehint
    def __init__(self, parent: ..., **kwargs) -> None:
        """Initializes the CustomTreeview object."""
        super().__init__(parent, **kwargs)

    # TODO: modularizar
    def display_data(self, data: pd.DataFrame) -> None:
        """Display data in the treeview, including the index as the first column."""

        if not data.index.name:
            data.index.name = "idx"  # TODO: cambia el nombre de la columna

        data = data.copy().round(3).reset_index()  # TODO: cambiar

        self.delete_data()

        self["columns"] = list(data.columns)
        self["show"] = "headings"

        for column in self["columns"]:
            self.heading(column, text=column)

        for row in data.itertuples(index=False, name=None):
            self.insert("", "end", values=row)

    def delete_data(self) -> None:
        """Delete all items in the treeview."""
        self.delete(*self.get_children())
