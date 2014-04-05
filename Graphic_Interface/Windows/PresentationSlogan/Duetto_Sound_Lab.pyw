from PyQt4.QtGui import *
from PyQt4.QtCore import *
import PyQt4.phonon as phonon

from Graphic_Interface.Windows.DuettoSoundLabWindow import DuettoSoundLabMAinWindow
from Graphic_Interface.Windows.PresentationSlogan.presentation import Ui_MainWindow


class Duetto_Sound_Lab(QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None):
        super(Duetto_Sound_Lab, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.SplashScreen)
        self.videoPlayer.load(phonon.Phonon.MediaSource("..\\..\\PresentationVideo\\duettoinit.wmv"))


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    dmw = DuettoSoundLabMAinWindow()

    duetto_sound_lab_window = Duetto_Sound_Lab()
    # show it

    def s():
        dmw.show()
        duetto_sound_lab_window.close()

    duetto_sound_lab_window.videoPlayer.finished.connect(s)
    duetto_sound_lab_window.show()
    duetto_sound_lab_window.videoPlayer.play()
    s()
    # create the GUI application
    # show it
    #dmw.show()
    sys.exit(app.exec_())
    # start the Qt main loop execution, exiting from this script
    # with the same return code of Qt application
