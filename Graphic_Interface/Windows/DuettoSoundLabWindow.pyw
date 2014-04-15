import sys
from apptools.undo.action.undo_action import UndoAction
from pyqtgraph.Qt import QtCore, QtGui
import numpy
import os
import pyqtgraph
import pyqtgraph.widgets.HistogramLUTWidget
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
from PyQt4.QtGui import QDialog, QMessageBox, QFileDialog, QActionGroup, QAction
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL, pyqtSlot, QTimer
from Graphic_Interface.Dialogs.NewFileDialog import NewFileDialog
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

MIN_SAMPLING_RATE = 1000
MAX_SAMPLING_RATE = 2000000


class InsertSilenceDialog(sdialog.Ui_Dialog, QDialog):
    pass


class ChangeVolumeDialog(cvdialog.Ui_Dialog, QDialog):
    pass


class FilterDialog(filterdg.Ui_Dialog, QDialog):
    pass

class DuettoSoundLabWindow(QtGui.QMainWindow, Ui_DuettoMainWindow):
    dropchanged = QtCore.pyqtSignal(QtCore.QMimeData)
    def __init__(self, parent=None):
        super(DuettoSoundLabWindow, self).__init__(parent)
        self.setupUi(self)


        self.hist = DuettoHorizontalHistogramWidget()
        self.widget.histogram = self.hist
        self.pow_overlap = 90
        self.Theme = 'Utils\\Themes\\RedBlackTheme.dth'
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
        self.statusbar = self.statusBar()
        self.statusbar.setSizeGripEnabled(False)
        self.widget.statusbar = self.statusbar
        self.statusbar.showMessage("Welcome to Duetto Sound Lab", 5000)
        params = [
        {'name': 'Oscillogram Settings', 'type': 'group', 'children': [
            {'name': 'Amplitude', 'type': 'group', 'children': [
                 {'name': 'Min', 'type': 'float', 'value': -100, 'step': 0.1},
                 {'name': 'Max', 'type': 'float', 'value': 100, 'step': 0.1},
            ]},

            {'name': 'Grid', 'type': 'group', 'children': [
                {'name': 'X', 'type': 'bool','default': self.defaultTheme.osc_GridX, 'value': self.defaultTheme.osc_GridX},
                {'name': 'Y', 'type': 'bool','default':self.defaultTheme.osc_GridY , 'value': self.defaultTheme.osc_GridY},

            ]},
            {'name':'Background color', 'type':'color','value':self.defaultTheme.osc_background, 'default':self.defaultTheme.osc_background},
            {'name': 'Plot color', 'type': 'color', 'value':self.defaultTheme.osc_plot, 'default': self.defaultTheme.osc_plot},
        ]},

        {'name': 'Spectrogram Settings', 'type': 'group', 'children': [
            {'name': 'Frequency', 'type': 'group', 'children': [
                {'name': 'Min', 'type': 'float', 'value': 0, 'step': 0.1},
                {'name': 'Max', 'type': 'float', 'value': 22, 'step': 0.1},
            ]},
            {'name': 'FFT size', 'type': 'list', 'default':512, 'values': {'256': 256, '512': 512, '1024': 1024, '2048': 2048, 'Automatic': 512}, 'value':'Automatic' },
            {'name': 'FFT window', 'type': 'list', 'value':self.widget.specgramSettings.windows[0],'default':self.widget.specgramSettings.windows[0],'values': {"blackman": self.widget.specgramSettings.windows[3],"rectangular": self.widget.specgramSettings.windows[1], "Hanning": self.widget.specgramSettings.windows[2], "Hamming": self.widget.specgramSettings.windows[0],'bartlett':self.widget.specgramSettings.windows[4],'kaiser':self.widget.specgramSettings.windows[5],'None':self.widget.specgramSettings.windows[6]}},
            {'name': 'FFT overlap', 'type': 'int', 'value':-1, 'limits': (-1, 99)},
            {'name': 'Threshold', 'type': 'group', 'children': [
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

             {'name': 'FFT size', 'type': 'list','default':512, 'values': {"256": 256, "512": 512, "1024": 1024, '2048': 2048, 'Automatic': 512}, 'value': 2},
             {'name': 'FFT window', 'type': 'list', 'value':self.widget.specgramSettings.windows[0],'default':self.widget.specgramSettings.windows[0],'values': {"blackman": self.widget.specgramSettings.windows[3],"rectangular": self.widget.specgramSettings.windows[1], "Hanning": self.widget.specgramSettings.windows[2], "Hamming": self.widget.specgramSettings.windows[0],'bartlett':self.widget.specgramSettings.windows[4],'kaiser':self.widget.specgramSettings.windows[5],'None':self.widget.specgramSettings.windows[6]}},
             {'name': 'FFT overlap', 'type': 'int', 'value':self.pow_overlap, 'limits' : (-1,100)},
             {'name': 'Grid', 'type': 'group', 'children': [
                {'name': 'X', 'type': 'bool','default': self.defaultTheme.pow_GridX, 'value': self.defaultTheme.pow_GridX},
                {'name': 'Y', 'type': 'bool','default':self.defaultTheme.pow_GridY , 'value': self.defaultTheme.pow_GridY},

             ]},
             {'name':'Background color', 'type':'color','value':self.defaultTheme.pow_Back, 'default':self.defaultTheme.pow_Back},
             {'name': 'Plot color', 'type': 'color', 'value':self.defaultTheme.pow_Plot, 'default': self.defaultTheme.pow_Plot},
        ]},
        {'name': 'Detection Settings', 'type': 'group', 'children': [
            {'name': 'Measurement Location', 'type': 'group', 'children': [
            {'name': 'Start', 'type': 'color', 'value': self.defaultTheme.startColor,'default': self.defaultTheme.startColor},
            {'name': 'Quartile25', 'type': 'color', 'value': self.defaultTheme.quart1Color,'default': self.defaultTheme.quart1Color},
            {'name':'Center', 'type':'color','value':self.defaultTheme.centerColor,'default':self.defaultTheme.centerColor},
            {'name': 'Quartile75', 'type': 'color', 'value':self.defaultTheme.quart2Color,'default':self.defaultTheme.quart2Color},
            {'name': 'End', 'type': 'color', 'value':self.defaultTheme.endColor,'default':self.defaultTheme.endColor},
        ]},]}

        ]
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
        self.widget.createContextCursor([self.actionCopy,self.actionCut,self.actionPaste,separator,
                                         self.actionPlay_Sound,self.actionPause_Sound,self.actionStop_Sound,self.actionRecord,separator2,
                                         self.action_Reverse,self.actionSilence,self.actionInsert_Silence])

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
        self.widget.openNew(44100, 16, 5., whiteNoise=False)
        self.setWindowTitle("Duetto Sound Lab - (new)")
        self.statusbar.showMessage("Welcome to Duetto Sound Lab.")

    def updateRegionTheme(self):
        reg = self.hist.item.region.getRegion()
        valueMin = self.ParamTree.param('Spectrogram Settings').param('Threshold').param('Min').value()
        valueMax = self.ParamTree.param('Spectrogram Settings').param('Threshold').param('Max').value()
        if reg[0] != valueMin:
            self.ParamTree.param('Spectrogram Settings').param('Threshold').param('Min').setValue(reg[0])
        if reg[1] != valueMax:
            self.ParamTree.param('Spectrogram Settings').param('Threshold').param('Max').setValue(reg[1])

    def SerializeTheme(self,filename):
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
        file = open(filename,'rb')
        data = pickle.load(file)
        file.close()
        return data


    @pyqtSlot()
    def on_actionSave_theme_triggered(self):
        filename = QFileDialog.getSaveFileName(parent=self,caption="Save Theme",filter="Duetto Theme Files (*.dth);;All Files (*)")
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
        self.ParamTree.param('Spectrogram Settings').param('Threshold').param('Min').setValue(data.histRange[0])
        self.ParamTree.param('Spectrogram Settings').param('Threshold').param('Max').setValue(data.histRange[1])
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
        filename = QFileDialog.getOpenFileName(parent=self, caption="Load Theme",filter="Duetto Theme Files (*.dth);;All Files (*)")
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
        self.widget.open(path)
        self.setWindowTitle("Duetto Sound Lab - " + self.widget.signalProcessor.signal.name())
        self.hist.item.region.lineMoved()
        self.hist.item.region.lineMoveFinished()
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
                self.hist.item.region.lineMoved()
                self.hist.item.region.lineMoveFinished()

            elif childName == 'Spectrogram Settings.Grid.X':
                self.widget.spec_gridx = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=True, updateOscillogram=False, updateSpectrogram=False)

            elif childName == 'Spectrogram Settings.Grid.Y':
                self.widget.spec_gridy = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=True, updateOscillogram=False, updateSpectrogram=False)

            elif childName == 'Spectrogram Settings.Threshold.Min':
                if self.hist.item.region.getRegion()[0] != data:
                    self.hist.item.region.setRegion([data,self.hist.item.region.getRegion()[1]])
                    self.hist.item.region.lineMoved()
                    self.hist.item.region.lineMoveFinished()

            elif childName == 'Spectrogram Settings.Threshold.Max':
                if self.hist.item.region.getRegion()[1] != data:
                    self.hist.item.region.setRegion([self.hist.item.region.getRegion()[0],data])
                    self.hist.item.region.lineMoved()
                    self.hist.item.region.lineMoveFinished()

            elif childName == 'Spectrogram Settings.FFT window':
                self.widget.specgramSettings.window = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=True, updateOscillogram=False, updateSpectrogram=True)
                self.hist.item.region.lineMoved()
                self.hist.item.region.lineMoveFinished()

            elif childName == 'Spectrogram Settings.Background color':
                self.widget.spec_background = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=True,updateOscillogram=False,updateSpectrogram=False)
                self.hist.item.region.lineMoved()
                self.hist.item.region.lineMoveFinished()

            elif childName == 'Spectrogram Settings.ColorMap':
                self.widget.axesSpecgram.getHistogramWidget().item._pixelVectorCache.append(data)

            elif childName == 'Spectrogram Settings.Frequency.Min':
                self.widget.minYSpc = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=True, updateOscillogram=False, updateSpectrogram=True)
                self.hist.item.region.lineMoved()
                self.hist.item.region.lineMoveFinished()

            elif childName == 'Spectrogram Settings.Frequency.Max':
                self.widget.maxYSpc = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=True, updateOscillogram=False, updateSpectrogram=True)
                self.hist.item.region.lineMoved()
                self.hist.item.region.lineMoveFinished()

            elif childName == 'Spectrogram Settings.FFT overlap':
                self.widget.specgramSettings.overlap = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=True, updateOscillogram=False, updateSpectrogram=True)
                self.hist.item.region.lineMoved()
                self.hist.item.region.lineMoveFinished()

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
                self.widget.refresh(dataChanged=True, updateOscillogram=False, updateSpectrogram=False)
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
            elif childName == 'Oscillogram Settings.Min amplitude':
                self.widget.minYOsc = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=True, updateOscillogram=True, updateSpectrogram=False)
            elif childName == 'Oscillogram Settings.Max amplitude':
                self.widget.maxYOsc = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=True, updateOscillogram=True, updateSpectrogram=False)
            elif childName == 'Oscillogram Settings.Amplitude.Min':
                self.widget.minYOsc = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=True, updateOscillogram=True, updateSpectrogram=False)
            elif childName == 'Oscillogram Settings.Amplitude.Max':
                self.widget.maxYOsc = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=True, updateOscillogram=True, updateSpectrogram=False)
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
        segWindow = SegmentationAndClasificationWindow(parent=self, signal=self.widget.signalProcessor.signal)

        segWindow.widget.maxYOsc =  self.ParamTree.param('Oscillogram Settings').param('Amplitude').param('Max').value()
        segWindow.widget.minYOsc = self.ParamTree.param('Oscillogram Settings').param('Amplitude').param('Min').value()
        segWindow.widget.minYSpc = self.ParamTree.param('Spectrogram Settings').param('Frequency').param('Min').value()
        segWindow.widget.maxYSpc = self.ParamTree.param('Spectrogram Settings').param('Frequency').param('Max').value()

        segWindow.load_Theme(SerializedData(self.widget.osc_background,self.widget.osc_color,self.widget.osc_gridx,
                              self.widget.osc_gridy, self.pow_spec_backg,self.pow_spec_plotColor,self.pow_spec_gridx,
                              self.pow_spec_gridy, self.widget.spec_background, self.widget.spec_gridx, self.widget.spec_gridy,
                              self.hist.item.gradient.saveState(),self.hist.item.region.getRegion(),end,center,start,quart1,quart2))


        self.widget.undoRedoManager.clearActions()


    @pyqtSlot()
    def on_actionZoom_Cursor_triggered(self):
        if self.actionZoom_Cursor.isChecked():
            self.actionPointer_Cursor.setChecked(False)
            self.widget.setSelectedTool('ZoomCursor')
        elif not self.actionPointer_Cursor.isChecked():
            self.actionZoom_Cursor.setChecked(True)

    @pyqtSlot()
    def on_actionPointer_Cursor_triggered(self):
        if self.actionPointer_Cursor.isChecked():
            self.actionZoom_Cursor.setChecked(False)
            self.widget.setSelectedTool('PointerCursor')
        elif not self.actionZoom_Cursor.isChecked():
            self.actionPointer_Cursor.setChecked(True)

    @pyqtSlot()
    def on_actionResampling_triggered(self):
        resamplingDialog = sdialog.Ui_Dialog()
        resamplingDialogWindow = InsertSilenceDialog()
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
        self.hist.item.region.lineMoved()
        self.hist.item.region.lineMoveFinished()

    @pyqtSlot()
    def on_actionCopy_triggered(self):
        self.widget.copy()
        self.hist.item.region.lineMoved()
        self.hist.item.region.lineMoveFinished()

    @pyqtSlot()
    def on_actionPaste_triggered(self):
        start, _ = self.widget.getIndexFromAndTo()
        self.widget.undoRedoManager.addAction(PasteAction(self.widget.signalProcessor.signal,start,self.widget.editionSignalProcessor.clipboard))
        self.widget.paste()
        self.hist.item.region.lineMoved()
        self.hist.item.region.lineMoveFinished()

    @pyqtSlot()
    def on_actionUndo_triggered(self):
        self.widget.undo()

    @pyqtSlot()
    def on_actionRedo_triggered(self):
        self.widget.redo()

    @pyqtSlot()
    def on_actionSmart_Scale_triggered(self):
        scaleDialog = cvdialog.Ui_Dialog()
        scaleDialogWindow = ChangeVolumeDialog()
        scaleDialog.setupUi(scaleDialogWindow)
        if scaleDialogWindow.exec_():
            factor = scaleDialog.spinboxConstValue.value()
            if scaleDialog.rbuttonConst.isChecked():
                function = "const"
            elif scaleDialog.rbuttonNormalize.isChecked():
                function = "normalize"
                factor = scaleDialog.spinboxNormalizePercent.value()
            else:
                function = scaleDialog.cboxModulationType.currentText()
            fade = "IN" if scaleDialog.rbuttonFadeIn.isChecked() else (
                "OUT" if scaleDialog.rbuttonFadeOut.isChecked() else "")
            start,end = self.widget.getIndexFromAndTo()
            self.widget.undoRedoManager.addAction(ScaleAction(self.widget.signalProcessor.signal,start,end,factor, function, fade))
            self.widget.scale(factor, function, fade)

    @pyqtSlot()
    def on_actionInsert_Silence_triggered(self):
        silenceDialog = sdialog.Ui_Dialog()
        silenceDialogWindow = InsertSilenceDialog()
        silenceDialog.setupUi(silenceDialogWindow)
        if silenceDialogWindow.exec_():
            start,end = self.widget.getIndexFromAndTo()
            ms = silenceDialog.insertSpinBox.value()
            self.widget.undoRedoManager.addAction(InsertSilenceAction(self.widget.signalProcessor.signal,start,ms))
            self.widget.insertSilence(ms)

    @pyqtSlot()
    def on_actionGenerate_Pink_Noise_triggered(self):
        whiteNoiseDialog = sdialog.Ui_Dialog()
        whiteNoiseDialogWindow = InsertSilenceDialog()
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
        whiteNoiseDialogWindow = InsertSilenceDialog()
        whiteNoiseDialog.setupUi(whiteNoiseDialogWindow)
        whiteNoiseDialog.label.setText("Select the duration in ms \n of the white noise.")
        whiteNoiseDialog.insertSpinBox.setValue(1000)
        if whiteNoiseDialogWindow.exec_():
            ms = whiteNoiseDialog.insertSpinBox.value()
            start,end = self.widget.getIndexFromAndTo()
            self.widget.undoRedoManager.addAction(GenerateWhiteNoiseAction(self.widget.signalProcessor.signal,start,ms))
            self.widget.insertWhiteNoise()

    def filter_helper(self):
        filterDialog = filterdg.Ui_Dialog()
        filterDialogWindow = InsertSilenceDialog()
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
        self.widget.undoRedoManager.addAction(UndoRedoAction(self.widget.zoomOut,self.widget.zoomIn))
        self.widget.zoomIn()

    @pyqtSlot()
    def on_actionZoom_out_triggered(self):
        self.widget.undoRedoManager.addAction(UndoRedoAction(self.widget.zoomIn,self.widget.zoomOut))
        self.widget.zoomOut()

    @pyqtSlot()
    def on_actionZoom_out_entire_file_triggered(self):
        self.widget.undoRedoManager.clearActions()
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
        dg_pow_spec = PowerSpectrumWindow(self,self.pow_spec_plotColor, self.pow_spec_backg, self.pow_spec_gridx, self.pow_spec_gridy)

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
        self.actionHighest_instant_frequency.setChecked(False)
        f = QFileDialog.getOpenFileName(self, "Select a file to open",
                                              filter="Wave Files (*.wav);;All Files (*)")
        if f != '':
            self.widget.specgramSettings.NFFT = self.ParamTree.param('Spectrogram Settings').param('FFT size').value()
            self.widget.specgramSettings.overlap = self.ParamTree.param('Spectrogram Settings').param('FFT overlap').value()
            path_base = os.path.split(str(f))[0]
            self.filesInFolder = self.folderFiles(path_base)
            self.filesInFolderIndex = self.filesInFolder.index(str(f))
            self.widget.open(f)
            self.setWindowTitle("Duetto Sound Lab - " + self.widget.signalProcessor.signal.name())

            self.ParamTree.param('Spectrogram Settings').param('Frequency').param('Min').setValue(self.widget.minYSpc)
            self.ParamTree.param('Spectrogram Settings').param('Frequency').param('Min').setDefault(self.widget.minYSpc)
            self.ParamTree.param('Spectrogram Settings').param('Frequency').param('Max').setValue(self.widget.maxYSpc)
            self.ParamTree.param('Spectrogram Settings').param('Frequency').param('Max').setDefault(self.widget.maxYSpc)

            self.hist.item.region.lineMoved()
            self.hist.item.region.lineMoveFinished()

    @pyqtSlot()
    def on_actionFile_Up_triggered(self):
        if self.filesInFolderIndex < len(self.filesInFolder)-1:
            self.filesInFolderIndex += 1
            if os.path.exists(self.filesInFolder[self.filesInFolderIndex]):
                self.widget.open(self.filesInFolder[self.filesInFolderIndex])
                self.setWindowTitle("Duetto Sound Lab - " + self.widget.signalProcessor.signal.name())
                self.hist.item.region.lineMoved()
                self.hist.item.region.lineMoveFinished()

    @pyqtSlot()
    def on_actionFile_Down_triggered(self):
        if self.filesInFolderIndex > 0:
            self.filesInFolderIndex -= 1
            if os.path.exists(self.filesInFolder[self.filesInFolderIndex]):
                self.widget.open(self.filesInFolder[self.filesInFolderIndex])
                self.setWindowTitle("Duetto Sound Lab - " + self.widget.signalProcessor.signal.name())
                self.hist.item.region.lineMoved()
                self.hist.item.region.lineMoveFinished()

    @pyqtSlot()
    def on_actionSave_triggered(self):
        fname = unicode(QFileDialog.getSaveFileName())
        if fname:
            self.widget.save(fname)

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
        self.horizontalScrollBar.setSingleStep((right - left) / 16)
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
