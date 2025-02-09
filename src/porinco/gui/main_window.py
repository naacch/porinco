"""Main window of the application."""

import customtkinter as ctk

TITLE = "PORINCO"
GEOMETRY = "800x600"


class MainWindow(ctk.CTk):
    """Main window of the application."""

    def __init__(self, *args, **kwargs):
        """Create the main window."""
        super().__init__(*args, **kwargs)
        self.title(TITLE)
        self.geometry(GEOMETRY)
