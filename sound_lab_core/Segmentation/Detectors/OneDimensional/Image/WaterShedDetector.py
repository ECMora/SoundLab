import numpy as np
import cv2
from sound_lab_core.Segmentation.Detectors.OneDimensional.OneDimensionalElementsDetector import \
    OneDimensionalElementsDetector
from duetto.dimensional_transformations.two_dimensional_transforms.Spectrogram.Spectrogram import Spectrogram
from duetto.dimensional_transformations.two_dimensional_transforms.Spectrogram.WindowFunctions import WindowFunction
from scipy.ndimage import label, find_objects


class WatershedDetector(OneDimensionalElementsDetector):

    def __init__(self, signal, min_size_ms=1, min_size_kHz=1):

        self._signal = None
        self.spec = None
        self.min_size_ms = min_size_ms
        self.min_size_kHz = min_size_kHz
        OneDimensionalElementsDetector.__init__(self, signal)

    @property
    def signal(self):
        return self._signal

    @signal.setter
    def signal(self, new_signal):
        self._signal = new_signal
        self.spec = Spectrogram(new_signal, 512, 500, WindowFunction.Hamming)
        self.spec.recomputeSpectrogram()

    def detect(self, indexFrom=0, indexTo=-1):
        indexTo = self.signal.length if indexTo == -1 else indexTo

        min_size_x = int(self.min_size_ms * self.signal.samplingRate / 1000.0)

        min_size_y = int(self.min_size_kHz * 1000.0 / (self.spec.freqs[1] - self.spec.freqs[0]))

        elems = self.detect_elements(self.signal.data[indexFrom:indexTo], min_size_x, min_size_y)

        self.detectionProgressChanged.emit(90)

        self.elements = [None for _ in elems]
        one_dim_class = self.get_one_dimensional_class()

        for i, c in enumerate(elems):
            self.elements[i] = one_dim_class(self.signal, c[0], c[1])

        self.detectionProgressChanged.emit(100)

        return self.elements

    def detect_elements(self, data, min_size_x, min_size_y):
        elems = []
        try:
            pxx = self.spec.matriz
            pxx = 10 * np.log10(pxx/pxx.max())
            pxx[pxx < -100] = -100
            gray = ((pxx - pxx.min()) / (pxx.max() - pxx.min()) * 255)
            gray.astype(np.uint8)
            img = np.zeros((pxx.shape[0],pxx.shape[1],3),dtype=np.uint8)
            img[:,:,0] += gray

            _, img_bin = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
            img_bin = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, np.ones((3, 3), dtype=int))
            border = cv2.dilate(img_bin, None, iterations=2)
            border = border - cv2.erode(border, None)

            dt = cv2.distanceTransform(img_bin, 2, 3)
            dt = ((dt - dt.min()) / (dt.max() - dt.min()) * 255).astype(np.uint8)
            dt = cv2.morphologyEx(dt, cv2.MORPH_CLOSE, np.ones((3, 3), dtype=int),iterations=3)
            dt = cv2.morphologyEx(dt, cv2.MORPH_OPEN, np.ones((3, 3), dtype=int),iterations=3)
            _, dt = cv2.threshold(dt, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            lbl, ncc = label(dt)

            # Completing the markers now.
            lbl[border == 255] = ncc + 1

            lbl = lbl.astype(np.int32)
            cv2.watershed(img, lbl)

            lbl[lbl == -1] = 0
            lbl[lbl == ncc + 1] = 0

            bounds = find_objects(lbl)

            for i in xrange(1,ncc):
                bnd = bounds[i-1]
                regionBounds = (bnd[0].start, bnd[0].stop, bnd[1].start, bnd[1].stop)
                if regionBounds[1] - regionBounds[0] >= min_size_x and regionBounds[3] - regionBounds[2] >= min_size_y:
                    elems.append((regionBounds[0],regionBounds[1]))

        except Exception as ex:
            elems = []
            print("detection error on method Water Sheed " + ex.message)

        return elems

