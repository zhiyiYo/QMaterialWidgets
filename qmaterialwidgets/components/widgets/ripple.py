# coding:utf-8
from typing import List
from enum import Enum


from PyQt5.QtCore import Qt, pyqtSignal, QEvent, QParallelAnimationGroup, QPoint, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QPainterPath
from PyQt5.QtWidgets import QWidget

from ...common.style_sheet import themeColor
from .overlay_widget import OverlayWidget


class RippleStyle(Enum):
    """ Ripple style """

    CENTERED = 0
    POSITIONED = 1
    NONE = 2



class RippleAnimation(QParallelAnimationGroup):
    """ Ripple animation """

    def __init__(self, center: QPoint, overlay=None, parent=None):
        super().__init__(parent=parent)
        self._radius = 0
        self._opacity = 0
        self.center = center
        self.overlay = overlay  # type: RippleOverlayWidget
        self.brush = QBrush(Qt.GlobalColor.black)

        self.radiusAni = QPropertyAnimation(self, b'radius', self)
        self.opacityAni = QPropertyAnimation(self, b'opacity', self)

        self.opacityAni.setStartValue(0.5)
        self.opacityAni.setEndValue(0)
        self.opacityAni.setDuration(800)
        self.opacityAni.setEasingCurve(QEasingCurve.Type.OutQuad)

        self.radiusAni.setStartValue(0)
        self.radiusAni.setEndValue(300)
        self.radiusAni.setDuration(800)
        self.radiusAni.setEasingCurve(QEasingCurve.Type.OutQuad)

        self.addAnimation(self.radiusAni)
        self.addAnimation(self.opacityAni)

    def setRadiusEndValue(self, radius: float):
        self.radiusAni.setEndValue(radius)

    def setRadiusDuration(self, duration: int):
        self.radiusAni.setDuration(duration)

    def setOpacityStartValue(self, opacity: float):
        self.opacityAni.setStartValue(opacity)

    def setOpacityDuration(self, duration: int):
        self.opacityAni.setDuration(duration)

    @pyqtProperty(float)
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, r):
        self._radius = r
        self.overlay.update()

    @pyqtProperty(float)
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, r):
        self._opacity = r
        self.overlay.update()

    def setColor(self, color: QColor):
        if self.brush.color() == color:
            return

        self.brush.setColor(color)
        self.overlay.update()

    def setBrush(self, brush: QBrush):
        self.brush = brush
        self.overlay.update()

    def setOverlay(self, overlay):
        self.overlay = overlay


class RippleOverlayWidget(OverlayWidget):
    """ Ripple overlay widget """

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.ripples = []    # type: List[RippleAnimation]
        self.clipPath = QPainterPath()
        self.isClipEnabled = True
        self.rippleStyle = RippleStyle.POSITIONED
        self.rippleOpacityDuration = 600
        self.rippleRadiusDuration = 800
        self.rippleStartOpacity = 0.35
        self.triggeredEvent = QEvent.Type.MouseButtonPress

        parent.installEventFilter(self)

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def setClipEnabled(self, isEnabled: bool):
        self.isClipEnabled = isEnabled
        self.update()

    def setClipPath(self, path: QPainterPath):
        self.clipPath = path
        self.update()

    def addRipple(self, ripple: RippleAnimation):
        """ add ripple animation """
        ripple.setOverlay(self)
        self.ripples.append(ripple)
        ripple.finished.connect(lambda :self.removeRipple(ripple))
        ripple.start()

    def removeRipple(self, ripple: RippleAnimation):
        if ripple not in self.ripples:
            return

        self.ripples.remove(ripple)
        ripple.deleteLater()
        self.update()

    def eventFilter(self, obj, e):
        if obj is not self.parent() or not obj.isEnabled() or self.rippleStyle == RippleStyle.NONE or \
                e.type() != self.triggeredEvent:
            return super().eventFilter(obj, e)

        # add ripple
        if self.rippleStyle == RippleStyle.CENTERED:
            pos = self._rippleCenter()
            radius = self.width() / 2
        else:
            pos = e.pos()
            radius = max(pos.x(), self.width() - pos.x())

        ripple = RippleAnimation(pos, self, self)
        ripple.setColor(self.rippleColor())
        ripple.setRadiusEndValue(radius)
        ripple.setOpacityStartValue(self.rippleStartOpacity)
        ripple.setRadiusDuration(self.rippleRadiusDuration)
        ripple.setOpacityDuration(self.rippleOpacityDuration)
        self.addRipple(ripple)
        return super().eventFilter(obj, e)

    def _rippleCenter(self):
        return self.rect().center()

    def setRippleStyle(self, style: RippleStyle):
        self.rippleStyle = style

    def rippleColor(self):
        return themeColor()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        if self.isClipEnabled:
            painter.setClipPath(self.clipPath)

        for ripple in self.ripples:
            self._drawRipple(painter, ripple)

    def _drawRipple(self, painter: QPainter, ripple: RippleAnimation):
        painter.setOpacity(ripple.opacity)
        painter.setBrush(ripple.brush)
        painter.drawEllipse(ripple.center, ripple.radius, ripple.radius)
