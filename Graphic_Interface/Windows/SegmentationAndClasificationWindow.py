from PyQt4 import QtCore
from PyQt4 import QtGui
from Duetto_Core.AudioSignals.AudioSignal import AudioSignal
from Graphic_Interface.Windows.segmentationAndCalsificationUI import Ui_MainWindow
from Graphic_Interface.Dialogs import ui_elemDetectSettings as elementdlg


class ElementsDetectDialog(elementdlg.Ui_elemDetectSettingsDialog,QtGui.QDialog):
    pass


class SegmentationAndClasificationWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None,signal=None):
        super(SegmentationAndClasificationWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        assert isinstance(signal,AudioSignal)
        self.widget = self.ui.widget
        self.widget.signalProcessor.signal = signal
        self.widget.mainCursor.min, self.widget.mainCursor.max = 0, len(self.widget.signalProcessor.signal.data)
        self.show()
        self.widget.visibleOscilogram = True
        self.widget.visibleSpectrogram = True
        self.widget.visualChanges = True
        self.widget.refresh()


    @QtCore.pyqtSlot()
    def on_actionOscilogram_Detection_triggered(self):
        elementsDetectorDialog = elementdlg.Ui_elemDetectSettingsDialog()
        elementsDetectorDialogWindow = ElementsDetectDialog()
        elementsDetectorDialog.setupUi(elementsDetectorDialogWindow)
        elementsDetectorDialog.dsbxThreshold.setValue(-40)
        elementsDetectorDialog.dsbxMinSize.setValue(1)
        elementsDetectorDialog.dsbxThreshold2.setValue(0)
        elementsDetectorDialog.dsbxMergeFactor.setValue(0.5)
        elementsDetectorDialog.dsbxDecay.setValue(1)
        if elementsDetectorDialogWindow.exec_() and elementsDetectorDialog.chbxDetectOsc.isChecked():
            threshold = abs(elementsDetectorDialog.dsbxThreshold.value())
            threshold2 = abs(elementsDetectorDialog.dsbxThreshold2.value())
            minsize = elementsDetectorDialog.dsbxMinSize.value()
            mergefactor = elementsDetectorDialog.dsbxMergeFactor.value()
            softfactor = elementsDetectorDialog.sbxSoftFactor.value()
            decay = elementsDetectorDialog.dsbxDecay.value()
            self.widget.detectElementsInOscilogram(threshold,decay,minsize,softfactor,mergefactor,threshold2)

    @QtCore.pyqtSlot()
    def on_actionEspectrogram_Detection_triggered(self):
        pass

    @QtCore.pyqtSlot()
    def on_actionClear_Cursors_triggered(self):
        self.widget.clearCursors()
        self.widget.visualChanges = True
        self.widget.refresh()