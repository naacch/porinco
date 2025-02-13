"""d"""

import customtkinter as ctk


class SelectionFrame(ctk.CTkFrame):
    """Frame for the selection module."""

    def __init__(self, *args, **kwargs) -> None:
        """Create the selection frame."""
        super().__init__(*args, **kwargs)

    def create_widgets(self) -> None:
        """Create the widgets."""
        ctk.CTkLabel(self, text="Normalization").place(relx=0.01, rely=0.01)
        ...
