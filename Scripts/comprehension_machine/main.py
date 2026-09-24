import sys
from PyQt6.QtWidgets import QApplication
from comprehension.ui.main_window_v5_integrated import TazvMainWindowIntegrated


def main():
    app = QApplication(sys.argv)
    window = TazvMainWindowIntegrated()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
