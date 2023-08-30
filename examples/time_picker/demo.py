# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout

from qmaterialwidgets import TimePickerDialog, setTheme, Theme, FilledSearchLineEdit, palette, TimePicker


class Demo(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # setTheme(Theme.DARK)
        self.setStyleSheet(f'Demo{{background:{palette.surface.name()}}}')
        self.setFixedSize(700, 500)

        self.lineEdit = FilledSearchLineEdit(self)
        self.picker = TimePicker(self)

        self.lineEdit.setLabel('Label')
        self.setLayout(QVBoxLayout(self))
        self.layout().addWidget(self.lineEdit)
        self.layout().addWidget(self.picker)
        self.layout().setContentsMargins(50, 50, 50, 50)

        # self.picker.setTime(QTime(13, 14))
        # self.picker.setFormat(Qt.DateFormat.ISODateWithMs)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
