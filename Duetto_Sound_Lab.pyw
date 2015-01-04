# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os, hashlib
import sys
from graphic_interface.windows.DuettoSoundLabWindow import DuettoSoundLabWindow
from graphic_interface.windows.PresentationSlogan.presentation import Ui_MainWindow


invalid_license_message = " Valid duetto Sound Lab license is missing or trial period is over.\n" + " If you have a valid license try to open the application again, otherwise" + " contact duetto support team."


class Duetto_Sound_Lab(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, path=""):
        super(Duetto_Sound_Lab, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.SplashScreen)
        # if path != "":
        # self.videoPlayer.load(phonon.Phonon.MediaSource(path))


def validLicense():
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
    except:
        pass
    return False


def loadAppStyle(qApp):
    """
    Load the style to the app
    :param qApp: The QApplication to load the style in.
    :return:
    """
    try:

        qss = QFile("styles/default.qss")
        qss.open(QIODevice.ReadOnly | QIODevice.Text)
        qApp.setStyleSheet(QString(qss.readAll()))
        qss.close()

    except Exception as ex:
        print("error loading app style. " + ex.message)


def loadLanguageTranslations(qApp):
    """
    Load the language I18n to an app.
    :param qApp:  The QApplication to load the language.
    :return:
    """
    try:

        locale = QLocale.system().name()
        qtTranslator = QTranslator()
        if qtTranslator.load(locale, "I18n\\"):
            app.installTranslator(qtTranslator)

    except Exception as ex:
        print("error loading language I18n to the app. " + ex.message)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    loadAppStyle(app)

    loadLanguageTranslations(app)

    # region Start Splash Screen Window
    dmw = DuettoSoundLabWindow()
    # path = os.path.join(os.path.join("Utils", "PresentationVideo"), "duettoinit.mp4")
    # duetto_sound_lab_window = Duetto_Sound_Lab(path=path if os.path.exists(path) else "")

    # def closeSplashScreenWindow():
    #     dmw.show()
    #     duetto_sound_lab_window.close()

    # show it

    # if os.path.exists(path):
    #     # duetto_sound_lab_window.videoPlayer.finished.connect(s)
    #     duetto_sound_lab_window.show()
    #     # duetto_sound_lab_window.videoPlayer.play()
    # else:
    #     closeSplashScreenWindow()
    #
    # closeSplashScreenWindow()

    # endregion

    if validLicense():
        # start the Qt main loop execution, exiting from this script
        # with the same return code of Qt application
        dmw.show()
        sys.exit(app.exec_())


    else:
        QMessageBox.warning(QMessageBox(), "Error",invalid_license_message)
        sys.exit(0)