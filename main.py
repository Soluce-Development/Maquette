import sys
from PyQt5.QtWidgets import QApplication

from Controllers import EventsHandler
from Models.ScreenModels import MainScreen

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_screen = MainScreen()

    main_screen.show()
    EventsHandler.add_events()
    sys.exit(app.exec_())
