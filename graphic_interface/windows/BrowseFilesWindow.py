# -*- coding: utf-8 -*-
from PyQt4 import QtGui
import os
from PyQt4.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt4.QtGui import QAbstractItemView, QFileDialog
import time
from __builtin__ import file
from duetto.audio_signals.AudioSignalPlayer import AudioSignalPlayer
from duetto.audio_signals import openSignal
from graphic_interface.windows.ui_python_files.BrowseFilesWindow import Ui_BrowseFilesWindow


class BrowseFilesWindow(QtGui.QMainWindow, Ui_BrowseFilesWindow):
    """
    Window that provide an interface to create two dimensional
    graphs.
    """

    # SIGNALS
    # signal raised when a file is selected by user and must be opened
    # raise the list (list of str with the paths) of selected files to open
    openFiles = pyqtSignal(list)

    # CONSTANTS
    # tha amount of decimal places to round math operations
    DECIMAL_PLACES = 2

    def __init__(self, parent=None, folderFiles=[]):
        """
        Create the window to browse along the files of a folder
        :param parent: The parent window
        :param folderFiles: the list of files in the folder
        :return:
        """
        super(QtGui.QMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.show()

        # the list of files full path on the table
        self.folderFiles = []

        # the path of the base of the folder
        self.selected_folder = '' if len(folderFiles) == 0 else os.path.dirname(unicode(folderFiles[0]))
        self.folderPath_lineEdit.setText(self.selected_folder)

        # add the files to the table widget
        for file_path in folderFiles:
            self.addFile(file_path)

        self.files_tablewidget.resizeColumnsToContents()
        self.selectAll_bttn.setText(self.tr(u"Select All"))

    # region Files Handling

    def filesSelected(self):
        """
        Get the files that are selected
        :return: list of tupple (filename, index on table's rows)
        """
        files = []

        for x in range(self.files_tablewidget.rowCount()):
            # if the row is selected
            if self.files_tablewidget.item(x, 0).checkState() == Qt.Checked:
                files.append((self.folderFiles[x],x))

        return files

    def addFile(self, file_path, row=-1):
        """
        Add the file at file_path to the widget table
        on the specified row
        :param file_path: the file path of the new file to add
        :param row: the row in which would be added the file. If -1 is inserted at the end
        :return:
        """
        # region Create Items for Table
        # check if the file was already added
        if file_path in self.folderFiles:
            return

        # get the row to insert at the file
        if row == -1:
            row = self.files_tablewidget.rowCount()
            self.files_tablewidget.setRowCount(row + 1)

        # get the name of the file
        try:
            name = os.path.basename(unicode(file_path))
        except Exception as ex:
            name = "-"

        file_name = QtGui.QTableWidgetItem(name)
        # set file name item to checkable
        file_name.setCheckState(Qt.Unchecked)
        file_name.checkState()

        # calculate the size of the file
        try:
            size = os.path.getsize(file_path)
            sufix = ["Bytes", "Kb", "Mb", "Gb"]
            j = 0
            while size > 1024 and j < len(sufix):
                size /= 1024.0
                j += 1
            size = str(round(size, self.DECIMAL_PLACES))+sufix[j]

        except Exception as ex:
            size = "-"

        file_size = QtGui.QTableWidgetItem(size)

        # get the creation date
        try:
            date = time.gmtime(os.path.getctime(file_path))
            date = str(time.strftime("%d/%m/%Y",date))
        except Exception as ex:
            date = "-"

        creation_date = QtGui.QTableWidgetItem(date)

        # get the file duration
        duration = QtGui.QTableWidgetItem(str(0))

        # endregion

        # add the values into the table widget
        for col, value in enumerate([file_name, file_size, creation_date, duration]):
            self.files_tablewidget.setItem(row, col, value)

        # add the new file to the folder files list
        self.folderFiles.append(file_path)
        self.files_tablewidget.resizeRowsToContents()

    @pyqtSlot()
    def on_actionAddFileButton_triggered(self):
        """
        Open the dialog to select a new file to open
        :return:
        """
        new_file = QFileDialog.getOpenFileName(parent=self, directory=self.selected_folder,
                                               caption=self.tr(u"Open File"),
                                               filter=self.tr(u"Wav Files") + u" (*.wav);(*.WAV);All Files (*)")

        # update the line edit with the name of the new file
        self.folderPath_lineEdit.setText(new_file)

        # add the new file into the table widget
        self.addFile(new_file)

    # endregion

    # region Files Selection

    @pyqtSlot()
    def on_actionInvertSelection_triggered(self):
        """
        Change the check state of every file in the table widget to
        it opposite. (Checked -> Unchecked and Unchecked -> Checked)
        :return:
        """
        for x in range(self.files_tablewidget.rowCount()):

            check_state = self.files_tablewidget.item(x, 0).checkState()

            if check_state == Qt.Checked:
                check_state = Qt.Unchecked

            elif check_state == Qt.Unchecked:
                check_state = Qt.Checked

            self.files_tablewidget.item(x, 0).setCheckState(check_state)

    @pyqtSlot()
    def on_actionSelectAll_triggered(self):
        """
        Switch between the select and deselect all actions.
        If select-all button text is 'Select All' then selects all the files
        of the table and if the text of the button is 'Deselect All' deselect all the files.
        Turn the label of the button to the opposite value to execute the opposite action the next time.
        :return:
        """

        check_state = Qt.Checked if self.selectAll_bttn.text() == self.tr(u"Select All") else Qt.Unchecked
        self.selectAll_bttn.setText(self.tr(u"Deselect All") if self.selectAll_bttn.text() == self.tr(u"Select All")
                                    else self.tr(u"Select All"))

        for x in range(self.files_tablewidget.rowCount()):
            self.files_tablewidget.item(x, 0).setCheckState(check_state)

    # endregion

    # region Files Up Down

    @pyqtSlot()
    def on_actionFileUp_triggered(self):
        """
        Open the next file to the current selection file on the tab widget.
        If there is more that one file selected open the next to the last file.
        If the last file is selected nothing is do it
        :return:
        """
        self.openNextUnselectedFile(up=True)

    @pyqtSlot()
    def on_actionFileDown_triggered(self):
        """
        Open the previous file to the current selection file on the tab widget.
        If there is more that one file selected open the previous to the first file.
        If the first file is selected nothing is do it
        :return:
        """
        self.openNextUnselectedFile(up=False)

    def openNextUnselectedFile(self, up=True):
        """
        Implements the logic of open unselected files of the files list.
        Open and select the next unselected file found.
        :param up: True if the next file if searched from the last selected index to the end of
        the list and False if the next file if searched from the first selected index
         to the start of the list
        :return:
        """
        if len(self.folderFiles) == 0:
            return

        files_selected_indexes = [x[1] for x in self.filesSelected()]

        # start at the index of the
        # next file to the last selected (the next unselected index) if 'up'
        # or the index before the first selected (the previous unselected index) if not 'up'
        start_index = files_selected_indexes[-1] + 1 if up else files_selected_indexes[0] - 1
        end_index = len(self.folderFiles) if up else -1
        step = 1 if up else -1

        for i in range(start_index, end_index, step):

            if self.files_tablewidget.item(i, 0).checkState() == Qt.Unchecked:
                # get the first unselected, change it state and open it
                self.files_tablewidget.item(i, 0).setCheckState(Qt.Checked)
                self.openFiles.emit([self.folderFiles[i]])
                return

    # endregion

    @pyqtSlot()
    def on_actionOpen_triggered(self):
        """
        Open the current selection files on the tab widget.
        If there is more that one file selected all are open.
        :return:
        """
        files_selected = [x[0] for x in self.filesSelected()]
        self.openFiles.emit(files_selected)

        if len(files_selected) > 0:
            self.close()

    @pyqtSlot()
    def on_actionPlay_triggered(self):
        """
        Play the currently selected file in the tab widget.
        If there are more that one file plays all in order of selection
        if no selection nothing is do it.
        :return:
        """
        files_selected = [x[0] for x in self.filesSelected()]
        # play the first file
        try:
            # self.player = AudioSignalPlayer(openSignal(files[0]))
            # self.player.play()
            pass
        except Exception as ex:
            pass
        print("Play")
