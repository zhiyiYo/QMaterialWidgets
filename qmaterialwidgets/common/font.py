# coding: utf-8
from PySide2.QtGui import QFont, QFontDatabase
from PySide2.QtWidgets import QWidget, QApplication


def setFont(widget: QWidget, fontSize=14, weight=QFont.Weight.Normal):
    """ set the font of widget

    Parameters
    ----------
    widget: QWidget
        the widget to set font

    fontSize: int
        font pixel size

    weight: `QFont.Weight`
        font weight
    """
    widget.setFont(getFont(fontSize, weight))


def getFont(fontSize=14, weight=QFont.Weight.Normal):
    """ create font

    Parameters
    ----------
    fontSize: int
        font pixel size

    weight: `QFont.Weight`
        font weight
    """
    font = QFont()
    font.setFamilies(['Roboto', 'Segoe UI', 'Microsoft YaHei', 'PingFang SC'])
    font.setPixelSize(fontSize)
    font.setWeight(weight)
    return font


def registerFonts():
    QFontDatabase.addApplicationFont(":/qmaterialwidgets/fonts/Roboto-Bold.ttf")
    QFontDatabase.addApplicationFont(":/qmaterialwidgets/fonts/Roboto-Thin.ttf")
    QFontDatabase.addApplicationFont(":/qmaterialwidgets/fonts/Roboto-Light.ttf")
    QFontDatabase.addApplicationFont(":/qmaterialwidgets/fonts/Roboto-Medium.ttf")
    QFontDatabase.addApplicationFont(":/qmaterialwidgets/fonts/Roboto-Regular.ttf")

