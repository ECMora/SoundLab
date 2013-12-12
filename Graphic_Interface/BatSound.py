from MainWindow import Ui_MplMainWindow
from MyPowerSpecWindow import PowerSpectrumWindow
from PyQt4 import QtCore
from PyQt4 import QtGui
import sys
from scipy.io.wavfile import read
from PyQt4.phonon import Phonon


class BatSoundWindow(QtGui.QMainWindow, Ui_MplMainWindow):
    def __init__(self, parent=None):
        super(BatSoundWindow, self).__init__(parent)
        self.setupUi(self)

        self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.mediaObject = Phonon.MediaObject(self)
        self.mediaObject.tick.connect(self.tick)
        Phonon.createPath(self.mediaObject, self.audioOutput)

        QtCore.QObject.connect(self.actionOpen, QtCore.
        SIGNAL('triggered()'), self.select_file)
        QtCore.QObject.connect(self.actionExit, QtCore.
        SIGNAL('triggered()'), QtGui.qApp, QtCore.SLOT("quit()"))
        QtCore.QObject.connect(self.actionPlay_Sound,QtCore.
                            SIGNAL('triggered()'),self.play_sound)
        QtCore.QObject.connect(self.actionStop_Sound,QtCore.
                            SIGNAL('triggered()'),self.mediaObject.stop)
        QtCore.QObject.connect(self.actionZoom_out_entire_file, QtCore.SIGNAL('triggered()'), self.widget.zoom_out_entire)
        QtCore.QObject.connect(self.actionZoomIn, QtCore.SIGNAL('triggered()'), self.widget.zoom_in)
        QtCore.QObject.connect(self.actionZoom_out, QtCore.SIGNAL('triggered()'), self.widget.zoom_out)
        self.dock_spec_settings.setVisible(False)
        self.dock_osc_settings.setVisible(False)
        self.dock_powspec_settings.setVisible(False)
        self.NFFT_pow = int(self.cbx_fftsize_pow.currentText())
        self.window_pow = self.cbx_fftwindow_pow.currentText()
        self.NFFT_spec = int(self.cbx_fftsize.currentText())
        self.window_spec = self.cbx_fftwindow.currentText()
        self.overlap_spec = (self.sbx_fftoverlap.value() * self.NFFT_spec)/100
        self.pow_spec_windows = []

    @QtCore.pyqtSlot()
    def on_actionClear_Spectogram_triggered(self):
        self.widget.update_spectrogram(self.NFFT_spec, self.overlap_spec)

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
        print self.widget.zmax, self.widget.zmin,self.widget.minIntervalLength

        if self.widget.first:
            self.widget.calc_highest_freq()
            self.widget.first = False
        if self.widget.zmax - self.widget.zmin < self.widget.minIntervalLength:
            m = QtGui.QMessageBox(self)
            m.setText("The least that you can select interval length is " + str(self.widget.minIntervalLength))
            m.show()
        else : self.widget.plot_highest_freq(self.widget.zmin, self.widget.zmax)

    @QtCore.pyqtSlot()
    def on_actionPower_Spectrum_triggered(self):
        dg_pow_spec = (PowerSpectrumWindow(self))
        minx = self.widget.zmin * self.widget.rate
        maxx = max(self.widget.zmax * self.widget.rate ,min(minx + self.NFFT_pow,len(self.widget.data)))
        dg_pow_spec.plot(self.widget.data[minx:maxx], self.widget.rate, self.NFFT_pow, self.window_pow)
        self.pow_spec_windows.append(dg_pow_spec)

    @QtCore.pyqtSlot()
    def on_actionPower_Spectrum_Settings_triggered(self):
        self.dock_powspec_settings.setVisible(True)
        self.dock_powspec_settings.setFloating(False)

    @QtCore.pyqtSlot()
    def on_actionSelect_all_triggered(self):
        self.widget.update_osc_span(self.widget.minact,self.widget.maxact)
        self.widget.update_spec_span(self.widget.minact,self.widget.maxact)

    @QtCore.pyqtSlot()
    def on_btnosc_apply_clicked(self):
        pass;

    @QtCore.pyqtSlot()
    def on_btnpow_apply_clicked(self):
        self.NFFT_pow = int(self.cbx_fftsize_pow.currentText())
        self.window_pow = self.cbx_fftwindow_pow.currentText()

    @QtCore.pyqtSlot()
    def on_btnspec_apply_clicked(self):
        self.NFFT_spec = int(self.cbx_fftsize.currentText())
        self.window_spec = self.cbx_fftwindow.currentText()
        self.overlap_spec = (self.NFFT_spec * self.sbx_fftoverlap.value())/100

        self.widget.update_spec_settings(NFFT=self.NFFT_spec,window=self.window_spec, overlap = self.overlap_spec)

    @QtCore.pyqtSlot()
    def on_actionSpectogram_Settings_triggered(self):
        self.dock_spec_settings.setVisible(True)
        self.dock_spec_settings.setFloating(False)

    @QtCore.pyqtSlot()
    def on_actionOscillogram_Settings_triggered(self):
        self.dock_osc_settings.setVisible(True)
        self.dock_osc_settings.setFloating(False)

    def select_file(self):
        self.actionHighest_instant_frequency.setChecked(False)
        file = QtGui.QFileDialog.getOpenFileName(self, caption="Select a wav file", filter="*.wav")
        if file != '':
            rate, data = read(file)
            self.first = True
            self.widget.read_file(rate, data , self.NFFT_spec, self.overlap_spec)
            self.mediaObject.setTickInterval(1)
            source = Phonon.MediaSource(file)
            self.mediaObject.setCurrentSource(source)

    def play_sound(self):
        if self.widget.zmin != self.widget.zmax:
            self.start = max(self.widget.zmin*1000, self.widget.minact*1000)
            self.end = min(self.start + (self.widget.zmax - self.widget.zmin)*1000, self.widget.maxact*1000)
        else:
            self.start = self.widget.minact*1000
            self.end = self.widget.maxact*1000

        self.mediaObject.seek(self.start)
        self.mediaObject.play()

    def tick(self,time):
        if time > self.end:
            self.mediaObject.stop()
        return

    @QtCore.pyqtSlot()
    def on_actionCombined_triggered(self):
        self.widget.graph_combined(512, 0)

    @QtCore.pyqtSlot()
    def on_actionSpectogram_triggered(self):
        self.widget.graph_spec(512, 0)

    @QtCore.pyqtSlot()
    def on_actionOscilogram_triggered(self):
        self.widget.graph_osc()

# create the GUI application
app = QtGui.QApplication(sys.argv)
# instantiate the main window
dmw = BatSoundWindow()
# show it
dmw.show()
# start the Qt main loop execution, exiting from this script
# with the same return code of Qt application
sys.exit(app.exec_())
