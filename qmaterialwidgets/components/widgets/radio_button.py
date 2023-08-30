# coding:utf-8
from PyQt5.QtCore import QRectF, QRect, QPoint
from PyQt5.QtGui import QPainterPath
from PyQt5.QtWidgets import QWidget, QRadioButton

from .ripple import RippleOverlayWidget, RippleStyle
from ...common.style_sheet import MaterialStyleSheet
from ...common.overload import singledispatchmethod


class RadioRippleOverlayWidget(RippleOverlayWidget):
    """ Radio overlay widget """

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.rippleRadiusDuration = 300
        self.rippleOpacityDuration = 1300
        self.rippleStartOpacity = 0.5

        path = QPainterPath()
        path.addEllipse(QRectF(self.overlayGeometry()))
        self.setClipPath(path)
        self.setRippleStyle(RippleStyle.CENTERED)

    def _rippleCenter(self):
        return QPoint(15, 15)

    def overlayGeometry(self):
        return QRect(0, 0, 30, 30)


class RadioButton(QRadioButton):
    """ Radio button """

    @singledispatchmethod
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.rippleWidget = RadioRippleOverlayWidget(self)
        MaterialStyleSheet.BUTTON.apply(self)

    @__init__.register
    def _(self, text: str, parent: QWidget = None):
        self.__init__(parent)
        self.setText(text)
