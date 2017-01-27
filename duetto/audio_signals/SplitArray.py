import numpy as np


class SplitArray:
    # if concatenateOnSlice is True, slices return numpy.ndarray else they return SplitArray
    def __init__(self, a=None, concatOnSlice=True, dtype=None):
        if a is None:
            self._data = []
            self._firsts = []
        else:
            self._data = [a]
            self._firsts = [0]
        self._dtype = dtype
        self._sliceCat = concatOnSlice

    def append(self, x):
        if self._data:
            np.append(self._data[-1], x)
        else:
            self._data = [np.array([x])]
            self._firsts = [0]

    def count(self):
        return self.__len__()

    def extend(self, other):
        if not len(other):
            return
        if isinstance(other, SplitArray):
            self._data.extend(other._data)
        else:
            self._firsts.append(len(self))
            self._data.append(other)

    def __len__(self):
        if self._data:
            return self._firsts[-1] + len(self._data[-1])
        return 0

    def __getitem__(self, item):
        if isinstance(item, int):
            if item < 0:
                item += len(self)
            l, i = self._bin_search(item)
            return self._data[l][i]
        elif isinstance(item, slice):  # undefined behavior when step is negative
            start = item.start if item.start is not None else 0
            stop = item.stop if item.stop is not None else len(self)
            step = item.step if item.step is not None else 1
            if start < 0:
                start = max(start + len(self), 0)
            if stop < 0:
                stop = max(stop + len(self), 0)

            if not self._data:
                slc = SplitArray(concatOnSlice=self._sliceCat)
            else:
                l, i = self._bin_search(start)
                if step == 1:
                    if i == 0 and stop - self._firsts[l] >= len(self._data[l]):
                        slc = SplitArray(self._data[l], concatOnSlice=self._sliceCat)
                    else:
                        slc = SplitArray(self._data[l][i: min(len(self._data[l]), stop - self._firsts[l])],
                                         concatOnSlice=self._sliceCat)
                    l += 1
                    while l < len(self._data) and self._firsts[l] + len(self._data[l]) < stop:
                        slc.extend(self._data[l])
                        l += 1
                    if l < len(self._data):
                        if stop - self._firsts[l] >= len(self._data[l]):
                            slc.extend(self._data[l])
                        elif stop - self._firsts[l] > 0:
                            slc.extend(self._data[l][:stop - self._firsts[l]])
                else:
                    slc = SplitArray(concatOnSlice=self._sliceCat)
                    while l < len(self._data) and start < stop:
                        i = start - self._firsts[l]
                        j = min(len(self._data[l]), stop - self._firsts[l])
                        slc.extend(self._data[l][i: j: step])
                        start += (j - i + step - 1) / step * step
                        l += 1

            if self._sliceCat:
                slc.join()
                return slc._data[0]
            else:
                return slc

    def __setitem__(self, key, value):
        l, i = self._bin_search(key)
        self._data[l][i] = value

    def __contains__(self, item):
        return any(item in l for l in self._data)

    def __iter__(self):
        for l in self._data:
            for x in l:
                yield x

    def __repr__(self):
        res = 'SplitArray(['
        for x in self:
            res += str(x) + ', '
        res = (res[:-2] if len(self) else res) + '])'
        return res

    def join(self):
        if self._data:
            self._data = [np.concatenate(self._data)]

    def _bin_search(self, index):
        a, b = 0, len(self._data) - 1
        while a < b:
            m = (a + b + 1) / 2
            if self._firsts[m] <= index:
                a = m
            else:
                b = m - 1
        return a, index - self._firsts[a]

    def to_ndarray(self):
        self.join()
        return self._data[0]

    @property
    def dtype(self):
        return self._dtype if self._dtype else (self._data[0].dtype if len(self._data) else np.dtype(np.int16))