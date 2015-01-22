from PyQt4.QtGui import QDialog
from graphic_interface.windows.ui_python_files import SoundDevicesDialog as sdDialog
from duetto.sound_devices.DevicesHandler import DevicesHandler


class SoundDevicesDialog(sdDialog.Ui_Dialog, QDialog):
    """
    Dialog that allow to select the sound device to play and record
    the signals. (Select inpuit and output sound devices from the installed on the
    computer)
    """
    # CONSTANTS
    # the static dictionary that memorize the dialog
    # element values during the application execution
    # region dialog elements values

    dialogValues = {'input_selected_index': 0,
                    'output_selected_index': 0}
    # endregion

    def __init__(self):
        """
        Initialize the dialogs elements with their last value
        """
        QDialog.__init__(self)
        self.setupUi(self)

        # active devices
        self.input_devices = DevicesHandler.getInputDevices()
        self.output_devices = DevicesHandler.getOutputDevices()

        self.inputDevice_cbox.currentIndexChanged.connect(
            lambda i: self.inputDevice_lbl.setText(self.inputDevice_cbox.itemText(i)))

        self.outputDevice_cbox.currentIndexChanged.connect(
            lambda j: self.outputDevice_lbl.setText(self.outputDevice_cbox.itemText(j)))

        for index, device in enumerate(self.input_devices):
            self.inputDevice_cbox.addItem(unicode(device))

        for index, device in enumerate(self.output_devices):
            self.outputDevice_cbox.addItem(unicode(device))

        self.load_values()
        self.btonaceptar.clicked.connect(self.save_values)

    # region memoization of selected previous values

    def load_values(self):
        """
        Load into the dialog elements the previously
        or default values.
        """
        if self.inputDevice_cbox.count() > 0:
            self.inputDevice_cbox.setCurrentIndex(self.dialogValues['input_selected_index'])

        if self.outputDevice_cbox.count() > 0:
            self.outputDevice_cbox.setCurrentIndex(self.dialogValues['output_selected_index'])

    def save_values(self):
        """
        Load into the dialog elements the previously
        or default values.
        """
        if self.inputDevice_cbox.count() > 0:
            self.dialogValues['input_selected_index'] = self.inputDevice_cbox.currentIndex()

        if self.outputDevice_cbox.count() > 0:
            self.dialogValues['output_selected_index'] = self.outputDevice_cbox.currentIndex()

    # endregion

    @property
    def inputDevice(self):
        return self.input_devices[self.inputDevice_cbox.currentIndex()]

    @property
    def outputDevice(self):
        return self.output_devices[self.outputDevice_cbox.currentIndex()]

