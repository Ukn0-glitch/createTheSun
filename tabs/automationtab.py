#standard imports
import json
import time
import copy
import observerModel
from math import floor, ceil
#third party imports
# from PyQt6.QtCore import *
# from PyQt6.QtWidgets import *
# from PyQt6.QtGui import *

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from PySide6.QtGui import Qt


#local imports
import gamedefine
import gameLogic.automationGameLogic as automationGameLogic

class automationBlock(QFrame):
    def __init__(self, name):
        self.name = name
        super().__init__()
        automationGameLogic.updateUpgradeStatus(self.name)
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        self.layout_ = QGridLayout()
        self.setMaximumSize(QSize(700, 200))
        self.lastTickTime = 0
        
        self.upgradeLabel = QLabel(automationGameLogic.parseUpgradeName(self.name))
        self.upgradeLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.upgradeLabel, 0, 0)
        
        self.upgradeDescription = QLabel(automationGameLogic.getDescription(self.name))
        self.upgradeDescription.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.upgradeDescription, 1, 0)
        
        self.upgradeButton = QPushButton(automationGameLogic.parseCost(self.name))
        self.upgradeButton.clicked.connect(self.purchase)
        self.layout_.addWidget(self.upgradeButton, 2, 0)
        
        self.usefulDescription = QLabel(automationGameLogic.parseUsefulDescription(self.name))
        self.layout_.addWidget(self.usefulDescription, 3, 0)
        self.setLayout(self.layout_)
        
    
    def purchase(self):
        observerModel.callEvent(observerModel.Observable.AUTOMATION_OBSERVABLE, observerModel.ObservableCallType.GAINED, (self.name, gamedefine.gamedefine.automationLevels[self.name])) 
        if automationGameLogic.canAffordUpgrade(self.name):
            automationGameLogic.purchaseUpgrade(self.name)
            automationGameLogic.updateUpgradeStatus(self.name)
                
            self.usefulDescription.setText(automationGameLogic.parseUsefulDescription(self.name))
            self.upgradeDescription.setText(automationGameLogic.getDescription(self.name))
            self.upgradeLabel.setText(automationGameLogic.parseUpgradeName(self.name))
            self.upgradeButton.setText(automationGameLogic.parseCost(self.name))
              

    def updateDisplay(self):
        if automationGameLogic.canAffordUpgrade(self.name):
            self.upgradeButton.setEnabled(True)
        else:
            self.upgradeButton.setEnabled(False)
            
        if gamedefine.gamedefine.automationDisabledState[self.name][0]:
            self.upgradeLabel.setText(f"Disabled | {automationGameLogic.parseUpgradeName(self.name)}")
        else:
            self.upgradeLabel.setText(automationGameLogic.parseUpgradeName(self.name))
        
        
    def updateInternal(self):
        if not gamedefine.gamedefine.automationLevels[self.name] == 0:
            if automationGameLogic.getCurrentInternalMultiLevelUpgrade(self.name)["type"] == "idleGenerator":
                self.lastTickTime = automationGameLogic.doUpgradeTask(self.name, self.lastTickTime)
            
    def updateEverything(self):
        self.updateDisplay()
        self.updateInternal()
        self.usefulDescription.setText(automationGameLogic.parseUsefulDescription(self.name))
        self.upgradeDescription.setText(automationGameLogic.getDescription(self.name))
        self.upgradeLabel.setText(automationGameLogic.parseUpgradeName(self.name))
        self.upgradeButton.setText(automationGameLogic.parseCost(self.name))
        

        
class content(QWidget):
    def __init__(self):
        super().__init__()
        self.layout_ = QVBoxLayout()
        self.layout_.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.automationBlocks = []
        for i in gamedefine.gamedefine.automationsToCreate:
            print("creating automation " + i)
            self.automationBlocks.append(automationBlock(i))
            self.layout_.addWidget(self.automationBlocks[-1])
        
        self.setLayout(self.layout_)
    
    def updateDisplay(self):
        for i in self.automationBlocks:
            i.updateDisplay()
        
    def updateInternal(self):
        for i in self.automationBlocks:
            i.updateInternal()
            
    def updateEverything(self):
        for i in self.automationBlocks:
            i.updateEverything()