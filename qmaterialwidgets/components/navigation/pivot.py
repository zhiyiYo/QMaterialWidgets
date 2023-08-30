# coding:utf-8
from typing import Dict

from PyQt5.QtCore import Qt, pyqtSignal, QRectF, QRect, QPropertyAnimation, QSize, QEasingCurve, QEvent
from PyQt5.QtGui import QPainter, QColor, QIcon, QPainterPath
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSizePolicy

from ...common.font import setFont
from ...common.router import qrouter
from ...common.style_sheet import themeColor, MaterialStyleSheet, palette
from ...common.icon import drawIcon, MaterialIconBase
from .navigation_widget import RouteKeyError, NavigationPushButton


class TabItem(NavigationPushButton):
    """ Tab item """

    itemClicked = pyqtSignal(bool)

    def __init__(self, text: str, parent=None):
        super().__init__(QIcon(), text, True, parent=parent)
        self.rippleWidget.rippleOpacityDuration = 600
        self.rippleWidget.rippleRadiusDuration = 600
        setFont(self, 13)
        self.setText(text)

        self.clicked.connect(lambda: self.itemClicked.emit(True))
        self._updateRipple()

    def sizeHint(self):
        w = self.fontMetrics().boundingRect(self.text()).width()
        w = max(16, w) + 32
        return QSize(w, 60)

    def setText(self, text: str):
        super().setText(text)
        self.setFixedSize(self.sizeHint())

    def _normalBackgroundColor(self):
        return QColor(0, 0, 0, 0)

    def _hoverBackgroundColor(self):
        return QColor(0, 0, 0, 0)

    def _pressedBackgroundColor(self):
        return QColor(0, 0, 0, 0)

    def _updateRipple(self):
        path = QPainterPath()
        path.addRect(QRectF(self.rect()))
        self.rippleWidget.setClipPath(path)

    def _drawBackground(self, painter: QPainter):
        painter.setBrush(self.backgroundColor)
        painter.drawRect(self.rect())

    def _drawIcon(self, painter: QPainter):
        rect = QRectF(self.width()/2-8, 10, 16, 16)
        selectedIcon = self._selectedIcon or self._icon

        if isinstance(selectedIcon, MaterialIconBase) and self.isSelected:
            selectedIcon.render(painter, rect, fill=themeColor().name())
        elif self.isSelected:
            drawIcon(selectedIcon, painter, rect)
        else:
            drawIcon(self._icon, painter, rect)

    def _drawText(self, painter: QPainter):
        painter.setFont(self.font())
        painter.setPen(themeColor() if self.isSelected else palette.onSurface)
        if self.icon().isNull():
            painter.drawText(self.rect(), Qt.AlignCenter, self.text())
        else:
            painter.drawText(
                QRect(0, 20, self.width(), self.height()-20), Qt.AlignCenter, self.text())


class TabIndicator(QWidget):
    """ Tab indicator """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(6)
        self.ani = QPropertyAnimation(self, b'geometry', self)
        self.ani.setDuration(250)
        self.ani.setEasingCurve(QEasingCurve.Type.InOutCirc)

        self.target = None

    def moveTo(self, widget: TabItem):
        self.target = widget
        widget.installEventFilter(self)

        self.ani.stop()
        self.ani.setEndValue(self.targetGeometry(widget))
        self.ani.start()

    def targetGeometry(self, widget: TabItem):
        w = widget.fontMetrics().boundingRect(widget.text()).width()
        x = int(widget.geometry().center().x() - w / 2)
        return QRect(x, self.parent().height()- self.height(), w, self.height())

    def eventFilter(self, obj, e):
        if obj is self.target and e.type() == QEvent.Type.Move:
            self.ani.stop()
            self.setGeometry(self.targetGeometry(self.target))

        return super().eventFilter(obj, e)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.NoPen)

        path = QPainterPath()
        path.addRoundedRect(0, 3, self.width(), 6, 3, 3)
        painter.fillPath(path, themeColor())


