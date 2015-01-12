#  -*- coding: utf-8 -*-
import os
import pickle
from duetto.audio_signals import AudioSignal, openSignal
from PyQt4 import QtGui,QtCore
from duetto.audio_signals.Synthesizer import Synthesizer
from duetto.signal_processing.filter_signal_processors.frequency_domain_filters import BandPassFilter, HighPassFilter, \
    BandStopFilter, LowPassFilter
from graphic_interface.widgets.signal_visualizer_tools.SignalVisualizerTool import Tools
from pyqtgraph.parametertree.parameterTypes import ListParameter
from pyqtgraph.parametertree import Parameter, ParameterTree
from PyQt4.QtGui import QDialog, QMessageBox, QFileDialog, QActionGroup, QAction
from PyQt4.QtCore import pyqtSlot, QMimeData, pyqtSignal, QTimer, QTranslator, QFile, QIODevice, QString
from duetto.dimensional_transformations.two_dimensional_transforms.Spectrogram.WindowFunctions import WindowFunction
from Utils.Utils import folderFiles,saveImage
from graphic_interface.widgets.QSignalVisualizerWidget import QSignalVisualizerWidget
from graphic_interface.windows.ParameterList import DuettoListParameterItem
from graphic_interface.dialogs.NewFileDialog import NewFileDialog
from graphic_interface.windows.OneDimensionalAnalysisWindow import OneDimensionalAnalysisWindow
from SegmentationAndClasificationWindow import SegmentationAndClasificationWindow
from graphic_interface.windows.Theme.WorkTheme import WorkTheme
from graphic_interface.windows.ui_python_files.MainWindow import Ui_DuettoMainWindow
from graphic_interface.dialogs import insertSilence as sdialog, FilterOptionsDialog as filterdg, \
    ChangeVolumeDialog as cvdialog
