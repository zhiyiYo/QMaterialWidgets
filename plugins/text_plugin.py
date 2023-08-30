# coding: utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtDesigner import QPyDesignerCustomWidgetPlugin

from qmaterialwidgets import (SpinBox, DoubleSpinBox, TextEdit, TimeEdit, DateTimeEdit, LineEdit,
                              DateEdit, SearchLineEdit, FilledSearchLineEdit, FilledLineEdit, FilledTextEdit)

from plugin_base import PluginBase


class TextPlugin(PluginBase):

    def group(self):
        return super().group() + ' (Text)'


class LineEditPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Line edit plugin """

    def createWidget(self, parent):
        return LineEdit(parent)

    def icon(self):
        return super().icon("TextBox")

    def name(self):
        return "LineEdit"


class FilledLineEditPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Line edit plugin """

    def createWidget(self, parent):
        return FilledLineEdit(parent)

    def icon(self):
        return super().icon("TextBox")

    def name(self):
        return "FilledLineEdit"


class SearchLineEditPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Search line edit plugin """

    def createWidget(self, parent):
        return SearchLineEdit(parent)

    def icon(self):
        return super().icon("TextBox")

    def name(self):
        return "SearchLineEdit"


class FilledSearchLineEditPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Search line edit plugin """

    def createWidget(self, parent):
        return FilledSearchLineEdit(parent)

    def icon(self):
        return super().icon("TextBox")

    def name(self):
        return "FilledSearchLineEdit"


class TextEditPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Text edit plugin """

    def createWidget(self, parent):
        return TextEdit(parent)

    def icon(self):
        return super().icon("RichEditBox")

    def name(self):
        return "TextEdit"


class FilledTextEditPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Filled text edit plugin """

    def createWidget(self, parent):
        return FilledTextEdit(parent)

    def icon(self):
        return super().icon("RichEditBox")

    def name(self):
        return "FilledTextEdit"


class DateEditPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Date edit plugin """

    def createWidget(self, parent):
        return DateEdit(parent)

    def icon(self):
        return super().icon("NumberBox")

    def name(self):
        return "DateEdit"


class TimeEditPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Time edit plugin """

    def createWidget(self, parent):
        return TimeEdit(parent)

    def icon(self):
        return super().icon("NumberBox")

    def name(self):
        return "TimeEdit"


class DateTimeEditPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Date time edit plugin """

    def createWidget(self, parent):
        return DateTimeEdit(parent)

    def icon(self):
        return super().icon("NumberBox")

    def name(self):
        return "DateTimeEdit"


class SpinBoxPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Spin box plugin """

    def createWidget(self, parent):
        return SpinBox(parent)

    def icon(self):
        return super().icon("NumberBox")

    def name(self):
        return "SpinBox"


class DoubleSpinBoxPlugin(TextPlugin, QPyDesignerCustomWidgetPlugin):
    """ Double spin box plugin """

    def createWidget(self, parent):
        return DoubleSpinBox(parent)

    def icon(self):
        return super().icon("NumberBox")

    def name(self):
        return "DoubleSpinBox"
