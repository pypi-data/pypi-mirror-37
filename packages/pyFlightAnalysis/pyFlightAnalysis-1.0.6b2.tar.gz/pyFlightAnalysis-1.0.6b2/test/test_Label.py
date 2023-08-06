from PyQt4 import QtCore,QtGui,QtOpenGL
import numpy as np
from pyulog.core import ULog 
import pyqtgraph as pg

from objloader import WFObject
from pyglet.resource import animation
from PyQt4.Qt import pyqtSignal
from __builtin__ import staticmethod
import sys

class Label(QtGui.QLabel):
    """ Add Clicked signal to Label
    """
    clicked = pyqtSignal(bool)
    def __init__(self,*args,**kwargs):
        super(Label,self).__init__(*args,**kwargs)
        self.pressed = False
        self.color = [240,240,240]
        self.clicked.connect(self.changeColor)
        
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.pressed = True
    
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.pressed:
            self.clicked.emit(True)
            self.pressed = False
    
    def changeColor(self):
        color = QtGui.QColorDialog.getColor()
        r = color.red()
        b = color.blue()
        g = color.green()
        self.color = [r,g,b]

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainwin = QtGui.QMainWindow()
    mainwin.setCentralWidget(Label())
    mainwin.show()
    sys.exit(app.exec_())
