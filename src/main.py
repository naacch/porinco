"""Main module for the application."""

from porinco import gui


def main() -> None:
    """Main function for the app."""
    main_window = gui.MainWindow()
    main_window.mainloop()


if __name__ == "__main__":
    main()
