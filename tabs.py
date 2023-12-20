from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import sys

import maintab
import upgradetab

class mainTab(QWidget):
    def updateDisplay(self):
        self.tabContent.updateDisplay()
    def updateInternal(self):
        pass
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.tabContent = maintab.content()
        self.layout.addWidget(self.tabContent)
        self.setLayout(self.layout)
    
    
        
class upgradeTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.tabContent = upgradetab.content()
        self.layout.addWidget(self.tabContent)
        self.setLayout(self.layout)
        
    def updateDisplay(self):
        self.tabContent.updateDisplay()
        
    def updateInternal(self):
        self.tabContent.updateInternal()
        
class settingsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Settings Tab"))
        self.setLayout(self.layout)
    def updateDisplay(self):
        return 0

class achievementsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Achievements Tab"))
        self.setLayout(self.layout)
    def updateDisplay(self):
        return 0

tabs = [mainTab, upgradeTab, settingsTab, achievementsTab]