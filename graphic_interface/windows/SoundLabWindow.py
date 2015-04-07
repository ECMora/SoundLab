# -*- coding: utf-8 -*-
from PyQt4.QtCore import pyqtSlot
import PyQt4.QtCore as QtCore
from PyQt4.QtGui import QActionGroup, QFileDialog, QSlider
from PyQt4 import QtGui
from utils.Utils import save_image, DECIMAL_PLACES
from graphic_interface.Settings.Workspace import Workspace
from graphic_interface.widgets.signal_visualizer_tools.SignalVisualizerTool import Tools


class SoundLabWindow(QtGui.QMainWindow):
    """
    Window that encapsulates the commonly operations with a
    sound lab window that contains a widget (QSignalVisualizer or descendant).
    provides usefull operations that delegates into the widget its implementation
    """

    # region Initialize

    def __init__(self, parent):
        """
        """
        QtGui.QMainWindow.__init__(self, parent)

        self.workSpace = Workspace()

        #  get the status bar to show messages to the user
        self.statusbar = self.statusBar()
        self.statusbar.setSizeGripEnabled(False)

        # action groups of common actions for sound lab window
        self.play_record_actions = QActionGroup(self)
        self.widgets_visibility_actions = QActionGroup(self)
        self.zoom_actions = QActionGroup(self)
        self.tools_actions = QActionGroup(self)
        self.save_images_actions = QActionGroup(self)

        # play volume bar
        self.volume_bar = QSlider(QtCore.Qt.Horizontal, self)
        self.volume_bar.setToolTip(self.tr(u"Volume bar for Play."))
        self.volume_bar.setMaximumWidth(100)
        self.volume_bar.setRange(0, 300)
        self.volume_bar.setValue(100)
        self.volume_bar.valueChanged.connect(self.change_volume)

        # text edit for the signal name on the toolbar
        self.signalNameLineEdit = QtGui.QLineEdit(self)
        self.signalNameLineEdit.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum))
        self.signalPropertiesTextLabel = QtGui.QLabel(self)
        self.signalPropertiesTextLabel.setAlignment(QtCore.Qt.AlignRight)
        self.signalPropertiesTextLabel.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum))

    # endregion

    def configureToolBarActionsGroups(self):
        """
        Configure the actions into groups for best visualization and
        user configuration.
        :return:
        """
        sep1, sep2, sep3, sep4 = [QtGui.QAction(self) for _ in range(4)]

        for sep in [sep1, sep2, sep3, sep4]:
            sep.setSeparator(True)

        # region play record actions
        play_record_actions_list = [self.actionPlay_Sound, self.actionPause_Sound, self.actionStop_Sound,
                                    self.actionRecord, self.actionPlayLoop, sep2]
        for act in play_record_actions_list:
            act.setActionGroup(self.play_record_actions)

        self.toolBar.addWidget(self.volume_bar)

        # endregion


        # region widgets visibility actions
        widgets_visibility_actions_list = [self.actionOscilogram, self.actionSpectogram, self.actionCombined,
                                           sep3]

        for act in widgets_visibility_actions_list:
            act.setActionGroup(self.widgets_visibility_actions)
        # endregion

        # region zoom actions
        zoom_actions_list = [self.actionZoomIn, self.actionZoom_out,
                             self.actionZoom_out_entire_file, sep4]

        for act in zoom_actions_list:
            act.setActionGroup(self.zoom_actions)

        # endregion

        # region Save Images actions
        save_images_actions_list = [self.actionOsc_Image, self.actionSpecgram_Image,
                                    self.actionCombined_Image]

        for act in save_images_actions_list:
            act.setActionGroup(self.save_images_actions)
        # endregion

        # region Tools actions
        tools_actions_list = [self.actionZoom_Cursor, self.actionPointer_Cursor,
                              self.actionRectangular_Cursor]

        for act in tools_actions_list:
            act.setActionGroup(self.tools_actions)
        # endregion

        actions_groups = [(self.play_record_actions, self.tr(u"Play/Record")),
                          (self.zoom_actions, self.tr(u"Zoom")),
                          (self.widgets_visibility_actions, self.tr(u"Widgets Visibility"))]

        # add to the customizable sound lab toolbar
        for act in actions_groups:
            # addActionGroup(actionGroup, name)
            self.toolBar.addActionGroup(act[0], act[1])

        # add the label for signal name (and edit line) that always wil be visible as an option
        # not like the other groups of actions that the user could customize visibility
        self.toolBar.addWidget(self.signalNameLineEdit)
        self.toolBar.addAction(sep1)
        self.toolBar.addWidget(self.signalPropertiesTextLabel)

    #  region Widget Tools
    @pyqtSlot()
    def on_actionZoom_Cursor_triggered(self):
        """
        Select the Zoom Tool as current working tool in the widget
        :return:
        """
        self.select_tool(self.actionZoom_Cursor, Tools.ZoomTool)

    @pyqtSlot()
    def on_actionRectangular_Cursor_triggered(self):
        """
        Select the Rectangular Cursor as current working tool in the widget
        :return:
        """
        self.select_tool(self.actionRectangular_Cursor, Tools.RectangularZoomTool)

    @pyqtSlot()
    def on_actionRectangular_Eraser_triggered(self):
        """
        Select the Rectangular Eraser as current working tool in the widget
        :return:
        """
        self.select_tool(self.actionRectangular_Eraser, Tools.RectangularEraser)

    @pyqtSlot()
    def on_actionPointer_Cursor_triggered(self):
        """
        Select the Pointer Cursor as current working tool in the widget
        :return:
        """
        self.select_tool(self.actionPointer_Cursor, Tools.PointerTool)

    def deselectToolsActions(self):
        """
        Change the checked status of all the actions tools to False
        """
        self.actionZoom_Cursor.setChecked(False)
        self.actionRectangular_Cursor.setChecked(False)
        self.actionPointer_Cursor.setChecked(False)

    def select_tool(self, tool_action, tool_type):
        """

        :param tool_action: the checkable action that handles the selection of the tool
        :param tool_type: the enum type of the tool to select in the widget
        :return:
        """
        self.deselectToolsActions()
        tool_action.setChecked(True)
        self.widget.setSelectedTool(tool_type)

    #  endregion

    #  region Save widgets Image

    @pyqtSlot()
    def on_actionOsc_Image_triggered(self):
        """
        Save to disc the image of the oscilogram graph.
        :return:
        """
        if self.widget.visibleOscilogram:
            fname = unicode(QFileDialog.getSaveFileName(self, self.tr(u"Save oscilogram graph as an Image"),
                                                u"oscilogram-Duetto-Image", u"*.jpg"))
            save_image(self.widget.axesOscilogram, fname)

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
            fname = unicode(QFileDialog.getSaveFileName(self, self.tr(u"Save specgram graph as an Image"),
                                                u"specgram-Duetto-Image", u"*.jpg"))
            save_image(self.widget.axesSpecgram, fname)
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
            fname = unicode(QFileDialog.getSaveFileName(self, self.tr(u"Save graph as an Image"),
                                                u"Duetto-Image", u"*.jpg"))
            save_image(self.widget, fname)
        else:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"),
                                      self.tr(u"One of the plot widgets is not visible.") + " \n" + self.tr(
                                          u"You should see the data that you are going to save."))

    #  endregion

    # region Zoom
    # delegate in the widget the zoom interaction with the signal
    @QtCore.pyqtSlot()
    def on_actionZoomIn_triggered(self):
        self.widget.zoomIn()

    @QtCore.pyqtSlot()
    def on_actionZoom_out_triggered(self):
        self.widget.zoomOut()

    @QtCore.pyqtSlot()
    def on_actionZoom_out_entire_file_triggered(self):
        self.widget.zoomNone()

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

        # udpate the workspace
        self.workSpace.visibleOscilogram = visibleOscilogram
        self.workSpace.visibleSpectrogram = visibleSpectrogram

        self.widget.graph()

    # endregion

    #  region Play, Pause, Stop, Record
    # delegate in the widget reproduction actions
    def change_volume(self, volume):
        # change volume in the player of the widget
        if self.widget:
            self.widget.change_volume(volume)
        self.updateStatusBar(self.tr(u"The volume has been changed to "+unicode(volume) + u"%."), 1000)

    @pyqtSlot()
    def on_actionPlay_Sound_triggered(self):
        try:
            self.widget.play()

        except Exception as ex:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"),
                                      self.tr(u"There is no selected audio input "
                                              u"device or the selected is unavailable"))

    @pyqtSlot()
    def on_actionPlayLoop_triggered(self):
        self.widget.setPlayLoopEnabled(self.actionPlayLoop.isChecked())

    @pyqtSlot()
    def on_actionStop_Sound_triggered(self):
        self.widget.stop()

    @pyqtSlot()
    def on_actionPause_Sound_triggered(self):
        self.widget.pause()

    def switchPlayStatus(self):
        """
        Change the play status of the signal from play-pause and vice versa
        :return:
        """
        self.widget.switchPlayStatus()

    # endregion

    # region Edition and Processing Methods

    # region Undo Redo

    @pyqtSlot()
    def on_actionUndo_triggered(self):
        self.widget.undo()

    @pyqtSlot()
    def on_actionRedo_triggered(self):
        self.widget.redo()

    # endregion

    #  region Cut, Copy, Paste
    @pyqtSlot()
    def on_actionCut_triggered(self):
        self.widget.cut()
        self.updateSignalPropertiesLabel(self.widget.signal)

    @pyqtSlot()
    def on_actionCopy_triggered(self):
        self.widget.copy()


    @pyqtSlot()
    def on_actionPaste_triggered(self):
        self.widget.paste()
        self.updateSignalPropertiesLabel(self.widget.signal)

    #  endregion

    # endregion

    def updateStatusBar(self, line, time=None):
        """
        Set a new message in the status bar of the window.
        :param line: string with the line to show in the status bar
        """
        if time is None:
            self.statusbar.showMessage(line)
        else:
            self.statusbar.showMessage(line, time)

    def updateSignalPropertiesLabel(self, signal):
        """
        Updates the text of the current signal properties in toolbar.
        :return:
        """
        # action signal is a place in the tool bar to show the current signal name
        self.signalNameLineEdit.setText(signal.name)

        sr = signal.samplingRate
        bit_depth = signal.bitDepth
        channels = signal.channelCount

        properties = u"    " + \
                     u" <b>" + self.tr(u"Sampling Rate: ") + u"</b>" + unicode(sr) + u"  " + \
                     u" <b>" + self.tr(u"Bit Depth: ") + u"</b>" + unicode(bit_depth) + u"  " + \
                     u" <b>" + self.tr(u"Channels: ") + u"</b>" + unicode(channels) + u"  " + \
                     u" <b>" + self.tr(u"Duration(s): ") + u"</b>" + unicode(round(signal.duration, DECIMAL_PLACES)) + \
                     u"    "

        self.signalPropertiesTextLabel.setText(properties)