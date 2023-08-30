# coding:utf-8
from enum import Enum
from typing import Union, List

from PyQt5.QtCore import (Qt, pyqtSignal, QRect, QRectF, QPropertyAnimation, pyqtProperty, QMargins,
                          QEasingCurve, QPoint, QEvent)
from PyQt5.QtGui import QColor, QPainter, QPen, QIcon, QPainterPath, QFont, QBrush, QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from ...common.config import isDarkTheme
from ...common.style_sheet import themeColor, palette
from ...common.icon import drawIcon, toQIcon
from ...common.icon import MaterialIconBase as FIF
from ...common.font import setFont
from ...common.color import translucent, mixColor
from ... common.animation import BackgroundAnimationWidget

from ..widgets.ripple import RippleOverlayWidget


class NavigationItemPosition(Enum):
    """ Navigation item position """
    TOP = 0
    SCROLL = 1
    BOTTOM = 2


class RouteKeyError(Exception):
    """ Route key error """



class NavigationWidget(BackgroundAnimationWidget, QWidget):
    """ Navigation widget """

    clicked = pyqtSignal(bool)  # whether triggered by the user
    EXPAND_WIDTH = 312

    def __init__(self, isSelectable: bool, parent=None):
        self.isSelected = False
        self.isSelectable = isSelectable
        super().__init__(parent)
        self.setFixedSize(40, 36)
        self.backgroundColorAni.finished.connect(self._resetBackgroundAniDuraction)

    def mouseReleaseEvent(self, e):
        if self.isSelectable:
            self.isHover = False
            self.isSelected = True

        self.backgroundColorAni.setDuration(200)
        super().mouseReleaseEvent(e)
        self.clicked.emit(True)

    def setSelected(self, isSelected: bool):
        """ set whether the button is selected

        Parameters
        ----------
        isSelected: bool
            whether the button is selected
        """
        if not self.isSelectable or self.isSelected == isSelected:
            return

        self.isSelected = isSelected
        self.setBackgroundColor(self._normalBackgroundColor())

    def _resetBackgroundAniDuraction(self):
        self.backgroundColorAni.setDuration(120)


class NavigationPushButton(NavigationWidget):
    """ Navigation push button """

    def __init__(self, icon: Union[str, QIcon, FIF], text: str, isSelectable: bool, selectedIcon=None, parent=None):
        super().__init__(isSelectable=isSelectable, parent=parent)
        self._icon = icon
        self._text = text
        self._selectedIcon = selectedIcon
        self.rippleWidget = RippleOverlayWidget(self)

        path = QPainterPath()
        path.addEllipse(QRectF(15, 8, 58, 32))
        self.rippleWidget.setClipPath(path)

        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(88, 64)
        setFont(self, 12)

    def selectedIcon(self):
        if self._selectedIcon:
            return toQIcon(self._selectedIcon)

        return QIcon()

    def setSelectedIcon(self, icon: Union[str, QIcon, FIF]):
        self._selectedIcon = icon
        self._updateBackgroundColor()

    def text(self):
        return self._text

    def setText(self, text: str):
        self._text = text
        self.update()

    def icon(self):
        return toQIcon(self._icon)

    def setIcon(self, icon: Union[str, QIcon, FIF]):
        self._icon = icon
        self.update()

    def _normalBackgroundColor(self):
        return palette.secondaryContainer if self.isSelected else QColor(0, 0, 0, 0)

    def _hoverBackgroundColor(self):
        if self.isSelected:
            return mixColor(palette.onSurface, palette.secondaryContainer, 0.08)

        return translucent(palette.onSurface, 20)

    def _pressedBackgroundColor(self):
        if self.isSelected:
            return mixColor(palette.onSurface, palette.secondaryContainer, 0.12)

        return translucent(palette.onSurface, 30)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        painter.setPen(Qt.NoPen)

        if not self.isEnabled():
            painter.setOpacity(0.4)

        self._drawBackground(painter)
        self._drawIcon(painter)
        self._drawText(painter)

    def _drawBackground(self, painter: QPainter):
        painter.setBrush(self.backgroundColor)
        painter.drawRoundedRect(15, 8, 58, 32, 16, 16)

    def _drawIcon(self, painter: QPainter):
        rect = QRect(33, 14, 20, 20)
        selectedIcon = self._selectedIcon or self._icon

        if self.isSelected:
            drawIcon(selectedIcon, painter, rect, QIcon.On)
        else:
            drawIcon(self._icon, painter, rect)

    def _drawText(self, painter: QPainter):
        painter.setFont(self.font())
        painter.setPen(palette.onSurface)
        painter.drawText(QRect(0, 39, self.width(), self.height()-39), Qt.AlignCenter, self.text())


