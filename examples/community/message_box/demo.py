# coding:utf-8
import sys
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QApplication, QWidget, QDialogButtonBox

from qmaterialwidgets import MessageBox, setTheme, Theme, FilledPushButton, palette, FluentIcon


class Demo(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.resize(950, 500)
        self.btn = FilledPushButton('Click Me', parent=self)
        self.btn.move(425, 225)
        self.btn.clicked.connect(self.showDialog)

        # setTheme(Theme.DARK)
        self.setStyleSheet(f'Demo{{background:{palette.surface.name()}}}')

    def showDialog(self):
        title = 'Are you sure you want to delete the folder?'
        content = """If you delete the "Music" folder from the list, the folder will no longer appear in the list"""
        w = MessageBox(title, content, self, ":/qmaterialwidgets/images/logo.png")
        w.setIconSize(QSize(50, 50))

        # NOTE: add custom button to button box
        # w.addButton(FilledPushButton('Apply'), QDialogButtonBox.ButtonRole.ApplyRole)

        if w.exec():
            print('Yes button is pressed')
        else:
            print('Cancel button is pressed')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
