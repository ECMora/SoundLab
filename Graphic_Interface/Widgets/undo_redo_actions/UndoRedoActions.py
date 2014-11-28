# -*- coding: utf-8 -*-
from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSignal, QObject
from PyQt4.QtGui import QApplication
from duetto.signal_processing.EditionSignalProcessor import EditionSignalProcessor
from Utils.Utils import FLOATING_POINT_EPSILON
from duetto.signal_processing.CommonSignalProcessor import CommonSignalProcessor
from duetto.signal_processing.filter_signal_processors.frequency_domain_filters import *
import numpy as np


class UndoRedoManager(QObject):
    """
    Data structure for handling undo and redo actions.
    """
    #signal that raise when an action is undo or redo
    actionExec = pyqtSignal(object)

    def __init__(self):
        QObject.__init__(self)

        #initial space for actions
        #list that stores the actions
        self.__actionsList = [None] * 20

        #index that points into the last action processed
        self.__actionIndex = -1

    def undo(self):
        """
        Undo the last action.
        """
        if self.__actionIndex >= 0:
            action = self.__actionsList[self.__actionIndex]
            if action is not None:
                action.undo()
                self.actionExec.emit(action)
            self.__actionIndex -= 1

    def redo(self):
        """
        Redo the last action.
        """
        if self.__actionIndex < self.count() - 1:
            self.__actionIndex += 1
            action = self.__actionsList[self.__actionIndex]
            if action is not None:
                action.redo()
                self.actionExec.emit(action)
            else:
                self.__actionIndex -= 1

    def add(self,action):
        """
        Add a new action to the object.
        @param action: The undo redo action to add.
        """
        if not isinstance(action, UndoRedoAction):
            return
        self.__actionIndex += 1
        if len(self.__actionsList) <= self.__actionIndex:
            self.__actionsList = [self.__actionsList[i] if i < len(self.__actionsList) else None for i in range(2*len(self.__actionsList))]
        elif self.__actionIndex > 0:
            #borrando las acciones que antes estaban por rehacer
            self.__actionsList[self.__actionIndex:] = [None] * (len(self.__actionsList) - self.__actionIndex)
        self.__actionsList[self.__actionIndex] = action

    def clear(self):
        """
        Clear all the actions.
        """
        self.__actionIndex = -1
        self.__actionsList = [None] * 20

    def count(self):
        """
        @return: The count of actions stored in the data structure.
        """
        return len([x for x in self.__actionsList if x is not None])


class UndoRedoAction(QObject):
    """
    Action that is posible make it undo and redo it.
    Its an interface for the implementation of every undo and redo action.
    Contains an undo method and a redo that are called when an undo or redo action its made
    respectivily.
    """
    # SIGNALS
    #signal raised when an action are performed and
    #the signal size is changed. Raise the new changed signal
    signal_size_changed = pyqtSignal(object)

    def __init__(self):
        QObject.__init__(self)

    def undo(self):
        pass

    def redo(self):
        pass


class ReverseAction(UndoRedoAction):
    def __init__(self,signal,start,end):
        UndoRedoAction.__init__(self)
        self.signal = signal
        self.start = start
        self.end = end

    def undo(self):
        CommonSignalProcessor(self.signal).reverse(self.start,self.end)

    def redo(self):
        CommonSignalProcessor(self.signal).reverse(self.start,self.end)


class ChangeSignAction(UndoRedoAction):
    def __init__(self,signal,start,end):
        UndoRedoAction.__init__(self)
        self.signal = signal
        self.start = start
        self.end = end

    def undo(self):
        CommonSignalProcessor(self.signal).changeSign(self.start,self.end)

    def redo(self):
        CommonSignalProcessor(self.signal).changeSign(self.start,self.end)


class SilenceAction(UndoRedoAction):
    def __init__(self,signal,start,end):
        UndoRedoAction.__init__(self)
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
        UndoRedoAction.__init__(self)
        self.signal = signal
        self.start = start
        self.ms = ms

    def undo(self):
        self.signal.data = np.concatenate((self.signal.data[:self.start],self.signal.data[self.start+int(self.ms*self.signal.samplingRate/1000.0):]))

    def redo(self):
        CommonSignalProcessor(self.signal).insertSilence(self.start,ms=self.ms)


