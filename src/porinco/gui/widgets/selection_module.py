"""d"""

from typing import Callable

import customtkinter as ctk

ACCEPT_BTN_COLOR = "grey67"


class SelectionFrame(ctk.CTkFrame):
    """Frame for the selection module."""

    def __init__(self, *args, **kwargs) -> None:
        """Create the selection frame."""
        super().__init__(*args, **kwargs)

    def create_widget(
        self,
        label_txt: str,
        options: list[str],
        option_menu_command: Callable | None = None,
        button_command: Callable | None = None,
    ) -> None:
        """Create the normalization module."""
        label = ctk.CTkLabel(self, text=label_txt)
        label.place(relx=0.01, rely=0.01)

        option_menu = ctk.CTkOptionMenu(
            self, values=list(options), command=option_menu_command
        )
        option_menu.set("Select an option")
        option_menu.place(relx=0.5, rely=0.3, relwidth=0.8, anchor="n")

        accept_button = ctk.CTkButton(
            self,
            text="Accept",
            fg_color=ACCEPT_BTN_COLOR,
            command=button_command,
        )
        accept_button.place(relx=0.5, rely=0.65, anchor="n")
