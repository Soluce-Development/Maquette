import sys

import GPIO as GPIO
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication

from Constants import SENSOR_PEDAL
from Controllers.EventsHandler import initial_events, add_events
from Models.ScreenModels import MainScreen

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setOverrideCursor(QCursor(Qt.BlankCursor))

    main_screen = MainScreen()

    main_screen.show()
    initial_events()
    add_events()
    GPIO.remove_event_detect(SENSOR_PEDAL)
    sys.exit(app.exec_())
