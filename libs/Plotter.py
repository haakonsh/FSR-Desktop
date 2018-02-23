# coding=utf-8
import matplotlib.pyplot as plt
import matplotlib
import numpy as np


class PlotObject(object):
    """
    Object containing the plots.
    """
    
    def __init__(self, device):
        
        matplotlib.interactive(True)
        fig, self.ax = plt.subplots()
        self.subPlotArray = []

        self.addSubPlot(title = 'Comparison between the outputs of the filters',
                        lable = 'Unity based normalization',
                        xdata = device.unityBasedNormalized[11],
                        color = 'b',
                        yscale = 'linear')

        self.addSubPlot(lable = 'Non-linearity compensation',
                        xdata = device.nonLinearityCompensated[11],
                        color = 'g',
                        title = None,
                        yscale = None)

        self.addSubPlot(lable = 'Averaging filter',
                        xdata = device.averaged[11],
                        color = 'r',
                        title = None,
                        yscale = 'linear')
        
        x = np.arange(0.0, 1.0, 0.001)
        y = np.arange(0.0, 1.0, 0.001)
        for i in range(0, len(y)):
            y[i] = 1 - np.exp(-5.35 * y[i])

        self.addPlot(figure = 2,
                     xdata = x,
                     ydata = y,
                     title = ('Non-linear compensation curve: ' + device.nonLinearityCompensationCurve))

        self.showPlot()
        
    def addSubPlot(self, title, lable, xdata, color, yscale):
        """
        
        :param title:   string
        :param lable:   string
        :param xdata:   array
        :param color:   matplotlib color string
        :param yscale:  string {“linear”, “log”, “symlog”, “logit”}
        :return:        None
        """
        placeholder, = self.ax.plot(xdata, color = color, label = lable)
        self.subPlotArray.append(placeholder)
        if title:
            self.ax.set_title(title)
        if yscale:
            self.ax.set_yscale(yscale)

        self.ax.legend(loc = 'best')
        self.ax.set_ybound(lower = 0.0, upper = 1.0)
        self.ax.grid(b = 'on', which = 'both', axis = 'both')
        self.ax.minorticks_on()

    def addPlot(self, figure,  title, xdata, ydata = None):
        """
        
        :param figure:  int
        :param title:   string
        :param xdata:   array
        :param ydata:   array
        :return:        None
        """
        plt.figure(num = figure)
        if ydata.any():
            plt.plot(xdata, ydata)
        else:
            plt.plot(xdata)
        plt.title(title)
        
    def showPlot(self):
        """
        :return: None
        """
        print (plt.isinteractive())
        plt.show()

