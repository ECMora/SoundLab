from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtGui import QDialog, QMessageBox, QTableWidgetItem, QColor
from duetto.audio_signals import AudioSignal
from duetto.audio_signals.audio_signals_stream_readers.FileManager import FileManager
import numpy as np
from graphic_interface.windows.ui_python_files.cross_correlationDialog import Ui_cross_correlationDialog


class Cross_correlationDialog(QDialog, Ui_cross_correlationDialog):

    elementSelected = pyqtSignal(int)

    def __init__(self, parent, signalDetectorWidget, signal, tableColorOdd=None, tableColorEven=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self._tableColorOdd = tableColorOdd if tableColorOdd is not None else QColor(0, 0, 255, 150)
        self._tableColorEven = tableColorEven if tableColorEven is not None else QColor(0, 255, 0, 150)

        self._signalDetectorWidget = signalDetectorWidget


        if signal and isinstance(signal, AudioSignal):
            self._refSignal = signal
        elif signal:
            self._refSignal = FileManager().read(unicode(signal))
        else:
            raise ValueError('signal must be a non empty string')

        self.oscillogramWidget.signal = self._refSignal
        self.oscillogramWidget.graph()
        self.spectrogramWidget.signal = self._refSignal
        self.spectrogramWidget.graph()

        self.matches = []
        self.find_match()

        self.fill_table()

    def selectElement(self, index):
        if index < self.matchTableWidget.rowCount():
            ordered_matches = self.matches
            if self.orderCheckBox.isChecked():
                ordered_matches = sorted(self.matches, key=lambda t: t[1], reverse=True)

            # find the one whose index is 'index'
            pos = 0
            for i, match, offset in ordered_matches:
                if i == index:
                    break
                pos += 1

            self.matchTableWidget.selectRow(pos)

    @pyqtSlot(int, int, int, int)
    def on_matchTableWidget_currentCellChanged(self, currentRow, currentColumn, previousRow, previousColumn):
        header_item = self.matchTableWidget.verticalHeaderItem(currentRow)
        if header_item is not None:
            current_element = int(header_item.text()) - 1
            self.elementSelected.emit(current_element)

    @pyqtSlot(int)
    def on_orderCheckBox_stateChanged(self, state):
        self.fill_table()

    def find_match(self):
        self.matches = []

        signal = self._signalDetectorWidget.signal

        if signal.samplingRate != self._refSignal.samplingRate:
            answer = QMessageBox.warning(self, self.tr(u"Different sampling rate."),
                                         self.tr(u"The signal and the reference segment have different sampling rates. "
                                                 u"The results you will get might not be what you are looking for. "
                                                 u"Consider resampling one of the sounds.\n"
                                                 u"Do you want to proceed anyway?"),
                                         QMessageBox.Yes | QMessageBox.No)
            if answer != QMessageBox.Yes:
                return

        ref_segment = np.array(self._refSignal.data, dtype=float)
        ref_segment_norm = np.linalg.norm(ref_segment)
        for i, element in enumerate(self._signalDetectorWidget._elements):
            segment = np.array(signal.data[element.indexFrom: element.indexTo], dtype=float)

            corr = np.correlate(segment, ref_segment, mode='same')
            corr /= 1.0 * np.linalg.norm(segment) * ref_segment_norm

            offset = np.argmax(corr)
            match = corr[offset]

            # in the corr array, the first len(self._refSignal.data)-1 values are negative offset, then 0 offset and
            # then len(segment)-1 values of positive offset
            offset -= len(ref_segment) + 1
            # transform to milliseconds
            offset = 1000.0 * offset / signal.samplingRate

            self.matches.append((i, match, offset))

    def fill_table(self):
        self.matchTableWidget.setRowCount(0)

        ordered_matches = self.matches
        if self.orderCheckBox.isChecked():
            ordered_matches = sorted(self.matches, key=lambda t: t[1], reverse=True)

        for i, match, offset in ordered_matches:
            row_count = self.matchTableWidget.rowCount()
            self.matchTableWidget.insertRow(row_count)
            item = QTableWidgetItem(str(i+1))
            self.matchTableWidget.setVerticalHeaderItem(row_count, item)

            item = QTableWidgetItem('{:.2%}'.format(match))
            item.setBackground(self._tableColorEven if i % 2 == 0 else self._tableColorOdd)
            self.matchTableWidget.setItem(row_count, 0, item)

            item = QTableWidgetItem(str('{:.0f} ms'.format(offset)))
            item.setBackground(self._tableColorEven if i % 2 == 0 else self._tableColorOdd)
            self.matchTableWidget.setItem(row_count, 1, item)

        self.matchTableWidget.resizeColumnsToContents()
        self.matchTableWidget.resizeRowsToContents()
