#standard imports
import json
#third party imports
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
#local imports
import gamedefine
import game
import logging
import urbanistFont
import observerModel

class purchaseStrip(QWidget):
    def __init__(self, name):
        super().__init__()
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.name = name
        if not gamedefine.internalGameDefine[name] == None:
            self.internalItem = gamedefine.internalGameDefine[name]
            self.visualItem = gamedefine.visualGameDefine[name]
        else:
            self.item = gamedefine.internalGameDefine["proton"]
            self.visualItem = gamedefine.visualGameDefine["proton"]
            name = "proton"
            logging.log(f"error importing item '{name}' from gamedefine", 3)

        self.setToolTip(gamedefine.visualGameDefine[name]["description"])
        self.setToolTipDuration(5000)
        
        self.label = QLabel(f"You have {gamedefine.amounts[name]} {self.visualItem['visualName'].lower()}")
        self.layout.addWidget(self.label)
        if not name == "quarks":
            self.purchaseButton = QPushButton("")
        else:
            self.purchaseButton = QPushButton("Free")
        self.purchaseButton.clicked.connect(self.purchase)
        self.layout.addWidget(self.purchaseButton)
        
        self.setLayout(self.layout)
    
    def purchase(self):
        observerModel.g_observable.notify_observers(type = "purchase", name = self.name)
        if self.name == "quarks":
            game.purchase("quarks")
            return 0
        
        if game.canAfford(self.name):
            game.purchase(self.name)

    def parseCost(self, name):
        what = self.internalItem["whatItCosts"]
        string = ["Cost: "]
        
        for i in what:
            string.append(str(i["amount"]) + " ")
            if i["amount"] == 1:
                string.append(i["what"][:-1])
            else:
                string.append(i["what"])
            if what.index(i) < len(what) - 2:
                string.append(", ")
            elif what.index(i) == len(what) - 2:
                string.append(" and ")
        
        return "".join(string)
    
    def updateTab(self):
        """
        Updates the tab with the current information.

        This method updates the label text to display the amount of a specific item the player has.
        It also updates the purchase button text to display the cost of the item.
        If the item is "quarks", the purchase button text is set to "Free".
        """
        self.label.setText(f"You have {game.humanReadableNumber(gamedefine.amounts[self.name])} {self.visualItem['visualName'].lower()}")
        
        if not gamedefine.internalGameDefine[self.name]["whatItCosts"][0]["amount"] == -1:

            self.purchaseButton.setText(self.parseCost(self.name))
            if not game.canAfford(self.name):
                self.purchaseButton.setDisabled(True)
            else:
                self.purchaseButton.setDisabled(False)
        else:
            self.purchaseButton.setText("Free")

class header(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.label = QLabel("Buy x")
        self.textEdit = QLineEdit()
        self.textEdit.setValidator(QIntValidator())
        self.textEdit.textChanged.connect(self.updateBuyMultiple)
        
    def updateBuyMultiple(self):
        gamedefine.mainTabBuyMultiple = int(self.textEdit.text())
    
        
    def switchBuyButton(self):
        pass
        
        
        
class content(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.purchaseStrips = []
        for i in gamedefine.purchaseToCreate:
            if not i == "electrons":
                print("Creating " + str(i))
                self.purchaseStrips.append(purchaseStrip(i))
                self.layout.addWidget(self.purchaseStrips[-1])
        
        self.setLayout(self.layout)
    
    def updateDisplay(self):
        for i in self.purchaseStrips:
            i.updateTab()
            