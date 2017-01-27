from math import sin, pi
from numpy import where
from duetto import FLOATING_POINT_EPSILON
from duetto.signal_processing.SignalProcessor import SignalProcessor


class CommonSignalProcessor(SignalProcessor):
    """
    Class that provides commonly used functions in signal processing
    """

    def __init__(self, signal=None):
        SignalProcessor.__init__(self, signal)

    def setSilence(self, indexFrom=0, indexTo=-1):
        """
        Sets to zero all the values of the signal data array
        in the specified interval.
        indexFrom and indexTo are the indexes for the interval.
        indexFrom is the beginning and  indexTo is the end of the interval
        by default are indexFrom=0, indexTo=-1
        """
        if indexTo == -1:
            indexTo = len(self.signal)

        # verify if the indexes are correct
        if self.checkIndexesOk(indexFrom, indexTo):
            selected_channel = self.signal.currentChannelIndex
            for channel in range(self.signal.channelCount):
                self.signal.currentChannelIndex = channel
                self.signal.data[indexFrom:indexTo] = 0
            self.signal.currentChannelIndex = selected_channel
            return self.signal
        else:
            raise IndexError()

    def reverse(self, indexFrom=0, indexTo=-1):
        """
        reverse the signal in the interval [indexFrom,indexTo]
         Example:
         data=[1,2,3,4,5]
         reverse()
         data=[5,4,3,2,1]
        """
        if indexTo == -1:
            indexTo = len(self.signal)

        #verify if the indexes are correct
        if self.checkIndexesOk(indexFrom, indexTo):
            selected_channel = self.signal.currentChannelIndex
            for channel in range(self.signal.channelCount):
                self.signal.currentChannelIndex = channel
                data = self.signal.data[indexFrom:indexTo]
                self.signal.data[indexFrom:indexTo] = data[::-1]
            self.signal.currentChannelIndex = selected_channel

            return self.signal
        else:
            raise IndexError()

    def negativesValues(self, indexFrom, indexTo=-1):
        """
        Set the positives values of the signal
        in the interval [indexFrom,indexTo]
        to 0.
        :param indexFrom:
        :param indexTo:
        :return:
        """
        return self.absoluteValue(indexFrom, indexTo, -1)

    def positivesValues(self, indexFrom, indexTo=-1):
        """
        Set the negatives values of the signal
        in the interval [indexFrom,indexTo]
        to 0.
        :param indexFrom:
        :param indexTo:
        :return:
        """
        return self.absoluteValue(indexFrom, indexTo, 1)

    def absoluteValue(self, indexFrom, indexTo=-1, sign=1):
        """
         If sign > 0 the values < 0 would be set to zero
         If sign < 0 the values > 0 would be set to zero
         Example:
         data=[1,-22,3,-4,5]
         result data
         data=[1,22,3,4,5]
        """
        if indexTo == -1:
            indexTo = len(self.signal)

        #verify if the indexes are correct
        if self.checkIndexesOk(indexFrom, indexTo):
            selected_channel = self.signal.currentChannelIndex
            for channel in range(self.signal.channelCount):
                self.signal.currentChannelIndex = channel
                self.signal.data[indexFrom:indexTo] = where(self.signal.data[indexFrom:indexTo] >= 0 if sign > 0
                                                            else
                                                            self.signal.data[indexFrom:indexTo] < 0
                                                            ,
                                                            self.signal.data[indexFrom:indexTo],0)
            self.signal.currentChannelIndex = selected_channel

            return self.signal
        else:
            raise IndexError()

    def changeSign(self, indexFrom, indexTo=-1):
        """
         change the sign of the  values of the signal in the interval [indexFrom,indexTo]
         Example:
         data=[1,-22,3,-4,5]
         data=[-1,22,-3,4,-5]
        """
        if indexTo == -1:
            indexTo = len(self.signal)
        if self.checkIndexesOk(indexFrom, indexTo):
            selected_channel = self.signal.currentChannelIndex
            for channel in range(self.signal.channelCount):
                self.signal.currentChannelIndex = channel
                self.signal.data[indexFrom:indexTo] = -self.signal.data[indexFrom:indexTo]

            self.signal.currentChannelIndex = selected_channel

            return self.signal
        else:
            raise IndexError()

    def normalize(self,indexFrom=0, indexTo=-1, factor=100):
        if indexTo == -1:
            indexTo = len(self.signal)

        if self.checkIndexesOk(indexFrom, indexTo):
            selected_channel = self.signal.currentChannelIndex
            for channel in range(self.signal.channelCount):
                self.signal.currentChannelIndex = channel
                max_value = max(abs(self.signal.data[indexFrom:indexTo]))
                new_max_value = factor * self.signal.maximumValue / 100.0
                self.signal.data[indexFrom:indexTo] *= new_max_value / max_value

            self.signal.currentChannelIndex = selected_channel

            return self.signal
        else:
            raise IndexError()

    def scale(self,indexFrom=0, indexTo=-1, factor=1):
        if abs(factor) < FLOATING_POINT_EPSILON:
            return
        if indexTo == -1:
            indexTo = len(self.signal)
        if self.checkIndexesOk(indexFrom, indexTo):
            selected_channel = self.signal.currentChannelIndex
            for channel in range(self.signal.channelCount):
                self.signal.currentChannelIndex = channel
                self.signal.data[indexFrom:indexTo] *= factor

            self.signal.currentChannelIndex = selected_channel

            return self.signal
        else:
            raise IndexError()

    def modulate(self, indexFrom=0, indexTo=-1,function="normalize", fade="IN"):

        """
        Performs an scale of the signal by a function in the given interval.
        :param indexFrom:
        :param indexTo:
        :param factor:
        :param function:
        :param fade:
        :return: :raise IndexError:
        """
        #get the size of the interval to be scaled. Is indexTo - indexFrom
        interval_length = indexTo - indexFrom if indexTo != -1 else len(self.signal) - indexFrom

        if self.checkIndexesOk(indexFrom, indexTo):
            #defining a local function for scale the interval
            def f(signal_data_index):
                if function == "Linear":
                    if fade == "OUT":
                        return 1 - (signal_data_index * 1.0) / interval_length
                    elif fade == "IN":
                        return (signal_data_index * 1.0) / interval_length
                elif function == "sin":
                    if fade == "OUT":
                        return sin((signal_data_index * 1.0 * pi) / (interval_length * 2) + pi / 2)
                    elif fade == "IN":
                        return sin((signal_data_index * 1.0 * pi) / (interval_length * 2))
                elif function == "sin-sqrt":
                    if fade == "OUT":
                        return (sin((signal_data_index * 1.0 * pi) / (interval_length * 2) + pi / 2)) ** 0.5
                    elif fade == "IN":
                        return (sin((signal_data_index * 1.0 * pi) / (interval_length * 2))) ** 0.5
                elif function == "sin^2":
                    if fade == "OUT":
                        return (sin((signal_data_index * 1.0 * pi) / (interval_length * 2) + pi / 2)) ** 2
                    elif fade == "IN":
                        return (sin((signal_data_index * 1.0 * pi) / (interval_length * 2))) ** 2
                elif function == "cuadratic":
                    if fade == "IN":
                        return (signal_data_index * 1.0 / interval_length) ** 2
                    elif fade == "OUT":
                        return (1 - (signal_data_index * 1.0) / interval_length) ** 2

            #scale the interval values by a function
            self.signal.data[indexFrom:indexTo] = [self.signal.data[indexFrom + index] * f(index) for index in
                                                       range(interval_length)]
            return self.signal
        else:
            raise IndexError()
