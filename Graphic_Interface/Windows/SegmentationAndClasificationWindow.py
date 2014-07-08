# -*- coding: utf-8 -*-
from math import log10
import os.path
from PyQt4.QtCore import pyqtSlot, Qt
import PyQt4.QtCore as QtCore
from PyQt4 import QtGui
from matplotlib import mlab
import xlwt
from PyQt4.QtGui import QFileDialog, QStandardItemModel, QAbstractItemView
from Duetto_Core.AudioSignals.AudioSignal import AudioSignal
from Duetto_Core.AudioSignals.WavFileSignal import WavFileSignal
from Duetto_Core.Segmentation.Detectors.ElementsDetectors.OneDimensional.OneDimensionalElementsDetector import DetectionType, AutomaticThresholdType, DetectionSettings
from Duetto_Core.Segmentation.Detectors.ElementsDetectors.OneDimensional import OneDimensionalElementsDetector
from Duetto_Core.Segmentation.Elements.Element import Element
from Duetto_Core.SignalProcessors.SignalProcessor import SignalProcessor
from Duetto_Core.SpecgramSettings import SpecgramSettings
from Duetto_Core.Segmentation.Elements.OneDimensionalElement import SpectralMeasurementLocation
from ..Dialogs.elemDetectSettings import ElemDetectSettingsDialog
from Graphic_Interface.Widgets.Tools import Tools
from SegmentationAndClasificationWindowUI import Ui_MainWindow


class SegmentationAndClasificationWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None,signal=None):
        super(QtGui.QMainWindow, self).__init__(parent)
        self.setupUi(self)
        if not signal:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), "Error", "There is no signal to analyze.")
        if len(signal.data) / signal.samplingRate > 60:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), "Error", "The signal has more than 1 min of duration.\n "
                                                                    "Use the splitter to divide it")
            self.close()
            self.rejectSignal = True
            return

        assert isinstance(signal, AudioSignal)
        self.widget.signalProcessor.signal = signal
        if parent is not None:
            self.widget.specgramSettings.NFFT = parent.widget.specgramSettings.NFFT
            self.widget.specgramSettings.overlap = parent.widget.specgramSettings.overlap
            self.widget.specgramSettings.window = parent.widget.specgramSettings.window
            self.widget.specgramSettings.visualOverlap = parent.widget.specgramSettings.visualOverlap
            if self.widget.specgramSettings.overlap < 0:
                if parent.widget.specgramSettings.visualOverlap < parent.widget.specgramSettings.NFFT:
                    self.widget.specgramSettings.overlap = parent.widget.specgramSettings.visualOverlap * 100.0 / parent.widget.specgramSettings.NFFT
                else:
                    self.widget.specgramSettings.overlap = 50

        self.widget.mainCursor.min = 0
        self.widget.mainCursor.max = len(self.widget.signalProcessor.signal.data)

        self.widget.computeSpecgramSettings()

        self.widget.visibleOscilogram = True
        self.widget.visibleSpectrogram = True

        self.widget.refresh()

        self.rejectSignal = False
        self.widget.mainCursor.min, self.widget.mainCursor.max = 0, len(self.widget.signalProcessor.signal.data)
        self.dockWidgetParameterTableOscilogram.setVisible(False)
        self.tableParameterOscilogram.resizeColumnsToContents()
        self.tableParameterOscilogram.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.show()

        self.parameterTable_rowcolor_odd,self.parameterTable_rowcolor_even = QtGui.QColor(0, 0, 255,150),QtGui.QColor(0, 255, 0, 150)
        self.algorithmDetectorSettings = DetectionSettings(DetectionType.Envelope_Abs_Decay_Averaged,AutomaticThresholdType.Global_MaxMean)

        self.spectralMeasurementLocation = SpectralMeasurementLocation()
        self.widget.axesOscilogram.threshold.sigPositionChangeFinished.connect(self.updateThreshold)
        self.widget.axesOscilogram.threshold.setBounds((-2**(self.widget.signalProcessor.signal.bitDepth-1),2**(self.widget.signalProcessor.signal.bitDepth-1)))
        self.detectionSettings = {"Threshold": -40, "Threshold2": 0, "MergeFactor": 5, "MinSize": 1, "Decay": 1,
                                  "SoftFactor": 6,"ThresholdSpectral": 95 ,"minSizeTimeSpectral": 0, "minSizeFreqSpectral": 0,
                                  "SpectralLocMeasureThreshold": -20,"PeaksThreshold": -20}
        self.noParametrizedmeditions = \
        [
                      ["Start(s)", True, lambda x,d: x.startTime()],
                      ["End(s)", True, lambda x,d: x.endTime()],
                      ["PeekToPeek(V)", False, lambda x,d: x.peekToPeek()],
                      ["RMS(V)", False, lambda x,d: x.rms()],
                      ["StartToMax(s)", False,lambda x,d: x.distanceFromStartToMax()],
                      ["Duration(s)", True,lambda x,d: x.duration()],
                      ["Spectral Elems", False,lambda x,d: x.spectralElements()],
                      ["Peak Freq Average(Hz)", False,lambda x,d: x.peakFreqAverage()],
                      ["Min Freq Average(Hz)", False,lambda x,d: x.minFreqAverage(d)],
                      ["Max Freq Average(Hz)", False,lambda x,d: x.maxFreqAverage(d)]


        ]
        self.parametrizedMeditions = [
            ["Max Freq(Hz)",False,lambda x,d :x.maxFreq(d)],
            ["Min Freq(Hz)",False,lambda x,d :x.minFreq(d)],
            ["Peak Freq(Hz)",False,lambda x,d :x.peakFreq(d)],
            ["Peak Amplitude(dB)",False,lambda x,d :x.peakAmplitude(d)],
            ["Band Width(Hz)",False,lambda x,d :x.bandwidth(d)],
            ["Peaks Above",False,lambda x,d :x.peaksAbove(d)],


        ] #the spectral parameters that changes in function of the location measurements
         #funciones que reciben un elemento spectral 2 dimensiones y devuelven el valor del parametro medido
        #the order of the elements in the array of self.parameterMeasurement["Temporal"] is relevant for the visualization in the table and the
        #binding to the checkboxes in the dialog of parameter measurement
        self.widget.axesSpecgram.PointerSpecChanged.connect(self.updateStatusBar)
        self.widget.axesOscilogram.PointerOscChanged.connect(self.updateStatusBar)
        separator = QtGui.QAction(self)
        separator.setSeparator(True)
        separator1 = QtGui.QAction(self)
        separator1.setSeparator(True)
        separator2 = QtGui.QAction(self)
        separator2.setSeparator(True)
        separator3 = QtGui.QAction(self)
        separator3.setSeparator(True)
        self.widget.createContextCursor([self.actionZoomIn,self.actionZoom_out,self.actionZoom_out_entire_file,separator1,self.actionCombined,self.actionOscilogram,self.actionSpectogram,
                                         separator,self.actionClear_Meditions,self.actionMeditions,self.actionView_Parameters,separator2,
                                         self.actionZoom_Cursor,self.actionPointer_Cursor,self.actionRectangular_Cursor,self.actionRectangular_Eraser,
                                         separator3,self.actionDelete_Selected_Elements,self.actionOsgram_Image,self.actionSpecgram_Image,self.actionCombined_Image])
        self.windowProgressDetection = QtGui.QProgressBar(self.widget)
        self.actionSignalName.setText(self.widget.signalName())
        self.widget.histogram.setImageItem(self.widget.axesSpecgram.imageItem)


    @pyqtSlot()
    def on_actionDelete_Selected_Elements_triggered(self):
        indx = self.widget.deleteSelectedElements()
        if indx is not None:
            pass        #delete from table

    @pyqtSlot()
    def on_actionDeselect_Elements_triggered(self):
        self.widget.selectElement()
        self.widget.clearZoomCursor()

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

    def updateStatusBar(self,line):
        self.statusbar.showMessage(line)

    @QtCore.pyqtSlot(int)
    def on_horizontalScrollBar_valueChanged(self, value):
        self.widget.changeRange(value, value + self.horizontalScrollBar.pageStep(), emit=False)


    @pyqtSlot()
    def on_actionFull_Screen_triggered(self):
        if self.actionFull_Screen.isChecked():
            self.showFullScreen()
        else:
            self.showNormal()

    #region Tools
    @pyqtSlot()
    def on_actionZoom_Cursor_triggered(self):
        if self.actionZoom_Cursor.isChecked():
            self.actionPointer_Cursor.setChecked(False)
            self.actionRectangular_Cursor.setChecked(False)
            self.actionRectangular_Eraser.setChecked(False)
            self.widget.setSelectedTool(Tools.Zoom)
        else:
            self.actionZoom_Cursor.setChecked(True)

    @pyqtSlot()
    def on_actionPointer_Cursor_triggered(self):
        if self.actionPointer_Cursor.isChecked():
            self.actionZoom_Cursor.setChecked(False)
            self.actionRectangular_Cursor.setChecked(False)
            self.actionRectangular_Eraser.setChecked(False)
            self.widget.setSelectedTool(Tools.PointerCursor)
        else:
            self.actionPointer_Cursor.setChecked(True)

    @pyqtSlot()
    def on_actionRectangular_Cursor_triggered(self):
        if self.actionRectangular_Cursor.isChecked():
            self.actionPointer_Cursor.setChecked(False)
            self.actionZoom_Cursor.setChecked(False)
            self.actionRectangular_Eraser.setChecked(False)
            self.widget.setSelectedTool(Tools.RectangularCursor)
        else:
            self.actionRectangular_Cursor.setChecked(True)

    @pyqtSlot()
    def on_actionRectangular_Eraser_triggered(self):
        if self.actionRectangular_Eraser.isChecked():
            self.actionZoom_Cursor.setChecked(False)
            self.actionPointer_Cursor.setChecked(False)
            self.actionRectangular_Cursor.setChecked(False)
            self.widget.setSelectedTool(Tools.RectangularEraser)
        else:
            self.actionRectangular_Eraser.setChecked(True)

    #endregion

    #region Threshold

    def getspectralParameters(self, spectralMeasurementLocation):
        """
        obtain the methods for spectral parameter meausrement of the measurementLocations
        """
        params = []
        threshold = self.detectionSettings["SpectralLocMeasureThreshold"]
        peaksThreshold = self.detectionSettings["PeaksThreshold"]
        if spectralMeasurementLocation.MEDITIONS[spectralMeasurementLocation.START][0]:
            for p in self.parametrizedMeditions:
                if p[1]:
                    params.append([p[0]+"(start)", p[2], {"location": spectralMeasurementLocation.START, "threshold": threshold, "peaksThreshold": peaksThreshold}])
        if spectralMeasurementLocation.MEDITIONS[spectralMeasurementLocation.CENTER][0]:
            for p in self.parametrizedMeditions:
                if p[1]:
                    params.append([p[0]+"(center)", p[2], {"location": spectralMeasurementLocation.CENTER, "threshold": threshold, "peaksThreshold": peaksThreshold}])
        if spectralMeasurementLocation.MEDITIONS[spectralMeasurementLocation.END][0]:
            for p in self.parametrizedMeditions:
                if p[1]:
                    params.append([p[0]+"(end)", p[2], {"location": spectralMeasurementLocation.END, "threshold": threshold, "peaksThreshold": peaksThreshold}])
        if spectralMeasurementLocation.MEDITIONS[spectralMeasurementLocation.QUARTILE25][0]:
            for p in self.parametrizedMeditions:
                if p[1]:
                    params.append([p[0]+"(quartile25)", p[2], {"location": spectralMeasurementLocation.QUARTILE25, "threshold": threshold, "peaksThreshold": peaksThreshold}])
        if spectralMeasurementLocation.MEDITIONS[spectralMeasurementLocation.QUARTILE75][0]:
            for p in self.parametrizedMeditions:
                if p[1]:
                    params.append([p[0]+"(quartile75)",p[2], {"location": spectralMeasurementLocation.QUARTILE75, "threshold": threshold, "peaksThreshold": peaksThreshold}])
        return params

    def updateThreshold(self,line):
        self.detectionSettings["Threshold"] = self.toDB() if line.value() == 0 else self.toDB(line.value())

    def updateThresholdLine(self):
        self.widget.axesOscilogram.threshold.setValue(round((10.0**((60+self.detectionSettings["Threshold"])/20.0))*(2**self.widget.signalProcessor.signal.bitDepth)/1000.0,0)
                                                      *self.widget.envelopeFactor-2**(self.widget.signalProcessor.signal.bitDepth-1))

    def toDB(self,value=None):
        if value is None:
            return -60
        return -60 + int(20*log10(abs((value+2**(self.widget.signalProcessor.signal.bitDepth-1))/self.widget.envelopeFactor)*1000.0/(2**self.widget.signalProcessor.signal.bitDepth)))

    @pyqtSlot(bool)
    def setVisibleThreshold(self,bool):
        self.widget.axesOscilogram.setVisibleThreshold(bool)
        self.widget.setEnvelopeVisibility(bool)

    #endregion

    #region Theme

    def load_Theme(self,theme):
        self.theme = theme
        self.widget.load_Theme(theme)
        #self.tableParameterOscilogram.setStyleSheet("background-color: #" +str(self.widget.osc_background) + ";")

    #endregion

    #region Visual Elements
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

        self.actionTemporal_Figures.setEnabled(visibility)
        self.actionTemporal_Numbers.setEnabled(visibility)

    @pyqtSlot()
    def on_actionTemporal_Numbers_triggered(self):
        visibility = self.actionTemporal_Numbers.isChecked()
        self.widget.changeElementsVisibility(visibility,Element.Text)

    @pyqtSlot()
    def on_actionSpectral_Numbers_triggered(self):
        visibility = self.actionSpectral_Numbers.isChecked()
        self.widget.changeElementsVisibility(visibility,Element.Text,oscilogramItems=False)

    @pyqtSlot()
    def on_actionSpectral_Figures_triggered(self):
        visibility = self.actionSpectral_Figures.isChecked()
        self.widget.changeElementsVisibility(visibility,Element.Figures,oscilogramItems=False)

    @pyqtSlot()
    def on_actionTemporal_Figures_triggered(self):
        visibility = self.actionTemporal_Figures.isChecked()
        self.widget.changeElementsVisibility(visibility,Element.Figures,oscilogramItems=True)

    @pyqtSlot()
    def on_actionSpectral_Elements_triggered(self):
        visibility = self.actionSpectral_Elements.isChecked()
        for e in self.widget.Elements:
            for e2 in e.twoDimensionalElements:
                e2.visible = visibility
        self.widget.drawElements(oscilogramItems=False)
        self.actionSpectral_Figures.setEnabled(visibility)
        self.actionSpectral_Numbers.setEnabled(visibility)
        self.actionSub_Elements_Peaks.setEnabled(visibility)


    #endregion

    #region Graphs Images
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
        fname = unicode(QFileDialog.getSaveFileName(self,"Save "+ text +" as an Image ",str(self.widget.signalName())+"-"+text+"-Duetto-Image","*.jpg"))
        if fname:
            #save as image
            image = QtGui.QPixmap.grabWindow(widget.winId())
            image.save(fname, 'jpg')

    #endregion

    #region Save Meditions, Excell and Batch Process
    @pyqtSlot()
    def on_actionMeditions_triggered(self, name="",table = None):
        if name != "":
            fname = name
        else:
            if not self.widget.signalProcessor.signal.opened():
                return
            fname = unicode(QFileDialog.getSaveFileName(self,"Save meditions as excel file",self.widget.signalName()+".xls","*.xls"))
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
                    self.listwidgetProgress.addItem("Processing "+signalProcessor.signal.name)

                    table = QtGui.QTableWidget()
                    spSettngs = SpecgramSettings(self.widget.specgramSettings.NFFT,self.widget.specgramSettings.overlap,self.widget.specgramSettings.window)
                    spSettngs.Pxx,spSettngs.freqs,spSettngs.bins = self.getSpectralData(signalProcessor.signal,self.widget.specgramSettings)

                    detector.detect(signalProcessor.signal,0,len(signalProcessor.signal.data),threshold=abs(self.detectionSettings["Threshold"]),
                                    decay=self.detectionSettings["Decay"], minSize=  self.detectionSettings["MinSize"],
                                           softfactor=self.detectionSettings["SoftFactor"], merge_factor=self.detectionSettings["MergeFactor"],
                                           secondThreshold=abs(self.detectionSettings["Threshold2"]),
                                           specgramSettings=spSettngs,
                                           detectionsettings=self.algorithmDetectorSettings,
                                           threshold_spectral=self.detectionSettings["ThresholdSpectral"],
                                           minsize_spectral=(self.detectionSettings["minSizeFreqSpectral"],self.detectionSettings["minSizeTimeSpectral"]),
                                           location= self.spectralMeasurementLocation,
                                           findSpectralSublements=False)

                    paramsTomeasure = [x for x in self.noParametrizedmeditions if x[1]]
                    spectralparamsTomeasure = self.getspectralParameters(self.spectralMeasurementLocation)

                    table.setRowCount(detector.elementCount())

                    table.setColumnCount(len(paramsTomeasure) + len(spectralparamsTomeasure))
                    columnNames = [label[0] for label in paramsTomeasure]
                    columnNames.extend([label[0] for label in spectralparamsTomeasure])
                    table.setHorizontalHeaderLabels(columnNames)
                    self.tableParameterOscilogram.resizeColumnsToContents()

                    self.listwidgetProgress.addItem("Save data of " +signalProcessor.signal.name)

                    for i,element in enumerate(detector.elements()):
                        for j,prop in enumerate(paramsTomeasure):
                            item = QtGui.QTableWidgetItem(str(prop[2](element,{"threshold": self.detectionSettings["SpectralLocMeasureThreshold"]})))
                            table.setItem(i, j, item)
                        for x,prop in enumerate(spectralparamsTomeasure):
                            item = QtGui.QTableWidgetItem(str(prop[1](element,prop[2])))
                            item.setBackgroundColor(self.parameterTable_rowcolor_odd if i%2==0 else self.parameterTable_rowcolor_even)
                            table.setItem(i, len(paramsTomeasure) + x, item)
                    if singlefile:
                        ws = wb.add_sheet(signalProcessor.signal.name)
                        self.writedata(ws,table)
                    else:
                        self.on_actionMeditions_triggered(os.path.join(directoryoutput,signalProcessor.signal.name+".xls"),table)
                    self.listwidgetProgress.addItem(signalProcessor.signal.name+" has been processed")
                    self.listwidgetProgress.update()
                    processed += 1
                except:
                    self.listwidgetProgress.addItem("Some problem found while processing ")
                self.progressBarProcesed.setValue(round(100.0*(processed)/len(sounds)))
                self.progressBarProcesed.update()
                #valorar si ya existe el fichero reescribirlo o guardalo con otro nombre
                if singlefile:
                    wb.save(os.path.join(directoryoutput,"Duetto Sound Lab Meditions.xls"))
            #open folder
        if self.rbttnSplitFile.isChecked():
            save = WavFileSignal()
            for filename in sounds:
                try:
                    signal = WavFileSignal(filename)
                    self.listwidgetProgress.addItem("Processing "+signal.name)
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
                            save.save(os.path.join(directoryoutput,str(i+1)+"-"+signal.name))
                    if left > 0:
                        save.data = signal.data[len(signal.data)-left:]
                        save.save(os.path.join(directoryoutput,str(pieces+1)+"-"+signal.name))
                    processed += 1
                    self.progressBarProcesed.setValue(100.0*processed/len(sounds))
                    self.listwidgetProgress.addItem(signal.name+" has been processed")
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
        columnNames = [x[0] for x in self.noParametrizedmeditions if x[1]]
        columnNames.extend([label[0] for label in spectralparamsTomeasure])
        for index,header in enumerate(columnNames):
            ws.write(0, index, header,styleheader)
        for i in range(1,tableParameter.model().rowCount()+1):
            for j in range(tableParameter.model().columnCount()):
                ws.write(i, j, str(tableParameter.item(i-1, j).data(Qt.DisplayRole).toString()),stylebody)
        ws.write(tableParameter.model().rowCount()+3,0,"Duetto Sound Lab Oscilogram Meditions",stylecopyrigth)

    #endregion

    #region Detection
    def setSettings(self,elementsDetectorDialog):
        elementsDetectorDialog.load_Theme(self.theme)
        elementsDetectorDialog.dsbxThreshold.setValue(self.detectionSettings["Threshold"])
        elementsDetectorDialog.sbxSoftFactor.setValue(self.detectionSettings["SoftFactor"])
        elementsDetectorDialog.dsbxMinSize.setValue(self.detectionSettings["MinSize"])
        elementsDetectorDialog.dsbxThreshold2.setValue(self.detectionSettings["Threshold2"])
        elementsDetectorDialog.dsbxMergeFactor.setValue(self.detectionSettings["MergeFactor"])
        elementsDetectorDialog.dsbxDecay.setValue(self.detectionSettings["Decay"])
        elementsDetectorDialog.detectionSettings =  self.algorithmDetectorSettings
        elementsDetectorDialog.cmbxDetectionMethod.setCurrentIndex(self.algorithmDetectorSettings.detectiontype)
        #specgram settings
        elementsDetectorDialog.dsbxThresholdSpec.setValue(self.detectionSettings["ThresholdSpectral"])
        elementsDetectorDialog.dsbxMinSizeFreq.setValue(self.detectionSettings["minSizeFreqSpectral"])
        elementsDetectorDialog.dsbxminSizeTime.setValue(self.detectionSettings["minSizeTimeSpectral"])
        elementsDetectorDialog.spbxSpectralLocMeasureThreshold.setValue(self.detectionSettings["SpectralLocMeasureThreshold"])
        elementsDetectorDialog.spbxPeaksThreshold.setValue(self.detectionSettings["PeaksThreshold"])

        #parameters
        elementsDetectorDialog.cbxStartTime.setChecked(self.noParametrizedmeditions[0][1])#start time
        elementsDetectorDialog.cbxEndTime.setChecked(self.noParametrizedmeditions[1][1])#end time
        elementsDetectorDialog.cbxPeekToPeek.setChecked(self.noParametrizedmeditions[2][1])#peek to peek
        elementsDetectorDialog.cbxRms.setChecked(self.noParametrizedmeditions[3][1])#rms
        elementsDetectorDialog.cbxStartToMax.setChecked(self.noParametrizedmeditions[4][1])#distance to max
        elementsDetectorDialog.cbxDuration.setChecked(self.noParametrizedmeditions[5][1])#duration
        elementsDetectorDialog.cbxSpectralElems.setChecked(self.noParametrizedmeditions[6][1])#spectral elems


        elementsDetectorDialog.cbxMaxFreq.setChecked(self.parametrizedMeditions[0][1])#max freq
        elementsDetectorDialog.cbxMinFreq.setChecked(self.parametrizedMeditions[1][1])#min freq
        elementsDetectorDialog.cbxPeakFreq.setChecked(self.parametrizedMeditions[2][1])#peak freq

        elementsDetectorDialog.cbxPeakAmplitude.setChecked(self.parametrizedMeditions[3][1])#peaak amplitude
        elementsDetectorDialog.cbxBandWidth.setChecked(self.parametrizedMeditions[4][1])#band width
        elementsDetectorDialog.cbxPeaksAbove.setChecked(self.parametrizedMeditions[5][1])#peaks above

        elementsDetectorDialog.widget.histogram.region.setRegion(self.theme.histRange)
        elementsDetectorDialog.widget.histogram.gradient.restoreState(self.theme.colorBarState)



        #measurements
        averageComputation = self.noParametrizedmeditions[7][1] or self.noParametrizedmeditions[8][1] or self.noParametrizedmeditions[9][1]
        elementsDetectorDialog.cbxmeasurementLocationStart.setChecked(self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.START][0])#start medition
        elementsDetectorDialog.cbxmeasurementLocationEnd.setChecked(self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.END][0])#end medition
        elementsDetectorDialog.cbxmeasurementLocationCenter.setChecked(self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.CENTER][0])#center medition
        elementsDetectorDialog.cbxmeasurementLocationQuartile25.setChecked(self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.QUARTILE25][0])#25 % medition
        elementsDetectorDialog.cbxmeasurementLocationQuartile75.setChecked(self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.QUARTILE75][0])#75 % medition
        elementsDetectorDialog.cbxmeasurementLocationAverage.setChecked(averageComputation)#75 % medition


    def getSettings(self,elementsDetectorDialog):
        self.detectionSettings["Threshold"] = elementsDetectorDialog.dsbxThreshold.value()
        self.detectionSettings["Threshold2"] = elementsDetectorDialog.dsbxThreshold2.value()
        self.detectionSettings["MinSize"] = elementsDetectorDialog.dsbxMinSize.value()
        self.detectionSettings["MergeFactor"] = elementsDetectorDialog.dsbxMergeFactor.value()
        self.detectionSettings["SoftFactor"] = elementsDetectorDialog.sbxSoftFactor.value()
        self.detectionSettings["Decay"] = elementsDetectorDialog.dsbxDecay.value()
        self.algorithmDetectorSettings = elementsDetectorDialog.detectionSettings

        #spectral
        self.detectionSettings["ThresholdSpectral"] = elementsDetectorDialog.dsbxThresholdSpec.value()
        self.detectionSettings["minSizeFreqSpectral"] = elementsDetectorDialog.dsbxMinSizeFreq.value()
        self.detectionSettings["minSizeTimeSpectral"] = elementsDetectorDialog.dsbxminSizeTime.value()
        self.detectionSettings["SpectralLocMeasureThreshold"] = elementsDetectorDialog.spbxSpectralLocMeasureThreshold.value()
        self.detectionSettings["PeaksThreshold"] = elementsDetectorDialog.spbxPeaksThreshold.value()
        self.updateThresholdLine()
        #parameters
        self.noParametrizedmeditions[0][1] = elementsDetectorDialog.cbxStartTime.isChecked()
        self.noParametrizedmeditions[1][1] = elementsDetectorDialog.cbxEndTime.isChecked()#end time
        self.noParametrizedmeditions[2][1] = elementsDetectorDialog.cbxPeekToPeek.isChecked()#peek to peek
        self.noParametrizedmeditions[3][1] = elementsDetectorDialog.cbxRms.isChecked()#rms
        self.noParametrizedmeditions[4][1] = elementsDetectorDialog.cbxStartToMax.isChecked()#distance to max
        self.noParametrizedmeditions[5][1] = elementsDetectorDialog.cbxDuration.isChecked()#duratio
        self.noParametrizedmeditions[6][1] = elementsDetectorDialog.cbxSpectralElems.isChecked()#duratio\

        self.noParametrizedmeditions[7][1] = elementsDetectorDialog.cbxPeakFreq.isChecked()#peak freq average
        self.noParametrizedmeditions[8][1] = elementsDetectorDialog.cbxMinFreq.isChecked()#min freq average
        self.noParametrizedmeditions[9][1] = elementsDetectorDialog.cbxMaxFreq.isChecked()#max freq average


        self.parametrizedMeditions[0][1] = elementsDetectorDialog.cbxMaxFreq.isChecked()#max freq
        self.parametrizedMeditions[1][1] = elementsDetectorDialog.cbxMinFreq.isChecked()#min freq
        self.parametrizedMeditions[2][1] = elementsDetectorDialog.cbxPeakFreq.isChecked()#peak freq
        self.parametrizedMeditions[3][1] = elementsDetectorDialog.cbxPeakAmplitude.isChecked()#peaak amplitude
        self.parametrizedMeditions[4][1] = elementsDetectorDialog.cbxBandWidth.isChecked()#band width
        self.parametrizedMeditions[5][1] = elementsDetectorDialog.cbxPeaksAbove.isChecked()#peak above

        #measurements
        self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.START][0] = elementsDetectorDialog.cbxmeasurementLocationStart.isChecked()#start medition
        self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.END][0]  = elementsDetectorDialog.cbxmeasurementLocationEnd.isChecked()#end medition
        self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.CENTER][0]  = elementsDetectorDialog.cbxmeasurementLocationCenter.isChecked()#center medition
        self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.QUARTILE25][0]  = elementsDetectorDialog.cbxmeasurementLocationQuartile25.isChecked()#25 % medition
        self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.QUARTILE75][0]  = elementsDetectorDialog.cbxmeasurementLocationQuartile75.isChecked()#75 % medition

    def updateDetectionProgressBar(self, x):
        self.windowProgressDetection.setValue(x)

    def elementSelectedInTable(self,row,column):
        self.tableParameterOscilogram.selectRow(row)
        self.widget.selectElement(row)#select the correct element in oscilogram

    @pyqtSlot()
    def on_actionDetection_triggered(self):
        elementsDetectorDialog = ElemDetectSettingsDialog(parent=self)
        self.setSettings(elementsDetectorDialog)
        self.widget.selectElement(-1)

        if elementsDetectorDialog.exec_():
            try:

                self.getSettings(elementsDetectorDialog)

                self.actionView_Threshold.setChecked(True)
                paramsTomeasure = [x for x in self.noParametrizedmeditions if x[1]]
                spectralparamsTomeasure = self.getspectralParameters(self.spectralMeasurementLocation)
                self.windowProgressDetection.resize(self.widget.width()/3, self.windowProgressDetection.size().height())
                self.windowProgressDetection.move(self.widget.x()+self.widget.width()/3,self.widget.y()-self.windowProgressDetection.height()/2 + self.widget.height()/2)
                self.windowProgressDetection.show()
                self.widget.detectElements(threshold=abs(self.detectionSettings["Threshold"]),detectionsettings=self.algorithmDetectorSettings,decay= self.detectionSettings["Decay"], minSize= self.detectionSettings["MinSize"],
                                           softfactor=self.detectionSettings["SoftFactor"], merge_factor=self.detectionSettings["MergeFactor"], threshold2= abs(self.detectionSettings["Threshold2"]),
                                           threshold_spectral=self.detectionSettings["ThresholdSpectral"],
                                           minsize_spectral=(self.detectionSettings["minSizeFreqSpectral"],
                                                             self.detectionSettings["minSizeTimeSpectral"]),
                                           location=self.spectralMeasurementLocation,
                                           progress=self.updateDetectionProgressBar,
                                           findSpectralSublements=elementsDetectorDialog.cbxSpectralSubelements.isChecked())

                self.tableParameterOscilogram.clear()
                self.tableParameterOscilogram.cellPressed.connect(self.elementSelectedInTable)
                self.tableParameterOscilogram.setRowCount(len(self.widget.Elements))
                self.tableParameterOscilogram.setColumnCount(len(paramsTomeasure) + len(spectralparamsTomeasure))
                columnNames = [label[0] for label in paramsTomeasure]
                columnNames.extend([label[0] for label in spectralparamsTomeasure])
                self.tableParameterOscilogram.setHorizontalHeaderLabels(columnNames)
                self.updateDetectionProgressBar(95)
                for index in range(len(self.widget.Elements)):
                    self.widget.Elements[index].clicked = lambda ind,buttn: self.elementSelectedInTable(ind,0)

                for i in range(self.tableParameterOscilogram.rowCount()):
                    for j,prop in enumerate(paramsTomeasure):
                        try:
                            item = QtGui.QTableWidgetItem(str(prop[2](self.widget.Elements[i],{"threshold": self.detectionSettings["SpectralLocMeasureThreshold"]})))
                            item.setBackgroundColor(self.parameterTable_rowcolor_odd if i%2==0 else self.parameterTable_rowcolor_even)
                        except:
                            item = QtGui.QTableWidgetItem("Error")
                        self.tableParameterOscilogram.setItem(i, j, item)
                    for x,prop in enumerate(spectralparamsTomeasure):
                        try:
                            item = QtGui.QTableWidgetItem(unicode(prop[1](self.widget.Elements[i],prop[2])))
                            item.setBackgroundColor(self.parameterTable_rowcolor_odd if i%2==0 else self.parameterTable_rowcolor_even)
                        except:
                            item = QtGui.QTableWidgetItem("Error")
                        self.tableParameterOscilogram.setItem(i, len(paramsTomeasure) + x, item)


                self.updateDetectionProgressBar(100)
            except:
                print("some detection errors")
                self.windowProgressDetection.hide()

            self.windowProgressDetection.hide()

    #endregion

    #region Close and Exit
    @pyqtSlot()
    def on_actionExit_triggered(self):
        self.close()



    def closeEvent(self,event):
        if self.widget.signalProcessor.signal.playStatus == AudioSignal.PLAYING or\
                        self.widget.signalProcessor.signal.playStatus == AudioSignal.RECORDING:
            self.widget.stop()
        mbox = QtGui.QMessageBox(QtGui.QMessageBox.Question,"Save meditions","Do you want to save the meditions?",QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel,self)
        if self.tableParameterOscilogram.rowCount() > 0:
            result = mbox.exec_()
            if result == QtGui.QMessageBox.Yes:
                wb = xlwt.Workbook()
                ws = wb.add_sheet(self.widget.signalName())
                self.writedata(ws, self.tableParameterOscilogram)
                fname = unicode(QFileDialog.getSaveFileName(self,"Save meditions as excel file",self.widget.signalName()+".xls","*.xls"))
                if fname:
                    wb.save(fname)
            elif result == QtGui.QMessageBox.Cancel:
                event.ignore()

    #endregion

    #region Time and Frecuency Domain Visualization
    @pyqtSlot()
    def on_actionClear_Meditions_triggered(self):
        self.widget.clearCursors()
        self.widget.selectElement()
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

    #endregion

    #region Sound
    @QtCore.pyqtSlot()
    def on_actionPlay_Sound_triggered(self):
        self.widget.play()

    @QtCore.pyqtSlot()
    def on_actionStop_Sound_triggered(self):
        self.widget.stop()

    @QtCore.pyqtSlot()
    def on_actionPause_Sound_triggered(self):
        self.widget.pause()

    #endregion

    #Zoom

    @QtCore.pyqtSlot()
    def on_actionZoomIn_triggered(self):
        self.widget.zoomIn()

    @QtCore.pyqtSlot()
    def on_actionZoom_out_triggered(self):
        self.widget.zoomOut()

    @QtCore.pyqtSlot()
    def on_actionZoom_out_entire_file_triggered(self):
        self.widget.zoomNone()


