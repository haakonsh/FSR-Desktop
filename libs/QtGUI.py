try:
    import math
    import sys
    from PyQt4 import QtGui, QtCore
    from random import randint
    from time import sleep

except ImportError as ie:
    print (str(ie))
    # Catched if any packages are missing
    missing = str(ie).split("named")[1]
    print("Software needs %s installed\nPlease run pip install %s and restart\r\n" % (missing, missing))
    input("Press any key to exit...")
    exit()
except ValueError as e:
    print (str(e))
    input("Press any key to exit...")
    exit()

def guiAppInit():
    try:
        app = QtGui.QApplication(sys.argv)
    
    except Exception as e:
        print("Unable to start QApplication.")
        print(str(e))
        exit()
    
    return app


def samplesToGui(device, number_of_sensors, number_of_samples, qt_app = None):
    try:
        color_list = [0] * number_of_sensors
        
        for i in range(0, number_of_samples):
            for j in range(0, number_of_sensors):
                color_list[j] = QtGui.QBrush(QtGui.QColor((device.samples[j][i] + 4096) * 2048))
                # 2^12bit = 4096. Adding this number shifts the value range into positive integers only.
            # TODO Call HexGridWidget.updateColor(colorList)
            qt_app.display.updateColors(color_list)
            qt_app.display.repaint()
            sleep(0.02)
    
    except Exception as e:
        print("Unable to update colors.")
        print(str(e))
        exit()
        

class Window(QtGui.QMainWindow):
    def __init__(self, number_of_hexagons, parent = None):
        super(Window, self).__init__(parent)
        
        self.setUpdatesEnabled(True)    # Needed in order to trigger the paintEvent of a QWidget
        self.setGeometry(100, 35, 750, 940)     # (pos x, pos y, width, height)
        self.setWindowTitle('MainWindow')
        
        self.mainWidget = QtGui.QWidget(self)
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.mainWidget.setLayout(self.verticalLayout)  # Vertical division of mainWidget
        
        self.display = HexGridWidget(vertices = 6, radius = 40, angularOffset = 0, number_of_hexagons = number_of_hexagons)
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
        print ("Window initialized!")
        self.colors = []
        
        #TODO Remove block
        for i in range(0, number_of_hexagons):
            self.colors.append(QtGui.QBrush(QtGui.QColor(randint(0, 255), randint(0, 255), randint(0, 255), 255)))
        self.display.updateColors(self.colors)
        # End of block
        
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
    def __init__(self, vertices, radius, number_of_hexagons, angularOffset = 0, parent = None):
        super(HexGridWidget, self).__init__(parent)
        
        self.number_of_hexagons = number_of_hexagons
        self.setGeometry(100, 35, 600, 840)
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
        
        for i in range(0, self.number_of_hexagons):
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
        for i in range(0, self.number_of_hexagons):
            self.brushList[i] = colorList[i]
        
        #return self.repaint()
    
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        for i in range(0, self.number_of_hexagons):
            painter.setBrush(self.brushList[i])
            painter.drawPolygon(self.polygon[i])


