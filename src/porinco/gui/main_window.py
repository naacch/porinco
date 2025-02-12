"""Main window of the application."""

from typing import Protocol

import customtkinter as ctk

from . import widgets as wdg

TITLE = "PORINCO"
GEOMETRY = "1400x800"


class Presenter(Protocol):
    """Presenter for the main window."""

    def open_file(self):
        """Open a file."""

    def export_file(self):
        """Export a file."""


class MainWindow(ctk.CTk):
    """Main window of the application."""

    def __init__(self, *args, **kwargs) -> None:
        """Create the main window."""
        super().__init__(*args, **kwargs)
        self.treeview = None
        self.title(TITLE)
        self.geometry(GEOMETRY)

    def create_ui(self, presenter: Presenter) -> None:
        """Create the ui for the main window."""

        self.treeview = wdg.CustomTreeview(self)
        self.treeview.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.75)

        btns_frame = wdg.ButtonsFrame(self)
        btns_frame.place(
            relx=0.01,
            rely=0.77,
            relwidth=0.15,
            relheight=0.22,
        )
        btns_kwargs = [
            {"text": "Open File", "height": 60, "command": presenter.open_file},
            {"text": "Export File", "height": 60, "command": presenter.export_file},
        ]
        btns_frame.create_buttons(btns_kwargs)
