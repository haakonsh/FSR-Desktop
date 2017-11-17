import sys
import math
from PyQt4 import QtGui, QtCore
from random import randint
from time import sleep


class Window(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)

        self.setUpdatesEnabled(True)
        self.setGeometry(350, 35, 750, 940)
        self.setWindowTitle('MainWindow')
        
        self.mainWidget = QtGui.QWidget(self)
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.mainWidget.setLayout(self.verticalLayout)
        
        self.display = HexGridWidget(vertices = 6, radius = 40, angularOffset = 0)
        
        self.control = QtGui.QDialogButtonBox(self.mainWidget)
        self.control.addButton('Play', self.control.ActionRole)
        self.control.addButton('Stop', self.control.ActionRole)
        self.control.addButton('Reset', self.control.ActionRole)
        
        self.verticalLayout.addWidget(self.display)
        self.verticalLayout.addWidget(self.control)
        
        self.setCentralWidget(self.mainWidget)
        self.mainWidget.resize(self.mainWidget.sizeHint())
        self.show()
        
        self.colors = []
        
        for i in range(0, 36):
            self.colors.append(QtGui.QBrush(QtGui.QColor(randint(0, 255), randint(0, 255), randint(0, 255), 255)))
        self.display.updateColors(self.colors)
        
class HexGridWidget(QtGui.QWidget):
    def __init__(self, vertices, radius, angularOffset = 0, parent = None):
        super(HexGridWidget, self).__init__(parent)
        
        self.setGeometry(350, 35, 600, 840)
        self.setUpdatesEnabled(True)
        self.pen = QtGui.QPen(QtGui.QColor(0, 0, 0))
        self.pen.setWidth = 3
        self.brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 255))
        self.brushList = []
        self.polygon = []
        
        for i in range(0, 6):
            for j in range(0, 6):
                self.polygon.append(self.createHexagon(vertices, radius, angularOffset))
                offsetRow = self.polygon[i * 6 + j].at(1) - self.polygon[i * 6 + j].at(3)
                offsetCol = self.polygon[i * 6 + j].at(5) - self.polygon[i * 6 + j].at(3)
                
                self.polygon[i*6 + j].translate(j * offsetCol.x() + i * offsetRow.x(), j * offsetCol.y() + i * offsetRow.y())  # Move the polygon points to the next position in the grid
                
        for i in range(0, 36):
            self.brushList.append(QtGui.QBrush(QtGui.QColor(255, 255, 255, 255)))
    
    def createHexagon(self, n, r, s):
        hexagon = QtGui.QPolygon()
        w = 360 / n
        
        for i in range(n):
            t = w * i + s
            x = r * math.cos(math.radians(t))
            y = r * math.sin(math.radians(t))
            hexagon.append(QtCore.QPoint(x + r, (self.height() / 2) + y))
        
        return hexagon
    
    def updateColors(self, colorList):
        for i in range(0, 36):
            self.brushList[i] = colorList[i]
        
        return self.repaint()
        
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        for i in range(0, 36):
            painter.setBrush(self.brushList[i])
            painter.drawPolygon(self.polygon[i])


def run():
    app = QtGui.QApplication(sys.argv)
    gui = Window()
    sys.exit(app.exec_())


run()
