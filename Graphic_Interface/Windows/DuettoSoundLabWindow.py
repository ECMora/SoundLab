import sys
from apptools.undo.action.undo_action import UndoAction
from PyQt4 import QtCore, QtGui
import os
from pyqtgraph.parametertree.parameterTypes import WidgetParameterItem,ListParameter
from pyqtgraph.python2_3 import asUnicode
from pyqtgraph.parametertree import Parameter, ParameterTree
from PyQt4.QtGui import QDialog, QMessageBox, QFileDialog, QActionGroup, QAction
from PyQt4.QtCore import SIGNAL, pyqtSlot, QTimer
from Graphic_Interface.Dialogs.NewFileDialog import NewFileDialog
from Duetto_Core.AudioSignals.WavFileSignal import WavFileSignal
from Graphic_Interface.Widgets.DuettoHistogram import DuettoHorizontalHistogramItem, DuettoHorizontalHistogramWidget
from SegmentationAndClasificationWindow import SegmentationAndClasificationWindow
from Duetto_Core.SignalProcessors.FilterSignalProcessor import FILTER_TYPE
from Graphic_Interface.UndoRedoActions import *
from MainWindow import Ui_DuettoMainWindow
from Graphic_Interface.Widgets.MyPowerSpecWindow import PowerSpectrumWindow
from Graphic_Interface.Dialogs import InsertSilenceDialog as sdialog, FilterOptionsDialog as filterdg, ChangeVolumeDialog as cvdialog
from PyQt4 import QtCore, QtGui
import pickle
from WorkTheme import SerializedData
from Graphic_Interface.Widgets.Tools import Tools

MIN_SAMPLING_RATE = 1000
MAX_SAMPLING_RATE = 2000000


class InsertSilenceDialog(sdialog.Ui_Dialog, QDialog):
    pass


class ChangeVolumeDialog(cvdialog.Ui_Dialog, QDialog):
    pass


class FilterDialog(filterdg.Ui_Dialog, QDialog):
    pass

class DuettoListParameterItem(WidgetParameterItem):
    """
    WidgetParameterItem subclass providing comboBox that lets the user select from a list of options.

    """
    def __init__(self, param, depth):
        param.opts['value'] = param.opts['value'][1]
        self.targetValue = None
        self.values = param.opts.get('values',[])
        self.valuesDict = {}
        for (a, b) in self.values:
            self.valuesDict[a] = b
        WidgetParameterItem.__init__(self, param, depth)

    def makeWidget(self):
        opts = self.param.opts
        t = opts['type']
        w = QtGui.QComboBox()
        w.setMaximumHeight(20)  ## set to match height of spin box and line edit
        w.sigChanged = w.currentIndexChanged
        w.value = self.value
        w.setValue = self.setValue
        self.widget = w  ## needs to be set before limits are changed
        self.limitsChanged(self.param, self.param.opts['limits'])
        if len(self.values) > 0:
            self.setValue(self.param.value())
        return w

    def value(self):
        key = asUnicode(self.widget.currentText())
        return self.valuesDict.get(key, None)

    def setValue(self, val):
        self.targetValue = val
        if val not in self.valuesDict.values():
            self.widget.setCurrentIndex(0)
        else:
            for i in range(len(self.values)):
                if self.values[i][1] == val:
                    self.widget.setCurrentIndex(i)
                    break

    def limitsChanged(self, param, limits):
        # set up forward / reverse mappings for name:value

        if len(limits) == 0:
            limits = ['']  ## Can never have an empty list--there is always at least a singhe blank item.

        try:
            self.widget.blockSignals(True)
            val = self.targetValue  #asUnicode(self.widget.currentText())

            self.widget.clear()
            for (k,v) in self.values:
                self.widget.addItem(k)
                if v == val:
                    self.widget.setCurrentIndex(self.widget.count()-1)
                    self.updateDisplayLabel()
        finally:
            self.widget.blockSignals(False)



