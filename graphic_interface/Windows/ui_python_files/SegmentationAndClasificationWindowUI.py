# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'graphic_interface\UI_Files\SegmentationAndClasificationWindowUI.ui'
#
# Created: Tue Feb 17 14:08:20 2015
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
        MainWindow.resize(596, 390)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/duetto_logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(_fromUtf8(""))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setStyleSheet(_fromUtf8(""))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.widget = QSignalDetectorWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout_2.addWidget(self.widget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = SoundLabToolBarWidget(MainWindow)
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
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 596, 21))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuParameters = QtGui.QMenu(self.menuBar)
        self.menuParameters.setObjectName(_fromUtf8("menuParameters"))
        self.menuDetection = QtGui.QMenu(self.menuBar)
        self.menuDetection.setObjectName(_fromUtf8("menuDetection"))
        self.menuTools = QtGui.QMenu(self.menuBar)
        self.menuTools.setObjectName(_fromUtf8("menuTools"))
        self.menuClasification = QtGui.QMenu(self.menuBar)
        self.menuClasification.setObjectName(_fromUtf8("menuClasification"))
        self.menuExport = QtGui.QMenu(self.menuBar)
        self.menuExport.setObjectName(_fromUtf8("menuExport"))
        self.menuGraph_Images = QtGui.QMenu(self.menuExport)
        self.menuGraph_Images.setObjectName(_fromUtf8("menuGraph_Images"))
        MainWindow.setMenuBar(self.menuBar)
        self.actionZoomIn = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/zoomin_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoomIn.setIcon(icon1)
        self.actionZoomIn.setObjectName(_fromUtf8("actionZoomIn"))
        self.actionZoom_out = QtGui.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/zoomout_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoom_out.setIcon(icon2)
        self.actionZoom_out.setObjectName(_fromUtf8("actionZoom_out"))
        self.actionSpectogram = QtGui.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/spec.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSpectogram.setIcon(icon3)
        self.actionSpectogram.setObjectName(_fromUtf8("actionSpectogram"))
        self.actionOscilogram = QtGui.QAction(MainWindow)
        self.actionOscilogram.setEnabled(True)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/osc.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOscilogram.setIcon(icon4)
        self.actionOscilogram.setVisible(True)
        self.actionOscilogram.setObjectName(_fromUtf8("actionOscilogram"))
        self.actionCombined = QtGui.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/combined.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCombined.setIcon(icon5)
        self.actionCombined.setObjectName(_fromUtf8("actionCombined"))
        self.actionPlay_Sound = QtGui.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/02049_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPlay_Sound.setIcon(icon6)
        self.actionPlay_Sound.setObjectName(_fromUtf8("actionPlay_Sound"))
        self.actionStop_Sound = QtGui.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/02051_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionStop_Sound.setIcon(icon7)
        self.actionStop_Sound.setObjectName(_fromUtf8("actionStop_Sound"))
        self.actionPause_Sound = QtGui.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/pausa.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPause_Sound.setIcon(icon8)
        self.actionPause_Sound.setObjectName(_fromUtf8("actionPause_Sound"))
        self.actionZoom_out_entire_file = QtGui.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/zoom_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoom_out_entire_file.setIcon(icon9)
        self.actionZoom_out_entire_file.setObjectName(_fromUtf8("actionZoom_out_entire_file"))
        self.actionCopy = QtGui.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/copy_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCopy.setIcon(icon10)
        self.actionCopy.setObjectName(_fromUtf8("actionCopy"))
        self.actionPaste = QtGui.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/paste_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPaste.setIcon(icon11)
        self.actionPaste.setObjectName(_fromUtf8("actionPaste"))
        self.actionCut = QtGui.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/cut_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCut.setIcon(icon12)
        self.actionCut.setObjectName(_fromUtf8("actionCut"))
        self.actionMeditions = QtGui.QAction(MainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/Excel.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionMeditions.setIcon(icon13)
        self.actionMeditions.setObjectName(_fromUtf8("actionMeditions"))
        self.actionView_Parameters = QtGui.QAction(MainWindow)
        self.actionView_Parameters.setCheckable(True)
        self.actionView_Parameters.setObjectName(_fromUtf8("actionView_Parameters"))
        self.actionDetection = QtGui.QAction(MainWindow)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/Process Viewer.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDetection.setIcon(icon14)
        self.actionDetection.setObjectName(_fromUtf8("actionDetection"))
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
        self.actionOsc_Image = QtGui.QAction(MainWindow)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/Camera.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOsc_Image.setIcon(icon15)
        self.actionOsc_Image.setObjectName(_fromUtf8("actionOsc_Image"))
        self.actionSpecgram_Image = QtGui.QAction(MainWindow)
        self.actionSpecgram_Image.setIcon(icon15)
        self.actionSpecgram_Image.setObjectName(_fromUtf8("actionSpecgram_Image"))
        self.actionTemporal_Figures = QtGui.QAction(MainWindow)
        self.actionTemporal_Figures.setCheckable(True)
        self.actionTemporal_Figures.setChecked(True)
        self.actionTemporal_Figures.setObjectName(_fromUtf8("actionTemporal_Figures"))
        self.actionCombined_Image = QtGui.QAction(MainWindow)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/Photofiltre.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCombined_Image.setIcon(icon16)
        self.actionCombined_Image.setObjectName(_fromUtf8("actionCombined_Image"))
        self.actionFull_Screen = QtGui.QAction(MainWindow)
        self.actionFull_Screen.setCheckable(True)
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/Position.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFull_Screen.setIcon(icon17)
        self.actionFull_Screen.setObjectName(_fromUtf8("actionFull_Screen"))
        self.actionExit = QtGui.QAction(MainWindow)
        icon18 = QtGui.QIcon()
        icon18.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/cerrar.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon18)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionRectangular_Cursor = QtGui.QAction(MainWindow)
        self.actionRectangular_Cursor.setCheckable(True)
        self.actionRectangular_Cursor.setObjectName(_fromUtf8("actionRectangular_Cursor"))
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
        icon19 = QtGui.QIcon()
        icon19.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/deleteElements.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDelete_Selected_Elements.setIcon(icon19)
        self.actionDelete_Selected_Elements.setObjectName(_fromUtf8("actionDelete_Selected_Elements"))
        self.actionDeselect_Elements = QtGui.QAction(MainWindow)
        icon20 = QtGui.QIcon()
        icon20.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/deselectElements.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDeselect_Elements.setIcon(icon20)
        self.actionDeselect_Elements.setObjectName(_fromUtf8("actionDeselect_Elements"))
        self.actionTwo_Dimensional_Graphs = QtGui.QAction(MainWindow)
        icon21 = QtGui.QIcon()
        icon21.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/2dgraphs.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionTwo_Dimensional_Graphs.setIcon(icon21)
        self.actionTwo_Dimensional_Graphs.setObjectName(_fromUtf8("actionTwo_Dimensional_Graphs"))
        self.actionClassification_Settings = QtGui.QAction(MainWindow)
        icon22 = QtGui.QIcon()
        icon22.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/ColorSync Utility.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionClassification_Settings.setIcon(icon22)
        self.actionClassification_Settings.setObjectName(_fromUtf8("actionClassification_Settings"))
        self.actionRecord = QtGui.QAction(MainWindow)
        icon23 = QtGui.QIcon()
        icon23.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/record_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRecord.setIcon(icon23)
        self.actionRecord.setObjectName(_fromUtf8("actionRecord"))
        self.actionPlayLoop = QtGui.QAction(MainWindow)
        self.actionPlayLoop.setCheckable(True)
        icon24 = QtGui.QIcon()
        icon24.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/Behavior.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPlayLoop.setIcon(icon24)
        self.actionPlayLoop.setObjectName(_fromUtf8("actionPlayLoop"))
        self.actionAddElement = QtGui.QAction(MainWindow)
        icon25 = QtGui.QIcon()
        icon25.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAddElement.setIcon(icon25)
        self.actionAddElement.setObjectName(_fromUtf8("actionAddElement"))
        self.actionSound_File_Segmentation = QtGui.QAction(MainWindow)
        icon26 = QtGui.QIcon()
        icon26.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/225.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSound_File_Segmentation.setIcon(icon26)
        self.actionSound_File_Segmentation.setObjectName(_fromUtf8("actionSound_File_Segmentation"))
        self.actionCross_correlation = QtGui.QAction(MainWindow)
        icon27 = QtGui.QIcon()
        icon27.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/cross-correlation.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCross_correlation.setIcon(icon27)
        self.actionCross_correlation.setObjectName(_fromUtf8("actionCross_correlation"))
        self.toolBar.addAction(self.actionClassification_Settings)
        self.toolBar.addAction(self.actionCross_correlation)
        self.menuParameters.addAction(self.actionView_Parameters)
        self.menuParameters.addSeparator()
        self.menuParameters.addAction(self.actionZoomIn)
        self.menuParameters.addAction(self.actionZoom_out)
        self.menuParameters.addAction(self.actionZoom_out_entire_file)
        self.menuParameters.addSeparator()
        self.menuParameters.addAction(self.actionTemporal_Elements)
        self.menuParameters.addAction(self.actionTemporal_Numbers)
        self.menuParameters.addAction(self.actionTemporal_Figures)
        self.menuParameters.addAction(self.actionSpectral_Elements)
        self.menuParameters.addAction(self.actionSpectral_Numbers)
        self.menuParameters.addAction(self.actionSpectral_Figures)
        self.menuParameters.addSeparator()
        self.menuParameters.addAction(self.actionTwo_Dimensional_Graphs)
        self.menuParameters.addAction(self.actionFull_Screen)
        self.menuDetection.addAction(self.actionDetection)
        self.menuDetection.addAction(self.actionDelete_Selected_Elements)
        self.menuDetection.addAction(self.actionDeselect_Elements)
        self.menuDetection.addAction(self.actionAddElement)
        self.menuTools.addAction(self.actionZoom_Cursor)
        self.menuTools.addAction(self.actionPointer_Cursor)
        self.menuTools.addAction(self.actionRectangular_Cursor)
        self.menuClasification.addAction(self.actionClassification_Settings)
        self.menuClasification.addAction(self.actionCross_correlation)
        self.menuGraph_Images.addAction(self.actionOsc_Image)
        self.menuGraph_Images.addAction(self.actionSpecgram_Image)
        self.menuGraph_Images.addAction(self.actionCombined_Image)
        self.menuExport.addAction(self.actionMeditions)
        self.menuExport.addAction(self.menuGraph_Images.menuAction())
        self.menuExport.addAction(self.actionSound_File_Segmentation)
        self.menuBar.addAction(self.menuExport.menuAction())
        self.menuBar.addAction(self.menuDetection.menuAction())
        self.menuBar.addAction(self.menuClasification.menuAction())
        self.menuBar.addAction(self.menuTools.menuAction())
        self.menuBar.addAction(self.menuParameters.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "duetto Sound Lab", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidgetParameterTableOscilogram.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Elements", None, QtGui.QApplication.UnicodeUTF8))
        self.tableParameterOscilogram.setToolTip(QtGui.QApplication.translate("MainWindow", "Oscilogram elements  meditions", None, QtGui.QApplication.UnicodeUTF8))
        self.menuParameters.setTitle(QtGui.QApplication.translate("MainWindow", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.menuDetection.setTitle(QtGui.QApplication.translate("MainWindow", "Detection", None, QtGui.QApplication.UnicodeUTF8))
        self.menuTools.setTitle(QtGui.QApplication.translate("MainWindow", "Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.menuClasification.setTitle(QtGui.QApplication.translate("MainWindow", "Classification", None, QtGui.QApplication.UnicodeUTF8))
        self.menuExport.setTitle(QtGui.QApplication.translate("MainWindow", "Export", None, QtGui.QApplication.UnicodeUTF8))
        self.menuGraph_Images.setTitle(QtGui.QApplication.translate("MainWindow", "Graph Images", None, QtGui.QApplication.UnicodeUTF8))
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
        self.actionZoom_out_entire_file.setText(QtGui.QApplication.translate("MainWindow", "Zoom None", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setText(QtGui.QApplication.translate("MainWindow", "Copy", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+C", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPaste.setText(QtGui.QApplication.translate("MainWindow", "Paste", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPaste.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+V", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setText(QtGui.QApplication.translate("MainWindow", "Cut", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+X", None, QtGui.QApplication.UnicodeUTF8))
        self.actionMeditions.setText(QtGui.QApplication.translate("MainWindow", "Measurements", None, QtGui.QApplication.UnicodeUTF8))
        self.actionView_Parameters.setText(QtGui.QApplication.translate("MainWindow", "Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.actionView_Parameters.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Space", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDetection.setText(QtGui.QApplication.translate("MainWindow", "Detect Elements", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDetection.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+D", None, QtGui.QApplication.UnicodeUTF8))
        self.actionView_Threshold.setText(QtGui.QApplication.translate("MainWindow", "Threshold", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTemporal_Elements.setText(QtGui.QApplication.translate("MainWindow", "Temporal Elements", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSpectral_Elements.setText(QtGui.QApplication.translate("MainWindow", "Spectral Elements", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSpectral_Figures.setText(QtGui.QApplication.translate("MainWindow", "Spectral Figures", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTemporal_Numbers.setText(QtGui.QApplication.translate("MainWindow", "Temporal Numbers", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSpectral_Numbers.setText(QtGui.QApplication.translate("MainWindow", "Spectral Numbers", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSub_Elements_Peaks.setText(QtGui.QApplication.translate("MainWindow", "Sub Elements Peaks", None, QtGui.QApplication.UnicodeUTF8))
        self.actionElements_Peaks.setText(QtGui.QApplication.translate("MainWindow", "Elements Peaks", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOsc_Image.setText(QtGui.QApplication.translate("MainWindow", "Osgram Image", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSpecgram_Image.setText(QtGui.QApplication.translate("MainWindow", "Specgram Image", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTemporal_Figures.setText(QtGui.QApplication.translate("MainWindow", "Temporal Figures", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCombined_Image.setText(QtGui.QApplication.translate("MainWindow", "Combined Image", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFull_Screen.setText(QtGui.QApplication.translate("MainWindow", "Full Screen", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setShortcut(QtGui.QApplication.translate("MainWindow", "Esc", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRectangular_Cursor.setText(QtGui.QApplication.translate("MainWindow", "Rectangular_Cursor", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoom_Cursor.setText(QtGui.QApplication.translate("MainWindow", "Zoom_Cursor", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPointer_Cursor.setText(QtGui.QApplication.translate("MainWindow", "Pointer Cursor", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSignalName.setText(QtGui.QApplication.translate("MainWindow", "SignalName", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDelete_Selected_Elements.setText(QtGui.QApplication.translate("MainWindow", "Delete Selected Elements", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDeselect_Elements.setText(QtGui.QApplication.translate("MainWindow", "Deselect Elements", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTwo_Dimensional_Graphs.setText(QtGui.QApplication.translate("MainWindow", "Two Dimensional Graphs", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClassification_Settings.setText(QtGui.QApplication.translate("MainWindow", "Edit Categories", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRecord.setText(QtGui.QApplication.translate("MainWindow", "Record", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPlayLoop.setText(QtGui.QApplication.translate("MainWindow", "PlayLoop", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPlayLoop.setToolTip(QtGui.QApplication.translate("MainWindow", "Play Loop", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAddElement.setText(QtGui.QApplication.translate("MainWindow", "AddElement", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAddElement.setToolTip(QtGui.QApplication.translate("MainWindow", "Mark Selected Region As Element", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSound_File_Segmentation.setText(QtGui.QApplication.translate("MainWindow", "Sound File Segmentation", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCross_correlation.setText(QtGui.QApplication.translate("MainWindow", "Cross-correlation", None, QtGui.QApplication.UnicodeUTF8))

from graphic_interface.widgets.SoundLabToolBar import SoundLabToolBarWidget
from pyqtgraph import TableWidget
from graphic_interface.widgets.QSignalDetectorWidget import QSignalDetectorWidget
import icons_rc
