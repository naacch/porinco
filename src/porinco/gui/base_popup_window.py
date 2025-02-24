"""Base class for popup windows."""

import customtkinter as ctk


class BasePopupWindow(ctk.CTkToplevel):
    """Base class for popup windows."""

    def __init__(self, title: str, geometry: str) -> None:
        """Create the popup window."""
        super().__init__()

        self.title(title)
        self.geometry(geometry)

        self._apply_theme()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self.grab_set()

    def _on_close(self) -> None:
        """Restore focus to the main window when closing."""
        self.grab_release()

    # FIXME: no funciona
    def change_icon(self, path: str) -> None:
        """Change the icon of the window."""
        self.iconbitmap(path)

    def _apply_theme(self) -> None:
        """Apply the current global theme."""
        current_theme = ctk.get_appearance_mode()
        ctk.set_appearance_mode(current_theme)
