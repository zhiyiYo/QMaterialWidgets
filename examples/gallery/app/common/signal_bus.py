# coding: utf-8
from PyQt5.QtCore import QObject, pyqtSignal


class SignalBus(QObject):
    """ pyqtSignal bus """

    switchToSampleCard = pyqtSignal(str, int)
    toggleThemeSignal = pyqtSignal()


signalBus = SignalBus()