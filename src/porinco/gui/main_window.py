"""Main window of the application."""

import tkinter as tk
from typing import Any, Protocol

import customtkinter as ctk

from . import widgets as wdg
from .polarity_window import PolarityWindow

TITLE = "porinco"
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

        norm_module_kwargs = {
            "label_txt": "Normalization",
            "options": list(presenter.normalizations.keys()),
            "option_menu_command": lambda value: presenter.update_selected_norm(value),
            "button_command": presenter.apply_and_display_norm,
        }
        norm_module = self._create_selection_frame(norm_module_kwargs)
        norm_module.place(relx=0.17, rely=0.83, relwidth=0.18, relheight=0.16)

        self._create_range_module()

        weighting_module_kwargs = {
            "label_txt": "Weighting",
            "options": [],
        }
        weighting_module = self._create_selection_frame(weighting_module_kwargs)
        weighting_module.place(relx=0.62, rely=0.83, relwidth=0.18, relheight=0.16)

        frame = ctk.CTkFrame(self, fg_color="#c90d0e")
        frame.place(relx=0.36, rely=0.77, relwidth=0.44, relheight=0.05)

        aggregation_module_kwargs = {
            "label_txt": "Aggregation",
            "options": [],
        }
        aggregation_module = self._create_selection_frame(aggregation_module_kwargs)
        aggregation_module.place(relx=0.81, rely=0.77, relwidth=0.18, relheight=0.16)

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

        self._create_sensitivity_module()

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

    def _create_selection_frame(self, widgets_kwargs: dict[str:Any]) -> None:
        """Create the selection frame."""
        frame = wdg.SelectionFrame(self)
        frame.create_widget(**widgets_kwargs)
        return frame

    def create_polarity_window(self, vars: list[str]) -> ctk.CTkToplevel:
        """Create and show the polarity selection window."""
        polarity_window = PolarityWindow(vars)
        return polarity_window

    # TODO: esto es caca, refactor
    def _create_range_module(self) -> None:
        """Create the range module."""
        frame = ctk.CTkFrame(self)
        frame.place(relx=0.36, rely=0.83, relwidth=0.25, relheight=0.16)

        ctk.CTkLabel(frame, text="Min range").grid(
            row=0, column=0, sticky="w", padx=(15, 0), pady=(10, 0)
        )
        ctk.CTkEntry(frame).grid(row=1, column=0, padx=5, pady=(0, 10))

        ctk.CTkLabel(frame, text="Max range").grid(
            row=0, column=2, sticky="w", padx=(15, 0), pady=(10, 0)
        )
        ctk.CTkEntry(frame).grid(row=1, column=2, padx=5, pady=(0, 10))

        # Button
        btn = ctk.CTkButton(frame, text="Accept", fg_color="grey67")
        btn.grid(row=2, column=0, columnspan=3, pady=(0, 10))

        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(2, weight=1)

    def _create_sensitivity_module(self) -> None:
        """Create the sensitivity module."""
        frame = ctk.CTkFrame(self)
        frame.place(relx=0.81, rely=0.94, relwidth=0.18, relheight=0.05)

        btn = ctk.CTkButton(frame, text="Sensitivity")
        btn.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8, anchor="center")

    def _get_frames(self, wdg: tk.Widget | None = None) -> list[ctk.CTkFrame]:
        """d"""
        wdg = self if not wdg else wdg

        frames = []

        for child in wdg.winfo_children():
            if isinstance(child, ctk.CTkFrame):
                frames.append(child)
                frames.extend(self._get_frames(child))
        return frames

    def change_icon(self, path: str) -> None:
        """Change the icon of the window."""
        self.iconbitmap(path)
