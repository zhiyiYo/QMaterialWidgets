# coding:utf-8
import sys
from typing import List

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout

from qmaterialwidgets import (FilledLineEdit, StrongBodyLabel, FilledSearchLineEdit, Action,
                              FluentIcon, setTheme, Theme, palette, LineEdit, SearchLineEdit)


class LineEditView(QWidget):

    def __init__(self, title: str, parent=None):
        super().__init__(parent=parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.titleLabel = StrongBodyLabel(title, self)

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 10)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

    def addLineEdits(self, lineEdits: list):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignLeft)
        self.vBoxLayout.addLayout(layout)

        for lineEdit in lineEdits:
            layout.addWidget(lineEdit)


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        self.setStyleSheet(f'Demo{{background:{palette.surface.name()}}}')

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(30)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.setContentsMargins(30, 30, 30, 30)

        # filled line edit
        self.filledLineEdit1 = FilledLineEdit(self)
        self.filledLineEdit2 = FilledLineEdit(self)
        self.filledLineEdit3 = FilledLineEdit(self)
        self.filledLineEdit4 = FilledSearchLineEdit(self)
        self.filledLineEdit5 = FilledSearchLineEdit(self)
        self.filledLineEdit6 = FilledSearchLineEdit(self)

        self.filledLineEdit3.setEnabled(False)
        self.filledLineEdit6.setEnabled(False)
        self.filledLineEdit2.setError(True)
        self.filledLineEdit5.setError(True)
        self.filledLineEdit4.setLabel('Label')
        self.filledLineEdit5.setLabel('Label')
        self.filledLineEdit6.setLabel('Label')

        # self.filledLineEdit1.setLabel('Label')
        # self.filledLineEdit1.setLeadingAction(Action(FluentIcon.BUS, 'Bus'))
        # self.filledLineEdit1.setTrailingAction(Action(FluentIcon.BUS, 'Bus'))

        self.addLineEditView('Filled line edits', [
            [self.filledLineEdit1, self.filledLineEdit2, self.filledLineEdit3],
            [self.filledLineEdit4, self.filledLineEdit5, self.filledLineEdit6],
        ])

        # outlined line edit
        self.lineEdit1 = LineEdit(self)
        self.lineEdit2 = LineEdit(self)
        self.lineEdit3 = LineEdit(self)
        self.lineEdit4 = SearchLineEdit(self)
        self.lineEdit5 = SearchLineEdit(self)
        self.lineEdit6 = SearchLineEdit(self)

        self.lineEdit3.setEnabled(False)
        self.lineEdit6.setEnabled(False)
        self.lineEdit2.setError(True)
        self.lineEdit5.setError(True)
        for lineEdit in self.findChildren(LineEdit):
            lineEdit.setLabel('Label')

        self.lineEdit1.setText('666')

        self.addLineEditView('Outlined line edits', [
            [self.lineEdit1, self.lineEdit2, self.lineEdit3],
            [self.lineEdit4, self.lineEdit5, self.lineEdit6],
        ])

    def addLineEditView(self, title, lineEdits: List[list]):
        view = LineEditView(title, self)
        for row in lineEdits:
            view.addLineEdits(row)

        self.vBoxLayout.addWidget(view)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()