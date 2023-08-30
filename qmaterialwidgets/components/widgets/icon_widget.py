# coding:utf-8
from typing import Union

from PyQt5.QtCore import pyqtProperty
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtWidgets import QWidget

from ...common.icon import MaterialIconBase, drawIcon, toQIcon
from ...common.overload import singledispatchmethod


class IconWidget(QWidget):
    """ Icon widget """

    @singledispatchmethod
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIcon(QIcon())

    @__init__.register
    def _(self, icon: MaterialIconBase, parent: QWidget = None):
        self.__init__(parent)
        self.setIcon(icon)

    @__init__.register
    def _(self, icon: QIcon, parent: QWidget = None):
        self.__init__(parent)
        self.setIcon(icon)

    @__init__.register
    def _(self, icon: str, parent: QWidget = None):
        self.__init__(parent)
        self.setIcon(icon)

    def getIcon(self):
        return toQIcon(self._icon)

    def setIcon(self, icon: Union[str, QIcon, MaterialIconBase]):
        self._icon = icon
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        drawIcon(self._icon, painter, self.rect())

    icon = pyqtProperty(QIcon, getIcon, setIcon)