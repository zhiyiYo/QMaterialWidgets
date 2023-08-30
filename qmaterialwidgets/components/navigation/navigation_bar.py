# coding:utf-8
from typing import Dict, Union

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QPainter, QColor, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from ...common.icon import drawIcon, MaterialIconBase
from ...common.router import qrouter
from ...common.style_sheet import MaterialStyleSheet
from ..widgets.scroll_area import SingleDirectionScrollArea
from .navigation_widget import NavigationPushButton, NavigationWidget, RouteKeyError, NavigationItemPosition


class NavigationBarBase(QWidget):
    """ Navigation bar base """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.items = {}   # type: Dict[str, NavigationWidget]
        self.history = qrouter

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        MaterialStyleSheet.NAVIGATION_INTERFACE.apply(self)

    def widget(self, routeKey: str):
        if routeKey not in self.items:
            raise RouteKeyError(f"`{routeKey}` is illegal.")

        return self.items[routeKey]

    def removeWidget(self, routeKey: str):
        """ remove widget

        Parameters
        ----------
        routeKey: str
            the unique name of item
        """
        if routeKey not in self.items:
            return

        widget = self.items.pop(routeKey)
        widget.deleteLater()
        self.history.remove(routeKey)

    def setCurrentItem(self, routeKey: str):
        """ set current selected item

        Parameters
        ----------
        routeKey: str
            the unique name of item
        """
        if routeKey not in self.items:
            return

        for k, widget in self.items.items():
            if isinstance(widget, NavigationWidget):
                widget.setSelected(k == routeKey)

    def _onWidgetClicked(self):
        widget = self.sender()  # type: NavigationWidget
        if isinstance(widget, NavigationWidget) and widget.isSelectable:
            self.setCurrentItem(widget.property('routeKey'))


class NavigationBar(NavigationBarBase):
    """ Navigation rail """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setSpacing(4)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 5)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def addItem(self, routeKey: str, icon: Union[str, QIcon, MaterialIconBase], text: str, onClick=None,
                selectable=True, selectedIcon=None):
        """ add navigation item

        Parameters
        ----------
        routeKey: str
            the unique name of item

        icon: str | QIcon | MaterialIconBase
            the icon of navigation item

        text: str
            the text of navigation item

        onClick: callable
            the slot connected to item clicked signal

        selectable: bool
            whether the item is selectable

        selectedIcon: str | QIcon | MaterialIconBase
            the icon of navigation item in selected state
        """
        return self.insertItem(-1, routeKey, icon, text, onClick, selectable, selectedIcon)

    def addWidget(self, routeKey: str, widget: NavigationWidget, onClick=None):
        """ add custom widget

        Parameters
        ----------
        routeKey: str
            the unique name of item

        widget: NavigationWidget
            the custom widget to be added

        onClick: callable
            the slot connected to item clicked signal
        """
        self.insertWidget(-1, routeKey, widget, onClick)

    def insertItem(self, index: int, routeKey: str, icon: Union[str, QIcon, MaterialIconBase], text: str, onClick=None,
                   selectable=True, selectedIcon=None):
        """ insert navigation tree item

        Parameters
        ----------
        index: int
            the insert position of parent widget

        routeKey: str
            the unique name of item

        icon: str | QIcon | MaterialIconBase
            the icon of navigation item

        text: str
            the text of navigation item

        onClick: callable
            the slot connected to item clicked signal

        selectable: bool
            whether the item is selectable

        selectedIcon: str | QIcon | MaterialIconBase
            the icon of navigation item in selected state
        """
        if routeKey in self.items:
            return

        w = NavigationPushButton(icon, text, selectable, selectedIcon, self)
        self.insertWidget(index, routeKey, w, onClick)
        return w

    def insertWidget(self, index: int, routeKey: str, widget: NavigationWidget, onClick=None):
        """ insert custom widget

        Parameters
        ----------
        index: int
            insert position

        routeKey: str
            the unique name of item

        widget: NavigationWidget
            the custom widget to be added

        onClick: callable
            the slot connected to item clicked signal
        """
        if routeKey in self.items:
            return

        self._registerWidget(routeKey, widget, onClick)
        self._insertWidgetToLayout(index, widget)

    def _registerWidget(self, routeKey: str, widget: NavigationWidget, onClick):
        """ register widget """
        widget.clicked.connect(self._onWidgetClicked)

        if onClick is not None:
            widget.clicked.connect(onClick)

        widget.setProperty('routeKey', routeKey)
        self.items[routeKey] = widget

    def _insertWidgetToLayout(self, index: int, widget: NavigationWidget):
        """ insert widget to layout """
        widget.setParent(self)
        self.hBoxLayout.insertWidget(index, widget)
        widget.show()


