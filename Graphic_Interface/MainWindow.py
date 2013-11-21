import sys
from PyQt4.QtGui import *
from pylab import *
from matplotlib.backends.qt4_editor.formlayout import QDialog
from Duetto_Core.AudioSignals.WavFileSignal import WavFileSignal
from Graphic_Interface.Dialogs import OptionsDialog as optdialog
from Graphic_Interface.Dialogs import InsertSilenceDialog as sdialog, FilterOptionsDialog as filterdg
from Graphic_Interface.DuettoMainWindow import *
from Duetto_Core.SignalProcessors.FilterSignalProcessor import FILTER_TYPE
from Graphic_Interface.DuettoNavigationToolBar import DuettoNavigationToolbar


class OptionsDialog(optdialog.Ui_Dialog,QDialog):
    pass
class InsertSilenceDialog(sdialog.Ui_Dialog,QDialog):
    pass
class FilterDialog(filterdg.Ui_Dialog,QDialog):
    pass

class MainWindow(QMainWindow,Ui_MainWindow):
    """
        This class is the main aplication window
        a MainWindow use a  QSignalVisualizer  control to process an audio signal
        Possible extension to handle more than one audio signal at time
        """
    def __init__(self):
        super(MainWindow, self).__init__()

    def enableScene(self):
        """
        Organize the layout of the aplication
        """
        vboxlayout=QtGui.QVBoxLayout(self.MainWindow.tabWidget.widget(0))
        vboxlayout.addWidget(self.MainWindow.signalVisualizer)
        vboxlayout2=QtGui.QVBoxLayout(self.MainWindow.centralwidget)
        vboxlayout2.addWidget(self.MainWindow.tabWidget)

        vboxlayout3=QtGui.QVBoxLayout(self.MainWindow.tabWidget.widget(2))
        vboxlayout3.addWidget(self.MainWindow.groupBoxBatchProcess)

        self.MainWindow.tabWidget.setParent(self.MainWindow.centralwidget)
        self.MainWindow.signalVisualizer.setParent(self.MainWindow.tabWidget.widget(0))

        separator = QAction(self.MainWindow.signalVisualizer)
        separator.setSeparator(True)

        self.MainWindow.signalVisualizer.addAction(self.MainWindow.actionCopiar)
        self.MainWindow.signalVisualizer.addAction(self.MainWindow.actionCortar)
        self.MainWindow.signalVisualizer.addAction(self.MainWindow.actionPegar)

        self.MainWindow.signalVisualizer.addAction(separator)

        self.MainWindow.signalVisualizer.addAction(self.MainWindow.actionFilter)
        self.MainWindow.signalVisualizer.addAction(self.MainWindow.actionReverse)
        self.MainWindow.signalVisualizer.addAction(self.MainWindow.actionClear_Silence)
        self.MainWindow.signalVisualizer.addAction(self.MainWindow.actionInsert_Silence)
        self.MainWindow.signalVisualizer.addAction(self.MainWindow.actionScale)

        deselectAction=QAction("Deselect Region",self.MainWindow.signalVisualizer)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/UI Files/resources/deselect.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        deselectAction.setIcon(icon)
        self.MainWindow.signalVisualizer.addAction(deselectAction)
        self.connect(deselectAction, QtCore.SIGNAL(QtCore.QString.fromUtf8("triggered()")), self.MainWindow.signalVisualizer.deselectZoomRegion)


        self.MainWindow.signalVisualizer.addAction(separator)

        self.MainWindow.signalVisualizer.addAction(self.MainWindow.actionRefresh_Signal)
        self.MainWindow.signalVisualizer.addAction(self.MainWindow.actionOpciones)
        ###navtoolbar = DuettoNavigationToolbar(self.MainWindow.signalVisualizer.figure.canvas, self.MainWindow.centralwidget)
        ##pack these widget into the vertical box
        #self.MainWindow.signalVisualizer.toolbar=navtoolbar
        #vboxlayout.addWidget(self.MainWindow.signalVisualizer.figure.canvas)
        #vboxlayout.addWidget(navtoolbar)



    def refreshSignal(self):
        """
        This method refresh the oscilogram and the specgram windows
        """
        if(self.MainWindow.signalVisualizer.signalProcessor.signal.opened()):
            self.MainWindow.signalVisualizer.visualChanges=True
            self.MainWindow.signalVisualizer.refresh()

    #region OPEN CLOSE AND SAVE EVENTS
    def closeEvent(self, event):
        if(self.MainWindow.signalVisualizer.signalProcessor.signal.opened()):
            save_changes = QMessageBox.question(None,
                           "Save", "Save unsaved changes?",
                           QMessageBox.Yes|QMessageBox.Default,
                           QMessageBox.No|QMessageBox.Escape)
            if(QMessageBox.Yes == save_changes or save_changes== QMessageBox.Default):
                fname = unicode(QFileDialog.getSaveFileName())
                if fname:
                    self.MainWindow.signalVisualizer.signalProcessori.signal.save(fname)


    def openEvent(self):
        formats = ["*.%s" % unicode(format).lower()\
                   for format in ["wav"]]
        openfilename =unicode(QFileDialog.getOpenFileName(self,
        "Choose File"))
        if openfilename:
            self.MainWindow.signalVisualizer.signalProcessor.signal=WavFileSignal()
            self.MainWindow.signalVisualizer.open(openfilename)
            self.MainWindow.signalVisualizer.visibleOscilogram=True
            self.MainWindow.signalVisualizer.visibleSpectrogram=True

    def saveEvent(self):
        if(self.MainWindow.signalVisualizer.signalProcessor.signal.opened()):
            fname = unicode(QFileDialog.getSaveFileName())
            if fname:
                self.MainWindow.signalVisualizer.save(fname)

    #endregion

    #region CUT COPY AND PASTE
    def cut(self):
        if(len(self.MainWindow.signalVisualizer.signalProcessor.signal.data)>0 and self.MainWindow.signalVisualizer.signalProcessor.signal.opened()):
            self.MainWindow.signalVisualizer.cut()

    def copy(self):
        if(len(self.MainWindow.signalVisualizer.signalProcessor.signal.data)>0and self.MainWindow.signalVisualizer.signalProcessor.signal.opened()):
            self.MainWindow.signalVisualizer.copy()

    def paste(self):
        if(self.MainWindow.signalVisualizer.signalProcessor.signal.opened):
            self.MainWindow.signalVisualizer.paste()
    #endregion

    def zoomIn(self):
        self.MainWindow.signalVisualizer.zoomIn()
    def reverse(self):
        self.MainWindow.signalVisualizer.reverse()

    def scale(self):
        silenceDialog=sdialog.Ui_Dialog()
        silenceDialogWindow=InsertSilenceDialog()
        silenceDialog.setupUi(silenceDialogWindow)
        silenceDialog.insertSpinBox.setValue(100)
        silenceDialog.label.setText("Select the factor to \n scale the signal in percent")
        if (silenceDialogWindow.exec_()):
            self.MainWindow.signalVisualizer.scale(silenceDialog.insertSpinBox.value())

    def insertSilence(self):
        silenceDialog=sdialog.Ui_Dialog()
        silenceDialogWindow=InsertSilenceDialog()
        silenceDialog.setupUi(silenceDialogWindow)
        if (silenceDialogWindow.exec_()):
            self.MainWindow.signalVisualizer.insertSilence(silenceDialog.insertSpinBox.value())

    def rms(self):
        self.MainWindow.signalVisualizer.rms()
    def envelope(self):
        self.MainWindow.signalVisualizer.envelope()
    def peaks(self):
        self.MainWindow.signalVisualizer.maxMinPeaks()
    def zoomOut(self):
        self.MainWindow.signalVisualizer.zoomOut()
    def filter(self):
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
                self.MainWindow.signalVisualizer.filter(type, Fc,Fl,Fu)

    def play(self):
        self.MainWindow.signalVisualizer.play()
    def pause(self):
        self.MainWindow.signalVisualizer.pause()

    def stop(self):
        self.MainWindow.signalVisualizer.stop()

    def silence(self):
        self.MainWindow.signalVisualizer.silence()
    def normalize(self):
        self.MainWindow.signalVisualizer.normalize()
    def uniformSegmenter(self):
        self.MainWindow.signalVisualizer.segment()
    def uniformSegmenter(self):
        self.MainWindow.signalVisualizer.uniformSegmenter()
    def pseudoUniformSegmenter(self):
        self.MainWindow.signalVisualizer.pseudoUniformSegmenter()
    def mean(self):
        self.MainWindow.signalVisualizer.mean()
    def zoomNone(self):
        self.MainWindow.signalVisualizer.zoomNone()
    def elements(self):
        self.MainWindow.signalVisualizer.elements()
    #modify the optios in the program
    #like FFT options and others
    def options(self):
        opt=optdialog.Ui_Dialog()
        options=OptionsDialog()
        opt.setupUi(options)
        opt.cboxFFTNumber.setCurrentIndex(opt.cboxFFTNumber.findText(str(self.MainWindow.signalVisualizer.specgramSettings.NFFT)))
        opt.cboxcolorpalette.setCurrentIndex(self.MainWindow.signalVisualizer.specgramSettings.colorPaleteIndex)
        opt.overlapspinbox.setValue(self.MainWindow.signalVisualizer.specgramSettings.overlap)
        opt.overlapspinboxthreshold.setValue(self.MainWindow.signalVisualizer.specgramSettings.threshold)
        opt.cboxwindowType.setCurrentIndex(self.MainWindow.signalVisualizer.specgramSettings.windows.index(self.MainWindow.signalVisualizer.specgramSettings.window))
        opt.checkBoxOsgram.setChecked(self.MainWindow.signalVisualizer.visibleOscilogram)
        opt.checkBoxSpecgram.setChecked(self.MainWindow.signalVisualizer.visibleSpectrogram)
        opt.checkBoxGrid.setChecked(self.MainWindow.signalVisualizer.specgramSettings.grid)
        opt.checkBoxCursors.setChecked(self.MainWindow.signalVisualizer.visibleCursors)
        if (options.exec_()):
            self.MainWindow.signalVisualizer.specgramSettings.NFFT=int(opt.cboxFFTNumber.currentText())
            self.MainWindow.signalVisualizer.specgramSettings.colorPaleteIndex=opt.cboxcolorpalette.currentIndex()
            self.MainWindow.signalVisualizer.specgramSettings.overlap=opt.overlapspinbox.value()
            self.MainWindow.signalVisualizer.specgramSettings.threshold=opt.overlapspinboxthreshold.value()
            self.MainWindow.signalVisualizer.specgramSettings.window=self.MainWindow.signalVisualizer.specgramSettings.windows[opt.cboxwindowType.currentIndex()]
            self.MainWindow.signalVisualizer.visibleOscilogram=opt.checkBoxOsgram.isChecked()
            self.MainWindow.signalVisualizer.visibleSpectrogram=opt.checkBoxSpecgram.isChecked()
            self.MainWindow.signalVisualizer.visibleCursors=opt.checkBoxCursors.isChecked()
            self.MainWindow.signalVisualizer.specgramSettings.grid=opt.checkBoxGrid.isChecked()
            self.MainWindow.signalVisualizer.visualChanges=True
            self.refreshSignal()


app = QtGui.QApplication(sys.argv)
generatedwindow=Ui_MainWindow()
DuettoWindow=MainWindow()
generatedwindow.setupUi(DuettoWindow)
DuettoWindow.MainWindow=generatedwindow
DuettoWindow.enableScene()
DuettoWindow.show()
sys.exit(app.exec_())
