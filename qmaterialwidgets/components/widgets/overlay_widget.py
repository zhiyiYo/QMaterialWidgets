# coding:utf-8
from PyQt6.QtCore import Qt, pyqtSignal, QEvent
from PyQt6.QtGui import QPixmap, QPainter, QColor
from PyQt6.QtWidgets import QWidget


class OverlayWidget(QWidget):
    """ Overlay widget """

    def __init__(self, parent: QWidget):
        super().__init__(parent=parent)
        parent.installEventFilter(self)

    def eventFilter(self, obj, e):
        if obj is not self.parent():
            return super().eventFilter(obj, e)

        if e.type() in [QEvent.Type.Move, QEvent.Type.Resize]:
            self.setGeometry(self.overlayGeometry())

        return super().eventFilter(obj, e)

    def overlayGeometry(self):
        return self.parentWidget().rect()
