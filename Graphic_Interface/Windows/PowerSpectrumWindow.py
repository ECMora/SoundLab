# -*- coding: utf-8 -*-
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
    def __init__(self,parent=None,minY=-50,maxY=5,lines=True):
        super(PowerSpectrumWindow, self).__init__(parent)
        self.ui = Ui_PowSpecWindow()
        self.ui.setupUi(self)
        self.show()
        self.plotColor = "FFF"
        self.backColor = "000"
        self.gridx = True
        self.gridy = True
        self.maxY = maxY
        self.minY = minY
        self.lines =lines
        self.ui.widget.PointerChanged.connect(self.updateStatusBar)
        self.ui.widget.getPlotItem().showGrid(x=self.gridx, y=self.gridy)

        self.ui.widget.getPlotItem().hideButtons()
        windows = FFTWindows()

        powSpecLogOptions = {u'name': u'Power spectrum (Logarithmic) Settings', u'type': u'group', u'children': [
            {u'name': u'FFT window', u'type': u'list', u'value':windows.Hanning,u'default':windows.Hanning,
             u'values': [(u'Bartlett',windows.Bartlett),(u"Blackman", windows.Blackman),(u"Hamming", windows.Hamming), (u"Hanning", windows.Hanning),(u'Kaiser',windows.Kaiser),(u'None',windows.WindowNone),(u"Rectangular", windows.Rectangular)]},
            {'name': 'Apply Function', 'type': 'action'},
        ]}

        powSpecAvOptions = {u'name': u'Power spectrum (Average) Settings', u'type': u'group', u'children': [
          {u'name':u'FFT size', u'type': u'list', u'default':512, u'values': [(u'Automatic', 512),(u"128", 128), (u"256", 256),(u"512", 512), (u"1024", 1024)], u'value': u'512'},
          {u'name': u'FFT window', u'type': u'list', u'value':windows.Hanning,u'default':windows.Hanning,
             u'values': [(u'Bartlett',windows.Bartlett),(u"Blackman", windows.Blackman),(u"Hamming", windows.Hamming), (u"Hanning", windows.Hanning),(u'Kaiser',windows.Kaiser),(u'None',windows.WindowNone),(u"Rectangular", windows.Rectangular)]},
          {u'name': u'FFT overlap', u'type': u'int', u'value':-1, u'limits': (-1, 99)},
          {'name': 'Apply Function', 'type': 'action'},
        ]}

        #Parameter Tree Settings
        params = [powSpecLogOptions, powSpecAvOptions]


        ListParameter.itemClass = DuettoListParameterItem
        self.ParamTree = Parameter.create(name=u'params', type=u'group', children=params)
        self.ParamTree.sigTreeStateChanged.connect(self.change)
        self.parameterTree = ParameterTree()
        self.parameterTree.setAutoScroll(True)
        self.parameterTree.setFixedWidth(340)

        self.parameterTree.setHeaderHidden(True)
        self.parameterTree.setParameters(self.ParamTree, showTop=False)

        lay1 = QtGui.QVBoxLayout()
        lay1.setMargin(0)
        lay1.addWidget(self.parameterTree)

        self.dock_settings_contents.setLayout(lay1)
        self.dockSettings.setVisible(False)
        self.dockSsettings.setFixedWidth(350)




    def load_Theme(self, theme):
        update_graph =False
        if self.backColor != theme.pow_Back:
            self.backColor = theme.pow_Back
            self.ui.widget.setBackground(self.backColor)

        if self.plotColor != theme.pow_Plot:
            self.plotColor = theme.pow_Plot
            update_graph =True

        if self.gridx != theme.pow_GridX or self.gridy != theme.pow_GridY:
            self.gridx = theme.pow_GridX
            self.gridy = theme.pow_GridY
            self.ui.widget.getPlotItem().showGrid(x=self.gridx, y=self.gridy)

        if update_graph:
            self.ui.widget.update()

    def updateStatusBar(self,message):
        self.ui.statusbar.showMessage(message, 5000)

    def plot(self, data, rate, NFFT, window,overlap):

        self.NFFT = NFFT
        self.window = window
        self.rate = rate
        self.overlap = overlap

        self.ui.widget.logarithmicProcessing(data, rate, window, self.plotColor, self.lines, self.maxY, self.minY)#rate,NFFT,window,overlap,self.maxY, self.minY, self.plotColor, self.lines)
        #self.ui.widget.cepstrumProcessing(data, rate, window, self.plotColor, self.lines, self.maxY, self.minY)#rate,NFFT,window,overlap,self.maxY, self.minY, self.plotColor, self.lines)
        #self.Pxx , self.freqs = self.ui.widget.averageProcessing(data, rate,NFFT,window,overlap,self.maxY, self.minY, self.plotColor, self.lines)

    def updatePowSpectrumInterval(self,data):
        self.plot(data,self.rate,self.NFFT,self.window,self.overlap)
