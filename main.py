import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication

from Controllers.EventsHandler import initial_events, add_events
from Models.ScreenModels import MainScreen

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOverrideCursor(QCursor(Qt.BlankCursor))

    main_screen = MainScreen()

    main_screen.show()
    initial_events()
    add_events()
    sys.exit(app.exec_())
