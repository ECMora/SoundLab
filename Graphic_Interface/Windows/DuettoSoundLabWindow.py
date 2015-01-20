#  -*- coding: utf-8 -*-
import os
import pickle
from duetto.audio_signals import AudioSignal, openSignal
from duetto.sound_devices.Device import Device
from duetto.sound_devices.DevicesHandler import DevicesHandler
from PyQt4 import QtGui,QtCore
from duetto.audio_signals.Synthesizer import Synthesizer
from duetto.signal_processing.filter_signal_processors.frequency_domain_filters import BandPassFilter, HighPassFilter, \
    BandStopFilter, LowPassFilter
from pyqtgraph.parametertree.parameterTypes import ListParameter
from pyqtgraph.parametertree import Parameter, ParameterTree
from PyQt4.QtGui import QDialog, QMessageBox, QFileDialog, QActionGroup, QAction
from PyQt4.QtCore import pyqtSlot, QMimeData, pyqtSignal, QTimer
from duetto.dimensional_transformations.two_dimensional_transforms.Spectrogram.WindowFunctions import WindowFunction
from Utils.Utils import folderFiles, saveImage, DECIMAL_PLACES
from graphic_interface.widgets.QSignalVisualizerWidget import QSignalVisualizerWidget
from graphic_interface.Settings.WorkTheme import WorkTheme
from graphic_interface.Settings.Workspace import Workspace
from graphic_interface.windows.ParameterList import DuettoListParameterItem

from graphic_interface.dialogs.NewFileDialog import NewFileDialog
from graphic_interface.windows.OneDimensionalAnalysisWindow import OneDimensionalAnalysisWindow
from SegmentationAndClasificationWindow import SegmentationAndClasificationWindow
from ui_python_files.MainWindow import Ui_DuettoMainWindow
from graphic_interface.dialogs import InsertSilenceDialog as sdialog, FilterOptionsDialog as filterdg, \
    ChangeVolumeDialog as cvdialog, SoundDevicesDialog as sdDialog
from sound_lab_core.Clasification.ClassificationData import ClassificationData
from graphic_interface.widgets.signal_visualizer_tools.SignalVisualizerTool import Tools
from BrowseFilesWindow import BrowseFilesWindow


class SoundDevicesDialog(sdDialog.Ui_Dialog,QDialog):
    """
    Dialog that allow to select the sound device to play and record
    the signals. (Select inpuit and output sound devices from the installed on the
    computer)
    """
    # CONSTANTS
    # the static dictionary that memorize the dialog
    # element values during the application execution
    # region dialog elements values

    dialogValues = {}
    # endregion

    # region Initialize

    def __init__(self, input, output):
        """
        Initialize the dialogs elements with their last value
        """
        QDialog.__init__(self)
        self.setupUi(self)

        self.inputLayout = QtGui.QGridLayout(self.grpBoxInput)
        self.inputLayout.setObjectName("gridInputLayout")

        self.outputLayout = QtGui.QGridLayout(self.grpBoxOutput)
        self.outputLayout.setObjectName("gridOutputLayout")

        self.loadInputDevices(input)
        self.loadOutputDevices(output)

    def loadInputDevices(self,input):
        """

        :return:
        """
        for index in range(len(input)):
            dev = input[index]
            rbutton = QtGui.QRadioButton(self.grpBoxInput)
            rbutton.setObjectName(str(index))
            rbutton.setText(dev.name + " " + str(dev.defaultSamplingRate * 1. / 1000) + " kHz " + str(
                dev.maxChannels) + " channels.")
            self.inputLayout.addWidget(rbutton)

    def loadOutputDevices(self,output):
        """

        :return:
        """
        for index in range(len(output)):
            dev = output[index]
            rbutton = QtGui.QRadioButton(self.grpBoxOutput)
            rbutton.setObjectName(str(index))
            rbutton.setText(dev.name + " " + str(dev.defaultSamplingRate * 1. / 1000) + " kHz " + str(
                dev.maxChannels) + " channels.")
            self.outputLayout.addWidget(rbutton)

    # endregion

    # region memoization of selected previous values

    def load_values(self):
        """
        Load into the dialog elements the previously
        or default values.
        """
        pass

    def save_values(self):
        """
        Load into the dialog elements the previously
        or default values.
        """

        pass

    # endregion

    @property
    def inputDeviceIndex(self):
        pass

    @property
    def outputDeviceIndex(self):
        pass


class InsertSilenceDialog(sdialog.Ui_Dialog, QDialog):
    """
    Dialog to select a duration for a signal insertion.
    """

    # CONSTANTS
    # the static dictionary that memorize the dialog
    # element values during the application execution
    # region dialog elements values

    dialogValues = {
        "insertSpinBox": 5000
    }
    # endregion

    def __init__(self):
        """
        Initialize the dialogs elements with their last value
        """
        QDialog.__init__(self)
        self.setupUi(self)

        # load the previous selected values for the dialog or the defaults ones
        self.load_values()
        self.btonaceptar.clicked.connect(self.save_values)

    def load_values(self):
        """
        Load into the dialog elements the previously
        or default values.
        """

        # set the values of the selected filter type on radio buttons
        self.insertSpinBox.setValue(self.dialogValues["insertSpinBox"])

    def save_values(self):
        """
        Load into the dialog elements the previously
        or default values.
        """

        # set the values of the selected amplitude modulation type on radio buttons
        self.dialogValues["insertSpinBox"] = self.insertSpinBox.value()


class ChangeVolumeDialog(cvdialog.Ui_Dialog, QDialog):
    """
    Dialog to select a time-amplitude modulation.
    """

    # CONSTANTS
    # the static dictionary that memorize the dialog
    # element values during the application execution

    # region dialog elements values

    dialogValues = {
        "rbuttonConst": True,
        "rbuttonFadeIn": False,
        "rbuttonFadeOut": False,
        "rbuttonNormalize": False,
        "spinboxConstValue": 1.00,
        "spinboxNormalizePercent": 50.00,
        "cboxModulationType": 0
    }
    # endregion

    def __init__(self):
        """
        Initialize the dialogs elements with their last value
        """
        QDialog.__init__(self)
        self.setupUi(self)

        # load the previous selected values for the dialog or the defaults ones
        self.load_values()
        self.buttonBox.accepted.connect(self.save_values)

    def load_values(self):
        """
        Load into the dialog elements the previously
        or default values.
        """

        # set the values of the selected filter type on radio buttons
        self.rbuttonConst.setChecked(self.dialogValues["rbuttonConst"])
        self.rbuttonFadeIn.setChecked(self.dialogValues["rbuttonFadeIn"])
        self.rbuttonFadeOut.setChecked(self.dialogValues["rbuttonFadeOut"])
        self.rbuttonNormalize.setChecked(self.dialogValues["rbuttonNormalize"])

        # set the values of every spin box with the previous or default selection
        self.spinboxConstValue.setValue(self.dialogValues["spinboxConstValue"])
        self.spinboxNormalizePercent.setValue(self.dialogValues["spinboxNormalizePercent"])
        self.cboxModulationType.setCurrentIndex(self.dialogValues["cboxModulationType"])

    def save_values(self):
        """
        Load into the dialog elements the previously
        or default values.
        """

        # set the values of the selected amplitude modulation type on radio buttons
        self.dialogValues["rbuttonConst"] = self.rbuttonConst.isChecked()
        self.dialogValues["rbuttonFadeIn"] = self.rbuttonFadeIn.isChecked()
        self.dialogValues["rbuttonFadeOut"] = self.rbuttonFadeOut.isChecked()
        self.dialogValues["rbuttonNormalize"] = self.rbuttonNormalize.isChecked()

        # set the values of the selected amplitude modulation
        self.dialogValues["spinboxConstValue"] = self.spinboxConstValue.value()
        self.dialogValues["spinboxNormalizePercent"] = self.spinboxNormalizePercent.value()
        self.dialogValues["cboxModulationType"] = self.cboxModulationType.currentIndex()


class FilterDialog(filterdg.Ui_Dialog, QDialog):
    """
    Dialog to select a filter.
    """

    # CONSTANTS
    # the static dictionary that memorize the dialog
    # element values during the application execution

    # region dialog elements values
    dialogValues = {
        "rButtonLowPass": True,
        "rButtonHighPass": False,
        "rButtonBandPass": False,
        "rButtonBandStop": False,
        "spinBoxLowPass": 0.00,
        "spinBoxHighPass": 0.00,
        "spinBoxBandStopFu": 0.00,
        "spinBoxBandStopFl": 0.00,
        "spinBoxBandPassFl": 0.00,
        "spinBoxBandPassFu": 0.00
    }
    # endregion

    def __init__(self):
        """
        Initialize the dialogs elements with their last value
        """
        QDialog.__init__(self)
        self.setupUi(self)

        # load the previous selected values for the dialog or the defaults ones
        self.load_values()
        self.btonaceptar.clicked.connect(self.save_values)

    def load_values(self):
        """
        Load into the dialog elements the previously
        or default values.
        """

        # set the values of the selected filter type on radio buttons
        self.rButtonLowPass.setChecked(self.dialogValues["rButtonLowPass"])
        self.rButtonHighPass.setChecked(self.dialogValues["rButtonHighPass"])
        self.rButtonBandStop.setChecked(self.dialogValues["rButtonBandStop"])
        self.rButtonBandPass.setChecked(self.dialogValues["rButtonBandPass"])

        # set the values of every spin box with the kHz of frequency selection
        self.spinBoxLowPass.setValue(self.dialogValues["spinBoxLowPass"])
        self.spinBoxHighPass.setValue(self.dialogValues["spinBoxHighPass"])
        self.spinBoxBandStopFu.setValue(self.dialogValues["spinBoxBandStopFu"])
        self.spinBoxBandStopFl.setValue(self.dialogValues["spinBoxBandStopFl"])
        self.spinBoxBandPassFl.setValue(self.dialogValues["spinBoxBandPassFl"])
        self.spinBoxBandPassFu.setValue(self.dialogValues["spinBoxBandPassFu"])

    def save_values(self):
        """
        Load into the dialog elements the previously
        or default values.
        """

        # save the values of the selected filter type on radio buttons
        self.dialogValues["rButtonLowPass"] = self.rButtonLowPass.isChecked()
        self.dialogValues["rButtonHighPass"] = self.rButtonHighPass.isChecked()
        self.dialogValues["rButtonBandStop"] = self.rButtonBandStop.isChecked()
        self.dialogValues["rButtonBandPass"] = self.rButtonBandPass.isChecked()

        # save the values of the spin box with the frequencies
        self.dialogValues["spinBoxLowPass"] = self.spinBoxLowPass.value()
        self.dialogValues["spinBoxHighPass"] = self.spinBoxHighPass.value()
        self.dialogValues["spinBoxBandStopFu"] = self.spinBoxBandStopFu.value()
        self.dialogValues["spinBoxBandStopFl"] = self.spinBoxBandStopFl.value()
        self.dialogValues["spinBoxBandPassFl"] = self.spinBoxBandPassFl.value()
        self.dialogValues["spinBoxBandPassFu"] = self.spinBoxBandPassFu.value()


