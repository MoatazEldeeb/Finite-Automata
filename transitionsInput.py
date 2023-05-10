import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
import networkx as nx
from FiniteAutomata import FA

class transitionInputWindow(QWidget):
    def __init__(self,alphabets,states,startState,acceptingStates,transitions):
        self.alphabets = alphabets
        self.states = states
        self.startState = startState
        self.acceptingStates = acceptingStates
        self.transitions = transitions
            
        super().__init__()
        self.resize(1600, 800)
        self.initUI()


    def get_input_fields_convert_to_nfa(self):
        ts ={}
        
        for i in range(self.table.rowCount()):
            colHeader = self.states[i]
            ts[colHeader]={}
            for j in range(self.table.columnCount()):
                
                rowHeader = self.alphabets[j]
                print(colHeader,"->>>", rowHeader)
                ts[colHeader][rowHeader]=[]
                item = self.table.item(i, j)
                if item is not None:
                    if ',' in item.text():
                        ts[colHeader][rowHeader] = (item.text().split(','))
                    elif item.text() == '':
                        ...
                    else:
                        ts[colHeader][rowHeader].append(item.text())

        return ts
        
    
    def inputToFA(self):
        self.nfa = FA(self.states,self.alphabets,self.startState,self.acceptingStates,self.get_input_fields_convert_to_nfa())
        print("NFA transitions:",self.nfa.transitions)
        self.dfa = self.nfa.convert2DFA()
        print("DFA transitions:",self.dfa.transitions)

        alphabets = self.dfa.alphabet
        states = self.dfa.states
        startState = self.dfa.startState
        acceptingStates = self.dfa.acceptingStates
        transitions = self.dfa.transitions
        self.close()
        self.dfaWindow = transitionInputWindow(alphabets,states,startState,acceptingStates,transitions)

        self.dfaWindow.show()
        
        
    def fillTable(self):
        
        for i in range(self.table.rowCount()):
            colHeader = self.states[i]
            print("State:",colHeader)
            for j in range(self.table.columnCount()):
                
                rowHeader = self.alphabets[j]
                print("Alphabet:",rowHeader)
                print("To:",self.transitions[colHeader][rowHeader])
                item = QTableWidgetItem(str(self.transitions[colHeader][rowHeader]))
                self.table.setItem(i, j,item)
        
    def initUI(self):
        
        n=len(self.alphabets)
        m=len(self.states)
        self.table = QTableWidget(m, n,parent=self)
        self.table.setGeometry(50,50,1100,700)
        statesLabels =[]
        for i in self.states:
            if i in self.acceptingStates:
                statesLabels.append("*"+i)
            elif i == self.startState:
                statesLabels.append("->"+i)
            else:
                statesLabels.append(i)
        self.table.setHorizontalHeaderLabels(self.alphabets)
        self.table.setVerticalHeaderLabels(statesLabels)
        for i in range(n):
                for j in range(m):
                    item = QTableWidgetItem()
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(i, j, item)
        if self.transitions is None:
            print(self.states)
            print(statesLabels)

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
        else:
            self.fillTable()
