import os.path
from PyQt4.QtCore import pyqtSlot, Qt
import PyQt4.QtCore as QtCore
from PyQt4 import QtGui
import xlwt
from PyQt4.QtGui import QFileDialog
from Duetto_Core.AudioSignals.AudioSignal import AudioSignal
from Duetto_Core.AudioSignals.WavFileSignal import WavFileSignal
from Duetto_Core.SignalProcessors.SignalProcessor import SignalProcessor
from ..Dialogs.elemDetectSettings import ElemDetectSettingsDialog
from SegmentationAndClasificationWindowUI import Ui_MainWindow
from ..Dialogs import ParametersMeasurementDialog as paramdialog
from Duetto_Core.Detectors.ElementsDetectors.OneDimensionalElementsDetector import OneDimensionalElementsDetector


class ParameterMeasurementDialog(paramdialog.Ui_ParameterMeasurement,QtGui.QDialog):
    pass


class SegmentationAndClasificationWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None,signal=None):
        super(SegmentationAndClasificationWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        if(signal is  None):
             QtGui.QMessageBox.warning(QtGui.QMessageBox(), "Error", "There is no signal to analyze.")
        assert isinstance(signal,AudioSignal)
        self.widget = self.ui.widget
        self.widget.signalProcessor.signal = signal
        self.widget.mainCursor.min, self.widget.mainCursor.max = 0, len(self.widget.signalProcessor.signal.data)
        self.ui.dockWidgetParameterTableOscilogram.setVisible(False)
        self.ui.dockWidgetParameterTableSpectrogram.setVisible(False)
        self.show()
        self.ui.dock_settings.setVisible(False)
        self.parameterTable_rowcolor_odd,self.parameterTable_rowcolor_even = QtGui.QColor(120,150,200,255),QtGui.QColor(150,200,250,255)
        self.parameterDecimalPlaces = 5
        self.widget.visibleOscilogram = True
        self.widget.visibleSpectrogram = True
        self.widget.visualChanges = True
        self.OscilogramThreshold = 0
        self.oscilogramDetectionSettings = {"Threshold": -40, "Threshold2": 0, "MergeFactor": 0.5, "MinSize": 1, "Decay": 1, "SoftFactor": 6}
        self.specgramDetectionSettings = {"Threshold": 95 ,"minSizeTime": 0, "minSizeFreq": 0, "mergeFactorTime": 0, "mergeFactorFreq": 0}
        sr = self.widget.signalProcessor.signal.samplingRate#["Mean", True, SignalProcessor.mean]
        self.parameterMeasurement = dict(
            Temporal=[["start", True, lambda x: x.startTime()], ["end", True,  lambda x: x.endTime()],
                      ["PeekToPeek", True, lambda x: x.peekToPeek()],
                      ["rms", True, lambda x: x.rms()],
                      ["DistanceFromStartToMax", True,lambda x: x.distanceFromStartToMax()],
                      ["PeakFreq(Hz)", True,lambda x: x.peakFreq()]],
                      #funciones que reciben un elemento temporal 1 dimension
            Spectral=[["startTime", True, lambda x: x.startTime()], ["endTime", True, lambda x: x.endTime()], ["startFrecuency", True,lambda x:x.minFreq()],[ "endFrecuency",True,lambda x:x.maxFreq()],
                      ["PeakFrecuency", True,lambda x:x.PeakFreq()]]) #funciones que reciben un elemento spectral 2 dimensiones y devuelven el valor del parametro medido
        #the order of the elements in the array of self.parameterMeasurement["Temporal"] is relevant for the visualization in the table and the
        #binding to the checkboxes in the dialog of parameter measurement
        self.widget.refresh()

    @pyqtSlot()
    def on_actionView_Parameters_triggered(self):
        if self.ui.dockWidgetParameterTableOscilogram.isVisible():
            self.ui.dockWidgetParameterTableOscilogram.setVisible(False)
        else:
            self.ui.dockWidgetParameterTableOscilogram.setVisible(True)
            self.ui.dockWidgetParameterTableOscilogram.setFloating(False)

        if self.ui.dockWidgetParameterTableSpectrogram.isVisible():
            self.ui.dockWidgetParameterTableSpectrogram.setVisible(False)
        else:
            self.ui.dockWidgetParameterTableSpectrogram.setVisible(True)
            self.ui.dockWidgetParameterTableSpectrogram.setFloating(False)

    @pyqtSlot()
    def on_actionExcel_File_triggered(self, name="",table = None):
        if name != "":
            fname = name
        else:
            if not self.widget.signalProcessor.signal.opened():
                return
            fname = unicode(QFileDialog.getSaveFileName(self,"Save meditions as excel file",self.widget.signalProcessor.signal.name()+".xls","*.xls"))
        if fname:
            wb = xlwt.Workbook()
            a =  "Temporal Meditions"
            ws = wb.add_sheet(a)
            self.writedata(ws,table)
            #add spectral meditions
            wb.save(fname)

    @pyqtSlot()
    def startBatchProcess(self):
        thread = QtCore.QThread(self)
        class worker(QtCore.QObject):
            def __init__(self,worker):
                QtCore.QObject.__init__(self)
                self.work=worker
        processworker=worker(self.batch)
        thread.started.connect(processworker.work)
        processworker.moveToThread(thread)
        thread.start()

    def batch(self):
        #start in a diferent thread
        threshold, decay, minsize= abs(self.oscilogramDetectionSettings["Threshold"]), self.oscilogramDetectionSettings["Decay"], self.oscilogramDetectionSettings["MinSize"],
        softfactor, mergefactor, threshold2 =  self.oscilogramDetectionSettings["SoftFactor"],self.oscilogramDetectionSettings["MergeFactor"],abs(self.oscilogramDetectionSettings["Threshold2"])
        table = QtGui.QTableWidget()

        detector = OneDimensionalElementsDetector()
        directoryinput = str(self.ui.lineeditFilePath.text())
        directoryoutput = str(self.ui.lineEditOutputFolder.text())
        if(not os.path.isdir(directoryinput)):
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), "Error", "The input path is not a directory.")
            return
        if(not os.path.isdir(directoryoutput)):
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), "Error", "The output path is not a directory.")
            return

        if self.ui.cbxSingleFile.isChecked():
            wb = xlwt.Workbook()


        sounds = []
        raiz = ""
        for root, dirs, files in os.walk(directoryinput):
            raiz = root if raiz == "" else raiz
            for f in files:
                sounds.append(os.path.join(root, f))
        totalms = 0
        for filename in sounds:
            try:
                signalProcessor = SignalProcessor()
                signalProcessor.signal.open(filename)
                totalms += len(signalProcessor.signal.data)/(1.0*signalProcessor.signal.samplingRate)
            except:
                pass
        msProcessed = 0


        for filename in sounds:
            try:
                signalProcessor = SignalProcessor()
                signalProcessor.signal.open(filename)
                self.ui.listwidgetProgress.addItem("Processing "+signalProcessor.signal.name())
                detector.detect(signalProcessor.signal,0,len(signalProcessor.signal.data),threshold, decay, minsize, softfactor, mergefactor, threshold2)
                table = QtGui.QTableWidget()
                table.setRowCount(detector.elementCount())
                paramsTomeasure = [x for x in self.parameterMeasurement["Temporal"] if x[1]]
                table.setColumnCount(len(paramsTomeasure))
                self.ui.listwidgetProgress.addItem("Save data of " +signalProcessor.signal.name())
                for i,element in enumerate(detector.elements()):
                    for j,prop in enumerate(paramsTomeasure):
                        item = QtGui.QTableWidgetItem(str(prop[2](element)))
                        table.setItem(i, j, item)
                table.setHorizontalHeaderLabels([label[0] for label in paramsTomeasure])
                if(self.ui.cbxSingleFile.isChecked()):
                    ws = wb.add_sheet(signalProcessor.signal.name())
                    self.writedata(ws,table)
                else:
                    self.on_actionExcel_File_triggered(os.path.join(directoryoutput,signalProcessor.signal.name()+".xls"),table)

                self.ui.listwidgetProgress.addItem(signalProcessor.signal.name()+" has been processed")
                msProcessed += len(signalProcessor.signal.data)/(1.0*signalProcessor.signal.samplingRate)
            except:
                self.ui.listwidgetProgress.addItem("Some problem found while processing " + signalProcessor.signal.name())
            self.ui.progressBarProcesed.setValue(round(100*(msProcessed+1)/totalms))
        self.ui.progressBarProcesed.setValue(100)
        name = "DuettoMeditions"
        #valorar si ya existe el fichero reescribirlo o guardalo con otro nombre
        wb.save(os.path.join(directoryoutput,name + ".xls"))

    def selectInputFolder(self):
        inputfolder = QFileDialog.getExistingDirectory()
        self.ui.lineeditFilePath.setText(inputfolder)

    def selectOutputFolder(self):
        outputfolder = QFileDialog.getExistingDirectory()
        self.ui.lineEditOutputFolder.setText (outputfolder)

    def writedata(self,ws,tableParameter=None):
        if(tableParameter is None):
            tableParameter = self.ui.tableParameterOscilogram
        #write the data of the meditions into the stylesheet of excell ws
        styleheader = xlwt.easyxf('font: name Times New Roman, color-index blue, bold on, height 300')
        stylebody = xlwt.easyxf('font: name Times New Roman, color-index black, height 220', num_format_str='#,##0.00')
        stylecopyrigth = xlwt.easyxf('font: name Arial, color-index pale_blue, height 250, italic on', num_format_str='#,##0.00')
        for index,header in enumerate([label[0] for label in self.parameterMeasurement["Temporal"]]):
            ws.write(0, index, header,styleheader)
        for i in range(1,tableParameter.model().rowCount()+1):
            for j in range(tableParameter.model().columnCount()):
                ws.write(i, j, str(tableParameter.item(i-1, j).data(Qt.DisplayRole).toString()),stylebody)
        ws.write(tableParameter.model().rowCount()+3,0,"Duetto Sound Lab Oscilogram Meditions",stylecopyrigth)

    @pyqtSlot()
    def on_actionDetection_triggered(self):
        elementsDetectorDialog = ElemDetectSettingsDialog(self)
        elementsDetectorDialog.dsbxThreshold.setValue(self.oscilogramDetectionSettings["Threshold"])
        elementsDetectorDialog.sbxSoftFactor.setValue(self.oscilogramDetectionSettings["SoftFactor"])
        elementsDetectorDialog.dsbxMinSize.setValue(self.oscilogramDetectionSettings["MinSize"])
        elementsDetectorDialog.dsbxThreshold2.setValue(self.oscilogramDetectionSettings["Threshold2"])
        elementsDetectorDialog.dsbxMergeFactor.setValue(self.oscilogramDetectionSettings["MergeFactor"])
        elementsDetectorDialog.dsbxDecay.setValue(self.oscilogramDetectionSettings["Decay"])
        #specgram settings
        elementsDetectorDialog.dsbxThresholdSpec.setValue(self.specgramDetectionSettings["Threshold"])
        elementsDetectorDialog.dsbxMinSizeFreq.setValue(self.specgramDetectionSettings["minSizeFreq"])
        elementsDetectorDialog.dsbxminSizeTime.setValue(self.specgramDetectionSettings["minSizeTime"])
        elementsDetectorDialog.sbxMergeFactorTime.setValue(self.specgramDetectionSettings["mergeFactorTime"])
        elementsDetectorDialog.sbxMergeFactorFreq.setValue(self.specgramDetectionSettings["mergeFactorFreq"])

        elementsDetectorDialog.widgetOscilogram.open("Didactic Signals\\recognition.wav")
        elementsDetectorDialog.widgetSpecgram.open("Didactic Signals\\recognition.wav")

        if elementsDetectorDialog.exec_():
            if elementsDetectorDialog.chbxDetectOsc.isChecked():
                try:
                    threshold = abs(elementsDetectorDialog.dsbxThreshold.value())
                    threshold2 = abs(elementsDetectorDialog.dsbxThreshold2.value())
                    minsize = elementsDetectorDialog.dsbxMinSize.value()
                    mergefactor = elementsDetectorDialog.dsbxMergeFactor.value()
                    softfactor = elementsDetectorDialog.sbxSoftFactor.value()
                    decay = elementsDetectorDialog.dsbxDecay.value()
                    self.oscilogramDetectionSettings["Threshold"] = -threshold
                    self.oscilogramDetectionSettings["Threshold2"] = -threshold2
                    self.oscilogramDetectionSettings["MinSize"] = minsize
                    self.oscilogramDetectionSettings["MergeFactor"] = mergefactor
                    self.oscilogramDetectionSettings["SoftFactor"] = softfactor
                    self.oscilogramDetectionSettings["Decay"] = decay
                    self.widget.detectElementsInOscilogram(threshold, decay, minsize, softfactor, mergefactor, threshold2)
                    self.ui.tableParameterOscilogram.clear()
                    self.ui.tableParameterOscilogram.setRowCount(len(self.widget.OscilogramElements))
                    paramsTomeasure = [x for x in self.parameterMeasurement["Temporal"] if x[1]]
                    self.ui.tableParameterOscilogram.setColumnCount(len(paramsTomeasure))
                    for i in range(self.ui.tableParameterOscilogram.rowCount()):
                        for j,prop in enumerate(paramsTomeasure):
                            item = QtGui.QTableWidgetItem(str(round(prop[2](self.widget.OscilogramElements[i]),self.parameterDecimalPlaces)))
                            item.setBackgroundColor(self.parameterTable_rowcolor_odd if i%2==0 else self.parameterTable_rowcolor_even)
                            self.ui.tableParameterOscilogram.setItem(i, j, item)

                except:
                    pass
                self.ui.tableParameterOscilogram.setHorizontalHeaderLabels([label[0] for label in paramsTomeasure])
            if elementsDetectorDialog.chbxDetectSpec.isChecked():
                try:
                    #updating previous data ofr detection
                    self.specgramDetectionSettings["Threshold"] = elementsDetectorDialog.dsbxThresholdSpec.value()
                    self.specgramDetectionSettings["minSizeFreq"] = elementsDetectorDialog.dsbxMinSizeFreq.value()
                    self.specgramDetectionSettings["minSizeTime"] = elementsDetectorDialog.dsbxminSizeTime.value()
                    self.specgramDetectionSettings["mergeFactorTime"] = elementsDetectorDialog.sbxMergeFactorTime.value()
                    self.specgramDetectionSettings["mergeFactorFreq"] = elementsDetectorDialog.sbxMergeFactorFreq.value()
                    print(len(self.widget.specgramSettings.Pxx))
                    print(len(self.widget.specgramSettings.Pxx[0]))
                    self.widget.detectElementsInEspectrogram(self.specgramDetectionSettings["Threshold"])

                    self.ui.tableParameterSpectrogram.clear()
                    self.ui.tableParameterSpectrogram.setRowCount(len(self.widget.SpectrogramElements))
                    paramsTomeasure = [x for x in self.parameterMeasurement["Spectral"] if x[1]]
                    self.ui.tableParameterSpectrogram.setColumnCount(len(paramsTomeasure))
                    for i in range(self.ui.tableParameterSpectrogram.rowCount()):
                        for j,prop in enumerate(paramsTomeasure):
                            item = QtGui.QTableWidgetItem(str(round(prop[2](self.widget.SpectrogramElements[i][0]),self.parameterDecimalPlaces)))
                            item.setBackgroundColor(self.parameterTable_rowcolor_odd if i%2==0 else self.parameterTable_rowcolor_even)
                            self.ui.tableParameterSpectrogram.setItem(i, j, item)
                except:
                    pass
                self.ui.tableParameterSpectrogram.setHorizontalHeaderLabels([label[0] for label in paramsTomeasure])


    @pyqtSlot()
    def on_actionParameters_Measurement_triggered(self):
        paramMeasurementDialog = paramdialog.Ui_ParameterMeasurement()
        paramMeasurementDialogWindow = ParameterMeasurementDialog()
        paramMeasurementDialog.setupUi(paramMeasurementDialogWindow)
        paramMeasurementDialog.cbxStartTime.setChecked(self.parameterMeasurement["Temporal"][0][1])#start time
        paramMeasurementDialog.cbxEndTime.setChecked(self.parameterMeasurement["Temporal"][1][1])#end time
        paramMeasurementDialog.cbxPeekToPeek.setChecked(self.parameterMeasurement["Temporal"][2][1])#peek to peek
        paramMeasurementDialog.cbxRms.setChecked(self.parameterMeasurement["Temporal"][3][1])#rms
        paramMeasurementDialog.cbxDistancefromStartToMax.setChecked(self.parameterMeasurement["Temporal"][4][1])#distance to max
        paramMeasurementDialog.cbxPeakFreq.setChecked(self.parameterMeasurement["Temporal"][5][1])#max freq
        if paramMeasurementDialogWindow.exec_():
            self.parameterMeasurement["Temporal"][0][1] = paramMeasurementDialog.cbxStartTime.isChecked()
            self.parameterMeasurement["Temporal"][1][1] = paramMeasurementDialog.cbxEndTime.isChecked()#end time
            self.parameterMeasurement["Temporal"][2][1] = paramMeasurementDialog.cbxPeekToPeek.isChecked()#peek to peek
            self.parameterMeasurement["Temporal"][3][1] = paramMeasurementDialog.cbxRms.isChecked()#rms
            self.parameterMeasurement["Temporal"][4][1] = paramMeasurementDialog.cbxDistancefromStartToMax.isChecked()#distance to max
            self.parameterMeasurement["Temporal"][5][1] = paramMeasurementDialog.cbxPeakFreq.isChecked()#max freq

    @pyqtSlot()
    def on_actionClear_Meditions_triggered(self):
        self.widget.clearCursors()
        self.widget.visualChanges = True
        self.widget.refresh()



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
    def on_actionPlay_Sound_triggered(self):
        self.widget.play()

    @QtCore.pyqtSlot()
    def on_actionStop_Sound_triggered(self):
        self.widget.stop()

    @QtCore.pyqtSlot()
    def on_actionPause_Sound_triggered(self):
        self.widget.pause()

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
    def on_actionSettings_triggered(self):
        if self.dock_settings.isVisible():
            self.dock_settings.setVisible(False)
        else:
            self.dock_settings.setVisible(True)
            self.dock_settings.setFloating(False)