class NavigationToolButton(NavigationPushButton):
    """ Navigation tool button """

    def __init__(self, icon: Union[str, QIcon, FIF], parent=None):
        super().__init__(icon, '', False, parent)

    def setCompacted(self, isCompacted: bool):
        self.setFixedSize(40, 36)


class NavigationSeparator(NavigationWidget):
    """ Navigation Separator """

    def __init__(self, parent=None):
        super().__init__(False, parent=parent)
        self.setCompacted(True)

    def setCompacted(self, isCompacted: bool):
        if isCompacted:
            self.setFixedSize(48, 3)
        else:
            self.setFixedSize(self.EXPAND_WIDTH + 10, 3)

        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        c = 255 if isDarkTheme() else 0
        pen = QPen(QColor(c, c, c, 15))
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(0, 1, self.width(), 1)


class NavigationTreeItem(NavigationPushButton):
    """ Navigation tree item widget """

    itemClicked = pyqtSignal(bool, bool)    # triggerByUser, clickArrow

    def __init__(self, icon: Union[str, QIcon, FIF], text: str, isSelectable: bool, parent=None):
        super().__init__(icon, text, isSelectable, parent)
        self._arrowAngle = 0
        self.rotateAni = QPropertyAnimation(self, b'arrowAngle', self)

    def setExpanded(self, isExpanded: bool):
        self.rotateAni.stop()
        self.rotateAni.setEndValue(180 if isExpanded else 0)
        self.rotateAni.setDuration(150)
        self.rotateAni.start()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        clickArrow = QRectF(self.width()-30, 8, 20, 20).contains(e.pos())
        self.itemClicked.emit(True, clickArrow and not self.parent().isLeaf())
        self.update()

    def _canDrawIndicator(self):
        p = self.parent()   # type: NavigationTreeWidget
        if p.isLeaf() or p.isSelected:
            return p.isSelected

        for child in p.treeChildren:
            if child.itemWidget._canDrawIndicator() and not child.isVisible():
                return True

        return False

    def _margins(self):
        p = self.parent()   # type: NavigationTreeWidget
        return QMargins(p.nodeDepth*28, 0, 20*bool(p.treeChildren), 0)

    def paintEvent(self, e):
        super().paintEvent(e)
        if self.isCompacted or not self.parent().treeChildren:
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        if self.isPressed:
            painter.setOpacity(0.7)
        if not self.isEnabled():
            painter.setOpacity(0.4)

        painter.translate(self.width() - 20, 18)
        painter.rotate(self.arrowAngle)
        FIF.ARROW_DOWN.render(painter, QRectF(-5, -5, 9.6, 9.6))

    def getArrowAngle(self):
        return self._arrowAngle

    def setArrowAngle(self, angle):
        self._arrowAngle = angle
        self.update()

    arrowAngle = pyqtProperty(float, getArrowAngle, setArrowAngle)


class NavigationTreeWidgetBase(NavigationWidget):
    """ Navigation tree widget base class """

    def addChild(self, child):
        """ add child

        Parameters
        ----------
        child: NavigationTreeWidgetBase
            child item
        """
        raise NotImplementedError

    def insertChild(self, index: int, child: NavigationWidget):
        """ insert child

        Parameters
        ----------
        child: NavigationTreeWidgetBase
            child item
        """
        raise NotImplementedError

    def removeChild(self, child: NavigationWidget):
        """ remove child

        Parameters
        ----------
        child: NavigationTreeWidgetBase
            child item
        """
        raise NotImplementedError

    def isRoot(self):
        """ is root node """
        return True

    def isLeaf(self):
        """ is leaf node """
        return True

    def setExpanded(self, isExpanded: bool):
        """ set the expanded status

        Parameters
        ----------
        isExpanded: bool
            whether to expand node
        """
        raise NotImplementedError

    def childItems(self) -> list:
        """ return child items """
        raise NotImplementedError


