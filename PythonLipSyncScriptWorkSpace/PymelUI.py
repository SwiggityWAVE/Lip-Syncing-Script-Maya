
import pymel.core as pm

blendShapes = pm.general.ls(exactType = "blendShape")
blendShapesAsString = []
for blendshape in blendShapes:
    blendShapesAsString.append(str(blendshape))


from PySide2 import QtCore, QtWidgets


#MAIN LOOP
wid = QtWidgets.QWidget()
wid.resize(1024, 1024)
wid.setWindowTitle("Window")



DropDown = QtWidgets.QComboBox(wid)
DropDown.addItems(blendShapesAsString)



wid.show()

"""
#Execute mainProgram
executeButton = QtWidgets.QPushButton('testFunc', parent = wid)
executeButton.resize(128, 32)
executeButton.move(20, 20)
executeButton.clicked.connect(runMainProgram)
"""

