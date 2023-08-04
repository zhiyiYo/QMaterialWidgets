# coding:utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout

from qmaterialwidgets import FilledTextEdit, FilledPushButton, TextEdit, setTheme, Theme, palette


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        self.setStyleSheet('Demo{background:'+palette.surface.name()+'}')

        self.hBoxLayout = QHBoxLayout(self)
        self.filledTextEdit = FilledTextEdit(self)
        self.textEdit = TextEdit(self)

        self.filledTextEdit.setLabel('Label')
        self.textEdit.setLabel('JoJo7')
        self.textEdit.setMarkdown("* Lesson 1: 别对我抱有什么奇怪的期待 \n* Lesson 2: 不要让肌肉察觉 \n* Lesson 3: 相信回旋吧，只管相信就是了！\n* Lesson 4: 表达敬意吧，表达出敬意，然后迈向回旋的另一个全新阶段 \n* Lesson 5: 最短的捷径就是绕原路，绕远路才是我的最短捷径")

        self.hBoxLayout.setContentsMargins(30, 30, 30, 30)
        self.hBoxLayout.setSpacing(50)
        self.hBoxLayout.addWidget(self.filledTextEdit)
        self.hBoxLayout.addWidget(self.textEdit)
        self.resize(800, 400)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()