from MainWindow import Ui_DuettoMainWindow
from MyPowerSpecWindow import PowerSpectrumWindow
from PyQt4 import QtCore
from PyQt4 import QtGui
from Duetto_Core.AudioSignals import WavFileSignal


class BatSoundWindow(QtGui.QMainWindow, Ui_DuettoMainWindow):
    def __init__(self, parent=None):
        super(BatSoundWindow, self).__init__(parent)
        self.setupUi(self)

        self.dock_spec_settings.setVisible(False)
        self.dock_osc_settings.setVisible(False)
        self.dock_powspec_settings.setVisible(False)
        self.NFFT_pow = int(self.cbx_fftsize_pow.currentText())
        self.window_pow = self.cbx_fftwindow_pow.currentText()
        self.NFFT_spec = int(self.cbx_fftsize.currentText())
        self.window_spec = self.cbx_fftwindow.currentText()
        self.overlap_spec = self.sbx_fftoverlap.value()
        self.pow_spec_windows = []

    @QtCore.pyqtSlot()
    def on_actionZoomIn_triggered(self):
        self.widget.zoomIn()

    @QtCore.pyqtSlot()
    def on_actionZoom_out_triggered(self):
        self.widget.zoomOut()

    @QtCore.pyqtSlot()
    def on_actionZoom_out_entire_file_triggered(self):
        self.widget.zoomNone()

    @QtCore.pyqtSlot()
    def on_actionClear_Spectogram_triggered(self):
        #self.widget.update_spectrogram(self.NFFT_spec, self.overlap_spec)
        pass

    @QtCore.pyqtSlot()
    def on_actionAll_Settings_triggered(self):
        self.dock_osc_settings.setVisible(True)
        self.dock_osc_settings.setFloating(False)

        self.dock_spec_settings.setVisible(True)
        self.dock_spec_settings.setFloating(False)

        self.dock_powspec_settings.setVisible(True)
        self.dock_powspec_settings.setFloating(False)

    @QtCore.pyqtSlot()
    def on_actionHighest_instant_frequency_triggered(self):
        #print self.widget.zmax, self.widget.zmin,self.widget.minIntervalLength
        #
        #if self.widget.first:
        #    self.widget.calc_highest_freq()
        #    self.widget.first = False
        #if self.widget.zmax - self.widget.zmin < self.widget.minIntervalLength:
        #    m = QtGui.QMessageBox(self)
        #    m.setText("The least that you can select interval length is " + str(self.widget.minIntervalLength))
        #    m.show()
        #else : self.widget.plot_highest_freq(self.widget.zmin, self.widget.zmax)
        pass

    @QtCore.pyqtSlot()
    def on_actionPower_Spectrum_triggered(self):
        dg_pow_spec = PowerSpectrumWindow(self)
        minx = self.widget.zmin * self.widget.rate
        maxx = max(self.widget.zmax * self.widget.rate, min(minx + self.NFFT_pow, len(self.widget.data)))
        dg_pow_spec.plot(self.widget.data[minx:maxx], self.widget.rate, self.NFFT_pow, self.window_pow)
        self.pow_spec_windows.append(dg_pow_spec)

    @QtCore.pyqtSlot()
    def on_actionPower_Spectrum_Settings_triggered(self):
        self.dock_powspec_settings.setVisible(True)
        self.dock_powspec_settings.setFloating(False)

    @QtCore.pyqtSlot()
    def on_actionSelect_all_triggered(self):
        self.widget.updateSpanSelector()

    @QtCore.pyqtSlot()
    def on_btnosc_apply_clicked(self):
        pass

    @QtCore.pyqtSlot()
    def on_btnpow_apply_clicked(self):
        self.NFFT_pow = int(self.cbx_fftsize_pow.currentText())
        self.window_pow = self.cbx_fftwindow_pow.currentText()

    @QtCore.pyqtSlot()
    def on_btnspec_apply_clicked(self):
        self.NFFT_spec = int(self.cbx_fftsize.currentText())
        self.window_spec = self.cbx_fftwindow.currentText()
        self.overlap_spec = self.sbx_fftoverlap.value()

        self.widget.specgramSettings.NFFT = self.NFFT_spec
        self.widget.specgramSettings.overlap = self.overlap_spec
        self.widget.visualChanges = True
        self.widget.refresh()
        # falta actualizar la ventana

    @QtCore.pyqtSlot()
    def on_actionSpectogram_Settings_triggered(self):
        self.dock_spec_settings.setVisible(True)
        self.dock_spec_settings.setFloating(False)

    @QtCore.pyqtSlot()
    def on_actionOscillogram_Settings_triggered(self):
        self.dock_osc_settings.setVisible(True)
        self.dock_osc_settings.setFloating(False)

    @QtCore.pyqtSlot()
    def on_actionOpen_triggered(self):
        self.actionHighest_instant_frequency.setChecked(False)
        f = QtGui.QFileDialog.getOpenFileName(self, "Select a file to open",
                                              filter="Wave Files (*.wav);;All Files (*)")
        if f != '':
            self.widget._setVisibleOscilogram(True)
            self.widget._setVisibleSpectrogram(True)
            self.widget.open(f)
            self.widget.specgramSettings.NFFT = self.NFFT_spec
            self.widget.specgramSettings.overlap = self.overlap_spec
            self.widget.visualChanges = True
            self.widget.refresh()
            self.first = True


    @QtCore.pyqtSlot()
    def on_actionPlay_Sound_triggered(self):
        self.widget.play()

    @QtCore.pyqtSlot()
    def on_actionStop_Sound_triggered(self):
        self.widget.stop()

    @QtCore.pyqtSlot()
    def on_actionRecord_triggered(self):
        self.widget.record()

    @QtCore.pyqtSlot()
    def on_actionCombined_triggered(self):
        self.widget._setVisibleOscilogram(True)
        self.widget._setVisibleSpectrogram(True)
        self.widget.refresh()

    @QtCore.pyqtSlot()
    def on_actionSpectogram_triggered(self):
        self.widget._setVisibleOscilogram(False)
        self.widget._setVisibleSpectrogram(True)
        self.widget.refresh()

    @QtCore.pyqtSlot()
    def on_actionOscilogram_triggered(self):
        self.widget._setVisibleOscilogram(True)
        self.widget._setVisibleSpectrogram(False)
        self.widget.refresh()

    @QtCore.pyqtSlot(int, int, int)
    def on_widget_rangeChanged(self, left, right, total):
        self.horizontalScrollBar.blockSignals(True)
        self.horizontalScrollBar.setValue(0)
        self.horizontalScrollBar.setMinimum(0)
        self.horizontalScrollBar.setMaximum(total - (right - left))
        self.horizontalScrollBar.setValue(left)
        self.horizontalScrollBar.setPageStep(right - left)
        self.horizontalScrollBar.setSingleStep((right - left) / 16)
        self.horizontalScrollBar.blockSignals(True)
        self.horizontalScrollBar.blockSignals(False)

    @QtCore.pyqtSlot(int)
    def on_horizontalScrollBar_valueChanged(self, value):
        self.widget.changeRange(value, value + self.horizontalScrollBar.pageStep(), emit=False)

if __name__ == '__main__':
    import sys

    # create the GUI application
    app = QtGui.QApplication(sys.argv)
    # instantiate the main window
    dmw = BatSoundWindow()
    # show it
    dmw.show()
    # start the Qt main loop execution, exiting from this script
    # with the same return code of Qt application
    sys.exit(app.exec_())
