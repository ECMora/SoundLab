# -*- coding: utf-8 -*-
from PyQt4.QtCore import QRect,Qt
from PyQt4.QtGui import QGraphicsView, QGraphicsScene, QPixmap
import random
from LimitedTimer import LimitedTimer


class EffectWindow(QGraphicsView):
    def __init__(self, parent=None, back_image=None):
        super(EffectWindow, self).__init__(parent)
        self.setWindowFlags(Qt.SplashScreen)
        self.scene = QGraphicsScene(self)

        self.setWindowOpacity(0)
        self.setScene(self.scene)
        if back_image is not None:
            assert isinstance(back_image, QPixmap)
            self.set_image(back_image)

        self.setGeometry(QRect(self.x(), self.y(), 100, 100))
        self.show()

    def set_image(self, image):
        self.scene.addPixmap(image.scaled(95, 95))

    def move_random(self, x1=0, x2=1300, y1=0, y2=768):
        x, y = random.randrange(x1, x2), random.randrange(y1, y2)
        self.setGeometry(QRect(x, y, 100, 100))
        return self

    def blink(self, time_limit=1000, time_interval=500):
        def _blink():
            self.setWindowOpacity(1 - self.windowOpacity())

        timer = LimitedTimer(self)
        timer.setInterval(time_interval)
        timer.timeout.connect(_blink)
        timer.start_limited(time_interval, time_limit / time_interval)
        return self

    def fade(self, time=1500, out=True):
        """
        :param time:  the time to  completely execute the fade in ms
        :param out: fade out or in. out by default
       """
        self.setWindowOpacity(1 if out else 0)
        timer = LimitedTimer(self)
        timer.timeout.connect(lambda: self.setWindowOpacity(self.windowOpacity() + -0.01 if out else 0.01))
        timer.start_limited(time / 100.0, 100)
        return self

    def vibrate(self, time_limit=1000):
        geometry = self.geometry()
        x, y = geometry.x(), geometry.y()

        def _move():
            self.setGeometry(
                QRect(x + random.randrange(-3, 3), y + random.randrange(-3, 3), geometry.width(), geometry.height()))

        timer = LimitedTimer(self)
        timer.timeout.connect(_move)
        timer.start_limited(time_limit / 100.0, 100)
        return self











