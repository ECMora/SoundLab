import numpy as np
import cv2
from sound_lab_core.Segmentation.Detectors.OneDimensional.OneDimensionalElementsDetector import \
    OneDimensionalElementsDetector
from duetto.dimensional_transformations.two_dimensional_transforms.Spectrogram.Spectrogram import Spectrogram
from duetto.dimensional_transformations.two_dimensional_transforms.Spectrogram.WindowFunctions import WindowFunction
from scipy.ndimage import label, find_objects


class GrabCutDetector(OneDimensionalElementsDetector):

    def __init__(self, signal=None, min_size_ms=1, min_size_kHz=1):
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
        if new_signal:
            self.spec = Spectrogram(new_signal, 512, 500, WindowFunction.Hamming)
            self.spec.recomputeSpectrogram()

    def detect(self, indexFrom=0, indexTo=-1):
        if not self.signal:
            return []
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

    def detect_elements(self,data, min_size_x, min_size_y):
        elems = []
        try:
            pxx = self.spec.matriz

            pxx[pxx < -100] = -100
            gray = ((pxx - pxx.min()) / (pxx.max() - pxx.min()) * 255).astype(np.uint8)

            ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            kernel = np.ones((3,3),np.uint8)
            opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations=2)
            sure_bg = cv2.dilate(opening,kernel,iterations=3)

            dt = cv2.distanceTransform(opening,2,3)
            dt = np.uint8((dt - dt.min()) / (dt.max() - dt.min()) * 255).astype(np.uint8)

            ret, sure_fg = cv2.threshold(dt,0, 255,cv2.THRESH_OTSU)
            sure_fg = cv2.morphologyEx(sure_fg, cv2.MORPH_CLOSE,kernel, iterations=3)
            sure_fg = cv2.morphologyEx(sure_fg, cv2.MORPH_OPEN,kernel, iterations=3)

            mask = np.zeros(gray.shape,np.uint8)
            mask += cv2.GC_PR_FGD
            mask[sure_fg == 255] = cv2.GC_FGD
            mask[sure_bg == 0] = cv2.GC_BGD

            bgdModel = np.zeros((1,65),np.float64)
            fgdModel = np.zeros((1,65),np.float64)

            img = np.zeros((pxx.shape[0],pxx.shape[1],3),dtype=np.uint8)
            img[:, :, 0] += gray

            cv2.grabCut(img,mask,None,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_MASK)
            mask = np.where((mask==2)|(mask==0),0,1).astype('uint8')

            lbl, ncc = label(mask)
            bounds = find_objects(lbl)

            for i in xrange(1,ncc):
                bnd = bounds[i-1]
                regionBounds = (bnd[0].start, bnd[0].stop, bnd[1].start, bnd[1].stop)
                if regionBounds[1] - regionBounds[0] >= min_size_x and regionBounds[3] - regionBounds[2] >= min_size_y:
                    elems.append((self.spec.from_spec_to_osc(regionBounds[0]),
                                  self.spec.from_spec_to_osc(regionBounds[1])))

        except Exception as ex:
            elems = []
            print("detection error on method Grab cut " + ex.message)

        return elems