class ModulateAction(UndoRedoAction):
    def __init__(self,signal,start,end,function, fade):
        UndoRedoAction.__init__(self)
        self.signal = signal
        self.start = start
        self.end = end
        self.function, self.fade = function,fade
        self.data = np.array(signal.data[start:end])

    def undo(self):
        for i in range(self.start,self.end):
            self.signal.data[i] = self.data[i - self.start]

    def redo(self):
        CommonSignalProcessor(self.signal).modulate(self.start,self.end, self.function, self.fade)


class ScaleAction(UndoRedoAction):
    def __init__(self, signal, start, end, factor):
        UndoRedoAction.__init__(self)
        if abs(factor) < FLOATING_POINT_EPSILON:
            raise Exception("The factor is to small for scale. Use silence instead.")
        self.signal = signal
        self.start = start
        self.end = end
        self.factor = factor
        self.inverse_factor = 1.0 / self.factor

    def undo(self):
        CommonSignalProcessor(self.signal).scale(self.start, self.end, self.inverse_factor)

    def redo(self):
        CommonSignalProcessor(self.signal).scale(self.start, self.end, self.factor)


class NormalizeAction(UndoRedoAction):
    def __init__(self, signal, start, end, factor):
        UndoRedoAction.__init__(self)
        self.signal = signal
        self.start = start
        self.end = end
        self.factor = factor
        self.inverse_factor = max(signal.data[start:end]) * 100.0 / signal.maximumValue

    def undo(self):
        CommonSignalProcessor(self.signal).normalize(self.start, self.end, self.inverse_factor)

    def redo(self):
        CommonSignalProcessor(self.signal).normalize(self.start, self.end, self.factor)


class FilterAction(UndoRedoAction):
    def __init__(self,signal,start,end,filterType,Fc,Fl,Fu):
        UndoRedoAction.__init__(self)
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
        UndoRedoAction.__init__(self)
        self.signal = signal
        self.oldsr = signal.samplingRate
        self.sr = sr

    def undo(self):
        self.signal.resampling(self.oldsr)

    def redo(self):
        self.signal.resampling(self.sr)


class GenerateWhiteNoiseAction(UndoRedoAction):
    def __init__(self,signal,start,ms):
        UndoRedoAction.__init__(self)
        self.signal = signal
        self.start = start
        self.ms = ms

    def undo(self):
        self.signal.data= np.concatenate((self.signal.data[:self.start],self.signal.data[self.start+int(self.ms*self.signal.samplingRate/1000.0):]))

    def redo(self):
        self.signal.generateWhiteNoise(self.ms,self.start)


class GeneratePinkNoiseAction(UndoRedoAction):
    def __init__(self,signal,start,ms, ftype, Fc, Fl, Fu):
        UndoRedoAction.__init__(self)
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
        UndoRedoAction.__init__(self)
        self.signal = signal
        self.start = start
        self.end = end
        self.editionProcesor = EditionSignalProcessor(self.signal)
        self.editionProcesor.signal_size_changed.connect(lambda :self.signal_size_changed.emit(self.signal))

    def undo(self):
       self.editionProcesor.paste(self.start)

    def redo(self):
        self.editionProcesor.cut(self.start, self.end)


class CopyAction(UndoRedoAction):
    def __init__(self, signal, start, end):
        UndoRedoAction.__init__(self)
        self.signal = signal
        self.start = start
        self.end = end
        self.editionProcesor = EditionSignalProcessor(self.signal)

    def undo(self):
        mime_data = QtCore.QMimeData()
        mime_data.setData("signal", QtCore.QByteArray(""))
        clip = QApplication.clipboard()
        clip.setMimeData(mime_data)

    def redo(self):
        self.editionProcesor.copy(self.start, self.end)


class PasteAction(UndoRedoAction):

    def __init__(self,signal,start,end):
        UndoRedoAction.__init__(self)
        self.signal = signal
        self.start = start
        self.end = end
        self.editionProcesor = EditionSignalProcessor(self.signal)
        self.editionProcesor.signal_size_changed.connect(lambda: self.signal_size_changed.emit(self.signal))

    def undo(self):
        self.editionProcesor.cut(self.start, self.end)

    def redo(self):
        self.editionProcesor.paste(self.start)


class Absolute_ValuesAction(UndoRedoAction):
    def __init__(self,signal,start,end,sign):
        UndoRedoAction.__init__(self)
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