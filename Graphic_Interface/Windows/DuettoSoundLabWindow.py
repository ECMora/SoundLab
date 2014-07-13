# -*- coding: utf-8 -*-
import os
import pickle
from PyQt4 import QtCore, QtGui
from pyqtgraph.python2_3 import asUnicode
from pyqtgraph.parametertree.parameterTypes import WidgetParameterItem,ListParameter
from Graphic_Interface.Windows.ParameterList import DuettoListParameterItem
from pyqtgraph.parametertree import Parameter, ParameterTree
from PyQt4.QtGui import QDialog, QMessageBox, QFileDialog, QActionGroup, QAction
from PyQt4.QtCore import SIGNAL, pyqtSlot, QTimer
from Graphic_Interface.Dialogs.NewFileDialog import NewFileDialog
from Duetto_Core.AudioSignals.WavFileSignal import WavFileSignal
from Graphic_Interface.Widgets.HorizontalHistogram import HorizontalHistogramWidget
from Graphic_Interface.Windows.PowerSpectrumWindow import PowerSpectrumWindow
from SegmentationAndClasificationWindow import SegmentationAndClasificationWindow
from Duetto_Core.SignalProcessors.FilterSignalProcessor import FILTER_TYPE
from Graphic_Interface.Widgets.UndoRedoActions import *
from MainWindow import Ui_DuettoMainWindow
from Graphic_Interface.Dialogs import InsertSilenceDialog as sdialog, FilterOptionsDialog as filterdg, ChangeVolumeDialog as cvdialog
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
        param.opts[u'value'] = param.opts[u'default']
        self.targetValue = None
        self.values = param.opts.get(u'values',[])
        self.valuesDict = {}
        for (a, b) in self.values:
            self.valuesDict[a] = b
        WidgetParameterItem.__init__(self, param, depth)

    def makeWidget(self):
        opts = self.param.opts
        t = opts[u'type']
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

        self.hist = HorizontalHistogramWidget()
        self.widget.histogram = self.hist
        self.pow_overlap = 90
        self.defaultTheme = self.DeSerializeTheme(os.path.join(os.path.join("Utils","Themes"),"RedBlackTheme.dth"))

        themesInFolder = self.folderFiles(os.path.join("Utils","Themes"),extensions=[".dth"])


        self.widget.osc_color = self.defaultTheme.osc_plot

        self.pow_spec_lines = True

        self.pow_spec_maxY = 5
        self.pow_spec_minY = -50
        self.widget.lines = True
        self.statusbar = self.statusBar()
        self.statusbar.setSizeGripEnabled(False)
        self.lastopen = ''
        self.statusbar.showMessage(u"Welcome to Duetto Sound Lab", 5000)
        params = [
        {u'name': u'Oscillogram Settings', u'type': u'group', u'children': [
            {u'name': u'Amplitude(%)', u'type': u'group', u'children': [
                 {u'name': u'Min', u'type': u'float', u'value': -100,u'step': 0.1},
                 {u'name': u'Max', u'type': u'float', u'value': 100, u'step': 0.1},
            ]},

            {u'name': u'Grid',u'type': u'group', u'children': [
                {u'name': u'X', u'type': u'bool',u'default': self.defaultTheme.osc_GridX, u'value': self.defaultTheme.osc_GridX},
                {u'name': u'Y', u'type': u'bool',u'default':self.defaultTheme.osc_GridY , u'value': self.defaultTheme.osc_GridY},

            ]},
            {u'name':u'Background color', u'type':u'color',u'value':self.defaultTheme.osc_background, u'default':self.defaultTheme.osc_background},
            {u'name': u'Plot color', u'type': u'color', u'value':self.defaultTheme.osc_plot,u'default': self.defaultTheme.osc_plot},
            {u'name': u'Connect Lines', u'type': u'bool',u'default': self.widget.lines, u'value': self.widget.lines},
        ]},

        {u'name': u'Spectrogram Settings', u'type': u'group', u'children': [
            {u'name': u'Frequency(kHz)', u'type':u'group', u'children': [
                {u'name': u'Min', u'type': u'float', u'value': 0, u'step': 0.1},
                {u'name': u'Max', u'type': u'float', u'value': 22, u'step': 0.1},
            ]},
           {u'name':u'FFT size', u'type': u'list', u'default':512, u'values': [(u'Automatic', 512),(u"8192",8192),(u"128", 128), (u"256", 256),(u"512", 512), (u"1024", 1024)], u'value': u'512'},
          {u'name': u'FFT window', u'type': u'list', u'value':self.widget.specgramSettings.windows[0],u'default':self.widget.specgramSettings.windows[0],u'values': [(u'Bartlett',self.widget.specgramSettings.windows[4]),(u"Blackman", self.widget.specgramSettings.windows[3]),(u"Hamming", self.widget.specgramSettings.windows[0]), (u"Hanning", self.widget.specgramSettings.windows[2]),(u'Kaiser',self.widget.specgramSettings.windows[5]),(u'None',self.widget.specgramSettings.windows[6]),(u"Rectangular", self.widget.specgramSettings.windows[1])]},
            {u'name': u'FFT overlap', u'type': u'int', u'value':-1, u'limits': (-1, 99)},
            {u'name': u'Threshold(dB)', u'type': u'group', u'children': [
                {u'name': u'Min', u'type': u'float',u'step':0.1,u'default': self.defaultTheme.histRange[0],u'value': self.defaultTheme.histRange[0]},
                {u'name': u'Max', u'type': u'float',u'step':0.1,u'default': self.defaultTheme.histRange[1] , u'value': self.defaultTheme.histRange[1]},
             ]},
            {u'name': u'Grid', u'type': u'group', u'children': [
                {u'name': u'X', u'type': u'bool',u'default': self.defaultTheme.spec_GridX, u'value': self.defaultTheme.spec_GridX},
                {u'name': u'Y', u'type': u'bool',u'default':self.defaultTheme.spec_GridY , u'value': self.defaultTheme.spec_GridY},

            ]},
            {u'name': u'Background color', u'type': u'color',u'value':self.defaultTheme.spec_background, u'default': self.defaultTheme.spec_background},
        ]},

        {u'name': u'Power Spectrum Settings', u'type': u'group', u'children': [

            {u'name': u'FFT size', u'type': u'list', u'default':512, u'values': [(u'Automatic', 512),(u"128", 128),(u"256", 256), (u"512", 512), (u"1024", 1024)], u'value': u'Automatic'},
            {u'name': u'FFT window',u'type': u'list', u'value':self.widget.specgramSettings.windows[0],u'default':self.widget.specgramSettings.windows[0],u'values': [(u'Bartlett',self.widget.specgramSettings.windows[4]),(u"Blackman", self.widget.specgramSettings.windows[3]),(u"Hamming", self.widget.specgramSettings.windows[0]), (u"Hanning", self.widget.specgramSettings.windows[2]),(u'Kaiser',self.widget.specgramSettings.windows[5]),(u'None',self.widget.specgramSettings.windows[6]),(u"Rectangular", self.widget.specgramSettings.windows[1])]},
            {u'name': u'FFT overlap', u'type': u'int',u'value':self.pow_overlap, u'limits' : (-1,100)},
            {u'name': u'Grid', u'type': u'group', u'children': [
                {u'name': u'X', u'type': u'bool',u'default': self.defaultTheme.pow_GridX, u'value': self.defaultTheme.pow_GridX},
                {u'name': u'Y', u'type': u'bool',u'default':self.defaultTheme.pow_GridY , u'value': self.defaultTheme.pow_GridY},

             ]},
             {u'name': u'Connect Lines',u'type': u'bool',u'default': self.pow_spec_lines, u'value': self.pow_spec_lines},
             {u'name': u'YBounds', u'type': u'group', u'children': [
                {u'name': u'MinY', u'type': u'int', u'limits' : (-60,5),u'default': -50, u'value': -50},
                {u'name': u'MaxY', u'type': u'int', u'limits' : (-60,5),u'default': 5 ,u'value': 5},


             ]},
             {u'name':u'Background color', u'type':u'color',u'value':self.defaultTheme.pow_Back, 'default':self.defaultTheme.pow_Back},
             {u'name': u'Plot color',u'type': u'color',u'value':self.defaultTheme.pow_Plot, 'default': self.defaultTheme.pow_Plot},
        ]},
        {u'name': u'Themes', u'type': u'group', u'children': [
         {u'name': u'Theme Selected', u'type': u'list', u'value':u"" if len(themesInFolder) == 0 else themesInFolder[0][themesInFolder[0].rfind(os.path.sep)+1:themesInFolder[0].rfind(".dth")],\
          u'default':u"" if len(themesInFolder) == 0 else themesInFolder[0],u'values': [(x[x.rfind(os.path.sep)+1:x.rfind(".dth")], x) for x in themesInFolder]},
        ]
        } ,
        {u'name': u'Detection Visual Settings', u'type': u'group', u'children': [
            {u'name': u'Measurement Location', u'type': u'group', u'children': [
            {u'name': u'Start', u'type': u'color',u'value': self.defaultTheme.startColor,u'default': self.defaultTheme.startColor},
            {u'name': u'Quartile25', u'type': u'color', u'value': self.defaultTheme.quart1Color,u'default': self.defaultTheme.quart1Color},
            {u'name':u'Center', u'type':u'color',u'value':self.defaultTheme.centerColor,u'default':self.defaultTheme.centerColor},
            {u'name': u'Quartile75', u'type': u'color', u'value':self.defaultTheme.quart2Color,u'default':self.defaultTheme.quart2Color},
            {u'name': u'End', u'type': u'color',u'value':self.defaultTheme.endColor,u'default':self.defaultTheme.endColor},
        ]},]}

        ]

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
        self.connect(self.widget, SIGNAL(u"IntervalChanged"), self.updatePowSpecWin)
        self.NFFT_pow = 512

        self.window_pow = self.widget.specgramSettings.windows[0]
        self.window_spec = self.widget.specgramSettings.windows[0]

        self.pow_spec_windows = []

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
        self.ParamTree.param(u'Spectrogram Settings').param(u'Frequency(kHz)').param(u'Min').setValue(min)
        self.ParamTree.param(u'Spectrogram Settings').param(u'Frequency(kHz)').param(u'Max').setValue(max)

    def changeAmplitude(self, min, max):
        self.ParamTree.param(u'Oscillogram Settings').param(u'Amplitude(%)').param(u'Min').setValue(min)
        self.ParamTree.param(u'Oscillogram Settings').param(u'Amplitude(%)').param(u'Max').setValue(max)

    def folderFiles(self,folder,extensions=None):
        files = []
        extensions = [".wav"] if extensions is None else extensions
        for root, dirs, filenames in os.walk(folder):
            for f in filenames:
                if extensions is None or any([f.endswith(x) for x in extensions]):
                    files.append(unicode(root+os.path.sep+f))

        return files

    def updateStatusBar(self,line):
        self.statusbar.showMessage(line)

    def on_load(self):
        self.widget.visibleOscilogram = True
        self.widget.visibleSpectrogram = True
        self.widget.specgramSettings.NFFT = self.ParamTree.param(u'Spectrogram Settings').param(u'FFT size').value()
        self.widget.specgramSettings.overlap = self.ParamTree.param(u'Spectrogram Settings').param(u'FFT overlap').value()
        p = os.path.join(os.path.join(u"Utils",u"Didactic Signals"),u"duetto.wav")
       
        if os.path.exists(p):
            self.widget.open(p)
            self.actionSignalName.setText(u"File Name: "+ self.widget.signalName())
        else:
            self.widget.openNew(44100, 16, 5., whiteNoise=False)
            self.actionSignalName.setText(u"File Name: Welcome to duetto")

        self.setWindowTitle(u"Duetto Sound Lab - Welcome to Duetto")
        self.statusbar.showMessage(u"Welcome to Duetto Sound Lab.")
        self.widget.load_Theme(self.defaultTheme)

    def updateRegionTheme(self):
        reg = self.hist.item.region.getRegion()
        valueMin = self.ParamTree.param(u'Spectrogram Settings').param(u'Threshold(dB)').param(u'Min').value()
        valueMax = self.ParamTree.param(u'Spectrogram Settings').param(u'Threshold(dB)').param(u'Max').value()
        if reg[0] != valueMin:
            self.ParamTree.param(u'Spectrogram Settings').param(u'Threshold(dB)').param(u'Min').setValue(reg[0])
        if reg[1] != valueMax:
            self.ParamTree.param(u'Spectrogram Settings').param(u'Threshold(dB)').param(u'Max').setValue(reg[1])

    def SerializeTheme(self,filename):
        if filename:
            self.defaultTheme.centerColor = self.ParamTree.param('Detection Settings').param('Measurement Location').param('Center').value()
            self.defaultTheme.startColor = self.ParamTree.param('Detection Settings').param('Measurement Location').param('Start').value()
            self.defaultTheme.quart1Color = self.ParamTree.param('Detection Settings').param('Measurement Location').param('Quartile25').value()
            self.defaultTheme.quart2Color = self.ParamTree.param('Detection Settings').param('Measurement Location').param('Quartile75').value()
            self.defaultTheme.endColor = self.ParamTree.param('Detection Settings').param('Measurement Location').param('End').value()
            self.defaultTheme.histRange = self.hist.item.region.getRegion()
            self.defaultTheme.colorBarState = self.hist.item.gradient.saveState()
            file = open(filename,'wb')
            pickle.dump(self.defaultTheme,file)
            file.close()

    def DeSerializeTheme(self,filename):
        if filename and os.path.exists(filename):
            file = open(filename,'rb')
            data = pickle.load(file)
            file.close()
            return data
        return SerializedData()


    @pyqtSlot()
    def on_actionChangePlayStatus_triggered(self):
        self.widget.changePlayStatus()

    @pyqtSlot()
    def on_actionSave_theme_triggered(self):
        filename = QFileDialog.getSaveFileName(parent=self,caption=u"Save Theme",directory = os.path.join(u"Utils",u"Themes"),filter=u"Duetto Theme Files (*.dth);;All Files (*)")
        if filename:
            self.SerializeTheme(filename)

    def updateMyTheme(self,theme):

        assert isinstance(theme, SerializedData)
        self.widget.osc_color = theme.osc_plot
        self.defaultTheme = theme
        self.widget.load_Theme(theme)
        self.hist.item.gradient.restoreState(theme.colorBarState)
        self.hist.item.region.setRegion(theme.histRange)

        self.hist.item.region.lineMoved()
        self.hist.item.region.lineMoveFinished()

        self.ParamTree.param(u'Oscillogram Settings').param(u'Grid').param(u'X').setValue(theme.osc_GridX)
        self.ParamTree.param(u'Oscillogram Settings').param(u'Grid').param(u'Y').setValue(theme.osc_GridY)
        self.ParamTree.param(u'Spectrogram Settings').param(u'Grid').param(u'X').setValue(theme.spec_GridX)
        self.ParamTree.param(u'Spectrogram Settings').param(u'Grid').param(u'Y').setValue(theme.spec_GridY)
        self.ParamTree.param(u'Oscillogram Settings').param(u'Background color').setValue(theme.osc_background)
        self.ParamTree.param(u'Oscillogram Settings').param(u'Plot color').setValue(theme.osc_plot)
        self.ParamTree.param(u'Spectrogram Settings').param(u'Background color').setValue(theme.spec_background)
        self.ParamTree.param(u'Spectrogram Settings').param(u'Threshold(dB)').param(u'Min').setValue(theme.histRange[0])
        self.ParamTree.param(u'Spectrogram Settings').param(u'Threshold(dB)').param(u'Max').setValue(theme.histRange[1])
        self.ParamTree.param(u'Power Spectrum Settings').param(u'Grid').param(u'X').setValue(self.defaultTheme.pow_GridX)
        self.ParamTree.param(u'Power Spectrum Settings').param(u'Grid').param(u'Y').setValue(self.defaultTheme.pow_GridY)
        self.ParamTree.param(u'Power Spectrum Settings').param(u'Background color').setValue(theme.pow_Back)
        self.ParamTree.param(u'Power Spectrum Settings').param(u'Plot color').setValue(self.defaultTheme.pow_Plot)
        self.ParamTree.param(u'Detection Visual Settings').param(u'Measurement Location').param(u'Center').setValue(theme.centerColor)
        self.ParamTree.param(u'Detection Visual Settings').param(u'Measurement Location').param(u'Start').setValue(theme.startColor)
        self.ParamTree.param(u'Detection Visual Settings').param(u'Measurement Location').param(u'Quartile25').setValue(theme.quart1Color)
        self.ParamTree.param(u'Detection Visual Settings').param(u'Measurement Location').param(u'Quartile75').setValue(theme.quart2Color)

    @pyqtSlot()
    def on_actionLoad_Theme_triggered(self):
        filename = QFileDialog.getOpenFileName(parent=self,directory = os.path.join(u"Utils",u"Themes"), caption=u"Load Theme",filter=u"Duetto Theme Files (*.dth);;All Files (*)")
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
        mimeUrl = u"".join([unicode(url.path()) for url in mimeData.urls()])

        self.widget.visibleOscilogram = True
        self.widget.visibleSpectrogram = True
        path = mimeUrl[1:len(mimeUrl)]
        path_base = os.path.split(path)[0]
        self.filesInFolder = self.folderFiles(path_base)

        try:
            self.filesInFolderIndex = self.filesInFolder.index(path)
        except:
            self.filesInFolderIndex = 0 if len(self.filesInFolder)>0 else -1

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

            if childName ==u'Spectrogram Settings.FFT size':
                self.widget.specgramSettings.NFFT = data
                self.widget.refresh(dataChanged=True, updateOscillogram=False, updateSpectrogram=True)

            elif childName == u'Spectrogram Settings.Grid.X':
                self.defaultTheme.spec_GridX = data

            elif childName == u'Spectrogram Settings.Grid.Y':
                self.defaultTheme.spec_GridY = data

            elif childName ==u'Spectrogram Settings.Threshold(dB).Min':
                if self.hist.item.region.getRegion()[0] != data:
                    if data > self.ParamTree.param(u'Spectrogram Settings').param(u'Threshold(dB)').param(u'Max').value():
                        self.ParamTree.param(u'Spectrogram Settings').param(u'Threshold(dB)').param(u'Min').setToDefault()
                        self.ParamTree.param(u'Spectrogram Settings').param(u'Threshold(dB)').param(u'Min').show()
                        return
                    self.hist.item.region.setRegion([data,self.hist.item.region.getRegion()[1]])
                    self.hist.item.region.lineMoved()
                    self.hist.item.region.lineMoveFinished()

            elif childName == u'Spectrogram Settings.Threshold(db%).Max':
                if self.hist.item.region.getRegion()[1] != data:
                    if data < self.ParamTree.param(u'Spectrogram Settings').param(u'Threshold(dB)').param(u'Min').value():
                        self.ParamTree.param(u'Spectrogram Settings').param(u'Threshold(dB)').param(u'Max').setToDefault()
                        self.ParamTree.param(u'Spectrogram Settings').param(u'Threshold(dB)').param(u'Max').setValue()
                        return
                    self.hist.item.region.setRegion([self.hist.item.region.getRegion()[0],data])
                    self.hist.item.region.lineMoved()
                    self.hist.item.region.lineMoveFinished()

            elif childName == u'Spectrogram Settings.FFT window':
                self.widget.specgramSettings.window = data
                self.widget.refresh(dataChanged=True, updateOscillogram=False, updateSpectrogram=True)

            elif childName == u'Spectrogram Settings.Background color':
                self.defaultTheme.spec_background = data

            elif childName == u'Spectrogram Settings.ColorMap':
                self.widget.axesSpecgram.getHistogramWidget().item._pixelVectorCache.append(data)

            elif childName ==u'Spectrogram Settings.Frequency(kHz).Min':
                self.defaultTheme.minYSpec = data

            elif childName == u'Spectrogram Settings.Frequency(kHz).Max':
                self.defaultTheme.maxYSpec = data

            elif childName == u'Spectrogram Settings.FFT overlap':
                self.widget.specgramSettings.overlap = data
                self.widget.refresh(dataChanged=True, updateOscillogram=False, updateSpectrogram=True)

            elif childName == u'Power Spectrum Settings.FFT size':
                self.NFFT_pow = data

            elif childName == u'Power Spectrum Settings.FFT window':
                self.window_pow = data
            elif childName == u'Power Spectrum Settings.FFT overlap':
                self.pow_overlap = data

            elif childName == u'Power Spectrum Settings.Background color':
                self.defaultTheme.pow_Back = data

            elif childName == u'Power Spectrum Settings.Plot color':
                self.defaultTheme.pow_Plot = data

            elif childName == u'Power Spectrum Settings.Grid.X':
                self.defaultTheme.pow_GridX = data

            elif childName == u'Power Spectrum Settings.Grid.Y':
                self.defaultTheme.pow_GridY = data

            elif childName == u'Oscillogram Settings.Background color':
                self.defaultTheme.osc_background = data

            elif childName == u'Oscillogram Settings.Grid.X':
                self.defaultTheme.osc_GridX = data

            elif childName == u'Oscillogram Settings.Grid.Y':
                self.defaultTheme.osc_GridY = data

            elif childName == u'Oscillogram Settings.Plot color':
                self.defaultTheme.osc_plot = data
                self.widget.osc_color = data
                self.widget.refresh(dataChanged=True, updateOscillogram=True, updateSpectrogram=False)
                return

            elif childName == u'Oscillogram Settings.Amplitude(%).Min':
                self.defaultTheme.minYOsc = data
            elif childName == u'Oscillogram Settings.Amplitude(%).Max':
                self.defaultTheme.maxYOsc = data
            elif childName == u'Oscillogram Settings.Connect Lines':
                self.widget.lines = data
                self.widget.refresh(dataChanged=True, updateOscillogram=True, updateSpectrogram=False)
                return

            elif childName ==u'Themes.Theme Selected':
                self.updateMyTheme(self.DeSerializeTheme(data))

            elif childName == u'Power Spectrum Settings.YBounds.MaxY':
                self.pow_spec_maxY = data
            elif childName == u'Power Spectrum Settings.YBounds.MinY':
                self.pow_spec_minY = data
            elif childName == u'Power Spectrum Settings.Connect Lines':
                self.pow_spec_lines = data

            self.widget.load_Theme(self.defaultTheme)
            #print('  parameter: %s' % childName)
            #print('  change:    %s' % change)
            #print('  data:      %s' % str(data))
            #print('  ----------')

    @pyqtSlot()
    def on_actionSegmentation_And_Clasification_triggered(self):
        self.defaultTheme.centerColor = self.ParamTree.param(u'Detection Visual Settings').param(u'Measurement Location').param(u'Center').value()
        self.defaultTheme.startColor = self.ParamTree.param(u'Detection Visual Settings').param(u'Measurement Location').param(u'Start').value()
        self.defaultTheme.quart1Color = self.ParamTree.param(u'Detection Visual Settings').param(u'Measurement Location').param(u'Quartile25').value()
        self.defaultTheme.quart2Color = self.ParamTree.param(u'Detection Visual Settings').param(u'Measurement Location').param(u'Quartile75').value()
        self.defaultTheme.endColor = self.ParamTree.param(u'Detection Visual Settings').param(u'Measurement Location').param(u'End').value()
        f,t = self.widget.getIndexFromAndTo()
        signal = WavFileSignal(samplingRate=self.widget.signalProcessor.signal.samplingRate,bitDepth=self.widget.signalProcessor.signal.bitDepth,whiteNoise=False)
        signal.name = self.widget.signalName()
        if t > f:
            signal.data = self.widget.signalProcessor.signal.data[f:t]

        segWindow = SegmentationAndClasificationWindow(parent=self, signal=signal)
        if not segWindow.rejectSignal:
            segWindow.widget.maxYOsc =  self.ParamTree.param(u'Oscillogram Settings').param(u'Amplitude(%)').param(u'Max').value()
            segWindow.widget.minYOsc = self.ParamTree.param(u'Oscillogram Settings').param(u'Amplitude(%)').param(u'Min').value()
            segWindow.widget.minYSpc = self.ParamTree.param(u'Spectrogram Settings').param(u'Frequency(kHz)').param(u'Min').value()
            segWindow.widget.maxYSpc = self.ParamTree.param(u'Spectrogram Settings').param(u'Frequency(kHz)').param(u'Max').value()

            self.defaultTheme.histRange = self.hist.item.region.getRegion()
            self.defaultTheme.colorBarState = self.hist.item.gradient.saveState()

            segWindow.load_Theme(self.defaultTheme)
            segWindow.widget.refresh()

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
        resamplingDialog.label.setText(u"Select the new Sampling Rate.")
        resamplingDialog.insertSpinBox.setValue(self.widget.signalProcessor.signal.samplingRate)
        if resamplingDialogWindow.exec_():
            val = resamplingDialog.insertSpinBox.value()
            if val > MIN_SAMPLING_RATE and val < MAX_SAMPLING_RATE:
                self.widget.undoRedoManager.addAction(ResamplingAction(self.widget.signalProcessor.signal,val))
                self.widget.resampling(val)
            else:
                if val < MIN_SAMPLING_RATE:
                    QMessageBox.warning(QMessageBox(), u"Error",
                                       u"Sampling rate should be greater than " + str(MIN_SAMPLING_RATE))
                elif val > MAX_SAMPLING_RATE:
                    QMessageBox.warning(QMessageBox(), u"Error",
                                        u"Sampling rate should be less than " + str(MAX_SAMPLING_RATE))

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
            fade = u""
            factor = scaleDialog.spinboxConstValue.value()
            if scaleDialog.rbuttonConst.isChecked():
                function = u"const"
            elif scaleDialog.rbuttonNormalize.isChecked():
                function = u"normalize"
                factor = scaleDialog.spinboxNormalizePercent.value()
            else:
                function = scaleDialog.cboxModulationType.currentText()
                fade = u"IN" if scaleDialog.rbuttonFadeIn.isChecked() else (u"OUT" if scaleDialog.rbuttonFadeOut.isChecked() else "")
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
        whiteNoiseDialog.label.setText(u"Select the duration in ms \n of the Pink Noise.")
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
        whiteNoiseDialog.label.setText(u"Select the duration in ms \n of the white noise.")
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
        dg_pow_spec = PowerSpectrumWindow(self,self.pow_spec_minY,self.pow_spec_maxY,self.pow_spec_lines)
        dg_pow_spec.load_Theme(self.defaultTheme)
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
        mbox = QtGui.QMessageBox(QtGui.QMessageBox.Question,u"Save",u"Do you want to save the signal?",QtGui.QMessageBox.Yes | QtGui.QMessageBox.No|QtGui.QMessageBox.Cancel,self)
        result = mbox.exec_()
        if self.widget.undoRedoManager.count() > 0 and  result == QtGui.QMessageBox.Yes:
            self.on_actionSave_triggered()
        elif result == QtGui.QMessageBox.Cancel and event is not None:
            event.ignore()

    @pyqtSlot()
    def on_actionNew_triggered(self):
        nfd = NewFileDialog(parent=self)
        if nfd.exec_():
            self.widget.specgramSettings.NFFT = self.ParamTree.param(u'Spectrogram Settings').param(u'FFT size').value()
            self.widget.specgramSettings.overlap = self.ParamTree.param(u'Spectrogram Settings').param(u'FFT overlap').value()
            self.widget.openNew(nfd.SamplingRate, nfd.BitDepth, nfd.Duration, nfd.WhiteNoise)
            self.setWindowTitle(u"Duetto Sound Lab - " + self.widget.signalName())
            self.actionSignalName.setText(u"File Name: "+self.widget.signalName())

            self.actionCombined.setEnabled(True)
            self.actionSpectogram.setEnabled(True)

    @pyqtSlot()
    def on_actionOpen_triggered(self):
        f = QFileDialog.getOpenFileName(self, u"Select a file to open",directory = self.lastopen,
                                              filter=u"Wave Files (*.wav);;All Files (*)")
        self._open(unicode(f))
        for win in self.pow_spec_windows: win.close()
        self.pow_spec_windows = []

    @pyqtSlot()
    def on_actionClose_triggered(self):
        self._save()
        self.on_load()

    def _open(self,f=''):

        self.actionCombined.setEnabled(True)
        self.actionSpectogram.setEnabled(True)
        if f != u'':
            try:
                self.lastopen = f
                self.widget.specgramSettings.NFFT = self.ParamTree.param(u'Spectrogram Settings').param(u'FFT size').value()
                self.widget.specgramSettings.overlap = self.ParamTree.param(u'Spectrogram Settings').param(u'FFT overlap').value()
                path_base = os.path.split(f)[0]
                self.filesInFolder = self.folderFiles(path_base)

                try:
                    self.filesInFolderIndex = self.filesInFolder.index(f)
                except:
                    self.filesInFolderIndex = 0 if len(self.filesInFolder) > 0 else -1

                self.widget.visibleSpectrogram = True # for restore the state lose in load
                self.widget.open(f)
                self.setWindowTitle(u"Duetto Sound Lab - " + self.widget.signalName())
                self.actionSignalName.setText(u"File Name: "+self.widget.signalName())
            except:
                QMessageBox.warning(QMessageBox(),u"Error", u"Could not load the file.\n"+f)
                self.widget.openNew(44100,16,1)

            valuemin = 0
            valuemax = self.widget.signalProcessor.signal.samplingRate/2000

            self.ParamTree.param(u'Spectrogram Settings').param(u'Frequency(kHz)').param(u'Min').setValue(valuemin)
            self.ParamTree.param(u'Spectrogram Settings').param(u'Frequency(kHz)').param(u'Max').setDefault(valuemax)
            self.ParamTree.param(u'Spectrogram Settings').param(u'Frequency(kHz)').param(u'Max').setValue(valuemax)

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
        fname = unicode(QFileDialog.getSaveFileName(self,u"Save signal",self.widget.signalName(),u"*.wav"))
        if fname:
            self.widget.save(fname)

    @pyqtSlot()
    def on_actionSave_selected_interval_as_triggered(self):
        fname = unicode(QFileDialog.getSaveFileName(self,u"Save signal",u"Selection-"+self.widget.signalName(),u"*.wav"))
        if fname:
            self.widget.saveSelected(fname)

    @pyqtSlot()
    def on_actionPlay_Sound_triggered(self):
        self.widget.play()


    @pyqtSlot()
    def on_actionStop_Sound_triggered(self):
        self.widget.stop()
        self.actionPlay_Sound.setEnabled(True)
        self.actionPause_Sound.setEnabled(True)
        self.actionZoom_out.setEnabled(True)
        self.actionZoomIn.setEnabled(True)
        self.actionZoom_out_entire_file.setEnabled(True)

    @pyqtSlot()
    def on_actionRecord_triggered(self):
        self.actionPlay_Sound.setEnabled(False)
        self.actionPause_Sound.setEnabled(False)
        self.actionZoom_out.setEnabled(False)
        self.actionZoomIn.setEnabled(False)
        self.actionZoom_out_entire_file.setEnabled(False)
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
            self.saveImage(self.widget.axesOscilogram,u"oscilogram")
        else:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), u"Error", u"The Oscilogram plot widget is not visible.\n You should see the data that you are going to save.")

    @pyqtSlot()
    def on_actionCombined_Image_triggered(self):
        if self.widget.visibleOscilogram and self.widget.visibleSpectrogram:
            self.saveImage(self.widget,"graph")
        else:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), u"Error", u"One of the plot widgets is not visible.\n You should see the data that you are going to save.")

    @pyqtSlot()
    def on_actionFull_Screen_triggered(self):
        if self.actionFull_Screen.isChecked():
            self.showFullScreen()
        else:
            self.showNormal()

    @pyqtSlot()
    def on_actionSpecgram_Image_triggered(self):
        if self.widget.visibleSpectrogram:
            self.saveImage(self.widget.axesSpecgram,u"specgram")
        else:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), u"Error",u"The Espectrogram plot widget is not visible.\n You should see the data that you are going to save.")

    def saveImage(self,widget,text=""):
        fname = unicode(QFileDialog.getSaveFileName(self,u"Save "+ text +u" as an Image ",str(self.widget.signalName())+u"-"+text+u"-Duetto-Image",u"*.jpg"))
        if fname:
            #save as image
            image = QtGui.QPixmap.grabWindow(widget.winId())
            image.save(fname,u'jpg')

    @pyqtSlot()
    def on_actionSaveColorBar_triggered(self):
        state = self.widget.axesSpecgram.getHistogramWidget().item.gradient.saveState()
        path = QtGui.QFileDialog.getSaveFileName(self, u"Save Color Bar", filter=u"Bar Files (*.bar);;All Files (*)")
        if path != u"":
            fh = open(path, 'w')
            fh.write(state.__repr__())
            fh.close()

    @pyqtSlot()
    def on_actionLoadColorBar_triggered(self):
        path = QtGui.QFileDialog.getOpenFileName(self, u"Load Color Bar", filter=u"Bar Files (*.bar);;All Files (*)")
        if path != "":
            fh = open(path, u'r')
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
        self.widget.playerSpeed = {u'1/8x': 12.5, u'1/4x': 25, u'1/2x': 50,
                                   u'1x': 100, u'2x': 200, u'4x': 400, u'8x': 800}[str(action.text())]
