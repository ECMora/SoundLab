# -*- coding: utf-8 -*-
from PyQt4.QtCore import QRect,Qt, QTimer
from PyQt4.QtGui import QGraphicsView, QGraphicsScene, QPixmap
import random


class ToastWidget(QGraphicsView):
    """
    A widget to create toast messages to the user
    A friendly interface messages. (include image, and visual effects as blinking, fade etc)
    """

    def __init__(self, parent=None, back_image=None, width=100, heigth=100):
        super(ToastWidget, self).__init__(parent)
        self.setWindowFlags(Qt.SplashScreen)
        self.scene = QGraphicsScene(self)

        self.timer = QTimer(self)

        self.setScene(self.scene)
        self.set_image(back_image)
        self.setGeometry(QRect(self.x(), self.y(), width, heigth))
        self.show()

    def set_image(self, image):
        if image is None:
            return

        if not isinstance(image, QPixmap):
            raise Exception("Image must be of type QPixmap")
        self.scene.clear()
        self.scene.addPixmap(image.scaled(95, 95))

    def move_random(self, x1=0, x2=1300, y1=0, y2=768):
        x, y = random.randrange(x1, x2), random.randrange(y1, y2)
        self.setGeometry(QRect(x, y, 100, 100))
        return self

    def blink(self, time_limit=1000, time_interval=500):
        def _blink():
            self.setWindowOpacity(1 - self.windowOpacity())

        # self.timer.stop()
        # self.timer.setInterval(time_interval)
        # self.timer.timeout.connect(_blink)
        # self.timer.start_limited(time_interval, time_limit / time_interval)
        return self

    def fade(self, time=1500):
        """
        :param time:  the time to  completely execute the fade in ms
        :param out: fade out or in. out by default
       """
        steps = 100
        self.timer.stop()
        self.setWindowOpacity(1)
        self.timer.timeout.connect(lambda: self.setWindowOpacity(self.windowOpacity() - 1.0/steps))
        self.timer.start(time * 1.0 / steps)
        # QTimer.singleShot(time, lambda: self.timer.stop())
        return self

    def disappear(self, time=1000):
        """
        """
        self.timer.stop()
        self.setWindowOpacity(1)
        self.timer.singleShot(time, lambda: self.setWindowOpacity(0))
        return self

    def vibrate(self, time_limit=1000):
        geometry = self.geometry()
        x, y = geometry.x(), geometry.y()

        def _move():
            self.setGeometry(
                QRect(x + random.randrange(-3, 3), y + random.randrange(-3, 3), geometry.width(), geometry.height()))

        return self











