# -*- coding: utf-8 -*-
from PyQt4.QtGui import QFileDialog
import numpy
from pyqtgraph.parametertree import Parameter, ParameterTree
import pyqtgraph as pg
from Graphic_Interface.Windows.Two_Dimensional_AnalisysWindowUI import Ui_TwoDimensionalWindow
from PyQt4 import QtGui

class TwoDimensionalAnalisysWindow(QtGui.QMainWindow,Ui_TwoDimensionalWindow):
    def __init__(self,parent=None,columns=None, data=None):
        super(TwoDimensionalAnalisysWindow, self).__init__(parent)
        self.setupUi(self)

        #self.axisX = pg.AxisItem(orientation='bottom')
        #self.axisY = pg.AxisItem(orientation='left')

        self.show()
        self.widget.getPlotItem().showGrid(x=True, y=True)
        self.widget.getPlotItem().hideButtons()
        self.widget.setMouseEnabled(x=False, y=False)
        self.widget.setMenuEnabled(False)
        self.widget.enableAutoRange()
        self.legend = None
        self.scatter_plot = None


        self.columns = columns if columns is not None else []
        self.visual_elements = []
        #the numpy [,] array with the parameter measurement
        self.data = data if data is not None else numpy.zeros(4).reshape((2,2))
        self.createParameterTreeOptions(self.columns)

    def createParameterTreeOptions(self,columnNames):

        xaxis = [unicode(x) for x in columnNames]
        if len(xaxis) == 0:
            return
        params = [
            {u'name': u'X Axis Parameter Settings', u'type': u'group', u'children':
                [{u'name': u'X Axis', u'type': u'list',u'value': xaxis[0],
                  u'default': xaxis[0], u'values': [(name, i) for i,name in enumerate(xaxis)]}]},
            {u'name': u'Y Axis Parameter Settings', u'type': u'group', u'children':
                [{u'name': u'Y Axis', u'type': u'list', u'value':xaxis[0],
             u'default': xaxis[0], u'values': [(name, i) for i,name in enumerate(xaxis)]}]},

            {u'name': u'Color', u'type': u'color', u'value': "00F"},
            {u'name': u'Figures Size', u'type': u'int', u'value': 8},
            {u'name': u'Figures Shape', u'type': u'list', u'value': "o",
             u'default': "o", u'values': [("Circle","o"),("Square","s"),("Triangle","t"),("Diamond","d"),("Plus","+")]},
            #{u'name': u'Include Legend', u'type': u'bool', u'value': True},
            {u'name': u'Save Graph as Image', u'type': u'action'},
            {u'name': u'Compute Two Dimensional Graph', u'type': u'action'}]

        lay1 = QtGui.QVBoxLayout()
        lay1.setMargin(0)

        self.ParamTree = Parameter.create(name=u'params', type=u'group', children=params)
        self.parameterTree = ParameterTree()
        lay1.addWidget(self.parameterTree)
        self.parameterTree.setAutoScroll(True)
        self.parameterTree.setHeaderHidden(True)
        self.parameterTree.setParameters(self.ParamTree, showTop=False)
        self.dockWidgetContents.setLayout(lay1)
        self.parameterTree.setFixedWidth(340)
        self.ParamTree.param(u'Compute Two Dimensional Graph').sigActivated.connect(self.plot)
        self.ParamTree.param(u'Save Graph as Image').sigActivated.connect(self.saveGraphImage)

    def load_Theme(self, theme):
        self.widget.setBackground(theme.osc_background)
        self.widget.getPlotItem().showGrid(x=theme.osc_GridX, y=theme.osc_GridY)

    def saveGraphImage(self):
        fname = unicode(QFileDialog.getSaveFileName(self,"Save two dimensional graphics as an Image ","-Duetto-Image","*.jpg"))
        if fname:
            #save as image
            image = QtGui.QPixmap.grabWindow(self.widget.winId())
            image.save(fname, 'jpg')

    def plot(self):
        #the elements and the colors to plot
        self.widget.clear()

        i, j = self.ParamTree.param(u'X Axis Parameter Settings').param(u'X Axis').value(),\
               self.ParamTree.param(u'Y Axis Parameter Settings').param(u'Y Axis').value()

        color = self.ParamTree.param(u'Color').value()
        shape = self.ParamTree.param(u'Figures Shape').value()
        fig_size = self.ParamTree.param(u'Figures Size').value()

        x_coords = [e[i] for e in self.data]
        y_coords = [e[j] for e in self.data]
        self.scatter_plot = pg.ScatterPlotItem(x=x_coords,y=y_coords,size=fig_size,symbol=shape,brush=(pg.mkBrush(color)))

        self.widget.getPlotItem().getAxis("bottom").setLabel(text=str(self.columns[i]))
        self.widget.getPlotItem().getAxis("left").setLabel(text=str(self.columns[j]))
        self.widget.addItem(self.scatter_plot)


        #if self.ParamTree.param(u'Include Legend').value() and self.legend is None:
        #    self.legend = self.widget.getPlotItem().addLegend()
        #    #legend.setParentItem(self.widget.getPlotItem())
        #    self.legend.addItem(self.scatter_plot,"<h3><br>X Axis: "+str(self.columns[i])+"<br>"
        #                                +"Y Axis: "+str(self.columns[j])+"</h3>")
        #











