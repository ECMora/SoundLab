from math import log10
import os.path
from PyQt4.QtCore import pyqtSlot, Qt
import PyQt4.QtCore as QtCore
from PyQt4 import QtGui
from matplotlib import mlab
import xlwt
from PyQt4.QtGui import QFileDialog
import pyqtgraph as pg
from Duetto_Core.AudioSignals.AudioSignal import AudioSignal
from Duetto_Core.AudioSignals.WavFileSignal import WavFileSignal
from Duetto_Core.Segmentation.Detectors.ElementsDetectors.OneDimensionalElementsDetector import OneDimensionalElementsDetector
from Duetto_Core.Segmentation.Elements.Element import Element
from Duetto_Core.SignalProcessors.SignalProcessor import SignalProcessor
from Duetto_Core.Segmentation.Elements.OneDimensionalElement import SpectralMeasurementLocation
from ..Dialogs.elemDetectSettings import ElemDetectSettingsDialog
from SegmentationAndClasificationWindowUI import Ui_MainWindow


class SegmentationAndClasificationWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None,signal=None):
        super(QtGui.QMainWindow, self).__init__(parent)
        self.setupUi(self)
        if(signal is  None):
             QtGui.QMessageBox.warning(QtGui.QMessageBox(), "Error", "There is no signal to analyze.")
        assert isinstance(signal,AudioSignal)
        if parent is not None:
            self.widget.specgramSettings = parent.widget.specgramSettings
        else:
            self.widget.visualChanges =True
            self.widget.refresh()

        self.widget.signalProcessor.signal = signal
        self.widget.mainCursor.min, self.widget.mainCursor.max = 0, len(self.widget.signalProcessor.signal.data)
        self.dockWidgetParameterTableOscilogram.setVisible(False)
        self.show()

        self.parameterTable_rowcolor_odd,self.parameterTable_rowcolor_even = QtGui.QColor(0, 0, 255,150),QtGui.QColor(0, 255, 0, 150)
        self.widget.visibleOscilogram = True
        self.widget.visibleSpectrogram = True
        self.spectralMeasurementLocation = SpectralMeasurementLocation()
        self.widget.axesOscilogram.threshold.sigPositionChangeFinished.connect(self.updateThreshold)
        self.widget.axesOscilogram.threshold.setBounds((0,2**(self.widget.signalProcessor.signal.bitDepth-1)))
        self.detectionSettings = {"Threshold": -40, "Threshold2": 0, "MergeFactor": 0.5, "MinSize": 1, "Decay": 1,
                                  "SoftFactor": 6,"ThresholdSpectral": 95 ,"minSizeTimeSpectral": 0, "minSizeFreqSpectral": 0,
                                  "SpectralLocMeasureThreshold": -20,"PeaksThreshold": -20}
        self.widget.axesOscilogram.threshold.setValue(10.0*(2**self.widget.signalProcessor.signal.bitDepth)/1000.0)
        self.temporalParameters = \
        [
                      ["Start(s)", True, lambda x: x.startTime()],
                      ["End(s)", True, lambda x: x.endTime()],
                      ["PeekToPeek(V)", True, lambda x: x.peekToPeek()],
                      ["RMS(V)", True, lambda x: x.rms()],
                      ["StartToMax(s)", True,lambda x: x.distanceFromStartToMax()],
                      ["Duration(s)", True,lambda x: x.duration()],
                      ["Spectral Elems", True,lambda x: x.spectralElements()]
        ]
        self.spectralParameters = [
            ["Max Freq(Hz)",True,lambda x,dict :x.maxFreq(dict)],
            ["Min Freq(Hz)",True,lambda x,dict :x.minFreq(dict)],
            ["Peak Freq(Hz)",True,lambda x,dict :x.peakFreq(dict)],
            ["Peak Amplitude(dB)",True,lambda x,dict :x.peakAmplitude(dict)],
            ["Band Width(Hz)",True,lambda x,dict :x.bandwidth(dict)],
            ["Peaks Above",True,lambda x,dict :x.peaksAbove(dict)]

        ] #the spectral parameters that changes in function of the location measurements
         #funciones que reciben un elemento spectral 2 dimensiones y devuelven el valor del parametro medido
        #the order of the elements in the array of self.parameterMeasurement["Temporal"] is relevant for the visualization in the table and the
        #binding to the checkboxes in the dialog of parameter measurement
        separator = QtGui.QAction(self)
        separator.setSeparator(True)
        self.widget.createContextCursor([self.actionZoomIn,self.actionZoom_out,self.actionZoom_out_entire_file,separator,self.actionCombined,self.actionOscilogram,self.actionSpectogram,separator,self.actionClear_Meditions,self.actionMeditions,self.actionView_Parameters])
        self.windowProgressDetection = QtGui.QProgressBar(self.widget)
        self.hist = pg.widgets.HistogramLUTWidget.HistogramLUTItem()
        self.hist.setImageItem(self.widget.axesSpecgram.imageItem)


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


    @pyqtSlot()
    def on_actionFull_Screen_triggered(self):
        if self.actionFull_Screen.isChecked():
            self.showFullScreen()
        else:
            self.showNormal()

    def getspectralParameters(self, spectralMeasurementLocation):
        """
        obtain the methods for spectral parameter meausrement of the measurementLocations
        """
        params = []
        threshold = self.detectionSettings["SpectralLocMeasureThreshold"]
        peaksThreshold = self.detectionSettings["PeaksThreshold"]
        if spectralMeasurementLocation.MEDITIONS[spectralMeasurementLocation.START][0]:
            for p in self.spectralParameters:
                if p[1]:
                    params.append([p[0]+"(start)", p[2], {"location": spectralMeasurementLocation.START, "threshold": threshold, "peaksThreshold": peaksThreshold}])
        if spectralMeasurementLocation.MEDITIONS[spectralMeasurementLocation.CENTER][0]:
            for p in self.spectralParameters:
                if p[1]:
                    params.append([p[0]+"(center)", p[2], {"location": spectralMeasurementLocation.CENTER, "threshold": threshold, "peaksThreshold": peaksThreshold}])
        if spectralMeasurementLocation.MEDITIONS[spectralMeasurementLocation.END][0]:
            for p in self.spectralParameters:
                if p[1]:
                    params.append([p[0]+"(end)", p[2], {"location": spectralMeasurementLocation.END, "threshold": threshold, "peaksThreshold": peaksThreshold}])
        if spectralMeasurementLocation.MEDITIONS[spectralMeasurementLocation.QUARTILE25][0]:
            for p in self.spectralParameters:
                if p[1]:
                    params.append([p[0]+"(quartile25)", p[2], {"location": spectralMeasurementLocation.QUARTILE25, "threshold": threshold, "peaksThreshold": peaksThreshold}])
        if spectralMeasurementLocation.MEDITIONS[spectralMeasurementLocation.QUARTILE75][0]:
            for p in self.spectralParameters:
                if p[1]:
                    params.append([p[0]+"(quartile75)",p[2], {"location": spectralMeasurementLocation.QUARTILE75, "threshold": threshold, "peaksThreshold": peaksThreshold}])
        return params

    def updateThreshold(self,line):
        self.detectionSettings["Threshold"] = self.toDB() if line.value() == 0 else self.toDB(line.value())

    def updateThresholdLine(self):
        self.widget.axesOscilogram.threshold.setValue(round((10.0**((60+self.detectionSettings["Threshold"])/20.0))*(2**self.widget.signalProcessor.signal.bitDepth)/1000.0,0))



    def toDB(self,value=None):
        if value is None:
            return -60
        return -60 + int(20*log10(abs(value)*1000.0/(2**self.widget.signalProcessor.signal.bitDepth)))

    @pyqtSlot(bool)
    def setVisibleThreshold(self,bool):
        self.widget.axesOscilogram.setVisibleThreshold(bool)
        self.widget.visibleEnvelope = bool

    def load_Theme(self,theme):
        self.theme = theme
        self.hist.region.setRegion(theme.histRange)
        self.hist.gradient.restoreState(theme.colorBarState)
        self.widget.load_Theme(theme)
        self.widget.visualChanges = True
        self.widget.refresh()
        self.hist.region.lineMoved()
        self.hist.region.lineMoveFinished()

    @pyqtSlot()
    def on_actionView_Parameters_triggered(self):
        self.dockWidgetParameterTableOscilogram.setVisible(self.actionView_Parameters.isChecked())


    @pyqtSlot()
    def on_actionElements_Peaks_triggered(self):
        visibility = self.actionElements_Peaks.isChecked()
        self.widget.changeElementsVisibility(visibility,Element.PeakFreqs,oscilogramItems=False)

    @pyqtSlot()
    def on_actionTemporal_Elements_triggered(self):
        visibility = self.actionTemporal_Elements.isChecked()
        for e in self.widget.Elements:
            e.visible = visibility
        self.widget.drawElements(oscilogramItems=True)

    @pyqtSlot()
    def on_actionSub_Elements_Peaks_triggered(self):
        visibility = self.actionSub_Elements_Peaks.isChecked()
        for e in self.widget.Elements:
            e.sublementsPeakFreqsVisible(visibility)
        self.widget.drawElements(oscilogramItems=False)

    @pyqtSlot()
    def on_actionTemporal_Numbers_triggered(self):
        visibility = self.actionTemporal_Numbers.isChecked()
        self.widget.changeElementsVisibility(visibility,Element.Text)

    @pyqtSlot()
    def on_actionSpectral_Numbers_triggered(self):
        visibility = self.actionSpectral_Numbers.isChecked()
        self.widget.changeElementsVisibility(visibility,Element.Text,oscilogramItems=False)

    @pyqtSlot()
    def on_actionSpectral_Locations_triggered(self):
        visibility = self.actionSpectral_Locations.isChecked()
        self.widget.changeElementsVisibility(visibility,Element.Locations,oscilogramItems=False)

    @pyqtSlot()
    def on_actionTemporal_Locations_triggered(self):
        visibility = self.actionTemporal_Locations.isChecked()
        self.widget.changeElementsVisibility(visibility,Element.Locations,oscilogramItems=True)

    @pyqtSlot()
    def on_actionSpectral_Elements_triggered(self):
        visibility = self.actionSpectral_Elements.isChecked()
        for e in self.widget.Elements:
            for e2 in e.twoDimensionalElements:
                e2.visible = visibility
        self.widget.drawElements(oscilogramItems=False)

    @pyqtSlot()
    def on_actionOsgram_Image_triggered(self):
        if self.widget.visibleOscilogram:
            self.saveImage(self.widget.axesOscilogram,"oscilogram")
        else:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), "Error", "The Oscilogram plot widget is not visible.\n You should see the data that you are going to save.")

    @pyqtSlot()
    def on_actionCombined_Image_triggered(self):
        if self.widget.visibleOscilogram and self.widget.visibleSpectrogram:
            self.saveImage(self.widget,"graph")
        else:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), "Error", "One of the plot widgets is not visible.\n You should see the data that you are going to save.")


    @pyqtSlot()
    def on_actionSpecgram_Image_triggered(self):
        if self.widget.visibleSpectrogram:
            self.saveImage(self.widget.axesSpecgram,"specgram")
        else:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), "Error", "The Espectrogram plot widget is not visible.\n You should see the data that you are going to save.")

    def saveImage(self,widget,text=""):
        fname = unicode(QFileDialog.getSaveFileName(self,"Save "+ text +" as an Image ",str(self.widget.signalProcessor.signal.name())+"-"+text+"-Duetto-Image","*.jpg"))
        if fname:
            #save as image
            image = QtGui.QPixmap.grabWindow(widget.winId())
            image.save(fname, 'jpg')

    @pyqtSlot()
    def on_actionMeditions_triggered(self, name="",table = None):
        if name != "":
            fname = name
        else:
            if not self.widget.signalProcessor.signal.opened():
                return
            fname = unicode(QFileDialog.getSaveFileName(self,"Save meditions as excel file",self.widget.signalProcessor.signal.name()+".xls","*.xls"))
        if fname:
            wb = xlwt.Workbook()
            a =  "Elements Meditions"
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

    def getSpectralData(self,signal,specgramSettings):
        """
        returns the spectral data pxx,bins and freqs of spectrogram
        """
        overlap = int(specgramSettings.NFFT * specgramSettings.overlap / 100)
        return mlab.specgram(signal.data,specgramSettings.NFFT, Fs=signal.samplingRate,
                                detrend=mlab.detrend_none, window=specgramSettings.window, noverlap=overlap,
                                sides="onesided")

    def batch(self):
        directoryinput = str(self.lineeditFilePath.text())
        directoryoutput = str(self.lineEditOutputFolder.text())
        if(not os.path.isdir(directoryinput)):
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), "Error", "The input path is not a directory.")
            return
        if(not os.path.isdir(directoryoutput)):
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), "Error", "The output path is not a directory.")
            return
        sounds = [] #the files
        raiz = ""

        for root, dirs, files in os.walk(directoryinput):
            raiz = root if raiz == "" else raiz
            for f in files:
                sounds.append(os.path.join(root, f))
        self.progressBarProcesed.setValue(0)
        processed = 0
        if self.rbttnDetection.isChecked():
            detector = OneDimensionalElementsDetector()

            singlefile = self.cbxSingleFile.isChecked()
            if singlefile:
                wb = xlwt.Workbook()

            for filename in sounds:
                try:
                    signalProcessor = SignalProcessor()
                    signalProcessor.signal = WavFileSignal(filename)
                    self.listwidgetProgress.addItem("Processing "+signalProcessor.signal.name())

                    table = QtGui.QTableWidget()
                    pxx,freqs,bins = self.getSpectralData(signalProcessor.signal,self.widget.specgramSettings)
                    detector.detect(signalProcessor.signal,0,len(signalProcessor.signal.data),abs(self.detectionSettings["Threshold"]), self.detectionSettings["Decay"],   self.detectionSettings["MinSize"],
                                           self.detectionSettings["SoftFactor"], self.detectionSettings["MergeFactor"], abs(self.detectionSettings["Threshold2"]),
                                           pxx=pxx,freqs=freqs,bins=bins,
                                           threshold_spectral=self.detectionSettings["ThresholdSpectral"],
                                           minsize_spectral=(self.detectionSettings["minSizeFreqSpectral"],self.detectionSettings["minSizeTimeSpectral"]),
                                           location= self.spectralMeasurementLocation)

                    paramsTomeasure = [x for x in self.temporalParameters if x[1]]
                    spectralparamsTomeasure = self.getspectralParameters(self.spectralMeasurementLocation)

                    table.setRowCount(detector.elementCount())

                    table.setColumnCount(len(paramsTomeasure) + len(spectralparamsTomeasure))
                    columnNames = [label[0] for label in paramsTomeasure]
                    columnNames.extend([label[0] for label in spectralparamsTomeasure])
                    table.setHorizontalHeaderLabels(columnNames)
                    self.listwidgetProgress.addItem("Save data of " +signalProcessor.signal.name())

                    for i,element in enumerate(detector.elements()):
                        for j,prop in enumerate(paramsTomeasure):
                            item = QtGui.QTableWidgetItem(str(prop[2](element)))
                            table.setItem(i, j, item)
                        for x,prop in enumerate(spectralparamsTomeasure):
                            item = QtGui.QTableWidgetItem(str(prop[1](element,prop[2])))
                            item.setBackgroundColor(self.parameterTable_rowcolor_odd if i%2==0 else self.parameterTable_rowcolor_even)
                            table.setItem(i, len(paramsTomeasure) + x, item)
                    if singlefile:
                        ws = wb.add_sheet(signalProcessor.signal.name())
                        self.writedata(ws,table)
                    else:
                        self.on_actionMeditions_triggered(os.path.join(directoryoutput,signalProcessor.signal.name()+".xls"),table)
                    self.listwidgetProgress.addItem(signalProcessor.signal.name()+" has been processed")
                    self.listwidgetProgress.update()
                    processed += 1
                except:
                    self.listwidgetProgress.addItem("Some problem found while processing ")
                self.progressBarProcesed.setValue(round(100.0*(processed)/len(sounds)))
                self.progressBarProcesed.update()
                #valorar si ya existe el fichero reescribirlo o guardalo con otro noBOx signal.samplingRate
                if singlefile:
                    wb.save(os.path.join(directoryoutput,"Duetto Sound Lab Meditions.xls"))
            #open folder
        if self.rbttnSplitFile.isChecked():
            save = WavFileSignal()
            for filename in sounds:
                try:
                    signal = WavFileSignal(filename)
                    self.listwidgetProgress.addItem("Processing "+signal.name())
                    save.channels = signal.channels
                    save.bitDepth = signal.bitDepth
                    save.samplingRate = signal.samplingRate
                    sr = signal.samplingRate
                    pieceSize = self.spboxSplitTime.value()*sr
                    pieces = len(signal.data)/pieceSize
                    left = len(signal.data)%pieceSize
                    if(pieces >= 1):
                        for i in range(pieces):
                            save.data = signal.data[i*pieceSize:(i+1)*pieceSize]
                            save.save(os.path.join(directoryoutput,str(i+1)+"-"+signal.name()))
                    if left > 0:
                        save.data = signal.data[len(signal.data)-left:]
                        save.save(os.path.join(directoryoutput,str(pieces+1)+"-"+signal.name()))
                    processed += 1
                    self.progressBarProcesed.setValue(100.0*processed/len(sounds))
                    self.listwidgetProgress.addItem(signal.name()+" has been processed")
                    self.progressBarProcesed.update()
                    self.listwidgetProgress.update()
                except:
                    print("some split problems")
        self.progressBarProcesed.setValue(100)

    def selectInputFolder(self):
        inputfolder = QFileDialog.getExistingDirectory()
        self.lineeditFilePath.setText(inputfolder)

    def selectOutputFolder(self):
        outputfolder = QFileDialog.getExistingDirectory()
        self.lineEditOutputFolder.setText (outputfolder)

    def writedata(self,ws,tableParameter=None):
        if(tableParameter is None):
            tableParameter = self.tableParameterOscilogram

        #write the data of the meditions into the stylesheet of excell ws
        styleheader = xlwt.easyxf('font: name Times New Roman, color-index black, bold on, height 300')
        stylebody = xlwt.easyxf('font: name Times New Roman, color-index black, height 220', num_format_str='#,##0.00')
        stylecopyrigth = xlwt.easyxf('font: name Arial, color-index pale_blue, height 250, italic on', num_format_str='#,##0.00')
        spectralparamsTomeasure = self.getspectralParameters(self.spectralMeasurementLocation)
        columnNames = [x[0] for x in self.temporalParameters if x[1]]
        columnNames.extend([label[0] for label in spectralparamsTomeasure])
        for index,header in enumerate(columnNames):
            ws.write(0, index, header,styleheader)
        for i in range(1,tableParameter.model().rowCount()+1):
            for j in range(tableParameter.model().columnCount()):
                ws.write(i, j, str(tableParameter.item(i-1, j).data(Qt.DisplayRole).toString()),stylebody)
        ws.write(tableParameter.model().rowCount()+3,0,"Duetto Sound Lab Oscilogram Meditions",stylecopyrigth)

    def setSettings(self,elementsDetectorDialog):
        elementsDetectorDialog.load_Theme(self.theme)

        elementsDetectorDialog.dsbxThreshold.setValue(self.detectionSettings["Threshold"])
        elementsDetectorDialog.sbxSoftFactor.setValue(self.detectionSettings["SoftFactor"])
        elementsDetectorDialog.dsbxMinSize.setValue(self.detectionSettings["MinSize"])
        elementsDetectorDialog.dsbxThreshold2.setValue(self.detectionSettings["Threshold2"])
        elementsDetectorDialog.dsbxMergeFactor.setValue(self.detectionSettings["MergeFactor"])
        elementsDetectorDialog.dsbxDecay.setValue(self.detectionSettings["Decay"])
        #specgram settings
        elementsDetectorDialog.dsbxThresholdSpec.setValue(self.detectionSettings["ThresholdSpectral"])
        elementsDetectorDialog.dsbxMinSizeFreq.setValue(self.detectionSettings["minSizeFreqSpectral"])
        elementsDetectorDialog.dsbxminSizeTime.setValue(self.detectionSettings["minSizeTimeSpectral"])
        elementsDetectorDialog.spbxSpectralLocMeasureThreshold.setValue(self.detectionSettings["SpectralLocMeasureThreshold"])
        elementsDetectorDialog.spbxPeaksThreshold.setValue(self.detectionSettings["PeaksThreshold"])

        #parameters
        elementsDetectorDialog.cbxStartTime.setChecked(self.temporalParameters[0][1])#start time
        elementsDetectorDialog.cbxEndTime.setChecked(self.temporalParameters[1][1])#end time
        elementsDetectorDialog.cbxPeekToPeek.setChecked(self.temporalParameters[2][1])#peek to peek
        elementsDetectorDialog.cbxRms.setChecked(self.temporalParameters[3][1])#rms
        elementsDetectorDialog.cbxStartToMax.setChecked(self.temporalParameters[4][1])#distance to max
        elementsDetectorDialog.cbxDuration.setChecked(self.temporalParameters[5][1])#duration
        elementsDetectorDialog.cbxSpectralElems.setChecked(self.temporalParameters[6][1])#duration


        elementsDetectorDialog.cbxMaxFreq.setChecked(self.spectralParameters[0][1])#max freq
        elementsDetectorDialog.cbxMinFreq.setChecked(self.spectralParameters[1][1])#min freq
        elementsDetectorDialog.cbxPeakFreq.setChecked(self.spectralParameters[2][1])#peak freq

        elementsDetectorDialog.cbxPeakAmplitude.setChecked(self.spectralParameters[3][1])#peaak amplitude
        elementsDetectorDialog.cbxBandWidth.setChecked(self.spectralParameters[4][1])#band width
        elementsDetectorDialog.cbxPeaksAbove.setChecked(self.spectralParameters[5][1])#peaks above

        #measurements
        elementsDetectorDialog.cbxmeasurementLocationStart.setChecked(self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.START][0])#start medition
        elementsDetectorDialog.cbxmeasurementLocationEnd.setChecked(self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.END][0])#end medition
        elementsDetectorDialog.cbxmeasurementLocationCenter.setChecked(self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.CENTER][0])#center medition
        elementsDetectorDialog.cbxmeasurementLocationQuartile25.setChecked(self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.QUARTILE25][0])#25 % medition
        elementsDetectorDialog.cbxmeasurementLocationQuartile75.setChecked(self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.QUARTILE75][0])#75 % medition

    def getSettings(self,elementsDetectorDialog):
        self.detectionSettings["Threshold"] = elementsDetectorDialog.dsbxThreshold.value()
        self.detectionSettings["Threshold2"] = elementsDetectorDialog.dsbxThreshold2.value()
        self.detectionSettings["MinSize"] = elementsDetectorDialog.dsbxMinSize.value()
        self.detectionSettings["MergeFactor"] = elementsDetectorDialog.dsbxMergeFactor.value()
        self.detectionSettings["SoftFactor"] = elementsDetectorDialog.sbxSoftFactor.value()
        self.detectionSettings["Decay"] = elementsDetectorDialog.dsbxDecay.value()
        #spectral
        self.detectionSettings["ThresholdSpectral"] = elementsDetectorDialog.dsbxThresholdSpec.value()
        self.detectionSettings["minSizeFreqSpectral"] = elementsDetectorDialog.dsbxMinSizeFreq.value()
        self.detectionSettings["minSizeTimeSpectral"] = elementsDetectorDialog.dsbxminSizeTime.value()
        self.detectionSettings["SpectralLocMeasureThreshold"] = elementsDetectorDialog.spbxSpectralLocMeasureThreshold.value()
        self.detectionSettings["PeaksThreshold"] = elementsDetectorDialog.spbxPeaksThreshold.value()
        self.updateThresholdLine()
        #parameters
        self.temporalParameters[0][1] = elementsDetectorDialog.cbxStartTime.isChecked()
        self.temporalParameters[1][1] = elementsDetectorDialog.cbxEndTime.isChecked()#end time
        self.temporalParameters[2][1] = elementsDetectorDialog.cbxPeekToPeek.isChecked()#peek to peek
        self.temporalParameters[3][1] = elementsDetectorDialog.cbxRms.isChecked()#rms
        self.temporalParameters[4][1] = elementsDetectorDialog.cbxStartToMax.isChecked()#distance to max
        self.temporalParameters[5][1] = elementsDetectorDialog.cbxDuration.isChecked()#duratio
        self.temporalParameters[6][1] = elementsDetectorDialog.cbxSpectralElems.isChecked()#duratio


        self.spectralParameters[0][1] = elementsDetectorDialog.cbxMaxFreq.isChecked()#max freq
        self.spectralParameters[1][1] = elementsDetectorDialog.cbxMinFreq.isChecked()#min freq
        self.spectralParameters[2][1] = elementsDetectorDialog.cbxPeakFreq.isChecked()#peak freq
        self.spectralParameters[3][1] = elementsDetectorDialog.cbxPeakAmplitude.isChecked()#peaak amplitude
        self.spectralParameters[4][1] = elementsDetectorDialog.cbxBandWidth.isChecked()#band width
        self.spectralParameters[5][1] = elementsDetectorDialog.cbxPeaksAbove.isChecked()#peak above

        #measurements
        self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.START][0] = elementsDetectorDialog.cbxmeasurementLocationStart.isChecked()#start medition
        self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.END][0]  = elementsDetectorDialog.cbxmeasurementLocationEnd.isChecked()#end medition
        self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.CENTER][0]  = elementsDetectorDialog.cbxmeasurementLocationCenter.isChecked()#center medition
        self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.QUARTILE25][0]  = elementsDetectorDialog.cbxmeasurementLocationQuartile25.isChecked()#25 % medition
        self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.QUARTILE75][0]  = elementsDetectorDialog.cbxmeasurementLocationQuartile75.isChecked()#75 % medition

    def updateDetectionProgressBar(self, x):
        self.windowProgressDetection.setValue(x)

    @pyqtSlot()
    def on_actionDetection_triggered(self):
        elementsDetectorDialog = ElemDetectSettingsDialog(parent=self)
        self.setSettings(elementsDetectorDialog)

        if elementsDetectorDialog.exec_():
            try:
                self.getSettings(elementsDetectorDialog)
                paramsTomeasure = [x for x in self.temporalParameters if x[1]]

                spectralparamsTomeasure = self.getspectralParameters(self.spectralMeasurementLocation)

                #locations is the amount of measurements to make
                self.windowProgressDetection.resize(self.widget.width()/3, self.windowProgressDetection.size().height())
                self.windowProgressDetection.move(self.widget.x()+self.widget.width()/3,self.widget.y()-self.windowProgressDetection.height()/2 + self.widget.height()/2)
                self.windowProgressDetection.show()
                self.widget.axesOscilogram.threshold.setValue((10.0**((60+self.detectionSettings["Threshold"])/20.0))*(2**self.widget.signalProcessor.signal.bitDepth)/1000.0)
                self.widget.detectElements(abs(self.detectionSettings["Threshold"]), self.detectionSettings["Decay"],   self.detectionSettings["MinSize"],
                                           self.detectionSettings["SoftFactor"], self.detectionSettings["MergeFactor"], abs(self.detectionSettings["Threshold2"]),
                                           threshold_spectral=self.detectionSettings["ThresholdSpectral"],
                                           minsize_spectral=(self.detectionSettings["minSizeFreqSpectral"],self.detectionSettings["minSizeTimeSpectral"]),
                                           location= self.spectralMeasurementLocation, progress=self.updateDetectionProgressBar, findSpectralSublements = elementsDetectorDialog.cbxSpectralSubelements.isChecked())



                self.tableParameterOscilogram.clear()
                self.tableParameterOscilogram.setRowCount(len(self.widget.Elements))
                self.tableParameterOscilogram.setColumnCount(len(paramsTomeasure) + len(spectralparamsTomeasure))
                columnNames = [label[0] for label in paramsTomeasure]
                columnNames.extend([label[0] for label in spectralparamsTomeasure])
                self.tableParameterOscilogram.setHorizontalHeaderLabels(columnNames)
                self.updateDetectionProgressBar(95)
                for i in range(self.tableParameterOscilogram.rowCount()):
                    for j,prop in enumerate(paramsTomeasure):
                        try:
                            item = QtGui.QTableWidgetItem(str(prop[2](self.widget.Elements[i])))
                            item.setBackgroundColor(self.parameterTable_rowcolor_odd if i%2==0 else self.parameterTable_rowcolor_even)
                        except:
                            item = QtGui.QTableWidgetItem("Error")
                        self.tableParameterOscilogram.setItem(i, j, item)

                    for x,prop in enumerate(spectralparamsTomeasure):
                        try:
                            item = QtGui.QTableWidgetItem(str(prop[1](self.widget.Elements[i],prop[2])))
                            item.setBackgroundColor(self.parameterTable_rowcolor_odd if i%2==0 else self.parameterTable_rowcolor_even)
                        except:
                            item = QtGui.QTableWidgetItem("Error")
                        self.tableParameterOscilogram.setItem(i, len(paramsTomeasure) + x, item)

                self.updateDetectionProgressBar(100)

            except:
                print("some detection errors")
                self.windowProgressDetection.hide()
            self.hist.region.lineMoved()
            self.hist.region.lineMoveFinished()
            self.windowProgressDetection.hide()


    @pyqtSlot()
    def on_actionClear_Meditions_triggered(self):
        self.widget.clearCursors()
        self.widget.visualChanges = True
        self.widget.refresh()
        self.hist.region.lineMoved()
        self.hist.region.lineMoveFinished()


    @QtCore.pyqtSlot()
    def on_actionCombined_triggered(self):
        self.widget.visibleOscilram=True
        self.widget.visibleSpectrogram=True
        self.widget.refresh(dataChanged=False)
        self.hist.region.lineMoved()
        self.hist.region.lineMoveFinished()

    @QtCore.pyqtSlot()
    def on_actionSpectogram_triggered(self):
        self.widget.visibleOscilogram=False
        self.widget.visibleSpectrogram=True
        self.widget.refresh(dataChanged=False)
        self.hist.region.lineMoved()
        self.hist.region.lineMoveFinished()

    @QtCore.pyqtSlot()
    def on_actionOscilogram_triggered(self):
        self.widget.visibleOscilogram=True
        self.widget.visibleSpectrogram=False
        self.widget.refresh(dataChanged=False)
        self.hist.region.lineMoved()
        self.hist.region.lineMoveFinished()

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