from sound_lab_core.Clasification.ClassificationData import ClassificationData
from graphic_interface.widgets.signal_visualizer_tools.SignalVisualizerTool import Tools


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

    #  SIGNALS
    #  signal raised when a file is drop into the window
    dropchanged = pyqtSignal(QMimeData)

    # signal raised when the user change the application language
    # raise the new language file path
    languageChanged = pyqtSignal(str)

    # signal raised when the user change the application style
    # raise the new style path
    styleChanged = pyqtSignal(str)

    #  CONSTANTS
    #  minimum and maximum sampling rate used on the application
    MIN_SAMPLING_RATE = 1000
    MAX_SAMPLING_RATE = 2000000

    # the max duration of signal that is possible to process
    # with the segmentation and classification window (in seconds)
    MAX_SIGNAL_DURATION_ALLOWED = 60

    #  Width and height of the dock window of visual options
    SETTINGS_WINDOW_WIDTH = 340
    SETTINGS_WINDOW_HEIGHT = 100

    # region Initialize

    def __init__(self, parent=None, signal_path=''):
        """
        :param parent:
        :param signal_path: Optional Signal path to open
        :return:
        """
        super(DuettoSoundLabWindow, self).__init__(parent)
        self.setupUi(self)

        #  theme for the visual options
        theme_path = os.path.join("Utils", "Themes", "default.dth")
        try:
            self.workTheme = self.deSerializeTheme(theme_path)
        except Exception as e:
            self.workTheme = WorkTheme()
            QMessageBox.warning(self, 'Error loading theme',
                                'An error occurred while loading the theme. A default theme will be loaded instead.\n' +
                                'Error: ' + str(e))

        # open a signal if any
        if signal_path == '':
            self.on_load()
        else:
            self._open(signal_path)


        self.configureSignalsTab()

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

        # self.showMaximized()
        #
        self.configureToolBarActionsGroups()

    def configureSignalsTab(self):
        """
        Set the starting setting of the signal tab to start execution
        :return:
        """
        # connect the signals for the changed tab and close tab events
        self.tabOpenedSignals.currentChanged.connect(self.currentSignalTabChanged)
        self.tabOpenedSignals.tabCloseRequested.connect(self.closeSignalAt)

        # add the tab context menu
        self.tabOpenedSignals.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        actions = [self.actionClose,self.actionCloseAll,self.actionCloseOthers, self.actionCloseUnmodified]
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
                    {u'name': u'X', u'type': u'bool', u'default': self.workTheme.oscillogramTheme.gridX,
                     u'value': self.workTheme.oscillogramTheme.gridX},
                    {u'name': u'Y', u'type': u'bool', u'default': self.workTheme.oscillogramTheme.gridY,
                     u'value': self.workTheme.oscillogramTheme.gridY},

                ]},
                {u'name': unicode(self.tr(u'Background color')), u'type': u'color',
                 u'value': self.workTheme.oscillogramTheme.background_color,
                 u'default': self.workTheme.oscillogramTheme.background_color},
                {u'name': unicode(self.tr(u'Plot color')), u'type': u'color',
                 u'value': self.workTheme.oscillogramTheme.plot_color,
                 u'default': self.workTheme.oscillogramTheme.plot_color},
                {u'name': unicode(self.tr(u'Connect Points')), u'type': u'bool',
                 u'default': self.workTheme.oscillogramTheme.connectPoints,
                 u'value': self.workTheme.oscillogramTheme.connectPoints},
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
                 u'value': WindowFunction.Rectangular,
                 u'default': WindowFunction.Rectangular,
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
                     u'default': self.workTheme.spectrogramTheme.histRange[0],
                     u'value': self.workTheme.spectrogramTheme.histRange[0]},
                    {u'name': unicode(self.tr(u'Max')), u'type': u'int', u'step': 1,
                     u'default': self.workTheme.spectrogramTheme.histRange[1],
                     u'value': self.workTheme.spectrogramTheme.histRange[1]},
                ]},
                {u'name': unicode(self.tr(u'Grid')), u'type': u'group', u'children': [
                    {u'name': u'X', u'type': u'bool', u'default': self.workTheme.spectrogramTheme.gridX,
                     u'value': self.workTheme.spectrogramTheme.gridX},
                    {u'name': u'Y', u'type': u'bool', u'default': self.workTheme.spectrogramTheme.gridY,
                     u'value': self.workTheme.spectrogramTheme.gridY},

                ]},
                {u'name': unicode(self.tr(u'Background color')), u'type': u'color',
                 u'value': self.workTheme.spectrogramTheme.background_color,
                 u'default': self.workTheme.spectrogramTheme.background_color},
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
                     u'value': self.workTheme.detectionTheme.startColor,
                     u'default': self.workTheme.detectionTheme.startColor},
                    {u'name': unicode(self.tr(u'Quartile25')), u'type': u'color',
                     u'value': self.workTheme.detectionTheme.quart1Color,
                     u'default': self.workTheme.detectionTheme.quart1Color},
                    {u'name': unicode(self.tr(u'Center')), u'type': u'color',
                     u'value': self.workTheme.detectionTheme.centerColor,
                     u'default': self.workTheme.detectionTheme.centerColor},
                    {u'name': unicode(self.tr(u'Quartile75')), u'type': u'color',
                     u'value': self.workTheme.detectionTheme.quart2Color,
                     u'default': self.workTheme.detectionTheme.quart2Color},
                    {u'name': unicode(self.tr(u'End')), u'type': u'color',
                     u'value': self.workTheme.detectionTheme.endColor,
                     u'default': self.workTheme.detectionTheme.endColor},
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
        # actions = [self.actionClose,  self.actionCloseOthers]

        # create the separators for the context menu
        sep1, sep2, sep3, sep4, sep5 = [QtGui.QAction(self) for _ in range(5)]

        for sep in [sep1, sep2, sep3, sep4, sep5]:
            sep.setSeparator(True)

        # add actions to the context menu
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

    def configureToolBarActionsGroups(self):
        """
        Configure the actions into groups for best visualization and
        user configuration.
        :return:
        """
        # region Add actions groups
        # create the separators for the actions
        sep1, sep2, sep3, sep4, sep5, sep6, sep7 = [QtGui.QAction(self) for _ in range(7)]

        for sep in [sep1, sep2, sep3, sep4, sep5, sep6, sep7]:
            sep.setSeparator(True)

        # open save actions
        open_save_actions = QActionGroup(self)
        open_save_actions_list = [self.actionNew, self.actionOpen, self.actionSave, sep1]

        self.toolBar.addActions(open_save_actions_list)
        for act in open_save_actions_list:
            act.setActionGroup(open_save_actions)

        # edition actions
        edition_actions = QActionGroup(self)
        edition_actions_list = [self.actionCopy, self.actionPaste, self.actionCut, sep2]

        self.toolBar.addActions(edition_actions_list)
        for act in edition_actions_list:
            act.setActionGroup(edition_actions)

        # play record actions
        play_record_actions = QActionGroup(self)
        play_record_actions_list = [self.actionPlay_Sound, self.actionPause_Sound, self.actionStop_Sound,
                                    self.actionRecord, sep3]

        self.toolBar.addActions(play_record_actions_list)
        for act in play_record_actions_list:
            act.setActionGroup(play_record_actions)

        # widgets visibility actions
        widgets_visibility_actions = QActionGroup(self)
        widgets_visibility_actions_list = [self.actionOscilogram, self.actionSpectogram, self.actionCombined,
                                           sep4]

        self.toolBar.addActions(widgets_visibility_actions_list)
        for act in widgets_visibility_actions_list:
            act.setActionGroup(widgets_visibility_actions)

        # undo redo actions
        undo_redo_actions = QActionGroup(self)
        undo_redo_actions_list = [self.actionUndo, self.actionRedo,sep5]

        self.toolBar.addActions(undo_redo_actions_list)
        for act in undo_redo_actions_list:
            act.setActionGroup(undo_redo_actions)

        # zoom actions
        zoom_actions = QActionGroup(self)
        zoom_actions_list = [self.actionZoomIn, self.actionZoom_out,
                                  self.actionZoom_out_entire_file,sep6]

        self.toolBar.addActions(zoom_actions_list)
        for act in zoom_actions_list:
            act.setActionGroup(zoom_actions)

        # File up down actions
        file_updown_actions = QActionGroup(self)
        file_updown_actions_list = [self.actionFile_Up, self.actionFile_Down, sep7]

        self.toolBar.addActions(file_updown_actions_list)
        for act in file_updown_actions_list:
            act.setActionGroup(file_updown_actions)

        # endregion

        # actions groups (action,name)

        actions_groups = [(edition_actions,"Edition"), (open_save_actions, "Open/Save"),
                          (play_record_actions, "Play/Record"), (zoom_actions, "Zoom"),
                          (widgets_visibility_actions, "Widgets Visibility"),
                          (undo_redo_actions, "Undo/Redo"), (file_updown_actions, "File Up/Down")]

        # add the way to change visibility on toolbar context menu
        for act in actions_groups:
            self.toolBar.addActionGroup(act[0], act[1])

        self.toolBar.addAction(self.actionSettings)
        self.toolBar.addAction(self.actionOneDimensionalTransformation)
        self.toolBar.addAction(self.actionSegmentation_And_Clasification)
        self.toolBar.addAction(self.actionSignalName)

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

    def loadSignalOnTab(self, signal):
        """
        Load a signal in the current widget tab
        :param signal: The signal to load
        :return:
        """
        self.widget.signal = signal
        self.widget.graph()

        # connect for data display
        self.widget.toolDataDetected.connect(self.updateStatusBar)

        # refresh and set visible both axes on the new widget
        self.changeWidgetsVisibility(True, True)

        self.widget.load_Theme(self.workTheme)

        # update the app title, tab text and signal properties label
        self.setWindowTitle(self.tr(u"duetto-Sound Lab - ") + self.widget.signalName())
        self.tabOpenedSignals.setTabText(self.tabOpenedSignals.currentIndex(), signal.name)
        self.updateSignalPropertiesLabel()

        # add context menu actions
        self.addWidgetContextMenuActions()

    def currentSignalTabChanged(self,tabIndex):
        """
        Update the window state and variables when the current signal tab has changed
        :param tabIndex: The new index of selected tab signal
        :return:
        """
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
        if self.tabOpenedSignals.count() > 1:
            self.save_signal_if_modified()
            self.tabOpenedSignals.removeTab(index)
        # add behavior for no signal opened and start window with options

    def closeAllTabs(self, exceptIndex=0):
        """
        Close the signals on all the opened tabs
        :param exceptIndex: Signal tab index to not close.
        :return:
        """
        # must be changed the default index when the app allow to
        # close all the signals instead of leave one opened always
        for i in range(self.tabOpenedSignals.count()-1, -1, -1):
            if i != exceptIndex:
                self.closeSignalAt(i)

    # endregion

    # region Widget Property
    @property
    def widget(self):
        """
        Gets the current widget selected or None if no signal is opened
        :return:
        """
        if self.tabOpenedSignals.count() == 0:
            return None

        return self.tabOpenedSignals.currentWidget()

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

        indexFrom, indexTo = self.widget.getIndexFromAndTo()
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

    def updateTheme(self, theme):
        """
        Update the current selected theme with the values of the supplied new one.
        :param theme: The new Theme to load
        :return:
        """
        assert isinstance(theme, WorkTheme)
        #  change the current theme
        self.workTheme = theme

        #  update the theme in the widget
        self.widget.load_Theme(theme)

        #  update values of the Param tree
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
        #  self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
        #  unicode(self.tr(u'Frequency(kHz)'))).param(unicode(self.tr(u'Min'))).setValue(theme.minYSpec / 1000.0)
        #  self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
        #  unicode(self.tr(u'Frequency(kHz)'))).param(unicode(self.tr(u'Max'))).setValue(theme.maxYSpec / 1000.0)
        #  self.ParamTree.param(unicode(self.tr(u'Oscillogram Settings'))).param(unicode(self.tr(u'Amplitude(%)'))).param(
        #  unicode(self.tr(u'Min'))).setValue(theme.minYOsc)
        #  self.ParamTree.param(unicode(self.tr(u'Oscillogram Settings'))).param(unicode(self.tr(u'Amplitude(%)'))).param(
        #  unicode(self.tr(u'Max'))).setValue(theme.maxYOsc)
        self.ParamTree.param(unicode(self.tr(u'Detection Visual Settings'))).param(
            unicode(self.tr(u'Measurement Location'))).param(unicode(self.tr(u'Center'))).setValue(
            theme.detectionTheme.centerColor)
        self.ParamTree.param(unicode(self.tr(u'Detection Visual Settings'))).param(
            unicode(self.tr(u'Measurement Location'))).param(unicode(self.tr(u'End'))).setValue(
            theme.detectionTheme.endColor)
        self.ParamTree.param(unicode(self.tr(u'Detection Visual Settings'))).param(
            unicode(self.tr(u'Measurement Location'))).param(unicode(self.tr(u'Start'))).setValue(
            theme.detectionTheme.startColor)
        self.ParamTree.param(unicode(self.tr(u'Detection Visual Settings'))).param(
            unicode(self.tr(u'Measurement Location'))).param(unicode(self.tr(u'Quartile25'))).setValue(
            theme.detectionTheme.quart1Color)
        self.ParamTree.param(unicode(self.tr(u'Detection Visual Settings'))).param(
            unicode(self.tr(u'Measurement Location'))).param(unicode(self.tr(u'Quartile75'))).setValue(
            theme.detectionTheme.quart2Color)

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
        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
            unicode(self.tr(u'Threshold(dB)'))).param(unicode(self.tr(u'Min'))).setValue(reg[0])
        self.ParamTree.param(unicode(self.tr(u'Spectrogram Settings'))).param(
            unicode(self.tr(u'Threshold(dB)'))).param(unicode(self.tr(u'Max'))).setValue(reg[1])
        self.workTheme.spectrogramTheme.histRange = reg

    def histogramGradientChanged(self):
        """
        Updates the variables in the param tree and the work theme that represent the gradient colors of the histogram.
        """
        self.workTheme.spectrogramTheme.colorBarState = self.hist.item.gradient.saveState()

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
            pickle.dump(self.workTheme, f)

    def change(self, param, changes):
        """
        Method that updates the internal variables and state of the widgets
        when a change is made in the visual options of the theme
        :param param: param
        :param changes: list with the changes in the param tree
        """
        graph = False
        loadTheme = False
        for param, change, data in changes:
            path = self.ParamTree.childPath(param)
            if path is not None:
                childName = '.'.join(path)
            else:
                childName = param.name()

            if childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'FFT size')):
                self.widget.axesSpecgram.specgramHandler.NFFT = data
                graph = True

            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'Grid')) + u"." + unicode(self.tr(u'X')):
                self.workTheme.spectrogramTheme.gridX = data
                loadTheme = True

            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'Grid')) + u"." + unicode(self.tr(u'Y')):
                self.workTheme.spectrogramTheme.gridY = data
                loadTheme = True

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
                    self.workTheme.spectrogramTheme.histRange = data, self.hist.item.region.getRegion()[1]
                    loadTheme = True

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
                    self.workTheme.spectrogramTheme.histRange = self.hist.item.region.getRegion()[0], data
                    loadTheme = True

            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'FFT window')):
                self.widget.axesSpecgram.specgramHandler.window = data
                graph = True

            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'Background color')):
                self.workTheme.spectrogramTheme.background_color = data
                loadTheme = True
            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'Frequency(kHz)')) + u"." + \
                    unicode(self.tr(u'Min')):
                pass  #  self.defaultTheme.spectrogramTheme.minY = data

            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'Frequency(kHz)')) + u"." + \
                    unicode(self.tr(u'Max')):
                pass  #  self.defaultTheme.spectrogramTheme.maxY = data

            elif childName == unicode(self.tr(u'Spectrogram Settings')) + u"." + \
                    unicode(self.tr(u'FFT overlap')):
                self.widget.axesSpecgram.specgramHandler.overlap = data
                graph = True

            elif childName == unicode(self.tr(u'Power Spectrum Settings')) + u"." + \
                    unicode(self.tr(u'FFT size')):
                self.NFFT_pow = data

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Background color')):
                self.workTheme.oscillogramTheme.background_color = data
                loadTheme = True

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Grid')) + u"." + \
                    unicode(self.tr(u'X')):
                self.workTheme.oscillogramTheme.gridX = data
                loadTheme = True

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Grid')) + u"." + \
                    unicode(self.tr(u'Y')):
                self.workTheme.oscillogramTheme.gridY = data
                loadTheme = True

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Plot color')):
                self.workTheme.oscillogramTheme.plot_color = data
                loadTheme = True

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Amplitude(%)')) + u"." + \
                    unicode(self.tr(u'Min')):
                pass  #  self.defaultTheme.oscillogramTheme.minY = data

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Amplitude(%)')) + u"." + \
                    unicode(self.tr(u'Max')):
                pass  #  self.defaultTheme.oscillogramTheme.maxY = data

            elif childName == unicode(self.tr(u'Oscillogram Settings')) + u"." + \
                    unicode(self.tr(u'Connect Points')):
                self.workTheme.oscillogramTheme.connectPoints = data
                loadTheme = True

            elif childName == unicode(self.tr(u'Themes')) + u"." + \
                    unicode(self.tr(u'Theme Selected')):
                try:
                    self.updateTheme(self.deSerializeTheme(data))
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

        if graph:
            self.widget.graph()
        if loadTheme:
            self.widget.load_Theme(self.workTheme)

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
        #          start, _ = self.widget.getIndexFromAndTo()
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
                freq_cut_lower = filterDialogWindow.spinBoxBandStopFl.value()
                freq_cut_upper = filterDialogWindow.spinBoxBandStopFu.value()
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

    def on_load(self):
        """
        Method that is called when the window has the initial state.
        That is: when the window is created,
                 when the current signal is closed but not the window.
        :return:
        """
        # show an initial state window with common options to open recent files
        # create new ones etc
        signal = Synthesizer.generateSilence(44100, 16, 5000)

        self.addSignalTab(signal)

    @pyqtSlot()
    def on_actionExit_triggered(self):
        self.close()

    def closeEvent(self, event):
        """
        Event for close. Release the resources and save changes.
        :param event:
        :return:
        """

        #  save the signal if any change
        self.save_signal_if_modified(event)

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
        unmodified_tabsignal_indexes = []
        for i in range(self.tabOpenedSignals.count()):
            if self.tabOpenedSignals.widget(i).undoRedoManager.count() == 0:
                unmodified_tabsignal_indexes.append(i)

        for index in unmodified_tabsignal_indexes:
            self.closeSignalAt(index)

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

        # close the opened windows of one dim processing
        # and restart the list of windows
        for win in self.one_dim_windows:
            win.close()
        self.one_dim_windows = []

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

                if currentTab:
                    self.loadSignalOnTab(signal)
                else:
                    self.addSignalTab(signal)

            except Exception as ex:
                QMessageBox.warning(QMessageBox(), self.tr(u"Error"),
                                    self.tr(u"Could not load the file.") +
                                    u"\n" + file_path)

                # recover from an open error by opening a default signal
                signal = Synthesizer.generateSilence(44100, 16, 1)

                if currentTab:
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
            mbox = QtGui.QMessageBox(QtGui.QMessageBox.Question, self.tr(u"Save"),
                                     self.tr(u"Do you want to save the signal " + widget.signalName() + u" ?"),
                                     QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel, self)
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

    # endregion

    # region Signal Properties Info Display

    def updateSignalPropertiesLabel(self):
        """
        Updates the text of the current signal properties in toolbar.
        :return:
        """
        #  action signal is a place in the tool bar to show the current signal name
        self.actionSignalName.setText(self.tr(u"Filename: ") + self.widget.signalName())

        sr = self.widget.signal.samplingRate
        bit_depth = self.widget.signal.bitDepth
        channels = self.widget.signal.channelCount

        tooltip = "Sampling Rate: " + str(sr) + \
                  "\nBit Depth: " + str(bit_depth) + \
                  "\nChannels: " + str(channels) + \
                  "\nDuration(s): " + str(self.widget.signal.duration)

        self.actionSignalName.setToolTip(tooltip)

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
                self._open(self.filesInFolder[self.filesInFolderIndex], currentTab = True)

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
        self.widget.switchPlayStatus()

    @pyqtSlot(QAction)
    def on_playSpeedChanged_triggered(self, action):
        """
        Change the play speed of the signal.
        :param action: the action to set the speed
        :return:
        """
        self.widget.stop()
        #  the spped is get form the text of the action (?? is posible to improve it ??)
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
        indexFrom, indexTo = self.widget.getIndexFromAndTo()
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

        indexFrom, indexTo = self.widget.getIndexFromAndTo()
        one_dim_window.graph(indexFrom, indexTo)

        #  store the opened one dimensional one_dim_transform windows for handling
        self.one_dim_windows.append(one_dim_window)

    #  endregion

    #  region Scroll Bar Range
    #  TODO comentar e implementar esta parte
    #  manipulation of the scrool bar to set the range
    #  of visualization of the signal on the widget

    @pyqtSlot(int, int, int)
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

    @pyqtSlot(int)
    def on_horizontalScrollBar_valueChanged(self, value):
        pass
        # self.widget.changeRange(value, value + self.horizontalScrollBar.pageStep(), emit=False)

    # endregion

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