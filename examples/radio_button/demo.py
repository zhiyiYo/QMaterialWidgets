# coding:utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from qmaterialwidgets import RadioButton, setTheme, Theme


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        setTheme(Theme.DARK)
        self.setStyleSheet('Demo{background:rgb(20, 18, 24)}')

        self.vBoxLayout = QVBoxLayout(self)
        self.button1 = RadioButton('Option 1', self)
        self.button2 = RadioButton('Option 2', self)
        self.button3 = RadioButton('Option 3', self)

        self.vBoxLayout.addWidget(self.button1, 0, Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.button2, 0, Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.button3, 0, Qt.AlignCenter)
        self.button2.setDisabled(True)
        self.button2.setChecked(True)
        self.resize(300, 150)


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
