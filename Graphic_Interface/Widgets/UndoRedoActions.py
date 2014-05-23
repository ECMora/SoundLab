# -*- coding: utf-8 -*-

from Duetto_Core.SignalProcessors.CommonSignalProcessor import CommonSignalProcessor
from Duetto_Core.SignalProcessors.FilterSignalProcessor import FilterSignalProcessor

import numpy as np


class UndoRedoManager:
    def __init__(self,widget):
        self.widget = widget
        self.actionsList = [None for _ in range(20)] #initial space for actions
        self.actionIndex = -1

    def undo(self):
        if(self.actionIndex >= 0):
            action = self.actionsList[self.actionIndex]
            if action is not None:
                action.undo()
                self.widget.visualChanges = True
                self.widget.refresh()
            self.actionIndex -= 1

    def redo(self):
        if self.actionIndex < len(self.actionsList)-1:
            self.actionIndex += 1
            action = self.actionsList[self.actionIndex]
            if action is not None:
                action.redo()
                self.widget.visualChanges = True
                self.widget.refresh()


    def addAction(self,action):
        self.actionIndex += 1
        if(len(self.actionsList) <= self.actionIndex):
            self.actionsList = [self.actionsList[i] if i < len(self.actionsList) else None for i in range(2*len(self.actionsList))]
        elif self.actionIndex > 0:
            for i in range(self.actionIndex,len(self.actionsList)):
                self.actionsList[i] = None
        self.actionsList[self.actionIndex] = action

    def clearActions(self):
        self.actionIndex = 0
        for i in range(len(self.actionsList)):
            self.actionsList[i] = None

    def count(self):
        return self.actionIndex+1


class UndoRedoAction:
    def __init__(self, undo, redo):
        assert callable(undo) and callable(redo)
        self.undo = undo
        self.redo = redo


class ReverseAction(UndoRedoAction):
    def __init__(self,signal,start,end):
        self.signal = signal
        self.start = start
        self.end = end

    def undo(self):
        CommonSignalProcessor(self.signal).reverse(self.start,self.end)

    def redo(self):
        CommonSignalProcessor(self.signal).reverse(self.start,self.end)


class ChangeSignAction(UndoRedoAction):
    def __init__(self,signal,start,end):
        self.signal = signal
        self.start = start
        self.end = end

    def undo(self):
        CommonSignalProcessor(self.signal).changeSign(self.start,self.end)

    def redo(self):
        CommonSignalProcessor(self.signal).changeSign(self.start,self.end)


class SilenceAction(UndoRedoAction):
    def __init__(self,signal,start,end):
        self.signal = signal
        self.start = start
        self.end = end
        self.data = np.array(signal.data[start:end])

    def undo(self):
        for i in range(self.start,self.end):
            self.signal.data[i] = self.data[i-self.start]

    def redo(self):
        CommonSignalProcessor(self.signal).setSilence(self.start,self.end)


class InsertSilenceAction(UndoRedoAction):
    def __init__(self,signal,start,ms):
        self.signal = signal
        self.start = start
        self.ms = ms

    def undo(self):
        self.signal.data = np.concatenate((self.signal.data[:self.start],self.signal.data[self.start+int(self.ms*self.signal.samplingRate/1000.0):]))

    def redo(self):
        CommonSignalProcessor(self.signal).insertSilence(self.start,ms=self.ms)


class ScaleAction(UndoRedoAction):
    def __init__(self,signal,start,end,factor, function, fade):
        self.signal = signal
        self.start = start
        self.end = end
        self.factor,self.function,self.fade= factor,function,fade
        self.data = np.array(signal.data[start:end])

    def undo(self):
        for i in range(self.start,self.end):
            self.signal.data[i] = self.data[i-self.start]

    def redo(self):
        CommonSignalProcessor(self.signal).scale(self.start,self.end,self.factor, self.function, self.fade)


class FilterAction(UndoRedoAction):
    def __init__(self,signal,start,end,filterType,Fc,Fl,Fu):
        self.signal = signal
        self.start = start
        self.end = end
        self.filterType,self.Fc,self.Fl,self.Fu = filterType,Fc,Fl,Fu
        self.data = np.array(signal.data[start:end])

    def undo(self):
        for i in range(self.start,self.end):
            self.signal.data[i] = self.data[i-self.start]

    def redo(self):
        FilterSignalProcessor(self.signal).filter(self.start,self.end,self.filterType,self.Fc,self.Fl,self.Fu)


class ResamplingAction(UndoRedoAction):
    def __init__(self,signal,sr):
        self.signal = signal
        self.oldsr = signal.samplingRate
        self.sr = sr

    def undo(self):
        self.signal.resampling(self.oldsr)

    def redo(self):
        self.signal.resampling(self.sr)


class GenerateWhiteNoiseAction(UndoRedoAction):
    def __init__(self,signal,start,ms):
        self.signal = signal
        self.start = start
        self.ms = ms

    def undo(self):
        self.signal.data= np.concatenate((self.signal.data[:self.start],self.signal.data[self.start+int(self.ms*self.signal.samplingRate/1000.0):]))

    def redo(self):
        self.signal.generateWhiteNoise(self.ms,self.start)


class GeneratePinkNoiseAction(UndoRedoAction):
    def __init__(self,signal,start,ms, ftype, Fc, Fl, Fu):
        self.signal = signal
        self.start = start
        self.ms = ms
        self.filterType,self.Fc,self.Fl,self.Fu = ftype,Fc,Fl,Fu


    def undo(self):
        self.signal.data= np.concatenate((self.signal.data[:self.start],self.signal.data[self.start+int(self.ms*self.signal.samplingRate/1000.0):]))

    def redo(self):
        self.signal.generateWhiteNoise(self.ms,self.start)
        FilterSignalProcessor(self.signal).filter(self.start,self.start + self.ms*self.signal.samplingRate/1000,self.filterType,self.Fc,self.Fl,self.Fu)


class CutAction(UndoRedoAction):
    def __init__(self,signal,start,end):
        self.signal = signal
        self.start = start
        self.end = end
        self.data = np.array(signal.data[start:end])

    def undo(self):
        self.signal.data = np.concatenate((self.signal.data[:self.start], self.data, self.signal.data[self.start+1:]))

    def redo(self):
        self.signal.data = np.concatenate((self.signal.data[:self.start], self.signal.data[self.end:]))


class PasteAction(UndoRedoAction):
    def __init__(self,signal,start,clipboard):
        self.signal = signal
        self.start = start
        self.end = start + len(clipboard)
        self.data = clipboard

    def redo(self):
        self.signal.data = np.concatenate((self.signal.data[:self.start], self.data, self.signal.data[self.start+1:]))

    def undo(self):
        self.signal.data = np.concatenate((self.signal.data[:self.start], self.signal.data[self.end:]))


class Absolute_ValuesAction(UndoRedoAction):
    def __init__(self,signal,start,end,sign):
        self.signal = signal
        self.start = start
        self.end = end
        self.sign = sign
        self.data = np.array(signal.data[start:end])

    def undo(self):
        for i in range(self.start,self.end):
            self.signal.data[i] = self.data[i-self.start]

    def redo(self):
        CommonSignalProcessor(self.signal).absoluteValue(self.start,self.end,self.sign)