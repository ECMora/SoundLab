# -*- coding: utf-8 -*-
import os
import pickle
from PyQt4 import QtCore, QtGui
from pyqtgraph.parametertree.parameterTypes import ListParameter
from pyqtgraph.parametertree import Parameter, ParameterTree
from PyQt4.QtGui import QDialog, QMessageBox, QFileDialog, QActionGroup, QAction
from PyQt4.QtCore import pyqtSlot
from Utils.Utils import saveImage, folderFiles
from graphic_interface.windows.ParameterList import DuettoListParameterItem
from graphic_interface.dialogs.NewFileDialog import NewFileDialog
from graphic_interface.windows.PowerSpectrumWindow import PowerSpectrumWindow
from SegmentationAndClasificationWindow import SegmentationAndClasificationWindow
from graphic_interface.widgets.undo_redo_actions.UndoRedoActions import *
from MainWindow import Ui_DuettoMainWindow
from graphic_interface.dialogs import InsertSilenceDialog as sdialog, FilterOptionsDialog as filterdg, \
    ChangeVolumeDialog as cvdialog
from graphic_interface.windows.WorkTheme import SerializedData
from sound_lab_core.Clasification.ClassificationData import ClassificationData
from duetto.dimensional_transformations.two_dimensional_transforms.Spectrogram.WindowFunctions import WindowFunction
from duetto.audio_signals.Synthesizer import Synthesizer
from graphic_interface.widgets.signal_visualizer_tools.SignalVisualizerTool import Tools


class InsertSilenceDialog(sdialog.Ui_Dialog, QDialog):
    pass


class ChangeVolumeDialog(cvdialog.Ui_Dialog, QDialog):
    pass


class FilterDialog(filterdg.Ui_Dialog, QDialog):
    pass


