# coding:utf-8
from enum import Enum
from typing import Union
from PyQt5.QtCore import Qt, pyqtSignal, QPointF, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPolygonF
from PyQt5.QtWidgets import QWidget

from ...common.font import getFont
from ...common.style_sheet import themeColor, palette
from ...common.animation import FadeInOutWidget


class BubblePosition(Enum):
    """ Bubble position """
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3


class BubbleWidget(FadeInOutWidget, QWidget):
    """ Bubble widget """

    def __init__(self, parent=None, position=BubblePosition.TOP):
        super().__init__(parent=parent)
        self._text = ''
        self._bubblePosition = position
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.Tool |
                            Qt.WindowType.NoDropShadowWindowHint)

    def setText(self, text: str):
        self._text = text
        self.adjustSize()
        self.update()

    def text(self):
        return self._text

    def setBubblePosition(self, position: BubblePosition):
        self._bubblePosition = position
        self.update()

    def bubblePosition(self):
        return self._bubblePosition

    def adjustSize(self):
        w = self.fontMetrics().boundingRect(self.text()).width()
        if len(self.text()) == 1:
            cw = w + 16
        else:
            cw = w + 12

        sz = int(1.414 * cw)
        self.setFixedSize(sz, sz)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.TextAntialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(themeColor())

        # draw circle
        r = self.width() / (2*1.414)
        cx, h = self.width() / 2, self.height()
        painter.drawEllipse(QPointF(cx, cx), r, r)

        # draw triangle
        pos = self._bubblePosition
        if pos == BubblePosition.TOP:
            painter.drawPolygon(QPolygonF([
                QPointF(cx - r/1.414, h-1-r/1.414),
                QPointF(cx + r/1.414, h-1-r/1.414),
                QPointF(cx, h),
            ]))
        elif pos == BubblePosition.BOTTOM:
            painter.drawPolygon(QPolygonF([
                QPointF(cx - r/1.414, r/1.414),
                QPointF(cx + r/1.414, r/1.414),
                QPointF(cx, 0),
            ]))
        elif pos == BubblePosition.RIGHT:
            painter.drawPolygon(QPolygonF([
                QPointF(cx - r/1.414, cx - r/1.414),
                QPointF(cx - r/1.414, cx + r/1.414),
                QPointF(0, cx),
            ]))
        else:
            painter.drawPolygon(QPolygonF([
                QPointF(cx + r/1.414, cx - r/1.414),
                QPointF(cx + r/1.414, cx + r/1.414),
                QPointF(self.width(), cx),
            ]))

        # draw text
        painter.setFont(getFont(11))
        painter.setPen(palette.onPrimary)
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())

    def exec(self, target: Union[QPoint, QWidget]):
        if isinstance(target, QWidget):
            target = self._targetToPoint(target)

        self.move(target)
        self.show()

    def _targetToPoint(self, target: QWidget):
        pos = target.mapToGlobal(QPoint())
        tw, th, w, h = target.width(), target.height(), self.width(), self.height()

        bp = self._bubblePosition
        if bp == BubblePosition.TOP:
            return QPoint(pos.x()+tw//2-w//2, pos.y()-h-2)
        if bp == BubblePosition.BOTTOM:
            return QPoint(pos.x()+tw//2-w//2, pos.y()+th+2)
        if bp == BubblePosition.LEFT:
            return QPoint(pos.x()-w-2, pos.y()+th//2-h//2)

        return QPoint(pos.x()+tw+2, pos.y()+th//2-h//2)
