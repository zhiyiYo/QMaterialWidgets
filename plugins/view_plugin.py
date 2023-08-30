# coding: utf-8
from PyQt5.QtDesigner import QPyDesignerCustomWidgetPlugin

from qmaterialwidgets import TableView, TableWidget, ListWidget, ListView

from plugin_base import PluginBase


class ViewPlugin(PluginBase):

    def group(self):
        return super().group() + ' (View)'



class ListWidgetPlugin(ViewPlugin, QPyDesignerCustomWidgetPlugin):
    """ List widget plugin """

    def createWidget(self, parent):
        return ListWidget(parent)

    def icon(self):
        return super().icon("ListView")

    def name(self):
        return "ListWidget"



class ListViewPlugin(ViewPlugin, QPyDesignerCustomWidgetPlugin):
    """ List view plugin """

    def createWidget(self, parent):
        return ListView(parent)

    def icon(self):
        return super().icon("ListView")

    def name(self):
        return "ListView"



class TableWidgetPlugin(ViewPlugin, QPyDesignerCustomWidgetPlugin):
    """ Table widget plugin """

    def createWidget(self, parent):
        return TableWidget(parent)

    def icon(self):
        return super().icon("DataGrid")

    def name(self):
        return "TableWidget"


class TableViewPlugin(ViewPlugin, QPyDesignerCustomWidgetPlugin):
    """ Table widget plugin """

    def createWidget(self, parent):
        return TableView(parent)

    def icon(self):
        return super().icon("DataGrid")

    def name(self):
        return "TableView"

