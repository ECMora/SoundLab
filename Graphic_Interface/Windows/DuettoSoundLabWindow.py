# -*- coding: utf-8 -*-
import os
import pickle
from PyQt4 import QtCore, QtGui
from pyqtgraph.python2_3 import asUnicode
from pyqtgraph.parametertree.parameterTypes import WidgetParameterItem, ListParameter
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
from Graphic_Interface.Dialogs import InsertSilenceDialog as sdialog, FilterOptionsDialog as filterdg, \
    ChangeVolumeDialog as cvdialog
from WorkTheme import SerializedData
from Graphic_Interface.Widgets.Tools import Tools
from Duetto_Core.Clasification.ClassificationData import ClassificationData


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

        self.hist = HorizontalHistogramWidget()
        self.widget.histogram = self.hist
        self.pow_overlap = 90
        self.defaultTheme = self.DeSerializeTheme(os.path.join(os.path.join("Utils", "Themes"), "RedBlackTheme.dth"))

        themesInFolder = self.folderFiles(os.path.join("Utils", "Themes"), extensions=[".dth"])

        self.widget.osc_color = self.defaultTheme.osc_plot

        self.pow_spec_lines = True

        self.pow_spec_maxY = 5
        self.pow_spec_minY = -50
        self.widget.lines = True
        self.statusbar = self.statusBar()
        self.statusbar.setSizeGripEnabled(False)
        self.lastopen = ''
        self.statusbar.showMessage(self.tr(u"Welcome to Duetto Sound Lab"), 5000)
        params = [
            {u'name': unicode(self.tr(u'Oscillogram Settings')), u'type': u'group', u'children': [
                {u'name': unicode(self.tr(u'Amplitude(%)')), u'type': u'group', u'children': [
                    {u'name': unicode(self.tr(u'Min')), u'type': u'float', u'value': -100, u'step': 0.1},
                    {u'name': unicode(self.tr(u'Max')), u'type': u'float', u'value': 100, u'step': 0.1},
                ]},

                {u'name': unicode(self.tr(u'Grid')), u'type': u'group', u'children': [
                    {u'name': u'X', u'type': u'bool', u'default': self.defaultTheme.osc_GridX,
                     u'value': self.defaultTheme.osc_GridX},
                    {u'name': u'Y', u'type': u'bool', u'default': self.defaultTheme.osc_GridY,
                     u'value': self.defaultTheme.osc_GridY},

                ]},
                {u'name': unicode(self.tr(u'Background color')), u'type': u'color',
                 u'value': self.defaultTheme.osc_background, u'default': self.defaultTheme.osc_background},
                {u'name': unicode(self.tr(u'Plot color')), u'type': u'color', u'value': self.defaultTheme.osc_plot,
                 u'default': self.defaultTheme.osc_plot},
                {u'name': unicode(self.tr(u'Connect Lines')), u'type': u'bool', u'default': self.widget.lines,
                 u'value': self.widget.lines},
            ]},

            {u'name': unicode(self.tr(u'Spectrogram Settings')), u'type': u'group', u'children': [
                {u'name': unicode(self.tr(u'Frequency(kHz)')), u'type': u'group', u'children': [
                    {u'name': unicode(self.tr(u'Min')), u'type': u'float', u'value': 0, u'step': 0.1},
                    {u'name': unicode(self.tr(u'Max')), u'type': u'float', u'value': 22, u'step': 0.1},
                ]},
                {u'name': unicode(self.tr(u'FFT size')), u'type': u'list', u'default': 512,
                 u'values': [(unicode(self.tr(u'Automatic')), 512), (u"8192", 8192), (u"128", 128), (u"256", 256),
                             (u"512", 512), (u"1024", 1024)], u'value': u'512'},
                {u'name': unicode(self.tr(u'FFT window')), u'type': u'list',
                 u'value': self.widget.specgramSettings.windows[0], u'default': self.widget.specgramSettings.windows[0],
                 u'values': [(u'Bartlett', self.widget.specgramSettings.windows[4]),
                             (u"Blackman", self.widget.specgramSettings.windows[3]),
                             (u"Hamming", self.widget.specgramSettings.windows[0]),
                             (u"Hanning", self.widget.specgramSettings.windows[2]),
                             (u'Kaiser', self.widget.specgramSettings.windows[5]),
                             (unicode(self.tr(u'None')), self.widget.specgramSettings.windows[6]),
                             (u"Rectangular", self.widget.specgramSettings.windows[1])]},
                {u'name': unicode(self.tr(u'FFT overlap')), u'type': u'int', u'value': -1, u'limits': (-1, 99)},
                {u'name': unicode(self.tr(u'Threshold(dB)')), u'type': u'group', u'children': [
                    {u'name': unicode(self.tr(u'Min')), u'type': u'float', u'step': 0.1,
                     u'default': self.defaultTheme.histRange[0], u'value': self.defaultTheme.histRange[0]},
                    {u'name': unicode(self.tr(u'Max')), u'type': u'float', u'step': 0.1,
                     u'default': self.defaultTheme.histRange[1], u'value': self.defaultTheme.histRange[1]},
                ]},
                {u'name': unicode(self.tr(u'Grid')), u'type': u'group', u'children': [
                    {u'name': u'X', u'type': u'bool', u'default': self.defaultTheme.spec_GridX,
                     u'value': self.defaultTheme.spec_GridX},
                    {u'name': u'Y', u'type': u'bool', u'default': self.defaultTheme.spec_GridY,
                     u'value': self.defaultTheme.spec_GridY},

                ]},
                {u'name': unicode(self.tr(u'Background color')), u'type': u'color',
                 u'value': self.defaultTheme.spec_background, u'default': self.defaultTheme.spec_background},
            ]},
            {u'name': unicode(self.tr(u'Themes')), u'type': u'group', u'children': [
                {u'name': unicode(self.tr(u'Theme Selected')), u'type': u'list',
                 u'value': u"" if len(themesInFolder) == 0 else themesInFolder[0][
                                                                themesInFolder[0].rfind(os.path.sep) + 1:themesInFolder[
                                                                    0].rfind(".dth")], \
                 u'default': u"" if len(themesInFolder) == 0 else themesInFolder[0],
                 u'values': [(x[x.rfind(os.path.sep) + 1:x.rfind(".dth")], x) for x in themesInFolder]},
            ]
            },
            {u'name': unicode(self.tr(u'Detection Visual Settings')), u'type': u'group', u'children': [
                {u'name': unicode(self.tr(u'Measurement Location')), u'type': u'group', u'children': [
                    {u'name': unicode(self.tr(u'Start')), u'type': u'color', u'value': self.defaultTheme.startColor,
                     u'default': self.defaultTheme.startColor},
                    {u'name': unicode(self.tr(u'Quartile25')), u'type': u'color',
                     u'value': self.defaultTheme.quart1Color, u'default': self.defaultTheme.quart1Color},
                    {u'name': unicode(self.tr(u'Center')), u'type': u'color', u'value': self.defaultTheme.centerColor,
                     u'default': self.defaultTheme.centerColor},
                    {u'name': unicode(self.tr(u'Quartile75')), u'type': u'color',
                     u'value': self.defaultTheme.quart2Color, u'default': self.defaultTheme.quart2Color},
                    {u'name': unicode(self.tr(u'End')), u'type': u'color', u'value': self.defaultTheme.endColor,
                     u'default': self.defaultTheme.endColor},
                ]}]}

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
        # the next 2 lines are a PARCHE for the error of deselect zoom region when the region changes
        self.hist.item.region.sigRegionChanged.connect(self.widget.clearZoomCursor)
        self.ParamTree.sigTreeStateChanged.connect(self.widget.clearZoomCursor)

        action = self.hist.item.gradient.hsvAction
        action.triggered.disconnect()
        action.triggered.connect(self.widget.SaveColorBar)
        action.setCheckable(False)
        action.setText(self.tr("Save"))
        #
        # # classifPath = os.path.join(os.path.join("Utils","Classification"),"classifSettings")
        self.classificationData = self.DeserializeClassificationData()

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
        self.widget.createContextCursor([self.actionCopy, self.actionCut, self.actionPaste, separator,
                                         self.actionNegative_Values, self.actionPositive_Values, self.actionChange_Sign,
                                         separator2,
                                         self.action_Reverse, self.actionSilence, self.actionInsert_Silence, separator3,
                                         self.actionZoom_Cursor, self.actionPointer_Cursor,
                                         self.actionRectangular_Cursor, self.actionRectangular_Eraser, separator4,
                                         self.actionOsc_Image, self.actionSpecgram_Image, self.actionCombined_Image])

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
        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
            unicode(self.tr(u'Frequency(kHz)'))).param(unicode(self.tr(u'Min').setValue(min)))
        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
            unicode(self.tr(u'Frequency(kHz)'))).param(unicode(self.tr(u'Max').setValue(max)))

    def changeAmplitude(self, min, max):
        self.ParamTree.param(unicode(self.tr(u'Oscillogram Settings'))).param(unicode(self.tr(u'Amplitude(%)'))).param(
            unicode(self.tr(u'Min'))).setValue(min)
        self.ParamTree.param(unicode(self.tr(u'Oscillogram Settings'))).param(unicode(self.tr(u'Amplitude(%)'))).param(
            unicode(self.tr(u'Max'))).setValue(max)

    def folderFiles(self, folder, extensions=None):
        files = []
        extensions = [".wav"] if extensions is None else extensions
        for root, dirs, filenames in os.walk(folder):
            for f in filenames:
                if extensions is None or any([f.endswith(x) for x in extensions]):
                    files.append(unicode(root + os.path.sep + f))

        return files

    def updateStatusBar(self, line):
        self.statusbar.showMessage(line)

    def on_load(self):
        self.widget.visibleOscilogram = True
        self.widget.visibleSpectrogram = True
        self.widget.specgramSettings.NFFT = self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
            unicode(self.tr(u'FFT size'))).value()
        self.widget.specgramSettings.overlap = self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
            unicode(self.tr(u'FFT overlap'))).value()
        p = os.path.join(os.path.join(u"Utils", u"Didactic Signals"), u"duetto.wav")

        if os.path.exists(p):
            self.widget.open(p)
            self.actionSignalName.setText(self.tr(u"File Name:") + u" " + self.widget.signalName())
        else:
            self.widget.openNew(44100, 16, 5., whiteNoise=False)
            self.actionSignalName.setText(self.tr(u"File Name: Welcome to duetto"))

        self.setWindowTitle(self.tr(u"Duetto Sound Lab - Welcome to Duetto"))
        self.statusbar.showMessage(self.tr(u"Welcome to Duetto Sound Lab."))
        self.widget.load_Theme(self.defaultTheme)

    def updateRegionTheme(self):
        reg = self.hist.item.region.getRegion()
        valueMin = self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
            unicode(self.tr(u'Threshold(dB)'))).param(unicode(self.tr(u'Min'))).value()
        valueMax = self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
            unicode(self.tr(u'Threshold(dB)'))).param(unicode(self.tr(u'Max'))).value()
        if reg[0] != valueMin:
            self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
                unicode(self.tr(u'Threshold(dB)'))).param(unicode(self.tr(u'Min'))).setValue(reg[0])
        if reg[1] != valueMax:
            self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
                unicode(self.tr(u'Threshold(dB)'))).param(unicode(self.tr(u'Max'))).setValue(reg[1])

    def SerializeTheme(self, filename):
        if filename:
            self.defaultTheme.centerColor = self.ParamTree.param(unicode(self.tr(u'Detection Visual Settings'))).param(
                unicode(self.tr(u'Measurement Location'))).param(unicode(self.tr(u'Center'))).value()
            self.defaultTheme.startColor = self.ParamTree.param(unicode(self.tr(u'Detection Visual Settings'))).param(
                unicode(self.tr(u'Measurement Location'))).param(unicode(self.tr(u'Start'))).value()
            self.defaultTheme.quart1Color = self.ParamTree.param(unicode(self.tr(u'Detection Visual Settings'))).param(
                unicode(self.tr(u'Measurement Location'))).param(unicode(self.tr(u'Quartile25'))).value()
            self.defaultTheme.quart2Color = self.ParamTree.param(unicode(self.tr(u'Detection Visual Settings'))).param(
                unicode(self.tr(u'Measurement Location'))).param(unicode(self.tr(u'Quartile75'))).value()
            self.defaultTheme.endColor = self.ParamTree.param(unicode(self.tr(u'Detection Visual Settings'))).param(
                unicode(self.tr(u'Measurement Location'))).param(unicode(self.tr(u'End'))).value()
            self.defaultTheme.histRange = self.hist.item.region.getRegion()
            self.defaultTheme.colorBarState = self.hist.item.gradient.saveState()
            file = open(filename, 'wb')
            pickle.dump(self.defaultTheme, file)
            file.close()

    def DeSerializeTheme(self, filename):
        if filename and os.path.exists(filename):
            file = open(filename, 'rb')
            data = pickle.load(file)
            file.close()
            return data
        return SerializedData()

    def SerializeClassificationData(self, filename=""):
        if filename and os.path.exists(filename):
            file = open(filename, 'wb')
            pickle.dump(self.classificationData, file)
            file.close()

    def DeserializeClassificationData(self, filename=""):
        if filename and os.path.exists(filename):
            file = open(filename, 'rb')
            data = pickle.load(file)
            file.close()
            return data
        return ClassificationData()

    @pyqtSlot()
    def on_actionChangePlayStatus_triggered(self):
        self.widget.changePlayStatus()

    @pyqtSlot()
    def on_actionSave_theme_triggered(self):
        filename = QFileDialog.getSaveFileName(parent=self, caption=self.tr(u"Save Theme"),
                                               directory=os.path.join(u"Utils", u"Themes"),
                                               filter=self.tr(u"Duetto Theme Files") + u"(*.dth);;All Files (*)")
        if filename:
            self.SerializeTheme(filename)

    def updateMyTheme(self, theme):

        assert isinstance(theme, SerializedData)
        self.widget.osc_color = theme.osc_plot
        self.defaultTheme = theme
        self.widget.load_Theme(theme)
        self.hist.item.gradient.restoreState(theme.colorBarState)
        self.hist.item.region.setRegion(theme.histRange)

        self.hist.item.region.lineMoved()
        self.hist.item.region.lineMoveFinished()

        self.ParamTree.param(unicode(self.tr(u'Oscillogram Settings'))).param(unicode(self.tr(u'Grid'))).param(
            unicode(self.tr(u'X'))).setValue(theme.osc_GridX)
        self.ParamTree.param(unicode(self.tr(u'Oscillogram Settings'))).param(unicode(self.tr(u'Grid'))).param(
            unicode(self.tr(u'Y'))).setValue(theme.osc_GridY)
        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(unicode(self.tr(u'Grid'))).param(
            unicode(self.tr(u'X'))).setValue(theme.spec_GridX)
        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(unicode(self.tr(u'Grid'))).param(
            unicode(self.tr(u'Y'))).setValue(theme.spec_GridY)
        self.ParamTree.param(unicode(self.tr(u'Oscillogram Settings'))).param(
            unicode(self.tr(u'Background color'))).setValue(theme.osc_background)
        self.ParamTree.param(unicode(self.tr(u'Oscillogram Settings'))).param(unicode(self.tr(u'Plot color'))).setValue(
            theme.osc_plot)
        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
            unicode(self.tr(u'Background color'))).setValue(theme.spec_background)
        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(unicode(self.tr(u'Threshold(dB)'))).param(
            unicode(self.tr(u'Min'))).setValue(theme.histRange[0])
        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(unicode(self.tr(u'Threshold(dB)'))).param(
            unicode(self.tr(u'Max'))).setValue(theme.histRange[1])
        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
            unicode(self.tr(u'Frequency(kHz)'))).param(unicode(self.tr(u'Min'))).setValue(theme.minYSpec / 1000.0)
        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
            unicode(self.tr(u'Frequency(kHz)'))).param(unicode(self.tr(u'Max'))).setValue(theme.maxYSpec / 1000.0)
        self.ParamTree.param(unicode(self.tr(u'Oscillogram Settings'))).param(unicode(self.tr(u'Amplitude(%)'))).param(
            unicode(self.tr(u'Min'))).setValue(theme.minYOsc)
        self.ParamTree.param(unicode(self.tr(u'Oscillogram Settings'))).param(unicode(self.tr(u'Amplitude(%)'))).param(
            unicode(self.tr(u'Max'))).setValue(theme.maxYOsc)
        self.ParamTree.param(unicode(self.tr(u'Detection Visual Settings'))).param(
            unicode(self.tr(u'Measurement Location'))).param(unicode(self.tr(u'Center'))).setValue(theme.centerColor)
        self.ParamTree.param(unicode(self.tr(u'Detection Visual Settings'))).param(
            unicode(self.tr(u'Measurement Location'))).param(unicode(self.tr(u'End'))).setValue(theme.endColor)
        self.ParamTree.param(unicode(self.tr(u'Detection Visual Settings'))).param(
            unicode(self.tr(u'Measurement Location'))).param(unicode(self.tr(u'Start'))).setValue(theme.startColor)
        self.ParamTree.param(unicode(self.tr(u'Detection Visual Settings'))).param(
            unicode(self.tr(u'Measurement Location'))).param(unicode(self.tr(u'Quartile25'))).setValue(
            theme.quart1Color)
        self.ParamTree.param(unicode(self.tr(u'Detection Visual Settings'))).param(
            unicode(self.tr(u'Measurement Location'))).param(unicode(self.tr(u'Quartile75'))).setValue(
            theme.quart2Color)

    @pyqtSlot()
    def on_actionLoad_Theme_triggered(self):
        filename = QFileDialog.getOpenFileName(parent=self, directory=os.path.join(u"Utils", u"Themes"),
                                               caption=self.tr(u"Load Theme"),
                                               filter=self.tr(u"Duetto Theme Files") + u" (*.dth);;All Files (*)")
        if filename and os.path.exists(filename):
            data = self.DeSerializeTheme(filename)
            self.updateMyTheme(data)

    # region Drag and Drop file

    def dragEnterEvent(self, event):
        event.acceptProposedAction()
        self.dropchanged.emit(event.mimeData())

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        mimeData = event.mimeData()
        if len(mimeData.urls()) > 1: return
        mimeUrl = u"".join([unicode(url.path()) for url in mimeData.urls()])

        self.widget.visibleOscilogram = True
        self.widget.visibleSpectrogram = True
        path = mimeUrl[1:len(mimeUrl)]
        path_base = os.path.split(path)[0]
        self.filesInFolder = self.folderFiles(path_base)

        try:
            self.filesInFolderIndex = self.filesInFolder.index(path)
        except:
            self.filesInFolderIndex = 0 if len(self.filesInFolder) > 0 else -1

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

            if childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'FFT size')):
                self.widget.specgramSettings.NFFT = data
                self.widget.refresh(dataChanged=True, updateOscillogram=False, updateSpectrogram=True)

            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'Grid')) + u"." + unicode(self.tr(u'X')):
                self.defaultTheme.spec_GridX = data
                print("XXX")


            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'Grid')) + u"." + unicode(self.tr(u'Y')):
                self.defaultTheme.spec_GridY = data

            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'Threshold(dB)')) + u"." + unicode(self.tr(u'Min')):
                if self.hist.item.region.getRegion()[0] != data:
                    if data > self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
                            unicode(self.tr(u'Threshold(dB)'))).param(unicode(self.tr(u'Max'))).value():
                        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
                            unicode(self.tr(u'Threshold(dB)'))).param(unicode(self.tr(u'Min'))).setToDefault()
                        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
                            unicode(self.tr(u'Threshold(dB)'))).param(unicode(self.tr(u'Min'))).show()
                        return
                    self.hist.item.region.setRegion([data, self.hist.item.region.getRegion()[1]])
                    self.hist.item.region.lineMoved()
                    self.hist.item.region.lineMoveFinished()

            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'Threshold(dB)')) + u"." + unicode(self.tr(u'Max')):
                if self.hist.item.region.getRegion()[1] != data:
                    if data < self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
                            unicode(self.tr(u'Threshold(dB)'))).param(unicode(self.tr(u'Min'))).value():
                        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
                            unicode(self.tr(u'Threshold(dB)'))).param(unicode(self.tr(u'Max'))).setToDefault()
                        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
                            unicode(self.tr(u'Threshold(dB)'))).param(unicode(self.tr(u'Max'))).setValue()
                        return
                    self.hist.item.region.setRegion([self.hist.item.region.getRegion()[0], data])
                    self.hist.item.region.lineMoved()
                    self.hist.item.region.lineMoveFinished()

            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'FFT window')):
                self.widget.specgramSettings.window = data
                self.widget.refresh(dataChanged=True, updateOscillogram=False, updateSpectrogram=True)

            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'Background color')):
                self.defaultTheme.spec_background = data

            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'ColorMap')):
                self.widget.axesSpecgram.getHistogramWidget().item._pixelVectorCache.append(data)

            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'Frequency(kHz)')) + u"." + \
                    unicode(self.tr(u'Min')):
                self.defaultTheme.minYSpec = data

            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'Frequency(kHz)')) + u"." + \
                    unicode(self.tr(u'Max')):
                self.defaultTheme.maxYSpec = data

            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'FFT overlap')):
                self.widget.specgramSettings.overlap = data
                self.widget.refresh(dataChanged=True, updateOscillogram=False, updateSpectrogram=True)

            elif childName == unicode(self.tr(u'Power Spectrum Settings')) + u"." +\
                    unicode(self.tr(u'FFT size')):
                self.NFFT_pow = data

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Background color')):
                self.defaultTheme.osc_background = data

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Grid')) + u"." +\
                    unicode(self.tr(u'X')):
                self.defaultTheme.osc_GridX = data

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Grid')) + u"." +\
                    unicode(self.tr(u'Y')):
                self.defaultTheme.osc_GridY = data

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Plot color')):
                self.defaultTheme.osc_plot = data
                self.widget.osc_color = data
                self.widget.refresh(dataChanged=True, updateOscillogram=True, updateSpectrogram=False)
                return

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Amplitude(%)')) + u"." +\
                    unicode(self.tr(u'Min')):
                self.defaultTheme.minYOsc = data

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Amplitude(%)')) + u"." +\
                    unicode(self.tr(u'Max')):
                self.defaultTheme.maxYOsc = data

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Connect Lines')):
                self.widget.lines = data
                self.widget.refresh(dataChanged=True, updateOscillogram=True, updateSpectrogram=False)
                return

            elif childName == unicode(self.tr(u'Themes')) + u"." + \
                    unicode(self.tr(u'Theme Selected')):
                self.updateMyTheme(self.DeSerializeTheme(data))

            self.widget.load_Theme(self.defaultTheme)
            #print('  parameter: %s' % childName)
            #print('  change:    %s' % change)
            #print('  data:      %s' % unicode(data))
            #print('  ----------')


    @pyqtSlot()
    def on_actionSegmentation_And_Clasification_triggered(self):
        self.defaultTheme.centerColor = self.ParamTree.param(unicode(self.tr(u'Detection Visual Settings'))).param(
            unicode(self.tr(u'Measurement Location'))).param(unicode(self.tr(u'Center'))).value()
        self.defaultTheme.startColor = self.ParamTree.param(unicode(self.tr(u'Detection Visual Settings'))).param(
            unicode(self.tr(u'Measurement Location'))).param(unicode(self.tr(u'Start'))).value()
        self.defaultTheme.quart1Color = self.ParamTree.param(unicode(self.tr(u'Detection Visual Settings'))).param(
            unicode(self.tr(u'Measurement Location'))).param(unicode(self.tr(u'Quartile25'))).value()
        self.defaultTheme.quart2Color = self.ParamTree.param(unicode(self.tr(u'Detection Visual Settings'))).param(
            unicode(self.tr(u'Measurement Location'))).param(unicode(self.tr(u'Quartile75'))).value()
        self.defaultTheme.endColor = self.ParamTree.param(unicode(self.tr(u'Detection Visual Settings'))).param(
            unicode(self.tr(u'Measurement Location'))).param(unicode(self.tr(u'End'))).value()
        f, t = self.widget.getIndexFromAndTo()
        signal = WavFileSignal(samplingRate=self.widget.signalProcessor.signal.samplingRate,
                               bitDepth=self.widget.signalProcessor.signal.bitDepth, whiteNoise=False)
        signal.name = self.widget.signalName()
        if t > f:
            signal.data = self.widget.signalProcessor.signal.data[f:t]

        segWindow = SegmentationAndClasificationWindow(parent=self, signal=signal,
                                                       classifcationSettings=self.classificationData)
        if not segWindow.rejectSignal:
            segWindow.widget.maxYOsc = self.ParamTree.param(unicode(self.tr(u'Oscillogram Settings'))).param(
                unicode(self.tr(u'Amplitude(%)'))).param(unicode(self.tr(u'Max'))).value()
            segWindow.widget.minYOsc = self.ParamTree.param(unicode(self.tr(u'Oscillogram Settings'))).param(
                unicode(self.tr(u'Amplitude(%)'))).param(unicode(self.tr(u'Min'))).value()
            segWindow.widget.minYSpc = self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
                unicode(self.tr(u'Frequency(kHz)'))).param(unicode(self.tr(u'Min'))).value()
            segWindow.widget.maxYSpc = self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
                unicode(self.tr(u'Frequency(kHz)'))).param(unicode(self.tr(u'Max'))).value()

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
        resamplingDialog.label.setText(self.tr(u"Select the new Sampling Rate."))
        resamplingDialog.insertSpinBox.setValue(self.widget.signalProcessor.signal.samplingRate)
        if resamplingDialogWindow.exec_():
            val = resamplingDialog.insertSpinBox.value()
            if val > MIN_SAMPLING_RATE and val < MAX_SAMPLING_RATE:
                self.widget.undoRedoManager.addAction(ResamplingAction(self.widget.signalProcessor.signal, val))
                self.widget.resampling(val)
            else:
                if val < MIN_SAMPLING_RATE:
                    QMessageBox.warning(QMessageBox(), self.tr(u"Error"),
                                        self.tr(u"Sampling rate should be greater than") + u" " + unicode(
                                            MIN_SAMPLING_RATE))
                elif val > MAX_SAMPLING_RATE:
                    QMessageBox.warning(QMessageBox(), self.tr(u"Error"),
                                        self.tr(u"Sampling rate should be less than") + u" " + unicode(
                                            MAX_SAMPLING_RATE))

    @pyqtSlot()
    def on_actionCut_triggered(self):
        start, end = self.widget.getIndexFromAndTo()
        self.widget.undoRedoManager.addAction(CutAction(self.widget.signalProcessor.signal, start, end))
        self.widget.cut()

    @pyqtSlot()
    def on_actionPositive_Values_triggered(self):
        start, end = self.widget.getIndexFromAndTo()
        self.widget.undoRedoManager.addAction(Absolute_ValuesAction(self.widget.signalProcessor.signal, start, end, 1))
        self.widget.absoluteValue(1)
        self.hist.item.region.lineMoved()
        self.hist.item.region.lineMoveFinished()

    @pyqtSlot()
    def on_actionChange_Sign_triggered(self):
        start, end = self.widget.getIndexFromAndTo()
        self.widget.undoRedoManager.addAction(ChangeSignAction(self.widget.signalProcessor.signal, start, end))
        self.widget.changeSign()
        self.hist.item.region.lineMoved()
        self.hist.item.region.lineMoveFinished()

    @pyqtSlot()
    def on_actionNegative_Values_triggered(self):
        start, end = self.widget.getIndexFromAndTo()
        self.widget.undoRedoManager.addAction(Absolute_ValuesAction(self.widget.signalProcessor.signal, start, end, -1))
        self.widget.absoluteValue(-1)
        self.hist.item.region.lineMoved()
        self.hist.item.region.lineMoveFinished()

    @pyqtSlot()
    def on_actionCopy_triggered(self):
        self.widget.copy()

    @pyqtSlot()
    def on_actionPaste_triggered(self):
        start, _ = self.widget.getIndexFromAndTo()
        self.widget.undoRedoManager.addAction(
            PasteAction(self.widget.signalProcessor.signal, start, self.widget.editionSignalProcessor.clipboard))
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
                fade = u"IN" if scaleDialog.rbuttonFadeIn.isChecked() else (
                    u"OUT" if scaleDialog.rbuttonFadeOut.isChecked() else "")
                if fade == "":
                    return
            start, end = self.widget.getIndexFromAndTo()
            self.widget.undoRedoManager.addAction(
                ScaleAction(self.widget.signalProcessor.signal, start, end, factor, function, fade))
            self.widget.scale(factor, function, fade)

    @pyqtSlot()
    def on_actionInsert_Silence_triggered(self):
        silenceDialog = sdialog.Ui_Dialog()
        silenceDialogWindow = InsertSilenceDialog(self)
        silenceDialog.setupUi(silenceDialogWindow)
        if silenceDialogWindow.exec_():
            start, end = self.widget.getIndexFromAndTo()
            ms = silenceDialog.insertSpinBox.value()
            self.widget.undoRedoManager.addAction(InsertSilenceAction(self.widget.signalProcessor.signal, start, ms))
            self.widget.insertSilence(ms)

    @pyqtSlot()
    def on_actionGenerate_Pink_Noise_triggered(self):
        whiteNoiseDialog = sdialog.Ui_Dialog()
        whiteNoiseDialogWindow = InsertSilenceDialog(self)
        whiteNoiseDialog.setupUi(whiteNoiseDialogWindow)
        whiteNoiseDialog.label.setText(self.tr(u"Select the duration in ms") + " \n" + self.tr(u"of the Pink Noise."))
        whiteNoiseDialog.insertSpinBox.setValue(1000)
        if whiteNoiseDialogWindow.exec_():
            type_, Fc, Fl, Fu = self.filter_helper()
            if type_ != None:
                ms = whiteNoiseDialog.insertSpinBox.value()
                start, _ = self.widget.getIndexFromAndTo()
                self.widget.undoRedoManager.addAction(
                    GeneratePinkNoiseAction(self.widget.signalProcessor.signal, start, ms, type_, Fc, Fl, Fu))
                self.widget.insertPinkNoise(ms, type_, Fc, Fl, Fu)

    @pyqtSlot()
    def on_actionGenerate_White_Noise_triggered(self):
        whiteNoiseDialog = sdialog.Ui_Dialog()
        whiteNoiseDialogWindow = InsertSilenceDialog(self)
        whiteNoiseDialog.setupUi(whiteNoiseDialogWindow)
        whiteNoiseDialog.label.setText(self.tr(u"Select the duration in ms") + u" \n" + self.tr(u"of the white noise."))
        whiteNoiseDialog.insertSpinBox.setValue(1000)
        if whiteNoiseDialogWindow.exec_():
            ms = whiteNoiseDialog.insertSpinBox.value()
            start, end = self.widget.getIndexFromAndTo()
            self.widget.undoRedoManager.addAction(
                GenerateWhiteNoiseAction(self.widget.signalProcessor.signal, start, ms))
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
            start, end = self.widget.getIndexFromAndTo()
            self.widget.undoRedoManager.addAction(
                FilterAction(self.widget.signalProcessor.signal, start, end, type_, Fc, Fl, Fu))
            self.widget.filter(type_, Fc, Fl, Fu)

    @pyqtSlot()
    def on_actionSilence_triggered(self):
        start, end = self.widget.getIndexFromAndTo()
        self.widget.undoRedoManager.addAction(SilenceAction(self.widget.signalProcessor.signal, start, end))
        self.widget.silence()

    @pyqtSlot()
    def on_actionNormalize_triggered(self):
        self.widget.undoRedoManager.addAction(UndoRedoAction(self.widget.normalizeUndoAction, self.widget.normalize))
        self.widget.normalize()

    @pyqtSlot()
    def on_actionFull_Screen_triggered(self):
        if self.actionFull_Screen.isChecked():
            self.showFullScreen()
        else:
            self.showNormal()

    @pyqtSlot()
    def on_action_Reverse_triggered(self):
        start, end = self.widget.getIndexFromAndTo()
        self.widget.undoRedoManager.addAction(ReverseAction(self.widget.signalProcessor.signal, start, end))
        self.widget.reverse()

    def updatePowSpecWin(self):
        for win in self.pow_spec_windows:
            win.updatePowSpectrumInterval([self.widget.zoomCursor.min, self.widget.zoomCursor.max])

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
        dg_pow_spec = PowerSpectrumWindow(self, self.pow_spec_lines, self.widget.signalProcessor.signal.data,
                                          [self.widget.zoomCursor.min, self.widget.zoomCursor.max],
                                          self.widget.specgramSettings.NFFT, self.defaultTheme,
                                          self.widget.signalProcessor.signal.samplingRate,
                                          self.widget.signalProcessor.signal.bitDepth,
                                          self.widget.updateBothZoomRegions)
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

    def closeEvent(self, event):
        # self.SerializeClassificationData(os.path.join(os.path.join("Utils","Classification"),"classifSettings"))
        print(self.widget.undoRedoManager.count())
        if self.widget.undoRedoManager.count() > 0:
            self._save(event)
        self.close()

    def _save(self, event=None):
        mbox = QtGui.QMessageBox(QtGui.QMessageBox.Question, self.tr(u"Save"),
                                 self.tr(u"Do you want to save the signal?"),
                                 QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel, self)
        result = mbox.exec_()
        if self.widget.undoRedoManager.count() > 0 and result == QtGui.QMessageBox.Yes:
            self.on_actionSave_triggered()
        elif result == QtGui.QMessageBox.Cancel and event is not None:
            event.ignore()

    @pyqtSlot()
    def on_actionNew_triggered(self):
        nfd = NewFileDialog(parent=self)
        if nfd.exec_():
            self.widget.specgramSettings.NFFT = self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
                unicode(self.tr(u'FFT size'))).value()
            self.widget.specgramSettings.overlap = self.ParamTree.param(
                unicode(self.tr(u'Spectrogram Settings'))).param(unicode(self.tr(u'FFT overlap'))).value()
            self.widget.openNew(nfd.SamplingRate, nfd.BitDepth, nfd.Duration, nfd.WhiteNoise)
            self.setWindowTitle(self.tr(u"Duetto Sound Lab - ") + self.widget.signalName())
            self.actionSignalName.setText(self.tr(u"File Name: ") + self.widget.signalName())

            self.actionCombined.setEnabled(True)
            self.actionSpectogram.setEnabled(True)

    @pyqtSlot()
    def on_actionOpen_triggered(self):
        f = QFileDialog.getOpenFileName(self, self.tr(u"Select a file to open"), directory=self.lastopen,
                                        filter=self.tr(u"Wave Files") + u"(*.wav);;All Files(*)")
        self._open(unicode(f))
        for win in self.pow_spec_windows: win.close()
        self.pow_spec_windows = []

    @pyqtSlot()
    def on_actionClose_triggered(self):
        self._save()
        self.on_load()

    def _open(self, f=''):
        self.actionCombined.setEnabled(True)
        self.actionSpectogram.setEnabled(True)

        if self.widget.signalProcessor.signal is not None and self.widget.signalProcessor.signal.playStatus == WavFileSignal.RECORDING:
            self.actionZoom_out.setEnabled(True)
            self.actionZoom_out_entire_file.setEnabled(True)
            self.actionZoomIn.setEnabled(True)
            self.actionPause_Sound.setEnabled(True)
            self.actionPlay_Sound.setEnabled(True)

        if f != u'':
            try:
                self.lastopen = f
                self.widget.specgramSettings.NFFT = self.ParamTree.param(
                    unicode(self.tr(u'Spectrogram Settings'))).param(unicode(self.tr(u'FFT size'))).value()
                self.widget.specgramSettings.overlap = self.ParamTree.param(
                    unicode(self.tr(u'Spectrogram Settings'))).param(unicode(self.tr(u'FFT overlap'))).value()
                path_base = os.path.split(f)[0]
                self.filesInFolder = self.folderFiles(path_base)

                try:
                    self.filesInFolderIndex = self.filesInFolder.index(f)
                except:
                    self.filesInFolderIndex = 0 if len(self.filesInFolder) > 0 else -1

                self.widget.visibleSpectrogram = True  # for restore the state lose in load
                self.widget.open(f)
                self.setWindowTitle(self.tr(u"Duetto Sound Lab - ") + self.widget.signalName())
                self.actionSignalName.setText(self.tr(u"File Name: ") + self.widget.signalName())
            except:
                QMessageBox.warning(QMessageBox(), self.tr(u"Error"), self.tr(u"Could not load the file.") + u"\n" + f)
                self.widget.openNew(44100, 16, 1)

            valuemin = 0
            valuemax = self.widget.signalProcessor.signal.samplingRate / 2000

            self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
                unicode(self.tr(u'Frequency(kHz)'))).param(unicode(self.tr(u'Min'))).setValue(valuemin)
            self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
                unicode(self.tr(u'Frequency(kHz)'))).param(unicode(self.tr(u'Max'))).setDefault(valuemax)
            self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
                unicode(self.tr(u'Frequency(kHz)'))).param(unicode(self.tr(u'Max'))).setValue(valuemax)

            self.actionPointer_Cursor.setChecked(False)
            self.actionRectangular_Cursor.setChecked(False)
            self.actionZoom_Cursor.setChecked(True)
            self.actionRectangular_Eraser.setChecked(False)

    @pyqtSlot()
    def on_actionFile_Up_triggered(self):
        if self.filesInFolderIndex > 0:
            self.filesInFolderIndex -= 1
            if os.path.exists(self.filesInFolder[self.filesInFolderIndex]):
                self._open(self.filesInFolder[self.filesInFolderIndex])


    @pyqtSlot()
    def on_actionFile_Down_triggered(self):
        if self.filesInFolderIndex < len(self.filesInFolder) - 1:
            self.filesInFolderIndex += 1
            if os.path.exists(self.filesInFolder[self.filesInFolderIndex]):
                self._open(self.filesInFolder[self.filesInFolderIndex])


    @pyqtSlot()
    def on_actionSave_triggered(self):
        fname = unicode(QFileDialog.getSaveFileName(self, self.tr(u"Save signal"), self.widget.signalName(), u"*.wav"))
        if fname:
            self.widget.save(fname)

    @pyqtSlot()
    def on_actionSave_selected_interval_as_triggered(self):
        fname = unicode(QFileDialog.getSaveFileName(self, self.tr(u"Save signal"),
                                                    self.tr(u"Selection-") + self.widget.signalName(), u"*.wav"))
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
        self.widget.visibleOscilogram = True
        self.widget.visibleSpectrogram = True
        self.widget.refresh()
        self.hist.item.region.lineMoved()
        self.hist.item.region.lineMoveFinished()

    @pyqtSlot()
    def on_actionSpectogram_triggered(self):
        self.widget.visibleOscilogram = False
        self.widget.visibleSpectrogram = True
        self.widget.refresh(updateOscillogram=False)
        self.hist.item.region.lineMoved()
        self.hist.item.region.lineMoveFinished()

    @pyqtSlot()
    def on_actionOscilogram_triggered(self):
        self.widget.visibleOscilogram = True
        self.widget.visibleSpectrogram = False
        self.widget.refresh(updateSpectrogram=False)

    @pyqtSlot()
    def on_actionOsc_Image_triggered(self):
        if self.widget.visibleOscilogram:
            self.saveImage(self.widget.axesOscilogram, self.tr(u"oscilogram"))
        else:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"),
                                      self.tr(u"The Oscilogram plot widget is not visible.") + u"\n" + self.tr(
                                          u"You should see the data that you are going to save."))

    @pyqtSlot()
    def on_actionCombined_Image_triggered(self):
        if self.widget.visibleOscilogram and self.widget.visibleSpectrogram:
            self.saveImage(self.widget, self.tr(u"graph"))
        else:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"),
                                      self.tr(u"One of the plot widgets is not visible.") + " \n" + self.tr(
                                          u"You should see the data that you are going to save."))

    @pyqtSlot()
    def on_actionFull_Screen_triggered(self):
        if self.actionFull_Screen.isChecked():
            self.showFullScreen()
        else:
            self.showNormal()

    @pyqtSlot()
    def on_actionSpecgram_Image_triggered(self):
        if self.widget.visibleSpectrogram:
            self.saveImage(self.widget.axesSpecgram, self.tr(u"specgram"))
        else:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"),
                                      self.tr(u"The Espectrogram plot widget is not visible.") + " \n" + self.tr(
                                          u"You should see the data that you are going to save."))

    def saveImage(self, widget, text=""):
        fname = unicode(QFileDialog.getSaveFileName(self, self.tr(u"Save ") + text + self.tr(u" as an Image "),
                                                    unicode(self.widget.signalName()) + u"-" + text + self.tr(
                                                        u"-Duetto-Image"), u"*.jpg"))
        if fname:
            #save as image
            image = QtGui.QPixmap.grabWindow(widget.winId())
            image.save(fname, u'jpg')

    @pyqtSlot()
    def on_actionSaveColorBar_triggered(self):
        state = self.widget.axesSpecgram.getHistogramWidget().item.gradient.saveState()
        path = QtGui.QFileDialog.getSaveFileName(self, self.tr(u"Save Color Bar"),
                                                 filter=self.tr(u"Bar Files") + u"(*.bar);;All Files (*)")
        if path != u"":
            fh = open(path, 'w')
            fh.write(state.__repr__())
            fh.close()

    @pyqtSlot()
    def on_actionLoadColorBar_triggered(self):
        path = QtGui.QFileDialog.getOpenFileName(self, self.tr(u"Load Color Bar"),
                                                 filter=self.tr(u"Bar Files") + u"(*.bar);;All Files (*)")
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
                                   u'1x': 100, u'2x': 200, u'4x': 400, u'8x': 800}[unicode(action.text())]
