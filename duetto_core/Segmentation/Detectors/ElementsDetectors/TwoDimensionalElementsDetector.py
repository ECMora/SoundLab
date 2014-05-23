# -*- coding: utf-8 -*-
from collections import deque
import numpy as np
from Duetto_Core.Segmentation.Detectors.Detector import Detector
from Duetto_Core.Segmentation.Elements.TwoDimensionalElement import SpecgramElement


class TwoDimensionalElementsDetector(Detector):
    def __init__(self):
        Detector.__init__(self)
        self.regionsOverUmbral = []
        self._nr, self._nc = 0, 0
        self._dr, self._dc = [-1,0,1,0], [0,1,0,-1]
        self._gt_tresh = np.ndarray((0, 0))
        self.pxx = np.ndarray((0, 0))
        self.markedPxx = self.pxx

    def detect(self, signal, threshold, pxx, freqs, bins, minsize=(0, 0),one_dimensional_parent=None,location=None):
        if(signal is None):
                return
        #gets the  relevant regions in spectrogram
        self.pxx = pxx
        self._nr, self._nc = self.pxx.shape
        self.markedPxx = np.zeros_like(self.pxx)
        self._gt_tresh = pxx > threshold
        gt_tresh_idx = np.argwhere(self._gt_tresh)
        elemIndex=1
        for i, j in gt_tresh_idx:
            if self._gt_tresh[i, j]:
                self.regionsOverUmbral.append([])
                regionBounds = self._islandDelete(i, j, len(self.regionsOverUmbral))
                if regionBounds[1] - regionBounds[0] <= minsize[0] \
                        or regionBounds[3] - regionBounds[2] <= minsize[1]:
                    for idxs in self.regionsOverUmbral.pop():
                        self.markedPxx[idxs[0], idxs[1]] = 0
                    continue
                else:
                    rc = SpecgramElement(signal,pxx[regionBounds[0]: regionBounds[1],regionBounds[2]:regionBounds[3]],freqs,regionBounds[0],regionBounds[1],bins,regionBounds[2],regionBounds[3],number=elemIndex,one_dimensional_parent=one_dimensional_parent,location=location, multipleSubelements=True)
                    elemIndex+=1
                    self.twodimensionalElements.append(rc)

    def _islandDelete(self, r, c, element_number):
        #deletes a boolean island in map with earth in the i, j position
        #returns a tuple with the min row ,max row, min column, max column coordinates of the bool island
        result = r, r, c, c
        q = deque()
        q.append((r, c))
        self._gt_tresh[r, c] = False
        while q:
            r, c = q.popleft()
            result = min(result[0], r), max(result[1], r), min(result[2], c), max(result[3], c)
            self.markedPxx[r, c] = element_number
            self.regionsOverUmbral[element_number - 1].append((r, c))
            for d in range(len(self._dr)):
                mr, mc = r + self._dr[d], c + self._dc[d]
                if 0 <= mr < self._nr and 0 <= mc < self._nc and self._gt_tresh[mr, mc]:
                    self._gt_tresh[mr, mc] = False
                    q.append((mr, mc))
        return result


