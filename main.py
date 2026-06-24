import sys
from PyQt5.QtWidgets import QApplication
from GUI import SnakeApp


def main() -> None:
    """Uruchamia aplikację Snake."""
    app = QApplication(sys.argv)

    window = SnakeApp()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()