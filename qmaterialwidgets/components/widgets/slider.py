# coding:utf-8
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QPoint, QRectF, QEvent
from PyQt5.QtGui import QColor, QMouseEvent, QPainter, QPainterPath
from PyQt5.QtWidgets import (QProxyStyle, QSlider, QStyle, QStyleOptionSlider,
                               QWidget, QGraphicsDropShadowEffect)

from ...common.animation import BackgroundAnimationWidget
from ...common.style_sheet import MaterialStyleSheet, themeColor, palette
from ...common.color import translucent
from ...common.overload import singledispatchmethod
from .bubble_widget import BubblePosition, BubbleWidget


class CircleHandle(QWidget):
    """ Circle handle """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.shadowEffect = QGraphicsDropShadowEffect(self)
        self.shadowEffect.setOffset(0, 2)
        self.shadowEffect.setColor(QColor(0, 0, 0, 75))
        self.shadowEffect.setBlurRadius(10)
        self.setGraphicsEffect(self.shadowEffect)
        self.setFixedSize(20, 20)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(themeColor())
        painter.drawEllipse(self.rect())


class SliderHandle(BackgroundAnimationWidget, QWidget):
    """ Slider handle """

    def __init__(self, parent: QSlider):
        super().__init__(parent=parent)
        self.bubble = BubbleWidget(self.window())
        self.handle = CircleHandle(self)
        self.handle.move(10, 10)
        self.setFixedSize(40, 40)

        self.bubble.setText(str(parent.value()))

    def _hoverBackgroundColor(self):
        return translucent(themeColor(), 20)

    def _pressedBackgroundColor(self):
        return translucent(themeColor(), 30)

    def enterEvent(self, e):
        BackgroundAnimationWidget.enterEvent(self, e)
        self.bubble.exec(self.handle)

    def leaveEvent(self, e):
        BackgroundAnimationWidget.leaveEvent(self, e)
        self.bubble.fadeOut()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.backgroundColor)
        painter.drawEllipse(self.rect())

    def setText(self, text: str):
        self.bubble.setText(text)
        if self.isVisible():
            self.bubble.exec(self.handle)

    def setBubblePosition(self, pos: BubblePosition):
        self.bubble.setBubblePosition(pos)


class Slider(QSlider):
    """ A slider can be clicked """

    clicked = pyqtSignal(int)

    @singledispatchmethod
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._postInit()

    @__init__.register
    def _(self, orientation: Qt.Orientation, parent: QWidget = None):
        super().__init__(orientation, parent=parent)
        self._postInit()

    def _postInit(self):
        self.handle = SliderHandle(self)
        self._pressedPos = QPoint()
        self.setOrientation(self.orientation())
        self.valueChanged.connect(self._adjustHandlePos)

    def setOrientation(self, orientation: Qt.Orientation) -> None:
        super().setOrientation(orientation)
        if orientation == Qt.Orientation.Horizontal:
            self.setFixedHeight(40)
            self.setBubblePosition(BubblePosition.TOP)
        else:
            self.setFixedWidth(40)
            self.setBubblePosition(BubblePosition.RIGHT)

    def setBubblePosition(self, pos: BubblePosition):
        self.handle.setBubblePosition(pos)

    def hideBubble(self):
        self.handle.bubble.hide()

    def _bubbleText(self) -> str:
        return str(self.value())

    def mousePressEvent(self, e: QMouseEvent):
        self._pressedPos = e.pos()
        self.setValue(self._posToValue(e.pos()))
        self.clicked.emit(self.value())

    def mouseMoveEvent(self, e: QMouseEvent):
        self.setValue(self._posToValue(e.pos()))
        self._pressedPos = e.pos()

    @property
    def grooveLength(self):
        l = self.width() if self.orientation() == Qt.Orientation.Horizontal else self.height()
        return l - self.handle.width()

    def _adjustHandlePos(self):
        total = max(self.maximum() - self.minimum(), 1)
        delta = int((self.value() - self.minimum()) / total * self.grooveLength)

        if self.orientation() == Qt.Orientation.Vertical:
            self.handle.move(0, delta)
        else:
            self.handle.move(delta, 0)

        self.handle.setText(self._bubbleText())

    def _posToValue(self, pos: QPoint):
        pd = self.handle.width() / 2
        gs = max(self.grooveLength, 1)
        v = pos.x() if self.orientation() == Qt.Orientation.Horizontal else pos.y()
        return int((v - pd) / gs * (self.maximum() - self.minimum()) + self.minimum())

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(palette.surfaceContainerHighest)

        if self.orientation() == Qt.Orientation.Horizontal:
            self._drawHorizonGroove(painter)
        else:
            self._drawVerticalGroove(painter)

    def _drawHorizonGroove(self, painter: QPainter):
        w, r = self.width(), self.handle.width() / 2
        painter.drawRoundedRect(QRectF(r, r-2, w-r*2, 4), 2, 2)

        if self.maximum() - self.minimum() == 0:
            return

        painter.setBrush(themeColor())
        aw = (self.value() - self.minimum()) / self.maximum() * (w - r*2)
        painter.drawRoundedRect(QRectF(r, r-2, aw, 4), 2, 2)

    def _drawVerticalGroove(self, painter: QPainter):
        h, r = self.height(), self.handle.width() / 2
        painter.drawRoundedRect(QRectF(r-2, r, 4, h-2*r), 2, 2)

        if self.maximum() - self.minimum() == 0:
            return

        painter.setBrush(themeColor())
        ah = (self.value() - self.minimum()) / self.maximum() * (h - r*2)
        painter.drawRoundedRect(QRectF(r-2, r, 4, ah), 2, 2)

    def resizeEvent(self, e):
        self._adjustHandlePos()
