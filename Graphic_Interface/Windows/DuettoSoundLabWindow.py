# -*- coding: utf-8 -*-
import os
import pickle
from PyQt4 import QtGui

from pyqtgraph.parametertree.parameterTypes import ListParameter
from pyqtgraph.parametertree import Parameter, ParameterTree
from PyQt4.QtGui import QDialog, QMessageBox, QFileDialog, QActionGroup, QAction
from PyQt4.QtCore import pyqtSlot
from duetto.dimensional_transformations.two_dimensional_transforms.Spectrogram.WindowFunctions import WindowFunction
from duetto.audio_signals.Synthesizer import Synthesizer
from Utils.Utils import folderFiles

from graphic_interface.windows.ParameterList import DuettoListParameterItem
from graphic_interface.dialogs.NewFileDialog import NewFileDialog
from graphic_interface.windows.PowerSpectrumWindow import PowerSpectrumWindow
from SegmentationAndClasificationWindow import SegmentationAndClasificationWindow
from graphic_interface.widgets.undo_redo_actions.UndoRedoActions import *
from MainWindow import Ui_DuettoMainWindow
from graphic_interface.dialogs import InsertSilenceDialog as sdialog, FilterOptionsDialog as filterdg, \
    ChangeVolumeDialog as cvdialog
