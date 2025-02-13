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

        self._create_data_file_module(presenter)
        self._create_polarity_module()
        self._create_norm_module()

    def _create_data_file_module(self, presenter: Presenter) -> None:
        """Create the data file module with open and export functionality."""
        frame = wdg.AutoArrangeFrame(self)
        frame.place(
            relx=0.01,
            rely=0.77,
            relwidth=0.15,
            relheight=0.22,
        )
        btns_kwargs = [
            {"text": "Open File", "height": 60, "command": presenter.open_file},
            {"text": "Export File", "height": 60, "command": presenter.export_file},
        ]
        btns = [ctk.CTkButton(frame, **kwargs) for kwargs in btns_kwargs]
        frame.place_widgets(btns)

    def _create_polarity_module(self) -> None:
        """Create the polarity module."""
        frame = ctk.CTkFrame(self)
        frame.place(relx=0.17, rely=0.77, relwidth=0.18, relheight=0.05)

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=0)
        frame.columnconfigure(2, weight=1)

        btn = ctk.CTkButton(frame, text="Polarity")
        btn.grid(row=0, column=0, padx=(10, 5), pady=5)

        cb = ctk.CTkCheckBox(frame, text="Taxonomy")
        cb.grid(row=0, column=2, padx=(5, 10), pady=5)

    def _create_norm_module(self) -> None:
        """Create the normalization module."""
        frame = wdg.SelectionFrame(self)
        frame.create_widgets()
        frame.place(relx=0.17, rely=0.83, relwidth=0.18, relheight=0.16)
