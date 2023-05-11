import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem,QTextEdit
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from FiniteAutomata import FA
from PDA import PDA
import json

class CFG_Transitions(QWidget):
    def __init__(self,variables,terminals,startVariable,production_rules):
        self.variables = variables
        self.terminals = terminals
        self.startVariable = startVariable
        self.production_rules = production_rules
            
        super().__init__()
        self.resize(1000, 800)
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
        
    
    def inputToCFG(self):

        production_rules_str = self.transitionBox.toPlainText()

        if self.is_json(production_rules_str):

            self.production_rules = dict(json.loads(self.transitionBox.toPlainText()))
            self.pda = PDA(self.variables, self.terminals, self.startVariable,self.production_rules)

            transitions = self.pda.transitions

            self.close()
            self.dfaWindow = CFG_Transitions(self.variables,self.terminals,self.startVariable,transitions)
            self.dfaWindow.show()

        else:
            self.error.setText('Input is not a Dictionary')

        
        
        
        
    def initUI(self):
        self.transitionBox = QtWidgets.QTextEdit(self)
        self.transitionBox.setGeometry(50,50,550,700)
        self.transitionBox.setObjectName("transitionBox")

        if self.production_rules is None:
            
            
            self.label = QtWidgets.QLabel(self)
            self.label.setGeometry(600, 100, 400, 50)
            self.label.setText("Enter the transition in the text box as a dict")

            self.label = QtWidgets.QLabel(self)
            self.label.setGeometry(600, 150, 400, 200)
            self.label.setText("{ 'S': ['aBc', 'ab'],'B': ['SB', '']}")

            self.label = QtWidgets.QLabel(self)
            self.label.setGeometry(600, 200, 400, 50)
            self.label.setText("To enter multiple rules (separate by ',')")

            self.convert = QtWidgets.QPushButton(self)
            self.convert.setGeometry(600, 700, 200, 50)
            self.convert.setObjectName("convert")
            self.convert.setText("Convert to DFA")
            self.convert.clicked.connect(self.inputToCFG)
            
            self.error = QtWidgets.QLabel(self)
            self.error.setStyleSheet("color: red;")
            self.error.setGeometry(600, 750, 400, 50)
        else:
            s = ""
            for key, values in self.production_rules.items():
                for value in values:
                    s+= (f"From {key[0]} with input '{key[1]}' and pop '{key[2]}': to {value[0]} and push '{value[1]}'") + '\n'
            self.transitionBox.setText(s)

    def is_json(self,myjson):
        try:
            json.loads(myjson)
        except ValueError as e:
            return False
        return True

