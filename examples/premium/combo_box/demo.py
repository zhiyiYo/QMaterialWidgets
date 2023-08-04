# coding:utf-8
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QCompleter, QHBoxLayout, QComboBox

from qmaterialwidgets import ComboBox, FilledComboBox, setTheme, Theme, setThemeColor, setFont, palette


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        self.setStyleSheet('Demo{background:white}')

        self.hBoxLayout = QHBoxLayout(self)
        self.comboBox = ComboBox(self)
        self.comboBox.setLabel('脑婆')

        items = ['shoko 🥰', '西宫硝子', 'aiko', '柳井爱子']
        self.comboBox.addItems(items)
        self.comboBox.setCurrentIndex(0)
        self.comboBox.currentTextChanged.connect(print)

        # setFont(self.comboBox, 16)
        # self.comboBox.setEditable(True)

        # NOTE: Completer is only applicable to editable combo box
        # self.completer = QCompleter(items, self)
        # self.comboBox.setCompleter(self.completer)

        self.resize(500, 500)
        self.comboBox.setFixedWidth(200)
        self.hBoxLayout.addWidget(self.comboBox)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()