class TabWidget(QWidget):
    """ Tab widget """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.items = {}  # type: Dict[str, TabItem]

        self.hBoxLayout = QHBoxLayout(self)
        self.indicator = TabIndicator(self)

        # self.setWidget(self.view)
        # self.setWidgetResizable(True)
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setViewportMargins(0, 0, 0, 0)

        MaterialStyleSheet.TAB_WIDGET.apply(self)

        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.setSizeConstraint(QHBoxLayout.SizeConstraint.SetMinimumSize)

        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

    def addItem(self, routeKey: str, text: str, onClick=None, icon=None):
        """ add item

        Parameters
        ----------
        routeKey: str
            the unique name of item

        text: str
            the text of navigation item

        onClick: callable
            the slot connected to item clicked signal

        icon: str
            the icon of navigation item
        """
        return self.insertItem(-1, routeKey, text, onClick, icon)

    def addWidget(self, routeKey: str, widget: TabItem, onClick=None):
        """ add widget

        Parameters
        ----------
        routeKey: str
            the unique name of item

        widget: PivotItem
            navigation widget

        onClick: callable
            the slot connected to item clicked signal
        """
        self.insertWidget(-1, routeKey, widget, onClick)

    def insertItem(self, index: int, routeKey: str, text: str, onClick=None, icon=None):
        """ insert item

        Parameters
        ----------
        index: int
            insert position

        routeKey: str
            the unique name of item

        text: str
            the text of navigation item

        onClick: callable
            the slot connected to item clicked signal

        icon: str
            the icon of navigation item
        """
        if routeKey in self.items:
            return

        item = TabItem(text, self)
        if icon:
            item.setIcon(icon)

        self.insertWidget(index, routeKey, item, onClick)
        return item

    def insertWidget(self, index: int, routeKey: str, widget: TabItem, onClick=None):
        """ insert item

        Parameters
        ----------
        index: int
            insert position

        routeKey: str
            the unique name of item

        widget: TabItem
            tab widget

        onClick: callable
            the slot connected to item clicked signal
        """
        if routeKey in self.items:
            return

        widget.setProperty('routeKey', routeKey)
        widget.itemClicked.connect(self._onItemClicked)
        if onClick:
            widget.itemClicked.connect(onClick)

        self.items[routeKey] = widget
        self.hBoxLayout.insertWidget(index, widget)
        self.hBoxLayout.insertStretch(index, 1)

        self._showIndicator(widget)

    def _showIndicator(self, widget: TabIndicator):
        if self.indicator.isVisible():
            return

        w = widget.fontMetrics().boundingRect(widget.text()).width()
        x = int(widget.geometry().center().x() - w / 2)

        self.indicator.show()
        self.indicator.setGeometry(QRect(x, widget.geometry().bottom()-6, w, 6))

    def removeWidget(self, routeKey: str):
        """ remove widget

        Parameters
        ----------
        routeKey: str
            the unique name of item
        """
        if routeKey not in self.items:
            return

        item = self.items.pop(routeKey)
        self.hBoxLayout.removeWidget(item)
        qrouter.remove(routeKey)
        item.deleteLater()

        if not self.items:
            self.indicator.hide()

    def clear(self):
        """ clear all navigation items """
        for k, w in self.items.items():
            self.hBoxLayout.removeWidget(w)
            qrouter.remove(k)
            w.deleteLater()

        self.items.clear()

    def setCurrentItem(self, routeKey: str):
        """ set current selected item

        Parameters
        ----------
        routeKey: str
            the unique name of item
        """
        if routeKey not in self.items:
            return

        for k, item in self.items.items():
            item.setSelected(k == routeKey)

        self.indicator.moveTo(self.widget(routeKey))

    def setItemFontSize(self, size: int):
        """ set the pixel font size of items """
        for item in self.items.values():
            font = item.font()
            font.setPixelSize(size)
            item.setFont(font)
            item.adjustSize()

    def _onItemClicked(self):
        item = self.sender()  # type: TabItem
        self.setCurrentItem(item.property('routeKey'))

    def widget(self, routeKey: str):
        if routeKey not in self.items:
            raise RouteKeyError(f"`{routeKey}` is illegal.")

        return self.items[routeKey]

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(palette.surfaceContainerHighest)

        y = self.height() - 1
        painter.drawLine(0, y, self.width(), y)
