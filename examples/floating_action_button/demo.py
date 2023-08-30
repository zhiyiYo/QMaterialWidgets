# coding:utf-8
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout

from qmaterialwidgets import (SurfaceFloatingActionButton, StrongBodyLabel, FluentIcon,
                              PrimaryFloatingActionButton, FloatingActionButtonSize,
                              SecondaryFloatingActionButton, TertiaryFloatingActionButton, Theme, setTheme)



class ButtonView(QWidget):
    """ Button view """

    def __init__(self, title: str, parent=None):
        super().__init__(parent=parent)
        self.setStyleSheet('Demo{background: rgb(254, 247, 255)}')
        self.vBoxLayout = QVBoxLayout(self)

        self.vBoxLayout.addWidget(StrongBodyLabel(title))
        self.vBoxLayout.setContentsMargins(30, 0, 30, 30)
        self.vBoxLayout.setSpacing(15)

    def addButtons(self, buttons):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(30)
        layout.setAlignment(Qt.AlignLeft)

        for button in buttons:
            layout.addWidget(button, 0, Qt.AlignLeft)

        self.vBoxLayout.addLayout(layout)


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        # self.setStyleSheet('Demo{background:rgb(32,32,32)}')
        self.setStyleSheet('Demo{background:rgb(254, 247, 255)}')

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.setSpacing(0)

        self.addButton('Surface', SurfaceFloatingActionButton, FluentIcon.HEART)
        self.addButton('Primary', PrimaryFloatingActionButton, FluentIcon.TRAIN)
        self.addButton('Secondary', SecondaryFloatingActionButton, FluentIcon.BUS)
        self.addButton('Tertiary', TertiaryFloatingActionButton, FluentIcon.CAFE)

    def addButton(self, title, Button, icon):
        view = ButtonView(title, self)

        for size in list(FloatingActionButtonSize._member_map_.values())[:2]:
            button1 = Button(icon)
            button1.setButtonSize(size)

            button2 = Button(icon)
            button2.setText('label')
            button2.setButtonSize(size)
            view.addButtons([button1, button2])

        self.vBoxLayout.addWidget(view)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