class DuettoSoundLabWindow(QtGui.QMainWindow, Ui_DuettoMainWindow):
    """
    Main window of the application.
    """

    # SIGNALS
    #signal raised when a file is drop into the window
    dropchanged = QtCore.pyqtSignal(QtCore.QMimeData)

    #CONSTANTS
    #minimum and maximum sampling rate used on the application
    MIN_SAMPLING_RATE = 1000
    MAX_SAMPLING_RATE = 2000000

    #Width and height of the dock window of visual options
    SETTINGS_WINDOW_WIDTH = 340
    SETTINGS_WINDOW_HEIGHT = 100

    def __init__(self, parent=None):
        super(DuettoSoundLabWindow, self).__init__(parent)
        self.setupUi(self)

        #theme for the visual options
        theme_path = os.path.join(os.path.join("Utils", "Themes"), "RedBlackTheme.dth")
        self.defaultTheme = self.DeSerializeTheme(theme_path)

        #get all the themes that are in the static folder for themes ("Utils\Themes\")
        themesInFolder = folderFiles(os.path.join("Utils", "Themes"), extensions=[".dth"])

        #get the histogram object of the spectrogram widget.
        #this histogram would be visualized outside the spectrogram widget for best
        #user interaction
        self.hist = self.widget.axesSpecgram.histogram
        self.hist.setFixedWidth(self.SETTINGS_WINDOW_WIDTH)
        self.hist.setFixedHeight(self.SETTINGS_WINDOW_HEIGHT)
        self.hist.item.gradient.restoreState(self.defaultTheme.colorBarState)
        self.hist.item.region.setRegion(self.defaultTheme.histRange)
        self.hist.item.region.sigRegionChanged.connect(self.updateRegionTheme)

        #TODO rearrange this visual options that must be inside the theme
        self.pow_spec_lines = True
        self.pow_spec_maxY = 5
        self.pow_spec_minY = -50
        self.widget.lines = True
        self.NFFT_pow = 512

        #the path to the last opened file signal
        self.last_opened_signal_path = ''

        #get the status bar to show messages to the user
        self.statusbar = self.statusBar()
        self.statusbar.setSizeGripEnabled(False)
        self.statusbar.showMessage(self.tr(u"Welcome to Duetto Sound Lab"), 5000)
        self.widget.toolDataDetected.connect(self.updateStatusBar)

        #user interface to manipulate several visual parameters
        #and display options of the application theme.
        #Is used a parameter tree to present to the user the visual options

        #region Parameter Tree definition

        params = [
            {u'name': unicode(self.tr(u'Oscillogram Settings')), u'type': u'group', u'children': [
                {u'name': unicode(self.tr(u'Amplitude(%)')), u'type': u'group', u'children': [
                    {u'name': unicode(self.tr(u'Min')), u'type': u'float', u'value': -100, u'step': 2},
                    {u'name': unicode(self.tr(u'Max')), u'type': u'float', u'value': 100, u'step': 2},
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
                 u'value': self.widget.axesSpecgram.specgramHandler.window, u'default': self.widget.axesSpecgram.specgramHandler.window,
                 u'values': [(u'Bartlett', WindowFunction.Bartlett),
                             (u"Blackman", WindowFunction.Blackman),
                             (u"Hamming",  WindowFunction.Hamming),
                             (u"Hanning",  WindowFunction.Hanning),
                             (u'Kaiser',  WindowFunction.Kaiser),
                             (unicode(self.tr(u'None')), WindowFunction.WindowNone),
                             (u"Rectangular", WindowFunction.Rectangular)]},
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
                                                                themesInFolder[0].rfind(os.path.sep) + 1
                                                                :themesInFolder[0].rfind(".dth")],
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
        #change the item class of the list parameter type to allow order in the children params added
        ListParameter.itemClass = DuettoListParameterItem

        #create the tree,  and connect
        self.ParamTree = Parameter.create(name=u'params', type=u'group', children=params)
        self.ParamTree.sigTreeStateChanged.connect(self.change)
        parameterTree = ParameterTree()
        parameterTree.setAutoScroll(True)
        parameterTree.setFixedWidth(self.SETTINGS_WINDOW_WIDTH)
        parameterTree.setHeaderHidden(True)
        parameterTree.setParameters(self.ParamTree, showTop=False)

        #endregion

        #set the vertical layout of the visual options window with the
        # param tree and the histogram color bar
        layout = QtGui.QVBoxLayout()
        layout.setMargin(0)
        layout.addWidget(parameterTree)
        layout.addWidget(self.hist)

        self.osc_settings_contents.setLayout(layout)
        self.dock_settings.setVisible(False)
        self.dock_settings.setFixedWidth(self.SETTINGS_WINDOW_WIDTH)

        #get the clasification data stored
        #classifPath = os.path.join(os.path.join("Utils","Classification"),"classifSettings")
        self.classificationData = self.DeserializeClassificationData()

        #variables to handle the navigation across the signal files of one folder
        #to allow to open all the files in the folder user friendly by action up/down next file
        self.filesInFolder = []
        self.filesInFolderIndex = -1

        #the list of one dimensional processing windows opened by the user.
        self.one_dim_windows = []

        #accept drops to open signals by drop
        self.setAcceptDrops(True)

        #create the separators for the context menu
        separator, separator2, separator3, separator4 = QtGui.QAction(self), QtGui.QAction(self), QtGui.QAction(self), QtGui.QAction(self)
        separator.setSeparator(True)
        separator2.setSeparator(True)
        separator3.setSeparator(True)
        separator4.setSeparator(True)

        #include the context menu actions into the widget
        self.widget.createContextCursor([self.actionCopy,
                                         self.actionCut,
                                         self.actionPaste,
                                         separator,
                                         self.actionNegative_Values,
                                         self.actionPositive_Values,
                                         self.actionChange_Sign,
                                         separator2,
                                         self.action_Reverse,
                                         self.actionSilence,
                                         self.actionInsert_Silence,
                                         separator3,
                                         self.actionZoom_Cursor,
                                         self.actionPointer_Cursor,
                                         self.actionRectangular_Cursor,
                                         self.actionRectangular_Eraser,
                                         separator4,
                                         self.actionOsc_Image,
                                         self.actionSpecgram_Image,
                                         self.actionCombined_Image
                                        ])
        #set a name for the default signal
        #action signal is a place in the tool bar to show the current signal name
        self.actionSignalName.setText("")

        #set the action group to change
        playSpeedActionGroup = QActionGroup(self)
        playSpeedActionGroup.addAction(self.action1_8x)
        playSpeedActionGroup.addAction(self.action1_4x)
        playSpeedActionGroup.addAction(self.action1_2x)
        playSpeedActionGroup.addAction(self.action1x)
        playSpeedActionGroup.addAction(self.action2x)
        playSpeedActionGroup.addAction(self.action4x)
        playSpeedActionGroup.addAction(self.action8x)
        playSpeedActionGroup.triggered.connect(self.on_playSpeedChanged_triggered)

        self.on_load()

    #region Segmentation And Clasification

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
        signal = self.widget.signal
        if t > f:
            signal = signal.copy(f, t)


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
            segWindow.widget.graph()

        self.widget.undoRedoManager.clear()

    #endregion

    #region Theme

    @pyqtSlot()
    def on_actionSave_theme_triggered(self):
        filename = QFileDialog.getSaveFileName(parent=self, caption=self.tr(u"Save Theme"),
                                               directory=os.path.join(u"Utils", u"Themes"),
                                               filter=self.tr(u"Duetto Theme Files") + u"(*.dth);;All Files (*)")
        if filename:
            self.SerializeTheme(filename)

    def updateMyTheme(self, theme):
        assert isinstance(theme, SerializedData)
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

    def DeSerializeTheme(self, filename):
        if filename and os.path.exists(filename):
            file = open(filename, 'rb')
            data = pickle.load(file)
            file.close()
            return data
        return SerializedData()

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

    def change(self, param, changes):
        """

        :param param:
        :param changes:
        :return:
        """
        for param, change, data in changes:
            path = self.ParamTree.childPath(param)
            if path is not None:
                childName = '.'.join(path)
            else:
                childName = param.name()

            if childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'FFT size')):
                self.widget.axesSpecgram.specgramHandler.NFFT = data
                self.widget.graph()

            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'Grid')) + u"." + unicode(self.tr(u'X')):
                self.defaultTheme.spec_GridX = data

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
                self.widget.axesSpecgram.specgramHandler.window = data
                self.widget.graph()

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
                self.widget.axesSpecgram.specgramHandler.overlap = data
                self.widget.graph()

            elif childName == unicode(self.tr(u'Power Spectrum Settings')) + u"." + \
                    unicode(self.tr(u'FFT size')):
                self.NFFT_pow = data

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Background color')):
                self.defaultTheme.osc_background = data

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Grid')) + u"." + \
                    unicode(self.tr(u'X')):
                self.defaultTheme.osc_GridX = data

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Grid')) + u"." + \
                    unicode(self.tr(u'Y')):
                self.defaultTheme.osc_GridY = data

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Plot color')):
                self.defaultTheme.osc_plot = data

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Amplitude(%)')) + u"." + \
                    unicode(self.tr(u'Min')):
                self.defaultTheme.minYOsc = data

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Amplitude(%)')) + u"." + \
                    unicode(self.tr(u'Max')):
                self.defaultTheme.maxYOsc = data

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Connect Lines')):
                self.widget.lines = data
                self.widget.graph()
                return

            elif childName == unicode(self.tr(u'Themes')) + u"." + \
                    unicode(self.tr(u'Theme Selected')):
                self.updateMyTheme(self.DeSerializeTheme(data))

            self.widget.load_Theme(self.defaultTheme)

    #endregion

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
        self.getFolderFiles(path)
        self._open(path)
        event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        event.accept()

    #endregion

    #region Widget Tools
    @pyqtSlot()
    def on_actionZoom_Cursor_triggered(self):
        self.deselectToolsActions()
        self.actionZoom_Cursor.setChecked(True)
        self.widget.setSelectedTool(Tools.ZoomTool)

    @pyqtSlot()
    def on_actionRectangular_Cursor_triggered(self):
        self.deselectToolsActions()
        self.actionRectangular_Cursor.setChecked(True)
        self.widget.setSelectedTool(Tools.RectangularZoomTool)

    @pyqtSlot()
    def on_actionRectangular_Eraser_triggered(self):
        self.deselectToolsActions()
        self.actionRectangular_Eraser.setChecked(True)
        self.widget.setSelectedTool(Tools.RectangularEraser)

    @pyqtSlot()
    def on_actionPointer_Cursor_triggered(self):
        self.deselectToolsActions()
        self.actionPointer_Cursor.setChecked(True)
        self.widget.setSelectedTool(Tools.PointerTool)

    def deselectToolsActions(self):
        """
        Change the checked status of all the tools to False
        """
        self.actionZoom_Cursor.setChecked(False)
        self.actionRectangular_Cursor.setChecked(False)
        self.actionRectangular_Eraser.setChecked(False)
        self.actionPointer_Cursor.setChecked(False)

    #endregion

    #region Cut, Copy, Paste
    @pyqtSlot()
    def on_actionCut_triggered(self):
        self.widget.cut()

    @pyqtSlot()
    def on_actionCopy_triggered(self):
        self.widget.copy()

    @pyqtSlot()
    def on_actionPaste_triggered(self):
        self.widget.paste()

    #endregion

    #region Undo Redo

    @pyqtSlot()
    def on_actionUndo_triggered(self):
        self.widget.undo()

    @pyqtSlot()
    def on_actionRedo_triggered(self):
        self.widget.redo()

    #endregion

    #region Signal Processing Methods

    @pyqtSlot()
    def on_actionPositive_Values_triggered(self):
        self.widget.absoluteValue(1)

    @pyqtSlot()
    def on_actionChange_Sign_triggered(self):
        self.widget.changeSign()

    @pyqtSlot()
    def on_actionNegative_Values_triggered(self):
        self.widget.absoluteValue(-1)

    @pyqtSlot()
    def on_actionSmart_Scale_triggered(self):
        scaleDialog = cvdialog.Ui_Dialog()
        scaleDialogWindow = ChangeVolumeDialog(self)
        scaleDialog.setupUi(scaleDialogWindow)
        if scaleDialogWindow.exec_():
            fade = u""
            factor = scaleDialog.spinboxConstValue.value()
            if scaleDialog.rbuttonConst.isChecked():
                self.widget.scale(factor)
            elif scaleDialog.rbuttonNormalize.isChecked():
                factor = scaleDialog.spinboxNormalizePercent.value()
                self.widget.normalize(factor)
            else:
                function = scaleDialog.cboxModulationType.currentText()
                fade = u"IN" if scaleDialog.rbuttonFadeIn.isChecked() else u"OUT"
                self.widget.modulate(function, fade)

    @pyqtSlot()
    def on_actionInsert_Silence_triggered(self):
        silenceDialog = sdialog.Ui_Dialog()
        silenceDialogWindow = InsertSilenceDialog(self)
        silenceDialog.setupUi(silenceDialogWindow)
        if silenceDialogWindow.exec_():
            start, end = self.widget.getIndexFromAndTo()
            ms = silenceDialog.insertSpinBox.value()
            self.widget.undoRedoManager.add(InsertSilenceAction(self.widget.signalProcessor.signal, start, ms))
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
                self.widget.undoRedoManager.add(
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
            self.widget.undoRedoManager.add(
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
            self.widget.undoRedoManager.add(
                FilterAction(self.widget.signalProcessor.signal, start, end, type_, Fc, Fl, Fu))
            self.widget.filter(type_, Fc, Fl, Fu)

    @pyqtSlot()
    def on_actionSilence_triggered(self):
        self.widget.silence()

    @pyqtSlot()
    def on_action_Reverse_triggered(self):
        self.widget.reverse()

    @pyqtSlot()
    def on_actionResampling_triggered(self):
        resamplingDialog = sdialog.Ui_Dialog()
        resamplingDialogWindow = InsertSilenceDialog(self)
        resamplingDialog.setupUi(resamplingDialogWindow)
        resamplingDialog.label.setText(self.tr(u"Select the new Sampling Rate."))
        resamplingDialog.insertSpinBox.setValue(self.widget.signalProcessor.signal.samplingRate)
        if resamplingDialogWindow.exec_():
            val = resamplingDialog.insertSpinBox.value()
            if self.MIN_SAMPLING_RATE < val < self.MAX_SAMPLING_RATE:
                self.widget.resampling(val)
            else:
                if val < self.MIN_SAMPLING_RATE:
                    QMessageBox.warning(QMessageBox(), self.tr(u"Error"),
                                        self.tr(u"Sampling rate should be greater than") + u" " + unicode(
                                            self.MIN_SAMPLING_RATE))
                elif val > self.MAX_SAMPLING_RATE:
                    QMessageBox.warning(QMessageBox(), self.tr(u"Error"),
                                        self.tr(u"Sampling rate should be less than") + u" " + unicode(
                                            self.MAX_SAMPLING_RATE))

    #endregion

    #region Zoom IN, OUT, NONE
    @pyqtSlot()
    def on_actionZoomIn_triggered(self):
        self.widget.zoomIn()

    @pyqtSlot()
    def on_actionZoom_out_triggered(self):
        self.widget.zoomOut()

    @pyqtSlot()
    def on_actionZoom_out_entire_file_triggered(self):
        self.widget.zoomNone()

    #endregion

    #region Open, Close and Save

    def on_load(self):
        self.widget.visibleOscilogram = True
        self.widget.visibleSpectrogram = True
        p = os.path.join(os.path.join(u"Utils", u"Didactic Signals"), u"duetto.wav")

        if os.path.exists(p):
            self.widget.open(p)
            self.actionSignalName.setText(self.tr(u"File Name:") + u" " + self.widget.signalName())
        else:
            signal = Synthesizer.generateSilence(44100, 16, 1)
            self.widget.signal = signal
            self.widget.graph()
            self.actionSignalName.setText(self.tr(u"File Name: Welcome to duetto"))

        #update data in the theme from the new signal
        self.changeFrequency(0, self.widget.signal.samplingRate/2000)
        self.setWindowTitle(self.tr(u"Duetto Sound Lab - Welcome to Duetto"))
        self.statusbar.showMessage(self.tr(u"Welcome to Duetto Sound Lab."))
        self.widget.load_Theme(self.defaultTheme)

    @pyqtSlot()
    def on_actionExit_triggered(self):
        self.close()

    def closeEvent(self, event):
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
            signal = Synthesizer.generateSilence(nfd.SamplingRate, nfd.BitDepth, nfd.Duration)
            self.widget.signal = signal
            self.setWindowTitle(self.tr(u"Duetto Sound Lab - ") + self.widget.signalName())
            self.actionSignalName.setText(self.tr(u"File Name: ") + self.widget.signalName())

            self.actionCombined.setEnabled(True)
            self.actionSpectogram.setEnabled(True)

    @pyqtSlot()
    def on_actionOpen_triggered(self):
        f = QFileDialog.getOpenFileName(self, self.tr(u"Select a file to open"),
                                        directory=self.last_opened_signal_path,
                                        filter=self.tr(u"Wave Files") + u"(*.wav);;All Files(*)")
        self._open(unicode(f))
        for win in self.one_dim_windows: win.close()
        self.one_dim_windows = []

    @pyqtSlot()
    def on_actionClose_triggered(self):
        self._save()
        self.on_load()

    def _open(self, f=''):
        self.actionCombined.setEnabled(True)
        self.actionSpectogram.setEnabled(True)

        if f != u'':
            try:
                self.last_opened_signal_path = f
                self.getFolderFiles(f)

                self.widget.visibleSpectrogram = True  # for restore the state lose in load
                self.widget.open(f)
                self.setWindowTitle(self.tr(u"Duetto Sound Lab - ") + self.widget.signalName())
                self.actionSignalName.setText(self.tr(u"File Name: ") + self.widget.signalName())
            except:
                QMessageBox.warning(QMessageBox(), self.tr(u"Error"), self.tr(u"Could not load the file.") + u"\n" + f)
                signal = Synthesizer.generateSilence(44100,16,1)
                self.widget.signal = signal

            self.widget.graph()


            valuemin = 0
            valuemax = self.widget.signal.samplingRate / 2000

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
    def on_actionSave_triggered(self):
        fname = unicode(QFileDialog.getSaveFileName(self, self.tr(u"Save signal"), self.widget.signalName(), u"*.wav"))
        if fname:
            self.widget.save(fname)

    @pyqtSlot()
    def on_actionSave_selected_interval_as_triggered(self):
        fname = unicode(QFileDialog.getSaveFileName(self, self.tr(u"Save signal"),
                                                    self.tr(u"Selection-") + self.widget.signalName(), u"*.wav"))
        if fname:
            self.widget.saveSelectedSectionAsSignal(fname)

    #endregion

    #region Folder Files UP and DOWN manipulation

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

    def getFolderFiles(self, path):
        try:
            path_base = os.path.split(path)[0]
            self.filesInFolder = folderFiles(path_base)
            self.filesInFolderIndex = self.filesInFolder.index(path)
        except:
            self.filesInFolderIndex = 0 if len(self.filesInFolder) > 0 else -1

    #endregion

    #region Play, Pause, Stop, Record
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
    def on_actionChangePlayStatus_triggered(self):
        self.widget.changePlayStatus()

    @pyqtSlot(QAction)
    def on_playSpeedChanged_triggered(self, action):
        self.widget.stop()
        speed = {u'1/8x': 12.5, u'1/4x': 25, u'1/2x': 50,
                                   u'1x': 100, u'2x': 200, u'4x': 400, u'8x': 800}[unicode(action.text())]
        self.widget.playSpeed = speed

    #endregion

    #region Widgets Visibility
    @pyqtSlot()
    def on_actionCombined_triggered(self):
        self.changeWidgetsVisibility(True, True)

    @pyqtSlot()
    def on_actionSpectogram_triggered(self):
        self.changeWidgetsVisibility(False, True)

    @pyqtSlot()
    def on_actionOscilogram_triggered(self):
        self.changeWidgetsVisibility(True, False)

    def changeWidgetsVisibility(self,visibleOscilogram=True, visibleSpectrogram=True):
        self.widget.visibleOscilogram = visibleOscilogram
        self.widget.visibleSpectrogram = visibleSpectrogram
        self.widget.graph()

    #endregion

    #region Save Widgets Image

    @pyqtSlot()
    def on_actionOsc_Image_triggered(self):
        if self.widget.visibleOscilogram:
            saveImage(self.widget.axesOscilogram, self.tr(u"oscilogram"))
        else:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"),
                                      self.tr(u"The Oscilogram plot widget is not visible.") + u"\n" + self.tr(
                                          u"You should see the data that you are going to save."))

    @pyqtSlot()
    def on_actionSpecgram_Image_triggered(self):
        if self.widget.visibleSpectrogram:
            saveImage(self.widget.axesSpecgram, self.tr(u"specgram"))
        else:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"),
                                      self.tr(u"The Espectrogram plot widget is not visible.") + " \n" + self.tr(
                                          u"You should see the data that you are going to save."))

    @pyqtSlot()
    def on_actionCombined_Image_triggered(self):
        if self.widget.visibleOscilogram and self.widget.visibleSpectrogram:
            saveImage(self.widget, self.tr(u"graph"))
        else:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"),
                                      self.tr(u"One of the plot widgets is not visible.") + " \n" + self.tr(
                                          u"You should see the data that you are going to save."))

    #endregion

    #region Onedimensional Transforms
    def updatePowSpecWin(self):
        for win in self.one_dim_windows:
            win.updatePowSpectrumInterval([self.widget.zoomCursor.min, self.widget.zoomCursor.max])

    @pyqtSlot()
    def on_actionPower_Spectrum_triggered(self):
        dg_pow_spec = PowerSpectrumWindow(self, self.pow_spec_lines, self.widget.signalProcessor.signal.data,
                                          [self.widget.zoomCursor.min, self.widget.zoomCursor.max],
                                          self.widget.specgramSettings.NFFT, self.defaultTheme,
                                          self.widget.signalProcessor.signal.samplingRate,
                                          self.widget.signalProcessor.signal.bitDepth,
                                          self.widget.updateBothZoomRegions)
        self.one_dim_windows.append(dg_pow_spec)

    #endregion

    #region Scroll Bar Range
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

    #endregion

    def changeFrequency(self, min, max):
        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
            unicode(self.tr(u'Frequency(kHz)'))).param(unicode(self.tr(u'Min'))).setValue(min)
        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
            unicode(self.tr(u'Frequency(kHz)'))).param(unicode(self.tr(u'Max'))).setValue(max)

    def changeAmplitude(self, min, max):
        self.ParamTree.param(unicode(self.tr(u'Oscillogram Settings'))).param(unicode(self.tr(u'Amplitude(%)'))).param(
            unicode(self.tr(u'Min'))).setValue(min)
        self.ParamTree.param(unicode(self.tr(u'Oscillogram Settings'))).param(unicode(self.tr(u'Amplitude(%)'))).param(
            unicode(self.tr(u'Max'))).setValue(max)

    def updateStatusBar(self, line):
        """
        Update the status bar window message.
        :param line: The (string) to show as message
        :return: None
        """
        self.statusbar.showMessage(line)

    @pyqtSlot()
    def on_actionFull_Screen_triggered(self):
        """
        Action that switch the window visualization state between
        Full Screen and Normal
        :return:
        """
        if self.actionFull_Screen.isChecked():
            self.showFullScreen()
        else:
            self.showNormal()

    @pyqtSlot()
    def on_actionSettings_triggered(self):
        """
        Method that switch the visibility  on the application of the
        settings window with the visual theme options
        :return:
        """
        if self.dock_settings.isVisible():
            self.dock_settings.setVisible(False)
        else:
            self.dock_settings.setVisible(True)
            self.dock_settings.setFloating(False)



