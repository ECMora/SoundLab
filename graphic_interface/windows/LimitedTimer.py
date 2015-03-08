# -*- coding: utf-8 -*-
from PyQt4.QtCore import QTimer


class LimitedTimer(QTimer):

    def __init__(self,parent=None,stop_callback=None):
        super(LimitedTimer, self).__init__(parent)
        self.__timeLimit = 0 #the amount of times that the timer would be
        self.__times = 0
        self.stop_callback = stop_callback

    def check_stop_condition(self):
        if self.__times >= self.__timeLimit:
            self.stop()
            self.__timeLimit = 0
            self.__times = 0
            if self.stop_callback is not None and callable(self.stop_callback):
                self.stop_callback()
                self.stop_callback = None

    def start_limited(self, ms, times=-1):
        """
        Starts a timer with  intervals of ms  and stop after times  executions
        :param ms: the interval for the timer in ms
        :param times: int. How many times the timer would raise the timeout event. -1 should be for ever
        """
        if times > 0:
            self.__timeLimit = times

            def check():
                self.check_stop_condition()
                self.__times += 1

            self.timeout.connect(check)
        self.start(ms)

