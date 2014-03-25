from collections import deque
import numpy as np
from Duetto_Core.Cursors.RectangularCursor import RectangularCursor
from Duetto_Core.Detectors.Detector import Detector


class SpectrogramHillDetector(Detector):
    def __init__(self):
        Detector.__init__(self)
        self.regionsOverUmbral = []
        self._nr, self._nc = 0, 0
        self._dr, self._dc = [], []
        self._gt_tresh = np.ndarray((0, 0))
        self.pxx = np.ndarray((0, 0))
        self.markedPxx = self.pxx

    def detect(self, signal, threshold, pxx, freqs, bins, threshold_is_percentile=True, minsize=(0, 0),
               merge_factor=(1, 1)):
        #gets the  relevant regions in spectrogram
        if threshold_is_percentile:
            threshold = np.percentile(pxx, threshold)
        self._set_movement_arrays(merge_factor)
        self.pxx = pxx
        self._nr, self._nc = self.pxx.shape
        self.markedPxx = np.zeros_like(self.pxx)
        self._gt_tresh = pxx > threshold
        gt_tresh_idx = np.argwhere(self._gt_tresh)
        for i, j in gt_tresh_idx:
            if self._gt_tresh[i, j]:
                self.regionsOverUmbral.append([])
                regionBounds = self._islandDelete(i, j, len(self.regionsOverUmbral))
                if freqs[regionBounds[1]] - freqs[regionBounds[0]] < minsize[0] \
                        and bins[regionBounds[3]] - bins[regionBounds[2]] < minsize[1]:
                    for idxs in self.regionsOverUmbral.pop():
                        self.markedPxx[idxs[0], idxs[1]] = 0
                    continue
                rc = RectangularCursor()
                rc.visualOptions.oscilogramCursor = False
                rc.intervalX.visualOptions.oscilogramCursor = False
                rc.intervalY.visualOptions.oscilogramCursor = False
                rc.intervalX.min, rc.intervalX.max = regionBounds[0], regionBounds[1]
                rc.intervalY.min, rc.intervalY.max = regionBounds[2], regionBounds[3]
                self.rectangles.append(rc)

    def _set_movement_arrays(self, merge_factor):
        self._dr, self._dc = [], []
        for i in range(- merge_factor[0], merge_factor[0] + 1):
            for j in range(- merge_factor[1], merge_factor[1] + 1):
                if i == j == 0: continue
                self._dr.append(i)
                self._dc.append(j)

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
