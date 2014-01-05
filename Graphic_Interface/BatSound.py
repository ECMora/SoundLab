from PyQt4.QtGui import QDialog, QMessageBox
from Duetto_Core.SignalProcessors.FilterSignalProcessor import FILTER_TYPE
from MainWindow import Ui_DuettoMainWindow
from MyPowerSpecWindow import PowerSpectrumWindow
from Graphic_Interface.Dialogs import InsertSilenceDialog as sdialog, FilterOptionsDialog as filterdg,ChangeVolumeDialog as cvdialog
from PyQt4 import QtCore
from PyQt4 import QtGui

import sys
from PyQt4.QtCore import SIGNAL
from Duetto_Core.AudioSignals import WavFileSignal


MIN_SAMPLING_RATE = 1000
MAX_SAMPLING_RATE = 2000000

class InsertSilenceDialog(sdialog.Ui_Dialog,QDialog):
    pass
class ChangeVolumeDialog(cvdialog.Ui_Dialog,QDialog):
    pass
class FilterDialog(filterdg.Ui_Dialog,QDialog):
    pass

class BatSoundWindow(QtGui.QMainWindow, Ui_DuettoMainWindow):
    def __init__(self, parent=None):
        super(BatSoundWindow, self).__init__(parent)
        self.setupUi(self)

        self.dock_spec_settings.setVisible(False)
        self.dock_osc_settings.setVisible(False)
        self.dock_powspec_settings.setVisible(False)
        self.connect(self.widget,SIGNAL("IntervalChanged"),self.updatePowSpecWin)
        self.NFFT_pow = int(self.cbx_fftsize_pow.currentText())
        self.window_pow = self.cbx_fftwindow_pow.currentText()
        self.NFFT_spec = int(self.cbx_fftsize.currentText())
        self.window_spec = self.cbx_fftwindow.currentText()
        self.overlap_spec = self.sbx_fftoverlap.value()
        self.pow_spec_windows = []



    @QtCore.pyqtSlot()
    def on_actionResampling_triggered(self):
        resamplingDialog=sdialog.Ui_Dialog()
        resamplingDialogWindow=InsertSilenceDialog()
        resamplingDialog.setupUi(resamplingDialogWindow)
        resamplingDialog.label.setText("Select the new Sampling Rate.")
        resamplingDialog.insertSpinBox.setValue(self.widget.signalProcessor.signal.samplingRate)
        if (resamplingDialogWindow.exec_()):
            val=resamplingDialog.insertSpinBox.value()
            if(val > MIN_SAMPLING_RATE and val < MAX_SAMPLING_RATE):
                self.widget.resampling(val)
            else:
                if(val < MIN_SAMPLING_RATE):
                    QMessageBox.warning(QMessageBox(), "Error",
                                        "Sampling rate should be greater than "+str(MIN_SAMPLING_RATE))
                elif(val > MAX_SAMPLING_RATE ):
                    QMessageBox.warning(QMessageBox(), "Error",
                                        "Sampling rate should be less than "+str(MAX_SAMPLING_RATE))

    @QtCore.pyqtSlot()
    def on_actionCut_triggered(self):
        self.widget.cut()

    @QtCore.pyqtSlot()
    def on_actionCopy_triggered(self):
        self.widget.copy()

    @QtCore.pyqtSlot()
    def on_actionPaste_triggered(self):
        self.widget.paste()

    @QtCore.pyqtSlot()
    def on_actionSmart_Scale_triggered(self):
        scaleDialog=cvdialog.Ui_Dialog()
        scaleDialogWindow=InsertSilenceDialog()
        scaleDialog.setupUi(scaleDialogWindow)
        if (scaleDialogWindow.exec_()):
            factor=scaleDialog.spinboxConstValue.value()
            if (scaleDialog.rbuttonConst.isChecked()):
                function = "const"
            elif(scaleDialog.rbuttonNormalize.isChecked()):
                function = "normalize"
                factor = scaleDialog.spinboxNormalizePercent.value()
            else:
                function = scaleDialog.cboxModulationType.currentText()
            fade = "IN" if scaleDialog.rbuttonFadeIn.isChecked() else ("OUT" if scaleDialog.rbuttonFadeOut.isChecked() else "")
            self.widget.scale(factor, function, fade)

    @QtCore.pyqtSlot()
    def on_actionInsert_Silence_triggered(self):
        silenceDialog=sdialog.Ui_Dialog()
        silenceDialogWindow=InsertSilenceDialog()
        silenceDialog.setupUi(silenceDialogWindow)
        if (silenceDialogWindow.exec_()):
            self.widget.insertSilence(silenceDialog.insertSpinBox.value())

    @QtCore.pyqtSlot()
    def on_actionGenerate_White_Noise_triggered(self):
        whiteNoiseDialog=sdialog.Ui_Dialog()
        whiteNoiseDialogWindow=InsertSilenceDialog()
        whiteNoiseDialog.setupUi(whiteNoiseDialogWindow)
        whiteNoiseDialog.label.setText("Select the duration in ms \n of the white noise.")
        whiteNoiseDialog.insertSpinBox.setValue(1000)
        if (whiteNoiseDialogWindow.exec_()):
            self.widget.insertWhiteNoise(whiteNoiseDialog.insertSpinBox.value())

    @QtCore.pyqtSlot()
    def on_actionFilter_triggered(self):
        filterDialog=filterdg.Ui_Dialog()
        filterDialogWindow=InsertSilenceDialog()
        filterDialog.setupUi(filterDialogWindow)
        if (filterDialogWindow.exec_()):
            type=None
            Fc,Fl,Fu=0,0,0
            if(filterDialog.rButtonLowPass.isChecked()):
                type=FILTER_TYPE().LOW_PASS
                Fc=filterDialog.spinBoxLowPass.value()
            elif(filterDialog.rButtonHighPass.isChecked()):
                type=FILTER_TYPE().HIGH_PASS
                Fc=filterDialog.spinBoxHighPass.value()

            elif(filterDialog.rButtonBandPass.isChecked()):
                type=FILTER_TYPE().BAND_PASS
                Fl=filterDialog.spinBoxBandPassFl.value()
                Fu=filterDialog.spinBoxBandPassFu.value()
            elif(filterDialog.rButtonBandStop.isChecked()):
                type=FILTER_TYPE().BAND_STOP
                Fl=filterDialog.spinBoxBandStopFl.value()
                Fu=filterDialog.spinBoxBandStopFu.value()

            if(type!=None):
                self.widget.filter(type, Fc,Fl,Fu)

    @QtCore.pyqtSlot()
    def on_actionSilence_triggered(self):
        self.widget.silence()

    @QtCore.pyqtSlot()
    def on_actionNormalize_triggered(self):
        self.widget.normalize()

    @QtCore.pyqtSlot()
    def on_action_Reverse_triggered(self):
        self.widget.reverse()


    def updatePowSpecWin(self):
       for win in self.pow_spec_windows:
           minx = self.widget.zoomCursor.min
           maxx = max(self.widget.zoomCursor.max ,min(minx + self.NFFT_pow,len(self.widget.signalProcessor.signal.data)))
           win.updatePowSpectrumInterval(self.widget.signalProcessor.signal.data[minx:maxx])


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

        minx = self.widget.zoomCursor.min
        maxx = max(self.widget.zoomCursor.max ,min(minx + self.NFFT_pow,len(self.widget.signalProcessor.signal.data)))
        dg_pow_spec.plot(self.widget.signalProcessor.signal.data[minx:maxx], self.widget.signalProcessor.signal.samplingRate, self.NFFT_pow, self.window_pow)

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
    def on_actionOsilogram_Detector_triggered(self):
        print("")

    @QtCore.pyqtSlot()
    def on_actionSpectrogram_Detector_triggered(self):
        print("SP")

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

