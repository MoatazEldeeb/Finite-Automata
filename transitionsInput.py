import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
import networkx as nx
from GoalPage import GoalPage
from FiniteAutomata import FA

class transitionInputWindow(QWidget):
    def __init__(self,alphabets,NFAstates,startState,acceptingStates):
        self.alphabets = alphabets
        self.NFAstates = NFAstates
        self.startState = startState
        self.acceptingStates = acceptingStates
        super().__init__()
        self.resize(1600, 800)
        self.initUI()

    def AddEdge(self):
        if self.edgeFrom.text() and self.edgeTo.text():
            if self.withCost:
                if self.incost.text().isdigit():
                    self.chart.updateGraph(self.edgeFrom.text(),self.edgeTo.text(),self.incost.text())
                else: self.error.setText("Cost must be integer")
            else:
                self.chart.updateGraph(self.edgeFrom.text(),self.edgeTo.text(),0)
            self.chart.draw_idle()
        else:
            self.error.setText("From, To and input are required")

    def NextPage(self):
        self.dWindow = GoalPage(self.chart.G)
        self.dWindow.show()

    def get_input_fields_convert_to_nfa(self):
        ts ={}
        
        for i in range(self.table.rowCount()):
            colHeader = self.NFAstates[i]
            ts[colHeader]={}
            for j in range(self.table.columnCount()):
                
                rowHeader = self.alphabets[j]
                print(colHeader,"->>>", rowHeader)
                ts[colHeader][rowHeader]=[]
                item = self.table.item(i, j)
                if item is not None:
                    if ',' in item.text():
                        ts[colHeader][rowHeader] = (item.text().split(','))
                    else:
                        ts[colHeader][rowHeader].append(item.text())

        print(ts)
        return ts
        
    
    def inputToFA(self):
        self.nfa = FA(self.NFAstates,self.alphabets,self.startState,self.acceptingStates,self.get_input_fields_convert_to_nfa())
        print(self.nfa.transitions)
        self.dfa = self.nfa.convert2DFA()
        print(self.dfa.transitions)
        

    def initUI(self):
        
        n=len(self.alphabets)
        m=len(self.NFAstates)
        self.table = QTableWidget(m, n,parent=self)
        self.table.setGeometry(50,50,1100,700)
        NFAstatesLabels =[]
        for i in self.NFAstates:
            if i in self.acceptingStates:
                NFAstatesLabels.append("*"+i)
            elif i == self.startState:
                NFAstatesLabels.append("->"+i)
            else:
                NFAstatesLabels.append(i)

        print(self.NFAstates)
        print(NFAstatesLabels)

        self.table.setHorizontalHeaderLabels(self.alphabets)
        self.table.setVerticalHeaderLabels(NFAstatesLabels)

        for i in range(n):
            for j in range(m):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, j, item)

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(1200, 100, 400, 50)
        self.label.setText("Enter the transition in the table")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(1200, 150, 400, 50)
        self.label.setText("To enter multiple destination states (separate by ',')")


        self.convert = QtWidgets.QPushButton(self)
        self.convert.setGeometry(1200, 700, 200, 50)
        self.convert.setObjectName("convert")
        self.convert.setText("Convert to DFA")
        self.convert.clicked.connect(self.inputToFA)
        
        self.error = QtWidgets.QLabel(self)
        self.error.setStyleSheet("color: red;")
        self.error.setGeometry(1200, 750, 400, 50)
