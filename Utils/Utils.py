# -*- coding: utf-8 -*-
from io import SEEK_CUR
import os
import pickle
from math import log10
import struct
from PyQt4.QtCore import QThread, pyqtSignal
from numpy import argmax
from PyQt4 import QtGui
from duetto.audio_signals.Synthesizer import Synthesizer


# region Methods
from numpy.compat import asbytes
from scipy.io import wavfile


def deserialize(filename):
    """
    Deserialize an object from a file.
    :param filename: the path to the file where the object is saved
    :return: the instance of tyhe serialized object in the file
    """
    if not os.path.exists(filename):
        raise Exception('File does not exist.')

    with open(filename, 'rb') as f:
        return pickle.load(f)


def serialize(filename, serializable_object):
    """
    Serialize an object to a file.
    :param filename: the path to the file for the object storage.
    :param object: the object to serialize.
    """
    if not filename:
        raise Exception("Invalid Path " + filename + " to save the object.")

    try:

        data_file = open(filename, 'wb')
        pickle.dump(serializable_object, data_file)
        data_file.close()

    except Exception as ex:
        print(ex.message)


def save_image(widget, fname=""):
    """
    Method that saves as image a widget by taking a screenshot of it.
    All the signal graphs save images methods delegate in this one their
    implementation.
    :param widget: The widget to save the screenshot.
    :param fname: File name to save
    """
    if fname:
        # save as image
        image = QtGui.QPixmap.grabWindow(widget.winId())
        image.save(fname, u'jpg')


def folder_files(folder, extensions=None):
    """
    Method that gets all the files that contains a provided folder in
    the file system.
    :param folder: The folder to search files.
    :param extensions: list with admissible file extensions to limit the search
    :return: list of string with path of every detected file.
    """
    # list of files to return
    files = []
    extensions = [u".wav"] if (extensions is None or len(extensions) == 0) else extensions

    # walk for the folder file system tree
    for root, dirs, filenames in os.walk(folder):
        for f in filenames:
            try:
                if any([unicode(f).lower().endswith(unicode(x)) for x in extensions]):
                    # if file extension is admissible

                    files.append(unicode(os.path.join(root, f)))
            except Exception as ex:
                print("Errors in get folder files. On file " + unicode(f) + ". " + ex.message)

    return files


def small_signal(signal, duration_ms=50):
    """
    Computes and return (through an heuristic) an small signal that represent
    the current one. The small signal has less than 100ms of duration and is
    provided as a way of search characteristics of the whole signal. Must be
    "as similar as possible to the complete signal".

    :param signal: The signal to become small
    :param duration_ms: The duration of the small signal to generate from the supplied one in ms
    :return: an AudioSignal.
    """
    if signal is None:
        return Synthesizer.generateSilence(samplingRate=44100, bitDepth=16,
                                           duration=50)

    if signal.duration <= duration_ms / 1000.0:
        return signal

    # small signal
    smaller_signal = Synthesizer.generateSilence(samplingRate=signal.samplingRate, bitDepth=signal.bitDepth,
                                                 duration=duration_ms + 1)

    # ensures that the max amplitude interval is in the small signal
    index_max_amp = argmax(signal.data)

    ms = signal.samplingRate / 1000.0

    index_from = int(max(0, index_max_amp - duration_ms * ms / 2))
    index_to = int(min(signal.length, index_max_amp + duration_ms * ms / 2))

    if index_to - index_from > smaller_signal.length:
        difference = smaller_signal.length - (index_to-index_from)
        index_to -= difference/2
        index_from += difference - difference / 2

    smaller_signal.data[:index_to - index_from] = signal.data[index_from:index_to]

    return smaller_signal


def toDB(value=0, min_value=1, max_value=1):
    return -60 + int(20 * log10(abs(value + max_value * 1000.0 / min_value)))


def fromdB(value_dB=0, min_value=1, max_value=1):
    return round((10.0 ** ((60 + value_dB) / 20.0)) * max_value / 1000.0, 0) - min_value

# endregion


# region Classes

class CallableStartThread(QThread):
    """
    A thread started by a function supplied
    """

    def __init__(self, parent=None, function=None):
        QThread.__init__(self, parent)
        self.function = function if function is not None else lambda: None

    def run(self):
        self.function()


class SegmentationThread(QThread):
    """
    Thread that execute the segmentation of a signal.
    """

    # SIGNALS
    # signal raised when the segmentation is finished
    segmentationFinished = pyqtSignal(list)

    def __init__(self, parent=None, detector=None):
        QThread.__init__(self, parent)
        self._detector = detector

    @property
    def detector(self):
        return self._detector

    @detector.setter
    def detector(self, value):
        if self.isRunning():
            return
        self._detector = value

    def run(self):
        if self.detector is not None:
            self.detector.detect()
            self.segmentationFinished.emit(self.detector.elements)


class MeasurementThread(QThread):

    def __init__(self, parent=None, segment_manager=None):
        QThread.__init__(self, parent)
        self.segment_manager = segment_manager

    def run(self):
        # measure the parameters over elements detected
        self.segment_manager.measure_parameters()

        # classify detected elements
        self.segment_manager.classify_elements()


class RecordThread(QThread):

    def __init__(self, parent=None, player=None):
        QThread.__init__(self, parent)
        self.player = player

    def run(self):
        if self.player is not None:
            self.player.record()

# endregion


# CONSTANTS

FLOATING_POINT_EPSILON = 0.01


DECIMAL_PLACES = 2


WORK_SPACE_FILE_NAME = "soundlab.ini"


def read_wav_metadata(stream):
    """
    Reads a stream that contains an wav signal. Returns a tuple containing sampling rate, bit depth, number of
    channels, user data, and data in that order. Before returning it closes the stream.
    :param stream: An instance of a class derived from io.IOBase.
        The stream from which to read. A call to its readable() and seekable() methods must return True. Its
        contents must be in WAV format, otherwise an exception is raised.
    """
    # read the first chunk (the riff chunk),
    # contains the size and a way to know this is a WAV stream
    fsize = wavfile._read_riff_chunk(stream)

    noc = 1
    bits = 16
    rate = 44100
    userData = ''
    data = None

    # read each chunk
    while stream.tell() < fsize:
        chunk_id = stream.read(4)

        if chunk_id == asbytes('fmt '):
            # read fmt chunk, contains all metadata
            size, comp, noc, rate, sbytes, ba, bits = wavfile._read_fmt_chunk(stream)
        elif chunk_id == asbytes('data'):
            # read data chunk
            if wavfile._big_endian:
                fmt = '>i'
            else:
                fmt = '<i'
            size = struct.unpack(fmt, stream.read(4))[0]
            stream.seek(size, SEEK_CUR)
        else:
            # ignore unknown chunk
            dt = stream.read(4)
            if wavfile._big_endian:
                fmt = '>i'
            else:
                fmt = '<i'
            size = struct.unpack(fmt, dt)[0]
            stream.seek(size, SEEK_CUR)

    stream.close()
    return rate, bits, noc, userData, size