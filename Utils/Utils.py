# -*- coding: utf-8 -*-
import os
import pickle
from math import log10
from numpy import argmax
from PyQt4 import QtGui
from PyQt4.QtGui import QFileDialog
from duetto.audio_signals.Synthesizer import Synthesizer

FLOATING_POINT_EPSILON = 0.01


DECIMAL_PLACES = 2


WORK_SPACE_FILE_NAME = "soundlab.ini"


def deSerialize(filename):
        """
        Deserialize an object from a file.
        :param filename: the path to the file where the object is saved
        :return: the instance of tyhe serialized object in the file
        """
        if not os.path.exists(filename):
            raise Exception('File does not exist.')

        with open(filename, 'r') as f:
            return pickle.load(f)


def serialize(filename, serializable_object):
        """
        Serialize an obeject to a file.
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


def saveImage(widget, text=""):
    """
    Method that saves as image a widget by taking a screenshot of it.
    All the signal graphs save images methods delegate in this one their
    implementation.
    :param widget: The widget to save the screenshot.
    :param text: Alternative image name to specify the widget or graph source of the picture.
    """
    parent = None
    fname = unicode(QFileDialog.getSaveFileName(parent, u"Save " + text + u" as an Image ",
                                                u"-" + text + u"-Duetto-Image", u"*.jpg"))
    if fname:
        # save as image
        image = QtGui.QPixmap.grabWindow(widget.winId())
        image.save(fname, u'jpg')


def folderFiles(folder, extensions=None):
    """
    Method that gets all the files that contains a provided folder in
    the file system.
    :param folder: The folder to search files.
    :param extensions: list with admissible file extensions to limit the search
    :return: list of string with path of every detected file.
    """
    # list of files to return
    files = []
    extensions = [".wav"] if (extensions is None or len(extensions) == 0) else extensions

    # walk for the folder file system tree
    for root, dirs, filenames in os.walk(folder):
        for f in filenames:
            if any([str(f).endswith(x) for x in extensions]):
                # if file extension is admissible
                files.append(unicode(root + "/" + f))

    return files


def smallSignal(signal, duration_ms=50):
    """
    computes and return (through an heuristic) an small signal
    that represent the current one. The small signal has less than 100ms of duration
    and is provided as a way of search characteristics of the whole signal.
    Must be "as similar as possible to the complete signal".
    :param duration_ms: The duration of the smal signal to genrate from the supplied one in ms
    :return: Audio signal.
    """
    if signal.duration < duration_ms / 1000.0:
        return signal

    return signal.copy(0, duration_ms * signal.samplingRate / 1000.0)

    if signal.duration < duration_ms / 1000.0:
        return signal

    # small signal
    small_signal = Synthesizer.generateSilence(samplingRate=signal.samplingRate, bitDepth=signal.bitDepth, duration=duration_ms)

    # garantize that the mas amplitude interval is in the small signal
    index_max_amp = argmax(signal.data)

    ms = signal.samplingRate / 1000.0

    index_from = max(0, index_max_amp - duration_ms * ms / 2)
    index_to   = min(small_signal.length, index_max_amp + duration_ms * ms / 2)

    print(index_from,index_to,index_max_amp)
    small_signal.data[0: index_to-index_from] = signal.data[index_from:index_to]

    return small_signal


def toDB(value=0, min_value=1, max_value=1):
    return -60 + int(20 * log10(abs(value + max_value * 1000.0 / min_value)))


def fromdB(value_dB=0, min_value=1, max_value=1):
    return round((10.0 ** ((60 + value_dB) / 20.0)) * max_value / 1000.0, 0) - min_value

