"""Weighting window module."""

from typing import Protocol

import customtkinter as ctk

from . import widgets as wdg
from .base_popup_window import BasePopupWindow

TITLE = "Weighting"
GEOMETRY = "700x125"


class Presenter(Protocol):
    def calculate_and_display_weighted_data(self) -> None: ...


class WeightingWindow(BasePopupWindow):
    """d"""

    def __init__(self) -> None:
        """Create the weighting window."""
        super().__init__(title=TITLE, geometry=GEOMETRY)
        self.tv = None

    def _create_widgets(self, presenter: Presenter) -> None:
        """d"""
        self.tv = wdg.CustomTreeview(self)
        self.tv.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.60)
        self.tv.add_horizontal_scrollbar()

        btn = ctk.CTkButton(
            self, text="Apply", command=lambda: self.btn_function(presenter)
        )
        btn.pack(side="bottom", pady=(5, 10))

    def display_data(self, data) -> None:
        """d"""
        if not self.tv:
            raise ValueError("No treeview to display data.")
        self.tv.display_data(data, False)

    def btn_function(self, presenter: Presenter) -> None:
        """d"""
        presenter.calculate_and_display_weighted_data()
        self.destroy()
