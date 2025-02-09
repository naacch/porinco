"""Custom TreeView widget for displaying."""

from tkinter import ttk


class CustomTreeview(ttk.Treeview):
    """Custom Treeview widget for displaying data."""

    # TODO: parent typehint
    def __init__(self, parent: ..., **kwargs) -> None:
        """Initializes the CustomTreeview object."""
        super().__init__(parent, **kwargs)
