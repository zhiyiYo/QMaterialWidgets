# coding:utf-8
from PyQt5.QtCore import (Qt, QRectF, QEasingCurve, QPropertyAnimation, QParallelAnimationGroup,
                            QSequentialAnimationGroup, pyqtProperty)
from PyQt5.QtGui import QColor, QPen, QPainter, QFont
from PyQt5.QtWidgets import QProgressBar

from .progress_bar import ProgressBar
from ...common.font import setFont
from ...common.style_sheet import themeColor, isDarkTheme


class ProgressRing(ProgressBar):
    """ Progress ring """

    def __init__(self, parent=None, useAni=True):
        super().__init__(parent, useAni=useAni)
        self.lightBackgroundColor = QColor(0, 0, 0, 34)
        self.darkBackgroundColor = QColor(255, 255, 255, 34)
        self._strokeWidth = 6

        self.setTextVisible(False)
        self.setFixedSize(100, 100)
        setFont(self)

    def getStrokeWidth(self):
        return self._strokeWidth

    def setStrokeWidth(self, w: int):
        self._strokeWidth = w
        self.update()

    def _drawText(self, painter: QPainter, text: str):
        """ draw text """
        painter.setFont(self.font())
        painter.setPen(Qt.white if isDarkTheme() else Qt.black)
        painter.drawText(self.rect(), Qt.AlignCenter, text)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        cw = self._strokeWidth    # circle thickness
        w = min(self.height(), self.width()) - cw
        rc = QRectF(cw/2, self.height()/2 - w/2, w, w)

        # draw background
        bc = self.darkBackgroundColor if isDarkTheme() else self.lightBackgroundColor
        pen = QPen(bc, cw, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        painter.drawArc(rc, 0, 360*16)

        if self.maximum() <= self.minimum():
            return

        # draw bar
        pen.setColor(themeColor())
        painter.setPen(pen)
        degree = int(self.val / (self.maximum() - self.minimum()) * 360)
        painter.drawArc(rc, 90*16, -degree*16)

        # draw text
        if self.isTextVisible():
            self._drawText(painter, self.valText())

    strokeWidth = pyqtProperty(int, getStrokeWidth, setStrokeWidth)


class IndeterminateProgressRing(QProgressBar):
    """ Indeterminate progress ring """

    def __init__(self, parent=None, start=True):
        super().__init__(parent=parent)
        self.lightBackgroundColor = QColor(0, 0, 0, 0)
        self.darkBackgroundColor = QColor(255, 255, 255, 0)
        self._strokeWidth = 6

        self._startAngle = -180
        self._spanAngle = 0

        self.startAngleAni = QPropertyAnimation(self, b'startAngle', self)
        self.spanAngleAni = QPropertyAnimation(self, b'spanAngle', self)
        self.aniGroup = QParallelAnimationGroup(self)

        # initialize start angle animation
        self.startAngleAni.setDuration(2000)
        self.startAngleAni.setStartValue(0)
        self.startAngleAni.setKeyValueAt(0.5, 450)
        self.startAngleAni.setEndValue(1080)

        # initialize span angle animation
        self.spanAngleAni.setDuration(2000)
        self.spanAngleAni.setStartValue(10)
        self.spanAngleAni.setKeyValueAt(0.5, 180)
        self.spanAngleAni.setEndValue(10)

        self.aniGroup.addAnimation(self.startAngleAni)
        self.aniGroup.addAnimation(self.spanAngleAni)
        self.aniGroup.setLoopCount(-1)

        self.setFixedSize(80, 80)

        if start:
            self.start()

    @pyqtProperty(int)
    def startAngle(self):
        return self._startAngle

    @startAngle.setter
    def startAngle(self, angle: int):
        self._startAngle = angle
        self.update()

    @pyqtProperty(int)
    def spanAngle(self):
        return self._spanAngle

    @spanAngle.setter
    def spanAngle(self, angle: int):
        self._spanAngle = angle
        self.update()

    def getStrokeWidth(self):
        return self._strokeWidth

    def setStrokeWidth(self, w: int):
        self._strokeWidth = w
        self.update()

    def start(self):
        """ start spin """
        self._startAngle = 0
        self._spanAngle = 0
        self.aniGroup.start()

    def stop(self):
        """ stop spin """
        self.aniGroup.stop()
        self.startAngle = 0
        self.spanAngle = 0

    def setCustomBackgroundColor(self, light, dark):
        """ set the custom background color

        Parameters
        ----------
        light, dark: str | Qt.GlobalColor | QColor
            background color in light/dark theme mode
        """
        self.lightBackgroundColor = QColor(light)
        self.darkBackgroundColor = QColor(dark)
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        cw = self._strokeWidth
        w = min(self.height(), self.width()) - cw
        rc = QRectF(cw/2, self.height()/2 - w/2, w, w)

        # draw background
        bc = self.darkBackgroundColor if isDarkTheme() else self.lightBackgroundColor
        pen = QPen(bc, cw, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        painter.drawArc(rc, 0, 360*16)

        # draw bar
        pen.setColor(themeColor())
        painter.setPen(pen)

        startAngle = -self.startAngle + 180
        painter.drawArc(rc, (startAngle % 360)*16, -self.spanAngle*16)

    strokeWidth = pyqtProperty(int, getStrokeWidth, setStrokeWidth)
