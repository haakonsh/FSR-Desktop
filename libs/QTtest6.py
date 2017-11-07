import sys
import math
from PyQt4 import QtGui, QtCore
from random import randint

NUMBER_OF_HEXAGONS = 36



class Window(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        
        self.setUpdatesEnabled(True)    # Needed in order to trigger the paintEvent of a QWidget
        self.setGeometry(350, 35, 750, 940)     # (pos x, pos y, width, height)
        self.setWindowTitle('MainWindow')
        
        self.mainWidget = QtGui.QWidget(self)
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.mainWidget.setLayout(self.verticalLayout)  # Vertical division of mainWidget
        
        self.display = HexGridWidget(vertices = 6, radius = 40, angularOffset = 0)
        self.verticalLayout.addWidget(self.display)     # Adds the hex grid to the mainWidget

        self.control = QtGui.QWidget(self)
        self.controlLayout = QtGui.QHBoxLayout(self)    # Horizontal division of the control QWidget
        
        self.playButton = QtGui.QPushButton("Play", self)
        self.stopButton = QtGui.QPushButton('Stop', self)
        self.resetButton = QtGui.QPushButton('Reset', self)
        self.playButton.clicked.connect(self.play)
        self.stopButton.clicked.connect(self.stop)
        self.resetButton.clicked.connect(self.reset)
        
        self.controlLayout.addWidget(self.playButton)
        self.controlLayout.addWidget(self.stopButton)
        self.controlLayout.addWidget(self.resetButton)
        
        self.verticalLayout.addLayout(self.controlLayout)   # Adds the control buttons to the mainWidget
        
        self.setCentralWidget(self.mainWidget)
        self.mainWidget.resize(self.mainWidget.sizeHint())
        self.show()     # Triggers the Window's paintEvent
        
        self.colors = []
        
        # TODO Remove block
        color = QtGui.QColor(255, 0, 0, 255)
        print (str(color.rgb()))
        print (str(hex(color.rgb())))
        # End of block
        
        for i in range(0, NUMBER_OF_HEXAGONS):
            self.colors.append(QtGui.QBrush(QtGui.QColor(randint(0, 255), randint(0, 255), randint(0, 255), 255)))
        self.display.updateColors(self.colors)
        
    def play(self):
        print ("Clicked Play!")
        #TODO Decode FSR hex value to a RGB int

    def stop(self):
        print ("Clicked Stop!")
        #TODO Stop playback of FSR
        
    def reset(self):
        print ("Clicked Reset!")
        #TODO Reset playback

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
                
                # Move the polygon points to the next position in the grid
                offsetRow = self.polygon[i * 6 + j].at(1) - self.polygon[i * 6 + j].at(3)
                offsetCol = self.polygon[i * 6 + j].at(5) - self.polygon[i * 6 + j].at(3)
                self.polygon[i * 6 + j].translate(j * offsetCol.x() + i * offsetRow.x(),
                                                  j * offsetCol.y() + i * offsetRow.y())
        
        for i in range(0, NUMBER_OF_HEXAGONS):
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
        for i in range(0, NUMBER_OF_HEXAGONS):
            self.brushList[i] = colorList[i]
        
        return self.repaint()
    
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        for i in range(0, NUMBER_OF_HEXAGONS):
            painter.setBrush(self.brushList[i])
            painter.drawPolygon(self.polygon[i])


def run():
    app = QtGui.QApplication(sys.argv)
    gui = Window()
    sys.exit(app.exec_())


run()
