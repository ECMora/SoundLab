import pyaudio
from PyAudioDevice import PyAudioDevice


class DevicesHandler(object):
    """
    Static class that handles the input and output devices from a fixed available set.
    """

    @staticmethod
    def getInputDevices():
        """
        This is a static public function to find all available input sound devices from the computer
        :return: input is a list of input Devices instances respectively
        """
        pa = pyaudio.PyAudio()
        input = []

        devices_count = pa.get_device_count()

        # for each audio device, determine if is an input or an output and add it to the appropriate list.
        for i in range(devices_count):
            device_info = pa.get_device_info_by_index(i)

            if device_info.get(u'maxInputChannels') > 0:
                device = PyAudioDevice(device_info)
                input.append(device)

        pa.terminate()

        return input

    @staticmethod
    def getOutputDevices():
        """
        This is a static public function to find all available output sound devices from the computer
        :return: output is a list of output Devices instances respectively
        """
        pa = pyaudio.PyAudio()
        output = []

        devices_count = pa.get_device_count()

        # a list comprehension implementation
        # output = [PyAudioDevice(pa.get_device_info_by_index(i))
        #           for i in range(devices_count) if pa.get_device_info_by_index(i).get('maxOutputChannels') > 0]

        # A better understandable implementation

        # for each audio device,
        # determine if is an input or an output and add it to the appropriate list.
        for i in range(devices_count):
            device_info = pa.get_device_info_by_index(i)

            if device_info.get(u'maxOutputChannels') > 0:
                device = PyAudioDevice(device_info)
                output.append(device)

        pa.terminate()

        return output