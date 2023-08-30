# coding:utf-8
from enum import Enum
from PyQt5.QtCore import QRectF, Qt, pyqtSignal, QSize
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect

from ...common.color import mixColor
from ...common.icon import MaterialIconBase, drawIcon
from ...common.font import setFont
from ...common.style_sheet import isDarkTheme, themeColor, ThemeColor, palette, hoverMixPrimary, pressedMixPrimary
from .button import ToolButton


class FloatingActionButtonSize(Enum):
    """ Floating action button size """
    SMALL = 0
    MIDDLE = 1
    LARGE = 2



class FloatingActionButtonBase(ToolButton):
    """ FLoating action button base class """

    def _postInit(self):
        self.rippleWidget.rippleOpacityDuration = 800

        self.shadowEffect = QGraphicsDropShadowEffect(self)
        self.shadowEffect.setColor(QColor(0, 0, 0, 90))
        self.shadowEffect.setBlurRadius(25)
        self.shadowEffect.setOffset(0, 2)
        self.setGraphicsEffect(self.shadowEffect)

        self.setButtonSize(FloatingActionButtonSize.SMALL)

    def setButtonSize(self, size: FloatingActionButtonSize):
        """ set floating action button size """
        self.buttonSize = size

        if size == FloatingActionButtonSize.SMALL:
            self.setIconSize(QSize(16, 16))
            self.setBorderRadius(11)
        elif size == FloatingActionButtonSize.MIDDLE:
            self.setIconSize(QSize(16, 16))
            self.setBorderRadius(14)
        else:
            self.setIconSize(QSize(22, 22))
            self.setBorderRadius(18)
            setFont(self, 18)

        self.setFixedSize(self.sizeHint())

    def sizeHint(self):
        if self.buttonSize == FloatingActionButtonSize.SMALL:
            size = QSize(40, 40)
            ds = 26
        elif self.buttonSize == FloatingActionButtonSize.MIDDLE:
            size = QSize(56, 56)
            ds = 12
        else:
            size = QSize(72, 72)
            ds = 10

        if not self.text():
            return size

        w = self.fontMetrics().boundingRect(self.text()).width() + ds
        return size + QSize(w, 0)

    def _iconColor(self):
        return QColor()

    def _disabledBackgroundColor(self):
        return QColor(46, 43, 49) if isDarkTheme() else QColor(226, 220, 228)

    def _drawIcon(self, icon, painter: QPainter, rect: QRectF, state=QIcon.State.Off):
        if isinstance(icon, MaterialIconBase) and self.isEnabled():
            icon = icon.icon(color=self._iconColor())

        if self.text():
            x = 20 if self.buttonSize != FloatingActionButtonSize.SMALL else 18
            rect = QRectF(x, rect.y(), rect.width(), rect.height())

        drawIcon(icon, painter, rect, state)

    def paintEvent(self, e):
        super().paintEvent(e)

        if not self.text():
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(self._iconColor())

        if self.buttonSize == FloatingActionButtonSize.SMALL:
            x = 44
        elif self.buttonSize == FloatingActionButtonSize.MIDDLE:
            x = 46
        else:
            x = 56

        rect = QRectF(x, 0, self.width() - x, self.height())
        painter.drawText(rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self.text())

    def setText(self, text: str):
        super().setText(text)
        self.setFixedSize(self.sizeHint())


class SurfaceFloatingActionButton(FloatingActionButtonBase):
    """ Surface floating action button """

    def _normalBackgroundColor(self):
        return palette.surfaceContainerHigh

    def _hoverBackgroundColor(self):
        return hoverMixPrimary(self._normalBackgroundColor())

    def _pressedBackgroundColor(self):
        return pressedMixPrimary(self._normalBackgroundColor())

    def _iconColor(self):
        return themeColor()


class PrimaryFloatingActionButton(FloatingActionButtonBase):
    """ Primary floating action button """

    def _normalBackgroundColor(self):
        return palette.primaryContainer

    def _hoverBackgroundColor(self):
        return hoverMixPrimary(self._normalBackgroundColor())

    def _pressedBackgroundColor(self):
        return pressedMixPrimary(self._normalBackgroundColor())

    def _iconColor(self):
        return palette.onPrimaryContainer


class SecondaryFloatingActionButton(FloatingActionButtonBase):
    """ Secondary floating action button """

    def _normalBackgroundColor(self):
        return palette.secondaryContainer

    def _hoverBackgroundColor(self):
        return mixColor(palette.onSecondaryContainer, self._normalBackgroundColor(), 0.08)

    def _pressedBackgroundColor(self):
        return mixColor(palette.onSecondaryContainer, self._normalBackgroundColor(), 0.12)

    def _iconColor(self):
        return palette.onSecondaryContainer


class TertiaryFloatingActionButton(FloatingActionButtonBase):
    """ Tertiary floating action button """

    def _postInit(self):
        super()._postInit()
        self.rippleWidget.rippleColor = lambda: palette.tertiary

    def _normalBackgroundColor(self):
        return palette.tertiaryContainer

    def _hoverBackgroundColor(self):
        return mixColor(palette.onTertiaryContainer, self._normalBackgroundColor(), 0.08)

    def _pressedBackgroundColor(self):
        return mixColor(palette.onTertiaryContainer, self._normalBackgroundColor(), 0.12)

    def _iconColor(self):
        return palette.onTertiaryContainer
