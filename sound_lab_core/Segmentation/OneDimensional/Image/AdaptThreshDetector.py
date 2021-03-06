from math import ceil

import numpy as np
import cv2
from duetto.dimensional_transformations.two_dimensional_transforms.Spectrogram.Spectrogram import Spectrogram
from duetto.dimensional_transformations.two_dimensional_transforms.Spectrogram.WindowFunctions import WindowFunction

from sound_lab_core.Segmentation.OneDimensional.OneDimensionalElementsDetector import \
    OneDimensionalElementsDetector


class AdaptThreshDetector(OneDimensionalElementsDetector):

    def __init__(self, signal, min_size_ms=1, min_size_kHz=1):
        self._signal = None
        self.spec = None

        self.min_size_ms = min_size_ms
        self.min_size_kHz = min_size_kHz
        self.elements = []
        self.intervalSize = 24000
        OneDimensionalElementsDetector.__init__(self, signal)


    @property
    def signal(self):
        return self._signal

    @signal.setter
    def signal(self, new_signal):
        self._signal = new_signal
        if new_signal:
            self.spec = Spectrogram(new_signal, 1024, 1000, WindowFunction.Hamming)
            self.spec.recomputeSpectrogram(maxCol=1000)

    def detect(self, indexFrom=0, indexTo=-1):
        indexTo = self.signal.length if indexTo == -1 else indexTo

        min_size_x = int(self.min_size_ms * self.signal.samplingRate / 1000.0) / 24

        min_size_y = int(self.min_size_kHz * 1000.0 / (self.spec.freqs[1] - self.spec.freqs[0]))

        number_of_intervals = int(ceil((indexTo - indexFrom) * 1.0 / self.intervalSize))
        elems = []

        self.detectionProgressChanged.emit(10)

        for i in xrange(number_of_intervals):
            self.detectionProgressChanged.emit(10 + 80 * i / number_of_intervals)

            temp = self.detect_elements(self.signal.data, indexFrom + i * self.intervalSize,
                                        indexFrom + (i+1) * self.intervalSize, min_size_x, min_size_y)
            if len(elems) > 0 and len(temp) > 0 and elems[-1][1] >= temp[0][0]:
                elems[-1] = (elems[-1][0], temp[0][1])
                elems.extend(temp[1:])
            elems.extend(temp)


        self.detectionProgressChanged.emit(90)

        self.elements = [None for _ in elems]
        one_dim_class = self.get_one_dimensional_class()

        for i, c in enumerate(elems):
            self.elements[i] = one_dim_class(self.signal, c[0], c[1])

        self.detectionProgressChanged.emit(100)

        return self.elements

    def detect_elements(self,data, start, end, min_size_x, min_size_y):
        elems = []
        if not self.signal:
            return elems
        try:
            self.spec.recomputeSpectrogram(start, end)
            img = self.spec.matriz
            img = np.power(10, img/10.0)
            img.astype('float')
            img = 255 * (img / np.amax(img))

            gray = img.astype('uint8')
            gray_blur = cv2.GaussianBlur(gray, (15, 15), 0)

            thresh = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 1)
            kernel = np.ones((3, 3), np.uint8)
            closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=3)
            contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for c in contours:
                upleft= np.amin(c,0)[0]
                downright = np.amax(c,0)[0]
                regionBounds = (upleft[1], downright[1], upleft[0], downright[0])
                if regionBounds[1] - regionBounds[0] >= min_size_x and regionBounds[3] - regionBounds[2] >= min_size_y:
                    elems.append((self.spec.from_spec_to_osc(regionBounds[0]),
                                  self.spec.from_spec_to_osc(regionBounds[1])))

        except Exception as ex:
            elems = []
            print("detection error on method Adapt threshold " + ex.message)

        return elems

