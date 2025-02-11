"""Main module for the application."""

from porinco import core, gui
from porinco.gui import presenter


def main() -> None:
    """Main function for the app."""
    main_window = gui.MainWindow()
    main_model = core.MainModel()
    main_presenter = presenter.MainPresenter(main_window, main_model)
    main_window.create_ui(main_presenter)
    main_window.mainloop()


if __name__ == "__main__":
    main()
