"""d"""  # TODO: docstrings

import customtkinter as ctk


class ButtonsFrame(ctk.CTkFrame):
    """d"""

    def __init__(self, *args, **kwargs) -> None:
        """d"""
        super().__init__(*args, **kwargs)
        self.buttons = []

    def create_buttons(self, btns_kwargs: list[dict]) -> None:
        """Create the buttons."""
        for kwargs in btns_kwargs:
            btn = ctk.CTkButton(self, **kwargs)
            btn.pack()  # TODO: cambiar
            self.buttons.append(btn)

    def get_buttons(self):
        """Get the buttons."""
        return self.buttons

    # Vale la pena agregar un metodo que borre los botones?
