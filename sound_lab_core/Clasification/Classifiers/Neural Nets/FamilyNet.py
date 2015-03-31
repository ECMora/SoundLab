import numpy as np

import Utilities as ut
from sound_lab_core.Clasification.Classifiers.NeuralNet import TransfFunctions, ErrorFunctions, NeuralNet
from sound_lab_core.ParametersMeasurement.Adapters.TimeParametersAdapters.DurationTimeParameterAdapter import DurationTimeParameterAdapter
from sound_lab_core.ParametersMeasurement.Adapters.TimeParametersAdapters.LocalMaxMeanAdapter import LocalMaxMeanParameterAdapter
from sound_lab_core.ParametersMeasurement.Adapters.TimeParametersAdapters.PeakToPeakParameterAdapter import PeakToPeakParameterAdapter
from sound_lab_core.ParametersMeasurement.Adapters.TimeParametersAdapters.RmsTimeParameterAdapter import RmsTimeParameterAdapter
from sound_lab_core.ParametersMeasurement.Adapters.TimeParametersAdapters.StartToMaxTimeParameterAdapter import StartToMaxTimeParameterAdapter
from sound_lab_core.ParametersMeasurement.Adapters.TimeParametersAdapters.ZeroCrossRateAdapter import ZeroCrossRateParameterAdapter
from sound_lab_core.ParametersMeasurement.Adapters.FreqParametersadapters.BandWidthParameterAdapter import BandWidthParameterAdapter
from sound_lab_core.ParametersMeasurement.Adapters.FreqParametersadapters.MaxFreqParameterAdapter import MaxFreqParameterAdapter
from sound_lab_core.ParametersMeasurement.Adapters.FreqParametersadapters.MinFreqParameterAdapter import MinFreqParameterAdapter
from sound_lab_core.ParametersMeasurement.Adapters.FreqParametersadapters.PeakFreqParameterAdapter import PeakFreqParameterAdapter
from sound_lab_core.ParametersMeasurement.Adapters.FreqParametersadapters.PeaksAboveParameterAdapter import PeaksAboveParameterAdapter


classes = ['FL', 'FMC', 'FMCa', 'FML']

X = None
Y = None

for cName in classes:
    folder = 'Segments'+'/'
    Xdata = np.asfarray(ut.deserialize(folder+cName))
    Ydata = [cName for i in xrange(len(Xdata))]
    if X is None:
        X = Xdata
        Y = Ydata
    else:
        X = np.concatenate((X,Xdata))
        Y += Ydata

# X = X * 1. / (X.max(axis=0) + 1)
# maxs = X.max(axis=0)
# mins = X.min(axis=0)
#
# for index in xrange(0,len(maxs)):
#     if maxs[index] == mins[index]:
#         maxs[index] += 1

minmax = [ [-5, 30] for i in np.arange(11)]
paramsList = [DurationTimeParameterAdapter, LocalMaxMeanParameterAdapter,
                       PeakToPeakParameterAdapter, RmsTimeParameterAdapter, StartToMaxTimeParameterAdapter,
                       ZeroCrossRateParameterAdapter, BandWidthParameterAdapter, MaxFreqParameterAdapter, MinFreqParameterAdapter,
                       PeakFreqParameterAdapter, PeaksAboveParameterAdapter]

net = NeuralNet(minmax,classes,paramsList,[6,len(classes)],
                transf=[TransfFunctions.SIGMOID(), TransfFunctions.SIGMOID()],errorf=ErrorFunctions.SSE)

error = net.train((X,Y),epochs=1500, learningRate=0.01, momentum=0.9)

NeuralNet.save(net,'Family.net')