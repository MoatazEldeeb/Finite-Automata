import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtWidgets,QtCore
from CFG_Transitions import CFG_Transitions


class firstWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.initUI()

    def next(self):
        variables = set(self.variables.text().split(','))
        terminals = set(self.terminals.text().split(','))
        startVariable = self.startVariable.text()
        self.transitionWindow = CFG_Transitions(variables,terminals,startVariable,None)
        
        self.transitionWindow.show()
    

    def initUI(self):

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(300, 50, 250, 40)
        self.label.setText("Variables:(separated by ',')")
        
        self.variables = QtWidgets.QLineEdit(self)
        self.variables.setGeometry(300, 100, 200, 40)
        self.variables.setPlaceholderText("Variables")
        self.variables.setObjectName("variables")

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(300, 150, 200, 40)
        self.label.setText("Terminals:(separated by ',')")
        
        self.terminals = QtWidgets.QLineEdit(self)
        self.terminals.setGeometry(300, 200, 200, 40)
        self.terminals.setPlaceholderText("Terminals")
        self.terminals.setObjectName("terminals")

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(300, 250, 200, 40)
        self.label.setText("Start Variable")
        
        self.startVariable = QtWidgets.QLineEdit(self)
        self.startVariable.setGeometry(300, 300, 200, 40)
        self.startVariable.setPlaceholderText("Start Variable")
        self.startVariable.setObjectName("startVariable")

        self.nextBtn = QtWidgets.QPushButton(self)
        self.nextBtn.setGeometry(200, 450, 400, 40)
        self.nextBtn.setText("Next")
        self.nextBtn.clicked.connect(self.next)
        self.nextBtn.setObjectName("nextBtn")


app = QApplication(sys.argv)
demo = firstWindow()
demo.show()
sys.exit(app.exec_())