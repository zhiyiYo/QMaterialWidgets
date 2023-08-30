# coding:utf-8
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QWidget

from qmaterialwidgets import Slider, setTheme, Theme, palette


class CustomSlider(Slider):

    def _bubbleText(self) -> str:
        return f"{(self.value()/10):.1f}"



class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        self.setStyleSheet(f'Demo{{background:{palette.surface.name()}}}')

        self.resize(300, 300)

        self.slider1 = Slider(Qt.Horizontal, self)
        self.slider1.setFixedWidth(250)
        self.slider1.move(40, 30)

        self.slider1 = CustomSlider(Qt.Horizontal, self)
        self.slider1.setFixedWidth(250)
        self.slider1.move(40, 80)

        self.slider3 = Slider(Qt.Vertical, self)
        self.slider3.setFixedHeight(150)
        self.slider3.move(130, 130)


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
