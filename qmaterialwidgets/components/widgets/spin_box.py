# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal, QEvent
from PyQt5.QtWidgets import (QSpinBox, QDoubleSpinBox, QToolButton, QHBoxLayout,
                               QDateEdit, QDateTimeEdit, QTimeEdit, QLineEdit, QAbstractSpinBox)

from ...common.style_sheet import MaterialStyleSheet
from ...common.font import setFont
from ...common.icon import Action
from .line_edit import LineEdit, LineEditIcon
from .menu import LineEditMenu


class SpinBoxBase:
    """ Spin box ui """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        setFont(self)

        self._edit = LineEdit(self)
        self.downButton = self._edit.setLeadingAction(Action(LineEditIcon.MINUS, ''))
        self.upButton = self._edit.setTrailingAction(Action(LineEditIcon.ADD, ''))
        self.setLineEdit(self._edit)

        self._edit.setClearButtonEnabled(False)

        self.upButton.clicked.connect(self.stepUp)
        self.downButton.clicked.connect(self.stepDown)

        self.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._showContextMenu)

        self.setFixedHeight(self.lineEdit().height()+3)
        self.installEventFilter(self.lineEdit())

    def eventFilter(self, obj, e):
        if obj is not self.lineEdit() or e.type() != QEvent.Type.Resize:
            return super().eventFilter(obj, e)

        if e.oldSize().height() != e.size().height():
            self.setFixedHeight(e.size().height()+3)

        return super().eventFilter(obj, e)

    def _showContextMenu(self, pos):
        menu = LineEditMenu(self.lineEdit())
        menu.exec_(self.mapToGlobal(pos))

    def setAccelerated(self, on: bool):
        super().setAccelerated(on)
        self.upButton.setAutoRepeat(on)
        self.downButton.setAutoRepeat(on)

    def paintEvent(self, e):
        pass

    def setLabel(self, label: str):
        self._edit.setLabel(label)
        self._edit.labelLabel.up()
        self.setFixedHeight(self._edit.height()+3)

    def setError(self, isError: bool):
        self._edit.setError(isError)

    def isError(self):
        return self._edit.isError()


class SpinBox(SpinBoxBase, QSpinBox):
    """ Spin box """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setMinimumWidth(120)


class DoubleSpinBox(SpinBoxBase, QDoubleSpinBox):
    """ Double spin box """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setMinimumWidth(140)


class TimeEdit(SpinBoxBase, QTimeEdit):
    """ Time edit """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setMinimumWidth(130)


class DateTimeEdit(SpinBoxBase, QDateTimeEdit):
    """ Date time edit """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setMinimumWidth(210)


class DateEdit(SpinBoxBase, QDateEdit):
    """ Date edit """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setMinimumWidth(175)