class NavigationTreeWidget(NavigationTreeWidgetBase):
    """ Navigation tree widget """

    def __init__(self, icon: Union[str, QIcon, FIF], text: str, isSelectable: bool, parent=None):
        super().__init__(isSelectable, parent)

        self.treeChildren = []  # type: List[NavigationTreeWidget]
        self.isExpanded = False

        self.itemWidget = NavigationTreeItem(icon, text, isSelectable, self)
        self.vBoxLayout = QVBoxLayout(self)
        self.expandAni = QPropertyAnimation(self, b'geometry', self)

        self.__initWidget()

    def __initWidget(self):
        self.vBoxLayout.setSpacing(4)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addWidget(self.itemWidget, 0, Qt.AlignmentFlag.AlignTop)

        self.itemWidget.itemClicked.connect(self._onClicked)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.expandAni.valueChanged.connect(lambda g: self.setFixedSize(g.size()))

    def addChild(self, child):
        self.insertChild(-1, child)

    def text(self):
        return self.itemWidget.text()

    def icon(self):
        return self.itemWidget.icon()

    def setText(self, text):
        self.itemWidget.setText(text)

    def setIcon(self, icon: Union[str, QIcon, FIF]):
        self.itemWidget.setIcon(icon)

    def setFont(self, font: QFont):
        super().setFont(font)
        self.itemWidget.setFont(font)

    def insertChild(self, index, child):
        if child in self.treeChildren:
            return

        child.treeParent = self
        child.nodeDepth = self.nodeDepth + 1
        child.setVisible(self.isExpanded)
        child.expandAni.valueChanged.connect(lambda: self.setFixedSize(self.sizeHint()))

        if index < 0:
            index = len(self.treeChildren)

        index += 1  # item widget should always be the first
        self.treeChildren.insert(index, child)
        self.vBoxLayout.insertWidget(index, child, 0, Qt.AlignTop)

    def removeChild(self, child):
        self.treeChildren.remove(child)
        self.vBoxLayout.removeWidget(child)

    def childItems(self) -> list:
        return self.treeChildren

    def setExpanded(self, isExpanded: bool, ani=False):
        """ set the expanded status """
        if isExpanded == self.isExpanded:
            return

        self.isExpanded = isExpanded
        self.itemWidget.setExpanded(isExpanded)

        for child in self.treeChildren:
            child.setVisible(isExpanded)
            child.setFixedSize(child.sizeHint())

        if ani:
            self.expandAni.stop()
            self.expandAni.setStartValue(self.geometry())
            self.expandAni.setEndValue(QRect(self.pos(), self.sizeHint()))
            self.expandAni.setDuration(120)
            self.expandAni.setEasingCurve(QEasingCurve.OutQuad)
            self.expandAni.start()
        else:
            self.setFixedSize(self.sizeHint())

    def isRoot(self):
        return self.treeParent is None

    def isLeaf(self):
        return len(self.treeChildren) == 0

    def setSelected(self, isSelected: bool):
        super().setSelected(isSelected)
        self.itemWidget.setSelected(isSelected)

    def mouseReleaseEvent(self, e):
        pass

    def setCompacted(self, isCompacted: bool):
        super().setCompacted(isCompacted)
        self.itemWidget.setCompacted(isCompacted)

    def _onClicked(self, triggerByUser, clickArrow):
        if not self.isCompacted:
            if self.isSelectable and not self.isSelected and not clickArrow:
                self.setExpanded(True, ani=True)
            else:
                self.setExpanded(not self.isExpanded, ani=True)

        if not clickArrow or self.isCompacted:
            self.clicked.emit(triggerByUser)

