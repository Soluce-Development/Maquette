from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi


class MainScreen(QMainWindow):

    def __init__(self):
        super().__init__()
        loadUi('./Views/AppScreen.ui', self)
