from PyQt4.QtGui import *
from PyQt4.QtCore import *
import PyQt4.phonon as phonon
import os,hashlib
from Graphic_Interface.Windows.DuettoSoundLabWindow import DuettoSoundLabWindow
from Graphic_Interface.Windows.PresentationSlogan.presentation import Ui_MainWindow


class Duetto_Sound_Lab(QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None,path=""):
        super(Duetto_Sound_Lab, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.SplashScreen)
        if path != "":
            self.videoPlayer.load(phonon.Phonon.MediaSource(path))


def validLicense():
    try:
        drives = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y", "Z"]
        for p in drives:
            x = p + ":" + os.sep
            if os.path.exists(x) and os.path.exists(os.path.join(x,"duetto")):
                result = hashlib.md5(open(os.path.join(x,"duetto")).readline()).hexdigest() == "b41b3527dd6c497c67d0f67a642574ea"
                if result:
                    return True
    except:
        pass
    return False


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    dmw = DuettoSoundLabWindow()
    path = os.path.join(os.path.join("Utils","PresentationVideo"),"duettoinit.mp4")
    duetto_sound_lab_window = Duetto_Sound_Lab(path=path if os.path.exists(path) else "")

    def s():
        dmw.show()
        duetto_sound_lab_window.close()
    ## show it
    if os.path.exists(path):
        duetto_sound_lab_window.videoPlayer.finished.connect(s)
        duetto_sound_lab_window.show()
        duetto_sound_lab_window.videoPlayer.play()
    else:
        s()
    s()
    # create the GUI application
    # show it
    if validLicense():
        sys.exit(app.exec_())
    else:
         QMessageBox.warning(QMessageBox(), "Error",
                                        "Your Duetto Sound Lab Licence its expired or has some troubles.\n"
                                        " Could be because your trial version is over. Try to open again.")
         sys.exit(0)

    # start the Qt main loop execution, exiting from this script
    # with the same return code of Qt application
