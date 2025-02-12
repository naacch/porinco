"""Module for the ButtonsFrame class."""

import customtkinter as ctk


class ButtonsFrame(ctk.CTkFrame):
    """Frame for buttons."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the ButtonsFrame object."""
        super().__init__(*args, **kwargs)
        self.buttons = []
        self._default_btn_height = 777  # xd

    def _frame_size(self) -> tuple[float, float]:
        """Returns the actual size of the frame."""
        return self.winfo_width(), self.winfo_height()

    def create_buttons(self, btns_kwargs: list[dict]) -> None:
        """Create the buttons after ensuring the frame is visible."""
        self.after(100, self._create_buttons, btns_kwargs)

    def _calculate_default_button_height(self, num_btns: int) -> float:
        """Calculate the default height for the buttons."""
        _, frame_height = self._frame_size()
        self._default_btn_height = frame_height / (num_btns * 2 + 1)

    @staticmethod
    def _calculate_buttons_total_height(
        btns_kwargs: list[dict], default_btn_height: float
    ) -> float:
        """Return the total height of the buttons."""
        return sum(kwargs.get("height", default_btn_height) for kwargs in btns_kwargs)

    def _create_buttons(self, btns_kwargs: list[dict]) -> None:
        """Create the buttons."""

        self.destroy_buttons()
        self._calculate_default_button_height(len(btns_kwargs))

        _, frame_height = self._frame_size()
        btns_total_height = self._calculate_buttons_total_height(
            btns_kwargs, self._default_btn_height
        )
        btn_height_step = (frame_height - btns_total_height) / (len(btns_kwargs) + 1)
        y_coord = btn_height_step

        for kwargs in btns_kwargs:
            # Set the default height if not provided
            kwargs.setdefault("height", self._default_btn_height)

            btn = ctk.CTkButton(self, **kwargs)
            btn.place(y=y_coord, relx=0.5, anchor="n")

            # Update the y coordinate for the next button
            y_coord += btn_height_step + kwargs["height"]

            self.buttons.append(btn)

    def get_buttons(self):
        """Get the buttons."""
        return self.buttons

    def destroy_buttons(self) -> None:
        """Destroy the buttons."""
        for btn in self.buttons:
            btn.destroy()
        self.buttons = []
