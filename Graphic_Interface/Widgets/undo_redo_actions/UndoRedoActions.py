# -*- coding: utf-8 -*-
from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSignal, QObject
from PyQt4.QtGui import QApplication
from duetto.audio_signals.Synthesizer import Synthesizer
from duetto.signal_processing.EditionSignalProcessor import EditionSignalProcessor
from utils.Utils import FLOATING_POINT_EPSILON
from duetto.signal_processing.CommonSignalProcessor import CommonSignalProcessor
from duetto.signal_processing.filter_signal_processors.frequency_domain_filters import *
import numpy as np


class UndoRedoManager(QObject):
    """
    Data structure for handling undo and redo actions.
    """

    # signal that raise when an action is undo or redo
    actionExec = pyqtSignal(object)

    # signal raised when a new action is added. raise the action
    actionAdded = pyqtSignal(object)

    def __init__(self):
        QObject.__init__(self)

        # initial space for actions
        # list that stores the actions
        self.__actionsList = [None] * 20

        # index that points into the last action processed
        self.actionIndex = -1

    def undo(self):
        """
        Undo the last action.
        """
        if self.actionIndex >= 0:
            action = self.__actionsList[self.actionIndex]
            self.actionIndex -= 1

            if action is not None:
                action.undo()

                self.actionExec.emit(action)

    def redo(self):
        """
        Redo the last action.
        """
        if self.actionIndex < self.count() - 1:
            self.actionIndex += 1
            action = self.__actionsList[self.actionIndex]
            if action is not None:
                action.redo()
                self.actionExec.emit(action)
            else:
                self.actionIndex -= 1

    def add(self, action):
        """
        Add a new action to the object.
        @param action: The undo redo action to add.
        """
        if not isinstance(action, UndoRedoAction):
            return
        self.actionIndex += 1

        if len(self.__actionsList) <= self.actionIndex:
            self.__actionsList = [self.__actionsList[i] if i < len(self.__actionsList) else None for i in range(2*len(self.__actionsList))]

        elif self.actionIndex > 0:
            # deleting all actions after current
            self.__actionsList[self.actionIndex:] = [None] * (len(self.__actionsList) - self.actionIndex)

        self.__actionsList[self.actionIndex] = action

        self.actionAdded.emit(action)

    def clear(self):
        """
        Clear all the actions.
        """
        self.actionIndex = -1
        self.__actionsList = [None] * 20

    def count(self):
        """
        @return: The count of actions stored in the data structure.
        """
        return len([x for x in self.__actionsList if x is not None])

    @property
    def current_action_index(self):
        return self.actionIndex


class UndoRedoAction(QObject):
    """
    Action that is posible make it undo and redo it.
    Its an interface for the implementation of every undo and redo action.
    Contains an undo method and a redo that are called when an undo or redo action its made
    respectivily.
    """
    def __init__(self):
        QObject.__init__(self)

    def undo(self):
        pass

    def redo(self):
        pass


class SignalNameChangeAction(UndoRedoAction):

    # signal raised when the name of the signal is changed by code
    # raise the new name
    signalNameChanged = pyqtSignal(str)

    def __init__(self, signal, new_name):
        UndoRedoAction.__init__(self)
        self.signal = signal
        self.old_name = self.signal.name
        self.new_name = new_name

    def undo(self):
        self.signal.name = self.old_name
        self.signalNameChanged.emit(self.signal.name)

    def redo(self):
        self.signal.name = self.new_name
        self.signalNameChanged.emit(self.signal.name)


class RecordAction(UndoRedoAction):
    """
    A record action over a signal
    """
    def __init__(self, signal):
        UndoRedoAction.__init__(self)
        self.signal = signal

        # update for multiple channels data signals
        # self.signal_data = np.copy(signal.data)
        # self.signal_old_data = signal.copy().data

    def undo(self):
        # self.signal.data = self.signal_old_data
        pass

    def redo(self):
        # self.signal.data = self.signal_data
        pass


class ReverseAction(UndoRedoAction):
    def __init__(self, signal, start, end):
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


class InsertSignalAction(UndoRedoAction):
    def __init__(self,signal,start,ms):
        UndoRedoAction.__init__(self)
        self.signal = signal
        self.start = start
        self.ms = ms

    def undo(self):
        EditionSignalProcessor(self.signal).cut(self.start, self.start + self.ms * self.signal.samplingRate/1000.0)
        # TODO clear the clipboard after cut

    def redo(self):
        pass


class InsertSilenceAction(InsertSignalAction):
    def __init__(self, signal, start, ms):
        InsertSignalAction.__init__(self, signal, start, ms)

    def redo(self):
        silence_signal = Synthesizer.generateSilence(self.signal.samplingRate, self.signal.bitDepth, self.ms)
        self.signal.insert(silence_signal, self.start)


class InsertWhiteNoiseAction(InsertSignalAction):
    def __init__(self, signal, start, ms):
        InsertSignalAction.__init__(self, signal, start, ms)

    def redo(self):
        Synthesizer.insertWhiteNoise(self.signal, self.ms, self.start)


class InsertPinkNoiseAction(InsertSignalAction):
    def __init__(self, signal, start, ms, ftype, Fc, Fl, Fu):
        InsertSignalAction.__init__(self, signal, start, ms)
        self.filterType, self.Fc, self.Fl, self.Fu = ftype, Fc, Fl, Fu

    def redo(self):
        self.signal.generateWhiteNoise(self.ms, self.start)
        FilterSignalProcessor(self.signal).filter(self.start, self.start + self.ms * self.signal.samplingRate / 1000,
                                                  self.filterType, self.Fc, self.Fl, self.Fu)


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
    def __init__(self, signal, start, end, filter_processor):
        UndoRedoAction.__init__(self)
        self.signal = signal
        self.start = start
        self.end = end
        self.filter_processor = filter_processor
        self.losed_signal_data = signal.data[start:end]

    def undo(self):
        self.signal.data[self.start:self.end] = self.losed_signal_data

    def redo(self):
        self.filter_processor.filter(self.start, self.end)


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

# region CUT,COPY,PASTE
class EditionAction(UndoRedoAction):

    def __init__(self, start, end, edition_signal_processor):
        UndoRedoAction.__init__(self)
        self.start = start
        self.end = end
        self.edition_signal_processor = edition_signal_processor
        self.previous_clipboard = self.edition_signal_processor.get_from_clipboard()


class CutAction(EditionAction):

    def __init__(self, start, end, edition_signal_processor):
        EditionAction.__init__(self, start, end, edition_signal_processor)

    def undo(self):
        self.edition_signal_processor.paste(self.start)
        self.edition_signal_processor.put_into_clipboard(self.previous_clipboard)

    def redo(self):
        self.edition_signal_processor.cut(self.start, self.end)


class PasteAction(EditionAction):

    def __init__(self, start, end, edition_signal_processor):
        EditionAction.__init__(self, start, end, edition_signal_processor)

    def undo(self):
        self.edition_signal_processor.cut(self.start, self.end)

    def redo(self):
        self.edition_signal_processor.paste(self.start)


class CopyAction(EditionAction):
    def __init__(self, start, end, edition_signal_processor):
        EditionAction.__init__(self, start, end, edition_signal_processor)

    def undo(self):
        self.edition_signal_processor.put_into_clipboard(self.previous_clipboard)

    def redo(self):
        self.edition_signal_processor.copy(self.start, self.end)

# endregion


class Absolute_ValuesAction(UndoRedoAction):
    def __init__(self, signal, start, end, sign):
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