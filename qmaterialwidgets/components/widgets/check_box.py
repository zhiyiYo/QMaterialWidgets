# coding: utf-8
from enum import Enum

from PyQt5.QtCore import Qt, QPoint, QRect, QRectF
from PyQt5.QtGui import QPainterPath, QPainter
from PyQt5.QtWidgets import QCheckBox, QStyle, QStyleOptionButton, QWidget

from ...common.icon import MaterialIconBase, Theme, getIconColor
from ...common.style_sheet import MaterialStyleSheet
from ...common.overload import singledispatchmethod
from .ripple import RippleStyle
from .radio_button import RadioRippleOverlayWidget


class CheckBoxIcon(MaterialIconBase, Enum):
    """ CheckBoxIcon """

    ACCEPT = "Accept"
    PARTIAL_ACCEPT = "PartialAccept"

    def path(self, theme=Theme.AUTO):
        c = getIconColor(theme, reverse=True)
        return f':/qmaterialwidgets/images/check_box/{self.value}_{c}.svg'


class CheckBoxRippleOverlayWidget(RadioRippleOverlayWidget):
    """ CheckBox overlay widget """

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
        return QPoint(18, 18)

    def overlayGeometry(self):
        return QRect(0, 0, 36, 36)



class CheckBox(QCheckBox):
    """ Check box """

    @singledispatchmethod
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        MaterialStyleSheet.CHECK_BOX.apply(self)
        self.rippleWidget = CheckBoxRippleOverlayWidget(self)

    @__init__.register
    def _(self, text: str, parent: QWidget = None):
        self.__init__(parent)
        self.setText(text)

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)

        if not self.isEnabled():
            painter.setOpacity(0.8)

        # get the rect of indicator
        opt = QStyleOptionButton()
        opt.initFrom(self)
        rect = self.style().subElementRect(QStyle.SubElement.SE_CheckBoxIndicator, opt, self)

        # draw indicator
        if self.checkState() == Qt.CheckState.Checked:
            CheckBoxIcon.ACCEPT.render(painter, rect)
        elif self.checkState() == Qt.CheckState.PartiallyChecked:
            CheckBoxIcon.PARTIAL_ACCEPT.render(painter, rect)
