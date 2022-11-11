from PyQt5.QtWidgets import QStackedWidget

from Models.ScreenModels import Screen, StartUp, ProgramsList, Machining, MachiningInterruption, EmergencyStop

Navigator = QStackedWidget()

MyStartUp = StartUp()
MyStartUp.setObjectName("StartUp")

MyProgramsList = ProgramsList()
MyProgramsList.setObjectName("ProgramsList")

MyMachining = Machining()
MyMachining.setObjectName("Machining")

MyMachiningInterruption = MachiningInterruption()
MyMachiningInterruption.setObjectName("MachiningInterruption")

MyEmergencyStop = EmergencyStop()
MyEmergencyStop.setObjectName("EmergencyStop")

Navigator.addWidget(MyStartUp)
Navigator.addWidget(MyProgramsList)
Navigator.addWidget(MyMachining)
Navigator.addWidget(MyMachiningInterruption)
Navigator.addWidget(MyEmergencyStop)

Screen.navigation("StartUp")


