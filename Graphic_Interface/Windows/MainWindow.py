# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Wed Jan 15 00:20:08 2014
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_DuettoMainWindow(object):
    def setupUi(self, DuettoMainWindow):
        DuettoMainWindow.setObjectName(_fromUtf8("DuettoMainWindow"))
        DuettoMainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        DuettoMainWindow.resize(1270, 700)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DuettoMainWindow.sizePolicy().hasHeightForWidth())
        DuettoMainWindow.setSizePolicy(sizePolicy)
        DuettoMainWindow.setMaximumSize(QtCore.QSize(1270, 760))
        self.centralwidget = QtGui.QWidget(DuettoMainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.widget = QSignalVisualizerWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.widget.setAutoFillBackground(True)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout_2.addWidget(self.widget)
        self.horizontalScrollBar = QtGui.QScrollBar(self.centralwidget)
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName(_fromUtf8("horizontalScrollBar"))
        self.verticalLayout_2.addWidget(self.horizontalScrollBar)
        DuettoMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(DuettoMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1270, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuTools = QtGui.QMenu(self.menubar)
        self.menuTools.setObjectName(_fromUtf8("menuTools"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuGenerate = QtGui.QMenu(self.menuEdit)
        self.menuGenerate.setObjectName(_fromUtf8("menuGenerate"))
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName(_fromUtf8("menuView"))
        self.menuSound = QtGui.QMenu(self.menubar)
        self.menuSound.setObjectName(_fromUtf8("menuSound"))
        self.menuView_2 = QtGui.QMenu(self.menubar)
        self.menuView_2.setObjectName(_fromUtf8("menuView_2"))
        self.menuDetection = QtGui.QMenu(self.menubar)
        self.menuDetection.setObjectName(_fromUtf8("menuDetection"))
        DuettoMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(DuettoMainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        DuettoMainWindow.setStatusBar(self.statusbar)
        self.dock_osc_settings = QtGui.QDockWidget(DuettoMainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dock_osc_settings.sizePolicy().hasHeightForWidth())
        self.dock_osc_settings.setSizePolicy(sizePolicy)
        self.dock_osc_settings.setMinimumSize(QtCore.QSize(180, 179))
        self.dock_osc_settings.setMaximumSize(QtCore.QSize(180, 179))
        self.dock_osc_settings.setFloating(True)
        self.dock_osc_settings.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
        self.dock_osc_settings.setObjectName(_fromUtf8("dock_osc_settings"))
        self.osc_settings_contents = QtGui.QWidget()
        self.osc_settings_contents.setObjectName(_fromUtf8("osc_settings_contents"))
        self.formLayout = QtGui.QFormLayout(self.osc_settings_contents)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_2 = QtGui.QLabel(self.osc_settings_contents)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.spinBox = QtGui.QSpinBox(self.osc_settings_contents)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.spinBox)
        self.label = QtGui.QLabel(self.osc_settings_contents)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label)
        self.min_amp_tbx = QtGui.QLineEdit(self.osc_settings_contents)
        self.min_amp_tbx.setObjectName(_fromUtf8("min_amp_tbx"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.min_amp_tbx)
        self.max_amp_tbx = QtGui.QLineEdit(self.osc_settings_contents)
        self.max_amp_tbx.setObjectName(_fromUtf8("max_amp_tbx"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.max_amp_tbx)
        self.btnosc_apply = QtGui.QPushButton(self.osc_settings_contents)
        self.btnosc_apply.setObjectName(_fromUtf8("btnosc_apply"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.btnosc_apply)
        self.dock_osc_settings.setWidget(self.osc_settings_contents)
        DuettoMainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dock_osc_settings)
        self.dock_spec_settings = QtGui.QDockWidget(DuettoMainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dock_spec_settings.sizePolicy().hasHeightForWidth())
        self.dock_spec_settings.setSizePolicy(sizePolicy)
        self.dock_spec_settings.setMinimumSize(QtCore.QSize(180, 200))
        self.dock_spec_settings.setMaximumSize(QtCore.QSize(180, 200))
        self.dock_spec_settings.setFloating(True)
        self.dock_spec_settings.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
        self.dock_spec_settings.setObjectName(_fromUtf8("dock_spec_settings"))
        self.spec_settings_contents = QtGui.QWidget()
        self.spec_settings_contents.setObjectName(_fromUtf8("spec_settings_contents"))
        self.formLayout_2 = QtGui.QFormLayout(self.spec_settings_contents)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_3 = QtGui.QLabel(self.spec_settings_contents)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_3)
        self.cbx_fftsize = QtGui.QComboBox(self.spec_settings_contents)
        self.cbx_fftsize.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.cbx_fftsize.setInsertPolicy(QtGui.QComboBox.InsertAfterCurrent)
        self.cbx_fftsize.setMinimumContentsLength(5)
        self.cbx_fftsize.setModelColumn(0)
        self.cbx_fftsize.setObjectName(_fromUtf8("cbx_fftsize"))
        self.cbx_fftsize.addItem(_fromUtf8(""))
        self.cbx_fftsize.addItem(_fromUtf8(""))
        self.cbx_fftsize.addItem(_fromUtf8(""))
        self.cbx_fftsize.addItem(_fromUtf8(""))
        self.cbx_fftsize.addItem(_fromUtf8(""))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.SpanningRole, self.cbx_fftsize)
        self.label_4 = QtGui.QLabel(self.spec_settings_contents)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_4)
        self.cbx_fftwindow = QtGui.QComboBox(self.spec_settings_contents)
        self.cbx_fftwindow.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.cbx_fftwindow.setMinimumContentsLength(0)
        self.cbx_fftwindow.setObjectName(_fromUtf8("cbx_fftwindow"))
        self.cbx_fftwindow.addItem(_fromUtf8(""))
        self.cbx_fftwindow.addItem(_fromUtf8(""))
        self.cbx_fftwindow.addItem(_fromUtf8(""))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.SpanningRole, self.cbx_fftwindow)
        self.label_5 = QtGui.QLabel(self.spec_settings_contents)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_5)
        self.sbx_fftoverlap = QtGui.QSpinBox(self.spec_settings_contents)
        self.sbx_fftoverlap.setMaximum(98)
        self.sbx_fftoverlap.setProperty("value", 98)
        self.sbx_fftoverlap.setObjectName(_fromUtf8("sbx_fftoverlap"))
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.LabelRole, self.sbx_fftoverlap)
        self.btnspec_apply = QtGui.QPushButton(self.spec_settings_contents)
        self.btnspec_apply.setObjectName(_fromUtf8("btnspec_apply"))
        self.formLayout_2.setWidget(6, QtGui.QFormLayout.LabelRole, self.btnspec_apply)
        self.dock_spec_settings.setWidget(self.spec_settings_contents)
        DuettoMainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dock_spec_settings)
        self.toolBar = QtGui.QToolBar(DuettoMainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        DuettoMainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.dock_powspec_settings = QtGui.QDockWidget(DuettoMainWindow)
        self.dock_powspec_settings.setMinimumSize(QtCore.QSize(180, 153))
        self.dock_powspec_settings.setMaximumSize(QtCore.QSize(180, 153))
        self.dock_powspec_settings.setFloating(False)
        self.dock_powspec_settings.setObjectName(_fromUtf8("dock_powspec_settings"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.formLayout_3 = QtGui.QFormLayout(self.dockWidgetContents)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.label_6 = QtGui.QLabel(self.dockWidgetContents)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_6)
        self.cbx_fftsize_pow = QtGui.QComboBox(self.dockWidgetContents)
        self.cbx_fftsize_pow.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.cbx_fftsize_pow.setInsertPolicy(QtGui.QComboBox.InsertAfterCurrent)
        self.cbx_fftsize_pow.setMinimumContentsLength(5)
        self.cbx_fftsize_pow.setModelColumn(0)
        self.cbx_fftsize_pow.setObjectName(_fromUtf8("cbx_fftsize_pow"))
        self.cbx_fftsize_pow.addItem(_fromUtf8(""))
        self.cbx_fftsize_pow.addItem(_fromUtf8(""))
        self.cbx_fftsize_pow.addItem(_fromUtf8(""))
        self.cbx_fftsize_pow.addItem(_fromUtf8(""))
        self.cbx_fftsize_pow.addItem(_fromUtf8(""))
        self.cbx_fftsize_pow.addItem(_fromUtf8(""))
        self.cbx_fftsize_pow.addItem(_fromUtf8(""))
        self.cbx_fftsize_pow.addItem(_fromUtf8(""))
        self.cbx_fftsize_pow.addItem(_fromUtf8(""))
        self.cbx_fftsize_pow.addItem(_fromUtf8(""))
        self.cbx_fftsize_pow.addItem(_fromUtf8(""))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.SpanningRole, self.cbx_fftsize_pow)
        self.label_7 = QtGui.QLabel(self.dockWidgetContents)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_7)
        self.cbx_fftwindow_pow = QtGui.QComboBox(self.dockWidgetContents)
        self.cbx_fftwindow_pow.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.cbx_fftwindow_pow.setMinimumContentsLength(0)
        self.cbx_fftwindow_pow.setObjectName(_fromUtf8("cbx_fftwindow_pow"))
        self.cbx_fftwindow_pow.addItem(_fromUtf8(""))
        self.cbx_fftwindow_pow.addItem(_fromUtf8(""))
        self.cbx_fftwindow_pow.addItem(_fromUtf8(""))
        self.formLayout_3.setWidget(3, QtGui.QFormLayout.SpanningRole, self.cbx_fftwindow_pow)
        self.btnpow_apply = QtGui.QPushButton(self.dockWidgetContents)
        self.btnpow_apply.setObjectName(_fromUtf8("btnpow_apply"))
        self.formLayout_3.setWidget(4, QtGui.QFormLayout.LabelRole, self.btnpow_apply)
        self.dock_powspec_settings.setWidget(self.dockWidgetContents)
        DuettoMainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dock_powspec_settings)
        self.actionOpen = QtGui.QAction(DuettoMainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/81.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionExit = QtGui.QAction(DuettoMainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionZoomIn = QtGui.QAction(DuettoMainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/zoomin_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoomIn.setIcon(icon1)
        self.actionZoomIn.setObjectName(_fromUtf8("actionZoomIn"))
        self.actionZoom_out = QtGui.QAction(DuettoMainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/zoomout_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoom_out.setIcon(icon2)
        self.actionZoom_out.setObjectName(_fromUtf8("actionZoom_out"))
        self.actionSelect_all = QtGui.QAction(DuettoMainWindow)
        self.actionSelect_all.setObjectName(_fromUtf8("actionSelect_all"))
        self.actionSpectogram = QtGui.QAction(DuettoMainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/spec.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSpectogram.setIcon(icon3)
        self.actionSpectogram.setObjectName(_fromUtf8("actionSpectogram"))
        self.actionOscilogram = QtGui.QAction(DuettoMainWindow)
        self.actionOscilogram.setEnabled(True)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/osc.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOscilogram.setIcon(icon4)
        self.actionOscilogram.setVisible(True)
        self.actionOscilogram.setObjectName(_fromUtf8("actionOscilogram"))
        self.actionCombined = QtGui.QAction(DuettoMainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/combined.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCombined.setIcon(icon5)
        self.actionCombined.setObjectName(_fromUtf8("actionCombined"))
        self.actionNew = QtGui.QAction(DuettoMainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/Leopard Icon 60.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon6)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionPower_Spectrum = QtGui.QAction(DuettoMainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/powerspec.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPower_Spectrum.setIcon(icon7)
        self.actionPower_Spectrum.setObjectName(_fromUtf8("actionPower_Spectrum"))
        self.actionOscillogram_Settings = QtGui.QAction(DuettoMainWindow)
        self.actionOscillogram_Settings.setObjectName(_fromUtf8("actionOscillogram_Settings"))
        self.actionSpectogram_Settings = QtGui.QAction(DuettoMainWindow)
        self.actionSpectogram_Settings.setObjectName(_fromUtf8("actionSpectogram_Settings"))
        self.actionPower_Spectrum_Settings = QtGui.QAction(DuettoMainWindow)
        self.actionPower_Spectrum_Settings.setObjectName(_fromUtf8("actionPower_Spectrum_Settings"))
        self.actionPlay_Sound = QtGui.QAction(DuettoMainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/02049_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPlay_Sound.setIcon(icon8)
        self.actionPlay_Sound.setObjectName(_fromUtf8("actionPlay_Sound"))
        self.actionStop_Sound = QtGui.QAction(DuettoMainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/02051_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionStop_Sound.setIcon(icon9)
        self.actionStop_Sound.setObjectName(_fromUtf8("actionStop_Sound"))
        self.actionPause_Sound = QtGui.QAction(DuettoMainWindow)
        self.actionPause_Sound.setObjectName(_fromUtf8("actionPause_Sound"))
        self.actionZoom_out_entire_file = QtGui.QAction(DuettoMainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/zoom_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoom_out_entire_file.setIcon(icon10)
        self.actionZoom_out_entire_file.setObjectName(_fromUtf8("actionZoom_out_entire_file"))
        self.actionSave = QtGui.QAction(DuettoMainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/225.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon11)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionCopy = QtGui.QAction(DuettoMainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/copy_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCopy.setIcon(icon12)
        self.actionCopy.setObjectName(_fromUtf8("actionCopy"))
        self.actionPaste = QtGui.QAction(DuettoMainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/paste_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPaste.setIcon(icon13)
        self.actionPaste.setObjectName(_fromUtf8("actionPaste"))
        self.actionCut = QtGui.QAction(DuettoMainWindow)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/cut_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCut.setIcon(icon14)
        self.actionCut.setObjectName(_fromUtf8("actionCut"))
        self.actionHighest_frecuency = QtGui.QAction(DuettoMainWindow)
        self.actionHighest_frecuency.setCheckable(False)
        self.actionHighest_frecuency.setEnabled(True)
        self.actionHighest_frecuency.setObjectName(_fromUtf8("actionHighest_frecuency"))
        self.actionHighest_instant_frequency = QtGui.QAction(DuettoMainWindow)
        self.actionHighest_instant_frequency.setCheckable(False)
        self.actionHighest_instant_frequency.setObjectName(_fromUtf8("actionHighest_instant_frequency"))
        self.actionClear_Spectogram = QtGui.QAction(DuettoMainWindow)
        self.actionClear_Spectogram.setObjectName(_fromUtf8("actionClear_Spectogram"))
        self.actionAll_Settings = QtGui.QAction(DuettoMainWindow)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/LeopardVista V4 Icon 09.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAll_Settings.setIcon(icon15)
        self.actionAll_Settings.setObjectName(_fromUtf8("actionAll_Settings"))
        self.actionRecord = QtGui.QAction(DuettoMainWindow)
        self.actionRecord.setObjectName(_fromUtf8("actionRecord"))
        self.action_Reverse = QtGui.QAction(DuettoMainWindow)
        self.action_Reverse.setObjectName(_fromUtf8("action_Reverse"))
        self.actionInsert_Silence = QtGui.QAction(DuettoMainWindow)
        self.actionInsert_Silence.setObjectName(_fromUtf8("actionInsert_Silence"))
        self.actionSilence = QtGui.QAction(DuettoMainWindow)
        self.actionSilence.setObjectName(_fromUtf8("actionSilence"))
        self.actionFilter = QtGui.QAction(DuettoMainWindow)
        self.actionFilter.setObjectName(_fromUtf8("actionFilter"))
        self.actionSmart_Scale = QtGui.QAction(DuettoMainWindow)
        self.actionSmart_Scale.setObjectName(_fromUtf8("actionSmart_Scale"))
        self.actionNormalize = QtGui.QAction(DuettoMainWindow)
        self.actionNormalize.setObjectName(_fromUtf8("actionNormalize"))
        self.actionResampling = QtGui.QAction(DuettoMainWindow)
        self.actionResampling.setObjectName(_fromUtf8("actionResampling"))
        self.actionGenerate_White_Noise = QtGui.QAction(DuettoMainWindow)
        self.actionGenerate_White_Noise.setObjectName(_fromUtf8("actionGenerate_White_Noise"))
        self.actionOsilogram_Detector = QtGui.QAction(DuettoMainWindow)
        self.actionOsilogram_Detector.setObjectName(_fromUtf8("actionOsilogram_Detector"))
        self.actionSpectrogram_Detector = QtGui.QAction(DuettoMainWindow)
        self.actionSpectrogram_Detector.setObjectName(_fromUtf8("actionSpectrogram_Detector"))
        self.actionEnvelope = QtGui.QAction(DuettoMainWindow)
        self.actionEnvelope.setObjectName(_fromUtf8("actionEnvelope"))
        self.actionGenerate_Pink_Noise = QtGui.QAction(DuettoMainWindow)
        self.actionGenerate_Pink_Noise.setObjectName(_fromUtf8("actionGenerate_Pink_Noise"))
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionExit)
        self.menuTools.addAction(self.actionZoomIn)
        self.menuTools.addAction(self.actionZoom_out)
        self.menuTools.addAction(self.actionZoom_out_entire_file)
        self.menuGenerate.addAction(self.actionGenerate_White_Noise)
        self.menuGenerate.addAction(self.actionGenerate_Pink_Noise)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionSelect_all)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.action_Reverse)
        self.menuEdit.addAction(self.actionInsert_Silence)
        self.menuEdit.addAction(self.actionSilence)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionFilter)
        self.menuEdit.addAction(self.actionSmart_Scale)
        self.menuEdit.addAction(self.actionNormalize)
        self.menuEdit.addAction(self.actionResampling)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.menuGenerate.menuAction())
        self.menuView.addAction(self.actionOscilogram)
        self.menuView.addAction(self.actionSpectogram)
        self.menuView.addAction(self.actionCombined)
        self.menuView.addAction(self.actionPower_Spectrum)
        self.menuView.addAction(self.actionEnvelope)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionOscillogram_Settings)
        self.menuView.addAction(self.actionSpectogram_Settings)
        self.menuView.addAction(self.actionPower_Spectrum_Settings)
        self.menuView.addAction(self.actionAll_Settings)
        self.menuSound.addAction(self.actionPlay_Sound)
        self.menuSound.addAction(self.actionStop_Sound)
        self.menuSound.addAction(self.actionPause_Sound)
        self.menuSound.addAction(self.actionRecord)
        self.menuView_2.addAction(self.actionHighest_instant_frequency)
        self.menuView_2.addAction(self.actionClear_Spectogram)
        self.menuDetection.addAction(self.actionOsilogram_Detector)
        self.menuDetection.addAction(self.actionSpectrogram_Detector)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuSound.menuAction())
        self.menubar.addAction(self.menuView_2.menuAction())
        self.menubar.addAction(self.menuDetection.menuAction())
        self.toolBar.addAction(self.actionNew)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionCopy)
        self.toolBar.addAction(self.actionCut)
        self.toolBar.addAction(self.actionPaste)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPlay_Sound)
        self.toolBar.addAction(self.actionStop_Sound)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionZoomIn)
        self.toolBar.addAction(self.actionZoom_out)
        self.toolBar.addAction(self.actionZoom_out_entire_file)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionCombined)
        self.toolBar.addAction(self.actionOscilogram)
        self.toolBar.addAction(self.actionSpectogram)
        self.toolBar.addAction(self.actionPower_Spectrum)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionAll_Settings)

        self.retranslateUi(DuettoMainWindow)
        self.cbx_fftsize.setCurrentIndex(3)
        self.cbx_fftsize_pow.setCurrentIndex(4)
        QtCore.QMetaObject.connectSlotsByName(DuettoMainWindow)

    def retranslateUi(self, DuettoMainWindow):
        DuettoMainWindow.setWindowTitle(_translate("DuettoMainWindow", "BatSound", None))
        self.menuFile.setTitle(_translate("DuettoMainWindow", "File", None))
        self.menuTools.setTitle(_translate("DuettoMainWindow", "Tools", None))
        self.menuEdit.setTitle(_translate("DuettoMainWindow", "Edit", None))
        self.menuGenerate.setTitle(_translate("DuettoMainWindow", "Generate", None))
        self.menuView.setTitle(_translate("DuettoMainWindow", "Analysis", None))
        self.menuSound.setTitle(_translate("DuettoMainWindow", "Sound", None))
        self.menuView_2.setTitle(_translate("DuettoMainWindow", "View", None))
        self.menuDetection.setTitle(_translate("DuettoMainWindow", "Detection", None))
        self.dock_osc_settings.setWindowTitle(_translate("DuettoMainWindow", "Oscillogram Settings", None))
        self.label_2.setText(_translate("DuettoMainWindow", "Milliseconds per plot", None))
        self.label.setText(_translate("DuettoMainWindow", "Min and max amplitude", None))
        self.btnosc_apply.setText(_translate("DuettoMainWindow", "Apply", None))
        self.dock_spec_settings.setWindowTitle(_translate("DuettoMainWindow", "Spectrogram Settings", None))
        self.label_3.setText(_translate("DuettoMainWindow", "FFT size", None))
        self.cbx_fftsize.setItemText(0, _translate("DuettoMainWindow", "Automatic", None))
        self.cbx_fftsize.setItemText(1, _translate("DuettoMainWindow", "2048", None))
        self.cbx_fftsize.setItemText(2, _translate("DuettoMainWindow", "1024", None))
        self.cbx_fftsize.setItemText(3, _translate("DuettoMainWindow", "512", None))
        self.cbx_fftsize.setItemText(4, _translate("DuettoMainWindow", "256", None))
        self.label_4.setText(_translate("DuettoMainWindow", "FFT window", None))
        self.cbx_fftwindow.setItemText(0, _translate("DuettoMainWindow", "Rectangular", None))
        self.cbx_fftwindow.setItemText(1, _translate("DuettoMainWindow", "Hanning", None))
        self.cbx_fftwindow.setItemText(2, _translate("DuettoMainWindow", "Hamming", None))
        self.label_5.setText(_translate("DuettoMainWindow", "FFT overlap", None))
        self.btnspec_apply.setText(_translate("DuettoMainWindow", "Apply", None))
        self.toolBar.setWindowTitle(_translate("DuettoMainWindow", "toolBar", None))
        self.dock_powspec_settings.setWindowTitle(_translate("DuettoMainWindow", "Power Spectrum Settings", None))
        self.label_6.setText(_translate("DuettoMainWindow", "FFT size", None))
        self.cbx_fftsize_pow.setItemText(0, _translate("DuettoMainWindow", "16384", None))
        self.cbx_fftsize_pow.setItemText(1, _translate("DuettoMainWindow", "8192", None))
        self.cbx_fftsize_pow.setItemText(2, _translate("DuettoMainWindow", "4096", None))
        self.cbx_fftsize_pow.setItemText(3, _translate("DuettoMainWindow", "2048", None))
        self.cbx_fftsize_pow.setItemText(4, _translate("DuettoMainWindow", "1024", None))
        self.cbx_fftsize_pow.setItemText(5, _translate("DuettoMainWindow", "512", None))
        self.cbx_fftsize_pow.setItemText(6, _translate("DuettoMainWindow", "256", None))
        self.cbx_fftsize_pow.setItemText(7, _translate("DuettoMainWindow", "128", None))
        self.cbx_fftsize_pow.setItemText(8, _translate("DuettoMainWindow", "64", None))
        self.cbx_fftsize_pow.setItemText(9, _translate("DuettoMainWindow", "32", None))
        self.cbx_fftsize_pow.setItemText(10, _translate("DuettoMainWindow", "16", None))
        self.label_7.setText(_translate("DuettoMainWindow", "FFT window", None))
        self.cbx_fftwindow_pow.setItemText(0, _translate("DuettoMainWindow", "Rectangular", None))
        self.cbx_fftwindow_pow.setItemText(1, _translate("DuettoMainWindow", "Hanning", None))
        self.cbx_fftwindow_pow.setItemText(2, _translate("DuettoMainWindow", "Hamming", None))
        self.btnpow_apply.setText(_translate("DuettoMainWindow", "Apply", None))
        self.actionOpen.setText(_translate("DuettoMainWindow", "Open", None))
        self.actionExit.setText(_translate("DuettoMainWindow", "Exit", None))
        self.actionZoomIn.setText(_translate("DuettoMainWindow", "Zoom in", None))
        self.actionZoom_out.setText(_translate("DuettoMainWindow", "Zoom out", None))
        self.actionSelect_all.setText(_translate("DuettoMainWindow", "Select all", None))
        self.actionSpectogram.setText(_translate("DuettoMainWindow", "Spectogram", None))
        self.actionOscilogram.setText(_translate("DuettoMainWindow", "Oscillogram", None))
        self.actionCombined.setText(_translate("DuettoMainWindow", "Combined", None))
        self.actionNew.setText(_translate("DuettoMainWindow", "New", None))
        self.actionPower_Spectrum.setText(_translate("DuettoMainWindow", "Power Spectrum", None))
        self.actionOscillogram_Settings.setText(_translate("DuettoMainWindow", "Oscillogram Settings", None))
        self.actionSpectogram_Settings.setText(_translate("DuettoMainWindow", "Spectrogram Settings", None))
        self.actionPower_Spectrum_Settings.setText(_translate("DuettoMainWindow", "Power Spectrum Settings", None))
        self.actionPlay_Sound.setText(_translate("DuettoMainWindow", "Play Sound", None))
        self.actionStop_Sound.setText(_translate("DuettoMainWindow", "Stop Sound", None))
        self.actionPause_Sound.setText(_translate("DuettoMainWindow", "Pause Sound", None))
        self.actionZoom_out_entire_file.setText(_translate("DuettoMainWindow", "Zoom out entire file", None))
        self.actionSave.setText(_translate("DuettoMainWindow", "Save as", None))
        self.actionCopy.setText(_translate("DuettoMainWindow", "Copy", None))
        self.actionPaste.setText(_translate("DuettoMainWindow", "Paste", None))
        self.actionCut.setText(_translate("DuettoMainWindow", "Cut", None))
        self.actionHighest_frecuency.setText(_translate("DuettoMainWindow", "Highest frequency", None))
        self.actionHighest_instant_frequency.setText(_translate("DuettoMainWindow", "Highest instant frequency ", None))
        self.actionClear_Spectogram.setText(_translate("DuettoMainWindow", "Clear Spectrogram", None))
        self.actionAll_Settings.setText(_translate("DuettoMainWindow", "All Settings", None))
        self.actionRecord.setText(_translate("DuettoMainWindow", "Record", None))
        self.action_Reverse.setText(_translate("DuettoMainWindow", "Reverse", None))
        self.actionInsert_Silence.setText(_translate("DuettoMainWindow", "Insert Silence", None))
        self.actionSilence.setText(_translate("DuettoMainWindow", "Silence", None))
        self.actionFilter.setText(_translate("DuettoMainWindow", "Filter", None))
        self.actionSmart_Scale.setText(_translate("DuettoMainWindow", "Smart Scale", None))
        self.actionNormalize.setText(_translate("DuettoMainWindow", "Normalize", None))
        self.actionResampling.setText(_translate("DuettoMainWindow", "Resampling", None))
        self.actionGenerate_White_Noise.setText(_translate("DuettoMainWindow", "White Noise", None))
        self.actionOsilogram_Detector.setText(_translate("DuettoMainWindow", "Osilogram Detector", None))
        self.actionSpectrogram_Detector.setText(_translate("DuettoMainWindow", "Spectrogram Detector", None))
        self.actionEnvelope.setText(_translate("DuettoMainWindow", "Envelope", None))
        self.actionGenerate_Pink_Noise.setText(_translate("DuettoMainWindow", "Pink Noise", None))

from Graphic_Interface.Widgets.QSignalVisualizerWidget import QSignalVisualizerWidget
import Graphic_Interface.icons_rc
