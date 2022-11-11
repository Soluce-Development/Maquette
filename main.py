import sys
from PyQt5.QtWidgets import QApplication

from Controllers.EventsHandler import initial_events, add_events
from Models.ScreenModels import MainScreen

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_screen = MainScreen()

    main_screen.show()
    initial_events()
    add_events()
    sys.exit(app.exec_())
