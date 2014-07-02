from PyQt4 import QtGui
from Duetto_Core.Segmentation.Elements.Element import Element
from .QSignalVisualizerWidget import QSignalVisualizerWidget
from Duetto_Core.Segmentation.Detectors.ElementsDetectors.OneDimensional.OneDimensionalElementsDetector import DetectionType,OneDimensionalElementsDetector
import pyqtgraph as pg
import numpy as np


class QSignalDetectorWidget(QSignalVisualizerWidget):
    """This widget performs several detections operations in a signal.

    """
    def __init__(self,parent):
        QSignalVisualizerWidget.__init__(self, parent)
        self.envelopeCurve = pg.PlotCurveItem(np.array([0]), pen=pg.mkPen(self.osc_color, width=1),
                                              shadowPen=pg.mkPen(QtGui.QColor(255, 0, 0), width=3))
        self.axesOscilogram.addItem(self.envelopeCurve)
        self.envelopeFactor = 2 #factor to expand the envelope for best visualization
        self.visibleElements = True
        self.Elements = []  # list of elements detected in oscilogram each element contains the object it self and the extra data for visualize it
        self.elements_detector = OneDimensionalElementsDetector()



    def load_Theme(self, theme):
        """
        this method implements the  way in wich the controls load the theme
        all changes made by the theme are made in this place
        """

        #assert isinstance(theme,SerializedData)
        QSignalVisualizerWidget.load_Theme(self,theme)
        self.envelopeCurve.setPen(pg.mkPen(self.osc_color, width=1))
        self.envelopeCurve.setShadowPen(pg.mkPen(QtGui.QColor(255, 0, 0), width=3))

    def setEnvelopeVisibility(self, bool):
        inaxes = self.envelopeCurve in self.axesOscilogram.items()
        if bool and not inaxes:
            self.axesOscilogram.addItem(self.envelopeCurve)
        elif not bool and inaxes:
            self.axesOscilogram.removeItem(self.envelopeCurve)
        self.axesOscilogram.update()

    def getTransformedEnvelope(self, array):
        self.envelopeFactor = (2.0 ** (self.signalProcessor.signal.bitDepth) * self.maxYOsc / 100) / array[
            np.argmax(array)]
        return (self.envelopeFactor * array - 2 ** (self.signalProcessor.signal.bitDepth - 1) * self.maxYOsc / 100)


    def detectElements(self, threshold=20, decay=1, minSize=0, detectionsettings=None, softfactor=5, merge_factor=50,
                       threshold2=0, threshold_spectral=95, pxx=[], freqs=[], bins=[], minsize_spectral=(0, 0),
                       location=None, progress=None, findSpectralSublements=True):
        self.clearCursors()
        self.elements_detector.detect(self.signalProcessor.signal, 0, len(self.signalProcessor.signal.data),
                                      threshold=threshold, detectionsettings=detectionsettings, decay=decay,
                                      minSize=minSize, softfactor=softfactor, merge_factor=merge_factor,
                                      secondThreshold=threshold2, threshold_spectral=threshold_spectral,
                                      minsize_spectral=minsize_spectral, location=location, progress=progress,
                                      findSpectralSublements=findSpectralSublements,
                                      specgramSettings=self.specgramSettings)

        if detectionsettings is None or detectionsettings.detectiontype == DetectionType.Envelope_Abs_Decay_Averaged or detectionsettings.detectiontype == DetectionType.Envelope_Rms:
            self.envelopeCurve.setData(self.getTransformedEnvelope(self.elements_detector.envelope))
            self.setEnvelopeVisibility(True)
            self.axesOscilogram.threshold.setValue(self.elements_detector.getThreshold())
        else:
            self.setEnvelopeVisibility(False)

        self.axesOscilogram.setVisibleThreshold(True)

        for c in self.elements_detector.elements:
            self.Elements.append(c)# the elment the space for the span selector and the text
            #incorporar deteccion en espectrograma
        if findSpectralSublements:
            self.drawElements()
        else:
            self.drawElements(oscilogramItems=True)


    def changeElementsVisibility(self, visible, element_type=Element.Figures, oscilogramItems=True):
        #change the visibility of the visual items in items
        #that objects must be previously added into oscilogram or specgram widgets
        iterable = self.Elements
        if not oscilogramItems:
            aux = [x.twoDimensionalElements for x in self.Elements]
            iterable = []
            for list in aux:
                iterable.extend(list)
        for e in iterable:
            if element_type is Element.Figures:
                for x in e.visual_figures:
                    x[1] = visible
            elif element_type is Element.Text:
                for x in e.visual_text:
                    x[1] = visible
            elif element_type is Element.Locations:
                for x in e.visual_locations:
                    x[1] = visible
            elif element_type is Element.PeakFreqs:
                for x in e.visual_peaksfreqs:
                    x[1] = visible
        self.drawElements()


    def drawElements(self, oscilogramItems=None):
        # if oscilogramItems = None its updated the oscilogram and spectrogram widgets
        osc = oscilogramItems is None or oscilogramItems
        spec = oscilogramItems is None or not oscilogramItems

        if (self.visibleOscilogram and osc):
            for i in range(len(self.Elements)):
                if self.Elements[i].visible:
                    for item, visible in self.Elements[i].visualwidgets():
                        if not visible:
                            self.axesOscilogram.removeItem(item)
                        else:
                            if (not item in self.axesOscilogram.items() and visible):
                                self.axesOscilogram.addItem(item)
                else:
                    for item, visible in self.Elements[i].visualwidgets():
                        self.axesOscilogram.removeItem(item)
            self.axesOscilogram.update()

        if (self.visibleSpectrogram and spec):
            for i in range(len(self.Elements)):
                for j in range(len(self.Elements[i].twoDimensionalElements)):
                    if self.Elements[i].twoDimensionalElements[j].visible:
                        for item, visible in self.Elements[i].twoDimensionalElements[j].visualwidgets():
                            if not visible:
                                self.axesSpecgram.viewBox.removeItem(item)
                            else:
                                if (not item in self.axesSpecgram.items() and visible):
                                    self.axesSpecgram.viewBox.addItem(item)
                    else:
                        for item, visible in self.Elements[i].twoDimensionalElements[j].visualwidgets():
                            self.axesSpecgram.viewBox.removeItem(item)

            self.axesSpecgram.update()

    def cleanVisibleCursors(self, oscilogram=True, specgram=True):
        if (oscilogram):
            for elem in self.Elements:
                for item, visible in elem.visualwidgets():
                    if (visible):
                        self.axesOscilogram.removeItem(item)
        if (specgram):
            for elem in self.Elements:
                for elem2 in elem.twoDimensionalElements:
                    for item, visible in elem2.visualwidgets():
                        if (visible):
                            self.axesSpecgram.viewBox.removeItem(item)

    def clearCursors(self, oscilogram=True, specgram=True):
        self.cleanVisibleCursors(oscilogram=True, specgram=True)
        self.Elements = [] if oscilogram and specgram else self.Elements

    def selectElement(self, number=-1):
        if len(self.Elements) > number and number >= 0:
            f, t = self.Elements[number].indexFrom, self.Elements[number].indexTo
            self.axesOscilogram.select_region(f, t, pg.mkBrush(QtGui.QColor(255, 255, 255, 150)))
            if f < self.mainCursor.min or t > self.mainCursor.max:
                sizeInterval = self.mainCursor.max - self.mainCursor.min
                self.mainCursor.min = max(0, (f + t - sizeInterval) / 2)
                self.mainCursor.max = min(self.mainCursor.min + sizeInterval, len(self.signalProcessor.signal.data))
                self.refresh()
        else:
            self.axesOscilogram.select_region(0, 0)

    def deleteElements(self):
        pass

    def deleteSelectedElement(self):
        pass

    def refresh(self, dataChanged=True, updateOscillogram=True, updateSpectrogram=True, partial=True):
        QSignalVisualizerWidget.refresh(self,dataChanged, updateOscillogram, updateSpectrogram, partial)
        if self.visibleElements:
            self.drawElements()