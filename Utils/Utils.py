# -*- coding: utf-8 -*-
import os
from PyQt4 import QtGui
from PyQt4.QtGui import QFileDialog

FLOATING_POINT_EPSILON = 0.01


def saveImage(widget, text=""):
    fname = unicode(QFileDialog.getSaveFileName(u"Save " + text + u" as an Image "),
                                                u"-" + text + u"-Duetto-Image", u"*.jpg")
    if fname:
        #save as image
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

    #walk for the folder file system tree
    for root, dirs, filenames in os.walk(folder):
        for f in filenames:
            if any([f.endswith(x) for x in extensions]):
                #if file extension is admissible
                files.append(unicode(root + os.path.sep + f))

    return files