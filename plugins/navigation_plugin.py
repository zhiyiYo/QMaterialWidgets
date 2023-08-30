# coding: utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtDesigner import QPyDesignerCustomWidgetPlugin

from qmaterialwidgets import NavigationRail, NavigationBar, TabWidget, SegmentedWidget, NavigationBar, FluentIcon

from plugin_base import PluginBase


class NavigationPlugin(PluginBase):

    def group(self):
        return super().group() + ' (Navigation)'


class NavigationRailPlugin(NavigationPlugin, QPyDesignerCustomWidgetPlugin):
    """ Navigation rail plugin """

    def createWidget(self, parent):
        return NavigationRail(parent)

    def icon(self):
        return super().icon("NavigationView")

    def name(self):
        return "NavigationRail"


class NavigationBarPlugin(NavigationPlugin, QPyDesignerCustomWidgetPlugin):
    """ Navigation abr plugin """

    def createWidget(self, parent):
        return NavigationBar(parent)

    def icon(self):
        return super().icon("NavigationView")

    def name(self):
        return "NavigationBar"


class TabWidgetPlugin(NavigationPlugin, QPyDesignerCustomWidgetPlugin):
    """ Tab widget plugin """

    def createWidget(self, parent):
        p = TabWidget(parent)
        for i in range(1, 4):
            p.addItem(f'Item{i}', f'Item{i}', print, FluentIcon.BASKETBALL)

        p.setCurrentItem('Item1')
        return p

    def icon(self):
        return super().icon("TabView")

    def name(self):
        return "TabWidget"

