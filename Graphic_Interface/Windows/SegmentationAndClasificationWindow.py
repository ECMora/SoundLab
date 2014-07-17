# -*- coding: utf-8 -*-
from math import log10
import os.path
from PyQt4.QtCore import pyqtSlot, Qt
import PyQt4.QtCore as QtCore
from PyQt4 import QtGui
from matplotlib import mlab
import xlwt
import numpy as np
from PyQt4.QtGui import QFileDialog, QAbstractItemView
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
from Graphic_Interface.Windows.TwoDimensionalAnalisysWindow import TwoDimensionalAnalisysWindow
from SegmentationAndClasificationWindowUI import Ui_MainWindow
from pyqtgraph.parametertree import Parameter, ParameterTree



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
                                  "SoftFactor": 6,"ThresholdSpectral": 95 ,"minSizeTimeSpectral": 0, "minSizeFreqSpectral": 0}

        params = [{u'name': u'Temporal Detection Settings', u'type': u'group', u'children': [
            {u'name': u'Detection Method', u'type': u'list', u'default':DetectionType.Envelope_Abs_Decay_Averaged, u'values':
                [(u'Local Max',DetectionType.LocalMax),
                             (u'Interval Rms',DetectionType.IntervalRms),(u'Interval Max Media',DetectionType.IntervalMaxMedia),
                             (u'Interval Max Proportion',DetectionType.IntervalMaxProportion),
                             (u'Envelope Abs Decay Averaged',DetectionType.Envelope_Abs_Decay_Averaged),(u'Envelope Rms',DetectionType.Envelope_Rms)]},
            {u'name': u'Threshold (db)', u'type': u'float', u'value': -40.00, u'step': 1},
            {u'name': u'Auto', u'type': u'bool',u'default': True, u'value': True},
            {u'name': u'Min Size (ms)', u'type': u'float', u'value': 1.00, u'step': 1},
            {u'name': u'Decay (ms)', u'type': u'float', u'value': 1.00, u'step': 0.5},
            {u'name': u'Threshold 2(db)', u'type': u'float', u'value': 0.00, u'step': 1},
            {u'name': u'Soft Factor', u'type': u'float', u'value': 6, u'step': 1},
            {u'name': u'Merge Factor (%)', u'type': u'float', u'value': 5.00, u'step': 1, u'limits' : (0,50)}
        ]},

        {u'name': u'Spectral Detection Settings', u'type': u'group', u'children': [
            {u'name': u'Detect Spectral Subelements', u'type': u'bool',u'default': False, u'value': False},
            {u'name': u'Threshold (%)', u'type': u'float', u'value': 95.00, u'step': 1, u'limits' : (0,100)},
            {u'name':u'Minimum size', u'type': u'group', u'children': [
                {u'name': u'Time (ms)', u'type': u'float', u'value': 0.00, u'step': 1},
                {u'name': u'Frequency (kHz)', u'type': u'float', u'value': 0.00, u'step': 1}]}
            ]},

         {u'name': u'Measurement Location', u'type': u'group', u'children': [
            {u'name': u'Start', u'type': u'bool',u'default': False, u'value': False},
            {u'name': u'Center', u'type': u'bool',u'default': False, u'value': False},
            {u'name': u'End', u'type': u'bool',u'default': False, u'value': False},
            {u'name': u'Quartile 25', u'type': u'bool',u'default': False, u'value': False},
            {u'name': u'Mean', u'type': u'bool',u'default': False, u'value': False},
            {u'name': u'Quartile 75', u'type': u'bool',u'default': False, u'value': False}]}
        ]

        self.timeMeditions = [
            ["Start(s)", True, lambda x,d: x.startTime()],
            ["End(s)", True, lambda x,d: x.endTime()],
            ["StartToMax(s)", False,lambda x,d: x.distanceFromStartToMax()],
            ["Duration(s)", True,lambda x,d: x.duration()],
        ]

        self.spectralMeditions = [
            ["Spectral Elems", False,lambda x,d: x.spectralElements()],
            ["Peak Freq(Hz)",False,lambda x,d :x.peakFreq(d)],
            ["Peak Amplitude(dB)",False,lambda x,d :x.peakAmplitude(d)],
            ["Frequency",
                [
                    ["Threshold (db)",-20]
                ],
                [
                    ["Min Freq(Hz)",False,lambda x,d :x.minFreq(d)],
                    ["Max Freq(Hz)",False,lambda x,d :x.maxFreq(d)],
                    ["Band Width(Hz)",False,lambda x,d :x.bandwidth(d)]
                ]
            ],
            ["Peaks",
                [
                    ["Threshold (db)",-20]
                ],
                [
                    ["Peaks Above",False,lambda x,d :x.peaksAbove(d)],
                ]
            ]

        ]

        self.waveMeditions = [
            ["PeekToPeek(V)", False, lambda x,d: x.peekToPeek()],
            ["RMS(V)", False, lambda x,d: x.rms()],
        ]

        self.meditions = [( u'Temporal Meditions',self.timeMeditions),(u'Spectral Meditions',self.spectralMeditions),(u'Waveform Meditions',self.waveMeditions)]

        for name,dict in self.meditions:
            children = []
            for x in dict:
                if isinstance(x[1],bool):
                    children.append({u'name': x[0], u'type': u'bool',u'default': x[1], u'value': x[1]})
                else:
                    temp = []
                    for y in x[1]:
                        temp.append({u'name': y[0], u'type': u'float', u'value':y[1], u'step': 0.1})
                    for y in x[2]:
                        temp.append({u'name': y[0], u'type': u'bool',u'default': y[1], u'value': y[1]})
                    children.append({u'name': x[0], u'type': u'group', u'children': temp})
            params.append({u'name': name, u'type': u'group', u'children': children})

        self.ParamTree = Parameter.create(name=u'params', type=u'group', children=params)

        #the spectral parameters that changes in function of the location measurements
        #funciones que reciben un elemento spectral 2 dimensiones y devuelven el valor del parametro medido
        #the order of the elements in the array of self.parameterMeasurement["Temporal"] is relevant for the visualization in the table and the
        #binding to the checkboxes in the dialog of parameter measurement
        self.widget.axesSpecgram.PointerSpecChanged.connect(self.updateStatusBar)
        self.widget.axesOscilogram.PointerOscChanged.connect(self.updateStatusBar)
        separator,separator1,separator2,separator3,separator4 = QtGui.QAction(self),QtGui.QAction(self),\
                                                                QtGui.QAction(self),QtGui.QAction(self),\
                                                                QtGui.QAction(self)

        separator.setSeparator(True)
        separator1.setSeparator(True)
        separator2.setSeparator(True)
        separator3.setSeparator(True)
        separator4.setSeparator(True)


        self.widget.createContextCursor([self.actionZoomIn,self.actionZoom_out,self.actionZoom_out_entire_file,separator1,self.actionCombined,self.actionOscilogram,self.actionSpectogram,
                                         separator,self.actionClear_Meditions,self.actionMeditions,self.actionView_Parameters,separator2,
                                         self.actionZoom_Cursor,self.actionPointer_Cursor,self.actionRectangular_Cursor,self.actionRectangular_Eraser,
                                         separator3,self.actionDeselect_Elements,self.actionDelete_Selected_Elements,separator4,self.actionOsgram_Image,self.actionSpecgram_Image,self.actionCombined_Image])
        self.windowProgressDetection = QtGui.QProgressBar(self.widget)
        self.actionSignalName.setText(self.widget.signalName())

        #array of windows with two dimensional graphs. Are stored for a similar behavior to the one dimensional
        #in the main window. Updates the graphs
        self.twodimensionalGraphs = []


        self.measuredParameters = np.array([[], []]) # stores the measured parameters of the sdetected elements
        #the names of the columns in the table of parameters measured
        self.columnNames = []
        self.widget.histogram.setImageItem(self.widget.axesSpecgram.imageItem)

    #region Two Dimensional Graphs

    @pyqtSlot()
    def on_actionTwo_Dimensional_Graphs_triggered(self):
        if self.tableParameterOscilogram.rowCount() == 0:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), "Error", "There is not detected elements.\n The two dimensional analisys requires at least one detected element.")
            return
        if self.tableParameterOscilogram.columnCount() == 0:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), "Error", "There is not parameters measurement.\n The two dimensional analisys requires at least one parameter measured.")
            return

        wnd = TwoDimensionalAnalisysWindow(self, columns=self.columnNames,data=self.measuredParameters)
        wnd.elementSelected.connect(self.elementSelectedInTable)
        if self.theme:
            wnd.load_Theme(self.theme)

        if len(self.twodimensionalGraphs) > 0:
            wnd.selectElement(self.twodimensionalGraphs[0].previousSelectedElement)

        self.twodimensionalGraphs.append(wnd)


    #endregion

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

    def getspectralParameters(self):
        """
        obtain the methods for spectral parameter meausrement of the measurementLocations
        """
        params = []

        for x in self.spectralMeditions:
            if isinstance(x[1],bool):
                if x[1]:
                    if self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.START][0]:
                        params.append([x[0]+"(start)", x[2], [["location",self.spectralMeasurementLocation.START]]])
                    if self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.CENTER][0]:
                        params.append([x[0]+"(center)", x[2],[["location",self.spectralMeasurementLocation.CENTER]]])
                    if self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.END][0]:
                        params.append([x[0]+"(end)", x[2], [["location",self.spectralMeasurementLocation.END]]])
                    if self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.QUARTILE25][0]:
                        params.append([x[0]+"(quartile25)", x[2],[["location",self.spectralMeasurementLocation.QUARTILE25]]])
                    if self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.QUARTILE75][0]:
                        params.append([x[0]+"(quartile75)", x[2],[["location",self.spectralMeasurementLocation.QUARTILE75]]])
            else:
                for y in x[2]:
                    if y[1]:
                        if self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.START][0]:
                            params.append([y[0]+"(start)", y[2], x[1].append(["location",self.spectralMeasurementLocation.START])])
                        if self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.CENTER][0]:
                            params.append([y[0]+"(center)", y[2],x[1].append(["location",self.spectralMeasurementLocation.CENTER])])
                        if self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.END][0]:
                            params.append([y[0]+"(end)", y[2], x[1].append(["location",self.spectralMeasurementLocation.END])])
                        if self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.QUARTILE25][0]:
                            params.append([y[0]+"(quartile25)", y[2],x[1].append(["location",self.spectralMeasurementLocation.QUARTILE25])])
                        if self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.QUARTILE75][0]:
                            params.append([y[0]+"(quartile75)", y[2],x[1].append(["location",self.spectralMeasurementLocation.QUARTILE75])])

        return params

    def getParameters(self):
         params = []
         for name,dict in self.meditions:
            if not name == u'Spectral Meditions':
                for x in dict:
                    if isinstance(x[1],bool):
                        if x[1]:
                            params.append([x[0], x[2], []])
                    else:
                        for y in x[2]:
                            if y[1]:
                                params.append([y[0], y[2], x[1]])
         return params + self.getspectralParameters()

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

        self.widget.histogram.item.region.lineMoved()
        self.widget.histogram.item.region.lineMoveFinished()

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

                    paramsTomeasure = self.getParameters()


                    table.setRowCount(detector.elementCount())

                    table.setColumnCount(len(paramsTomeasure))
                    self.columnNames = [label[0] for label in paramsTomeasure]


                    table.setHorizontalHeaderLabels(self.columnNames)
                    self.tableParameterOscilogram.resizeColumnsToContents()

                    self.listwidgetProgress.addItem("Save data of " +signalProcessor.signal.name)

                    for i,element in enumerate(detector.elements()):
                        for j,prop in enumerate(paramsTomeasure):
                            item = QtGui.QTableWidgetItem(str(prop[1](element,prop[2])))
                            item.setBackgroundColor(self.parameterTable_rowcolor_odd if i%2==0 else self.parameterTable_rowcolor_even)
                            table.setItem(i, j, item)
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

        for index,header in enumerate(self.columnNames):
            ws.write(0, index, header,styleheader)
        for i in range(1,tableParameter.model().rowCount()+1):
            for j in range(tableParameter.model().columnCount()):
                ws.write(i, j, str(tableParameter.item(i-1, j).data(Qt.DisplayRole).toString()),stylebody)
        ws.write(tableParameter.model().rowCount()+3,0,"Duetto Sound Lab Oscilogram Meditions",stylecopyrigth)

    #endregion

    #region Detection

    def getSettings(self,elementsDetectorDialog):

        self.detectionSettings["Threshold"] = self.ParamTree.param(u'Temporal Detection Settings').param(u'Threshold (db)').value()
        self.detectionSettings["Threshold2"] = self.ParamTree.param(u'Temporal Detection Settings').param(u'Threshold 2(db)').value()
        self.detectionSettings["MinSize"] = self.ParamTree.param(u'Temporal Detection Settings').param(u'Min Size (ms)').value()
        self.detectionSettings["MergeFactor"] = self.ParamTree.param(u'Temporal Detection Settings').param(u'Merge Factor (%)').value()
        self.detectionSettings["SoftFactor"] = self.ParamTree.param(u'Temporal Detection Settings').param(u'Soft Factor').value()
        self.detectionSettings["Decay"] = self.ParamTree.param(u'Temporal Detection Settings').param(u'Decay (ms)').value()
        self.algorithmDetectorSettings = elementsDetectorDialog.detectionSettings

        #spectral
        self.detectionSettings["ThresholdSpectral"] = self.ParamTree.param(u'Spectral Detection Settings').param(u'Threshold (%)').value()
        self.detectionSettings["minSizeFreqSpectral"] = self.ParamTree.param(u'Spectral Detection Settings').param(u'Minimum size').param(u'Frequency (kHz)').value()
        self.detectionSettings["minSizeTimeSpectral"] = self.ParamTree.param(u'Spectral Detection Settings').param(u'Minimum size').param(u'Time (ms)').value()
        self.updateThresholdLine()
        #parameters


        for name,dict in self.meditions:
            for x in dict:
                if isinstance(x[1],bool):
                    x[1] = self.ParamTree.param(name).param(x[0]).value()
                else:
                    for y in x[1]:
                        y[1] = self.ParamTree.param(name).param(x[0]).param(y[0]).value()
                    for y in x[2]:
                        y[1] = self.ParamTree.param(name).param(x[0]).param(y[0]).value()

        #measurements u'Measurement Location'
        self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.START][0] = self.ParamTree.param(u'Measurement Location').param(u'Start').value()
        self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.END][0]  = self.ParamTree.param(u'Measurement Location').param(u'End').value()
        self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.CENTER][0]  = self.ParamTree.param(u'Measurement Location').param(u'Center').value()
        self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.QUARTILE25][0]  = self.ParamTree.param(u'Measurement Location').param(u'Quartile 25').value()
        self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.QUARTILE75][0]  = self.ParamTree.param(u'Measurement Location').param( u'Quartile 75').value()


    def updateDetectionProgressBar(self, x):
        self.windowProgressDetection.setValue(x)

    def elementSelectedInTable(self,row,column=0):
        self.tableParameterOscilogram.selectRow(row)
        self.widget.selectElement(row)#select the correct element in oscilogram
        for wnd in self.twodimensionalGraphs:
            wnd.selectElement(row)

    @pyqtSlot()
    def on_actionDetection_triggered(self):
        elementsDetectorDialog = ElemDetectSettingsDialog(parent=self,paramTree=self.ParamTree)
        elementsDetectorDialog.load_Theme(self.theme)
        self.widget.selectElement(-1)

        if elementsDetectorDialog.exec_():
            try:

                self.getSettings(elementsDetectorDialog)

                self.actionView_Threshold.setChecked(True)
                paramsTomeasure = self.getParameters()

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
                                           findSpectralSublements= self.ParamTree.param(u'Spectral Detection Settings').param(u'Detect Spectral Subelements').value())


                self.tableParameterOscilogram.clear()
                self.tableParameterOscilogram.cellPressed.connect(self.elementSelectedInTable)
                self.tableParameterOscilogram.setRowCount(len(self.widget.Elements))
                self.tableParameterOscilogram.setColumnCount(len(paramsTomeasure))
                self.columnNames = [label[0] for label in paramsTomeasure]
                self.tableParameterOscilogram.setHorizontalHeaderLabels(self.columnNames)
                self.updateDetectionProgressBar(95)


                #for select the element in the table. Binding for the element click to the table
                for index in range(len(self.widget.Elements)):
                    self.widget.Elements[index].elementClicked.connect(self.elementSelectedInTable)

                #the table of parameters stored as a numpy array
                self.measuredParameters = np.zeros(len(self.widget.Elements)*len(self.columnNames)).reshape((len(self.widget.Elements),len(self.columnNames)))

                for i in range(self.tableParameterOscilogram.rowCount()):
                    for j,prop in enumerate(paramsTomeasure):
                        try:
                            self.measuredParameters[i,j] = prop[1](self.widget.Elements[i],prop[2])
                            item = QtGui.QTableWidgetItem(unicode(self.measuredParameters[i,j]))
                            item.setBackgroundColor(self.parameterTable_rowcolor_odd if i%2==0 else self.parameterTable_rowcolor_even)
                        except Exception as e:
                            item = QtGui.QTableWidgetItem("Error"+e.message)
                        self.tableParameterOscilogram.setItem(i, j, item)


                self.updateDetectionProgressBar(100)

                for wnd in self.twodimensionalGraphs:
                    wnd.loadData(self.columnNames,self.measuredParameters)

            except Exception:
                print("some detection errors")

            self.widget.refresh()

            self.windowProgressDetection.hide()

    #endregion

    #region Zoom

    @QtCore.pyqtSlot()
    def on_actionZoomIn_triggered(self):
        self.widget.zoomIn()

    @QtCore.pyqtSlot()
    def on_actionZoom_out_triggered(self):
        self.widget.zoomOut()

    @QtCore.pyqtSlot()
    def on_actionZoom_out_entire_file_triggered(self):
        self.widget.zoomNone()

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
            if result == QtGui.QMessageBox.Cancel:
                event.ignore()
                return
            elif result == QtGui.QMessageBox.Yes:
                wb = xlwt.Workbook()
                ws = wb.add_sheet(self.widget.signalName())
                self.writedata(ws, self.tableParameterOscilogram)
                fname = unicode(QFileDialog.getSaveFileName(self,"Save meditions as excel file",self.widget.signalName()+".xls","*.xls"))
                if fname:
                    wb.save(fname)
            for w in self.twodimensionalGraphs:
                w.close()


    #endregion

    #region Time and Frecuency Domain Visualization
    @pyqtSlot()
    def on_actionClear_Meditions_triggered(self):
        self.widget.clearDetection()
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

    @pyqtSlot()
    def on_actionDelete_Selected_Elements_triggered(self):
        indx = self.widget.deleteSelectedElements()

        if indx is not None and indx[0] >=0 and indx[1] < self.tableParameterOscilogram.rowCount():
            for i in range(indx[1],indx[0]-1,-1):
                #delete from table
                self.tableParameterOscilogram.removeRow(i)

            for i in range(self.tableParameterOscilogram.rowCount()):
                #update table bacground color
                for j in range(self.tableParameterOscilogram.columnCount()):
                    self.tableParameterOscilogram.item(i,j).setBackgroundColor(self.parameterTable_rowcolor_odd if i%2 == 0 else self.parameterTable_rowcolor_even)

            #updates the numpy array  with the detected parameters
            self.measuredParameters = np.concatenate((self.measuredParameters[:indx[0]],self.measuredParameters[indx[1]+1:]))
            self.tableParameterOscilogram.update()
            for wnd in self.twodimensionalGraphs:
                wnd.loadData(self.columnNames,self.measuredParameters)

            self.on_actionDeselect_Elements_triggered()

    @pyqtSlot()
    def on_actionDeselect_Elements_triggered(self):
        self.widget.selectElement() # select the element
        self.widget.clearZoomCursor()


