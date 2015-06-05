# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Fac Biologia\DUETTO PROGRAMS\Desktop\Sound Lab\duetto-SoundLab\graphic_interface\UI_Files\SegmentationAndClasificationWindowUI.ui'
#
# Created: Fri Jun 05 09:44:23 2015
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
        self.tableParameterOscilogram.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
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
        self.actionRecord = QtGui.QAction(MainWindow)
        icon22 = QtGui.QIcon()
        icon22.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/record_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRecord.setIcon(icon22)
        self.actionRecord.setObjectName(_fromUtf8("actionRecord"))
        self.actionPlayLoop = QtGui.QAction(MainWindow)
        self.actionPlayLoop.setCheckable(True)
        icon23 = QtGui.QIcon()
        icon23.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/Behavior.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPlayLoop.setIcon(icon23)
        self.actionPlayLoop.setObjectName(_fromUtf8("actionPlayLoop"))
        self.actionAddElement = QtGui.QAction(MainWindow)
        icon24 = QtGui.QIcon()
        icon24.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAddElement.setIcon(icon24)
        self.actionAddElement.setObjectName(_fromUtf8("actionAddElement"))
        self.actionSound_File_Segmentation = QtGui.QAction(MainWindow)
        icon25 = QtGui.QIcon()
        icon25.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/225.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSound_File_Segmentation.setIcon(icon25)
        self.actionSound_File_Segmentation.setObjectName(_fromUtf8("actionSound_File_Segmentation"))
        self.actionTemporal_Parameters = QtGui.QAction(MainWindow)
        self.actionTemporal_Parameters.setCheckable(True)
        self.actionTemporal_Parameters.setChecked(True)
        self.actionTemporal_Parameters.setObjectName(_fromUtf8("actionTemporal_Parameters"))
        self.actionSpectral_Parameters = QtGui.QAction(MainWindow)
        self.actionSpectral_Parameters.setCheckable(True)
        self.actionSpectral_Parameters.setChecked(True)
        self.actionSpectral_Parameters.setObjectName(_fromUtf8("actionSpectral_Parameters"))
        self.actionCross_correlation = QtGui.QAction(MainWindow)
        icon26 = QtGui.QIcon()
        icon26.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/cross-correlation.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCross_correlation.setIcon(icon26)
        self.actionCross_correlation.setObjectName(_fromUtf8("actionCross_correlation"))
        self.actionSelectedElement_Correlation = QtGui.QAction(MainWindow)
        self.actionSelectedElement_Correlation.setObjectName(_fromUtf8("actionSelectedElement_Correlation"))
        self.actionClassify = QtGui.QAction(MainWindow)
        self.actionClassify.setObjectName(_fromUtf8("actionClassify"))
        self.actionDelete_All = QtGui.QAction(MainWindow)
        self.actionDelete_All.setObjectName(_fromUtf8("actionDelete_All"))
        self.actionParameter_Measurement = QtGui.QAction(MainWindow)
        self.actionParameter_Measurement.setObjectName(_fromUtf8("actionParameter_Measurement"))
        self.toolBar.addAction(self.actionCross_correlation)
        self.menuParameters.addAction(self.actionView_Parameters)
        self.menuParameters.addAction(self.actionFull_Screen)
        self.menuParameters.addSeparator()
        self.menuParameters.addAction(self.actionTwo_Dimensional_Graphs)
        self.menuParameters.addSeparator()
        self.menuParameters.addAction(self.actionTemporal_Elements)
        self.menuParameters.addAction(self.actionTemporal_Numbers)
        self.menuParameters.addAction(self.actionTemporal_Figures)
        self.menuParameters.addAction(self.actionTemporal_Parameters)
        self.menuParameters.addSeparator()
        self.menuParameters.addAction(self.actionSpectral_Elements)
        self.menuParameters.addAction(self.actionSpectral_Numbers)
        self.menuParameters.addAction(self.actionSpectral_Figures)
        self.menuParameters.addAction(self.actionSpectral_Parameters)
        self.menuParameters.addSeparator()
        self.menuDetection.addAction(self.actionAddElement)
        self.menuDetection.addAction(self.actionDelete_Selected_Elements)
        self.menuDetection.addAction(self.actionDelete_All)
        self.menuDetection.addAction(self.actionDetection)
        self.menuDetection.addAction(self.actionParameter_Measurement)
        self.menuDetection.addSeparator()
        self.menuDetection.addAction(self.actionClassify)
        self.menuDetection.addAction(self.actionDeselect_Elements)
        self.menuTools.addAction(self.actionZoomIn)
        self.menuTools.addAction(self.actionZoom_out)
        self.menuTools.addAction(self.actionZoom_out_entire_file)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionZoom_Cursor)
        self.menuTools.addAction(self.actionPointer_Cursor)
        self.menuTools.addAction(self.actionRectangular_Cursor)
        self.menuGraph_Images.addAction(self.actionOsc_Image)
        self.menuGraph_Images.addAction(self.actionSpecgram_Image)
        self.menuGraph_Images.addAction(self.actionCombined_Image)
        self.menuExport.addAction(self.actionMeditions)
        self.menuExport.addAction(self.actionSound_File_Segmentation)
        self.menuExport.addAction(self.menuGraph_Images.menuAction())
        self.menuBar.addAction(self.menuDetection.menuAction())
        self.menuBar.addAction(self.menuExport.menuAction())
        self.menuBar.addAction(self.menuTools.menuAction())
        self.menuBar.addAction(self.menuParameters.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "duetto Sound Lab", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.dockWidgetParameterTableOscilogram.setWindowTitle(_translate("MainWindow", "Elements", None))
        self.tableParameterOscilogram.setToolTip(_translate("MainWindow", "Oscilogram elements  meditions", None))
        self.menuParameters.setTitle(_translate("MainWindow", "View", None))
        self.menuDetection.setTitle(_translate("MainWindow", "Elements", None))
        self.menuTools.setTitle(_translate("MainWindow", "Tools", None))
        self.menuExport.setTitle(_translate("MainWindow", "Export", None))
        self.menuGraph_Images.setTitle(_translate("MainWindow", "Graph Images", None))
        self.actionZoomIn.setText(_translate("MainWindow", "Zoom in", None))
        self.actionZoomIn.setShortcut(_translate("MainWindow", "+", None))
        self.actionZoom_out.setText(_translate("MainWindow", "Zoom out", None))
        self.actionZoom_out.setShortcut(_translate("MainWindow", "-", None))
        self.actionSpectogram.setText(_translate("MainWindow", "Spectogram", None))
        self.actionOscilogram.setText(_translate("MainWindow", "Oscillogram", None))
        self.actionCombined.setText(_translate("MainWindow", "Combined", None))
        self.actionPlay_Sound.setText(_translate("MainWindow", "Play Sound", None))
        self.actionPlay_Sound.setShortcut(_translate("MainWindow", "Space", None))
        self.actionStop_Sound.setText(_translate("MainWindow", "Stop Sound", None))
        self.actionPause_Sound.setText(_translate("MainWindow", "Pause Sound", None))
        self.actionZoom_out_entire_file.setText(_translate("MainWindow", "Zoom None", None))
        self.actionCopy.setText(_translate("MainWindow", "Copy", None))
        self.actionCopy.setShortcut(_translate("MainWindow", "Ctrl+C", None))
        self.actionPaste.setText(_translate("MainWindow", "Paste", None))
        self.actionPaste.setShortcut(_translate("MainWindow", "Ctrl+V", None))
        self.actionCut.setText(_translate("MainWindow", "Cut", None))
        self.actionCut.setShortcut(_translate("MainWindow", "Ctrl+X", None))
        self.actionMeditions.setText(_translate("MainWindow", "Measurements as Excel", None))
        self.actionView_Parameters.setText(_translate("MainWindow", "Parameters", None))
        self.actionView_Parameters.setShortcut(_translate("MainWindow", "Ctrl+Space", None))
        self.actionDetection.setText(_translate("MainWindow", "Detect", None))
        self.actionDetection.setShortcut(_translate("MainWindow", "Ctrl+D", None))
        self.actionTemporal_Elements.setText(_translate("MainWindow", "Temporal Elements", None))
        self.actionSpectral_Elements.setText(_translate("MainWindow", "Spectral Elements", None))
        self.actionSpectral_Figures.setText(_translate("MainWindow", "Spectral Figures", None))
        self.actionTemporal_Numbers.setText(_translate("MainWindow", "Temporal Numbers", None))
        self.actionSpectral_Numbers.setText(_translate("MainWindow", "Spectral Numbers", None))
        self.actionSub_Elements_Peaks.setText(_translate("MainWindow", "Sub Elements Peaks", None))
        self.actionOsc_Image.setText(_translate("MainWindow", "Osgram Image", None))
        self.actionSpecgram_Image.setText(_translate("MainWindow", "Specgram Image", None))
        self.actionTemporal_Figures.setText(_translate("MainWindow", "Temporal Figures", None))
        self.actionCombined_Image.setText(_translate("MainWindow", "Combined Image", None))
        self.actionFull_Screen.setText(_translate("MainWindow", "Full Screen", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        self.actionExit.setShortcut(_translate("MainWindow", "Esc", None))
        self.actionRectangular_Cursor.setText(_translate("MainWindow", "Rectangular_Cursor", None))
        self.actionZoom_Cursor.setText(_translate("MainWindow", "Zoom_Cursor", None))
        self.actionPointer_Cursor.setText(_translate("MainWindow", "Pointer Cursor", None))
        self.actionSignalName.setText(_translate("MainWindow", "SignalName", None))
        self.actionDelete_Selected_Elements.setText(_translate("MainWindow", "Delete", None))
        self.actionDeselect_Elements.setText(_translate("MainWindow", "Deselect", None))
        self.actionTwo_Dimensional_Graphs.setText(_translate("MainWindow", "Two Dimensional Graphs", None))
        self.actionRecord.setText(_translate("MainWindow", "Record", None))
        self.actionPlayLoop.setText(_translate("MainWindow", "PlayLoop", None))
        self.actionPlayLoop.setToolTip(_translate("MainWindow", "Play Loop", None))
        self.actionAddElement.setText(_translate("MainWindow", "Add", None))
        self.actionAddElement.setToolTip(_translate("MainWindow", "Mark Selected Region As Element", None))
        self.actionSound_File_Segmentation.setText(_translate("MainWindow", "Segmentation on file", None))
        self.actionTemporal_Parameters.setText(_translate("MainWindow", "Temporal Parameters", None))
        self.actionSpectral_Parameters.setText(_translate("MainWindow", "Spectral Parameters", None))
        self.actionCross_correlation.setText(_translate("MainWindow", "Cross-correlation", None))
        self.actionSelectedElement_Correlation.setText(_translate("MainWindow", "Selected Element Correlation", None))
        self.actionClassify.setText(_translate("MainWindow", "Classify", None))
        self.actionDelete_All.setText(_translate("MainWindow", "Delete All", None))
        self.actionDelete_All.setToolTip(_translate("MainWindow", "Delete All the detected elements", None))
        self.actionParameter_Measurement.setText(_translate("MainWindow", "Parameter Measurement", None))

from graphic_interface.widgets.SoundLabToolBar import SoundLabToolBarWidget
from pyqtgraph import TableWidget
from graphic_interface.widgets.QSignalDetectorWidget import QSignalDetectorWidget
import icons_rc
