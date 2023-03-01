from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.uic import loadUi
import RPi.GPIO as GPIO

from utils.dataManager import update_data, get_datas
from Constants import *

from Controllers.EventsHandler import toggledd


class Screen(QWidget):
    """Parent class of every screen."""

    def __init__(self):
        super().__init__()

    @staticmethod
    def navigation(goto: str):

        from Controllers.Navigator import Navigator, MyStartUp, MyProgramsList, MyMachining, \
            MyMachiningInterruption, MyEmergencyStop

        for screen in range(0, Navigator.count()):

            my_screen = Navigator.widget(screen)

            if my_screen.objectName() == goto:
                Navigator.setCurrentWidget(my_screen)

        if Navigator.currentWidget() == MyStartUp:
            MyStartUp.update_progressBar(0)

        if Navigator.currentWidget() == MyProgramsList:
            MyProgramsList.handle_error_messages()
            MyProgramsList.handle_navigation()

        if Navigator.currentWidget() == MyMachining:
            MyMachining.text_program.setText(get_datas("program"))
            MyMachining.program_timer(0)

        if Navigator.currentWidget() == MyMachiningInterruption:
            MyMachiningInterruption.update_progressBar(0)

        if Navigator.currentWidget() == MyEmergencyStop:
            MyEmergencyStop.wait_for_emergency_released()


class MainScreen(QMainWindow, Screen):

    def __init__(self):
        super().__init__()
        loadUi('./Views/MainScreen.ui', self)

        self.setWindowTitle("Logiciel de démonstration")

        from Controllers.Navigator import Navigator
        self.setCentralWidget(Navigator)


class StartUp(QMainWindow, Screen):
    """Start up screen displays when the system is turn on."""

    def __init__(self):
        super(StartUp, self).__init__()
        loadUi('./Views/StartUp.ui', self)

    def update_progressBar(self, pourcentage):
        pourcentage += 1
        if pourcentage <= 100:
            self.progressBar.setValue(pourcentage)
            QtCore.QTimer.singleShot(30, lambda: self.update_progressBar(pourcentage))
        else:
            self.navigation('ProgramsList')


class ProgramsList(QMainWindow, Screen):
    """Programs list screens displays after start up"""

    def __init__(self):
        super(ProgramsList, self).__init__()
        loadUi('./Views/ProgramsList.ui', self)

        self.btn_prog1.clicked.connect(lambda: self.program_selection_handler(self.btn_prog1))
        self.btn_prog2.clicked.connect(lambda: self.program_selection_handler(self.btn_prog2))
        self.btn_prog3.clicked.connect(lambda: self.program_selection_handler(self.btn_prog3))

        # self.btn_start.clicked.connect(self.handle_navigation)

        self.program_chosen = False
        self.enabled = False
        self.text_choose_program.setText("")

    def handle_navigation(self):
        if self.program_chosen and self.enabled:
            if not GPIO.input(BTN_START):
                self.navigation('Machining')
        elif not self.program_chosen:
            self.text_choose_program.setText("Veuillez choisir un programme")

        QtCore.QTimer.singleShot(10, self.handle_navigation)

    def handle_error_messages(self):

        if GPIO.input(BTN_EMERGENCY):
            self.text_emergency.setText("Arrêt d'urgence enclenché, impossible d'usiner")
        else:
            self.text_emergency.setText("")

        if GPIO.input(SENSOR_DOOR) or not GPIO.input(BTN_DOOR):
            # self.text_door.setText("Porte ouverte, impossible d'usiner")
            global toggledd
            self.text_door.setText(str(GPIO.input(SENSOR_PEDAL)))
        else:
            self.text_door.setText("")

        if not GPIO.input(BTN_EMERGENCY) and not GPIO.input(SENSOR_DOOR):
            # self.btn_start.setEnabled(True)
            self.enabled = True

        else:
            # self.btn_start.setEnabled(False)
            self.enabled = False

        QtCore.QTimer.singleShot(10, self.handle_error_messages)

    def program_selection_handler(self, btn_clicked):
        self.program_chosen = True
        self.text_choose_program.setText("")
        if btn_clicked.objectName() == "btn_prog1":
            update_data("program", "programme 1")
            update_data("duration", "5000")
        if btn_clicked.objectName() == "btn_prog2":
            update_data("program", "programme 2")
            update_data("duration", "6000")
            self.program = "programme 2"
        if btn_clicked.objectName() == "btn_prog3":
            update_data("program", "programme 3")
            update_data("duration", "8000")
            self.program = "programme 3"

        self.btn_prog1.setChecked(False)
        self.btn_prog2.setChecked(False)
        self.btn_prog3.setChecked(False)
        btn_clicked.setChecked(True)


class Machining(QMainWindow, Screen):
    """Machining screen displays when a program is running."""

    def __init__(self):
        super(Machining, self).__init__()
        loadUi('./Views/Machining.ui', self)

        self.stopped = False

        self.btn_stop.clicked.connect(self.program_stopped)

    def program_timer(self, sec):

        if GPIO.input(BTN_EMERGENCY):
            self.navigation('EmergencyStop')
            GPIO.output(LED_MACHINING, GPIO.LOW)
            return

        if self.stopped:
            self.stopped = False
            return

        sec += 1
        if sec <= 100:
            self.progressBar.setValue(sec)
            get_datas("duration")
            interval = int(int(get_datas("duration")) / 100)
            QTimer.singleShot(interval, lambda: self.program_timer(sec))
            GPIO.output(LED_MACHINING, GPIO.HIGH)
        else:
            self.navigation('ProgramsList')
            GPIO.output(LED_MACHINING, GPIO.LOW)

    def program_stopped(self):
        self.stopped = True
        self.navigation('MachiningInterruption')
        GPIO.output(LED_MACHINING, GPIO.LOW)


class MachiningInterruption(QMainWindow, Screen):
    """Machining screen displays when a program is running."""

    def __init__(self):
        super(MachiningInterruption, self).__init__()
        loadUi('./Views/MachiningInterruption.ui', self)

    def update_progressBar(self, v):
        pourcentage += 1
        if pourcentage <= 100:
            self.progressBar.setValue(pourcentage)
            QtCore.QTimer.singleShot(10, lambda: self.update_progressBar(pourcentage))
        else:
            self.navigation('ProgramsList')


class EmergencyStop(QMainWindow, Screen):
    """Emergency screen displays when the emergency button is pressed."""

    def __init__(self):
        super(EmergencyStop, self).__init__()
        loadUi('./Views/EmergencyStop.ui', self)

    def wait_for_emergency_released(self):
        if not GPIO.input(BTN_EMERGENCY):
            self.navigation('ProgramsList')
            return
        QtCore.QTimer.singleShot(10, self.wait_for_emergency_released)
