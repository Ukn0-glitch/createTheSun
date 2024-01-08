import gamedefine
import copy
from PyQt6.QtCore import QSaveFile
import os
import json
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QVBoxLayout

save_ = {}


def save():
    save_ = gamedefine.getSaveData()
    
    appdata = os.environ["APPDATA"]
    savedir = os.path.join(appdata, "CreateTheSun", "Saves")
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    savefile = os.path.join(savedir, "save.json")
    with open(savefile, "w") as f:
        json.dump(save_, f)
    
    
def load():
    dialog = CustomDialog("Are you sure you want to load? This will overwrite your current save.", "Load", True, QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No)
    
    if dialog.exec() == QDialog.DialogCode.Rejected:
        return
    
    appdata = os.environ["APPDATA"]
    savedir = os.path.join(appdata, "CreateTheSun", "Saves")
    if not os.path.exists(savedir):
        return
    savefile = os.path.join(savedir, "save.json")
    if not os.path.exists(savefile):
        return
    with open(savefile, "r") as f:
        save_ = json.load(f)
    
    gamedefine.loadSave(save_)
    
    
class CustomDialog(QDialog):
    def __init__(self, text, windowTitle = "Dialog", cancelable = True, customQBtn = None ):
        super().__init__()

        self.setWindowTitle(windowTitle)
        if not customQBtn == None:
            if cancelable == True:
                QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
            else:
                QBtn = QDialogButtonBox.StandardButton.Ok
        else:
            QBtn = customQBtn

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout_ = QVBoxLayout()
        message = QLabel(text)
        self.layout_.addWidget(message)
        self.layout_.addWidget(self.buttonBox)   
        self.setLayout(self.layout_)
        
