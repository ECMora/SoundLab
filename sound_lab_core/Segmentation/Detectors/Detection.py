class AutomaticThresholdType:
    UserDefined = 0
    Global_MaxMean = 1
    Global_MaxMean_Sdv = 2
    Global_MaxMean_Half_Sdv = 3
    Global_MaxMean_Two_Sdv = 4
    Local_MaxMean = 5
    Local_MaxMean_Sdv = 6
    Local_MaxMean_Half_Sdv = 7
    Local_MaxMean_Two_Sdv = 8


class DetectionType:
    LocalMax = 0
    LocalHoldTime = 1
    LocalMaxProportion = 2
    IntervalRms = 3
    IntervalMaxMedia = 4
    IntervalMaxProportion = 5
    IntervalFrecuencies = 6
    Envelope_Abs_Decay_Averaged = 7
    Envelope_Rms = 8


class DetectionSettings:
    def __init__(self, detectiontype, automaticthresholdtype):
        self.detectiontype = detectiontype
        self.automaticthresholdtype = automaticthresholdtype

