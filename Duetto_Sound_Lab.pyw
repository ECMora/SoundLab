# -*- coding: utf-8 -*-
import os
import hashlib
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from utils.Utils import deserialize, WORK_SPACE_FILE_NAME, CallableStartThread
from graphic_interface.Settings.Workspace import Workspace
from graphic_interface.windows.SoundLabMainWindow import SoundLabMainWindow
from graphic_interface.windows.PresentationSlogan.presentation import Ui_MainWindow
from graphic_interface.segment_visualization.VisualItemsCache import VisualItemsCache
from utils.db.DB_ORM import clean_db

invalid_license_message = " A valid duetto Sound Lab license is missing or your trial period is over.\n" + \
                          " If you have a valid license try to open the application again, otherwise" + \
                          " contact duetto support team for information."


class DuettoSoundLab(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, path=""):
        super(DuettoSoundLab, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.SplashScreen)
        # if path != "":
        # self.videoPlayer.load(phonon.Phonon.MediaSource(path))


def valid_license():
    return True
    try:
        drives = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                  "U", "V", "W", "X", "Y", "Z"]
        for p in drives:
            x = p + ":" + os.sep
            if os.path.exists(x) and os.path.exists(os.path.join(x, "duetto")):
                result = hashlib.md5(
                    open(os.path.join(x, "duetto")).readline()).hexdigest() == "b41b3527dd6c497c67d0f67a642574ea"
                if result:
                    return True
    except Exception as e:
        pass
    return False


def check_license():
    """
    Check the license validness and close the
    app with no valid license message if the license fails
    :return:
    """
    if not valid_license():
        finish()


def finish(message=invalid_license_message):
    """
    End the application with the invalid license message
    :return:
    """
    QMessageBox.warning(QMessageBox(), "Error", message)
    sys.exit(0)


def load_app_style(qApp=None, style_file=None):
    """
    Load the style to the app
    :param qApp: The QApplication to load the style in.
    :return:
    """
    try:
        if qApp is None:
            return

        if style_file is not None and os.path.exists(style_file):
            qss = QFile(style_file)
            qss.open(QIODevice.ReadOnly | QIODevice.Text)
            qApp.setStyleSheet(QString(qss.readAll()))
            qss.close()

    except Exception as ex:
        print("error loading app style. " + ex.message)


def create_visual_item_cache():
    VisualItemsCache()


def load_language_translations(app=None, translation_file=None, window=None):
    """
    Load the language I18n to an app.
    :param app:  The QApplication to load the language.
    :return:
    """
    try:
        if app is None:
            return

        # load a supplied translation
        if translation_file is not None and os.path.exists(translation_file):
            translator = QTranslator()
            if translator.load(translation_file):
                app.installTranslator(translator)
                if window:
                    window.retranslateUi(window)
            return
        else:
            locale = QLocale.system().name()
            qt_translator = QTranslator()

            # install localization if any exists
            if qt_translator.load(locale, "I18n\\"):
                app.installTranslator(qt_translator)

    except Exception as ex:
        print("error loading language I18n to the app. " + ex.message)


if __name__ == '__main__':
    from pyqtgraph import setConfigOptions
    # pyqtgraph option to not use weave to speed up some operations
    setConfigOptions(useWeave=False)

    app = QApplication(sys.argv)
    app.setEffectEnabled(Qt.UI_FadeMenu)
    app.setEffectEnabled(Qt.UI_AnimateCombo)
    app.setEffectEnabled(Qt.UI_AnimateMenu)
    app.setEffectEnabled(Qt.UI_AnimateToolBox)
    app.setEffectEnabled(Qt.UI_AnimateTooltip)

    args = sys.argv[1] if len(sys.argv) > 1 else ''

    workspace_path = os.path.join("Utils", WORK_SPACE_FILE_NAME)
    workSpace = None
    try:
        clean_db()

    except Exception as ex:
        print("Error cleaning the db. " + ex.message)

    if os.path.exists(workspace_path):
        workSpace = deserialize(workspace_path)

        if isinstance(workSpace, Workspace):

            # load_language_translations(app, workSpace.language)
            load_app_style(app, workSpace.style)
        else:
            workSpace = None

    dmw = SoundLabMainWindow(signal_path=args, workSpace=workSpace)

    dmw.languageChanged.connect(lambda data: load_language_translations(app, data, dmw))
    dmw.styleChanged.connect(lambda data: load_app_style(app, data))

    license_checker_timer = QTimer()
    license_checker_timer.timeout.connect(check_license)

    if valid_license():
        license_checker_timer.start(1000)

        # create items
        create_visual_item_cache()
        dmw.show()

        sys.exit(app.exec_())

    else:
        finish()