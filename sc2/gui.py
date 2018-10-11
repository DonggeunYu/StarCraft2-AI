import cv2
import sys
import sc2
import numpy as np

from sc2.map_info import map_environment
from sc2 import position
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import QImage
from PyQt5.uic import loadUi

class Form(QtWidgets.QDialog):
    def __init__(self, parent=None):
        print("Start gui.py")

        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi("pyqt5_gui.ui")
        self.ui.show()
        self.loadimage(map_environment.map_array)


    def loadimage(self, fname):
        print(np.shape(fname))
        self.image = cv2.imread(fname)
        self.displayImage()

    def displayImage(self):
        self.imgLabel.setPixmap(QPixmap=fromImage(img))
        self.imgLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignHCenter)

def Show_Gui():
    app = QtWidgets.QApplication(sys.argv)
    w = Form()
    sys.exit(app.exec())

Show_Gui() #Test