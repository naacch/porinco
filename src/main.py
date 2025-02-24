"""Main module for the application."""

import customtkinter as ctk

from porinco import core, gui
from porinco.gui import presenter

ctk.set_default_color_theme("src/porinco/gui/resources/themes/metal.json")


def main() -> None:
    """Main function for the app."""
    main_window = gui.MainWindow()
    main_model = core.MainModel()
    main_presenter = presenter.MainPresenter(
        main_window, main_model, core.NORMALIZATIONS, core.WEIGHTINGS
    )
    main_presenter.run()


if __name__ == "__main__":
    main()
