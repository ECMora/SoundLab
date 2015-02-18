# region Interval Methods

def intervals_frecuency_bands_distribution_detector(self, data, threshold, minSize, merge_factor):
    """
    frecuencies highly defined
    """
    # ind,vals = self.localMax(data)
    # vals = diff(vals)
    # _threshold = vals.var()
    # def function(d):
    # ind,vals = self.localMax(d)
    #     freqs = diff(ind)
    #     v = var(freqs)
    #     sorted_diff = sort(freqs)
    #
    #     return v if mean(vals) > threshold else _threshold
    #
    # return self.interval_detector(data,_threshold,minSize,merge_factor,function,comparer_greater_threshold=False)
    pass


def intervals_frecuency_distribution_detector(self, data, threshold, minSize, merge_factor):
    """
    Multiple frecs or noise
    uses the property of amplitude of the signal to discard silence intervals
    """
    ind, vals = self.localMax(data)
    vals = diff(vals)
    _threshold = vals.var()

    def function(d):
        ind, vals = self.localMax(d)
        return var(diff(ind)) if mean(vals) > threshold else _threshold

    return self.interval_detector(data, _threshold, minSize, merge_factor, function, comparer_greater_threshold=False)


def interval_rms_detector(self, data, threshold, minSize, merge_factor):
    def function(d):
        ind, vals = self.localMax(d)
        x = 0
        if len(vals) > 0:
            vals = array(vals, dtype=long)
            x = sqrt(sum(vals ** 2) / vals.size)
        return x

    return self.interval_detector(data, threshold, minSize, merge_factor, function)


def interval_detector(self, data, threshold, minSize, merge_factor, function, comparer_greater_threshold=True):
    """
    if comparer_greater_threshold then the intervals > threshold else intervals < threshold would be acepted
    """
    minSize = int(minSize)
    if minSize == 0:
        minSize = len(data) / 1000

    f_interval = lambda ind: function(data[ind - minSize / 2:ind + minSize / 2])

    detected = array([f_interval(i) for i in arange(minSize / 2, data.size, minSize / 2)])

    if self.progress is not None:
        self.progress(10)

    if comparer_greater_threshold:
        detected = mlab.contiguous_regions(detected > threshold)
    else:
        detected = mlab.contiguous_regions(detected < threshold)

    if self.progress is not None:
        self.progress(20)

    detected = [((x[0]) * minSize / 2, (x[1]) * minSize / 2) for x in detected if x[1] > 1 + x[0]]

    if self.progress is not None:
        self.progress(25)

    if merge_factor > 0:
        detected = self.mergeIntervals(detected, merge_factor)

    if self.progress is not None:
        self.progress(30)

    return detected


def interval_maxmean_detector(self, data, threshold, minSize, merge_factor):
    function = lambda d: self.localMax(d)[1].mean()

    return self.interval_detector(data, threshold, minSize, merge_factor, function)


def interval_percentmaxpeaks_detector(self, data, threshold, minSize, merge_factor):
    _, vals_data = self.localMax(data)
    if vals_data.size == 0:
        _threshold = 0
    else:
        _threshold = where(vals_data > threshold)[0].size * 1.0 / vals_data.size

    def function(d):
        _, vals = self.localMax(d)
        x = 0
        if vals.size > 0:
            x = where(vals > threshold)[0].size * 1.0 / vals.size
        return x

    return self.interval_detector(data, _threshold, minSize, merge_factor, function)

# endregion
