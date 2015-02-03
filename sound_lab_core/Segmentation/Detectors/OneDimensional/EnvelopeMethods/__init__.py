# region Envelope Methods

def abs_decay_averaged_envelope(self, data, decay=1, softfactor=6, progress=None, position=(5, 15), type="sin"):
    """
    decay is the minThresholdLabel number of samples in data that separates two elements
    """
    progress_interval = position[1] - position[0]
    if progress is not None:
        progress(position[0] + progress_interval / 10.0)
    rectified = array(abs(data))
    if progress is not None:
        progress(position[0] + progress_interval / 5.0)
    i = 1
    arr = zeros(len(rectified), dtype=int32)
    current = rectified[0]
    fall_init = None
    progress_size = len(arr) / 8.0

    while i < len(arr):
        if fall_init is not None:
            value = rectified[fall_init]
            if type == "lineal":
                value -= rectified[fall_init] * (i - fall_init) / decay  # lineal
            elif type == "sin":
                value = rectified[fall_init] * sin(((i - fall_init) * 1.0 * pi) / (decay * 2) + pi / 2)
            elif type == "cuadratic":
                value = rectified[fall_init] * (1 - ((i - fall_init) * 1.0) / decay) ** 2

            arr[i - 1] = max(value, rectified[i])
            fall_init = None if (value <= rectified[i] or i - fall_init >= decay) else fall_init
        else:
            fall_init = i - 1 if rectified[i] < current else None
            arr[i - 1] = current
        current = rectified[i]
        i += 1
        if i % progress_size == 0 and progress is not None:
            progress(position[0] + (i / progress_size) * progress_interval / 10.0)
    arr[-1] = current

    if softfactor > 1:
        return array([mean(arr[i - softfactor:i]) for i, _ in enumerate(arr, start=softfactor)])
    return arr


def rms_moving_average_envelope(self, data, minSize=1, progress=None, position=(5, 20)):
    minSize = int(minSize)
    if minSize % 2 != 0:
        minSize += 1
    i = minSize / 2

    d = array(data, dtype=long)

    if self.progress is not None:
        self.progress(5)

    g = cumsum(d ** 2)

    if self.progress is not None:
        self.progress(10)
    f = lambda ind: abs(d[ind]) if ind < minSize / 2 or ind > d.size - minSize / 4 else sqrt(
        (g[ind - 1 + minSize / 4] - g[ind - 1 - minSize / 4]) * 0.5 / minSize)

    intervals = array([f(x) for x in arange(d.size)])

    return intervals


def envelope_frecuency_increased_detector(self):
    pass


# endregion

# region Point to Point Methods

def local_naive_max_detector(self, data, threshold, minSize, merge_factor):
    indexes, vals = self.localMax(data)
    if self.progress is not None:
        self.progress(10)
    detected = mlab.contiguous_regions(vals > threshold)

    if self.progress is not None:
        self.progress(20)

    detected = [(indexes[x[0] + 1], indexes[x[1] - 1]) for x in detected if
                (indexes[x[1] - 1] - indexes[x[0] + 1]) > minSize]

    if self.progress is not None:
        self.progress(30)

    if merge_factor > 0:
        detected = self.mergeIntervals(detected, merge_factor)

    return detected


def local_hold_detector(self, data, threshold, minSize, merge_factor):
    """
    saltos de la mitad del tamanno minimo
    """
    data = abs(data)
    i = 0
    start = -1
    posible_end = -1
    minSize = int(minSize)
    mark = -1
    intervals = []

    progressupdate = len(data) / 4
    while i < len(data):
        if data[i] >= threshold:
            start = i if start == -1 else start
            i += minSize / 2
            if i >= len(data):
                i = len(data) - 1
            posible_end = i

        elif i > posible_end and (posible_end != -1 and start != -1 and posible_end - start > minSize):
            intervals.append((start, posible_end))
            posible_end = -1
            start = -1

        i += 1
        if self.progress is not None and i % progressupdate == 0:
            self.progress(10 + 5 * i / progressupdate)

    if self.progress is not None:
        self.progress(25)

    intervals = self.mergeIntervals(intervals, merge_factor)

    if self.progress is not None:
        self.progress(30)

    return [c for c in intervals if (c[1] - c[0]) > minSize]


def local_max_percent_detector(self, data, threshold, minSize, merge_factor, end_size_element_size_relation=90):
    """
    the intervals that has a proportion of ots maxThresholdLabel above threshold
    """
    indexes, vals = self.localMax(data)
    global_proportion = where(vals >= threshold)[0].size * 1.0 / vals.size
    i = 0
    start = -1

    posible_end = -1
    minSize = int(minSize)
    intervals = []
    local_proportion = 1.0 if vals[i] >= threshold else 0.0
    max_val = local_proportion

    progressupdate = len(vals) / 4

    if self.progress is not None:
        self.progress(10)

    while i < len(vals):
        if local_proportion >= global_proportion and local_proportion > max_val * end_size_element_size_relation / 100.0:
            start = i if start == -1 else start
            posible_end = i
            local_proportion = (local_proportion * (i - start + 1) + (1.0 if vals[i] >= threshold else 0.0)) * 1.0 / (
                i - start + 2)
            max_val = max(max_val, local_proportion)
        else:
            if posible_end != -1 and start != -1:
                intervals.append((indexes[start], indexes[posible_end]))

            local_proportion = 1.0 if vals[i] >= threshold else 0.0
            max_val = local_proportion
            posible_end = -1
            start = -1
        i += 1
        if self.progress is not None and i % progressupdate == 0:
            self.progress(10 + 5 * i / progressupdate)

    if posible_end != -1 and start != -1 and posible_end - start > minSize:
        intervals.append((indexes[start], indexes[posible_end]))

    if self.progress is not None:
        self.progress(25)

    intervals = self.mergeIntervals(intervals, merge_factor)

    if self.progress is not None:
        self.progress(30)

    return [c for c in intervals if (c[1] - c[0]) > minSize]

# endregion