class NavigationRail(NavigationBarBase):
    """ Navigation rail """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.scrollArea = SingleDirectionScrollArea(self)
        self.scrollWidget = QWidget()

        self.vBoxLayout = QVBoxLayout(self)
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QVBoxLayout()
        self.scrollLayout = QVBoxLayout(self.scrollWidget)

        self.__initWidget()

    def __initWidget(self):
        self.resize(48, self.height())
        self.window().installEventFilter(self)

        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidget(self.scrollWidget)
        self.scrollArea.setWidgetResizable(True)

        self.scrollWidget.setObjectName('scrollWidget')
        MaterialStyleSheet.NAVIGATION_INTERFACE.apply(self)
        MaterialStyleSheet.NAVIGATION_INTERFACE.apply(self.scrollWidget)
        self.__initLayout()

    def __initLayout(self):
        self.vBoxLayout.setContentsMargins(0, 0, 0, 15)
        self.topLayout.setContentsMargins(0, 0, 0, 0)
        self.bottomLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(4)
        self.topLayout.setSpacing(4)
        self.bottomLayout.setSpacing(4)
        self.scrollLayout.setSpacing(4)

        self.vBoxLayout.addLayout(self.topLayout, 0)
        self.vBoxLayout.addWidget(self.scrollArea)
        self.vBoxLayout.addLayout(self.bottomLayout, 0)

        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.topLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scrollLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.bottomLayout.setAlignment(Qt.AlignmentFlag.AlignBottom)

    def addItem(self, routeKey: str, icon: Union[str, QIcon, MaterialIconBase], text: str, onClick=None,
                selectable=True, selectedIcon=None, position=NavigationItemPosition.TOP):
        """ add navigation item

        Parameters
        ----------
        routeKey: str
            the unique name of item

        icon: str | QIcon | MaterialIconBase
            the icon of navigation item

        text: str
            the text of navigation item

        onClick: callable
            the slot connected to item clicked signal

        selectable: bool
            whether the item is selectable

        selectedIcon: str | QIcon | MaterialIconBase
            the icon of navigation item in selected state

        position: NavigationItemPosition
            where the button is added
        """
        return self.insertItem(-1, routeKey, icon, text, onClick, selectable, selectedIcon, position)

    def addWidget(self, routeKey: str, widget: NavigationWidget, onClick=None, position=NavigationItemPosition.TOP):
        """ add custom widget

        Parameters
        ----------
        routeKey: str
            the unique name of item

        widget: NavigationWidget
            the custom widget to be added

        onClick: callable
            the slot connected to item clicked signal

        position: NavigationItemPosition
            where the button is added
        """
        self.insertWidget(-1, routeKey, widget, onClick, position)

    def insertItem(self, index: int, routeKey: str, icon: Union[str, QIcon, MaterialIconBase], text: str, onClick=None,
                   selectable=True, selectedIcon=None, position=NavigationItemPosition.TOP):
        """ insert navigation tree item

        Parameters
        ----------
        index: int
            the insert position of parent widget

        routeKey: str
            the unique name of item

        icon: str | QIcon | MaterialIconBase
            the icon of navigation item

        text: str
            the text of navigation item

        onClick: callable
            the slot connected to item clicked signal

        selectable: bool
            whether the item is selectable

        selectedIcon: str | QIcon | MaterialIconBase
            the icon of navigation item in selected state

        position: NavigationItemPosition
            where the button is added
        """
        if routeKey in self.items:
            return

        w = NavigationPushButton(icon, text, selectable, selectedIcon, self)
        self.insertWidget(index, routeKey, w, onClick, position)
        return w

    def insertWidget(self, index: int, routeKey: str, widget: NavigationWidget, onClick=None,
                     position=NavigationItemPosition.TOP):
        """ insert custom widget

        Parameters
        ----------
        index: int
            insert position

        routeKey: str
            the unique name of item

        widget: NavigationWidget
            the custom widget to be added

        onClick: callable
            the slot connected to item clicked signal

        position: NavigationItemPosition
            where the button is added
        """
        if routeKey in self.items:
            return

        self._registerWidget(routeKey, widget, onClick)
        self._insertWidgetToLayout(index, widget, position)

    def _registerWidget(self, routeKey: str, widget: NavigationWidget, onClick):
        """ register widget """
        widget.clicked.connect(self._onWidgetClicked)

        if onClick is not None:
            widget.clicked.connect(onClick)

        widget.setProperty('routeKey', routeKey)
        self.items[routeKey] = widget

    def _insertWidgetToLayout(self, index: int, widget: NavigationWidget, position: NavigationItemPosition):
        """ insert widget to layout """
        if position == NavigationItemPosition.TOP:
            widget.setParent(self)
            self.topLayout.insertWidget(index, widget, 0, Qt.AlignTop | Qt.AlignHCenter)
        elif position == NavigationItemPosition.SCROLL:
            widget.setParent(self.scrollWidget)
            self.scrollLayout.insertWidget(index, widget, 0, Qt.AlignTop | Qt.AlignHCenter)
        else:
            widget.setParent(self)
            self.bottomLayout.insertWidget(index, widget, 0, Qt.AlignBottom | Qt.AlignHCenter)

        widget.show()

