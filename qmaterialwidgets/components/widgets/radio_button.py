# coding:utf-8
from PySide2.QtCore import Qt, Signal, QEvent, QRect, QPoint
from PySide2.QtGui import QPainterPath
from PySide2.QtWidgets import QWidget, QRadioButton

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
        path.addEllipse(self.overlayGeometry())
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
