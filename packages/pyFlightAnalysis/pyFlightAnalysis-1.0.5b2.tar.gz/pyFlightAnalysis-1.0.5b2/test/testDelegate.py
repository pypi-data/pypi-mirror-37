#coding:utf-8


from __future__ import division
import time
import sys
from collections import namedtuple,OrderedDict
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.raw.GL.VERSION.GL_1_1 import GL_SHININESS
from numpy import cos,sin,pi
from PyQt4 import QtCore,QtGui,QtOpenGL
import numpy as np
from pyulog.core import ULog 
import pyqtgraph as pg

from objloader import WFObject
from pyglet.resource import animation
from PyQt4.Qt import pyqtSignal
from __builtin__ import staticmethod




class TableModel(QtCore.QAbstractTableModel):
    """
    A simple 5x4 table model to demonstrate the delegates
    """
    def rowCount(self, parent=QtCore.QModelIndex()): return 5
    def columnCount(self, parent=QtCore.QModelIndex()): return 5

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid(): return None
        if not role==QtCore.Qt.DisplayRole: return None
        return "{0:02d}".format(index.row())
        
    def setData(self, index, value, role=QtCore.Qt.DisplayRole):
        print "setData", index.row(), index.column(), value

    def flags(self, index):
        if (index.column() == 0):
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
        else:
            return QtCore.Qt.ItemIsEnabled

class ButtonDelegate(QtGui.QItemDelegate):

    def __init__(self, parent):
        QtGui.QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        combo = QtGui.QPushButton(str(index.data()), parent)

        #self.connect(combo, QtCore.SIGNAL("currentIndexChanged(int)"), self, QtCore.SLOT("currentIndexChanged()"))
        combo.clicked.connect(self.currentIndexChanged)
        return combo
        
    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        #editor.setCurrentIndex(int(index.model().data(index)))
        editor.blockSignals(False)
        
    def setModelData(self, editor, model, index):
        model.setData(index, editor.text())
        
    @QtCore.pyqtSlot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())
        
class ComboDelegate(QtGui.QItemDelegate):
    """
    A delegate that places a fully functioning QComboBox in every
    cell of the column to which it's applied
    """
    def __init__(self, parent):

        QtGui.QItemDelegate.__init__(self, parent)
        
    def createEditor(self, parent, option, index):
        combo = QtGui.QComboBox(parent)
        num = int(index.model().data(index.model().index(0,4)).toString())
        li = [str(i) for i in range(num)]
        li.append('New')
        combo.addItems(li)
        #combo.setCurrentIndex(parent.current_graph_index)
        self.connect(combo, QtCore.SIGNAL("currentIndexChanged(int)"), self, QtCore.SLOT("currentIndexChanged()"))
        return combo
        
    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        ind = index.model().data(index).toString()
        print(ind)
        editor.setCurrentIndex(int(ind))
        editor.blockSignals(False)
        
    def setModelData(self, editor, model, index):
        num = int(index.model().data(index.model().index(0,4)).toString())
        print(index.row(),index.column())
        num += 1
        model.setData(model.index(0,4),str(num))
        model.setData(index, editor.currentIndex())
            
        
    @QtCore.pyqtSlot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())
    
class myWin(QtGui.QMainWindow):
    def __init__(self,*args,**kwargs):
        super(myWin,self).__init__(*args,**kwargs)
        self.center_widget = win_model()
        self.view = QtGui.QTableView(self)
        self.view.setModel(self.center_widget.model)
        print(id(self.center_widget))
        self.view.setItemDelegateForColumn(1,ComboDelegate(self.center_widget))
        self.setCentralWidget(self.view)

class win_model(QtGui.QWidget):
    def __init__(self,*args,**kwargs):
        super(win_model,self).__init__(*args,**kwargs)
        self.model = QtGui.QStandardItemModel(self)
        self.model.setHorizontalHeaderLabels(['Labels','Index','Color','Show','Numbers'])
        self.graph_count = 0
        self.model.insertRow(0)
        self.model.setData(self.model.index(0,0),'rollspeed')
        self.model.setData(self.model.index(0,1),'1')
        self.model.setData(self.model.index(0,2),'red')
        self.model.setData(self.model.index(0,3),'on')
        self.model.setData(self.model.index(0,4),'1')
        

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainwin = myWin()
    mainwin.show()
    sys.exit(app.exec_())
        
