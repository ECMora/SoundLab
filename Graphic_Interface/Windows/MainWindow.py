# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Biologia\DUETTO PROGRAMS\Desktop\Sound Lab\DuettoSystem\graphic_interface\UI_Files\MainWindow.ui'
#
# Created: Sun Nov 23 11:55:13 2014
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DuettoMainWindow(object):
    def setupUi(self, DuettoMainWindow):
        DuettoMainWindow.setObjectName(_fromUtf8("DuettoMainWindow"))
        DuettoMainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        DuettoMainWindow.resize(936, 593)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DuettoMainWindow.sizePolicy().hasHeightForWidth())
        DuettoMainWindow.setSizePolicy(sizePolicy)
        DuettoMainWindow.setAutoFillBackground(False)
        DuettoMainWindow.setStyleSheet(_fromUtf8("color: rgb(0, 0, 0);\n"
"background-color: qlineargradient(spread:pad, x1:0.517, y1:0.0337727, x2:0.528682, y2:1, stop:0.0284091 rgba(88, 120, 223, 255), stop:0.988636 rgba(255, 255, 255, 250));\n"
"selection-color: rgb(0, 0, 0);"))
        self.centralwidget = QtGui.QWidget(DuettoMainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.widget = QSignalVisualizerWidget(self.centralwidget)
        self.widget.setStyleSheet(_fromUtf8("background-color: rgb(217, 217, 217);\n"
"border-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.136364 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));"))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout_2.addWidget(self.widget)
        self.horizontalScrollBar = QtGui.QScrollBar(self.centralwidget)
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName(_fromUtf8("horizontalScrollBar"))
        self.verticalLayout_2.addWidget(self.horizontalScrollBar)
        DuettoMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(DuettoMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 936, 21))
        self.menubar.setAutoFillBackground(False)
        self.menubar.setStyleSheet(_fromUtf8(""))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setGeometry(QtCore.QRect(42, 141, 158, 288))
        self.menuFile.setAutoFillBackground(False)
        self.menuFile.setStyleSheet(_fromUtf8(""))
        self.menuFile.setTearOffEnabled(False)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuTools = QtGui.QMenu(self.menubar)
        self.menuTools.setStyleSheet(_fromUtf8(""))
        self.menuTools.setObjectName(_fromUtf8("menuTools"))
        self.menuExport = QtGui.QMenu(self.menuTools)
        self.menuExport.setObjectName(_fromUtf8("menuExport"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setStyleSheet(_fromUtf8(""))
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuGenerate = QtGui.QMenu(self.menuEdit)
        self.menuGenerate.setObjectName(_fromUtf8("menuGenerate"))
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setStyleSheet(_fromUtf8(""))
        self.menuView.setObjectName(_fromUtf8("menuView"))
        self.menuSound = QtGui.QMenu(self.menubar)
        self.menuSound.setStyleSheet(_fromUtf8(""))
        self.menuSound.setObjectName(_fromUtf8("menuSound"))
        self.menuPlay_Speed = QtGui.QMenu(self.menuSound)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/Macromedia.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuPlay_Speed.setIcon(icon)
        self.menuPlay_Speed.setObjectName(_fromUtf8("menuPlay_Speed"))
        DuettoMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(DuettoMainWindow)
        self.statusbar.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        DuettoMainWindow.setStatusBar(self.statusbar)
        self.dock_settings = QtGui.QDockWidget(DuettoMainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dock_settings.sizePolicy().hasHeightForWidth())
        self.dock_settings.setSizePolicy(sizePolicy)
        self.dock_settings.setMinimumSize(QtCore.QSize(250, 40))
        self.dock_settings.setMaximumSize(QtCore.QSize(250, 524287))
        self.dock_settings.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.dock_settings.setFloating(False)
        self.dock_settings.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
        self.dock_settings.setObjectName(_fromUtf8("dock_settings"))
        self.osc_settings_contents = QtGui.QWidget()
        self.osc_settings_contents.setObjectName(_fromUtf8("osc_settings_contents"))
        self.dock_settings.setWidget(self.osc_settings_contents)
        DuettoMainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dock_settings)
        self.toolBar = QtGui.QToolBar(DuettoMainWindow)
        self.toolBar.setStyleSheet(_fromUtf8(""))
        self.toolBar.setIconSize(QtCore.QSize(20, 20))
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        DuettoMainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionOpen = QtGui.QAction(DuettoMainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/81.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon1)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionExit = QtGui.QAction(DuettoMainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/cerrar.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon2)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionZoomIn = QtGui.QAction(DuettoMainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/zoomin_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoomIn.setIcon(icon3)
        self.actionZoomIn.setObjectName(_fromUtf8("actionZoomIn"))
        self.actionZoom_out = QtGui.QAction(DuettoMainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/zoomout_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoom_out.setIcon(icon4)
        self.actionZoom_out.setObjectName(_fromUtf8("actionZoom_out"))
        self.actionSpectogram = QtGui.QAction(DuettoMainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/spec.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSpectogram.setIcon(icon5)
        self.actionSpectogram.setObjectName(_fromUtf8("actionSpectogram"))
        self.actionOscilogram = QtGui.QAction(DuettoMainWindow)
        self.actionOscilogram.setEnabled(True)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/osc.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOscilogram.setIcon(icon6)
        self.actionOscilogram.setVisible(True)
        self.actionOscilogram.setObjectName(_fromUtf8("actionOscilogram"))
        self.actionCombined = QtGui.QAction(DuettoMainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/combined.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCombined.setIcon(icon7)
        self.actionCombined.setObjectName(_fromUtf8("actionCombined"))
        self.actionNew = QtGui.QAction(DuettoMainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/Leopard Icon 60.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon8)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionPower_Spectrum = QtGui.QAction(DuettoMainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/powerspec.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPower_Spectrum.setIcon(icon9)
        self.actionPower_Spectrum.setObjectName(_fromUtf8("actionPower_Spectrum"))
        self.actionOscillogram_Settings = QtGui.QAction(DuettoMainWindow)
        self.actionOscillogram_Settings.setObjectName(_fromUtf8("actionOscillogram_Settings"))
        self.actionSpectogram_Settings = QtGui.QAction(DuettoMainWindow)
        self.actionSpectogram_Settings.setObjectName(_fromUtf8("actionSpectogram_Settings"))
        self.actionPower_Spectrum_Settings = QtGui.QAction(DuettoMainWindow)
        self.actionPower_Spectrum_Settings.setObjectName(_fromUtf8("actionPower_Spectrum_Settings"))
        self.actionPlay_Sound = QtGui.QAction(DuettoMainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/02049_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPlay_Sound.setIcon(icon10)
        self.actionPlay_Sound.setObjectName(_fromUtf8("actionPlay_Sound"))
        self.actionStop_Sound = QtGui.QAction(DuettoMainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/02051_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionStop_Sound.setIcon(icon11)
        self.actionStop_Sound.setObjectName(_fromUtf8("actionStop_Sound"))
        self.actionPause_Sound = QtGui.QAction(DuettoMainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/pausa.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPause_Sound.setIcon(icon12)
        self.actionPause_Sound.setObjectName(_fromUtf8("actionPause_Sound"))
        self.actionZoom_out_entire_file = QtGui.QAction(DuettoMainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/zoom_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoom_out_entire_file.setIcon(icon13)
        self.actionZoom_out_entire_file.setObjectName(_fromUtf8("actionZoom_out_entire_file"))
        self.actionSave = QtGui.QAction(DuettoMainWindow)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/225.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon14)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionCopy = QtGui.QAction(DuettoMainWindow)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/copy_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCopy.setIcon(icon15)
        self.actionCopy.setObjectName(_fromUtf8("actionCopy"))
        self.actionPaste = QtGui.QAction(DuettoMainWindow)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/paste_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPaste.setIcon(icon16)
        self.actionPaste.setObjectName(_fromUtf8("actionPaste"))
        self.actionCut = QtGui.QAction(DuettoMainWindow)
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/cut_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCut.setIcon(icon17)
        self.actionCut.setObjectName(_fromUtf8("actionCut"))
        self.actionSettings = QtGui.QAction(DuettoMainWindow)
        icon18 = QtGui.QIcon()
        icon18.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/ColorSync Utility.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSettings.setIcon(icon18)
        self.actionSettings.setObjectName(_fromUtf8("actionSettings"))
        self.actionRecord = QtGui.QAction(DuettoMainWindow)
        icon19 = QtGui.QIcon()
        icon19.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/record_26x26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRecord.setIcon(icon19)
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
        self.actionResampling = QtGui.QAction(DuettoMainWindow)
        self.actionResampling.setObjectName(_fromUtf8("actionResampling"))
        self.actionGenerate_White_Noise = QtGui.QAction(DuettoMainWindow)
        self.actionGenerate_White_Noise.setObjectName(_fromUtf8("actionGenerate_White_Noise"))
        self.actionSegmentation_And_Clasification = QtGui.QAction(DuettoMainWindow)
        icon20 = QtGui.QIcon()
        icon20.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/Process Viewer.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSegmentation_And_Clasification.setIcon(icon20)
        self.actionSegmentation_And_Clasification.setObjectName(_fromUtf8("actionSegmentation_And_Clasification"))
        self.actionGenerate_Pink_Noise = QtGui.QAction(DuettoMainWindow)
        self.actionGenerate_Pink_Noise.setObjectName(_fromUtf8("actionGenerate_Pink_Noise"))
        self.actionSave_theme = QtGui.QAction(DuettoMainWindow)
        self.actionSave_theme.setObjectName(_fromUtf8("actionSave_theme"))
        self.actionLoad_Theme = QtGui.QAction(DuettoMainWindow)
        self.actionLoad_Theme.setObjectName(_fromUtf8("actionLoad_Theme"))
        self.actionUndo = QtGui.QAction(DuettoMainWindow)
        icon21 = QtGui.QIcon()
        icon21.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/undo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionUndo.setIcon(icon21)
        self.actionUndo.setObjectName(_fromUtf8("actionUndo"))
        self.actionRedo = QtGui.QAction(DuettoMainWindow)
        icon22 = QtGui.QIcon()
        icon22.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/redo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRedo.setIcon(icon22)
        self.actionRedo.setObjectName(_fromUtf8("actionRedo"))
        self.actionZoom_Cursor = QtGui.QAction(DuettoMainWindow)
        self.actionZoom_Cursor.setCheckable(True)
        self.actionZoom_Cursor.setChecked(True)
        self.actionZoom_Cursor.setAutoRepeat(False)
        self.actionZoom_Cursor.setPriority(QtGui.QAction.HighPriority)
        self.actionZoom_Cursor.setObjectName(_fromUtf8("actionZoom_Cursor"))
        self.actionPointer_Cursor = QtGui.QAction(DuettoMainWindow)
        self.actionPointer_Cursor.setCheckable(True)
        self.actionPointer_Cursor.setAutoRepeat(False)
        self.actionPointer_Cursor.setPriority(QtGui.QAction.HighPriority)
        self.actionPointer_Cursor.setObjectName(_fromUtf8("actionPointer_Cursor"))
        self.actionFull_Screen = QtGui.QAction(DuettoMainWindow)
        self.actionFull_Screen.setCheckable(True)
        icon23 = QtGui.QIcon()
        icon23.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/Position.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFull_Screen.setIcon(icon23)
        self.actionFull_Screen.setObjectName(_fromUtf8("actionFull_Screen"))
        self.actionFile_Up = QtGui.QAction(DuettoMainWindow)
        icon24 = QtGui.QIcon()
        icon24.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/upfile.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFile_Up.setIcon(icon24)
        self.actionFile_Up.setObjectName(_fromUtf8("actionFile_Up"))
        self.actionFile_Down = QtGui.QAction(DuettoMainWindow)
        icon25 = QtGui.QIcon()
        icon25.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/downfile.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFile_Down.setIcon(icon25)
        self.actionFile_Down.setObjectName(_fromUtf8("actionFile_Down"))
        self.actionOsc_Image = QtGui.QAction(DuettoMainWindow)
        icon26 = QtGui.QIcon()
        icon26.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/Camera.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOsc_Image.setIcon(icon26)
        self.actionOsc_Image.setObjectName(_fromUtf8("actionOsc_Image"))
        self.actionSpecgram_Image = QtGui.QAction(DuettoMainWindow)
        self.actionSpecgram_Image.setIcon(icon26)
        self.actionSpecgram_Image.setObjectName(_fromUtf8("actionSpecgram_Image"))
        self.actionCombined_Image = QtGui.QAction(DuettoMainWindow)
        icon27 = QtGui.QIcon()
        icon27.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/Photofiltre.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCombined_Image.setIcon(icon27)
        self.actionCombined_Image.setObjectName(_fromUtf8("actionCombined_Image"))
        self.actionRectangular_Cursor = QtGui.QAction(DuettoMainWindow)
        self.actionRectangular_Cursor.setCheckable(True)
        self.actionRectangular_Cursor.setObjectName(_fromUtf8("actionRectangular_Cursor"))
        self.actionRectangular_Eraser = QtGui.QAction(DuettoMainWindow)
        self.actionRectangular_Eraser.setCheckable(True)
        self.actionRectangular_Eraser.setObjectName(_fromUtf8("actionRectangular_Eraser"))
        self.actionPositive_Values = QtGui.QAction(DuettoMainWindow)
        self.actionPositive_Values.setObjectName(_fromUtf8("actionPositive_Values"))
        self.actionNegative_Values = QtGui.QAction(DuettoMainWindow)
        self.actionNegative_Values.setObjectName(_fromUtf8("actionNegative_Values"))
        self.actionSignalName = QtGui.QAction(DuettoMainWindow)
        self.actionSignalName.setObjectName(_fromUtf8("actionSignalName"))
        self.action1_8x = QtGui.QAction(DuettoMainWindow)
        self.action1_8x.setCheckable(True)
        self.action1_8x.setObjectName(_fromUtf8("action1_8x"))
        self.action1_4x = QtGui.QAction(DuettoMainWindow)
        self.action1_4x.setCheckable(True)
        self.action1_4x.setObjectName(_fromUtf8("action1_4x"))
        self.action1_2x = QtGui.QAction(DuettoMainWindow)
        self.action1_2x.setCheckable(True)
        self.action1_2x.setObjectName(_fromUtf8("action1_2x"))
        self.action8x = QtGui.QAction(DuettoMainWindow)
        self.action8x.setCheckable(True)
        self.action8x.setObjectName(_fromUtf8("action8x"))
        self.action4x = QtGui.QAction(DuettoMainWindow)
        self.action4x.setCheckable(True)
        self.action4x.setObjectName(_fromUtf8("action4x"))
        self.action2x = QtGui.QAction(DuettoMainWindow)
        self.action2x.setCheckable(True)
        self.action2x.setObjectName(_fromUtf8("action2x"))
        self.action1x = QtGui.QAction(DuettoMainWindow)
        self.action1x.setCheckable(True)
        self.action1x.setChecked(True)
        self.action1x.setObjectName(_fromUtf8("action1x"))
        self.actionChange_Sign = QtGui.QAction(DuettoMainWindow)
        self.actionChange_Sign.setObjectName(_fromUtf8("actionChange_Sign"))
        self.actionChangePlayStatus = QtGui.QAction(DuettoMainWindow)
        self.actionChangePlayStatus.setObjectName(_fromUtf8("actionChangePlayStatus"))
        self.actionSave_selected_interval_as = QtGui.QAction(DuettoMainWindow)
        self.actionSave_selected_interval_as.setIcon(icon14)
        self.actionSave_selected_interval_as.setObjectName(_fromUtf8("actionSave_selected_interval_as"))
        self.actionClose = QtGui.QAction(DuettoMainWindow)
        self.actionClose.setObjectName(_fromUtf8("actionClose"))
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave_selected_interval_as)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionFile_Up)
        self.menuFile.addAction(self.actionFile_Down)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionLoad_Theme)
        self.menuFile.addAction(self.actionSave_theme)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menuFile.addAction(self.actionExit)
        self.menuExport.addAction(self.actionOsc_Image)
        self.menuExport.addAction(self.actionSpecgram_Image)
        self.menuExport.addAction(self.actionCombined_Image)
        self.menuTools.addAction(self.actionZoomIn)
        self.menuTools.addAction(self.actionZoom_out)
        self.menuTools.addAction(self.actionZoom_out_entire_file)
        self.menuTools.addAction(self.actionFull_Screen)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionZoom_Cursor)
        self.menuTools.addAction(self.actionPointer_Cursor)
        self.menuTools.addAction(self.actionRectangular_Cursor)
        self.menuTools.addAction(self.actionRectangular_Eraser)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.menuExport.menuAction())
        self.menuGenerate.addAction(self.actionGenerate_White_Noise)
        self.menuGenerate.addAction(self.actionGenerate_Pink_Noise)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionPositive_Values)
        self.menuEdit.addAction(self.actionNegative_Values)
        self.menuEdit.addAction(self.actionChange_Sign)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.action_Reverse)
        self.menuEdit.addAction(self.actionInsert_Silence)
        self.menuEdit.addAction(self.actionSilence)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionFilter)
        self.menuEdit.addAction(self.actionSmart_Scale)
        self.menuEdit.addAction(self.actionResampling)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.menuGenerate.menuAction())
        self.menuView.addAction(self.actionOscilogram)
        self.menuView.addAction(self.actionSpectogram)
        self.menuView.addAction(self.actionCombined)
        self.menuView.addAction(self.actionPower_Spectrum)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionSettings)
        self.menuView.addAction(self.actionSegmentation_And_Clasification)
        self.menuPlay_Speed.addAction(self.action1_8x)
        self.menuPlay_Speed.addAction(self.action1_4x)
        self.menuPlay_Speed.addAction(self.action1_2x)
        self.menuPlay_Speed.addAction(self.action1x)
        self.menuPlay_Speed.addAction(self.action2x)
        self.menuPlay_Speed.addAction(self.action4x)
        self.menuPlay_Speed.addAction(self.action8x)
        self.menuSound.addAction(self.actionPlay_Sound)
        self.menuSound.addAction(self.actionStop_Sound)
        self.menuSound.addAction(self.actionPause_Sound)
        self.menuSound.addAction(self.actionRecord)
        self.menuSound.addSeparator()
        self.menuSound.addAction(self.menuPlay_Speed.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuSound.menuAction())
        self.toolBar.addAction(self.actionNew)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionCopy)
        self.toolBar.addAction(self.actionCut)
        self.toolBar.addAction(self.actionPaste)
        self.toolBar.addAction(self.actionUndo)
        self.toolBar.addAction(self.actionRedo)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionRecord)
        self.toolBar.addAction(self.actionPause_Sound)
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
        self.toolBar.addAction(self.actionSettings)
        self.toolBar.addAction(self.actionSegmentation_And_Clasification)
        self.toolBar.addAction(self.actionFile_Up)
        self.toolBar.addAction(self.actionFile_Down)
        self.toolBar.addAction(self.actionSignalName)

        self.retranslateUi(DuettoMainWindow)
        QtCore.QMetaObject.connectSlotsByName(DuettoMainWindow)

    def retranslateUi(self, DuettoMainWindow):
        DuettoMainWindow.setWindowTitle(QtGui.QApplication.translate("DuettoMainWindow", "Duetto Sound Lab", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("DuettoMainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuTools.setTitle(QtGui.QApplication.translate("DuettoMainWindow", "Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.menuExport.setTitle(QtGui.QApplication.translate("DuettoMainWindow", "Export", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(QtGui.QApplication.translate("DuettoMainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuGenerate.setTitle(QtGui.QApplication.translate("DuettoMainWindow", "Generate", None, QtGui.QApplication.UnicodeUTF8))
        self.menuView.setTitle(QtGui.QApplication.translate("DuettoMainWindow", "Analysis", None, QtGui.QApplication.UnicodeUTF8))
        self.menuSound.setTitle(QtGui.QApplication.translate("DuettoMainWindow", "Sound", None, QtGui.QApplication.UnicodeUTF8))
        self.menuPlay_Speed.setTitle(QtGui.QApplication.translate("DuettoMainWindow", "Play Speed", None, QtGui.QApplication.UnicodeUTF8))
        self.dock_settings.setWindowTitle(QtGui.QApplication.translate("DuettoMainWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("DuettoMainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("DuettoMainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setShortcut(QtGui.QApplication.translate("DuettoMainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("DuettoMainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setShortcut(QtGui.QApplication.translate("DuettoMainWindow", "Esc", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoomIn.setText(QtGui.QApplication.translate("DuettoMainWindow", "Zoom in", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoomIn.setShortcut(QtGui.QApplication.translate("DuettoMainWindow", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoom_out.setText(QtGui.QApplication.translate("DuettoMainWindow", "Zoom out", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoom_out.setShortcut(QtGui.QApplication.translate("DuettoMainWindow", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSpectogram.setText(QtGui.QApplication.translate("DuettoMainWindow", "Spectogram", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOscilogram.setText(QtGui.QApplication.translate("DuettoMainWindow", "Oscillogram", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCombined.setText(QtGui.QApplication.translate("DuettoMainWindow", "Combined", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setText(QtGui.QApplication.translate("DuettoMainWindow", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setShortcut(QtGui.QApplication.translate("DuettoMainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPower_Spectrum.setText(QtGui.QApplication.translate("DuettoMainWindow", "Power Spectrum", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOscillogram_Settings.setText(QtGui.QApplication.translate("DuettoMainWindow", "Oscillogram Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSpectogram_Settings.setText(QtGui.QApplication.translate("DuettoMainWindow", "Spectrogram Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPower_Spectrum_Settings.setText(QtGui.QApplication.translate("DuettoMainWindow", "Power Spectrum Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPlay_Sound.setText(QtGui.QApplication.translate("DuettoMainWindow", "Play Sound", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPlay_Sound.setShortcut(QtGui.QApplication.translate("DuettoMainWindow", "Ctrl+P", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStop_Sound.setText(QtGui.QApplication.translate("DuettoMainWindow", "Stop Sound", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPause_Sound.setText(QtGui.QApplication.translate("DuettoMainWindow", "Pause Sound", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPause_Sound.setShortcut(QtGui.QApplication.translate("DuettoMainWindow", "P", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoom_out_entire_file.setText(QtGui.QApplication.translate("DuettoMainWindow", "Zoom out entire file", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("DuettoMainWindow", "Save as", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setShortcut(QtGui.QApplication.translate("DuettoMainWindow", "Ctrl+G", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setText(QtGui.QApplication.translate("DuettoMainWindow", "Copy", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setShortcut(QtGui.QApplication.translate("DuettoMainWindow", "Ctrl+C", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPaste.setText(QtGui.QApplication.translate("DuettoMainWindow", "Paste", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPaste.setShortcut(QtGui.QApplication.translate("DuettoMainWindow", "Ctrl+V", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setText(QtGui.QApplication.translate("DuettoMainWindow", "Cut", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setShortcut(QtGui.QApplication.translate("DuettoMainWindow", "Ctrl+X", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSettings.setText(QtGui.QApplication.translate("DuettoMainWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSettings.setShortcut(QtGui.QApplication.translate("DuettoMainWindow", "Ctrl+Space", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRecord.setText(QtGui.QApplication.translate("DuettoMainWindow", "Record", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Reverse.setText(QtGui.QApplication.translate("DuettoMainWindow", "Reverse", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Reverse.setShortcut(QtGui.QApplication.translate("DuettoMainWindow", "Ctrl+R", None, QtGui.QApplication.UnicodeUTF8))
        self.actionInsert_Silence.setText(QtGui.QApplication.translate("DuettoMainWindow", "Insert Silence", None, QtGui.QApplication.UnicodeUTF8))
        self.actionInsert_Silence.setShortcut(QtGui.QApplication.translate("DuettoMainWindow", "Ctrl+I", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSilence.setText(QtGui.QApplication.translate("DuettoMainWindow", "Silence", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSilence.setShortcut(QtGui.QApplication.translate("DuettoMainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFilter.setText(QtGui.QApplication.translate("DuettoMainWindow", "Filter", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFilter.setShortcut(QtGui.QApplication.translate("DuettoMainWindow", "Ctrl+F", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSmart_Scale.setText(QtGui.QApplication.translate("DuettoMainWindow", "Change Volume", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSmart_Scale.setShortcut(QtGui.QApplication.translate("DuettoMainWindow", "Ctrl+A", None, QtGui.QApplication.UnicodeUTF8))
        self.actionResampling.setText(QtGui.QApplication.translate("DuettoMainWindow", "Resampling", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGenerate_White_Noise.setText(QtGui.QApplication.translate("DuettoMainWindow", "White Noise", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSegmentation_And_Clasification.setText(QtGui.QApplication.translate("DuettoMainWindow", "Segmentation And Clasification", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGenerate_Pink_Noise.setText(QtGui.QApplication.translate("DuettoMainWindow", "Pink Noise", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_theme.setText(QtGui.QApplication.translate("DuettoMainWindow", "Save theme as", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_theme.setShortcut(QtGui.QApplication.translate("DuettoMainWindow", "Ctrl+Shift+T", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad_Theme.setText(QtGui.QApplication.translate("DuettoMainWindow", "Load theme", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad_Theme.setShortcut(QtGui.QApplication.translate("DuettoMainWindow", "Ctrl+T", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUndo.setText(QtGui.QApplication.translate("DuettoMainWindow", "Undo", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUndo.setShortcut(QtGui.QApplication.translate("DuettoMainWindow", "Ctrl+Z", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRedo.setText(QtGui.QApplication.translate("DuettoMainWindow", "Redo", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRedo.setShortcut(QtGui.QApplication.translate("DuettoMainWindow", "Ctrl+Y", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoom_Cursor.setText(QtGui.QApplication.translate("DuettoMainWindow", "Zoom Cursor", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoom_Cursor.setShortcut(QtGui.QApplication.translate("DuettoMainWindow", "Ctrl+Shift+Z", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPointer_Cursor.setText(QtGui.QApplication.translate("DuettoMainWindow", "Pointer Cursor", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPointer_Cursor.setShortcut(QtGui.QApplication.translate("DuettoMainWindow", "Ctrl+Shift+P", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFull_Screen.setText(QtGui.QApplication.translate("DuettoMainWindow", "Full Screen", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFull_Screen.setShortcut(QtGui.QApplication.translate("DuettoMainWindow", "Ctrl+S, Ctrl+F", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFile_Up.setText(QtGui.QApplication.translate("DuettoMainWindow", "File Up", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFile_Up.setShortcut(QtGui.QApplication.translate("DuettoMainWindow", "Ctrl+Up", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFile_Down.setText(QtGui.QApplication.translate("DuettoMainWindow", "File Down", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFile_Down.setShortcut(QtGui.QApplication.translate("DuettoMainWindow", "Ctrl+Down", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOsc_Image.setText(QtGui.QApplication.translate("DuettoMainWindow", "Osc Image", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSpecgram_Image.setText(QtGui.QApplication.translate("DuettoMainWindow", "Specgram Image", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCombined_Image.setText(QtGui.QApplication.translate("DuettoMainWindow", "Combined Image", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRectangular_Cursor.setText(QtGui.QApplication.translate("DuettoMainWindow", "Rectangular Cursor", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRectangular_Eraser.setText(QtGui.QApplication.translate("DuettoMainWindow", "Rectangular Eraser", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPositive_Values.setText(QtGui.QApplication.translate("DuettoMainWindow", "Positive Values", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNegative_Values.setText(QtGui.QApplication.translate("DuettoMainWindow", "Negative Values", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSignalName.setText(QtGui.QApplication.translate("DuettoMainWindow", "SignalName", None, QtGui.QApplication.UnicodeUTF8))
        self.action1_8x.setText(QtGui.QApplication.translate("DuettoMainWindow", "1/8x", None, QtGui.QApplication.UnicodeUTF8))
        self.action1_4x.setText(QtGui.QApplication.translate("DuettoMainWindow", "1/4x", None, QtGui.QApplication.UnicodeUTF8))
        self.action1_2x.setText(QtGui.QApplication.translate("DuettoMainWindow", "1/2x", None, QtGui.QApplication.UnicodeUTF8))
        self.action8x.setText(QtGui.QApplication.translate("DuettoMainWindow", "8x", None, QtGui.QApplication.UnicodeUTF8))
        self.action4x.setText(QtGui.QApplication.translate("DuettoMainWindow", "4x", None, QtGui.QApplication.UnicodeUTF8))
        self.action2x.setText(QtGui.QApplication.translate("DuettoMainWindow", "2x", None, QtGui.QApplication.UnicodeUTF8))
        self.action1x.setText(QtGui.QApplication.translate("DuettoMainWindow", "1x", None, QtGui.QApplication.UnicodeUTF8))
        self.actionChange_Sign.setText(QtGui.QApplication.translate("DuettoMainWindow", "Change Sign", None, QtGui.QApplication.UnicodeUTF8))
        self.actionChangePlayStatus.setText(QtGui.QApplication.translate("DuettoMainWindow", "changePlayStatus", None, QtGui.QApplication.UnicodeUTF8))
        self.actionChangePlayStatus.setShortcut(QtGui.QApplication.translate("DuettoMainWindow", "Space", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_selected_interval_as.setText(QtGui.QApplication.translate("DuettoMainWindow", "Save selected as", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setText(QtGui.QApplication.translate("DuettoMainWindow", "Close", None, QtGui.QApplication.UnicodeUTF8))

from ..Widgets.QSignalVisualizerWidget import QSignalVisualizerWidget
import icons_rc