class DuettoSoundLabWindow(QtGui.QMainWindow, Ui_DuettoMainWindow):
    dropchanged = QtCore.pyqtSignal(QtCore.QMimeData)
    def __init__(self, parent=None):
        super(DuettoSoundLabWindow, self).__init__(parent)
        self.setupUi(self)


        self.hist = DuettoHorizontalHistogramWidget()
        self.widget.histogram = self.hist
        self.pow_overlap = 90
        self.Theme = os.path.join(os.path.join("Utils","Themes"),"RedBlackTheme.dth")
        self.defaultTheme = self.DeSerializeTheme(self.Theme)
        self.widget.spec_background = self.defaultTheme.spec_background
        self.widget.osc_background = self.defaultTheme.osc_background
        self.widget.osc_color = self.defaultTheme.osc_plot
        self.widget.osc_gridx = self.defaultTheme.osc_GridX
        self.widget.osc_gridy = self.defaultTheme.osc_GridY
        self.widget.spec_gridx = self.defaultTheme.spec_GridX
        self.widget.spec_gridy = self.defaultTheme.spec_GridY
        self.pow_spec_backg = self.defaultTheme.pow_Back
        self.pow_spec_plotColor = self.defaultTheme.pow_Plot
        self.pow_spec_gridx = self.defaultTheme.pow_GridX
        self.pow_spec_gridy = self.defaultTheme.pow_GridY
        self.pow_spec_lines = True

        self.pow_spec_maxY = 5
        self.pow_spec_minY = -50
        self.widget.lines = True
        self.statusbar = self.statusBar()
        self.statusbar.setSizeGripEnabled(False)
        self.widget.statusbar = self.statusbar
        self.lastopen = ''
        self.statusbar.showMessage("Welcome to Duetto Sound Lab", 5000)
        params = [
        {'name': 'Oscillogram Settings', 'type': 'group', 'children': [
            {'name': 'Amplitude(%)', 'type': 'group', 'children': [
                 {'name': 'Min', 'type': 'float', 'value': -100, 'step': 0.1},
                 {'name': 'Max', 'type': 'float', 'value': 100, 'step': 0.1},
            ]},

            {'name': 'Grid', 'type': 'group', 'children': [
                {'name': 'X', 'type': 'bool','default': self.defaultTheme.osc_GridX, 'value': self.defaultTheme.osc_GridX},
                {'name': 'Y', 'type': 'bool','default':self.defaultTheme.osc_GridY , 'value': self.defaultTheme.osc_GridY},

            ]},
            {'name':'Background color', 'type':'color','value':self.defaultTheme.osc_background, 'default':self.defaultTheme.osc_background},
            {'name': 'Plot color', 'type': 'color', 'value':self.defaultTheme.osc_plot, 'default': self.defaultTheme.osc_plot},
            {'name': 'Connect Lines', 'type': 'bool','default': self.widget.lines, 'value': self.widget.lines},
        ]},

        {'name': 'Spectrogram Settings', 'type': 'group', 'children': [
            {'name': 'Frequency(kHz)', 'type': 'group', 'children': [
                {'name': 'Min', 'type': 'float', 'value': 0, 'step': 0.1},
                {'name': 'Max', 'type': 'float', 'value': 22, 'step': 0.1},
            ]},
           {'name': 'FFT size', 'type': 'list', 'default':512, 'values': [('Automatic', 512),("32",32),("64", 64),("128", 128), ("512", 512), ("1024", 1024), ('2048', 2048),('4096', 4096)], 'value': '512'},
          {'name': 'FFT window', 'type': 'list', 'value':self.widget.specgramSettings.windows[0],'default':self.widget.specgramSettings.windows[0],'values': [('Bartlett',self.widget.specgramSettings.windows[4]),("Blackman", self.widget.specgramSettings.windows[3]),("Hamming", self.widget.specgramSettings.windows[0]), ("Hanning", self.widget.specgramSettings.windows[2]),('Kaiser',self.widget.specgramSettings.windows[5]),('None',self.widget.specgramSettings.windows[6]),("Rectangular", self.widget.specgramSettings.windows[1])]},
            {'name': 'FFT overlap', 'type': 'int', 'value':-1, 'limits': (-1, 99)},
            {'name': 'Threshold(dB)', 'type': 'group', 'children': [
                {'name': 'Min', 'type': 'float','step':0.1,'default': self.defaultTheme.histRange[0], 'value': self.defaultTheme.histRange[0]},
                {'name': 'Max', 'type': 'float','step':0.1,'default': self.defaultTheme.histRange[1] , 'value': self.defaultTheme.histRange[1]},
             ]},
            {'name': 'Grid', 'type': 'group', 'children': [
                {'name': 'X', 'type': 'bool','default': self.defaultTheme.spec_GridX, 'value': self.defaultTheme.spec_GridX},
                {'name': 'Y', 'type': 'bool','default':self.defaultTheme.spec_GridY , 'value': self.defaultTheme.spec_GridY},

            ]},
            {'name': 'Background color', 'type': 'color', 'value':self.defaultTheme.spec_background, 'default': self.defaultTheme.spec_background},
        ]},

        {'name': 'Power Spectrum Settings', 'type': 'group', 'children': [

            {'name': 'FFT size', 'type': 'list', 'default':512, 'values': [('Automatic', 512),("32",32),("64", 64),("128", 128), ("512", 512), ("1024", 1024), ('2048', 2048),('4096', 4096)], 'value': 'Automatic'},
            {'name': 'FFT window', 'type': 'list', 'value':self.widget.specgramSettings.windows[0],'default':self.widget.specgramSettings.windows[0],'values': [('Bartlett',self.widget.specgramSettings.windows[4]),("Blackman", self.widget.specgramSettings.windows[3]),("Hamming", self.widget.specgramSettings.windows[0]), ("Hanning", self.widget.specgramSettings.windows[2]),('Kaiser',self.widget.specgramSettings.windows[5]),('None',self.widget.specgramSettings.windows[6]),("Rectangular", self.widget.specgramSettings.windows[1])]},
            {'name': 'FFT overlap', 'type': 'int', 'value':self.pow_overlap, 'limits' : (-1,100)},
            {'name': 'Grid', 'type': 'group', 'children': [
                {'name': 'X', 'type': 'bool','default': self.defaultTheme.pow_GridX, 'value': self.defaultTheme.pow_GridX},
                {'name': 'Y', 'type': 'bool','default':self.defaultTheme.pow_GridY , 'value': self.defaultTheme.pow_GridY},

             ]},
             {'name': 'Connect Lines', 'type': 'bool','default': self.pow_spec_lines, 'value': self.pow_spec_lines},
             {'name': 'YBounds', 'type': 'group', 'children': [
                {'name': 'MinY', 'type': 'int', 'limits' : (-60,5),'default': -50, 'value': -50},
                {'name': 'MaxY', 'type': 'int', 'limits' : (-60,5),'default': 5 , 'value': 5},


             ]},
             {'name':'Background color', 'type':'color','value':self.defaultTheme.pow_Back, 'default':self.defaultTheme.pow_Back},
             {'name': 'Plot color', 'type': 'color', 'value':self.defaultTheme.pow_Plot, 'default': self.defaultTheme.pow_Plot},
        ]},
        {'name': 'Themes', 'type': 'group', 'children': [
         {'name': 'Theme Selected', 'type': 'list', 'value':"RedBlackTheme.dth",'default':"RedBlackTheme.dth",'values': [("BatsoundLikeTheme","BatsoundLikeTheme.dth"),("PinkBlueTheme","PinkBlueTheme.dth"),("RedBlackTheme","RedBlackTheme.dth"),("WhiteBlueTheme","WhiteBlueTheme.dth")]},
        ]
        } ,
        {'name': 'Detection Settings', 'type': 'group', 'children': [
            {'name': 'Measurement Location', 'type': 'group', 'children': [
            {'name': 'Start', 'type': 'color', 'value': self.defaultTheme.startColor,'default': self.defaultTheme.startColor},
            {'name': 'Quartile25', 'type': 'color', 'value': self.defaultTheme.quart1Color,'default': self.defaultTheme.quart1Color},
            {'name':'Center', 'type':'color','value':self.defaultTheme.centerColor,'default':self.defaultTheme.centerColor},
            {'name': 'Quartile75', 'type': 'color', 'value':self.defaultTheme.quart2Color,'default':self.defaultTheme.quart2Color},
            {'name': 'End', 'type': 'color', 'value':self.defaultTheme.endColor,'default':self.defaultTheme.endColor},
        ]},]}

        ]

        ListParameter.itemClass = DuettoListParameterItem
        self.ParamTree = Parameter.create(name='params', type='group', children=params)
        self.ParamTree.sigTreeStateChanged.connect(self.change)
        self.parameterTree = ParameterTree()
        self.parameterTree.setAutoScroll(True)
        self.parameterTree.setFixedWidth(340)

        self.parameterTree.setHeaderHidden(True)
        self.parameterTree.setParameters(self.ParamTree, showTop=False)

        lay1 = QtGui.QVBoxLayout()
        lay1.setMargin(0)
        lay1.addWidget(self.parameterTree)

        self.hist.setFixedWidth(340)
        self.hist.setFixedHeight(100)
        self.hist.item.setImageItem(self.widget.axesSpecgram.imageItem)
        self.hist.item.gradient.restoreState(self.defaultTheme.colorBarState)
        self.hist.item.region.setRegion(self.defaultTheme.histRange)
        self.hist.item.region.sigRegionChanged.connect(self.updateRegionTheme)

        action = self.hist.item.gradient.hsvAction
        action.triggered.disconnect()
        action.triggered.connect(self.widget.SaveColorBar)
        action.setCheckable(False)
        action.setText("Save")

        lay1.addWidget(self.hist)
        self.osc_settings_contents.setLayout(lay1)
        self.dock_settings.setVisible(False)
        self.dock_settings.setFixedWidth(350)

        self.filesInFolder = []
        self.filesInFolderIndex = -1

        self.widget.axesSpecgram.PointerSpecChanged.connect(self.updateStatusBar)
        self.widget.axesOscilogram.PointerOscChanged.connect(self.updateStatusBar)
        self.widget.rangeFrequencyChanged.connect(self.changeFrequency)
        self.widget.rangeAmplitudeChanged.connect(self.changeAmplitude)
        self.connect(self.widget, SIGNAL("IntervalChanged"), self.updatePowSpecWin)
        self.NFFT_pow = 512

        self.window_pow = self.widget.specgramSettings.windows[0]
        self.window_spec = self.widget.specgramSettings.windows[0]
        self.colorBarsPath = "ColorBars"
        self.pow_spec_windows = []
        self.loadAllColorBars()
        self.setAcceptDrops(True)
        separator = QtGui.QAction(self)
        separator.setSeparator(True)
        separator2 = QtGui.QAction(self)
        separator2.setSeparator(True)
        separator3 = QtGui.QAction(self)
        separator3.setSeparator(True)
        separator4 = QtGui.QAction(self)
        separator4.setSeparator(True)

        self.widget.setStyleSheet(self.styleSheet())
        self.widget.createContextCursor([self.actionCopy,self.actionCut,self.actionPaste,separator,
                                         self.actionNegative_Values,self.actionPositive_Values,self.actionChange_Sign,separator2,
                                         self.action_Reverse,self.actionSilence,self.actionInsert_Silence,separator3,
                                         self.actionZoom_Cursor,self.actionPointer_Cursor,self.actionRectangular_Cursor,self.actionRectangular_Eraser,separator4,
                                         self.actionOsc_Image,self.actionSpecgram_Image,self.actionCombined_Image])

        self.actionSignalName.setText("")
        g = QActionGroup(self)
        g.addAction(self.action1_8x)
        g.addAction(self.action1_4x)
        g.addAction(self.action1_2x)
        g.addAction(self.action1x)
        g.addAction(self.action2x)
        g.addAction(self.action4x)
        g.addAction(self.action8x)
        g.triggered.connect(self.on_g_triggered)

        QTimer.singleShot(0, self.on_load)

    def changeFrequency(self, min, max):
        self.ParamTree.param('Spectrogram Settings').param('Frequency(kHz)').param('Min').setValue(min)
        self.ParamTree.param('Spectrogram Settings').param('Frequency(kHz)').param('Max').setValue(max)

    def changeAmplitude(self, min, max):
        self.ParamTree.param('Oscillogram Settings').param('Amplitude(%)').param('Min').setValue(min)
        self.ParamTree.param('Oscillogram Settings').param('Amplitude(%)').param('Max').setValue(max)

    def folderFiles(self,folder):
        files = []
        for root, dirs, filenames in os.walk(folder):
            for f in filenames:
                files.append(root+"/"+f)   #cambio provisional mientras el sistema no sea multiplataforma
        return files

    def updateStatusBar(self,line):
        self.statusbar.showMessage(line)

    def on_load(self):
        self.widget.visibleOscilogram = True
        self.widget.visibleSpectrogram = True
        self.widget.specgramSettings.NFFT = self.ParamTree.param('Spectrogram Settings').param('FFT size').value()
        self.widget.specgramSettings.overlap = self.ParamTree.param('Spectrogram Settings').param('FFT overlap').value()
        p = os.path.join(os.path.join("Utils","Didactic Signals"),"duetto.wav")
        if os.path.exists(p):
            self.widget.open(p)
            self.widget.visibleSpectrogram = False
            self.actionSignalName.setText(u"File Name: "+ self.widget.signalProcessor.signal.name())
        else:
            self.widget.openNew(44100, 16, 5., whiteNoise=False)
            self.actionSignalName.setText(u"File Name: "+ self.widget.signalProcessor.signal.name())

        self.setWindowTitle("Duetto Sound Lab - Welcome to Duetto")
        self.statusbar.showMessage("Welcome to Duetto Sound Lab.")

    def updateRegionTheme(self):
        reg = self.hist.item.region.getRegion()
        valueMin = self.ParamTree.param('Spectrogram Settings').param('Threshold(dB)').param('Min').value()
        valueMax = self.ParamTree.param('Spectrogram Settings').param('Threshold(dB)').param('Max').value()
        if reg[0] != valueMin:
            self.ParamTree.param('Spectrogram Settings').param('Threshold(dB)').param('Min').setValue(reg[0])
        if reg[1] != valueMax:
            self.ParamTree.param('Spectrogram Settings').param('Threshold(dB)').param('Max').setValue(reg[1])

    def SerializeTheme(self,filename):
        if filename:
            center = self.ParamTree.param('Detection Settings').param('Measurement Location').param('Center').value()
            start = self.ParamTree.param('Detection Settings').param('Measurement Location').param('Start').value()
            quart1 = self.ParamTree.param('Detection Settings').param('Measurement Location').param('Quartile25').value()
            quart2 = self.ParamTree.param('Detection Settings').param('Measurement Location').param('Quartile75').value()
            end = self.ParamTree.param('Detection Settings').param('Measurement Location').param('End').value()
            data = SerializedData(self.widget.osc_background,self.widget.osc_color,self.widget.osc_gridx,
                                  self.widget.osc_gridy,self.pow_spec_backg,self.pow_spec_plotColor,self.pow_spec_gridx,
                                  self.pow_spec_gridy,self.widget.spec_background, self.widget.spec_gridx, self.widget.spec_gridy,
                                  self.hist.item.gradient.saveState(),self.hist.item.region.getRegion(),end,center,start,quart1,quart2)
            file = open(filename,'wb')
            pickle.dump(data,file)
            file.close()

    def DeSerializeTheme(self,filename):
        if filename:
            file = open(filename,'rb')
            data = pickle.load(file)
            file.close()
            return data


    @pyqtSlot()
    def on_actionChangePlayStatus_triggered(self):
        self.widget.changePlayStatus()

    @pyqtSlot()
    def on_actionSave_theme_triggered(self):
        filename = QFileDialog.getSaveFileName(parent=self,caption="Save Theme",directory = os.path.join("Utils","Themes"),filter="Duetto Theme Files (*.dth);;All Files (*)")
        if filename:
            self.SerializeTheme(filename)

    def updateMyTheme(self,data):
        self.widget.spec_background = data.spec_background
        self.widget.osc_background = data.osc_background
        self.widget.osc_color = data.osc_plot
        self.widget.osc_gridx = data.osc_GridX
        self.widget.osc_gridy = data.osc_GridY
        self.widget.spec_gridx = data.spec_GridX
        self.widget.spec_gridy = data.spec_GridY
        self.pow_spec_backg = data.pow_Back
        self.pow_spec_plotColor = data.pow_Plot
        self.pow_spec_gridx = data.pow_GridX
        self.pow_spec_gridy = data.pow_GridY
        self.hist.item.gradient.restoreState(data.colorBarState)
        self.hist.item.region.setRegion(data.histRange)

        self.hist.item.region.lineMoved()
        self.hist.item.region.lineMoveFinished()
        self.ParamTree.param('Oscillogram Settings').param('Grid').param('X').setValue(self.widget.osc_gridx)
        self.ParamTree.param('Oscillogram Settings').param('Grid').param('Y').setValue(self.widget.osc_gridy)
        self.ParamTree.param('Spectrogram Settings').param('Grid').param('X').setValue(self.widget.spec_gridx)
        self.ParamTree.param('Spectrogram Settings').param('Grid').param('Y').setValue(self.widget.spec_gridy)
        self.ParamTree.param('Oscillogram Settings').param('Background color').setValue(self.widget.osc_background)
        self.ParamTree.param('Oscillogram Settings').param('Plot color').setValue(self.widget.osc_color)
        self.ParamTree.param('Spectrogram Settings').param('Background color').setValue(self.widget.spec_background)
        self.ParamTree.param('Spectrogram Settings').param('Threshold(dB)').param('Min').setValue(data.histRange[0])
        self.ParamTree.param('Spectrogram Settings').param('Threshold(dB)').param('Max').setValue(data.histRange[1])
        self.ParamTree.param('Power Spectrum Settings').param('Grid').param('X').setValue(self.pow_spec_gridx)
        self.ParamTree.param('Power Spectrum Settings').param('Grid').param('Y').setValue(self.pow_spec_gridy)
        self.ParamTree.param('Power Spectrum Settings').param('Background color').setValue(data.pow_Back)
        self.ParamTree.param('Power Spectrum Settings').param('Plot color').setValue(self.pow_spec_plotColor)
        self.ParamTree.param('Detection Settings').param('Measurement Location').param('Center').setValue(data.centerColor)
        self.ParamTree.param('Detection Settings').param('Measurement Location').param('Start').setValue(data.startColor)
        self.ParamTree.param('Detection Settings').param('Measurement Location').param('Quartile25').setValue(data.quart1Color)
        self.ParamTree.param('Detection Settings').param('Measurement Location').param('Quartile75').setValue(data.quart2Color)

    @pyqtSlot()
    def on_actionLoad_Theme_triggered(self):
        filename = QFileDialog.getOpenFileName(parent=self,directory = os.path.join("Utils","Themes"), caption="Load Theme",filter="Duetto Theme Files (*.dth);;All Files (*)")
        data = self.DeSerializeTheme(filename)
        self.updateMyTheme(data)

    #region Drag and Drop file

    def dragEnterEvent(self, event):
        event.acceptProposedAction()
        self.dropchanged.emit(event.mimeData())

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        mimeData = event.mimeData()
        if len(mimeData.urls())>1:return
        mimeUrl = "".join([str(url.path()) for url in mimeData.urls()])

        self.widget.visibleOscilogram = True
        self.widget.visibleSpectrogram = True
        path = mimeUrl[1:len(mimeUrl)]
        path_base = os.path.split(path)[0]
        self.filesInFolder = self.folderFiles(path_base)
        self.filesInFolderIndex = self.filesInFolder.index(path)
        self._open(path)
        event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        event.accept()


    #endregion

    def change(self, param, changes):
        #print("tree changes:")
        #pow = False

        for param, change, data in changes:
            path = self.ParamTree.childPath(param)
            if path is not None:
                childName = '.'.join(path)
            else:
                childName = param.name()

            if childName == 'Spectrogram Settings.FFT size':
                self.widget.specgramSettings.NFFT = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=True, updateOscillogram=False, updateSpectrogram=True)

            elif childName == 'Spectrogram Settings.Grid.X':
                self.widget.spec_gridx = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=True, updateOscillogram=False, updateSpectrogram=False)

            elif childName == 'Spectrogram Settings.Grid.Y':
                self.widget.spec_gridy = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=True, updateOscillogram=False, updateSpectrogram=False)

            elif childName == 'Spectrogram Settings.Threshold(dB).Min':
                if self.hist.item.region.getRegion()[0] != data:
                    if data > self.ParamTree.param('Spectrogram Settings').param('Threshold(dB)').param('Max').value():
                        self.ParamTree.param('Spectrogram Settings').param('Threshold(dB)').param('Min').setToDefault()
                        self.ParamTree.param('Spectrogram Settings').param('Threshold(dB)').param('Min').show()
                        return
                    self.hist.item.region.setRegion([data,self.hist.item.region.getRegion()[1]])
                    self.hist.item.region.lineMoved()
                    self.hist.item.region.lineMoveFinished()

            elif childName == 'Spectrogram Settings.Threshold(db%).Max':
                if self.hist.item.region.getRegion()[1] != data:
                    if data < self.ParamTree.param('Spectrogram Settings').param('Threshold(dB)').param('Min').value():
                        self.ParamTree.param('Spectrogram Settings').param('Threshold(dB)').param('Max').setToDefault()
                        self.ParamTree.param('Spectrogram Settings').param('Threshold(dB)').param('Max').setValue()
                        return
                    self.hist.item.region.setRegion([self.hist.item.region.getRegion()[0],data])
                    self.hist.item.region.lineMoved()
                    self.hist.item.region.lineMoveFinished()

            elif childName == 'Spectrogram Settings.FFT window':
                self.widget.specgramSettings.window = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=True, updateOscillogram=False, updateSpectrogram=True)

            elif childName == 'Spectrogram Settings.Background color':
                self.widget.spec_background = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=False,updateOscillogram=False,updateSpectrogram=True)

            elif childName == 'Spectrogram Settings.ColorMap':
                self.widget.axesSpecgram.getHistogramWidget().item._pixelVectorCache.append(data)

            elif childName == 'Spectrogram Settings.Frequency(kHz).Min':
                self.widget.minYSpc = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=True, updateOscillogram=False, updateSpectrogram=True)

            elif childName == 'Spectrogram Settings.Frequency(kHz).Max':
                self.widget.maxYSpc = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=True, updateOscillogram=False, updateSpectrogram=True)

            elif childName == 'Spectrogram Settings.FFT overlap':
                self.widget.specgramSettings.overlap = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=True, updateOscillogram=False, updateSpectrogram=True)

            elif childName == 'Power Spectrum Settings.FFT size':
                self.NFFT_pow = data

            elif childName == 'Power Spectrum Settings.FFT window':
                self.window_pow = data
            elif childName == 'Power Spectrum Settings.FFT overlap':
                self.pow_overlap = data

            elif childName == 'Power Spectrum Settings.Background color':
                self.pow_spec_backg = data

            elif childName == 'Power Spectrum Settings.Plot color':
                self.pow_spec_plotColor = data

            elif childName == 'Power Spectrum Settings.Grid.X':
                self.pow_spec_gridx = data

            elif childName == 'Power Spectrum Settings.Grid.Y':
                self.pow_spec_gridy = data

            elif childName == 'Oscillogram Settings.Background color':
                self.widget.osc_background = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=False, updateOscillogram=True, updateSpectrogram=False)
            elif childName == 'Oscillogram Settings.Grid.X':
                self.widget.osc_gridx = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=True, updateOscillogram=False, updateSpectrogram=False)
            elif childName == 'Oscillogram Settings.Grid.Y':
                self.widget.osc_gridy = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=True, updateOscillogram=False, updateSpectrogram=False)
            elif childName == 'Oscillogram Settings.Plot color':
                self.widget.osc_color = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=True, updateOscillogram=True, updateSpectrogram=False)
            elif childName == 'Oscillogram Settings.Amplitude(%).Min':
                self.widget.minYOsc = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=True, updateOscillogram=True, updateSpectrogram=False)
            elif childName == 'Oscillogram Settings.Amplitude(%).Max':
                self.widget.maxYOsc = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=True, updateOscillogram=True, updateSpectrogram=False)
            elif childName == 'Oscillogram Settings.Connect Lines':
                self.widget.lines = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=True, updateOscillogram=True, updateSpectrogram=False)
            elif childName == 'Oscillogram Settings.Connect Lines':
                self.pow_spec_lines = data
                self.widget.lines = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=True, updateOscillogram=True, updateSpectrogram=False)

            elif childName == 'Themes.Theme Selected':
                p = os.path.join(os.path.join("Utils","Themes"),data)
                theme = self.DeSerializeTheme(p)
                self.updateMyTheme(theme)
            elif childName == 'Power Spectrum Settings.YBounds.MaxY':
                self.pow_spec_maxY = data
            elif childName == 'Power Spectrum Settings.YBounds.MinY':
                self.pow_spec_minY = data
            elif childName == 'Power Spectrum Settings.Connect Lines':
                self.pow_spec_lines = data
            #print('  parameter: %s' % childName)
            #print('  change:    %s' % change)
            #print('  data:      %s' % str(data))
            #print('  ----------')

    @pyqtSlot()
    def on_actionSegmentation_And_Clasification_triggered(self):
        center = self.ParamTree.param('Detection Settings').param('Measurement Location').param('Center').value()
        start = self.ParamTree.param('Detection Settings').param('Measurement Location').param('Start').value()
        quart1 = self.ParamTree.param('Detection Settings').param('Measurement Location').param('Quartile25').value()
        quart2 = self.ParamTree.param('Detection Settings').param('Measurement Location').param('Quartile75').value()
        end = self.ParamTree.param('Detection Settings').param('Measurement Location').param('End').value()
        signal = WavFileSignal(self.widget.signalProcessor.signal.path)
        f,t = self.widget.getIndexFromAndTo()

        if t > f:
            signal.data = self.widget.signalProcessor.signal.data[f:t]

        segWindow = SegmentationAndClasificationWindow(parent=self, signal=signal)
        if not segWindow.rejectSignal:
            segWindow.widget.maxYOsc =  self.ParamTree.param('Oscillogram Settings').param('Amplitude(%)').param('Max').value()
            segWindow.widget.minYOsc = self.ParamTree.param('Oscillogram Settings').param('Amplitude(%)').param('Min').value()
            segWindow.widget.minYSpc = self.ParamTree.param('Spectrogram Settings').param('Frequency(kHz)').param('Min').value()
            segWindow.widget.maxYSpc = self.ParamTree.param('Spectrogram Settings').param('Frequency(kHz)').param('Max').value()

            segWindow.load_Theme(SerializedData(self.widget.osc_background,self.widget.osc_color,self.widget.osc_gridx,
                                  self.widget.osc_gridy, self.pow_spec_backg,self.pow_spec_plotColor,self.pow_spec_gridx,
                                  self.pow_spec_gridy, self.widget.spec_background, self.widget.spec_gridx, self.widget.spec_gridy,
                                  self.hist.item.gradient.saveState(),self.hist.item.region.getRegion(),end,center,start,quart1,quart2))

        self.widget.undoRedoManager.clearActions()


    @pyqtSlot()
    def on_actionZoom_Cursor_triggered(self):
        if self.actionZoom_Cursor.isChecked():
            self.actionPointer_Cursor.setChecked(False)
            self.actionRectangular_Cursor.setChecked(False)
            self.actionRectangular_Eraser.setChecked(False)
            self.widget.setSelectedTool(Tools.Zoom)
        else:
            self.actionZoom_Cursor.setChecked(True)

    @pyqtSlot()
    def on_actionRectangular_Cursor_triggered(self):
        if self.actionRectangular_Cursor.isChecked():
            self.actionPointer_Cursor.setChecked(False)
            self.actionZoom_Cursor.setChecked(False)
            self.actionRectangular_Eraser.setChecked(False)
            self.widget.setSelectedTool(Tools.RectangularCursor)
        else:
            self.actionRectangular_Cursor.setChecked(True)

    @pyqtSlot()
    def on_actionRectangular_Eraser_triggered(self):
        if self.actionRectangular_Eraser.isChecked():
            self.actionZoom_Cursor.setChecked(False)
            self.actionPointer_Cursor.setChecked(False)
            self.actionRectangular_Cursor.setChecked(False)
            self.widget.setSelectedTool(Tools.RectangularEraser)
        else:
            self.actionRectangular_Eraser.setChecked(True)

    @pyqtSlot()
    def on_actionPointer_Cursor_triggered(self):
        if self.actionPointer_Cursor.isChecked():
            self.actionZoom_Cursor.setChecked(False)
            self.actionRectangular_Cursor.setChecked(False)
            self.actionRectangular_Eraser.setChecked(False)
            self.widget.setSelectedTool(Tools.PointerCursor)
        else:
            self.actionPointer_Cursor.setChecked(True)

    @pyqtSlot()
    def on_actionResampling_triggered(self):
        resamplingDialog = sdialog.Ui_Dialog()
        resamplingDialogWindow = InsertSilenceDialog(self)
        resamplingDialog.setupUi(resamplingDialogWindow)
        resamplingDialog.label.setText("Select the new Sampling Rate.")
        resamplingDialog.insertSpinBox.setValue(self.widget.signalProcessor.signal.samplingRate)
        if resamplingDialogWindow.exec_():
            val = resamplingDialog.insertSpinBox.value()
            if val > MIN_SAMPLING_RATE and val < MAX_SAMPLING_RATE:
                self.widget.undoRedoManager.addAction(ResamplingAction(self.widget.signalProcessor.signal,val))
                self.widget.resampling(val)
            else:
                if val < MIN_SAMPLING_RATE:
                    QMessageBox.warning(QMessageBox(), "Error",
                                        "Sampling rate should be greater than " + str(MIN_SAMPLING_RATE))
                elif val > MAX_SAMPLING_RATE:
                    QMessageBox.warning(QMessageBox(), "Error",
                                        "Sampling rate should be less than " + str(MAX_SAMPLING_RATE))

    @pyqtSlot()
    def on_actionCut_triggered(self):
        start, end = self.widget.getIndexFromAndTo()
        self.widget.undoRedoManager.addAction(CutAction(self.widget.signalProcessor.signal,start,end))
        self.widget.cut()

    @pyqtSlot()
    def on_actionPositive_Values_triggered(self):
        start, end = self.widget.getIndexFromAndTo()
        self.widget.undoRedoManager.addAction(Absolute_ValuesAction(self.widget.signalProcessor.signal,start,end,1))
        self.widget.absoluteValue(1)
        self.hist.item.region.lineMoved()
        self.hist.item.region.lineMoveFinished()

    @pyqtSlot()
    def on_actionChange_Sign_triggered(self):
        start, end = self.widget.getIndexFromAndTo()
        self.widget.undoRedoManager.addAction(ChangeSignAction(self.widget.signalProcessor.signal,start,end))
        self.widget.changeSign()
        self.hist.item.region.lineMoved()
        self.hist.item.region.lineMoveFinished()

    @pyqtSlot()
    def on_actionNegative_Values_triggered(self):
        start, end = self.widget.getIndexFromAndTo()
        self.widget.undoRedoManager.addAction(Absolute_ValuesAction(self.widget.signalProcessor.signal,start,end,-1))
        self.widget.absoluteValue(-1)
        self.hist.item.region.lineMoved()
        self.hist.item.region.lineMoveFinished()

    @pyqtSlot()
    def on_actionCopy_triggered(self):
        self.widget.copy()

    @pyqtSlot()
    def on_actionPaste_triggered(self):
        start, _ = self.widget.getIndexFromAndTo()
        self.widget.undoRedoManager.addAction(PasteAction(self.widget.signalProcessor.signal,start,self.widget.editionSignalProcessor.clipboard))
        self.widget.paste()

    @pyqtSlot()
    def on_actionUndo_triggered(self):
        self.widget.undo()

    @pyqtSlot()
    def on_actionRedo_triggered(self):
        self.widget.redo()

    @pyqtSlot()
    def on_actionSmart_Scale_triggered(self):
        scaleDialog = cvdialog.Ui_Dialog()
        scaleDialogWindow = ChangeVolumeDialog(self)
        scaleDialog.setupUi(scaleDialogWindow)
        if scaleDialogWindow.exec_():
            fade = ""
            factor = scaleDialog.spinboxConstValue.value()
            if scaleDialog.rbuttonConst.isChecked():
                function = "const"
            elif scaleDialog.rbuttonNormalize.isChecked():
                function = "normalize"
                factor = scaleDialog.spinboxNormalizePercent.value()
            else:
                function = scaleDialog.cboxModulationType.currentText()
                fade = "IN" if scaleDialog.rbuttonFadeIn.isChecked() else ("OUT" if scaleDialog.rbuttonFadeOut.isChecked() else "")
                if fade == "":
                    return
            start,end = self.widget.getIndexFromAndTo()
            self.widget.undoRedoManager.addAction(ScaleAction(self.widget.signalProcessor.signal,start,end,factor, function, fade))
            self.widget.scale(factor, function, fade)

    @pyqtSlot()
    def on_actionInsert_Silence_triggered(self):
        silenceDialog = sdialog.Ui_Dialog()
        silenceDialogWindow = InsertSilenceDialog(self)
        silenceDialog.setupUi(silenceDialogWindow)
        if silenceDialogWindow.exec_():
            start,end = self.widget.getIndexFromAndTo()
            ms = silenceDialog.insertSpinBox.value()
            self.widget.undoRedoManager.addAction(InsertSilenceAction(self.widget.signalProcessor.signal,start,ms))
            self.widget.insertSilence(ms)

    @pyqtSlot()
    def on_actionGenerate_Pink_Noise_triggered(self):
        whiteNoiseDialog = sdialog.Ui_Dialog()
        whiteNoiseDialogWindow = InsertSilenceDialog(self)
        whiteNoiseDialog.setupUi(whiteNoiseDialogWindow)
        whiteNoiseDialog.label.setText("Select the duration in ms \n of the Pink Noise.")
        whiteNoiseDialog.insertSpinBox.setValue(1000)
        if whiteNoiseDialogWindow.exec_():
            type_, Fc, Fl, Fu = self.filter_helper()
            if type_ != None:
                ms = whiteNoiseDialog.insertSpinBox.value()
                start, _ = self.widget.getIndexFromAndTo()
                self.widget.undoRedoManager.addAction(GeneratePinkNoiseAction(self.widget.signalProcessor.signal,start,ms, type_, Fc, Fl, Fu))
                self.widget.insertPinkNoise(ms, type_, Fc, Fl, Fu)

    @pyqtSlot()
    def on_actionGenerate_White_Noise_triggered(self):
        whiteNoiseDialog = sdialog.Ui_Dialog()
        whiteNoiseDialogWindow = InsertSilenceDialog(self)
        whiteNoiseDialog.setupUi(whiteNoiseDialogWindow)
        whiteNoiseDialog.label.setText("Select the duration in ms \n of the white noise.")
        whiteNoiseDialog.insertSpinBox.setValue(1000)
        if whiteNoiseDialogWindow.exec_():
            ms = whiteNoiseDialog.insertSpinBox.value()
            start,end = self.widget.getIndexFromAndTo()
            self.widget.undoRedoManager.addAction(GenerateWhiteNoiseAction(self.widget.signalProcessor.signal,start,ms))
            self.widget.insertWhiteNoise(ms)

    def filter_helper(self):
        filterDialog = filterdg.Ui_Dialog()
        filterDialogWindow = InsertSilenceDialog(self)
        filterDialog.setupUi(filterDialogWindow)
        if filterDialogWindow.exec_():
            type_ = None
            Fc, Fl, Fu = 0, 0, 0
            if filterDialog.rButtonLowPass.isChecked():
                type_ = FILTER_TYPE().LOW_PASS
                Fc = filterDialog.spinBoxLowPass.value()
            elif filterDialog.rButtonHighPass.isChecked():
                type_ = FILTER_TYPE().HIGH_PASS
                Fc = filterDialog.spinBoxHighPass.value()

            elif filterDialog.rButtonBandPass.isChecked():
                type_ = FILTER_TYPE().BAND_PASS
                Fl = filterDialog.spinBoxBandPassFl.value()
                Fu = filterDialog.spinBoxBandPassFu.value()
            elif filterDialog.rButtonBandStop.isChecked():
                type_ = FILTER_TYPE().BAND_STOP
                Fl = filterDialog.spinBoxBandStopFl.value()
                Fu = filterDialog.spinBoxBandStopFu.value()
        return type_, Fc, Fl, Fu

    @pyqtSlot()
    def on_actionFilter_triggered(self):
        type_, Fc, Fl, Fu = self.filter_helper()
        if type_ is not None:
            start,end = self.widget.getIndexFromAndTo()
            self.widget.undoRedoManager.addAction(FilterAction(self.widget.signalProcessor.signal,start,end,type_, Fc, Fl, Fu))
            self.widget.filter(type_, Fc, Fl, Fu)

    @pyqtSlot()
    def on_actionSilence_triggered(self):
        start,end = self.widget.getIndexFromAndTo()
        self.widget.undoRedoManager.addAction(SilenceAction(self.widget.signalProcessor.signal,start,end))
        self.widget.silence()

    @pyqtSlot()
    def on_actionNormalize_triggered(self):
        self.widget.undoRedoManager.addAction(UndoRedoAction(self.widget.normalizeUndoAction,self.widget.normalize))
        self.widget.normalize()

    @pyqtSlot()
    def on_actionFull_Screen_triggered(self):
        if self.actionFull_Screen.isChecked():
            self.showFullScreen()
        else:
            self.showNormal()

    @pyqtSlot()
    def on_action_Reverse_triggered(self):
        start,end = self.widget.getIndexFromAndTo()
        self.widget.undoRedoManager.addAction(ReverseAction(self.widget.signalProcessor.signal,start,end))
        self.widget.reverse()

    def updatePowSpecWin(self):
        for win in self.pow_spec_windows:
            minx = self.widget.zoomCursor.min
            maxx = max(self.widget.zoomCursor.max,
                       min(minx + self.NFFT_pow, len(self.widget.signalProcessor.signal.data)))
            win.updatePowSpectrumInterval(self.widget.signalProcessor.signal.data[minx:maxx])

    @pyqtSlot()
    def on_actionZoomIn_triggered(self):
        self.widget.zoomIn()

    @pyqtSlot()
    def on_actionZoom_out_triggered(self):
        self.widget.zoomOut()

    @pyqtSlot()
    def on_actionZoom_out_entire_file_triggered(self):
        self.widget.zoomNone()

    @pyqtSlot()
    def on_actionSettings_triggered(self):
        if self.dock_settings.isVisible():
            self.dock_settings.setVisible(False)
        else:
            self.dock_settings.setVisible(True)
            self.dock_settings.setFloating(False)

    @pyqtSlot()
    def on_actionPower_Spectrum_triggered(self):
        dg_pow_spec = PowerSpectrumWindow(self,self.pow_spec_plotColor, self.pow_spec_backg, self.pow_spec_gridx, self.pow_spec_gridy,self.pow_spec_minY,self.pow_spec_maxY,self.pow_spec_lines)

        minx = self.widget.zoomCursor.min
        maxx = max(self.widget.zoomCursor.max, min(minx + self.NFFT_pow, len(self.widget.signalProcessor.signal.data)))
        dg_pow_spec.plot(self.widget.signalProcessor.signal.data[minx:maxx],
                         self.widget.signalProcessor.signal.samplingRate, self.NFFT_pow, self.window_pow, self.pow_overlap)

        self.pow_spec_windows.append(dg_pow_spec)

    @pyqtSlot()
    def on_actionSelect_all_triggered(self):
        self.widget.updateSpanSelector()

    @pyqtSlot()
    def on_actionSpectogram_Settings_triggered(self):
        self.dock_spec_settings.setVisible(True)
        self.dock_spec_settings.setFloating(False)


    @pyqtSlot()
    def on_actionExit_triggered(self):
        self.close()

    def closeEvent(self,event):
        self._save(event)
        self.close()

    def _save(self,event = None):
        mbox = QtGui.QMessageBox(QtGui.QMessageBox.Question,"Save","Do you want to save the signal?",QtGui.QMessageBox.Yes | QtGui.QMessageBox.No|QtGui.QMessageBox.Cancel,self)
        result = mbox.exec_()
        if self.widget.undoRedoManager.count() > 0 and  result == QtGui.QMessageBox.Yes:
            self.on_actionSave_triggered()
        elif result == QtGui.QMessageBox.Cancel and event is not None:
            event.ignore()




    @pyqtSlot()
    def on_actionNew_triggered(self):
        nfd = NewFileDialog(parent=self)
        if nfd.exec_():
            self.widget.specgramSettings.NFFT = self.ParamTree.param('Spectrogram Settings').param('FFT size').value()
            self.widget.specgramSettings.overlap = self.ParamTree.param('Spectrogram Settings').param('FFT overlap').value()
            self.widget.openNew(nfd.SamplingRate, nfd.BitDepth, nfd.Duration, nfd.WhiteNoise)
            self.setWindowTitle("Duetto Sound Lab - (new)")

    @pyqtSlot()
    def on_actionOpen_triggered(self):
        f = QFileDialog.getOpenFileName(self, "Select a file to open",directory = self.lastopen,
                                              filter="Wave Files (*.wav);;All Files (*)")
        self._open(f)

    @pyqtSlot()
    def on_actionClose_triggered(self):
        self._save()
        self.on_load()

    def _open(self,f=''):
        if f != '':
            try:
                self.lastopen = f
                self.widget.specgramSettings.NFFT = self.ParamTree.param('Spectrogram Settings').param('FFT size').value()
                self.widget.specgramSettings.overlap = self.ParamTree.param('Spectrogram Settings').param('FFT overlap').value()
                path_base = os.path.split(unicode(f))[0]
                self.filesInFolder = self.folderFiles(path_base)
                self.filesInFolderIndex = self.filesInFolder.index(str(f))
                self.widget.visibleSpectrogram = True # for restore the state lose in load

                self.widget.open(f)
                self.setWindowTitle("Duetto Sound Lab - " + self.widget.signalProcessor.signal.name())
                self.actionSignalName.setText(u"File Name: "+self.widget.signalProcessor.signal.name())
            except:
                QMessageBox.warning(QMessageBox(), "Error", "Could not load the file.\n"+f)
                self.widget.openNew(44100,16,1)



            valuemin = self.widget.minYSpc
            valuemax = self.widget.maxYSpc
            #print((valuemax,valuemin))
            self.ParamTree.param('Spectrogram Settings').param('Frequency(kHz)').param('Min').setValue(valuemin)
            self.ParamTree.param('Spectrogram Settings').param('Frequency(kHz)').param('Min').setDefault(valuemin)
            self.ParamTree.param('Spectrogram Settings').param('Frequency(kHz)').param('Max').setValue(valuemax)
            self.ParamTree.param('Spectrogram Settings').param('Frequency(kHz)').param('Max').setDefault(valuemax)
            self.actionPointer_Cursor.setChecked(False)
            self.actionRectangular_Cursor.setChecked(False)
            self.actionZoom_Cursor.setChecked(True)
            self.actionRectangular_Eraser.setChecked(False)

    @pyqtSlot()
    def on_actionFile_Up_triggered(self):
        if self.filesInFolderIndex < len(self.filesInFolder)-1:
            self.filesInFolderIndex += 1
            if os.path.exists(self.filesInFolder[self.filesInFolderIndex]):
                self._open(self.filesInFolder[self.filesInFolderIndex])


    @pyqtSlot()
    def on_actionFile_Down_triggered(self):
        if self.filesInFolderIndex > 0:
            self.filesInFolderIndex -= 1
            if os.path.exists(self.filesInFolder[self.filesInFolderIndex]):
                self._open(self.filesInFolder[self.filesInFolderIndex])


    @pyqtSlot()
    def on_actionSave_triggered(self):
        fname = unicode(QFileDialog.getSaveFileName(self,"Save signal",self.widget.signalProcessor.signal.name(),"*.wav"))
        if fname:
            self.widget.save(fname)

    @pyqtSlot()
    def on_actionSave_selected_interval_as_triggered(self):
        fname = unicode(QFileDialog.getSaveFileName(self,"Save signal","Selection-"+self.widget.signalProcessor.signal.name(),"*.wav"))
        if fname:
            self.widget.saveSelected(fname)

    @pyqtSlot()
    def on_actionPlay_Sound_triggered(self):
        self.widget.play()


    @pyqtSlot()
    def on_actionStop_Sound_triggered(self):
        self.widget.stop()
        self.hist.item.region.lineMoved()
        self.hist.item.region.lineMoveFinished()

    @pyqtSlot()
    def on_actionRecord_triggered(self):
        self.widget.record()

    @pyqtSlot()
    def on_actionPause_Sound_triggered(self):
        self.widget.pause()

    @pyqtSlot()
    def on_actionCombined_triggered(self):
        self.widget.visibleOscilogram=True
        self.widget.visibleSpectrogram=True
        self.widget.refresh()
        self.hist.item.region.lineMoved()
        self.hist.item.region.lineMoveFinished()

    @pyqtSlot()
    def on_actionSpectogram_triggered(self):
        self.widget.visibleOscilogram=False
        self.widget.visibleSpectrogram=True
        self.widget.refresh(updateOscillogram=False)
        self.hist.item.region.lineMoved()
        self.hist.item.region.lineMoveFinished()

    @pyqtSlot()
    def on_actionOscilogram_triggered(self):
        self.widget.visibleOscilogram=True
        self.widget.visibleSpectrogram=False
        self.widget.refresh(updateSpectrogram=False)

    @pyqtSlot()
    def on_actionOsc_Image_triggered(self):
        if self.widget.visibleOscilogram:
            self.saveImage(self.widget.axesOscilogram,"oscilogram")
        else:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), "Error", "The Oscilogram plot widget is not visible.\n You should see the data that you are going to save.")

    @pyqtSlot()
    def on_actionCombined_Image_triggered(self):
        if self.widget.visibleOscilogram and self.widget.visibleSpectrogram:
            self.saveImage(self.widget,"graph")
        else:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), "Error", "One of the plot widgets is not visible.\n You should see the data that you are going to save.")

    @pyqtSlot()
    def on_actionFull_Screen_triggered(self):
        if self.actionFull_Screen.isChecked():
            self.showFullScreen()
        else:
            self.showNormal()

    @pyqtSlot()
    def on_actionSpecgram_Image_triggered(self):
        if self.widget.visibleSpectrogram:
            self.saveImage(self.widget.axesSpecgram,"specgram")
        else:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), "Error", "The Espectrogram plot widget is not visible.\n You should see the data that you are going to save.")

    def saveImage(self,widget,text=""):
        fname = unicode(QFileDialog.getSaveFileName(self,"Save "+ text +" as an Image ",str(self.widget.signalProcessor.signal.name())+"-"+text+"-Duetto-Image","*.jpg"))
        if fname:
            #save as image
            image = QtGui.QPixmap.grabWindow(widget.winId())
            image.save(fname, 'jpg')

    @pyqtSlot()
    def on_actionSaveColorBar_triggered(self):
        state = self.widget.axesSpecgram.getHistogramWidget().item.gradient.saveState()
        path = QtGui.QFileDialog.getSaveFileName(self, "Save Color Bar", filter="Bar Files (*.bar);;All Files (*)")
        if path != "":
            fh = open(path, 'w')
            fh.write(state.__repr__())
            fh.close()

    @pyqtSlot()
    def on_actionLoadColorBar_triggered(self):
        path = QtGui.QFileDialog.getOpenFileName(self, "Load Color Bar", filter="Bar Files (*.bar);;All Files (*)")
        if path != "":
            fh = open(path, 'r')
            state = eval(fh.readline())
            self.widget.axesSpecgram.getHistogramWidget().item.gradient.restoreState(state)

    @QtCore.pyqtSlot(int, int, int)
    def on_widget_rangeChanged(self, left, right, total):
        self.horizontalScrollBar.blockSignals(True)
        self.horizontalScrollBar.setValue(0)
        self.horizontalScrollBar.setMinimum(0)
        self.horizontalScrollBar.setMaximum(total - (right - left))
        self.horizontalScrollBar.setValue(left)
        self.horizontalScrollBar.setPageStep(right - left)
        self.horizontalScrollBar.setSingleStep((right - left) / 8)
        self.horizontalScrollBar.blockSignals(True)
        self.horizontalScrollBar.blockSignals(False)

    @QtCore.pyqtSlot(int)
    def on_horizontalScrollBar_valueChanged(self, value):
        self.widget.changeRange(value, value + self.horizontalScrollBar.pageStep(), emit=False)

    @pyqtSlot(QAction)
    def on_g_triggered(self, action):
        self.widget.stop()
        self.widget.playerSpeed = {'1/8x': 12.5, '1/4x': 25, '1/2x': 50,
                                   '1x': 100, '2x': 200, '4x': 400, '8x': 800}[str(action.text())]

    def loadAllColorBars(self):
        if os.path.exists(self.colorBarsPath):
            for i in os.listdir(self.colorBarsPath):
                if os.path.isfile(self.colorBarsPath+'\\'+ i):
                    print(i)
