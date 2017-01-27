# -*- coding: utf-8 -*-
import matplotlib.mlab as mlab
import numpy


class WindowFunction:
    """
    Class to group several window functions for signal processing
    """

    @staticmethod
    def Hanning(M):
        return numpy.hanning(len(M))*M

    @staticmethod
    def Rectangular(M):
        """
        :param M:
        :return:
        """
        return numpy.kaiser(len(M),0)
        # i = numpy.argmax(M)
        # r = len(M) - i - 1
        #
        # return numpy.arange(1,0,-1.0/len(M)) if i ==0 else \
        # (numpy.arange(0,1,1.0/len(M)) if i==len(M)-1 else \
        #  numpy.concatenate((numpy.arange(0,1,1.0/(i+1)),\
        #                                       numpy.arange(1,0,-1.0/(len(M)-i-1)))))

    @staticmethod
    def Kaiser(M):
        return numpy.kaiser(len(M),14)

    @staticmethod
    def Blackman(M):
        return numpy.blackman(len(M))

    @staticmethod
    def Bartlett(M):
        return numpy.bartlett(len(M))

    @staticmethod
    def Hamming(M):
        return numpy.hamming(len(M))

    @staticmethod
    def WindowNone(M):
        return mlab.window_none(len(M))


