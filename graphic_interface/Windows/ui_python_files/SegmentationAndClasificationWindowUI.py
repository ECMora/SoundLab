# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Biologia\DUETTO PROGRAMS\Desktop\Sound Lab\DuettoSystem\graphic_interface\UI_Files\SegmentationAndClasificationWindowUI.ui'
#
# Created: Sat Jan 03 20:02:38 2015
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.resize(906, 569)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(_fromUtf8(""))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setStyleSheet(_fromUtf8(""))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tabwidget = QtGui.QTabWidget(self.centralwidget)
        self.tabwidget.setStyleSheet(_fromUtf8(""))
        self.tabwidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabwidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabwidget.setUsesScrollButtons(True)
        self.tabwidget.setTabsClosable(False)
        self.tabwidget.setMovable(True)
        self.tabwidget.setObjectName(_fromUtf8("tabwidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout = QtGui.QGridLayout(self.tab)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.widget = QSignalDetectorWidget(self.tab)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)
        self.tabwidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setStyleSheet(_fromUtf8(""))
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.gridLayout_4 = QtGui.QGridLayout(self.tab_2)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.pushButtonInputFolder = QtGui.QPushButton(self.tab_2)
        self.pushButtonInputFolder.setStyleSheet(_fromUtf8("background-color: rgb(200, 200, 255);"))
        self.pushButtonInputFolder.setFlat(False)
        self.pushButtonInputFolder.setObjectName(_fromUtf8("pushButtonInputFolder"))
        self.gridLayout_4.addWidget(self.pushButtonInputFolder, 0, 1, 1, 1)
        self.listwidgetProgress = QtGui.QListWidget(self.tab_2)
        self.listwidgetProgress.setStyleSheet(_fromUtf8("background-color: rgb(200, 200, 255);"))
        self.listwidgetProgress.setObjectName(_fromUtf8("listwidgetProgress"))
        self.gridLayout_4.addWidget(self.listwidgetProgress, 4, 0, 1, 1)
        self.progressBarProcesed = QtGui.QProgressBar(self.tab_2)
        self.progressBarProcesed.setProperty("value", 0)
        self.progressBarProcesed.setObjectName(_fromUtf8("progressBarProcesed"))
        self.gridLayout_4.addWidget(self.progressBarProcesed, 6, 0, 1, 1)
        self.lineEditOutputFolder = QtGui.QLineEdit(self.tab_2)
        self.lineEditOutputFolder.setStyleSheet(_fromUtf8("background-color: rgb(200, 200, 255);"))
        self.lineEditOutputFolder.setObjectName(_fromUtf8("lineEditOutputFolder"))
        self.gridLayout_4.addWidget(self.lineEditOutputFolder, 1, 0, 1, 1)
        self.lineeditFilePath = QtGui.QLineEdit(self.tab_2)
        self.lineeditFilePath.setStyleSheet(_fromUtf8("background-color: rgb(200, 200, 255);"))
        self.lineeditFilePath.setObjectName(_fromUtf8("lineeditFilePath"))
        self.gridLayout_4.addWidget(self.lineeditFilePath, 0, 0, 1, 1)
        self.pushButtonOutputFolder = QtGui.QPushButton(self.tab_2)
        self.pushButtonOutputFolder.setStyleSheet(_fromUtf8("background-color: rgb(200, 200, 255);"))
        self.pushButtonOutputFolder.setObjectName(_fromUtf8("pushButtonOutputFolder"))
        self.gridLayout_4.addWidget(self.pushButtonOutputFolder, 1, 1, 1, 1)
        self.groupBox = QtGui.QGroupBox(self.tab_2)
        self.groupBox.setStyleSheet(_fromUtf8("background-color: rgb(200, 200, 255);"))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout = QtGui.QFormLayout(self.groupBox)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.rbttnDetection = QtGui.QRadioButton(self.groupBox)
        self.rbttnDetection.setStyleSheet(_fromUtf8("background-color: rgba(94, 116, 236, 207);"))
        self.rbttnDetection.setCheckable(True)
        self.rbttnDetection.setChecked(True)
        self.rbttnDetection.setObjectName(_fromUtf8("rbttnDetection"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.rbttnDetection)
        self.rbttnSplitFile = QtGui.QRadioButton(self.groupBox)
        self.rbttnSplitFile.setStyleSheet(_fromUtf8("background-color: rgba(94, 116, 236, 207);"))
        self.rbttnSplitFile.setObjectName(_fromUtf8("rbttnSplitFile"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.rbttnSplitFile)
        self.spboxSplitTime = QtGui.QSpinBox(self.groupBox)
        self.spboxSplitTime.setStyleSheet(_fromUtf8("background-color: rgba(94, 116, 236, 207);"))
        self.spboxSplitTime.setMinimum(30)
        self.spboxSplitTime.setMaximum(120)
        self.spboxSplitTime.setProperty("value", 60)
        self.spboxSplitTime.setObjectName(_fromUtf8("spboxSplitTime"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.spboxSplitTime)
        self.pushButtonStart = QtGui.QPushButton(self.groupBox)
        self.pushButtonStart.setObjectName(_fromUtf8("pushButtonStart"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.SpanningRole, self.pushButtonStart)
        self.gridLayout_4.addWidget(self.groupBox, 4, 1, 1, 2)
        self.cbxSingleFile = QtGui.QCheckBox(self.tab_2)
        self.cbxSingleFile.setStyleSheet(_fromUtf8("background-color: rgb(200, 200, 255);"))
        self.cbxSingleFile.setObjectName(_fromUtf8("cbxSingleFile"))
        self.gridLayout_4.addWidget(self.cbxSingleFile, 0, 2, 1, 1)
        self.tabwidget.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout_2.addWidget(self.tabwidget)
        self.horizontalScrollBar = QtGui.QScrollBar(self.centralwidget)
        self.horizontalScrollBar.setStyleSheet(_fromUtf8(""))
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName(_fromUtf8("horizontalScrollBar"))
        self.verticalLayout_2.addWidget(self.horizontalScrollBar)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setMaximumSize(QtCore.QSize(16777215, 16777201))
        self.toolBar.setStyleSheet(_fromUtf8(""))
        self.toolBar.setIconSize(QtCore.QSize(20, 20))
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.dockWidgetParameterTableOscilogram = QtGui.QDockWidget(MainWindow)
        self.dockWidgetParameterTableOscilogram.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.dockWidgetParameterTableOscilogram.setObjectName(_fromUtf8("dockWidgetParameterTableOscilogram"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.tableParameterOscilogram = TableWidget(self.dockWidgetContents)
        self.tableParameterOscilogram.setObjectName(_fromUtf8("tableParameterOscilogram"))
        self.tableParameterOscilogram.setColumnCount(0)
        self.tableParameterOscilogram.setRowCount(0)
        self.verticalLayout_3.addWidget(self.tableParameterOscilogram)
        self.dockWidgetParameterTableOscilogram.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.dockWidgetParameterTableOscilogram)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 906, 21))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuParameters = QtGui.QMenu(self.menuBar)
        self.menuParameters.setObjectName(_fromUtf8("menuParameters"))
        self.menuPeak_Frecuencies = QtGui.QMenu(self.menuParameters)
        self.menuPeak_Frecuencies.setObjectName(_fromUtf8("menuPeak_Frecuencies"))
        self.menuDetection = QtGui.QMenu(self.menuBar)
        self.menuDetection.setObjectName(_fromUtf8("menuDetection"))
        self.menuTools = QtGui.QMenu(self.menuBar)
        self.menuTools.setObjectName(_fromUtf8("menuTools"))
        self.menuClasification = QtGui.QMenu(self.menuBar)
        self.menuClasification.setObjectName(_fromUtf8("menuClasification"))
        MainWindow.setMenuBar(self.menuBar)
        self.actionZoomIn = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/zoomin_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoomIn.setIcon(icon)
        self.actionZoomIn.setObjectName(_fromUtf8("actionZoomIn"))
        self.actionZoom_out = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/zoomout_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoom_out.setIcon(icon1)
        self.actionZoom_out.setObjectName(_fromUtf8("actionZoom_out"))
        self.actionSpectogram = QtGui.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/spec.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSpectogram.setIcon(icon2)
        self.actionSpectogram.setObjectName(_fromUtf8("actionSpectogram"))
        self.actionOscilogram = QtGui.QAction(MainWindow)
        self.actionOscilogram.setEnabled(True)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/osc.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOscilogram.setIcon(icon3)
        self.actionOscilogram.setVisible(True)
        self.actionOscilogram.setObjectName(_fromUtf8("actionOscilogram"))
        self.actionCombined = QtGui.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/combined.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCombined.setIcon(icon4)
        self.actionCombined.setObjectName(_fromUtf8("actionCombined"))
        self.actionPlay_Sound = QtGui.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/02049_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPlay_Sound.setIcon(icon5)
        self.actionPlay_Sound.setObjectName(_fromUtf8("actionPlay_Sound"))
        self.actionStop_Sound = QtGui.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/02051_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionStop_Sound.setIcon(icon6)
        self.actionStop_Sound.setObjectName(_fromUtf8("actionStop_Sound"))
        self.actionPause_Sound = QtGui.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/pausa.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPause_Sound.setIcon(icon7)
        self.actionPause_Sound.setObjectName(_fromUtf8("actionPause_Sound"))
        self.actionZoom_out_entire_file = QtGui.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/zoom_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoom_out_entire_file.setIcon(icon8)
        self.actionZoom_out_entire_file.setObjectName(_fromUtf8("actionZoom_out_entire_file"))
        self.actionCopy = QtGui.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/copy_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCopy.setIcon(icon9)
        self.actionCopy.setObjectName(_fromUtf8("actionCopy"))
        self.actionPaste = QtGui.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/paste_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPaste.setIcon(icon10)
        self.actionPaste.setObjectName(_fromUtf8("actionPaste"))
        self.actionCut = QtGui.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/cut_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCut.setIcon(icon11)
        self.actionCut.setObjectName(_fromUtf8("actionCut"))
        self.actionMeditions = QtGui.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/Excel.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionMeditions.setIcon(icon12)
        self.actionMeditions.setObjectName(_fromUtf8("actionMeditions"))
        self.actionView_Parameters = QtGui.QAction(MainWindow)
        self.actionView_Parameters.setCheckable(True)
        self.actionView_Parameters.setObjectName(_fromUtf8("actionView_Parameters"))
        self.actionDetection = QtGui.QAction(MainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/Process Viewer.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDetection.setIcon(icon13)
        self.actionDetection.setObjectName(_fromUtf8("actionDetection"))
        self.actionClear_Meditions = QtGui.QAction(MainWindow)
        self.actionClear_Meditions.setObjectName(_fromUtf8("actionClear_Meditions"))
        self.actionView_Threshold = QtGui.QAction(MainWindow)
        self.actionView_Threshold.setCheckable(True)
        self.actionView_Threshold.setObjectName(_fromUtf8("actionView_Threshold"))
        self.actionTemporal_Elements = QtGui.QAction(MainWindow)
        self.actionTemporal_Elements.setCheckable(True)
        self.actionTemporal_Elements.setChecked(True)
        self.actionTemporal_Elements.setObjectName(_fromUtf8("actionTemporal_Elements"))
        self.actionSpectral_Elements = QtGui.QAction(MainWindow)
        self.actionSpectral_Elements.setCheckable(True)
        self.actionSpectral_Elements.setChecked(True)
        self.actionSpectral_Elements.setObjectName(_fromUtf8("actionSpectral_Elements"))
        self.actionSpectral_Figures = QtGui.QAction(MainWindow)
        self.actionSpectral_Figures.setCheckable(True)
        self.actionSpectral_Figures.setChecked(True)
        self.actionSpectral_Figures.setObjectName(_fromUtf8("actionSpectral_Figures"))
        self.actionTemporal_Numbers = QtGui.QAction(MainWindow)
        self.actionTemporal_Numbers.setCheckable(True)
        self.actionTemporal_Numbers.setChecked(True)
        self.actionTemporal_Numbers.setObjectName(_fromUtf8("actionTemporal_Numbers"))
        self.actionSpectral_Numbers = QtGui.QAction(MainWindow)
        self.actionSpectral_Numbers.setCheckable(True)
        self.actionSpectral_Numbers.setChecked(True)
        self.actionSpectral_Numbers.setObjectName(_fromUtf8("actionSpectral_Numbers"))
        self.actionSub_Elements_Peaks = QtGui.QAction(MainWindow)
        self.actionSub_Elements_Peaks.setCheckable(True)
        self.actionSub_Elements_Peaks.setObjectName(_fromUtf8("actionSub_Elements_Peaks"))
        self.actionElements_Peaks = QtGui.QAction(MainWindow)
        self.actionElements_Peaks.setCheckable(True)
        self.actionElements_Peaks.setObjectName(_fromUtf8("actionElements_Peaks"))
        self.actionOsgram_Image = QtGui.QAction(MainWindow)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/Camera.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOsgram_Image.setIcon(icon14)
        self.actionOsgram_Image.setObjectName(_fromUtf8("actionOsgram_Image"))
        self.actionSpecgram_Image = QtGui.QAction(MainWindow)
        self.actionSpecgram_Image.setIcon(icon14)
        self.actionSpecgram_Image.setObjectName(_fromUtf8("actionSpecgram_Image"))
        self.actionTemporal_Figures = QtGui.QAction(MainWindow)
        self.actionTemporal_Figures.setCheckable(True)
        self.actionTemporal_Figures.setChecked(True)
        self.actionTemporal_Figures.setObjectName(_fromUtf8("actionTemporal_Figures"))
        self.actionCombined_Image = QtGui.QAction(MainWindow)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/Photofiltre.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCombined_Image.setIcon(icon15)
        self.actionCombined_Image.setObjectName(_fromUtf8("actionCombined_Image"))
        self.actionFull_Screen = QtGui.QAction(MainWindow)
        self.actionFull_Screen.setCheckable(True)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/Position.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFull_Screen.setIcon(icon16)
        self.actionFull_Screen.setObjectName(_fromUtf8("actionFull_Screen"))
        self.actionExit = QtGui.QAction(MainWindow)
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/cerrar.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon17)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionRectangular_Cursor = QtGui.QAction(MainWindow)
        self.actionRectangular_Cursor.setCheckable(True)
        self.actionRectangular_Cursor.setObjectName(_fromUtf8("actionRectangular_Cursor"))
        self.actionRectangular_Eraser = QtGui.QAction(MainWindow)
        self.actionRectangular_Eraser.setCheckable(True)
        self.actionRectangular_Eraser.setObjectName(_fromUtf8("actionRectangular_Eraser"))
        self.actionZoom_Cursor = QtGui.QAction(MainWindow)
        self.actionZoom_Cursor.setCheckable(True)
        self.actionZoom_Cursor.setChecked(True)
        self.actionZoom_Cursor.setObjectName(_fromUtf8("actionZoom_Cursor"))
        self.actionPointer_Cursor = QtGui.QAction(MainWindow)
        self.actionPointer_Cursor.setCheckable(True)
        self.actionPointer_Cursor.setObjectName(_fromUtf8("actionPointer_Cursor"))
        self.actionSignalName = QtGui.QAction(MainWindow)
        self.actionSignalName.setObjectName(_fromUtf8("actionSignalName"))
        self.actionDelete_Selected_Elements = QtGui.QAction(MainWindow)
        icon18 = QtGui.QIcon()
        icon18.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/deleteElements.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDelete_Selected_Elements.setIcon(icon18)
        self.actionDelete_Selected_Elements.setObjectName(_fromUtf8("actionDelete_Selected_Elements"))
        self.actionDeselect_Elements = QtGui.QAction(MainWindow)
        icon19 = QtGui.QIcon()
        icon19.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/deselectElements.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDeselect_Elements.setIcon(icon19)
        self.actionDeselect_Elements.setObjectName(_fromUtf8("actionDeselect_Elements"))
        self.actionTwo_Dimensional_Graphs = QtGui.QAction(MainWindow)
        icon20 = QtGui.QIcon()
        icon20.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/2dgraphs.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionTwo_Dimensional_Graphs.setIcon(icon20)
        self.actionTwo_Dimensional_Graphs.setObjectName(_fromUtf8("actionTwo_Dimensional_Graphs"))
        self.actionTraining_Mode = QtGui.QAction(MainWindow)
        self.actionTraining_Mode.setCheckable(True)
        self.actionTraining_Mode.setChecked(True)
        self.actionTraining_Mode.setObjectName(_fromUtf8("actionTraining_Mode"))
        self.actionClassification_Settings = QtGui.QAction(MainWindow)
        icon21 = QtGui.QIcon()
        icon21.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/categories.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionClassification_Settings.setIcon(icon21)
        self.actionClassification_Settings.setObjectName(_fromUtf8("actionClassification_Settings"))
        self.actionMethod = QtGui.QAction(MainWindow)
        self.actionMethod.setObjectName(_fromUtf8("actionMethod"))
        self.toolBar.addAction(self.actionDetection)
        self.toolBar.addAction(self.actionTwo_Dimensional_Graphs)
        self.toolBar.addAction(self.actionDelete_Selected_Elements)
        self.toolBar.addAction(self.actionDeselect_Elements)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionClassification_Settings)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionZoomIn)
        self.toolBar.addAction(self.actionZoom_out)
        self.toolBar.addAction(self.actionZoom_out_entire_file)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPlay_Sound)
        self.toolBar.addAction(self.actionPause_Sound)
        self.toolBar.addAction(self.actionStop_Sound)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionFull_Screen)
        self.toolBar.addAction(self.actionCombined)
        self.toolBar.addAction(self.actionOscilogram)
        self.toolBar.addAction(self.actionSpectogram)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSignalName)
        self.menuPeak_Frecuencies.addAction(self.actionElements_Peaks)
        self.menuPeak_Frecuencies.addAction(self.actionSub_Elements_Peaks)
        self.menuParameters.addAction(self.actionView_Parameters)
        self.menuParameters.addAction(self.actionView_Threshold)
        self.menuParameters.addAction(self.actionTemporal_Elements)
        self.menuParameters.addAction(self.actionTemporal_Numbers)
        self.menuParameters.addAction(self.actionTemporal_Figures)
        self.menuParameters.addAction(self.actionSpectral_Elements)
        self.menuParameters.addAction(self.actionSpectral_Numbers)
        self.menuParameters.addAction(self.actionSpectral_Figures)
        self.menuParameters.addAction(self.menuPeak_Frecuencies.menuAction())
        self.menuParameters.addAction(self.actionFull_Screen)
        self.menuDetection.addAction(self.actionDetection)
        self.menuDetection.addAction(self.actionDelete_Selected_Elements)
        self.menuDetection.addAction(self.actionDeselect_Elements)
        self.menuDetection.addAction(self.actionMeditions)
        self.menuTools.addAction(self.actionZoomIn)
        self.menuTools.addAction(self.actionZoom_out)
        self.menuTools.addAction(self.actionZoom_out_entire_file)
        self.menuTools.addAction(self.actionFull_Screen)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionOsgram_Image)
        self.menuTools.addAction(self.actionSpecgram_Image)
        self.menuTools.addAction(self.actionCombined_Image)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionZoom_Cursor)
        self.menuTools.addAction(self.actionPointer_Cursor)
        self.menuTools.addAction(self.actionRectangular_Cursor)
        self.menuTools.addAction(self.actionRectangular_Eraser)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionTwo_Dimensional_Graphs)
        self.menuClasification.addAction(self.actionClassification_Settings)
        self.menuBar.addAction(self.menuDetection.menuAction())
        self.menuBar.addAction(self.menuClasification.menuAction())
        self.menuBar.addAction(self.menuTools.menuAction())
        self.menuBar.addAction(self.menuParameters.menuAction())

        self.retranslateUi(MainWindow)
        self.tabwidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.pushButtonInputFolder, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.selectInputFolder)
        QtCore.QObject.connect(self.pushButtonOutputFolder, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.selectOutputFolder)
        QtCore.QObject.connect(self.pushButtonStart, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.startBatchProcess)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Duetto Sound Lab", None, QtGui.QApplication.UnicodeUTF8))
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "Detection", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonInputFolder.setText(QtGui.QApplication.translate("MainWindow", "Explore", None, QtGui.QApplication.UnicodeUTF8))
        self.progressBarProcesed.setStyleSheet(QtGui.QApplication.translate("MainWindow", "background-color: rgb(200, 200, 255);", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditOutputFolder.setText(QtGui.QApplication.translate("MainWindow", "Select the folder of output procesed files", None, QtGui.QApplication.UnicodeUTF8))
        self.lineeditFilePath.setText(QtGui.QApplication.translate("MainWindow", "Select the folder of input audio files", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOutputFolder.setText(QtGui.QApplication.translate("MainWindow", "Explore", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Action", None, QtGui.QApplication.UnicodeUTF8))
        self.rbttnDetection.setText(QtGui.QApplication.translate("MainWindow", "Detection", None, QtGui.QApplication.UnicodeUTF8))
        self.rbttnSplitFile.setText(QtGui.QApplication.translate("MainWindow", "Split Files", None, QtGui.QApplication.UnicodeUTF8))
        self.spboxSplitTime.setSuffix(QtGui.QApplication.translate("MainWindow", "sec", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonStart.setText(QtGui.QApplication.translate("MainWindow", "Process", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxSingleFile.setText(QtGui.QApplication.translate("MainWindow", "Single Excell", None, QtGui.QApplication.UnicodeUTF8))
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.tab_2), QtGui.QApplication.translate("MainWindow", "Batch Process", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidgetParameterTableOscilogram.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Elements", None, QtGui.QApplication.UnicodeUTF8))
        self.tableParameterOscilogram.setToolTip(QtGui.QApplication.translate("MainWindow", "Oscilogram elements  meditions", None, QtGui.QApplication.UnicodeUTF8))
        self.menuParameters.setTitle(QtGui.QApplication.translate("MainWindow", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.menuPeak_Frecuencies.setTitle(QtGui.QApplication.translate("MainWindow", "Peak Frecuencies", None, QtGui.QApplication.UnicodeUTF8))
        self.menuDetection.setTitle(QtGui.QApplication.translate("MainWindow", "Detection", None, QtGui.QApplication.UnicodeUTF8))
        self.menuTools.setTitle(QtGui.QApplication.translate("MainWindow", "Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.menuClasification.setTitle(QtGui.QApplication.translate("MainWindow", "Classification", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoomIn.setText(QtGui.QApplication.translate("MainWindow", "Zoom in", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoomIn.setShortcut(QtGui.QApplication.translate("MainWindow", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoom_out.setText(QtGui.QApplication.translate("MainWindow", "Zoom out", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoom_out.setShortcut(QtGui.QApplication.translate("MainWindow", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSpectogram.setText(QtGui.QApplication.translate("MainWindow", "Spectogram", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOscilogram.setText(QtGui.QApplication.translate("MainWindow", "Oscillogram", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCombined.setText(QtGui.QApplication.translate("MainWindow", "Combined", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPlay_Sound.setText(QtGui.QApplication.translate("MainWindow", "Play Sound", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPlay_Sound.setShortcut(QtGui.QApplication.translate("MainWindow", "Space", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStop_Sound.setText(QtGui.QApplication.translate("MainWindow", "Stop Sound", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPause_Sound.setText(QtGui.QApplication.translate("MainWindow", "Pause Sound", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoom_out_entire_file.setText(QtGui.QApplication.translate("MainWindow", "Zoom out entire file", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setText(QtGui.QApplication.translate("MainWindow", "Copy", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+C", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPaste.setText(QtGui.QApplication.translate("MainWindow", "Paste", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPaste.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+V", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setText(QtGui.QApplication.translate("MainWindow", "Cut", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+X", None, QtGui.QApplication.UnicodeUTF8))
        self.actionMeditions.setText(QtGui.QApplication.translate("MainWindow", "Save Meditions", None, QtGui.QApplication.UnicodeUTF8))
        self.actionView_Parameters.setText(QtGui.QApplication.translate("MainWindow", "Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.actionView_Parameters.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Space", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDetection.setText(QtGui.QApplication.translate("MainWindow", "Detect Elements", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDetection.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+D", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClear_Meditions.setText(QtGui.QApplication.translate("MainWindow", "Clear Meditions", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClear_Meditions.setShortcut(QtGui.QApplication.translate("MainWindow", "Alt+E", None, QtGui.QApplication.UnicodeUTF8))
        self.actionView_Threshold.setText(QtGui.QApplication.translate("MainWindow", "Threshold", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTemporal_Elements.setText(QtGui.QApplication.translate("MainWindow", "Temporal Elements", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSpectral_Elements.setText(QtGui.QApplication.translate("MainWindow", "Spectral Elements", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSpectral_Figures.setText(QtGui.QApplication.translate("MainWindow", "Spectral Figures", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTemporal_Numbers.setText(QtGui.QApplication.translate("MainWindow", "Temporal Numbers", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSpectral_Numbers.setText(QtGui.QApplication.translate("MainWindow", "Spectral Numbers", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSub_Elements_Peaks.setText(QtGui.QApplication.translate("MainWindow", "Sub Elements Peaks", None, QtGui.QApplication.UnicodeUTF8))
        self.actionElements_Peaks.setText(QtGui.QApplication.translate("MainWindow", "Elements Peaks", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOsgram_Image.setText(QtGui.QApplication.translate("MainWindow", "Osgram Image", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSpecgram_Image.setText(QtGui.QApplication.translate("MainWindow", "Specgram Image", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTemporal_Figures.setText(QtGui.QApplication.translate("MainWindow", "Temporal Figures", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCombined_Image.setText(QtGui.QApplication.translate("MainWindow", "Combined Image", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFull_Screen.setText(QtGui.QApplication.translate("MainWindow", "Full Screen", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setShortcut(QtGui.QApplication.translate("MainWindow", "Esc", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRectangular_Cursor.setText(QtGui.QApplication.translate("MainWindow", "Rectangular_Cursor", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRectangular_Eraser.setText(QtGui.QApplication.translate("MainWindow", "Rectangular_Eraser", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoom_Cursor.setText(QtGui.QApplication.translate("MainWindow", "Zoom_Cursor", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPointer_Cursor.setText(QtGui.QApplication.translate("MainWindow", "Pointer Cursor", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSignalName.setText(QtGui.QApplication.translate("MainWindow", "SignalName", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDelete_Selected_Elements.setText(QtGui.QApplication.translate("MainWindow", "Delete Selected Elements", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDeselect_Elements.setText(QtGui.QApplication.translate("MainWindow", "Deselect Elements", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTwo_Dimensional_Graphs.setText(QtGui.QApplication.translate("MainWindow", "Two Dimensional Graphs", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTraining_Mode.setText(QtGui.QApplication.translate("MainWindow", "Training Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClassification_Settings.setText(QtGui.QApplication.translate("MainWindow", "Edit Categories", None, QtGui.QApplication.UnicodeUTF8))
        self.actionMethod.setText(QtGui.QApplication.translate("MainWindow", "Method", None, QtGui.QApplication.UnicodeUTF8))

from pyqtgraph import TableWidget
from graphic_interface.widgets.QSignalDetectorWidget import QSignalDetectorWidget
import icons_rc
