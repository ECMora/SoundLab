# -*- coding: utf-8 -*-
from numpy import *
import matplotlib.mlab as mlab
from Duetto_Core.Segmentation.Detectors.ElementsDetectors.ElementsDetector import ElementsDetector
from Duetto_Core.Segmentation.Elements.OneDimensionalElement import OscilogramElement


class AutomaticThresholdType:
    Global_MaxMean,\
    Global_MaxMean_Sdv,\
    Global_MaxMean_Half_Sdv,\
    Global_MaxMean_Two_Sdv,\
    Local_MaxMean,\
    Local_MaxMean_Sdv,\
    Local_MaxMean_Half_Sdv,\
    Local_MaxMean_Two_Sdv,\
    UserDefined = range(9)

class DetectionType:
    LocalMax,LocalHoldTime,LocalMaxProportion,IntervalRms,IntervalMaxMedia, IntervalMaxProportion,IntervalFrecuencies,Envelope_Abs_Decay_Averaged,Envelope_Rms = range(9)

class DetectionSettings:
    def __init__(self,detectiontype,automaticthresholdtype):
        self.detectiontype=detectiontype
        self.automaticthresholdtype = automaticthresholdtype


class OneDimensionalElementsDetector(ElementsDetector):
    #progress = pyqtSignal(int)

    def __init__(self,progress=None):
        ElementsDetector.__init__(self)
        self.threshold = array([0])
        self.progress = progress
        self.envelope = array([0])
        self.detectionsettings = None

    def detect(self,signal, indexFrom=0, indexTo=-1,detectionsettings=None, threshold=0, decay=1,minSize=1.0,softfactor = 5,merge_factor=50,secondThreshold=0,
               threshold_spectral=95, minsize_spectral=(0, 0),location = None,progress=None,findSpectralSublements = False,specgramSettings=None):
        """
        decay in ms to prevent locals falls, should be as long as the min size of the separation between
        elements
        softfactor points to make a moving average in data
        merge_factor in %
        threshold in dB from the max value
        """
        if detectionsettings is not None:
            self.detectionsettings = detectionsettings
        else:
            self.detectionsettings = DetectionSettings(DetectionType.Envelope_Abs_Decay_Averaged,AutomaticThresholdType.Global_MaxMean)

        if specgramSettings is None:
            return
        if progress is not None:
            self.progress = progress
        if(signal is None):
            return
        if indexTo == -1:
            indexTo = len(signal.data)
        decay = int(decay*signal.samplingRate/1000)  #salto para evitar caidas locales
        if abs(threshold) < 0.01:  # to prevent numeric errors
            self.computeThreshold(signal.data[indexFrom : indexTo],method=AutomaticThresholdType.Global_MaxMean)
            threshold = self.getThreshold(0)
        else:
            #translate the threshold from dB scale to V value
            #maxThreshold is 60 when you simplify --> 20*log10((2**signal.bitDepth)*1000.0/(2**signal.bitDepth))
            if self.detectionsettings.automaticthresholdtype == AutomaticThresholdType.UserDefined:
                threshold = (10.0**((60-threshold)/20.0))*(2**signal.bitDepth)/1000.0
                self.threshold= [threshold]
            else:
                 self.computeThreshold(signal.data[indexFrom : indexTo],method=self.detectionsettings.automaticthresholdtype)

            threshold = self.getThreshold(0)
        if secondThreshold > 0:
            secondThreshold = (10.0**((60-secondThreshold)/20.0))*(2**signal.bitDepth)/1000.0
        #if merge_factor != 0:
        #    merge_factor = merge_factor*signal.samplingRate/1000.0
        if minSize != 0:
            minSize = minSize*signal.samplingRate/1000.0
            minSize = int(minSize)
        if progress is not None:
            self.progress(2)

        threshold_spectral = percentile(specgramSettings.Pxx,threshold_spectral)
        trim_threshold =  threshold_spectral
        if progress is not None:
            self.progress(5)
        elems = []
        if self.detectionsettings.detectiontype == DetectionType.Envelope_Abs_Decay_Averaged or self.detectionsettings.detectiontype == DetectionType.Envelope_Rms:
            elems = self.envelope_detector(self.detectionsettings.detectiontype,signal.data[indexFrom : indexTo],threshold, minSize=minSize,
                                       decay=decay, softfactor=softfactor, merge_factor=merge_factor,secondThreshold=secondThreshold)

        #points
        elif self.detectionsettings.detectiontype == DetectionType.LocalMax:
             elems = self.local_naive_max_detector(signal.data[indexFrom : indexTo],threshold,minSize,merge_factor)

        elif self.detectionsettings.detectiontype == DetectionType.LocalHoldTime:
            elems = self.local_hold_detector(signal.data[indexFrom : indexTo],threshold,minSize,merge_factor)

        elif self.detectionsettings.detectiontype == DetectionType.LocalMaxProportion:
            elems = self.local_max_percent_detector(signal.data[indexFrom : indexTo],threshold,minSize,merge_factor)

        #intervals
        elif self.detectionsettings.detectiontype == DetectionType.IntervalRms:
            elems = self.interval_rms_detector(signal.data[indexFrom : indexTo],threshold,minSize,merge_factor)

        elif self.detectionsettings.detectiontype == DetectionType.IntervalMaxMedia:
            elems = self.interval_maxmean_detector(signal.data[indexFrom : indexTo],threshold,minSize,merge_factor)

        elif self.detectionsettings.detectiontype == DetectionType.IntervalMaxProportion:
            elems = self.interval_percentmaxpeaks_detector(signal.data[indexFrom : indexTo],threshold,minSize,merge_factor)

        elif self.detectionsettings.detectiontype == DetectionType.IntervalFrecuencies:
            elems = self.intervals_frecuency_distribution_detector(signal.data[indexFrom : indexTo],threshold,minSize,merge_factor)

        l = len(elems)
        progress_size = l/10 if l > 10 else 3
        stepsize = 50/(10 if l > 10 else 3)
        self.oneDimensionalElements = [None for _ in elems]
        for i,c in enumerate(elems):
            self.oneDimensionalElements[i] = OscilogramElement(signal,c[0], c[1],number=i+1,threshold_spectral= threshold_spectral,
                                                               minsize_spectral=minsize_spectral,location=location,findSpectralSublements = findSpectralSublements,
                                                               specgramSettings=specgramSettings,trim_threshold=trim_threshold)
            #descartar elemento si no posee informacion espectral suficiente
            if progress is not None and i % progress_size == 0:
                self.progress(40 + (i/progress_size)*stepsize)

    def localMax(self,data,threshold=0,positives = None):
        """
        identify the local  (positives or not) max that are above threshold
       """
        indexes = []
        values = []
        data = array(data)

        if positives is not None and positives:
            data = where(data >= threshold,data,0)
        elif positives is not None:
            data = where(data < -threshold,data,0)

        data = abs(data)

        for i in range(1,data.size-1):
            if (data[i] > data[i - 1] and data[i] > data[i + 1]) or (data[i] == data[i - 1] == data[i + 1]):
                indexes.append(i)
                values.append(data[i])

        return array(indexes),array(values)

    #Detectors
    def computeThreshold(self,data,total=True,method=AutomaticThresholdType.Global_MaxMean_Half_Sdv,overlap=0):
        """
        total or local
        methods
        """
        self.threshold = []
        if total:
            if method == AutomaticThresholdType.Global_MaxMean:
                indexes,vals = self.localMax(data)
                self.threshold = [vals.mean()]
            elif method == AutomaticThresholdType.Global_MaxMean_Sdv:
                indexes,vals = self.localMax(data)
                self.threshold = [vals.mean() - vals.std()]
            elif method == AutomaticThresholdType.Global_MaxMean_Half_Sdv:
                indexes,vals = self.localMax(data)
                self.threshold = [vals.mean() - vals.std()/2]
            elif method == AutomaticThresholdType.Global_MaxMean_Two_Sdv:
                indexes,vals = self.localMax(data)
                self.threshold = [vals.mean() - 2*vals.std()]
        else:
            pass


    def getThreshold(self,i=0):
        if len(self.threshold) == 1:
            return self.threshold[0]

        return 0

    #Envelopes

    def envelope_detector(self,envelope_method, data,threshold=0, minSize=1, decay=1, softfactor=10, merge_factor=0,secondThreshold=0):
        """
        data is a numpy array
        minSize is the min amplitude of an element
        merge_factor is the % of separation between 2 elements that is assumed as one (merge the 2 into one)
        """
        if envelope_method == DetectionType.Envelope_Abs_Decay_Averaged:
            self.envelope = self.abs_decay_averaged_envelope(data, decay=decay,softfactor=softfactor, progress = self.progress, position= (5,15))
        elif envelope_method == DetectionType.Envelope_Rms:
            self.envelope = self.rms_moving_average_envelope(data,minSize,progress = self.progress, position= (5,15))

        if self.progress is not None:
            self.progress(15)

        regions = mlab.contiguous_regions(self.envelope > threshold)

        if self.progress is not None:
            self.progress(20)

        if secondThreshold > 0:
            for i in range(len(regions)):
                left = mlab.cross_from_above(self.envelope[regions[i][0]:(0 if i == 0 else regions[i-1][1]):-1], secondThreshold)
                left = 0 if len(left) == 0 else left[0]
                rigth = mlab.cross_from_above(self.envelope[regions[i][1]:(-1 if i == len(regions)-1 else regions[i+1][0]-1)], secondThreshold)
                rigth = 0 if len(rigth) == 0 else rigth[0]
                regions[i] = (regions[i][0]-left,regions[i][1]+rigth)
        if self.progress is not None:
            self.progress(30)
        if merge_factor > 0:
            regions = self.mergeIntervals(regions, merge_factor)
        if self.progress is not None:
            self.progress(38)
        regions = [c for c in regions if (c[1]-c[0]) > minSize]
        if self.progress is not None:
            self.progress(40)
        return regions

    def abs_decay_averaged_envelope(self,data, decay=1,softfactor=6,progress= None,position= (5,15),type="sin"):
        """
        decay is the min number of samples in data that separates two elements
        """
        progress_interval = position[1]-position[0]
        if progress is not None:
            progress(position[0]+progress_interval/10.0)
        rectified = array(abs(data))
        if progress is not None:
            progress(position[0]+progress_interval/5.0)
        i = 1
        arr = zeros(len(rectified), dtype=int32)
        current = rectified[0]
        fall_init = None
        progress_size = len(arr)/8.0

        while i < len(arr):
            if fall_init is not None:
                value = rectified[fall_init]
                if type=="lineal":
                    value -= rectified[fall_init]*(i-fall_init)/decay #lineal
                elif type=="sin":
                    value = rectified[fall_init]*sin(((i-fall_init)*1.0*pi)/(decay*2)+pi/2)
                elif type=="cuadratic":
                    value = rectified[fall_init]*(1-((i-fall_init)*1.0)/decay)**2

                arr[i-1] = max(value, rectified[i])
                fall_init = None if(value <= rectified[i] or i-fall_init >= decay) else fall_init
            else:
                fall_init = i-1 if rectified[i] < current else None
                arr[i-1] = current
            current = rectified[i]
            i += 1
            if i % progress_size == 0 and progress is not None:
                progress(position[0]+(i/progress_size)*progress_interval/10.0)
        arr[-1] = current

        if softfactor > 1:
            return array([mean(arr[i-softfactor:i]) for i,_ in enumerate(arr, start=softfactor)])
        return arr

    def rms_moving_average_envelope(self,data,minSize=1,progress= None,position= (5,20)):
        minSize = int(minSize)
        if minSize % 2 != 0:
            minSize+=1
        i = minSize/2

        d = array(data,dtype=long)

        if self.progress is not None:
            self.progress(5)

        g =cumsum(d**2)

        if self.progress is not None:
            self.progress(10)
        f = lambda ind:abs(d[ind]) if ind < minSize/2 or ind > d.size-minSize/4 else sqrt((g[ind-1+minSize/4]-g[ind-1-minSize/4])*0.5/minSize)

        intervals = array([f(x) for x in arange(d.size)])

        return intervals

    def envelope_frecuency_increased_detector(self):
        pass

    #Amplitude
    #Intervals
    def interval_rms_detector(self,data,threshold,minSize,merge_factor):
        def function(d):
            ind,vals = self.localMax(d)
            x = 0
            if len(vals) > 0:
                vals = array(vals,dtype=long)
                x = sqrt(sum(vals**2)/vals.size)
            return x

        return self.interval_detector(data,threshold,minSize,merge_factor,function)

    def interval_detector(self,data,threshold,minSize,merge_factor,function,comparer_greater_threshold = True):
        """
        if comparer_greater_threshold then the intervals > threshold else intervals < threshold would be acepted
        """
        minSize = int(minSize)
        if minSize == 0:
            minSize = len(data)/1000

        f_interval = lambda ind: function(data[ind-minSize/2:ind+minSize/2])

        detected = array([f_interval(i) for i in arange(minSize/2,data.size,minSize/2)])

        if self.progress is not None:
            self.progress(10)

        if comparer_greater_threshold:
            detected = mlab.contiguous_regions(detected > threshold)
        else:
            detected = mlab.contiguous_regions(detected < threshold)


        if self.progress is not None:
            self.progress(20)

        detected = [((x[0])*minSize/2,(x[1])*minSize/2) for x in detected if x[1]>1+x[0]]

        if self.progress is not None:
            self.progress(25)

        if merge_factor > 0:
            detected = self.mergeIntervals(detected, merge_factor)

        if self.progress is not None:
            self.progress(30)

        return detected

    def interval_maxmean_detector(self,data,threshold,minSize,merge_factor):
        function = lambda d: self.localMax(d)[1].mean()

        return self.interval_detector(data,threshold,minSize,merge_factor,function)

    def interval_percentmaxpeaks_detector(self,data,threshold,minSize,merge_factor):
        _,vals_data = self.localMax(data)
        if vals_data.size == 0:
            _threshold = 0
        else:
            _threshold = where(vals_data > threshold)[0].size*1.0/vals_data.size

        def function(d):
            _,vals = self.localMax(d)
            x = 0
            if vals.size>0:
                x = where(vals > threshold)[0].size*1.0/vals.size
            return x
        return self.interval_detector(data,_threshold,minSize,merge_factor,function)

    #Point to Point

    def local_naive_max_detector(self,data,threshold,minSize,merge_factor):
        indexes,vals = self.localMax(data)
        if self.progress is not None:
            self.progress(10)
        detected = mlab.contiguous_regions(vals > threshold)

        if self.progress is not None:
            self.progress(20)

        detected = [(indexes[x[0]+1],indexes[x[1]-1]) for x in detected if (indexes[x[1]-1]-indexes[x[0]+1]) > minSize]

        if self.progress is not None:
            self.progress(30)

        if merge_factor > 0:
            detected = self.mergeIntervals(detected, merge_factor)

        return detected

    def local_hold_detector(self,data,threshold,minSize,merge_factor):
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

        progressupdate = len(data)/4
        while i < len(data):
            if data[i] >= threshold:
                start = i if start == -1 else start
                i += minSize/2
                if i>= len(data):
                    i = len(data) - 1
                posible_end = i

            elif i > posible_end and (posible_end != -1 and start != -1 and posible_end - start > minSize):
                intervals.append((start,posible_end))
                posible_end = -1
                start = -1

            i+=1
            if self.progress is not None and i%progressupdate==0:
                self.progress(10 + 5* i/progressupdate)

        if self.progress is not None:
            self.progress(25)


        intervals = self.mergeIntervals(intervals,merge_factor)

        if self.progress is not None:
            self.progress(30)

        return [c for c in intervals if (c[1]-c[0]) > minSize]

    def local_max_percent_detector(self,data,threshold,minSize,merge_factor,end_size_element_size_relation=90):
        """
        the intervals that has a proportion of ots max above threshold
        """
        indexes,vals = self.localMax(data)
        global_proportion = where(vals >=threshold)[0].size*1.0/vals.size
        i = 0
        start = -1

        posible_end = -1
        minSize = int(minSize)
        intervals = []
        local_proportion = 1.0 if vals[i] >= threshold else 0.0
        max_val = local_proportion

        progressupdate = len(vals)/4


        if self.progress is not None:
            self.progress(10)

        while i < len(vals):
            if local_proportion >= global_proportion and local_proportion > max_val*end_size_element_size_relation/100.0:
                start = i if start == -1 else start
                posible_end = i
                local_proportion = (local_proportion * (i-start+1) + (1.0 if vals[i] >= threshold else 0.0))*1.0/(i-start+2)
                max_val = max(max_val,local_proportion)
            else:
                if posible_end != -1 and start != -1:
                    intervals.append((indexes[start],indexes[posible_end]))

                local_proportion = 1.0 if vals[i] >= threshold else 0.0
                max_val = local_proportion
                posible_end = -1
                start = -1
            i+=1
            if self.progress is not None and i%progressupdate==0:
                self.progress(10 + 5* i/progressupdate)

        if posible_end != -1 and start != -1 and posible_end - start > minSize:
            intervals.append((indexes[start],indexes[posible_end]))

        if self.progress is not None:
            self.progress(25)

        intervals = self.mergeIntervals(intervals,merge_factor)

        if self.progress is not None:
            self.progress(30)

        return [c for c in intervals if (c[1]-c[0]) > minSize]

    #Pure Frecuency
    #Intervals
    def intervals_frecuency_bands_distribution_detector(self,data,threshold,minSize,merge_factor):
        """
        frecuencies highly defined
        """
        #ind,vals = self.localMax(data)
        #vals = diff(vals)
        #_threshold = vals.var()
        #def function(d):
        #    ind,vals = self.localMax(d)
        #    freqs = diff(ind)
        #    v = var(freqs)
        #    sorted_diff = sort(freqs)
        #
        #    return v if mean(vals) > threshold else _threshold
        #
        #return self.interval_detector(data,_threshold,minSize,merge_factor,function,comparer_greater_threshold=False)
        pass

    def intervals_frecuency_distribution_detector(self,data,threshold,minSize,merge_factor):
        """
        Multiple frecs or noise
        uses the property of amplitude of the signal to discard silence intervals
        """
        ind,vals = self.localMax(data)
        vals = diff(vals)
        _threshold = vals.var()
        def function(d):
            ind,vals = self.localMax(d)
            return var(diff(ind)) if mean(vals) > threshold else _threshold

        return self.interval_detector(data,_threshold,minSize,merge_factor,function,comparer_greater_threshold=False)
