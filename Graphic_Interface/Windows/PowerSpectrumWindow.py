# -*- coding: utf-8 -*-
from PyQt4.QtCore import pyqtSlot
from Graphic_Interface.Widgets.Power_Spectrum  import Ui_PowSpecWindow
from PyQt4 import QtGui
from Graphic_Interface.Windows.ParameterList import DuettoListParameterItem
from pyqtgraph.parametertree.parameterTypes import WidgetParameterItem,ListParameter
from pyqtgraph.parametertree import Parameter, ParameterTree


class PowerSpectrumWindow(QtGui.QMainWindow,Ui_PowSpecWindow):
    def __init__(self,parent=None,lines=True,data=[],range=[],NFFTSpec=0,theme=None,rate=2, bitdepth=0, updateInterval=lambda:None):
        super(PowerSpectrumWindow, self).__init__(parent)
        self.ui = Ui_PowSpecWindow()
        self.ui.setupUi(self)
        self.ui.widget.setData(data, range, bitdepth, rate, NFFTSpec, updateInterval)
        self.show()
        self.ui.widget.backColor = theme.pow_Back
        self.ui.widget.plotColor = theme.pow_Plot
        self.ui.widget.gridX = theme.pow_GridX
        self.ui.widget.gridY = theme.pow_GridY
        self.ui.widget.PointerChanged.connect(self.updateStatusBar)
        self.ui.widget.getPlotItem().hideButtons()
        self.ui.dock_settings_contents.setStyleSheet("background-color:#DDF")
        #Parameter Tree Settings

        params = self.ui.widget.getParamsList()

        wSettings = {u'name': unicode(self.tr(u'Window Settings')), u'type': u'group', u'children': [
            {u'name': unicode(self.tr(u'Plot color')), u'type': u'color', u'value':self.ui.widget.plotColor},
            {u'name': unicode(self.tr(u'Background color')), u'type': u'color', u'value':self.ui.widget.backColor},
            {u'name': unicode(self.tr(u'Grid')), u'type': u'group', u'children':[
                {u'name': unicode(self.tr(u'X')), u'type': u'bool', u'value': self.ui.widget.gridX},
                {u'name': unicode(self.tr(u'Y')), u'type': u'bool', u'value':self.ui.widget.gridY}]},
            # {u'name': u'Lines', u'type':u'bool', u'value': self.ui.widget.lines},
        ]}
        params.append(wSettings)
        ListParameter.itemClass = DuettoListParameterItem
        self.ParamTree = Parameter.create(name=u'params', type=u'group', children=params)
        self.ParamTree.sigTreeStateChanged.connect(self.windowSettingsChange)
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

    def windowSettingsChange(self, param, changes):

        for param, change, data in changes:
            path = self.ParamTree.childPath(param)
            if path is not None:
                childName = '.'.join(path)
            else:
                childName = param.name()

            if childName == unicode(self.tr(u'Window Settings.Plot color')):
                self.ui.widget.plotColor = data
            elif childName == unicode(self.tr(u'Window Settings.Background color')):
                self.ui.widget.backColor = data
                self.ui.widget.setBackground(data)
                return
            elif childName == unicode(self.tr(u'Window Settings.Grid.X')):
                self.ui.widget.gridX = data
                self.ui.widget.showGrid(x=data, y=self.ui.widget.gridY)
                return
            elif childName == unicode(self.tr(u'Window Settings.Grid.Y')):
                self.ui.widget.gridY = data
                self.ui.widget.showGrid(x=self.ui.widget.gridX, y=data)
                return
            else: return
            self.ui.widget.refresh()

    @pyqtSlot()
    def on_actionOneDimFunctSettings_triggered(self):
        if self.ui.dockSettings.isVisible():
            self.ui.dockSettings.setVisible(False)
        else: self.ui.dockSettings.setVisible(True)

    def updateStatusBar(self,message):
        self.ui.statusbar.showMessage(message, 5000)

    def updatePowSpectrumInterval(self,range):
        self.ui.widget.updateLast(range)
