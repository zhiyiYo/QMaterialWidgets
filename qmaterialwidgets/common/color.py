# coding:utf-8
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QColor, QPalette


def mixColor(c1: QColor, c2: QColor, weight: float):
    """ mix two color

    Parameters
    ----------
    c1, c2: QColor
        the color to be mixed

    weight: float
        the weight of first color
    """
    r = int(c1.red()*weight + c2.red()*(1-weight))
    g = int(c1.green()*weight + c2.green()*(1-weight))
    b = int(c1.blue()*weight + c2.blue()*(1-weight))
    return QColor(r, g, b)


def mixLight(color: QColor, weight: float):
    """ mix color with white

    Parameters
    ----------
    color: QColor
        the color to be mixed

    weight: float
        the weight of `color`
    """
    return mixColor(color, QColor(255, 255, 255), weight)

def mixDark(color: QColor, weight: float):
    """ mix color with black

    Parameters
    ----------
    color: QColor
        the color to be mixed

    weight: float
        the weight of `color`
    """
    return mixColor(color, QColor(0, 0, 0), weight)


def translucent(color: QColor, alpha: int):
    return QColor(color.red(), color.green(), color.blue(), alpha)