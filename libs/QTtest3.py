import sys
import math
from PyQt4 import QtGui, QtCore

class Window(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        
        self.setGeometry(350, 200, 810, 640)
        self.setWindowTitle('MainWindow')

        self.mainWidget = QtGui.QWidget(self)
        self.gridLayout = QtGui.QGridLayout(self.mainWidget)
        self.gridLayout.sizeConstraint = QtGui.QLayout.SetDefaultConstraint

        self.listOfWidgets = []

        number = 0
        for row in range(1, 7):
            for col in range(1, 7):
                self.listOfWidgets.append(HexWidget(parent = self.mainWidget, vertices = 6, radius = 50, angularOffset = 0))
                self.gridLayout.addWidget(self.listOfWidgets[number], row, col)
                number += 1

        self.mainWidget.setLayout(self.gridLayout)
        self.setCentralWidget(self.mainWidget)
        self.mainWidget.resize(self.mainWidget.sizeHint())
        self.show()
        

class HexWidget(QtGui.QWidget):
    def __init__(self, vertices, radius, angularOffset = 0, parent = None):
        super(HexWidget, self).__init__(parent)
        self.pen = QtGui.QPen(QtGui.QColor(0, 0, 0))
        self.pen.setWidth = 3
        self.verticalHeight = 0
        self.horizontalHeight = 0
        self.brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 255))
        self.polygon = self.createHexagon(vertices, radius, angularOffset)
        self.polygon.translate(25, 35)
        
        self.setUpdatesEnabled(True)
        
    def createHexagon(self, n, r, s):
        hexagon = QtGui.QPolygon()
        w = 360 / n
        
        for i in range(n):
            t = w * i + s
            x = r * math.cos(math.radians(t))
            y = r * math.sin(math.radians(t))
            hexagon.append(QtCore.QPoint(self.width() / 2 + x, self.height() / 2 + y))
            
        return hexagon
    
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.drawPolygon(self.polygon)


def run():
    app = QtGui.QApplication(sys.argv)
    gui = Window()
    sys.exit(app.exec_())


run()
