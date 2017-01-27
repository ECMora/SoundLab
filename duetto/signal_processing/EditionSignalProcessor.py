# coding=utf-8
from PyQt4 import QtCore
import cPickle

from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QApplication

from duetto.audio_signals import AudioSignal
from duetto.signal_processing.SignalProcessor import SignalProcessor


class EditionSignalProcessor(SignalProcessor):
    """
    Class that execute the operation of edition in an AudioSignal.
    Allows cut, copy and paste a section of the signal.
    The edition actions are implemented by using the QClipboard of the QtFramework
    so a QApplication object must be created first.
    """

    # SIGNALS
    # signal raised when a cut or paste action are performed and
    # the signal size is changed.
    signal_size_changed = pyqtSignal()

    def __init__(self, signal=None):
        SignalProcessor.__init__(self, signal)

    def cut(self, start_index, end_index):
        """
        Cut a section of the signal
        :param start_index: The start index of data signal array for cut
        :param end_index: The end index of data signal array for cut
        :return:
        :raise IndexError:
        """
        if self.checkIndexesOk(start_index,end_index):
            try:
                self.__put_into_clipboard(start_index, end_index)
                self.signal.remove(start_index, end_index)

                self.signal_size_changed.emit()
            except Exception as e:
                raise Exception(e.message)
        else:
            raise IndexError()

    def __put_into_clipboard(self,indexFrom,indexTo):
        """
        Put the information of a section of the current signal
        into the application clipboard.
        :param indexFrom: start index of the section
        :param indexTo: end index of the section
        """
        try:
            # get an slice of the signal by copy a section
            signal_piece = self.signal.copy(indexFrom, indexTo)

            # serialize as byte array the signal
            pickle_data = cPickle.dumps(signal_piece)

            # set the serialized signal into clipboard
            mime_data = QtCore.QMimeData()
            mime_data.setData("signal", QtCore.QByteArray(pickle_data))
            clip = QApplication.clipboard()
            clip.setMimeData(mime_data)

        except Exception as e:
            raise Exception(e.message)

    def __get_from_clipboard(self):
        """
        Obtains the data previously stored in the application clipboard.
        :return None if error, the stored in the clipboard signal otherwise
        """
        try:
            #get the data stored in the clipboard
            clip = QApplication.clipboard()
            signal_data = clip.mimeData().data("signal")

            #deserialize the signal
            signal = cPickle.loads(signal_data.data())

            if not isinstance(signal, AudioSignal):
                raise Exception

            return signal
        except Exception as e:
            raise Exception(e.message)

    def copy(self, start_index, end_index):
        """
        Copy a section of the signal for future paste.
        :param start_index: The start index of data signal array for copy
        :param end_index: The end index of data signal array for copy
        :return: :raise IndexError:
        """
        if self.checkIndexesOk(start_index,end_index):
            self.__put_into_clipboard(start_index, end_index)
        else:
            raise IndexError()

    def paste(self, start_index):
        """
        Paste the values on data into the signal at index start_index
        :param start_index:
        :raise IndexError:
        """
        if self.checkIndexesOk(start_index,start_index):
            # get the signal stored in the clipboard if any
            clipboard_signal = self.__get_from_clipboard()
            # compare the two signals metadata (== overload) to decide if coan be concatenated
            if clipboard_signal is not None and self.signal == clipboard_signal:
                self.signal.insert(clipboard_signal, start_index)
                self.signal_size_changed.emit()
        else:
            raise IndexError()

