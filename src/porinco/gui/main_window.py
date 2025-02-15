"""Main window of the application."""

from typing import Protocol

import customtkinter as ctk

from . import widgets as wdg
from .polarity_window import PolarityWindow

TITLE = "PORINCO"
GEOMETRY = "1400x800"


class Presenter(Protocol):
    """Presenter for the main window."""

    normalizations: dict  # TODO: typehints

    def open_file(self) -> None: ...
    def export_file(self) -> None: ...
    def update_selected_norm(self, norm: str) -> None: ...
    def apply_and_display_norm(self) -> None: ...
    def open_polarity_window(self) -> None: ...


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
        self._create_polarity_module(presenter)
        self._create_norm_module(presenter)

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

    def _create_polarity_module(self, presenter: Presenter) -> None:
        """Create the polarity module."""
        frame = ctk.CTkFrame(self)
        frame.place(relx=0.17, rely=0.77, relwidth=0.18, relheight=0.05)

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=0)
        frame.columnconfigure(2, weight=1)

        btn = ctk.CTkButton(
            frame, text="Polarity", command=presenter.open_polarity_window
        )
        btn.grid(row=0, column=0, padx=(10, 5), pady=5)

        cb = ctk.CTkCheckBox(frame, text="Taxonomy")
        cb.grid(row=0, column=2, padx=(5, 10), pady=5)

    def _create_norm_module(self, presenter: Presenter) -> None:
        """Create the normalization module."""
        outer_frame = wdg.SelectionFrame(self)
        iner_frame = wdg.AutoArrangeFrame(outer_frame)

        label = ctk.CTkLabel(outer_frame, text="Normalization")

        option_menu = ctk.CTkOptionMenu(
            iner_frame,
            values=list(presenter.normalizations.keys()),
            command=lambda value: presenter.update_selected_norm(value),
        )
        option_menu.set("Select an option")

        widgets = [
            option_menu,
            ctk.CTkButton(
                iner_frame, text="Accept", command=presenter.apply_and_display_norm
            ),
        ]

        iner_frame.place_widgets(widgets)

        outer_frame.place(relx=0.17, rely=0.83, relwidth=0.18, relheight=0.16)
        outer_frame.place_widgets(label, iner_frame)

    def create_polarity_window(self, vars: list[str]) -> ctk.CTkToplevel:
        """Create and show the polarity selection window."""
        polarity_window = PolarityWindow(vars)
        return polarity_window