class DuettoSoundLabWindow(QtGui.QMainWindow, Ui_DuettoMainWindow):
    """
    Main window of the application.
    """

    #  region SIGNALS
    #  signal raised when a file is drop into the window
    dropchanged = pyqtSignal(QMimeData)

    # signal raised when the user change the application language
    # raise the new language file path
    languageChanged = pyqtSignal(str)

    # signal raised when the user change the application style
    # raise the new style path
    styleChanged = pyqtSignal(str)

    # endregion

    #  region CONSTANTS
    #  minimum and maximum sampling rate used on the application
    MIN_SAMPLING_RATE = 1000
    MAX_SAMPLING_RATE = 2000000

    # the max duration of signal that is possible to process
    # with the segmentation and classification window (in seconds)
    MAX_SIGNAL_DURATION_ALLOWED = 60

    #  Width and height of the dock window of visual options
    SETTINGS_WINDOW_WIDTH = 340
    SETTINGS_WINDOW_HEIGHT = 100

    #
    DECIMAL_PLACES = 2

    # endregion

    # region Initialize

    def __init__(self, parent=None, signal_path=''):
        """
        :param parent:
        :param signal_path: Optional Signal path to open
        :return:
        """
        super(DuettoSoundLabWindow, self).__init__(parent)
        self.setupUi(self)

        # the recent files list contains the latest ones in the end (it should
        # probably be reversed for display)
        self._appSettings = {'Workspace': Workspace(), 'RecentFiles': []}
        
        #  theme for the visual options
        theme_path = os.path.join("Utils", "Themes", "default.dth")

        try:
            self._appSettings['Workspace'].workTheme = self.deSerializeTheme(theme_path)

        except Exception as e:
            self._appSettings['Workspace'].workTheme = WorkTheme()
            QMessageBox.warning(self, 'Error loading theme',
                                'An error occurred while loading the theme. A default theme will be loaded instead.\n' +
                                'Error: ' + str(e))

        # the list with all the actions that are depending
        # of at least one open signal. Are disabled if there is no open signal
        self.signalDependingActions = []

        # text edit for the signal name
        self.signalNameLineEdit = QtGui.QLineEdit(self)
        self.signalNameLineEdit.textChanged.connect(lambda text: self.signalNameChanged(text))
        self.signalNameLineEdit.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum))

        self.addSignalTab(Synthesizer.generateSilence(duration=1))

        # some initial state configurations
        self.configureSignalsTab()
        self.configureNoOpenedWidget()
        self.configureActionsGroups()

        # get all the themes that are in the static folder for themes ("Utils\Themes\")
        app_themes = folderFiles(os.path.join("Utils", "Themes"), extensions=[".dth"])

        # get all the styles that are in the static folder for styles ("styles\")
        app_styles = folderFiles("styles", extensions=[".qss"])

        # get all the languages translations that are in the static folder for languagues ("I18n\")
        app_languagues = folderFiles("I18n", extensions=[".qm"])

        #  get the histogram object of the spectrogram widget.
        #  this histogram would be visualized outside the spectrogram widget for best
        #  user interaction
        self.hist = self.widget.axesSpecgram.histogram
        self.hist.setFixedWidth(self.SETTINGS_WINDOW_WIDTH)
        self.hist.setFixedHeight(self.SETTINGS_WINDOW_HEIGHT)
        self.hist.item.gradient.restoreState(self.workTheme.spectrogramTheme.colorBarState)
        self.hist.item.region.setRegion(self.workTheme.spectrogramTheme.histRange)
        self.hist.item.region.sigRegionChanged.connect(self.updateRegionTheme)
        self.hist.item.gradient.sigGradientChanged.connect(self.histogramGradientChanged)

        #  the path to the last opened file signal used to
        #  give higher user friendly interaction on file search
        self.last_opened_signal_path = ''

        #  get the status bar to show messages to the user
        self.statusbar = self.statusBar()
        self.statusbar.setSizeGripEnabled(False)
        self.statusbar.showMessage(self.tr(u"Welcome to duetto-Sound Lab"), 5000)

        #  user interface to manipulate several visual parameters
        #  and display options of the application theme.
        #  Is used a parameter tree to present to the user the visual options

        #  region Parameter Tree definition

        #  create the tree,  and connect
        self.ParamTree = self.__getParamsTree(app_styles, app_languagues, app_themes)

        self.ParamTree.sigTreeStateChanged.connect(self.change)

        parameterTree = ParameterTree()
        parameterTree.setAutoScroll(True)
        parameterTree.setFixedWidth(self.SETTINGS_WINDOW_WIDTH)
        parameterTree.setHeaderHidden(True)
        parameterTree.setParameters(self.ParamTree, showTop=False)

        #  endregion

        #  set the vertical layout of the visual options window with the
        #  param tree and the histogram color bar
        layout = QtGui.QVBoxLayout()
        layout.setMargin(0)
        layout.addWidget(parameterTree)
        layout.addWidget(self.hist)

        self.hist.item.gradient.restoreState(self.workTheme.spectrogramTheme.colorBarState)
        self.hist.item.region.setRegion(self.workTheme.spectrogramTheme.histRange)

        self.osc_settings_contents.setLayout(layout)
        self.dock_settings.setVisible(False)
        self.dock_settings.setFixedWidth(self.SETTINGS_WINDOW_WIDTH)

        #  get the clasification data stored
        #  classifPath = os.path.join(os.path.join("Utils","Classification"),"classifSettings")
        self.classificationData = self.deserializeClassificationData()

        #  variables to handle the navigation across the signal files of one folder
        #  to allow to open all the files in the folder user friendly by action up/down next file
        self.filesInFolder = []
        self.filesInFolderIndex = -1

        #  the list of one dimensional processing windows opened by the user.
        self.one_dim_windows = []

        #  accept drops to open signals by drop
        self.setAcceptDrops(True)

        #  set the action group to change the play speed of the opened signal
        playSpeedActionGroup = QActionGroup(self)
        playSpeedActionGroup.addAction(self.action1_8x)
        playSpeedActionGroup.addAction(self.action1_4x)
        playSpeedActionGroup.addAction(self.action1_2x)
        playSpeedActionGroup.addAction(self.action1x)
        playSpeedActionGroup.addAction(self.action2x)
        playSpeedActionGroup.addAction(self.action4x)
        playSpeedActionGroup.addAction(self.action8x)
        playSpeedActionGroup.triggered.connect(self.on_playSpeedChanged_triggered)


        # close the signal of the opening
        self.tabOpenedSignals.removeTab(0)

        # set the values for start with no opened signals
        self.setNoSignalsOpenState(signals_open=False)

        # open a signal if any
        if signal_path != '':
            self._open(unicode(signal_path))

        self.showMaximized()
        self.on_load_first_time()

    def setNoSignalsOpenState(self, signals_open):
        """
        Configure the app behavior and variables for a no open signal situation.
        In this case just to show the no signal opened widget and hide the tabbar with signals.
        :param signals_open: True if there is signals open. False otherwise
        :return:
        """
        # set the tab bar with signals visible and the action
        # that depend of signals enabled if there is opened signals
        self.setSignalActionsEnabledState(signals_open)
        self.tabOpenedSignals.setVisible(signals_open)

        # set visible the label of no opened signals if no signals are opened
        self.noSignalOpened_lbl.setVisible(not signals_open)

        # set the defaults name for signal on edit and window title
        if not signals_open:
            self.signalNameLineEdit.setText("")
            self.signalNameLineEdit.setToolTip("")
            self.setWindowTitle(self.tr(u"duetto-Sound Lab"))

    def configureNoOpenedWidget(self):
        """
        Configure the no Opened signals widget to show.
        :return:
        """
        # the widget for no opened signals configuration is just
        # to set it invisible at starting
        # when a more complicated logic will be needed put it here
        self.noSignalOpened_lbl.setVisible(False)

    def configureSignalsTab(self):
        """
        Set the starting setting of the signal tab to start execution
        :return:
        """
        # connect the signals for the changed tab and close tab events
        self.tabOpenedSignals.currentChanged.connect(self.currentSignalTabChanged)
        self.tabOpenedSignals.tabCloseRequested.connect(self.closeSignalAt)

        # add the tab context menu
        self.tabOpenedSignals.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        actions = [self.actionClose, self.actionCloseAll, self.actionCloseOthers,
                   self.actionCloseUnmodified, self.actionOpenInOtherTab,
                   self.actionOpen_Selection]
        for act in actions:
            self.tabOpenedSignals.addAction(act)

    def __getParamsTree(self, app_styles, app_languagues, app_themes):
        """
        Defines and return the Param Tree with the app options
        :return:
        """

        # region params definition
        params = [
            {u'name': unicode(self.tr(u'Oscillogram Settings')), u'type': u'group', u'children': [
                {u'name': unicode(self.tr(u'Amplitude(%)')), u'type': u'group', u'children': [
                    {u'name': unicode(self.tr(u'Min')), u'type': u'float', u'value': -100, u'step': 2},
                    {u'name': unicode(self.tr(u'Max')), u'type': u'float', u'value': 100, u'step': 2},
                ]},

                {u'name': unicode(self.tr(u'Grid')), u'type': u'group', u'children': [
                    {u'name': u'X', u'type': u'bool', u'default': self._appSettings['Workspace'].workTheme.oscillogramTheme.gridX,
                     u'value': self._appSettings['Workspace'].workTheme.oscillogramTheme.gridX},
                    {u'name': u'Y', u'type': u'bool', u'default': self._appSettings['Workspace'].workTheme.oscillogramTheme.gridY,
                     u'value': self._appSettings['Workspace'].workTheme.oscillogramTheme.gridY},

                ]},
                {u'name': unicode(self.tr(u'Background color')), u'type': u'color',
                 u'value': self._appSettings['Workspace'].workTheme.oscillogramTheme.background_color,
                 u'default': self._appSettings['Workspace'].workTheme.oscillogramTheme.background_color},
                {u'name': unicode(self.tr(u'Plot color')), u'type': u'color',
                 u'value': self._appSettings['Workspace'].workTheme.oscillogramTheme.plot_color,
                 u'default': self._appSettings['Workspace'].workTheme.oscillogramTheme.plot_color},
                {u'name': unicode(self.tr(u'Connect Points')), u'type': u'bool',
                 u'default': self._appSettings['Workspace'].workTheme.oscillogramTheme.connectPoints,
                 u'value': self._appSettings['Workspace'].workTheme.oscillogramTheme.connectPoints},
            ]},

            {u'name': unicode(self.tr(u'Spectrogram Settings')), u'type': u'group', u'children': [
                {u'name': unicode(self.tr(u'Frequency(kHz)')), u'type': u'group', u'children': [
                    {u'name': unicode(self.tr(u'Min')), u'type': u'float', u'value': 0, u'step': 0.1},
                    {u'name': unicode(self.tr(u'Max')), u'type': u'float', u'value': 22, u'step': 0.1},
                ]},
                {u'name': unicode(self.tr(u'FFT size')), u'type': u'list', u'default': 512,
                 u'values': [(u"128", 128), (u"256", 256), (u"512", 512), (u"1024", 1024), (u"8192", 8192)],
                 u'value': u'512'},
                {u'name': unicode(self.tr(u'FFT window')), u'type': u'list',
                 u'value': WindowFunction.Hanning,
                 u'default': WindowFunction.Hanning,
                 u'values': [(u'Bartlett', WindowFunction.Bartlett),
                             (u"Blackman", WindowFunction.Blackman),
                             (u"Hamming", WindowFunction.Hamming),
                             (u"Hanning", WindowFunction.Hanning),
                             (u'Kaiser', WindowFunction.Kaiser),
                             (unicode(self.tr(u'None')), WindowFunction.WindowNone),
                             (u"Rectangular", WindowFunction.Rectangular)]},
                {u'name': unicode(self.tr(u'FFT overlap')), u'type': u'int', u'value': -1, u'limits': (-1, 99)},
                {u'name': unicode(self.tr(u'Threshold(dB)')), u'type': u'group', u'children': [
                    {u'name': unicode(self.tr(u'Min')), u'type': u'int', u'step': 1,
                     u'default': self._appSettings['Workspace'].workTheme.spectrogramTheme.histRange[0],
                     u'value': self._appSettings['Workspace'].workTheme.spectrogramTheme.histRange[0]},
                    {u'name': unicode(self.tr(u'Max')), u'type': u'float', u'step': 0.1,
                     u'default': self._appSettings['Workspace'].workTheme.spectrogramTheme.histRange[1],
                     u'value': self._appSettings['Workspace'].workTheme.spectrogramTheme.histRange[1]},
                ]},
                {u'name': unicode(self.tr(u'Grid')), u'type': u'group', u'children': [
                    {u'name': u'X', u'type': u'bool', u'default': self._appSettings['Workspace'].workTheme.spectrogramTheme.gridX,
                     u'value': self._appSettings['Workspace'].workTheme.spectrogramTheme.gridX},
                    {u'name': u'Y', u'type': u'bool', u'default': self._appSettings['Workspace'].workTheme.spectrogramTheme.gridY,
                     u'value': self._appSettings['Workspace'].workTheme.spectrogramTheme.gridY},

                ]},
                {u'name': unicode(self.tr(u'Background color')), u'type': u'color',
                 u'value': self._appSettings['Workspace'].workTheme.spectrogramTheme.background_color,
                 u'default': self._appSettings['Workspace'].workTheme.spectrogramTheme.background_color},
            ]},
            {u'name': unicode(self.tr(u'Themes')), u'type': u'group', u'children': [
                {u'name': unicode(self.tr(u'Theme Selected')), u'type': u'list',
                 u'value': u"" if not app_themes else os.path.basename(app_themes[0])[:-4],
                 u'default': u"" if not app_themes else os.path.basename(app_themes[0])[:-4],
                 u'values': [(u"", u"")] if not app_themes else [(os.path.basename(x)[:-4], x) for x in
                                                                 app_themes]},
            ]
            },
            {u'name': unicode(self.tr(u'Language')), u'type': u'group', u'children': [
                {u'name': unicode(self.tr(u'Language Selected')), u'type': u'list',
                 u'value': u"" if not app_languagues else os.path.basename(app_languagues[0])[:-4],
                 u'default': u"" if not app_languagues else os.path.basename(app_languagues[0])[:-4],
                 u'values': [(u"", u"")] if not app_languagues else [(os.path.basename(x)[:-4], x) for x in
                                                                     app_languagues]},
            ]
            },
            {u'name': unicode(self.tr(u'Style')), u'type': u'group', u'children': [
                {u'name': unicode(self.tr(u'Style Selected')), u'type': u'list',
                 u'value': u"" if not app_styles else os.path.basename(app_styles[0])[:-4],
                 u'default': u"" if not app_styles else os.path.basename(app_styles[0])[:-4],
                 u'values': [(u"", u"")] if not app_styles else [(os.path.basename(x)[:-4], x) for x in
                                                                 app_styles]},
            ]
            },
            {u'name': unicode(self.tr(u'Tabs')), u'type': u'group', u'children': [
                {u'name': unicode(self.tr(u'Tab Position')), u'type': u'list',
                 u'value': QtGui.QTabWidget.North,
                 u'default': QtGui.QTabWidget.North,
                 u'values': [(u'North', QtGui.QTabWidget.North),
                             (u"South", QtGui.QTabWidget.South),
                             (u"West", QtGui.QTabWidget.West),
                             (u"East", QtGui.QTabWidget.East)
                            ]},
                {u'name': unicode(self.tr(u'Tab Shape')), u'type': u'list',
                 u'value': QtGui.QTabWidget.Rounded,
                 u'default': QtGui.QTabWidget.Triangular,
                 u'values': [(u'Rounded', QtGui.QTabWidget.Rounded),
                             (u"Triangular", QtGui.QTabWidget.Triangular)
                 ]}
            ]
            },
            {u'name': unicode(self.tr(u'Detection Visual Settings')), u'type': u'group', u'children': [
                {u'name': unicode(self.tr(u'Measurement Location')), u'type': u'group', u'children': [
                    {u'name': unicode(self.tr(u'Start')), u'type': u'color',
                     u'value': self._appSettings['Workspace'].workTheme.detectionTheme.startColor,
                     u'default': self._appSettings['Workspace'].workTheme.detectionTheme.startColor},
                    {u'name': unicode(self.tr(u'Quartile25')), u'type': u'color',
                     u'value': self._appSettings['Workspace'].workTheme.detectionTheme.quart1Color,
                     u'default': self._appSettings['Workspace'].workTheme.detectionTheme.quart1Color},
                    {u'name': unicode(self.tr(u'Center')), u'type': u'color',
                     u'value': self._appSettings['Workspace'].workTheme.detectionTheme.centerColor,
                     u'default': self._appSettings['Workspace'].workTheme.detectionTheme.centerColor},
                    {u'name': unicode(self.tr(u'Quartile75')), u'type': u'color',
                     u'value': self._appSettings['Workspace'].workTheme.detectionTheme.quart2Color,
                     u'default': self._appSettings['Workspace'].workTheme.detectionTheme.quart2Color},
                    {u'name': unicode(self.tr(u'End')), u'type': u'color',
                     u'value': self._appSettings['Workspace'].workTheme.detectionTheme.endColor,
                     u'default': self._appSettings['Workspace'].workTheme.detectionTheme.endColor},
                ]}]}

        ]
        #  endregion

        # change the item class of the list parameter type to allow order in the children params added
        ListParameter.itemClass = DuettoListParameterItem

        return Parameter.create(name=u'params', type=u'group', children=params)

    def addWidgetContextMenuActions(self):
        """
        Adds the context menu options to the current signal widget
        :return:
        """

        # create the separators for the context menu
        sep1, sep2, sep3, sep4, sep5 = [QtGui.QAction(self) for _ in range(5)]

        for sep in [sep1, sep2, sep3, sep4, sep5]:
            sep.setSeparator(True)

        # region add actions to the context menu
        self.widget.createContextCursor([
            # Close Actions
            # self.actionCloseAll,
            # self.actionCloseUnmodified,
            # sep1,

            # Edition Actions
            self.actionCopy,
            self.actionCut,
            self.actionPaste,
            sep2,

            # Signal Data Sign Actions
            self.actionNegative_Values,
            self.actionPositive_Values,
            self.actionChange_Sign,
            sep3,

            #  common signal processing actions
            self.action_Reverse,
            self.actionSilence,
            self.actionInsert_Silence,
            sep4,

            #  Tools
            self.actionZoom_Cursor,
            self.actionPointer_Cursor,
            self.actionRectangular_Cursor,
            self.actionRectangular_Eraser,
            sep5,

            #  widgets images
            self.actionOsc_Image,
            self.actionSpecgram_Image,
            self.actionCombined_Image
        ])
        # endregion

    def configureActionsGroups(self):
        """
        Configure the actions into groups for best visualization and
        user configuration.
        :return:
        """

        # region Add actions groups
        # create the separators for the actions
        sep1, sep2, sep3, sep4, sep5, sep6, sep7,sep8 = [QtGui.QAction(self) for _ in range(8)]

        for sep in [sep1, sep2, sep3, sep4, sep5, sep6, sep7,sep8]:
            sep.setSeparator(True)

        # region open save actions
        open_save_actions = QActionGroup(self)
        open_save_actions_list = [self.actionNew, self.actionOpen, self.actionSave, sep1]

        for act in open_save_actions_list:
            act.setActionGroup(open_save_actions)
        # endregion

        # region edition actions
        edition_actions = QActionGroup(self)
        edition_actions_list = [self.actionCopy, self.actionPaste, self.actionCut, sep2]

        for act in edition_actions_list:
            act.setActionGroup(edition_actions)
        # endregion

        # region play record actions
        play_record_actions = QActionGroup(self)
        play_record_actions_list = [self.actionPlay_Sound, self.actionPause_Sound, self.actionStop_Sound,
                                    self.actionRecord, sep3]

        for act in play_record_actions_list:
            act.setActionGroup(play_record_actions)
        # endregion

        # region widgets visibility actions
        widgets_visibility_actions = QActionGroup(self)
        widgets_visibility_actions_list = [self.actionOscilogram, self.actionSpectogram, self.actionCombined,
                                           sep4]

        for act in widgets_visibility_actions_list:
            act.setActionGroup(widgets_visibility_actions)
        # endregion

        # region undo redo actions
        undo_redo_actions = QActionGroup(self)
        undo_redo_actions_list = [self.actionUndo, self.actionRedo,sep5]

        for act in undo_redo_actions_list:
            act.setActionGroup(undo_redo_actions)

        # endregion

        # region zoom actions
        zoom_actions = QActionGroup(self)
        zoom_actions_list = [self.actionZoomIn, self.actionZoom_out,
                                  self.actionZoom_out_entire_file,sep6]

        for act in zoom_actions_list:
            act.setActionGroup(zoom_actions)

        # endregion

        # region File up down actions
        file_updown_actions = QActionGroup(self)
        file_updown_actions_list = [self.actionFile_Up, self.actionFile_Down, sep7]

        for act in file_updown_actions_list:
            act.setActionGroup(file_updown_actions)

        # endregion

        # region Segmentation and Transformations actions
        segm_transf_actions = QActionGroup(self)
        segm_transf_actions_list = [self.actionOneDimensionalTransformation,
                                   self.actionSegmentation_And_Clasification, sep8]

        for act in segm_transf_actions_list:
            act.setActionGroup(segm_transf_actions)

        # endregion

        # region Processing actions
        processing_actions = QActionGroup(self)
        processing_actions_list = [self.actionPositive_Values,self.actionNegative_Values,self.actionChange_Sign,
                                   self.action_Reverse, self.actionSilence, self.actionFilter, self.actionSmart_Scale,
                                   self.actionResampling,self.actionInsert_Silence,self.actionGenerate_White_Noise,self.actionGenerate_Pink_Noise]

        for act in processing_actions_list:
            act.setActionGroup(processing_actions)

        # endregion

        # region Save Images actions
        save_images_actions = QActionGroup(self)
        save_images_actions_list = [self.actionOsc_Image,self.actionSpecgram_Image,
                                   self.actionCombined_Image]

        for act in save_images_actions_list:
            act.setActionGroup(save_images_actions)
        # endregion

        # region Save actions
        save_actions = QActionGroup(self)
        save_actions_list = [self.actionSave,self.actionSave_selected_interval_as,
                             self.actionOpen_Selection, self.actionSaveAs]

        for act in save_actions_list:
            act.setActionGroup(save_actions)
        # endregion

        # region Tools actions
        tools_actions = QActionGroup(self)
        tools_actions_list = [self.actionZoom_Cursor,self.actionPointer_Cursor,
                              self.actionRectangular_Cursor,self.actionRectangular_Eraser]

        for act in tools_actions_list:
            act.setActionGroup(tools_actions)
        # endregion

        # endregion

        # add the actions to the signalDependingActions list
        for action_group in [edition_actions, play_record_actions,save_actions, tools_actions,
                             widgets_visibility_actions,zoom_actions, undo_redo_actions,
                             segm_transf_actions, save_images_actions,processing_actions]:

            self.signalDependingActions.extend(action_group.actions())

        # actions groups (action,name of group)
        actions_groups = [(open_save_actions, self.tr(u"Open/Save")),(undo_redo_actions, self.tr(u"Undo/Redo")),
                          (edition_actions,self.tr(u"Edition")),(play_record_actions, self.tr(u"Play/Record")),
                          (zoom_actions, self.tr(u"Zoom")),(widgets_visibility_actions, self.tr(u"Widgets Visibility")),
                          (file_updown_actions, self.tr(u"File Up/Down")), (segm_transf_actions, self.tr(u"Processing"))]

        # add to the customizable sound lab toolbar
        for act in actions_groups:
            #            addActionGroup(actionGroup, name)
            self.toolBar.addActionGroup(act[0], act[1])

        # add other signal depending actions that not belong to any group
        self.toolBar.addAction(self.actionSettings)
        self.toolBar.addWidget(self.signalNameLineEdit)

        self.signalDependingActions.append(self.signalNameLineEdit)

    def setSignalActionsEnabledState(self, enable_state=True):
        """
        Set the enabled state to the action that depends of at least one signal
        opened to be performed.
        :param enable: The enable state to set
        :return:
        """
        for action in self.signalDependingActions:
            action.setEnabled(enable_state)

    # endregion

    # region TAB Multiple Files Handling

    def addSignalTab(self, signal):
        """
        Add a tab to open a new signal
        :param signal: The signal to open in the new tab
        :return:
        """
        self.tabOpenedSignals.addTab(QSignalVisualizerWidget(self), signal.name)
        self.tabOpenedSignals.setCurrentIndex(self.tabOpenedSignals.count()-1)
        self.loadSignalOnTab(signal)

        # if is the first signal to open close the "No opened signals widget"
        if self.tabOpenedSignals.count() == 1:
            self.setNoSignalsOpenState(signals_open=True)

    def loadSignalOnTab(self, signal, tabIndex=None):
        """
        Load a signal in the current widget tab
        :param signal: The signal to load
        :param tabIndex: The tab index in which the signal would be loaded. If None then is
        the current tab
        :return:
        """
        if tabIndex is not None:
            # ensure the index is inside the allowed interval
            if 0 > tabIndex or tabIndex >= self.tabOpenedSignals.count():
                return

            # select the tab at 'tabIndex' position
            if tabIndex != self.tabOpenedSignals.currentIndex():
                self.tabOpenedSignals.setCurrentIndex(tabIndex)

        self.widget.signal = signal
        self.widget.graph()

        # connect the histogram
        self.hist = self.widget.axesSpecgram.histogram

        # connect for data display
        self.widget.toolDataDetected.connect(self.updateStatusBar)

        # refresh and set the visibility of the axes on the new widget
        self.changeWidgetsVisibility(True, True)

        self.widget.load_Theme(self._appSettings['Workspace'].workTheme)

        # update the app title, tab text and signal properties label
        self.signalNameChanged(self.widget.signalName())
        self.updateSignalPropertiesLabel()

        # add context menu actions
        self.addWidgetContextMenuActions()

    def signalNameChanged(self, new_name):
        """
        Update the window variables dependent of the signal name when a change is made
        on the text line edit for the signal name.
        :param new_name: The new signal name
        :return:
        """
        self.setWindowTitle(self.tr(u"duetto-Sound Lab - ") + new_name)
        self.tabOpenedSignals.setTabText(self.tabOpenedSignals.currentIndex(), new_name)
        if self.widget is not None:
            self.widget.signal.name = new_name

    def currentSignalTabChanged(self,tabIndex):
        """
        Update the window state and variables when the current signal tab has changed
        :param tabIndex: The new index of selected tab signal
        :return:
        """
        # when there is no tab in the tab widget in
        # the documentation says the index raised is -1
        if tabIndex < 0:
            return

        # update the app title and signal properties label
        self.setWindowTitle(self.tr(u"duetto-Sound Lab - ") + self.widget.signalName())
        self.updateSignalPropertiesLabel()

        # update the tool selected
        tool = self.widget.selectedTool
        self.deselectToolsActions()

        if tool == Tools.ZoomTool:
            self.actionZoom_Cursor.setChecked(True)

        elif tool == Tools.PointerTool:
            self.actionPointer_Cursor.setChecked(True)

        elif tool == Tools.RectangularZoomTool:
            self.actionRectangular_Cursor.setChecked(True)

        # update the theme on the new selected widget
        self.widget.load_Theme(self.workTheme)
        self.widget.graph()

    def closeSignalAt(self, index):
        """
        Close the tab with signal at tab index index
        :param index: index of the tab signal to close.
        :return:
        """
        if index < 0 or index >= self.tabOpenedSignals.count():
            return

        self.save_signal_if_modified(signal_index=index)
        self.tabOpenedSignals.removeTab(index)

        # if close the last opened signal show the widget for no opened signals
        if self.tabOpenedSignals.count() == 0:
            self.setNoSignalsOpenState(signals_open=False)

    def closeAllTabs(self, exceptIndex=-1):
        """
        Close the signals on all the opened tabs
        :param exceptIndex: Signal tab index to not close.
        :return:
        """
        # close all the signals
        for i in range(self.tabOpenedSignals.count()-1, -1, -1):
            if i != exceptIndex:
                self.closeSignalAt(i)

    # endregion

    # region Properties

    @property
    def widget(self):
        """
        Gets the current widget selected or None if no signal is opened
        :return:
        """
        if self.tabOpenedSignals.count() == 0:
            return None

        return self.tabOpenedSignals.currentWidget()

    @property
    def workTheme(self):
        """
        Gets the current working theme selected
        :return:
        """
        return self._appSettings['Workspace'].workTheme

    # endregion

    #  region Segmentation And Clasification

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
            print("Error al deserializar los datos de clasificacion. " + ex.message)
            #  return a default
            return ClassificationData()

    @pyqtSlot()
    def on_actionSegmentation_And_Clasification_triggered(self):
        """
        Open the signal selected in the segmentation and classification window
        :return:
        """
        #  get the signal to analyze in segmentation window
        #  could be the currently visible signal or the selected by zoom tool

        signal = self.widget.signal

        indexFrom, indexTo = self.widget.selectedRegion

        if indexTo > indexFrom:
            signal = signal.copy(indexFrom, indexTo)

        # check if the signal can be analyzed acording to its
        # duration and the max duration signal allowed
        if signal.duration > self.MAX_SIGNAL_DURATION_ALLOWED:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"),
                                      self.tr(u"The signal is larger than the maximum duration allowed.") + " \n" +
                                      self.tr(u"Use the splitter to divide it"))
            return

        segWindow = SegmentationAndClasificationWindow(parent=self, signal=signal,
                                                       classifcationSettings=self.classificationData)

        # load the theme and clear the undo redo actions in the current window.
        segWindow.load_Theme(self.workTheme)
        self.widget.undoRedoManager.clear()

    #  endregion

    #  region Theme
    @pyqtSlot()
    def on_actionSaveTheme_triggered(self):
        """
        Save to disc the current theme with the visual options.
        """

        selected_theme = self.ParamTree.param(unicode(self.tr(u'Themes'))).param(
            unicode(self.tr(u'Theme Selected'))).value()

        theme_path = os.path.join("Utils", "Themes", selected_theme + ".dth")

        self.serializeTheme(theme_path)

    @pyqtSlot()
    def on_actionSaveThemeAs_triggered(self):
        """
        Save to disc the current theme with the visual options.
        """
        filename = QFileDialog.getSaveFileName(parent=self, caption=self.tr(u"Save Theme"),
                                               directory=os.path.join(u"Utils", u"Themes"),
                                               filter=self.tr(u"duetto Theme Files") + u"(*.dth);;All Files (*)")
        if filename:
            self.serializeTheme(filename)

    def _updateParamTree(self):
        """
        Updates the values of the param tree to match those of the current workspace. It blocks the param tree signals
        momentarily to avoid triggering any action other than updating the param tree.
        """
        self.ParamTree.blockSignals(True)

        self.ParamTree.param(unicode(self.tr(u'Oscillogram Settings')))\
            .param(unicode(self.tr(u'Amplitude(%)')))\
            .param(unicode(self.tr(u'Min')))\
            .setValue(int(self._appSettings['Workspace'].oscillogramWorkspace.minY * 100))
        self.ParamTree.param(unicode(self.tr(u'Oscillogram Settings')))\
            .param(unicode(self.tr(u'Amplitude(%)')))\
            .param(unicode(self.tr(u'Max')))\
            .setValue(int(self._appSettings['Workspace'].oscillogramWorkspace.maxY * 100))

        self.ParamTree.param(unicode(self.tr(u'Oscillogram Settings')))\
            .param(unicode(self.tr(u'Grid')))\
            .param(unicode(self.tr(u'X')))\
            .setValue(self._appSettings['Workspace'].oscillogramWorkspace.theme.gridX)
        self.ParamTree.param(unicode(self.tr(u'Oscillogram Settings')))\
            .param(unicode(self.tr(u'Grid')))\
            .param(unicode(self.tr(u'Y')))\
            .setValue(self._appSettings['Workspace'].oscillogramWorkspace.theme.gridY)

        self.ParamTree.param(unicode(self.tr(u'Oscillogram Settings')))\
            .param(unicode(self.tr(u'Background color')))\
            .setValue(self._appSettings['Workspace'].oscillogramWorkspace.theme.background_color)
        self.ParamTree.param(unicode(self.tr(u'Oscillogram Settings')))\
            .param(unicode(self.tr(u'Plot color')))\
            .setValue(self._appSettings['Workspace'].oscillogramWorkspace.theme.plot_color)
        self.ParamTree.param(unicode(self.tr(u'Oscillogram Settings')))\
            .param(unicode(self.tr(u'Connect Points')))\
            .setValue(self._appSettings['Workspace'].oscillogramWorkspace.theme.connectPoints)

        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings')))\
            .param(unicode(self.tr(u'Frequency(kHz)')))\
            .param(unicode(self.tr(u'Min')))\
            .setValue(self._appSettings['Workspace'].spectrogramWorkspace.minY / 1000.0)
        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings')))\
            .param(unicode(self.tr(u'Frequency(kHz)')))\
            .param(unicode(self.tr(u'Max')))\
            .setValue(self._appSettings['Workspace'].spectrogramWorkspace.maxY / 1000.0)

        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings')))\
            .param(unicode(self.tr(u'FFT size')))\
            .setValue(self._appSettings['Workspace'].spectrogramWorkspace.FFTSize)
        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings')))\
            .param(unicode(self.tr(u'FFT window')))\
            .setValue(self._appSettings['Workspace'].spectrogramWorkspace.FFTWindow)
        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings')))\
            .param(unicode(self.tr(u'FFT overlap')))\
            .setValue(self._appSettings['Workspace'].spectrogramWorkspace.FFTOverlap)

        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings')))\
            .param(unicode(self.tr(u'Threshold(dB)')))\
            .param(unicode(self.tr(u'Min')))\
            .setValue(self._appSettings['Workspace'].spectrogramWorkspace.theme.histRange[0])
        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings')))\
            .param(unicode(self.tr(u'Threshold(dB)')))\
            .param(unicode(self.tr(u'Max')))\
            .setValue(self._appSettings['Workspace'].spectrogramWorkspace.theme.histRange[1])

        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings')))\
            .param(unicode(self.tr(u'Grid')))\
            .param(unicode(self.tr(u'X')))\
            .setValue(self._appSettings['Workspace'].spectrogramWorkspace.theme.gridX)
        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings')))\
            .param(unicode(self.tr(u'Grid')))\
            .param(unicode(self.tr(u'Y')))\
            .setValue(self._appSettings['Workspace'].spectrogramWorkspace.theme.gridY)

        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings')))\
            .param(unicode(self.tr(u'Background color')))\
            .setValue(self._appSettings['Workspace'].spectrogramWorkspace.theme.background_color)

        self.ParamTree.param(unicode(self.tr(u'Detection Visual Settings')))\
            .param(unicode(self.tr(u'Measurement Location')))\
            .param(unicode(self.tr(u'Start')))\
            .setValue(self._appSettings['Workspace'].detectionWorkspace.theme.startColor)
        self.ParamTree.param(unicode(self.tr(u'Detection Visual Settings')))\
            .param(unicode(self.tr(u'Measurement Location')))\
            .param(unicode(self.tr(u'Quartile25')))\
            .setValue(self._appSettings['Workspace'].detectionWorkspace.theme.quart1Color)
        self.ParamTree.param(unicode(self.tr(u'Detection Visual Settings')))\
            .param(unicode(self.tr(u'Measurement Location')))\
            .param(unicode(self.tr(u'Center')))\
            .setValue(self._appSettings['Workspace'].detectionWorkspace.theme.centerColor)
        self.ParamTree.param(unicode(self.tr(u'Detection Visual Settings')))\
            .param(unicode(self.tr(u'Measurement Location')))\
            .param(unicode(self.tr(u'Quartile75')))\
            .setValue(self._appSettings['Workspace'].detectionWorkspace.theme.quart2Color)
        self.ParamTree.param(unicode(self.tr(u'Detection Visual Settings')))\
            .param(unicode(self.tr(u'Measurement Location')))\
            .param(unicode(self.tr(u'End')))\
            .setValue(self._appSettings['Workspace'].detectionWorkspace.theme.endColor)

        self.ParamTree.blockSignals(False)
        
    def updateTheme(self, theme):
        """
        Update the current selected theme with the values of the supplied new one.
        :param theme: The new Theme to load
        :return:
        """
        assert isinstance(theme, WorkTheme)
        #  change the current theme
        self._appSettings['Workspace'].workTheme = theme

        #  update the theme in the widget
        self.widget.load_Theme(theme)

        # update the param tree to show the values of the new theme
        self._updateParamTree()

    @pyqtSlot()
    def on_actionLoadTheme_triggered(self):
        """
        Load a new theme (previously saved) from disc.
        """
        filename = QFileDialog.getOpenFileName(parent=self, directory=os.path.join(u"Utils", u"Themes"),
                                               caption=self.tr(u"Load Theme"),
                                               filter=self.tr(u"duetto Theme Files") + u" (*.dth);;All Files (*)")
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
        :return: the instance of WorkTheme serialized into the file
        """
        assert filename, 'Invalid file path.'
        assert os.path.exists(filename), 'File does not exist.'

        with open(filename, 'r') as f:
            return pickle.load(f)

    def updateRegionTheme(self):
        """
        Updates the variables in the param tree and the work theme that represent the region of the histogram.
        """
        reg = self.hist.item.region.getRegion()
        # we only need to set the values to the param tree and it automatically calls the change method and does
        # everything else
        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
            unicode(self.tr(u'Threshold(dB)'))).param(unicode(self.tr(u'Min'))).setValue(reg[0])
        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
            unicode(self.tr(u'Threshold(dB)'))).param(unicode(self.tr(u'Max'))).setValue(reg[1])

    def histogramGradientChanged(self, gradient):
        """
        Updates the variables in the work theme that represent the gradient colors of the histogram.
        """
        # as the histogram is connected to the
        self._appSettings['Workspace'].spectrogramWorkspace.theme.colorBarState = gradient.saveState()

    def serializeTheme(self, filename):
        """
        Serialize a theme to a file.
        :param filename: the path to the file for the theme storage.
        """
        assert filename, 'Invalid file path.'
        #  get the histogram region and colorbar values
        #  self.workTheme.histRange = self.hist.item.region.getRegion()
        #  self.workTheme.colorBarState = self.hist.item.gradient.saveState()

        #  save theme to disc
        with open(filename, 'w') as f:
            pickle.dump(self._appSettings['Workspace'].workTheme, f)

    def change(self, param, changes):
        """
        Method that updates the internal variables and state of the widgets
        when a change is made in the visual options of the theme
        :param param: param
        :param changes: list with the changes in the param tree
        """
        for param, change, data in changes:
            path = self.ParamTree.childPath(param)
            if path is not None:
                childName = '.'.join(path)
            else:
                childName = param.name()

            if childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'FFT size')):
                self._appSettings['Workspace'].spectrogramWorkspace.FFTSize = data

            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'Grid')) + u"." + unicode(self.tr(u'X')):
                self._appSettings['Workspace'].spectrogramWorkspace.theme.gridX = data

            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'Grid')) + u"." + unicode(self.tr(u'Y')):
                self._appSettings['Workspace'].spectrogramWorkspace.theme.gridY = data

            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'Threshold(dB)')) + u"." + unicode(self.tr(u'Min')):
                if data > self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
                        unicode(self.tr(u'Threshold(dB)'))).param(unicode(self.tr(u'Max'))).value():
                    self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
                        unicode(self.tr(u'Threshold(dB)'))).param(unicode(self.tr(u'Min'))).setToDefault()
                    # self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
                    #     unicode(self.tr(u'Threshold(dB)'))).param(unicode(self.tr(u'Min'))).show()
                    # return
                self._appSettings['Workspace'].spectrogramWorkspace.theme.histRange = data, self.hist.item.region.getRegion()[1]

            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'Threshold(dB)')) + u"." + unicode(self.tr(u'Max')):
                if data < self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
                        unicode(self.tr(u'Threshold(dB)'))).param(unicode(self.tr(u'Min'))).value():
                    self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
                        unicode(self.tr(u'Threshold(dB)'))).param(unicode(self.tr(u'Max'))).setToDefault()
                    # self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
                    #     unicode(self.tr(u'Threshold(dB)'))).param(unicode(self.tr(u'Max'))).setValue()
                    # return
                self._appSettings['Workspace'].spectrogramWorkspace.theme.histRange = self.hist.item.region.getRegion()[0], data

            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'FFT window')):
                self._appSettings['Workspace'].spectrogramWorkspace.FFTWindow = data

            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'Background color')):
                self._appSettings['Workspace'].spectrogramWorkspace.theme.background_color = data
            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'Frequency(kHz)')) + u"." + \
                    unicode(self.tr(u'Min')):
                self._appSettings['Workspace'].spectrogramWorkspace.minY = data * 1000

            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'Frequency(kHz)')) + u"." + \
                    unicode(self.tr(u'Max')):
                self._appSettings['Workspace'].spectrogramWorkspace.maxY = data * 1000

            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'FFT overlap')):
                self._appSettings['Workspace'].spectrogramWorkspace.FFTOverlap = data / 100.0

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Background color')):
                self._appSettings['Workspace'].oscillogramWorkspace.theme.background_color = data

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Grid')) + u"." + \
                    unicode(self.tr(u'X')):
                self._appSettings['Workspace'].oscillogramWorkspace.theme.gridX = data

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Grid')) + u"." + \
                    unicode(self.tr(u'Y')):
                self._appSettings['Workspace'].oscillogramWorkspace.theme.gridY = data

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Plot color')):
                self._appSettings['Workspace'].oscillogramWorkspace.theme.plot_color = data

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Amplitude(%)')) + u"." + \
                    unicode(self.tr(u'Min')):
                self._appSettings['Workspace'].oscillogramWorkspace.minY = data / 100.0

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Amplitude(%)')) + u"." + \
                    unicode(self.tr(u'Max')):
                self._appSettings['Workspace'].oscillogramWorkspace.maxY = data / 100.0

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Connect Points')):
                self._appSettings['Workspace'].oscillogramWorkspace.theme.connectPoints = data

            elif childName == unicode(self.tr(u'Themes')) + u"." + \
                    unicode(self.tr(u'Theme Selected')):
                try:
                    self.updateTheme(self.deSerializeTheme(data))
                    return
                except Exception as e:
                    QMessageBox.warning(self, 'Error loading theme',
                                        'An error occurred while loading the theme.\nError:\n' + str(e))
            elif childName == unicode(self.tr(u'Style')) + u"." + \
                    unicode(self.tr(u'Style Selected')):
                self.styleChanged.emit(data)

            elif childName == unicode(self.tr(u'Language')) + u"." + \
                    unicode(self.tr(u'Language Selected')):
                self.languageChanged.emit(data)

            elif childName == unicode(self.tr(u'Tabs')) + u"." + \
                    unicode(self.tr(u'Tab Position')):
                self.tabOpenedSignals.setTabPosition(data)

            elif childName == unicode(self.tr(u'Tabs')) + u"." + \
                              unicode(self.tr(u'Tab Shape')):
                self.tabOpenedSignals.setTabShape(data)

        self.widget.load_workspace(self._appSettings['Workspace'])

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

    #  endregion

    #  region Drag and Drop file
    #  implementation of the events for drag and drop files into the window
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

        #  get the path from the url
        path = mimeUrl[1:len(mimeUrl)]

        #  open the signal in path if any
        self._open(path)

        #  accept the event
        event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        event.accept()

    #  endregion

    #  region Widget Tools
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

    #  endregion

    #  region Cut, Copy, Paste
    @pyqtSlot()
    def on_actionCut_triggered(self):
        self.widget.cut()

    @pyqtSlot()
    def on_actionCopy_triggered(self):
        self.widget.copy()

    @pyqtSlot()
    def on_actionPaste_triggered(self):
        self.widget.paste()

    #  endregion

    #  region Undo Redo

    @pyqtSlot()
    def on_actionUndo_triggered(self):
        self.widget.undo()

    @pyqtSlot()
    def on_actionRedo_triggered(self):
        self.widget.redo()

    # endregion

    #  region Signal Processing Methods

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
        scaleDialogWindow = ChangeVolumeDialog()

        if scaleDialogWindow.exec_():
            factor = scaleDialogWindow.spinboxConstValue.value()

            if scaleDialogWindow.rbuttonConst.isChecked():
                # scale by a constant factor
                self.widget.scale(factor)

            elif scaleDialogWindow.rbuttonNormalize.isChecked():
                # scale by normalize the signal to the factor amplitude
                factor = scaleDialogWindow.spinboxNormalizePercent.value()
                self.widget.normalize(factor)

            else:
                # scale by using a function
                function = scaleDialogWindow.cboxModulationType.currentText()
                fade = u"IN" if scaleDialogWindow.rbuttonFadeIn.isChecked() else u"OUT"
                self.widget.modulate(function, fade)

    @pyqtSlot()
    def on_actionInsert_Silence_triggered(self):
        """
        Insert an amount of silence time on the signal
        :return:
        """
        silenceDialogWindow = InsertSilenceDialog()

        if silenceDialogWindow.exec_():
            # get the time in ms to insert as silence
            ms = silenceDialogWindow.insertSpinBox.value()
            self.widget.insertSilence(ms)

    @pyqtSlot()
    def on_actionGenerate_Pink_Noise_triggered(self):
        """
        Insert a pink noise signal on the current analyzed signal
        :return:
        """
        # reuse the insert silence dialog
        whiteNoiseDialogWindow = InsertSilenceDialog()

        # change the label for the new task of insert pink noise
        whiteNoiseDialogWindow.label.setText(self.tr(u"Select the duration in ms") + " \n" + self.tr(u"of the Pink Noise."))

        # 1 second time by default
        whiteNoiseDialogWindow.insertSpinBox.setValue(1000)

        #  if whiteNoiseDialogWindow.exec_():
        #      type_, Fc, Fl, Fu = self.filter_helper()
        #      if type_ != None:
        #          ms = whiteNoiseDialog.insertSpinBox.value()
        #          start, _ = self.widget.selectedRegion
        #          self.widget.undoRedoManager.add(
        #              GeneratePinkNoiseAction(self.widget.signalProcessor.signal, start, ms, type_, Fc, Fl, Fu))
        #          self.widget.insertPinkNoise(ms, type_, Fc, Fl, Fu)

    @pyqtSlot()
    def on_actionGenerate_White_Noise_triggered(self):
        """
        Insert a white noise signal on the current analyzed signal
        :return:
        """
        # reuse the insert silence dialog
        whiteNoiseDialogWindow = InsertSilenceDialog()

        # change the label for the new task of insert white noise
        whiteNoiseDialogWindow.label.setText(self.tr(u"Select the duration in ms") + u" \n" + self.tr(u"of the White Noise."))

        # 1 second time by default
        whiteNoiseDialogWindow.insertSpinBox.setValue(1000)

        if whiteNoiseDialogWindow.exec_():
            ms = whiteNoiseDialogWindow.insertSpinBox.value()
            self.widget.insertWhiteNoise(ms)

    def filter_helper(self):
        """
        Open the filter dialog and returns the concrete
        filter implementation according to the user selection.
        :return:
        """
        filterDialogWindow = FilterDialog()

        # open the filter dialog
        if filterDialogWindow.exec_():
            #  Low Pass Filter
            if filterDialogWindow.rButtonLowPass.isChecked():
                # get the frequency of cut for the low pass filter
                # (the freq in the dialog are in kHz)
                freq_cut = filterDialogWindow.spinBoxLowPass.value() * 1000
                return LowPassFilter(self.widget.signal, freq_cut)

            #  High Pass Filter
            elif filterDialogWindow.rButtonHighPass.isChecked():
                # get the frequency of cut for the high pass filter
                freq_cut = filterDialogWindow.spinBoxHighPass.value() * 1000
                return HighPassFilter(self.widget.signal, freq_cut)

            #  Band Pass Filter
            elif filterDialogWindow.rButtonBandPass.isChecked():
                #  get the frequencies of cut (upper and lower)
                #  for the Band pass filter
                freq_cut_lower = filterDialogWindow.spinBoxBandPassFl.value() * 1000
                freq_cut_upper = filterDialogWindow.spinBoxBandPassFu.value() * 1000
                return BandPassFilter(self.widget.signal, freq_cut_lower, freq_cut_upper)

            #  Band Stop Filter
            elif filterDialogWindow.rButtonBandStop.isChecked():
                #  get the frequencies of cut (upper and lower)
                #  for the Band Stop filter
                freq_cut_lower = filterDialogWindow.spinBoxBandStopFl.value() * 1000
                freq_cut_upper = filterDialogWindow.spinBoxBandStopFu.value() * 1000
                return BandStopFilter(self.widget.signal, freq_cut_lower, freq_cut_upper)

                # None if there is no filter implementation selected
        return None

    @pyqtSlot()
    def on_actionFilter_triggered(self):
        """
        execute a filter on the signal
        :return:
        """
        filter_method = self.filter_helper()

        # if there is a filter selection made then execute the filter
        if filter_method is not None:
            self.widget.filter(filter_method)


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
        # reuse the insert silence dialog
        resamplingDialog = sdialog.Ui_Dialog()
        resamplingDialogWindow = InsertSilenceDialog(self)
        resamplingDialog.setupUi(resamplingDialogWindow)

        # change the label for the new task of resampling
        resamplingDialog.label.setText(self.tr(u"Select the new Sampling Rate."))

        # set by default the current sampling rate
        resamplingDialog.insertSpinBox.setValue(self.widget.signal.samplingRate)

        if resamplingDialogWindow.exec_():
            # get the new sampling rate
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

    # endregion

    #  region Zoom IN, OUT, NONE
    # delegate the task of zoom in, out and none
    # in the widget operations
    @pyqtSlot()
    def on_actionZoomIn_triggered(self):
        self.widget.zoomIn()

    @pyqtSlot()
    def on_actionZoom_out_triggered(self):
        self.widget.zoomOut()

    @pyqtSlot()
    def on_actionZoom_out_entire_file_triggered(self):
        self.widget.zoomNone()

    # endregion

    #  region Open, Close and Save

    def on_load_first_time(self):
        """
        Method called when the window is first opened.
        It prompts the user whether to restore the last working session
        and initializes stuffs accordingly.
        """
        if os.path.exists('duetto.ini'):
            try:
                with open('duetto.ini', 'r') as f:
                    settings = pickle.load(f)
            except:
                QMessageBox.warning(self, self.tr(u'Error loading application settings.'),
                                    self.tr(u'An error occurred when loading some application settings. Default '
                                            u'settings will be applied but some information might have been lost.'))

                self._appSettings = {'Workspace': Workspace(),
                                     'RecentFiles': []}
                return

            self._appSettings = settings

            answer = QMessageBox.question(self, self.tr(u'Restore workspace?'),
                                          self.tr(u'Do you wish to restore the state of the last work session?'),
                                          QMessageBox.Yes | QMessageBox.No)
            if answer == QMessageBox.Yes:
                try:
                    self._open(self._appSettings['Workspace'].openedFile)
                except:
                    QMessageBox.warning(self, self.tr(u'Error restoring workspace.'),
                                        self.tr(u'An error occurred when restoring the workspace. The default state '
                                                u'will be loaded instead.'))
                else:
                    return

            self._appSettings['Workspace'] = Workspace()

    @pyqtSlot()
    def on_actionExit_triggered(self):
        self.close()

    def closeEvent(self, event):
        """
        Event for close. Release the resources and save changes.
        :param event:
        :return:
        """

        #  save the signal if any opened and changed
        for i in range(self.tabOpenedSignals.count()):
            self.save_signal_if_modified(event, signal_index=i)

        #  close the window
        self.close()

    @pyqtSlot()
    def on_actionClose_triggered(self, signal_index=None):
        """
        Action to close the current analyzed signal.
        :param signal_index: The index of the signal tab to close
        :return:
        """
        signal_index = self.tabOpenedSignals.currentIndex() if signal_index is None else signal_index
        # save the signal if any change
        self.save_signal_if_modified(signal_index)

        self.closeSignalAt(signal_index)

    @pyqtSlot()
    def on_actionCloseAll_triggered(self):
        """
        Close all the signals opened
        :return:
        """
        self.closeAllTabs()

    @pyqtSlot()
    def on_actionCloseOthers_triggered(self, signal_index=None):
        """
        Close the signals on tabs different that the index supplied
        :param signal_index: The index of the signal tab to close
        :return:
        """
        signal_index = self.tabOpenedSignals.currentIndex() if signal_index is None else signal_index
        self.closeAllTabs(exceptIndex=signal_index)

    @pyqtSlot()
    def on_actionCloseUnmodified_triggered(self):
        """
        Close the signals that not have been changed
        :return:
        """

        # delete the signals at indexes from greater to lower to avoid
        # change index values in the process
        for i in range(self.tabOpenedSignals.count()-1, -1, -1):
            try:

                if self.tabOpenedSignals.widget(i).undoRedoManager.count() == 0:
                    self.closeSignalAt(i)

            except Exception as ex:
                print("Error closing signal at index "+str(i) + " " + ex.message)

    @pyqtSlot()
    def on_actionNew_triggered(self):
        """
        create a new signal by syntetizer and open it in the widget.
        :return:
        """
        new_file_dialog = NewFileDialog(parent=self)

        # excute the dialog of new signals generation
        if new_file_dialog.exec_():
            if new_file_dialog.rbtnSilence.isChecked():
                signal = Synthesizer.generateSilence(new_file_dialog.SamplingRate, new_file_dialog.BitDepth,
                                                     new_file_dialog.Duration * 1000)
            elif new_file_dialog.rbtnWhiteNoise.isChecked():
                signal = Synthesizer.insertWhiteNoise(
                    AudioSignal(new_file_dialog.SamplingRate, new_file_dialog.BitDepth, 1),
                    new_file_dialog.Duration*1000)

            self.addSignalTab(signal)

    @pyqtSlot()
    def on_actionOpen_triggered(self):
        """
        Open a new file signal.
        :return:
        """
        file_name = QFileDialog.getOpenFileName(self, self.tr(u"Select a file to open"),
                                                directory=self.last_opened_signal_path,
                                                filter=self.tr(u"Wave Files") + u"(*.wav);;All Files(*)")
        self._open(unicode(file_name))

    @pyqtSlot()
    def on_actionOpenInOtherTab_triggered(self):
        """
        Open the current selected signal on the tab widget into another tab.
        :return:
        """
        signal = self.widget.signal.copy()

        self.addSignalTab(signal)

    @pyqtSlot()
    def on_actionBrowse_triggered(self):
        """
        :return:
        """
        browse_wnd = BrowseFilesWindow(self,self.filesInFolder)

        # connect the signals for open in the current window
        browse_wnd.openFiles.connect(self.open_files)

    def open_files(self, pathlist):
        """
        Open several files at same time.
        :param pathlist:
        :return:
        """
        # open in the current tab just the first of the signals otherwise would
        # be opened just one tab
        for i, path in enumerate(pathlist):
            self._open(path, currentTab=(i == 0))

    def _open(self, file_path='', currentTab=False):
        """
        Method that open a signal from a file path
        :param file_path: The path to the signal on disc
        :param currentTab: If true open the new signal on the current tab
        otherwise is open on new tab
        :return:
        """
        if file_path != u'':
            try:
                # set the variables for folder files management
                self.last_opened_signal_path = file_path
                self.getFolderFiles(file_path)
                signal = openSignal(file_path)
            except Exception as ex:
                QMessageBox.warning(QMessageBox(), self.tr(u"Error"),
                                    self.tr(u"Could not load the file.") +
                                    u"\n" + file_path)
                print(ex.message)


                # recover from an open error by opening a default signal
                signal = Synthesizer.generateSilence(44100, 16, 1)

            if currentTab and self.tabOpenedSignals.count() > 0:
                self.loadSignalOnTab(signal)
            else:
                self.addSignalTab(signal)


            self.changeFrequency(0, self.widget.signal.samplingRate / 2000)
            self.changeAmplitude(-100, 100)

            # select the zoom tool as default
            self.on_actionZoom_Cursor_triggered()

    def save_signal_if_modified(self, event=None, signal_index=None):
        """
        Method that save the current tab signal to disc if there was made some change on it.
        :param event: The close event if the next action is to close the window.
        Is used to reject the event if the user wants to cancel the save operation.
        :param signal_index: The index of the signal tab to save
        :return:
        """
        signal_index = self.tabOpenedSignals.currentIndex() if signal_index is None else signal_index
        widget = self.tabOpenedSignals.widget(signal_index)

        if widget.undoRedoManager.count() > 0:
            # if any action was made then ask for save the signal
            buttons_box = QtGui.QMessageBox.Yes | QtGui.QMessageBox.No

            if event is not None:
                buttons_box = buttons_box | QtGui.QMessageBox.Cancel

            mbox = QtGui.QMessageBox(QtGui.QMessageBox.Question, self.tr(u"Save"),
                                     self.tr(u"Do you want to save the signal " + widget.signalName() + u" ?"),
                                     buttons_box, self)
            result = mbox.exec_()

            if result == QtGui.QMessageBox.Yes:
                self.on_actionSave_triggered(signal_index)

            elif result == QtGui.QMessageBox.Cancel and event is not None:
                event.ignore()

    @pyqtSlot()
    def on_actionSave_triggered(self, signal_index=None):
        """
        Save the signal currently analyzed into disc
        :param signal_index: The index of the signal tab to save
        :return:
        """
        signal_index = self.tabOpenedSignals.currentIndex() if signal_index is None else signal_index
        widget = self.tabOpenedSignals.widget(signal_index)

        if widget.signalFilePath is not None:
            widget.save()
        else:
            self.on_actionSaveAs_triggered(signal_index)

    @pyqtSlot()
    def on_actionSaveAs_triggered(self, signal_index=None):
        """
        Save the signal currently analyzed into disc
        :param signal_index: The index of the signal tab to save
        :return:
        """
        signal_index = self.tabOpenedSignals.currentIndex() if signal_index is None else signal_index
        widget = self.tabOpenedSignals.widget(signal_index)

        # get the filename to store the signal
        file_name = unicode(QFileDialog.getSaveFileName(self, self.tr(u"Save signal"),
                                                        widget.signalName(), u"*.wav"))
        if file_name:
            widget.save(file_name)

    @pyqtSlot()
    def on_actionSave_selected_interval_as_triggered(self, signal_index=None):
        """
        Save the signal currently visible (or selected) into disc  as a new signal
        :param signal_index: The index of the signal tab to save
        :return:
        """
        signal_index = self.tabOpenedSignals.currentIndex() if signal_index is None else signal_index
        widget = self.tabOpenedSignals.widget(signal_index)

        #  get the filename to store the new signal
        file_name = unicode(QFileDialog.getSaveFileName(self, self.tr(u"Save signal"),
                                                        self.tr(u"Selection-") +
                                                        widget.signalName(), u"*.wav"))
        if file_name:
            widget.saveSelectedSectionAsSignal(file_name)


    @pyqtSlot()
    def on_actionOpen_Selection_triggered(self, signal_index=None):
        """
        Open the signal currently visible (or selected) into a new tab
        :param signal_index: The index of the signal tab to open on a new tab
        :return:
        """
        signal_index = self.tabOpenedSignals.currentIndex() if signal_index is None else signal_index
        widget = self.tabOpenedSignals.widget(signal_index)

        indexFrom, indexTo = self.widget.selectedRegion
        self.addSignalTab(widget.signal.copy(indexFrom, indexTo))

    # endregion

    # region Signal Properties Info Display

    def updateSignalPropertiesLabel(self):
        """
        Updates the text of the current signal properties in toolbar.
        :return:
        """
        #  action signal is a place in the tool bar to show the current signal name
        self.signalNameLineEdit.setText(self.widget.signalName())

        sr = self.widget.signal.samplingRate
        bit_depth = self.widget.signal.bitDepth
        channels = self.widget.signal.channelCount

        tooltip = "Sampling Rate: " + str(sr) + \
                  "\nBit Depth: " + str(bit_depth) + \
                  "\nChannels: " + str(channels) + \
                  "\nDuration(s): " + str(round(self.widget.signal.duration, DECIMAL_PLACES))

        self.signalNameLineEdit.setToolTip(tooltip)

    # endregion

    #  region Folder Files UP and DOWN manipulation
    # a way to browse for the signal files of a folder
    # by a simple and user friendly mechanism
    @pyqtSlot()
    def on_actionFile_Up_triggered(self):
        """
        open the previous file signal in the folder that is been analyzed
        :return:
        """
        if self.filesInFolderIndex > 0:
            # if there is files in the folder to be opened
            # or the current file signal is not the first on the folder
            self.filesInFolderIndex -= 1

            # try to open the file in the new signal file path
            if os.path.exists(self.filesInFolder[self.filesInFolderIndex]):
                self._open(self.filesInFolder[self.filesInFolderIndex],currentTab=True)

    @pyqtSlot()
    def on_actionFile_Down_triggered(self):
        """
        open the next file signal in the folder that is been analyzed
        :return:
        """
        if self.filesInFolderIndex < len(self.filesInFolder) - 1:
            # if the current file signal is not the last on the folder
            self.filesInFolderIndex += 1

            #  try to open the file in the new signal file path
            if os.path.exists(self.filesInFolder[self.filesInFolderIndex]):
                self._open(self.filesInFolder[self.filesInFolderIndex], currentTab=True)

    def getFolderFiles(self, file_path):
        """
        Get all the paths to files in the folder where file_path is.
        :param file_path: The path to a file that is on the folder desired.
        :return:
        """
        try:
            #  get the folder of the path and the files on that folder.
            path_base = os.path.split(file_path)[0]
            self.filesInFolder = folderFiles(path_base)

            # set the current index to the index of the supplied file_path
            self.filesInFolderIndex = self.filesInFolder.index(file_path)
        except:
            # if somethign wrong go to the initial state
            self.filesInFolder = []
            self.filesInFolderIndex = -1

    # endregion

    #  region Play, Pause, Stop, Record
    # delegate in the widget the reproduction actions

    @pyqtSlot()
    def on_actionSound_Devices_triggered(self):
        """
        Open a dialog to select the audio devices for input and output
        :return:
        """
        # active devices
        input_devices = DevicesHandler.getInputDevices()
        output_devices = DevicesHandler.getOutputDevices()

        dialog = SoundDevicesDialog(input_devices, output_devices)

        if dialog.exec_():
            self.widget.inputDevice = input_devices[dialog.inputDeviceIndex]


            for index in range(len(output_devices)):
                if dialog.grpBoxOutput.findChild(QtGui.QRadioButton, str(index)).isChecked():
                    self.widget.outputDevice = output_devices[index]
                    break

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
    def on_actionSwitchPlayStatus_triggered(self):
        """
        Change the play status of the signal from play-pause and vice versa
        :return:
        """
        print("Stwich Play status")
        self.widget.switchPlayStatus()

    @pyqtSlot(QAction)
    def on_playSpeedChanged_triggered(self, action):
        """
        Change the play speed of the signal.
        :param action: the action to set the speed
        :return:
        """

        # stop prevoiusly playing or recording at other speed.

        if self.widget is not None:
            self.widget.stop()

        #  the speed is get form the text of the action (?? it is possible to improve it ??)
        speed = {u'1/8x': 12.5, u'1/4x': 25, u'1/2x': 50,
                 u'1x': 100, u'2x': 200, u'4x': 400, u'8x': 800}[unicode(action.text())]

        self.widget.playSpeed = speed

    # endregion

    #  region Widgets And Window Visibility

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

    def changeWidgetsVisibility(self, visibleOscilogram=True, visibleSpectrogram=True):
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

    # endregion

    #  region Save widgets Image

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

    #  endregion

    #  region One dimensional Transforms
    def updateOneDimWindow(self):
        """
        Update the current interval of visualization/processing
        of the signal in the opened one dimensional windows
        :return:
        """
        indexFrom, indexTo = self.widget.selectedRegion
        for win in self.one_dim_windows:
            win.graph(indexFrom, indexTo)

    @pyqtSlot()
    def on_actionPower_Spectrum_triggered(self):
        """
        Create a one dimensional one_dim_transform window and show it.
        :return:
        """

        one_dim_window = OneDimensionalAnalysisWindow(self,self.widget.signal)
        one_dim_window.load_Theme(self.workTheme.oscillogramTheme)

        indexFrom, indexTo = self.widget.selectedRegion
        one_dim_window.graph(indexFrom, indexTo)

        #  store the opened one dimensional one_dim_transform windows for handling
        self.one_dim_windows.append(one_dim_window)

    #  endregion

    def updateStatusBar(self, line):
        """
        Update the status bar window message.
        :param line: The (string) to show as message
        :return: None
        """
        self.statusbar.showMessage(line)

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