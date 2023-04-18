import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtWidgets,QtCore
from directed import directedGraphWindow 
from transitionsInput import transitionInputWindow

class firstWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.initUI()

    def next(self):
        alphabets = self.alphabets.text().split(',')
        NFAstates = self.states.text().split(',')
        startState = self.startState.text()
        acceptingStates = self.acceptingStates.text().split(',')
        self.transitionWindow = transitionInputWindow(alphabets,NFAstates,startState,acceptingStates)
        
        self.transitionWindow.show()
    

    def initUI(self):

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(300, 50, 200, 40)
        self.label.setText("Alphabets:(separated by ',')")
        
        self.alphabets = QtWidgets.QLineEdit(self)
        self.alphabets.setGeometry(300, 100, 200, 40)
        self.alphabets.setPlaceholderText("Alphabets")
        self.alphabets.setObjectName("alphabets")

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(300, 150, 200, 40)
        self.label.setText("States:(separated by ',')")
        
        self.states = QtWidgets.QLineEdit(self)
        self.states.setGeometry(300, 200, 200, 40)
        self.states.setPlaceholderText("States")
        self.states.setObjectName("states")

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(300, 250, 200, 40)
        self.label.setText("Start State")
        
        self.startState = QtWidgets.QLineEdit(self)
        self.startState.setGeometry(300, 300, 200, 40)
        self.startState.setPlaceholderText("Start State")
        self.startState.setObjectName("startState")

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(300, 350, 200, 40)
        self.label.setText("Accepting States:(separated by ',')")
        
        self.acceptingStates = QtWidgets.QLineEdit(self)
        self.acceptingStates.setGeometry(300, 400, 200, 40)
        self.acceptingStates.setPlaceholderText("Accepting States")
        self.acceptingStates.setObjectName("acceptingStates")

        self.nextBtn = QtWidgets.QPushButton(self)
        self.nextBtn.setGeometry(200, 450, 400, 40)
        self.nextBtn.setText("Next")
        self.nextBtn.clicked.connect(self.next)
        self.nextBtn.setObjectName("nextBtn")


app = QApplication(sys.argv)
demo = firstWindow()
demo.show()
sys.exit(app.exec_())