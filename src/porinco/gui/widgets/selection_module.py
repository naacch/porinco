"""d"""

import customtkinter as ctk


class SelectionFrame(ctk.CTkFrame):
    """Frame for the selection module."""

    def __init__(self, *args, **kwargs) -> None:
        """Create the selection frame."""
        super().__init__(*args, **kwargs)

    def place_widgets(self, label: ctk.CTkLabel, frame: ctk.CTkFrame) -> None:
        """Create the widgets."""
        label.place(relx=0.01, rely=0.01)
        frame.place(relx=0.5, rely=1.0, relwidth=0.8, relheight=0.8, anchor="s")
