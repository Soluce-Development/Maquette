import sys
from PyQt5.QtWidgets import QApplication
from Models.ScreenModels import MainScreen


if __name__ == "__main__":

    app = QApplication(sys.argv)
    main_screen = MainScreen()
    main_screen.showMaximized()
    sys.exit(app.exec_())
