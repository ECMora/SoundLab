from PyQt4.QtGui import QDialog
from Graphic_Interface.Dialogs.ui_elemDetectSettings import Ui_elemDetectSettingsDialog


class ElemDetectSettingsDialog(Ui_elemDetectSettingsDialog, QDialog):
    def __init__(self, parent=None, winfdow_flags=0):
        QDialog.__init__(self, parent, flags)
