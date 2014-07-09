# -*- coding: utf-8 -*-
from PyQt4.QtCore import pyqtSlot
from matplotlib import mlab
import numpy
from Graphic_Interface.Widgets.Power_Spectrum  import Ui_PowSpecWindow
from PyQt4 import QtGui,QtCore
from Duetto_Core.SpecgramSettings import FFTWindows
from Graphic_Interface.Windows.ParameterList import DuettoListParameterItem
from pyqtgraph.parametertree.Parameter import Parameter, ParameterItem
from pyqtgraph.parametertree.parameterTypes import WidgetParameterItem,ListParameter
from pyqtgraph.parametertree import Parameter, ParameterTree


class PowerSpectrumWindow(QtGui.QMainWindow,Ui_PowSpecWindow):
    def __init__(self,parent=None,minY=-50,maxY=5,lines=True,data=[],rate=2):
        super(PowerSpectrumWindow, self).__init__(parent)
        self.ui = Ui_PowSpecWindow()
        self.ui.setupUi(self)
        self.ui.widget.setData(data)
        self.ui.widget.Fs = rate
        self.show()
        self.ui.widget.maxY = maxY
        self.ui.widget.minY = minY
        self.ui.widget.lines =lines
        self.ui.widget.PointerChanged.connect(self.updateStatusBar)
        self.ui.widget.getPlotItem().hideButtons()
        self.ui.dock_settings_contents.setStyleSheet("")
        #Parameter Tree Settings
        params = self.ui.widget.getParamsList()

        ListParameter.itemClass = DuettoListParameterItem
        self.ParamTree = Parameter.create(name=u'params', type=u'group', children=params)
        self.ui.widget.connectSignals(self.ParamTree)

        self.parameterTree = ParameterTree()
        self.parameterTree.setAutoScroll(True)
        self.parameterTree.setFixedWidth(210)

        self.parameterTree.setHeaderHidden(True)
        self.parameterTree.setParameters(self.ParamTree, showTop=False)

        lay1 = QtGui.QVBoxLayout()
        lay1.setMargin(0)
        lay1.addWidget(self.parameterTree)

        self.ui.dock_settings_contents.setLayout(lay1)
        self.ui.dockSettings.setVisible(False)
        self.ui.dockSettings.setFixedWidth(210)


    @pyqtSlot()
    def on_actionOneDimFunctSettings_triggered(self):
        if self.ui.dockSettings.isVisible():
            self.ui.dockSettings.setVisible(False)
        else: self.ui.dockSettings.setVisible(True)


    def load_Theme(self, theme):
         self.ui.widget.backColor = theme.pow_Back
         self.ui.widget.plotColor = theme.pow_Plot
         self.ui.widget.gridX = theme.pow_GridX
         self.ui.widget.gridY = theme.pow_GridY


    def updateStatusBar(self,message):
        self.ui.statusbar.showMessage(message, 5000)

    def updatePowSpectrumInterval(self,data):
        self.ui.widget.updateLast(data)
