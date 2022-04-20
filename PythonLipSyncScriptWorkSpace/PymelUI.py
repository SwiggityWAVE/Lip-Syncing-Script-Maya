from PySide2 import QtCore, QtWidgets
import pymel.core as pm

def ChangeFilePathForAudioFile():
    pm.fileDialog2(fileFilter="*.wav")
    print("audioFile")
  
def ChangeFilePathForModel():
    print("model")
    
def ChangeFilePathForConfig():
    print("config")



#MAIN LOOP
wid = QtWidgets.QWidget()
wid.resize(1024, 1024)
wid.setWindowTitle("Window")

#File system

filePathKeys = ["audioFile", "model", "config"]
filePaths = {"audioFile" : "something.wav", "model" : "ModelPath", "config" : "ConfigPath"}
filePathQLineEdit = []
changeFilePathQPushButton = []

index = 0
for key in filePathKeys:
    filePathQLineEdit.append(QtWidgets.QLineEdit(filePaths[key], parent = wid))
    filePathQLineEdit[index].move(256, 48 * index)
    
    changeFilePathQPushButton.append(QtWidgets.QPushButton('ChangeFilePath', parent = wid))
    changeFilePathQPushButton[index].move(400, 48 * index)
    index += 1
    
changeFilePathQPushButton[0].clicked.connect(ChangeFilePathForAudioFile)
changeFilePathQPushButton[1].clicked.connect(ChangeFilePathForModel)
changeFilePathQPushButton[2].clicked.connect(ChangeFilePathForConfig)

#Viseme System
#Lists all blendshapes in scene
blendShapes = pm.general.ls(exactType = "blendShape")
blendShapesAsString = []
for blendshape in blendShapes:
    blendShapesAsString.append(str(blendshape))


visemeList = ["Silent: ", "PP: ", "FF: ", "TH: ", "DD: ", "kk: ", "CH: ", "SS: ", "nn: ", "RR: ", "aa: ", "E: ", "I: ", "O: ", "U: "]
visemeLabel = []
visemeQComboBox = []


index = 0
for viseme in visemeList:
    visemeLabel.append(QtWidgets.QLabel(wid))
    visemeLabel[index].setText(visemeList[index])
    visemeLabel[index].move(0, 48 * index)
    
    visemeQComboBox.append(QtWidgets.QComboBox(wid))
    visemeQComboBox[index].addItems(blendShapesAsString)
    visemeQComboBox[index].move(visemeLabel[index].width(), 48 * index)
    
    
    index += 1





############################################
"""
dropDown = QtWidgets.QComboBox(wid)
dropDown.addItems(blendShapesAsString)
dropDown.move(dropDownLabel.width(), 0)
"""



wid.show()

"""
#Execute mainProgram
executeButton = QtWidgets.QPushButton('testFunc', parent = wid)
executeButton.resize(128, 32)
executeButton.move(20, 20)
executeButton.clicked.connect(runMainProgram)
"""

