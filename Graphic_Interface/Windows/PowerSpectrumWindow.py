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
    def __init__(self,parent=None,minY=-50,maxY=5,lines=True,data=[],theme=None,rate=2, bitdepth=0,maxYOsc=0):
        super(PowerSpectrumWindow, self).__init__(parent)
        self.ui = Ui_PowSpecWindow()
        self.ui.setupUi(self)
        self.ui.widget.setData(data,bitdepth,maxYOsc,rate)
        self.ui.widget.Fs = rate
        self.show()
        self.ui.widget.backColor = theme.pow_Back
        self.ui.widget.plotColor = theme.pow_Plot
        self.ui.widget.gridX = theme.pow_GridX
        self.ui.widget.gridY = theme.pow_GridY
        self.ui.widget.PointerChanged.connect(self.updateStatusBar)
        self.ui.widget.getPlotItem().hideButtons()
        self.ui.dock_settings_contents.setStyleSheet("")
        #Parameter Tree Settings

        params = self.ui.widget.getParamsList()

        wSettings = {u'name': u'Window Settings', u'type': u'group', u'children': [
            {u'name':u'Plot color', u'type': u'color', u'value':self.ui.widget.plotColor},
            {u'name': u'Background color', u'type': u'color', u'value':self.ui.widget.backColor},
            {u'name': u'Grid', u'type': u'group', u'children':[
                {u'name': u'X', u'type': u'bool', u'value': self.ui.widget.gridX},
                {u'name': u'Y', u'type': u'bool', u'value':self.ui.widget.gridY}]},
        ]}
        params.append(wSettings)
        ListParameter.itemClass = DuettoListParameterItem
        self.ParamTree = Parameter.create(name=u'params', type=u'group', children=params)
        self.ui.widget.connectSignals(self.ParamTree)

        self.parameterTree = ParameterTree()
        self.parameterTree.setAutoScroll(True)
        self.parameterTree.setFixedWidth(250)

        self.parameterTree.setHeaderHidden(True)
        self.parameterTree.setParameters(self.ParamTree, showTop=False)

        lay1 = QtGui.QVBoxLayout()
        lay1.setMargin(0)
        lay1.addWidget(self.parameterTree)

        self.ui.dock_settings_contents.setLayout(lay1)
        self.ui.dockSettings.setVisible(False)
        self.ui.dockSettings.setFixedWidth(250)


    @pyqtSlot()
    def on_actionOneDimFunctSettings_triggered(self):
        if self.ui.dockSettings.isVisible():
            self.ui.dockSettings.setVisible(False)
        else: self.ui.dockSettings.setVisible(True)

    def updateStatusBar(self,message):
        self.ui.statusbar.showMessage(message, 5000)

    def updatePowSpectrumInterval(self,data):
        self.ui.widget.updateLast(data)