from graphic_interface.windows.WorkTheme import WorkTheme
from sound_lab_core.Clasification.ClassificationData import ClassificationData
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
        self.defaultTheme = WorkTheme()  # self.DeSerializeTheme(os.path.join("Utils", "Themes", "RedBlackTheme.dth"))

        #get all the themes that are in the static folder for themes ("Utils\Themes\")
        themesInFolder = folderFiles(os.path.join("Utils", "Themes"), extensions=[".dth"])

        #get the histogram object of the spectrogram widget.
        #this histogram would be visualized outside the spectrogram widget for best
        #user interaction
        self.hist = self.widget.axesSpecgram.histogram
        self.hist.setFixedWidth(self.SETTINGS_WINDOW_WIDTH)
        self.hist.setFixedHeight(self.SETTINGS_WINDOW_HEIGHT)
        self.hist.item.gradient.restoreState(self.defaultTheme.spectrogramTheme.colorBarState)
        self.hist.item.region.setRegion(self.defaultTheme.spectrogramTheme.histRange)
        self.hist.item.region.sigRegionChanged.connect(self.updateRegionTheme)

        #TODO rearrange this visual options that must be inside the theme
        self.pow_spec_lines = True
        self.pow_spec_maxY = 5
        self.pow_spec_minY = -50
        self.widget.lines = True
        self.NFFT_pow = 512

        #the path to the last opened file signal used to
        #give higher user friendly interaction on file search
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
                    {u'name': u'X', u'type': u'bool', u'default': self.defaultTheme.oscillogramTheme.gridX,
                     u'value': self.defaultTheme.oscillogramTheme.gridX},
                    {u'name': u'Y', u'type': u'bool', u'default': self.defaultTheme.oscillogramTheme.gridY,
                     u'value': self.defaultTheme.oscillogramTheme.gridY},

                ]},
                {u'name': unicode(self.tr(u'Background color')), u'type': u'color',
                 u'value': self.defaultTheme.oscillogramTheme.background_color,
                 u'default': self.defaultTheme.oscillogramTheme.background_color},
                {u'name': unicode(self.tr(u'Plot color')), u'type': u'color',
                 u'value': self.defaultTheme.oscillogramTheme.plot_color,
                 u'default': self.defaultTheme.oscillogramTheme.plot_color},
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
                 u'value': self.widget.axesSpecgram.specgramHandler.window,
                 u'default': self.widget.axesSpecgram.specgramHandler.window,
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
                     u'default': self.defaultTheme.spectrogramTheme.histRange[0],
                     u'value': self.defaultTheme.spectrogramTheme.histRange[0]},
                    {u'name': unicode(self.tr(u'Max')), u'type': u'float', u'step': 0.1,
                     u'default': self.defaultTheme.spectrogramTheme.histRange[1],
                     u'value': self.defaultTheme.spectrogramTheme.histRange[1]},
                ]},
                {u'name': unicode(self.tr(u'Grid')), u'type': u'group', u'children': [
                    {u'name': u'X', u'type': u'bool', u'default': self.defaultTheme.spectrogramTheme.gridX,
                     u'value': self.defaultTheme.spectrogramTheme.gridX},
                    {u'name': u'Y', u'type': u'bool', u'default': self.defaultTheme.spectrogramTheme.gridY,
                     u'value': self.defaultTheme.spectrogramTheme.gridY},

                ]},
                {u'name': unicode(self.tr(u'Background color')), u'type': u'color',
                 u'value': self.defaultTheme.spectrogramTheme.background_color,
                 u'default': self.defaultTheme.spectrogramTheme.background_color},
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
            # {u'name': unicode(self.tr(u'Detection Visual Settings')), u'type': u'group', u'children': [
            #     {u'name': unicode(self.tr(u'Measurement Location')), u'type': u'group', u'children': [
            #         {u'name': unicode(self.tr(u'Start')), u'type': u'color',
            #          u'value': self.defaultTheme.startColor,
            #          u'default': self.defaultTheme.startColor},
            #         {u'name': unicode(self.tr(u'Quartile25')), u'type': u'color',
            #          u'value': self.defaultTheme.quart1Color,
            #          u'default': self.defaultTheme.quart1Color},
            #         {u'name': unicode(self.tr(u'Center')), u'type': u'color',
            #          u'value': self.defaultTheme.centerColor,
            #          u'default': self.defaultTheme.centerColor},
            #         {u'name': unicode(self.tr(u'Quartile75')), u'type': u'color',
            #          u'value': self.defaultTheme.quart2Color,
            #          u'default': self.defaultTheme.quart2Color},
            #         {u'name': unicode(self.tr(u'End')), u'type': u'color',
            #          u'value': self.defaultTheme.endColor,
            #          u'default': self.defaultTheme.endColor},
            #     ]}]}

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
        self.hist.item.gradient.restoreState(self.defaultTheme.spectrogramTheme.colorBarState)
        self.hist.item.region.setRegion(self.defaultTheme.spectrogramTheme.histRange)

        self.osc_settings_contents.setLayout(layout)
        self.dock_settings.setVisible(False)
        self.dock_settings.setFixedWidth(self.SETTINGS_WINDOW_WIDTH)

        #get the clasification data stored
        #classifPath = os.path.join(os.path.join("Utils","Classification"),"classifSettings")
        self.classificationData = self.deserializeClassificationData()

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

        #set the action group to change the play speed of the opened signal
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

    def serializeClassificationData(self, filename=""):
        """
        Store in disc the classification data manipulated by the application
        :param filename: file path to store the data
        :return:
        """
        if filename and os.path.exists(filename):
            try:
                classif_data_file = open(filename, 'wb')
                pickle.dump(self.classificationData, classif_data_file)
                classif_data_file.close()
            except Exception as ex:
                raise ex

    def deserializeClassificationData(self, filename=""):
        """
        Get the classification data previously stored on disc
        :param filename:
        :return:
        """
        try:
            if filename and os.path.exists(filename):
                classif_data_file = open(filename, 'rb')
                data = pickle.load(classif_data_file)
                classif_data_file.close()
                return data

        except Exception as ex:
            print("Error al deserializar los datos de clasificacion. "+ex.message)
            #return a default
            return ClassificationData()

    @pyqtSlot()
    def on_actionSegmentation_And_Clasification_triggered(self):
        """
        Open the signal selected in the segmentation and classification window
        :return:
        """

        #get the signal to analyze in segmentation window
        #could be the currently visible signal or the selected by zoom tool
        indexFrom, indexTo = self.widget.getIndexFromAndTo()
        signal = self.widget.signal
        if indexTo > indexFrom:
            signal = signal.copy(indexFrom, indexTo)

        #create the window and provide it the signal
        segWindow = SegmentationAndClasificationWindow(parent=self, signal=signal,
                                                       classifcationSettings=self.classificationData)
        if segWindow.rejectSignal:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"),
                                      self.tr(u"The signal couldn't be open with for Segmentation and Classfication."))
        else:
            #if the signal is possible to process by the segmentation classification window
            #the theme is loaded and the undo redo actions in the current window are cleared.
            segWindow.load_Theme(self.defaultTheme)
            self.widget.undoRedoManager.clear()

    #endregion

    #region Theme

    @pyqtSlot()
    def on_actionSave_theme_triggered(self):
        """
        Save to disc the current theme with the visual options.
        :return:
        """
        filename = QFileDialog.getSaveFileName(parent=self, caption=self.tr(u"Save Theme"),
                                               directory=os.path.join(u"Utils", u"Themes"),
                                               filter=self.tr(u"Duetto Theme Files") + u"(*.dth);;All Files (*)")
        if filename:
            self.serializeTheme(filename)

    def updateTheme(self, theme):
        """
        Update the current selected theme with the values of the supplied new one.
        :param theme: The new Theme to load
        :return:
        """
        assert isinstance(theme, WorkTheme)
        #change the current theme
        self.defaultTheme = theme

        #update the theme in the widget
        self.widget.load_Theme(theme)
        self.hist.item.gradient.restoreState(theme.spectrogramTheme.colorBarState)
        self.hist.item.region.setRegion(theme.spectrogramTheme.histRange)
        self.hist.item.region.lineMoved()
        self.hist.item.region.lineMoveFinished()

        self.ParamTree.param(unicode(self.tr(u'Oscillogram Settings'))).param(unicode(self.tr(u'Grid'))).param(
            unicode(self.tr(u'X'))).setValue(theme.oscillogramTheme.gridX)
        self.ParamTree.param(unicode(self.tr(u'Oscillogram Settings'))).param(unicode(self.tr(u'Grid'))).param(
            unicode(self.tr(u'Y'))).setValue(theme.oscillogramTheme.gridY)
        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(unicode(self.tr(u'Grid'))).param(
            unicode(self.tr(u'X'))).setValue(theme.spectrogramTheme.gridX)
        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(unicode(self.tr(u'Grid'))).param(
            unicode(self.tr(u'Y'))).setValue(theme.spectrogramTheme.gridY)
        self.ParamTree.param(unicode(self.tr(u'Oscillogram Settings'))).param(
            unicode(self.tr(u'Background color'))).setValue(theme.oscillogramTheme.background_color)
        self.ParamTree.param(unicode(self.tr(u'Oscillogram Settings'))).param(unicode(self.tr(u'Plot color'))).setValue(
            theme.oscillogramTheme.plot_color)
        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
            unicode(self.tr(u'Background color'))).setValue(theme.spectrogramTheme.background_color)
        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(unicode(self.tr(u'Threshold(dB)'))).param(
            unicode(self.tr(u'Min'))).setValue(theme.spectrogramTheme.histRange[0])
        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(unicode(self.tr(u'Threshold(dB)'))).param(
            unicode(self.tr(u'Max'))).setValue(theme.spectrogramTheme.histRange[1])
        # self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
        #     unicode(self.tr(u'Frequency(kHz)'))).param(unicode(self.tr(u'Min'))).setValue(theme.minYSpec / 1000.0)
        # self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
        #     unicode(self.tr(u'Frequency(kHz)'))).param(unicode(self.tr(u'Max'))).setValue(theme.maxYSpec / 1000.0)
        # self.ParamTree.param(unicode(self.tr(u'Oscillogram Settings'))).param(unicode(self.tr(u'Amplitude(%)'))).param(
        #     unicode(self.tr(u'Min'))).setValue(theme.minYOsc)
        # self.ParamTree.param(unicode(self.tr(u'Oscillogram Settings'))).param(unicode(self.tr(u'Amplitude(%)'))).param(
        #     unicode(self.tr(u'Max'))).setValue(theme.maxYOsc)
        # self.ParamTree.param(unicode(self.tr(u'Detection Visual Settings'))).param(
        #     unicode(self.tr(u'Measurement Location'))).param(unicode(self.tr(u'Center'))).setValue(theme.centerColor)
        # self.ParamTree.param(unicode(self.tr(u'Detection Visual Settings'))).param(
        #     unicode(self.tr(u'Measurement Location'))).param(unicode(self.tr(u'End'))).setValue(theme.endColor)
        # self.ParamTree.param(unicode(self.tr(u'Detection Visual Settings'))).param(
        #     unicode(self.tr(u'Measurement Location'))).param(unicode(self.tr(u'Start'))).setValue(theme.startColor)
        # self.ParamTree.param(unicode(self.tr(u'Detection Visual Settings'))).param(
        #     unicode(self.tr(u'Measurement Location'))).param(unicode(self.tr(u'Quartile25'))).setValue(
        #     theme.quart1Color)
        # self.ParamTree.param(unicode(self.tr(u'Detection Visual Settings'))).param(
        #     unicode(self.tr(u'Measurement Location'))).param(unicode(self.tr(u'Quartile75'))).setValue(
        #     theme.quart2Color)

    @pyqtSlot()
    def on_actionLoad_Theme_triggered(self):
        """
        Load a new theme (previously saved) from disc.
        :return:
        """
        filename = QFileDialog.getOpenFileName(parent=self, directory=os.path.join(u"Utils", u"Themes"),
                                               caption=self.tr(u"Load Theme"),
                                               filter=self.tr(u"Duetto Theme Files") + u" (*.dth);;All Files (*)")
        if filename and os.path.exists(filename):
            try:
                theme = self.deSerializeTheme(filename)
                self.updateTheme(theme)

            except Exception as ex:
                raise ex

    def deSerializeTheme(self, filename):
        """
        Deserialize a theme from a file.
        :param filename: the path to the file where the theme is saved
        :return:
        """
        if filename and os.path.exists(filename):
            try:
                file = open(filename, 'rb')
                data = pickle.load(file)
                file.close()
                return data
            except Exception as ex:
                raise ex

    def updateRegionTheme(self):
        """
        Update the variables in the param tree that represent the region of the histogram
        :return:
        """
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

    def serializeTheme(self, filename):
        """
        Serialize a theme to a file.
        :param filename: the path to the file for the theme storage.
        :return:
        """
        if filename:
            #get the histogram region and colorbar values
            self.defaultTheme.histRange = self.hist.item.region.getRegion()
            self.defaultTheme.colorBarState = self.hist.item.gradient.saveState()

            #save to disc the theme
            try:
                saved_theme = open(filename, 'wb')
                pickle.dump(self.defaultTheme, saved_theme)
                saved_theme.close()

            except Exception as ex:
                raise ex

    def change(self, param, changes):
        """
        Method that update the internal variables and state of the widgets
        when a change is made in the visual options of the theme
        :param param: param
        :param changes: list with the changes in the param tree
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
                self.defaultTheme.spectrogramTheme.gridX = data

            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'Grid')) + u"." + unicode(self.tr(u'Y')):
                self.defaultTheme.spectrogramTheme.gridY = data

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
                self.defaultTheme.spectrogramTheme.background_color = data

            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'ColorMap')):
                self.widget.axesSpecgram.getHistogramWidget().item._pixelVectorCache.append(data)

            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'Frequency(kHz)')) + u"." + \
                    unicode(self.tr(u'Min')):
                pass# self.defaultTheme.spectrogramTheme.minY = data

            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'Frequency(kHz)')) + u"." + \
                    unicode(self.tr(u'Max')):
                pass# self.defaultTheme.spectrogramTheme.maxY = data

            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'FFT overlap')):
                self.widget.axesSpecgram.specgramHandler.overlap = data
                self.widget.graph()

            elif childName == unicode(self.tr(u'Power Spectrum Settings')) + u"." + \
                    unicode(self.tr(u'FFT size')):
                self.NFFT_pow = data

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Background color')):
                self.defaultTheme.oscillogramTheme.background_color = data

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Grid')) + u"." + \
                    unicode(self.tr(u'X')):
                self.defaultTheme.oscillogramTheme.gridX = data

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Grid')) + u"." + \
                    unicode(self.tr(u'Y')):
                self.defaultTheme.oscillogramTheme.gridY = data

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Plot color')):
                self.defaultTheme.oscillogramTheme.plot_color = data

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Amplitude(%)')) + u"." + \
                    unicode(self.tr(u'Min')):
                pass# self.defaultTheme.oscillogramTheme.minY = data

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Amplitude(%)')) + u"." + \
                    unicode(self.tr(u'Max')):
                pass# self.defaultTheme.oscillogramTheme.maxY = data

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Connect Lines')):
                self.widget.lines = data
                self.widget.graph()
                return

            elif childName == unicode(self.tr(u'Themes')) + u"." + \
                    unicode(self.tr(u'Theme Selected')):
                self.updateTheme(self.deSerializeTheme(data))

            self.widget.load_Theme(self.defaultTheme)

    def changeFrequency(self, min, max):
        """
        Method that update the max and min frequency
        that is showed on the theme visual options for spectrogram.
        This method is used when the widget's signal change and must be
        updated with the new signal frequency range. Is also called when the widget change
        the visible range fo frequencies by a tool intercation or programatically.
        :param min: min frequecny in Khz
        :param max: max frequency in Khz
        :return:
        """
        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
            unicode(self.tr(u'Frequency(kHz)'))).param(unicode(self.tr(u'Min'))).setValue(min)
        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
            unicode(self.tr(u'Frequency(kHz)'))).param(unicode(self.tr(u'Max'))).setValue(max)
        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
            unicode(self.tr(u'Frequency(kHz)'))).param(unicode(self.tr(u'Max'))).setDefault(max)

    def changeAmplitude(self, min, max):
        """
        Method that update the max and min amplitude
        that is showed on the theme visual options for oscilogram.
        This method is used when the widget's signal change and must be
        updated with the new signal range. Is also called when the widget change
        the visible range by a tool intercation or programatically.
        :param min: min amplitude in % of maxmimum value allowed by the signal bit depth
        :param max: max amplitude in % of maxmimum value allowed by the signal bit depth
        :return:
        """
        self.ParamTree.param(unicode(self.tr(u'Oscillogram Settings'))).param(unicode(self.tr(u'Amplitude(%)'))).param(
            unicode(self.tr(u'Min'))).setValue(min)
        self.ParamTree.param(unicode(self.tr(u'Oscillogram Settings'))).param(unicode(self.tr(u'Amplitude(%)'))).param(
            unicode(self.tr(u'Max'))).setValue(max)

    #endregion

    # region Drag and Drop file
    #implementation of the events for drag and drop files into the window
    def dragEnterEvent(self, event):
        event.acceptProposedAction()
        self.dropchanged.emit(event.mimeData())

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        """
        catch a file and open the signal in it
        :param event:
        :return:
        """
        mimeData = event.mimeData()
        if len(mimeData.urls()) > 1:
            return

        mimeUrl = u"".join([unicode(url.path()) for url in mimeData.urls()])

        #get the path from the url
        path = mimeUrl[1:len(mimeUrl)]

        #open the signal in path if any
        self._open(path)

        #accept the event
        event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        event.accept()

    #endregion

    #region Widget Tools
    @pyqtSlot()
    def on_actionZoom_Cursor_triggered(self):
        """
        Select the Zoom Tool as current working tool in the widget
        :return:
        """
        self.deselectToolsActions()
        self.actionZoom_Cursor.setChecked(True)
        self.widget.setSelectedTool(Tools.ZoomTool)

    @pyqtSlot()
    def on_actionRectangular_Cursor_triggered(self):
        """
        Select the Rectangular Cursor as current working tool in the widget
        :return:
        """
        self.deselectToolsActions()
        self.actionRectangular_Cursor.setChecked(True)
        self.widget.setSelectedTool(Tools.RectangularZoomTool)

    @pyqtSlot()
    def on_actionRectangular_Eraser_triggered(self):
        """
        Select the Rectangular Eraser as current working tool in the widget
        :return:
        """
        self.deselectToolsActions()
        self.actionRectangular_Eraser.setChecked(True)
        self.widget.setSelectedTool(Tools.RectangularEraser)

    @pyqtSlot()
    def on_actionPointer_Cursor_triggered(self):
        """
        Select the Pointer Cursor as current working tool in the widget
        :return:
        """
        self.deselectToolsActions()
        self.actionPointer_Cursor.setChecked(True)
        self.widget.setSelectedTool(Tools.PointerTool)

    def deselectToolsActions(self):
        """
        Change the checked status of all the actions tools to False
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
        """
        Execute the scale on the selected section of the signal.
        :return:
        """
        scaleDialog = cvdialog.Ui_Dialog()
        scaleDialogWindow = ChangeVolumeDialog(self)
        scaleDialog.setupUi(scaleDialogWindow)

        if scaleDialogWindow.exec_():
            factor = scaleDialog.spinboxConstValue.value()

            if scaleDialog.rbuttonConst.isChecked():
                #scale by a constant factor
                self.widget.scale(factor)

            elif scaleDialog.rbuttonNormalize.isChecked():
                #scale by normalize the signal to the factor amplitude
                factor = scaleDialog.spinboxNormalizePercent.value()
                self.widget.normalize(factor)

            else:
                #scale by using a function
                function = scaleDialog.cboxModulationType.currentText()
                fade = u"IN" if scaleDialog.rbuttonFadeIn.isChecked() else u"OUT"
                self.widget.modulate(function, fade)

    @pyqtSlot()
    def on_actionInsert_Silence_triggered(self):
        """
        Insert an amount of silence time on the signal
        :return:
        """
        silenceDialog = sdialog.Ui_Dialog()
        silenceDialogWindow = InsertSilenceDialog(self)
        silenceDialog.setupUi(silenceDialogWindow)

        if silenceDialogWindow.exec_():
            #get the time in ms to insert as silence
            ms = silenceDialog.insertSpinBox.value()
            self.widget.insertSilence(ms)

    @pyqtSlot()
    def on_actionGenerate_Pink_Noise_triggered(self):
        """
        Insert a pink noise signal on the current analyzed signal
        :return:
        """
        #reuse the insert silence dialog
        whiteNoiseDialog = sdialog.Ui_Dialog()
        whiteNoiseDialogWindow = InsertSilenceDialog(self)
        whiteNoiseDialog.setupUi(whiteNoiseDialogWindow)

        #change the label for the new task of insert pink noise
        whiteNoiseDialog.label.setText(self.tr(u"Select the duration in ms") + " \n" + self.tr(u"of the Pink Noise."))

        #1 second time by default
        whiteNoiseDialog.insertSpinBox.setValue(1000)

        # if whiteNoiseDialogWindow.exec_():
        #     type_, Fc, Fl, Fu = self.filter_helper()
        #     if type_ != None:
        #         ms = whiteNoiseDialog.insertSpinBox.value()
        #         start, _ = self.widget.getIndexFromAndTo()
        #         self.widget.undoRedoManager.add(
        #             GeneratePinkNoiseAction(self.widget.signalProcessor.signal, start, ms, type_, Fc, Fl, Fu))
        #         self.widget.insertPinkNoise(ms, type_, Fc, Fl, Fu)

    @pyqtSlot()
    def on_actionGenerate_White_Noise_triggered(self):
        """
        Insert a white noise signal on the current analyzed signal
        :return:
        """
        #reuse the insert silence dialog
        whiteNoiseDialog = sdialog.Ui_Dialog()
        whiteNoiseDialogWindow = InsertSilenceDialog(self)
        whiteNoiseDialog.setupUi(whiteNoiseDialogWindow)

        #change the label for the new task of insert white noise
        whiteNoiseDialog.label.setText(self.tr(u"Select the duration in ms") + u" \n" + self.tr(u"of the White Noise."))

        #1 second time by default
        whiteNoiseDialog.insertSpinBox.setValue(1000)

        # if whiteNoiseDialogWindow.exec_():
        #     ms = whiteNoiseDialog.insertSpinBox.value()
        #     start, end = self.widget.getIndexFromAndTo()
        #     self.widget.undoRedoManager.add(
        #         GenerateWhiteNoiseAction(self.widget.signalProcessor.signal, start, ms))
        #     self.widget.insertWhiteNoise(ms)

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
        """
        execute a filter on the signal
        :return:
        """
        pass
        # type_, Fc, Fl, Fu = self.filter_helper()
        # if type_ is not None:
        #     self.widget.filter(type_, Fc, Fl, Fu)

    @pyqtSlot()
    def on_actionSilence_triggered(self):
        self.widget.silence()

    @pyqtSlot()
    def on_action_Reverse_triggered(self):
        self.widget.reverse()

    @pyqtSlot()
    def on_actionResampling_triggered(self):
        """

        :return:
        """
        #reuse the insert silence dialog
        resamplingDialog = sdialog.Ui_Dialog()
        resamplingDialogWindow = InsertSilenceDialog(self)
        resamplingDialog.setupUi(resamplingDialogWindow)

        #change the label for the new task of resampling
        resamplingDialog.label.setText(self.tr(u"Select the new Sampling Rate."))

        #set by default the current sampling rate
        resamplingDialog.insertSpinBox.setValue(self.widget.signal.samplingRate)

        if resamplingDialogWindow.exec_():
            #get the new sampling rate
            val = resamplingDialog.insertSpinBox.value()

            if self.MIN_SAMPLING_RATE <= val <= self.MAX_SAMPLING_RATE:
                self.widget.resampling(val)

            elif val < self.MIN_SAMPLING_RATE:
                QMessageBox.warning(QMessageBox(), self.tr(u"Error"),
                                        self.tr(u"Sampling rate should be greater than") + u" " + unicode(
                                        self.MIN_SAMPLING_RATE))
            else:
                QMessageBox.warning(QMessageBox(), self.tr(u"Error"),
                                    self.tr(u"Sampling rate should be less than") + u" " + unicode(
                                    self.MAX_SAMPLING_RATE))

    #endregion

    #region Zoom IN, OUT, NONE
    #delegate the task of zoom in, out and none
    #in the widget operations
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
        """
        Method that is call when the window has the initial state.
        That is: when the window is created,
                 when the current signal is closed but not the window.
        :return:
        """

        #get the didactic signal if exists
        duetto_signal = os.path.join(os.path.join(u"Utils", u"Didactic Signals"), u"duetto.wav")

        if os.path.exists(duetto_signal):
            self.widget.open(duetto_signal)
            self.actionSignalName.setText(self.tr(u"File Name:") + u" " + self.widget.signalName())
        else:
            signal = Synthesizer.generateSilence(44100, 16, 1)
            self.widget.signal = signal
            self.actionSignalName.setText(self.tr(u"File Name: Welcome to duetto"))

        #refresh and set visible both axes
        self.changeWidgetsVisibility(True, True)

        #update data in the theme from the new signal
        self.changeFrequency(0, self.widget.signal.samplingRate/2000)
        self.changeAmplitude(-100,100)
        self.widget.load_Theme(self.defaultTheme)

        #set some initial status behavior
        self.setWindowTitle(self.tr(u"Duetto Sound Lab - Welcome to Duetto"))
        self.statusbar.showMessage(self.tr(u"Welcome to Duetto Sound Lab."),5000)

    @pyqtSlot()
    def on_actionExit_triggered(self):
        self.close()

    def closeEvent(self, event):
        """
        Event for close. Release the resources and save changes.
        :param event:
        :return:
        """

        #save the signal if any change
        self.save_signal_if_modified(event)

        #close the window
        self.close()

    @pyqtSlot()
    def on_actionClose_triggered(self):
        """
        Action to close the current analyzed signal. returns the window to its initial state.
        :return:
        """
        #save the signal if any change
        self.save_signal_if_modified()

        #restart the window initial state
        self.on_load()

    def save_signal_if_modified(self, event=None):
        """
        Method that save the signal to disc if there was made some change on it.
        :param event: The close event if the next action is to close the window.
        Is used to reject the event if the user wants to cancel the save operation.
        :return:
        """
        if self.widget.undoRedoManager.count() > 0:
            #if any action was made then ask for save the signal
            mbox = QtGui.QMessageBox(QtGui.QMessageBox.Question, self.tr(u"Save"),
                                     self.tr(u"Do you want to save the signal?"),
                                     QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel, self)
            result = mbox.exec_()

            if result == QtGui.QMessageBox.Yes:
                self.on_actionSave_triggered()

            elif result == QtGui.QMessageBox.Cancel and event is not None:
                event.ignore()

    @pyqtSlot()
    def on_actionNew_triggered(self):
        """
        create a new signal by syntetizer and open it in the widget.
        :return:
        """
        new_file_dialog = NewFileDialog(parent=self)
        if new_file_dialog.exec_():
            pass
            # self.widget.specgramSettings.NFFT = self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
            #     unicode(self.tr(u'FFT size'))).value()
            # self.widget.specgramSettings.overlap = self.ParamTree.param(
            #     unicode(self.tr(u'Spectrogram Settings'))).param(unicode(self.tr(u'FFT overlap'))).value()
            # signal = Synthesizer.generateSilence(new_file_dialog.SamplingRate, new_file_dialog.BitDepth, new_file_dialog.Duration)
            # self.widget.signal = signal
            # self.setWindowTitle(self.tr(u"Duetto Sound Lab - ") + self.widget.signalName())
            # self.actionSignalName.setText(self.tr(u"File Name: ") + self.widget.signalName())
            #

    @pyqtSlot()
    def on_actionOpen_triggered(self):
        """
        Open a new file signal.
        :return:
        """
        file_name = QFileDialog.getOpenFileName(self, self.tr(u"Select a file to open"),
                                        directory = self.last_opened_signal_path,
                                        filter = self.tr(u"Wave Files") + u"(*.wav);;All Files(*)")
        self._open(unicode(file_name))

        #close the opened windows of one dim processing
        #and restart the list of windows
        for win in self.one_dim_windows:
            win.close()
        self.one_dim_windows = []

    def _open(self, file_path=''):
        """
        Method that open a signal from a file path
        :param file_path: The path to the signal on disc
        :return:
        """
        if file_path != u'':
            try:
                #set the variables for folder files management
                self.last_opened_signal_path = file_path
                self.getFolderFiles(file_path)

                self.widget.open(file_path)
                self.setWindowTitle(self.tr(u"Duetto Sound Lab - ") + self.widget.signalName())
                self.actionSignalName.setText(self.tr(u"File Name: ") + self.widget.signalName())
            except Exception as ex:
                print(ex.message)
                QMessageBox.warning(QMessageBox(), self.tr(u"Error"),
                                    self.tr(u"Could not load the file.") +
                                    u"\n" + file_path)

                #recover from an open error by opening a default signal
                signal = Synthesizer.generateSilence(44100, 16, 1)
                self.widget.signal = signal

            self.widget.graph()

            #update the theme values from the new of the opened signal
            self.changeFrequency(0, self.widget.signal.samplingRate / 2000)
            self.changeAmplitude(-100, 100)

            #select the zoom tool as default
            self.on_actionZoom_Cursor_triggered()

    @pyqtSlot()
    def on_actionSave_triggered(self):
        """
        Save the signal currently analyzed into disc
        :return:
        """
        #get the filename to store the signal
        file_name = unicode(QFileDialog.getSaveFileName(self, self.tr(u"Save signal"),
                                                        self.widget.signalName(), u"*.wav"))
        if file_name:
            self.widget.save(file_name)

    @pyqtSlot()
    def on_actionSave_selected_interval_as_triggered(self):
        """
        Save the signal currently visible (or selected) into disc  as a new signal
        :return:
        """
        # get the filename to store the new signal
        file_name = unicode(QFileDialog.getSaveFileName(self, self.tr(u"Save signal"),
                                                    self.tr(u"Selection-") +
                                                    self.widget.signalName(), u"*.wav"))
        if file_name:
            self.widget.saveSelectedSectionAsSignal(file_name)

    #endregion

    #region Folder Files UP and DOWN manipulation
    #a way to browse for the signal files of a folder
    #by a simple and user friendly mechanism
    @pyqtSlot()
    def on_actionFile_Up_triggered(self):
        """
        open the previous file signal in the folder that is been analyzed
        :return:
        """
        if self.filesInFolderIndex > 0:
            #if there is files in the folder to be opened
            #or the current file signal is not the first on the folder
            self.filesInFolderIndex -= 1

            #try to open the file in the new signal file path
            if os.path.exists(self.filesInFolder[self.filesInFolderIndex]):
                self._open(self.filesInFolder[self.filesInFolderIndex])

    @pyqtSlot()
    def on_actionFile_Down_triggered(self):
        """
        open the next file signal in the folder that is been analyzed
        :return:
        """
        if self.filesInFolderIndex < len(self.filesInFolder) - 1:
            #if the current file signal is not the last on the folder
            self.filesInFolderIndex += 1

            # try to open the file in the new signal file path
            if os.path.exists(self.filesInFolder[self.filesInFolderIndex]):
                self._open(self.filesInFolder[self.filesInFolderIndex])

    def getFolderFiles(self, file_path):
        """
        Get all the paths to files in the folder where file_path is.
        :param file_path: The path to a file that is on the folder desired.
        :return:
        """
        try:
            # get the folder of the path and the files on that folder.
            path_base = os.path.split(file_path)[0]
            self.filesInFolder = folderFiles(path_base)

            #set the current index to the index of the supplied file_path
            self.filesInFolderIndex = self.filesInFolder.index(file_path)

        except:
            #if somethign wrong go to the initial state
            self.filesInFolder = []
            self.filesInFolderIndex = -1

    #endregion

    #region Play, Pause, Stop, Record
    #delegate in the widget the reproduction actions
    @pyqtSlot()
    def on_actionPlay_Sound_triggered(self):
        self.widget.play()

    @pyqtSlot()
    def on_actionStop_Sound_triggered(self):
        self.widget.stop()

    @pyqtSlot()
    def on_actionRecord_triggered(self):
        self.widget.record()

    @pyqtSlot()
    def on_actionPause_Sound_triggered(self):
        self.widget.pause()

    @pyqtSlot()
    def on_actionChangePlayStatus_triggered(self):
        """
        Change the play status of the signal from play-pause and vice versa
        :return:
        """
        self.widget.switchPlayStatus()

    @pyqtSlot(QAction)
    def on_playSpeedChanged_triggered(self, action):
        """
        Change the play speed of the signal.
        :param action: the action to set the speed
        :return:
        """
        self.widget.stop()
        # the spped is get form the text of the action (?? is posible to improve it ??)
        speed = {u'1/8x': 12.5, u'1/4x': 25, u'1/2x': 50,
                                   u'1x': 100, u'2x': 200, u'4x': 400, u'8x': 800}[unicode(action.text())]

        self.widget.playSpeed = speed

    #endregion

    #region Widgets Visibility
    @pyqtSlot()
    def on_actionCombined_triggered(self):
        """
        Shows both axes visualization oscilogram and spectrogram.
        :return:
        """
        self.changeWidgetsVisibility(True, True)

    @pyqtSlot()
    def on_actionSpectogram_triggered(self):
        """
        Shows the spectrogram visualization graph only.
        :return:
        """
        self.changeWidgetsVisibility(False, True)

    @pyqtSlot()
    def on_actionOscilogram_triggered(self):
        """
        Shows the oscilogram visualization graph only.
        :return:
        """
        self.changeWidgetsVisibility(True, False)

    def changeWidgetsVisibility(self,visibleOscilogram=True, visibleSpectrogram=True):
        """
        Method that change the visibility of the widgets
        oscilogram and spectrogram on the main widget
        :param visibleOscilogram:  Visibility of the oscilogram
        :param visibleSpectrogram: Visibility of the spectrogram
        :return:
        """
        self.widget.visibleOscilogram = visibleOscilogram
        self.widget.visibleSpectrogram = visibleSpectrogram
        self.widget.graph()

    #endregion

    #region Save Widgets Image

    @pyqtSlot()
    def on_actionOsc_Image_triggered(self):
        """
        Save to disc the image of the oscilogram graph.
        :return:
        """
        if self.widget.visibleOscilogram:
            saveImage(self.widget.axesOscilogram, self.tr(u"oscilogram"))
        else:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"),
                                      self.tr(u"The Oscilogram plot widget is not visible.") + u"\n" + self.tr(
                                          u"You should see the data that you are going to save."))

    @pyqtSlot()
    def on_actionSpecgram_Image_triggered(self):
        """
        Save to disc the image of the spectrogram graph.
        :return:
        """
        if self.widget.visibleSpectrogram:
            saveImage(self.widget.axesSpecgram, self.tr(u"specgram"))
        else:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"),
                                      self.tr(u"The Espectrogram plot widget is not visible.") + " \n" + self.tr(
                                          u"You should see the data that you are going to save."))

    @pyqtSlot()
    def on_actionCombined_Image_triggered(self):
        """
        Save to disc the image of the both (oscilogram and spectrogram)
        visualization graphs.
        :return:
        """
        if self.widget.visibleOscilogram and self.widget.visibleSpectrogram:
            saveImage(self.widget, self.tr(u"graph"))
        else:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"),
                                      self.tr(u"One of the plot widgets is not visible.") + " \n" + self.tr(
                                          u"You should see the data that you are going to save."))

    #endregion

    #region Onedimensional Transforms
    def updatePowSpecWin(self):
        """
        Update the current interval of visualization/processing
        of the signal in the opened one dimensional windows
        :return:
        """
        indexFrom, indexTo = self.widget.getIndexFromAndTo()
        for win in self.one_dim_windows:
            win.updatePowSpectrumInterval([indexFrom, indexTo])

    @pyqtSlot()
    def on_actionPower_Spectrum_triggered(self):
        """
        Create a one dimensional transform window and show it.
        :return:
        """
        indexFrom, indexTo = self.widget.getIndexFromAndTo()
        dg_pow_spec = PowerSpectrumWindow(self, self.pow_spec_lines, self.widget.signal.data,
                                          [indexFrom, indexTo],
                                          self.widget.specgramSettings.NFFT,
                                          self.defaultTheme,
                                          self.widget.signal.samplingRate,
                                          self.widget.signal.bitDepth,
                                          self.widget.updateBothZoomRegions)

        #store the opened one dimensional transform windows for handling
        self.one_dim_windows.append(dg_pow_spec)

    #endregion

    #region Scroll Bar Range
    #TODO comentar e implementar esta parte
    # manipulation of the scrool bar to set the range
    #of visualization of the signal on the widget

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