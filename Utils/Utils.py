# -*- coding: utf-8 -*-
import os
import pickle
from PyQt4 import QtGui
from PyQt4.QtGui import QFileDialog

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