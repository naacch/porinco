"""Polarity window."""

from typing import Protocol

import customtkinter as ctk

from .base_popup_window import BasePopupWindow

TITLE = "Polarity"
GEOMETRY = "200x400"


class Presenter(Protocol):
    def _update_negative_variables(self, neg_vars: list[str]) -> None: ...


class PolarityWindow(BasePopupWindow):
    """d"""

    def __init__(self, vars: list[str]) -> None:
        """Create the polarity window."""
        super().__init__(title=TITLE, geometry=GEOMETRY)

        # FIXME: no funciona
        self.change_icon("src/porinco/gui/resources/icon.ico")

        self.vars = vars
        self.check_boxes = []

    def _create_widgets(self, presenter: Presenter) -> None:
        """Create widgets in the window."""
        label = ctk.CTkLabel(
            self,
            text="Select variables with\nnegative polarity:",
            anchor="w",
            justify="left",
        )
        label.place(relx=0.01, rely=0.01)

        frame = ctk.CTkScrollableFrame(self)
        frame.place(relx=0.01, rely=0.1, relwidth=0.98, relheight=0.75)

        self.check_boxes = []

        for var in self.vars:
            cb = ctk.CTkCheckBox(frame, text=var)
            cb.pack(anchor="w", pady=(0, 5))
            self.check_boxes.append(cb)

        btn = ctk.CTkButton(
            self, text="Apply", command=lambda: self.button_function(presenter)
        )
        btn.pack(side="bottom", pady=(5, 10))

    def button_function(self, presenter: Presenter) -> list[str]:
        """Get the variables with negative polarity."""
        presenter._update_negative_variables(
            [cb.cget("text") for cb in self.check_boxes if cb.get() == 1]
        )
        self.destroy()
