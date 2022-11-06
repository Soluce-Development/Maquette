from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.uic import loadUi

from utils.dataManager import update_data, get_datas


class Screen(QWidget):
    """Parent class of every screen."""

    def __init__(self):
        super().__init__()

    @staticmethod
    def navigation(goto: str):

        from Controllers.Navigator import Navigator, MyStartUp, MyMachining, MyMachiningInterruption

        for screen in range(0, Navigator.count()):

            my_screen = Navigator.widget(screen)

            if my_screen.objectName() == goto:
                Navigator.setCurrentWidget(my_screen)

        if Navigator.currentWidget() == MyStartUp:
            MyStartUp.update_progressBar(0)

        if Navigator.currentWidget() == MyMachining:
            MyMachining.text_program.setText(get_datas("program"))
            MyMachining.program_timer(0)

        if Navigator.currentWidget() == MyMachiningInterruption:
            MyMachiningInterruption.update_progressBar(0)


class MainScreen(QMainWindow, Screen):

    def __init__(self):
        super().__init__()
        loadUi('./Views/MainScreen.ui', self)

        self.setWindowTitle("Logiciel de démonstration")

        self.setFixedWidth(600)
        self.setFixedHeight(300)

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

        self.btn_start.clicked.connect(lambda: self.navigation('Machining'))

    def program_selection_handler(self, btn_clicked):

        match btn_clicked.objectName():
            case "btn_prog1":
                update_data("program", "programme 1")
            case "btn_prog2":
                update_data("program", "programme 2")
            case "btn_prog3":
                update_data("program", "programme 3")

        self.btn_start.setEnabled(True)

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

        sec += 1
        print(sec)
        if self.stopped:
            self.stopped = False
            self.navigation('MachiningInterruption')
            return
        if sec <= 100:
            self.progressBar.setValue(sec)
            get_datas("duration")
            interval = int(int(get_datas("duration")) / 100)
            QTimer.singleShot(interval, lambda: self.program_timer(sec))
        else:
            self.navigation('ProgramsList')

    def program_stopped(self):
        self.stopped = True
        self.navigation('MachiningInterruption')


class MachiningInterruption(QMainWindow, Screen):
    """Machining screen displays when a program is running."""

    def __init__(self):
        super(MachiningInterruption, self).__init__()
        loadUi('./Views/MachiningInterruption.ui', self)

    def update_progressBar(self, pourcentage):
        pourcentage += 1
        if pourcentage <= 100:
            self.progressBar.setValue(pourcentage)
            QtCore.QTimer.singleShot(10, lambda: self.update_progressBar(pourcentage))
        else:
            self.navigation('ProgramsList')
