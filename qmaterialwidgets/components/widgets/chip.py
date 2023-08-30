# coding:utf-8
from enum import Enum
from PyQt5.QtCore import QRectF, Qt, pyqtSignal, pyqtProperty, QSize
from PyQt5.QtGui import QPixmap, QPainter, QColor, QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QGraphicsDropShadowEffect

from qmaterialwidgets.common.config import Theme
from qmaterialwidgets.components.widgets.menu import RoundMenu

from ...common.icon import MaterialIconBase, drawIcon, FluentIcon
from ...common.color import translucent, mixColor
from ...common.style_sheet import themeColor, isDarkTheme, palette
from .button import PushButton, TransparentToolButton, OutlinedPushButton, DropDownButtonBase


class ChipIcon(MaterialIconBase, Enum):
    """ Chip icon """

    CLOSE = "Close"
    ACCEPT = "Accept"

    def path(self, theme=Theme.AUTO) -> str:
        return f":/qmaterialwidgets/images/chip/{self.value}.svg"


class ChipCloseButton(TransparentToolButton):
    """ Chip close button """

    def _postInit(self):
        self.setIconSize(QSize(18, 18))
        self.setFixedSize(24, 24)

    def _drawIcon(self, icon, painter: QPainter, rect: QRectF, state=QIcon.State.Off):
        if self.parent().isChecked():
            icon = ChipIcon.CLOSE.icon(color=palette.onSecondaryContainer)
        else:
            icon = ChipIcon.CLOSE.icon(color=palette.onSurfaceVariant)

        drawIcon(icon, painter, rect, state)


class ChipBase(OutlinedPushButton):
    """ Chip base class """

    def _postInit(self):
        super()._postInit()
        self.setIconSize(QSize(18, 18))
        self.setBorderRadius(8)
        self.toggled.connect(self._updateBackgroundColor)

    def _normalBackgroundColor(self):
        return palette.secondaryContainer if self.isChecked() else QColor(0, 0, 0, 0)

    def _hoverBackgroundColor(self):
        if not self.isChecked():
            return translucent(palette.onSurfaceVariant, 20)

        return mixColor(palette.onSurfaceVariant, palette.secondaryContainer, 0.08)

    def _pressedBackgroundColor(self):
        if not self.isChecked():
            return translucent(palette.onSurfaceVariant, 30)

        return mixColor(palette.onSurfaceVariant, palette.secondaryContainer, 0.12)

    def _drawIcon(self, icon, painter, rect, state=QIcon.State.Off):
        rect.moveLeft(12)
        return super()._drawIcon(icon, painter, rect, state)

    def _drawBackground(self, painter: QPainter):
        if not self.isChecked():
            return super()._drawBackground(painter)

        painter.setPen(self.backgroundColor)
        PushButton._drawBackground(self, painter)


class InputChip(ChipBase):
    """ Input Chip """

    def _postInit(self):
        super()._postInit()
        self._isClosable = False
        self.closeButton = ChipCloseButton(self)
        self.setClosable(False)

    def isClosable(self):
        return self._isClosable

    def setClosable(self, isEnabled: bool):
        self._isClosable = isEnabled
        self.closeButton.setVisible(isEnabled)

        # adjust padding right
        self.setProperty('isClosable', isEnabled)
        self.setStyle(QApplication.style())

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.closeButton.move(self.width() - 30, self.height()//2-12)

    closable = pyqtProperty(bool, isClosable, setClosable)


class EvalatedChipBase:
    """ Elevated chip base class """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shadowEffect = QGraphicsDropShadowEffect(self)
        self.shadowEffect.setColor(QColor(0, 0, 0, 75))
        self.shadowEffect.setBlurRadius(7)
        self.shadowEffect.setOffset(0, 2)
        self.setGraphicsEffect(self.shadowEffect)

    def _normalBackgroundColor(self):
        return palette.secondaryContainer if self.isChecked() else palette.surfaceContainerLow

    def _hoverBackgroundColor(self):
        return mixColor(palette.onSurfaceVariant, self._normalBackgroundColor(), 0.08)

    def _pressedBackgroundColor(self):
        return mixColor(palette.onSurfaceVariant, self._normalBackgroundColor(), 0.12)

    def _drawBackground(self, painter: QPainter):
        painter.setPen(self.backgroundColor)
        PushButton._drawBackground(self, painter)


class ElevatedInputChip(EvalatedChipBase, InputChip):
    """ Elevated input chip """


class FilterChip(DropDownButtonBase, ChipBase):
    """ Filter chip """

    def _postInit(self):
        super()._postInit()
        self.setCheckable(True)
        self.setChecked(False)
        self.toggled.connect(self._onChipToggled)

        self.setProperty('hasDropMenu', False)

    def setMenu(self, menu: RoundMenu):
        self.setProperty('hasDropMenu', True)
        self.setStyle(QApplication.style())
        super().setMenu(menu)

    def _onChipToggled(self):
        if self.isChecked():
            self.setProperty('hasIcon', True)
        elif self.icon().isNull():
            self.setProperty('hasIcon', False)

        self.setStyle(QApplication.style())

    def _drawIcon(self, icon, painter, rect, state=QIcon.State.Off):
        # replace icon icon with check indicator
        if self.isChecked():
            icon = ChipIcon.ACCEPT.icon(color=palette.onSecondaryContainer)

        super()._drawIcon(icon, painter, rect, state)

    def _drawDropDownIcon(self, painter, rect):
        rect.moveLeft(self.width() - 30)
        super()._drawDropDownIcon(painter, rect)

    def paintEvent(self, e):
        if self.menu():
            DropDownButtonBase.paintEvent(self, e)
        else:
            ChipBase.paintEvent(self, e)


class ElevatedFilterChip(EvalatedChipBase, FilterChip):
    """ Elevated filter chip """
