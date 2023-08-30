# coding:utf-8
from typing import Union

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPainter, QColor
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel

from ..common.icon import MaterialIconBase
from ..common.router import qrouter
from ..common.style_sheet import MaterialStyleSheet, isDarkTheme, palette
from ..components.widgets.frameless_window import FramelessWindow
from ..components.navigation import NavigationRail, NavigationItemPosition, NavigationPushButton, NavigationBar
from .stacked_widget import StackedWidget

from qframelesswindow import TitleBar


class MaterialWindowBase(FramelessWindow):
    """ Material window base class """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.stackedWidget = StackedWidget(self)
        self.navigationInterface = None

        # initialize layout
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)

        MaterialStyleSheet.MATERIAL_WINDOW.apply(self.stackedWidget)

    def addSubInterface(self, interface: QWidget, icon: Union[MaterialIconBase, QIcon, str], text: str,
                        selectedIcon=None, position=NavigationItemPosition.TOP) -> NavigationPushButton:
        """ add sub interface, the object name of `interface` should be set already
        before calling this method

        Parameters
        ----------
        interface: QWidget
            the subinterface to be added

        icon: MaterialIconBase | QIcon | str
            the icon of navigation item

        text: str
            the text of navigation item

        selectedIcon: str | QIcon | MaterialIconBase
            the icon of navigation item in selected state

        position: NavigationItemPosition
            the position of navigation item
        """
        if not interface.objectName():
            raise ValueError(
                "The object name of `interface` can't be empty string.")

        self.stackedWidget.addWidget(interface)

        # add navigation item
        routeKey = interface.objectName()
        item = self.navigationInterface.addItem(
            routeKey=routeKey,
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            selectedIcon=selectedIcon,
            position=position
        )

        if self.stackedWidget.count() == 1:
            self.stackedWidget.currentChanged.connect(self._onCurrentInterfaceChanged)
            self.navigationInterface.setCurrentItem(routeKey)
            qrouter.setDefaultRouteKey(self.stackedWidget, routeKey)

        return item

    def switchTo(self, interface: QWidget):
        self.stackedWidget.setCurrentWidget(interface, popOut=False)

    def _onCurrentInterfaceChanged(self, index: int):
        widget = self.stackedWidget.widget(index)
        self.navigationInterface.setCurrentItem(widget.objectName())
        qrouter.push(self.stackedWidget, widget.objectName())

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)

        if isDarkTheme():
            painter.setBrush(QColor(32, 32, 32))
        else:
            painter.setBrush(QColor(243, 243, 243))

        painter.drawRect(self.rect())


class MaterialTitleBarBase(TitleBar):
    """ Material title bar base"""

    def __init__(self, parent):
        super().__init__(parent)
        self.iconLabel = QLabel(self)
        self.titleLabel = QLabel(self)

        self.iconLabel.setFixedSize(18, 18)
        self.titleLabel.setObjectName('titleLabel')
        MaterialStyleSheet.MATERIAL_WINDOW.apply(self)

        self.window().windowIconChanged.connect(self.setIcon)
        self.window().windowTitleChanged.connect(self.setTitle)

    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(18, 18))


class SplitMaterialTitleBar(MaterialTitleBarBase):
    """ Material title bar"""

    def __init__(self, parent):
        super().__init__(parent)
        # add window icon
        self.hBoxLayout.insertSpacing(0, 60)
        self.hBoxLayout.insertWidget(1, self.iconLabel, 0, Qt.AlignLeft | Qt.AlignBottom)

        # add title label
        self.hBoxLayout.insertWidget(2, self.titleLabel, 0, Qt.AlignLeft | Qt.AlignBottom)


