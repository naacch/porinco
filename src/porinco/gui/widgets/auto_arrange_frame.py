"""d"""

import tkinter as tk

import customtkinter as ctk


class AutoArrangeFrame(ctk.CTkFrame):
    """Frame that automatically arranges widgets vertically."""

    def __init__(self, *args, **kwargs) -> None:
        """Create the frame."""
        super().__init__(*args, **kwargs)
        self.widgets = []

    def _frame_size(self) -> tuple[float, float]:
        """Returns the actual size of the frame."""
        return self.winfo_width(), self.winfo_height()

    def place_widgets(self, widgets: list[tk.Widget]) -> None:
        """Create the widgets after ensuring the frame is visible."""
        if not widgets:
            raise ValueError("No widgets to place.")

        self.after(100, self._place_widgets, widgets)

    # I don't like this way of calculating the total height of the widgets.
    # I would prefer to calculate the total height of the widgets before placing them.
    def _get_widgets_total_height(self, widgets: list[tk.Widget]) -> float:
        """Return the total height of the widgets."""
        for wdg in widgets:
            wdg.place(x=-7_777_777, y=-7_777_777)  # xd

        self.update_idletasks()

        total_height = sum(wdg.winfo_height() for wdg in widgets)

        for wdg in widgets:
            wdg.place_forget()

        return total_height

    # TODO: cambiar para que cuando cambie el tamaño del frame se recalcule la posición de los widgets
    def _place_widgets(self, widgets: list[tk.Widget]) -> None:
        """Place the widgets in the frame."""

        _, frame_height = self._frame_size()
        widgets_total_height = self._get_widgets_total_height(widgets)

        self.destroy_widgets()

        height_step = (frame_height - widgets_total_height) / (len(widgets) + 1)
        y_coord = height_step

        for wdg in widgets:
            wdg.place(y=y_coord, relx=0.5, anchor="n")
            # Update the y coordinate for the next button
            y_coord += height_step + wdg.winfo_height()

        self.widgets = widgets

    def get_widgets(self) -> list[tk.Widget]:
        """Get the widgets."""
        return self.widgets

    def destroy_widgets(self) -> None:
        """Destroy the widgets."""
        for wdg in self.widgets:
            wdg.destroy()
        self.widgets = []
