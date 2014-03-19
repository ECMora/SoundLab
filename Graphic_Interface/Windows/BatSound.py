import sys
from pyqtgraph.Qt import QtCore, QtGui
import numpy
import os
import pyqtgraph
import pyqtgraph.widgets.HistogramLUTWidget
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
from PyQt4.QtGui import QDialog, QMessageBox, QFileDialog
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL
from SegmentationAndClasificationWindow import SegmentationAndClasificationWindow
from Duetto_Core.SignalProcessors.FilterSignalProcessor import FILTER_TYPE
from MainWindow import Ui_DuettoMainWindow
from Graphic_Interface.Widgets.MyPowerSpecWindow import PowerSpectrumWindow
from Graphic_Interface.Dialogs import InsertSilenceDialog as sdialog, FilterOptionsDialog as filterdg, ChangeVolumeDialog as cvdialog
from PyQt4 import QtCore, QtGui

MIN_SAMPLING_RATE = 1000
MAX_SAMPLING_RATE = 2000000


class InsertSilenceDialog(sdialog.Ui_Dialog, QDialog):
    pass


class ChangeVolumeDialog(cvdialog.Ui_Dialog, QDialog):
    pass


class FilterDialog(filterdg.Ui_Dialog, QDialog):
    pass


class BatSoundWindow(QtGui.QMainWindow, Ui_DuettoMainWindow):
    dropchanged = QtCore.pyqtSignal(QtCore.QMimeData)
    def __init__(self, parent=None):
        super(BatSoundWindow, self).__init__(parent)
        self.setupUi(self)
        params = [
        {'name': 'Oscillogram Settings', 'type': 'group', 'children': [
            {'name': 'Milliseconds per plot', 'type': 'int', 'value': 0},
            {'name': 'Min amplitude', 'type': 'float', 'value': 0, 'step': 0.1},
            {'name': 'Max amplitude', 'type': 'float', 'value': 0, 'step': 0.1},
            {'name': 'Grid', 'type': 'group', 'children': [
                {'name': 'X', 'type': 'bool','default': True, 'value': True},
                {'name': 'Y', 'type': 'bool','default':True , 'value': True},

            ]},
            {'name':'Background color', 'type':'color','value':"000", 'default':"000"},
            {'name': 'Plot color', 'type': 'color', 'value':"FFF", 'default': "FFF"},
        ]},

        {'name': 'Spectrogram Settings', 'type': 'group', 'children': [

            {'name': 'FFT size', 'type': 'list','values': {'256': 256, '512': 512, '1024': 1024, '2048': 2048, 'Automatic': 512}, 'value':'Automatic' },
            {'name': 'FFT window', 'type': 'list', 'value':'None','default':self.widget.specgramSettings.windows[6],'values': {"blackman": self.widget.specgramSettings.windows[3],"rectangular": self.widget.specgramSettings.windows[1], "Hanning": self.widget.specgramSettings.windows[2], "Hamming": self.widget.specgramSettings.windows[0],'bartlett':self.widget.specgramSettings.windows[4],'kaiser':self.widget.specgramSettings.windows[5],'None':self.widget.specgramSettings.windows[6]}},
            {'name': 'FFT overlap', 'type': 'int', 'value':90, 'max' : 100},
            {'name': 'Background color', 'type': 'color', 'value':"000", 'default': "000"},
        ]},

        {'name': 'Power Spectrum Settings', 'type': 'group', 'children': [

             {'name': 'FFT size', 'type': 'list','default':512, 'values': {"256": 256, "512": 512, "1024": 1024, '2048': 2048, 'Automatic': 512}, 'value': 2},
             {'name': 'FFT window', 'type': 'list', 'value':'None','default':self.widget.specgramSettings.windows[6],'values': {"blackman": self.widget.specgramSettings.windows[3],"rectangular": self.widget.specgramSettings.windows[1], "Hanning": self.widget.specgramSettings.windows[2], "Hamming": self.widget.specgramSettings.windows[0],'bartlett':self.widget.specgramSettings.windows[4],'kaiser':self.widget.specgramSettings.windows[5],'None':self.widget.specgramSettings.windows[6]}},
             {'name': 'Grid', 'type': 'group', 'children': [
                {'name': 'X', 'type': 'bool','default': True, 'value': True},
                {'name': 'Y', 'type': 'bool','default':True , 'value': True},

             ]},
             {'name':'Background color', 'type':'color','value':"000", 'default':"000"},
             {'name': 'Plot color', 'type': 'color', 'value':"FFF", 'default': "FFF"},
        ]},

        ]
        self.ParamTree = Parameter.create(name='params', type='group', children=params)
        self.ParamTree.sigTreeStateChanged.connect(self.change)
        self.t = ParameterTree()
        self.t.setAutoScroll(True)
        self.t.setFixedWidth(340)
        self.t.setFixedHeight(450)
        self.t.setHeaderHidden(True)
        self.t.setParameters(self.ParamTree, showTop=False)

        lay1 = QtGui.QVBoxLayout()
        lay1.addWidget(self.t)

        self.hist = pyqtgraph.widgets.HistogramLUTWidget.HistogramLUTWidget()
        self.hist.setFixedWidth(340)
        self.hist.setFixedHeight(100)
        self.hist.item.setImageItem(self.widget.axesSpecgram.imageItem)

        action = self.hist.item.gradient.hsvAction
        action.triggered.disconnect()
        action.triggered.connect(self.widget.SaveColorBar)
        action.setCheckable(False)
        action.setText("Save")

        lay1.addWidget(self.hist)
        self.osc_settings_contents.setLayout(lay1)
        self.osc_settings_contents.layout().addWidget(self.hist)
        self.dock_settings.setVisible(False)
        self.dock_settings.setFixedWidth(350)


        self.connect(self.widget,SIGNAL("IntervalChanged"),self.updatePowSpecWin)
        self.NFFT_pow = 512

        self.window_pow = self.widget.specgramSettings.windows[6]
        self.pow_spec_backg = "000"
        self.pow_spec_plotColor = "FFF"
        self.pow_spec_gridx = True
        self.pow_spec_gridy = True
        self.colorBarsPath = "ColorBars"
        self.pow_spec_windows = []
        self.loadAllColorBars()
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        event.acceptProposedAction()
        self.dropchanged.emit(event.mimeData())

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        mimeData = event.mimeData()
        if len(mimeData.urls())>1:return
        mimeUrl = "".join([str(url.path()) for url in mimeData.urls()])

        print(mimeUrl)
        self.widget.visibleOscilogram = True
        self.widget.visibleSpectrogram = True
        self.widget.specgramSettings.NFFT = 512
        self.widget.specgramSettings.overlap = 90
        self.widget.open(mimeUrl[1:len(mimeUrl)])
        self.setWindowTitle("Duetto Sound Lab - " + self.widget.signalProcessor.signal.name())
        self.first = True
        event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        event.accept()

    def change(self, param, changes):
        print("tree changes:")
        pow = False
        for param, change, data in changes:
            path = self.ParamTree.childPath(param)
            if path is not None:
                childName = '.'.join(path)
            else:
                childName = param.name()

            if childName == 'Spectrogram Settings.FFT size':
                self.widget.specgramSettings.NFFT = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=True, updateOscillogram=False, updateSpectrogram=True)

            elif childName == 'Spectrogram Settings.FFT window':
                self.widget.specgramSettings.window = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=True, updateOscillogram=False, updateSpectrogram=True)

            elif childName == 'Spectrogram Settings.Background color':
                self.widget.spec_background = data

            elif childName == 'Spectrogram Settings.ColorMap':
                self.widget.axesSpecgram.getHistogramWidget().item._pixelVectorCache.append(data)

            elif childName == 'Spectrogram Settings.FFT overlap':
                self.widget.specgramSettings.overlap = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=True, updateOscillogram=False, updateSpectrogram=True)

            elif childName == 'Power Spectrum Settings.FFT size':
                self.NFFT_pow = data

            elif childName == 'Power Spectrum Settings.FFT window':
                self.window_pow = data

            elif childName == 'Power Spectrum Settings.Background color':
                self.pow_spec_backg = data

            elif childName == 'Power Spectrum Settings.Plot color':
                self.pow_spec_plotColor = data

            elif childName == 'Power Spectrum Settings.Grid.X':
                self.pow_spec_gridx = data

            elif childName == 'Power Spectrum Settings.Grid.Y':
                self.pow_spec_gridy = data

            elif childName == 'Oscillogram Settings.Background color':
                self.widget.osc_background = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=True, updateOscillogram=True, updateSpectrogram=False)
            elif childName == 'Oscillogram Settings.Grid.X':
                self.widget.osc_gridx = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=False, updateOscillogram=False, updateSpectrogram=False)
            elif childName == 'Oscillogram Settings.Grid.Y':
                self.widget.osc_gridy = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=False, updateOscillogram=False, updateSpectrogram=False)
            elif childName == 'Oscillogram Settings.Plot color':
                self.widget.osc_color = data
                self.widget.visualChanges = True
                self.widget.refresh(dataChanged=True, updateOscillogram=True, updateSpectrogram=False)

            print('  parameter: %s' % childName)
            print('  change:    %s' % change)
            print('  data:      %s' % str(data))
            print('  ----------')

    @QtCore.pyqtSlot()
    def on_actionSegmentation_And_Clasification_triggered(self):
        segWindow = SegmentationAndClasificationWindow(parent=self, signal=self.widget.signalProcessor.signal)

    @QtCore.pyqtSlot()
    def on_actionResampling_triggered(self):
        resamplingDialog = sdialog.Ui_Dialog()
        resamplingDialogWindow = InsertSilenceDialog()
        resamplingDialog.setupUi(resamplingDialogWindow)
        resamplingDialog.label.setText("Select the new Sampling Rate.")
        resamplingDialog.insertSpinBox.setValue(self.widget.signalProcessor.signal.samplingRate)
        if resamplingDialogWindow.exec_():
            val = resamplingDialog.insertSpinBox.value()
            if val > MIN_SAMPLING_RATE and val < MAX_SAMPLING_RATE:
                self.widget.resampling(val)
            else:
                if val < MIN_SAMPLING_RATE:
                    QMessageBox.warning(QMessageBox(), "Error",
                                        "Sampling rate should be greater than " + str(MIN_SAMPLING_RATE))
                elif val > MAX_SAMPLING_RATE:
                    QMessageBox.warning(QMessageBox(), "Error",
                                        "Sampling rate should be less than " + str(MAX_SAMPLING_RATE))

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
        scaleDialog = cvdialog.Ui_Dialog()
        scaleDialogWindow = InsertSilenceDialog()
        scaleDialog.setupUi(scaleDialogWindow)
        if scaleDialogWindow.exec_():
            factor = scaleDialog.spinboxConstValue.value()
            if scaleDialog.rbuttonConst.isChecked():
                function = "const"
            elif scaleDialog.rbuttonNormalize.isChecked():
                function = "normalize"
                factor = scaleDialog.spinboxNormalizePercent.value()
            else:
                function = scaleDialog.cboxModulationType.currentText()
            fade = "IN" if scaleDialog.rbuttonFadeIn.isChecked() else (
                "OUT" if scaleDialog.rbuttonFadeOut.isChecked() else "")
            self.widget.scale(factor, function, fade)

    @QtCore.pyqtSlot()
    def on_actionInsert_Silence_triggered(self):
        silenceDialog = sdialog.Ui_Dialog()
        silenceDialogWindow = InsertSilenceDialog()
        silenceDialog.setupUi(silenceDialogWindow)
        if silenceDialogWindow.exec_():
            self.widget.insertSilence(silenceDialog.insertSpinBox.value())

    @QtCore.pyqtSlot()
    def on_actionGenerate_Pink_Noise_triggered(self):
        whiteNoiseDialog = sdialog.Ui_Dialog()
        whiteNoiseDialogWindow = InsertSilenceDialog()
        whiteNoiseDialog.setupUi(whiteNoiseDialogWindow)
        whiteNoiseDialog.label.setText("Select the duration in ms \n of the Pink Noise.")
        whiteNoiseDialog.insertSpinBox.setValue(1000)
        if whiteNoiseDialogWindow.exec_():
            type_, Fc, Fl, Fu = self.filter_helper()
            if type_ != None:
                self.widget.insertPinkNoise(whiteNoiseDialog.insertSpinBox.value(), type_, Fc, Fl, Fu)

    @QtCore.pyqtSlot()
    def on_actionGenerate_White_Noise_triggered(self):
        whiteNoiseDialog = sdialog.Ui_Dialog()
        whiteNoiseDialogWindow = InsertSilenceDialog()
        whiteNoiseDialog.setupUi(whiteNoiseDialogWindow)
        whiteNoiseDialog.label.setText("Select the duration in ms \n of the white noise.")
        whiteNoiseDialog.insertSpinBox.setValue(1000)
        if whiteNoiseDialogWindow.exec_():
            self.widget.insertWhiteNoise(whiteNoiseDialog.insertSpinBox.value())

    def filter_helper(self):
        filterDialog = filterdg.Ui_Dialog()
        filterDialogWindow = InsertSilenceDialog()
        filterDialog.setupUi(filterDialogWindow)
        if filterDialogWindow.exec_():
            type_ = None
            Fc, Fl, Fu = 0, 0, 0
            if filterDialog.rButtonLowPass.isChecked():
                type_ = FILTER_TYPE().LOW_PASS
                Fc = filterDialog.spinBoxLowPass.value()
            elif filterDialog.rButtonHighPass.isChecked():
                type_ = FILTER_TYPE().HIGH_PASS
                Fc = filterDialog.spinBoxHighPass.value()

            elif filterDialog.rButtonBandPass.isChecked():
                type_ = FILTER_TYPE().BAND_PASS
                Fl = filterDialog.spinBoxBandPassFl.value()
                Fu = filterDialog.spinBoxBandPassFu.value()
            elif filterDialog.rButtonBandStop.isChecked():
                type_ = FILTER_TYPE().BAND_STOP
                Fl = filterDialog.spinBoxBandStopFl.value()
                Fu = filterDialog.spinBoxBandStopFu.value()
        return type_, Fc, Fl, Fu

    @QtCore.pyqtSlot()
    def on_actionFilter_triggered(self):
        type_, Fc, Fl, Fu = self.filter_helper()
        if type_ is not None:
            self.widget.filter(type_, Fc, Fl, Fu)

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
            maxx = max(self.widget.zoomCursor.max,
                       min(minx + self.NFFT_pow, len(self.widget.signalProcessor.signal.data)))
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
    def on_actionSettings_triggered(self):
        if self.dock_settings.isVisible():
            self.dock_settings.setVisible(False)
        else:
            self.dock_settings.setVisible(True)
            self.dock_settings.setFloating(False)

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
        dg_pow_spec = PowerSpectrumWindow(self,self.pow_spec_plotColor, self.pow_spec_backg, self.pow_spec_gridx, self.pow_spec_gridy)

        minx = self.widget.zoomCursor.min
        maxx = max(self.widget.zoomCursor.max, min(minx + self.NFFT_pow, len(self.widget.signalProcessor.signal.data)))
        dg_pow_spec.plot(self.widget.signalProcessor.signal.data,
                         self.widget.signalProcessor.signal.samplingRate, self.NFFT_pow, self.window_pow)

        self.pow_spec_windows.append(dg_pow_spec)

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
    def on_actionEnvelope_triggered(self):
        self.widget.envelope()

    @QtCore.pyqtSlot()
    def on_actionOpen_triggered(self):
        self.actionHighest_instant_frequency.setChecked(False)
        f = QFileDialog.getOpenFileName(self, "Select a file to open",
                                              filter="Wave Files (*.wav);;All Files (*)")
        if f != '':
            self.widget.visibleOscilogram = True
            self.widget.visibleSpectrogram = True
            self.widget.specgramSettings.NFFT = 512
            self.widget.specgramSettings.overlap = 90
            self.widget.open(f)
            self.setWindowTitle("Duetto Sound Lab - " + self.widget.signalProcessor.signal.name())
            self.first = True

    @QtCore.pyqtSlot()
    def on_actionSave_triggered(self):
        fname = unicode(QFileDialog.getSaveFileName())
        if fname:
            self.widget.save(fname)

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
    def on_actionPause_Sound_triggered(self):
        self.widget.pause()

    @QtCore.pyqtSlot()
    def on_actionCombined_triggered(self):
        self.widget.visibleOscilogram=True
        self.widget.visibleSpectrogram=True
        self.widget.refresh(dataChanged=False)

    @QtCore.pyqtSlot()
    def on_actionSpectogram_triggered(self):
        self.widget.visibleOscilogram=False
        self.widget.visibleSpectrogram=True
        self.widget.refresh(dataChanged=False)

    @QtCore.pyqtSlot()
    def on_actionOscilogram_triggered(self):
        self.widget.visibleOscilogram=True
        self.widget.visibleSpectrogram=False
        self.widget.refresh(dataChanged=False)

    @QtCore.pyqtSlot()
    def on_actionSaveColorBar_triggered(self):
        state = self.widget.axesSpecgram.getHistogramWidget().item.gradient.saveState()
        path = QtGui.QFileDialog.getSaveFileName(self, "Save Color Bar", filter="Bar Files (*.bar);;All Files (*)")
        if path != "":
            fh = open(path, 'w')
            fh.write(state.__repr__())
            fh.close()

    @QtCore.pyqtSlot()
    def on_actionLoadColorBar_triggered(self):
        path = QtGui.QFileDialog.getOpenFileName(self, "Load Color Bar", filter="Bar Files (*.bar);;All Files (*)")
        if path != "":
            fh = open(path, 'r')
            state = eval(fh.readline())
            self.widget.axesSpecgram.getHistogramWidget().item.gradient.restoreState(state)

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

    def loadAllColorBars(self):
        if os.path.exists(self.colorBarsPath):
            for i in os.listdir(self.colorBarsPath):
                if os.path.isfile(self.colorBarsPath+'\\'+ i):
                    print(i)