class SplitMaterialWindow(MaterialWindowBase):
    """ Split material window """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitleBar(SplitMaterialTitleBar(self))

        self.navigationInterface = NavigationRail(self)
        self.widgetLayout = QHBoxLayout()

        # initialize layout
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addLayout(self.widgetLayout)
        self.hBoxLayout.setStretchFactor(self.widgetLayout, 1)

        self.widgetLayout.addWidget(self.stackedWidget)
        self.widgetLayout.setContentsMargins(0, 0, 0, 0)

        self.titleBar.raise_()
        self.navigationInterface.vBoxLayout.insertSpacing(0, 5)

    def resizeEvent(self, e):
        self.titleBar.move(46, 0)
        self.titleBar.resize(self.width()-46, self.titleBar.height())


class MaterialTitleBar(MaterialTitleBarBase):

    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(48)
        self.hBoxLayout.removeWidget(self.minBtn)
        self.hBoxLayout.removeWidget(self.maxBtn)
        self.hBoxLayout.removeWidget(self.closeBtn)

        # add window icon
        self.hBoxLayout.insertWidget(0, self.iconLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)

        # add title label
        self.hBoxLayout.insertWidget(1, self.titleLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)

        self.vBoxLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setSpacing(0)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.setAlignment(Qt.AlignTop)
        self.buttonLayout.addWidget(self.minBtn)
        self.buttonLayout.addWidget(self.maxBtn)
        self.buttonLayout.addWidget(self.closeBtn)

        self.vBoxLayout.addLayout(self.buttonLayout)
        self.vBoxLayout.addStretch(1)

        self.hBoxLayout.addLayout(self.vBoxLayout, 0)
        self.hBoxLayout.insertSpacing(0, 20)


class MaterialWindow(MaterialWindowBase):
    """ Material window in Microsoft Store style """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitleBar(MaterialTitleBar(self))
        self.navigationInterface = NavigationRail(self)

        # initialize layout
        self.hBoxLayout.setContentsMargins(0, 48, 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addWidget(self.stackedWidget, 1)

        self.titleBar.raise_()
        self.titleBar.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)


class BottomNavMaterialTitleBar(MaterialTitleBar):
    """ Bottom navigation material title bar """

    def __init__(self, parent):
        super().__init__(parent)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 16)
        self.hBoxLayout.insertWidget(1, self.iconLabel, 0, Qt.AlignmentFlag.AlignLeft)
        self.hBoxLayout.insertWidget(2, self.titleLabel, 0, Qt.AlignmentFlag.AlignLeft)


class BottomNavMaterialWindow(MaterialWindowBase):
    """ Bottom navigation material window """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitleBar(BottomNavMaterialTitleBar(self))

        self.vBoxLayout = QVBoxLayout()
        self.navigationInterface = NavigationBar(self)

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.addWidget(self.navigationInterface)

        self.hBoxLayout.setContentsMargins(0, 48, 0, 0)
        self.hBoxLayout.addLayout(self.vBoxLayout, 1)

    def addSubInterface(self, interface: QWidget, icon: Union[MaterialIconBase, QIcon, str], text: str,
                        selectedIcon=None) -> NavigationPushButton:
        """ add sub interface, the object name of `interface` should be set already
        before calling this method

        Parameters
        ----------
        interface: QWidget
            the subinterface to be added

        icon: MaterialIconBase | QIcon | str
            the icon of navigation item

        text: str
            the text of navigation item

        selectedIcon: str | QIcon | MaterialIconBase
            the icon of navigation item in selected state
        """
        if not interface.objectName():
            raise ValueError(
                "The object name of `interface` can't be empty string.")

        self.stackedWidget.addWidget(interface)

        # add navigation item
        routeKey = interface.objectName()
        item = self.navigationInterface.addItem(
            routeKey=routeKey,
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            selectedIcon=selectedIcon,
        )

        if self.stackedWidget.count() == 1:
            self.stackedWidget.currentChanged.connect(
                self._onCurrentInterfaceChanged)
            self.navigationInterface.setCurrentItem(routeKey)
            qrouter.setDefaultRouteKey(self.stackedWidget, routeKey)

        return item
