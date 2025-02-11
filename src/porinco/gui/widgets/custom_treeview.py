"""Custom TreeView widget for displaying."""

from tkinter import ttk

import pandas as pd


class CustomTreeview(ttk.Treeview):
    """Custom Treeview widget for displaying data."""

    # TODO: parent typehint
    def __init__(self, parent: ..., **kwargs) -> None:
        """Initializes the CustomTreeview object."""
        super().__init__(parent, **kwargs)

    def insert_data(self, data: pd.DataFrame) -> None:
        """Insert data into the treeview."""

    def delete_data(self) -> None:
        """Delete all items in the treeview."""
        self.delete(*self.get_children())
