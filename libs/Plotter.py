import matplotlib.pyplot as plt
import matplotlib
import numpy as np


class PlotObject(object):
    """
    Object containing the plots.
    """
    
    def __init__(self):
        matplotlib.interactive(True)
        fig, self.ax = plt.subplots()
        self.array = []
        self.number = 0
        
    def addPlot(self, title, ylabel, xlabel, xdata, color, ydata = None):
        """
        :param title:   string
        :param ylabel:  string
        :param xlabel:  string
        :param xdata:   array
        :param color:   matplotlib color string
        :param ydata:   array
        :return:        None
        """
        
        placeholder,  = self.ax.plot(xdata, color = color, label = title)
        self.array.append(placeholder)

    def addPlot2(self, title, xdata, ydata = None):
        """
        :param title:   string
        :param ylabel:  string
        :param xlabel:  string
        :param xdata:   array
        :param color:   matplotlib color string
        :param ydata:   array
        :return:        None
        """
    
        placeholder, = self.ax.plot(xdata, ydata, label = title)
        self.array.append(placeholder)
        

    def showPlot(self):
        self.ax.legend(loc = 'best')
        print (plt.isinteractive())
        plt.show()

