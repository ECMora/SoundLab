#  -*- coding: utf-8 -*-
from utils.Utils import *
from duetto.audio_signals import openSignal
from duetto.audio_signals.audio_signals_stream_readers.FileManager import FileManager
from ui_python_files.BatchWindow import Ui_MainWindow


class BatchWindow(QtGui.QMainWindow, Ui_MainWindow):
    """
    Main window of the application.
    """

    def __init__(self, parent=None):
        """
        """
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

    def batch(self):
        """
        Method that performs the batch procesing
        :return:
        """

        # get the input audio files folder
        # and the output meditions folder
        directoryinput = str(self.lineeditFilePath.text())
        directoryoutput = str(self.lineEditOutputFolder.text())

        # validate the folders
        if not os.path.isdir(directoryinput):
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"),
                                      self.tr(u"The input path is not a directory."))
            return
        if not os.path.isdir(directoryoutput):
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"),
                                      self.tr(u"The output path is not a directory."))
            return

        sounds = folder_files(directoryinput)  # the audio files to process

        # updating the progress bar
        self.progressBarProcesed.setValue(0)

        # the number of files processed for use in the progress bar update
        files_processed = 0

        if self.rbttnSplitFile.isChecked():
            for filename in sounds:
                try:
                    signal = openSignal(filename)
                    self.listwidgetProgress.addItem(self.tr(u"Processing") + u" " + signal.name)

                    sr = signal.samplingRate
                    pieceSize = self.spboxSplitTime.value() * sr
                    pieces = len(signal.data) / pieceSize
                    left = len(signal.data) % pieceSize
                    if pieces >= 1:
                        for i in range(pieces):
                            save = signal.copy(i * pieceSize, (i + 1) * pieceSize)
                            FileManager().write(save, os.path.join(directoryoutput, str(i + 1) + "-" + signal.name))
                    if left > 0:
                        save = signal.copy(signal.length - left, signal.length)
                        FileManager().write(save, os.path.join(directoryoutput, str(pieces + 1) + "-" + signal.name))

                    files_processed += 1

                    self.progressBarProcesed.setValue(100.0 * files_processed / len(sounds))
                    self.listwidgetProgress.addItem(signal.name + u" " + self.tr(u"has been files_processed"))
                    self.progressBarProcesed.repaint()
                    self.listwidgetProgress.repaint()

                except Exception as ex:
                    print("some split problems: " + ex.message)

        self.progressBarProcesed.setValue(100)

    def selectInputFolder(self):
        """
        Select a valid folder in the file system..
        :return:
        """
        inputfolder = QFileDialog.getExistingDirectory()

        # update the line edit with the name of
        self.lineeditFilePath.setText(inputfolder)

    def selectOutputFolder(self):
        """
        Select a valid folder in the file system to save the batch result data.
        :return:
        """
        output_folder = QFileDialog.getExistingDirectory()
        self.lineEditOutputFolder.setText(output_folder)