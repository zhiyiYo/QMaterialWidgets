# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget

from qmaterialwidgets import SwitchButton, setTheme, Theme, palette


class Demo(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # setTheme(Theme.DARK)
        self.setStyleSheet('Demo{background:'+palette.surface.name()+'}')

        self.resize(160, 80)
        self.switchButton = SwitchButton(parent=self)
        self.switchButton.move(48, 24)
        self.switchButton.checkedChanged.connect(self.onCheckedChanged)

    def onCheckedChanged(self, isChecked: bool):
        text = 'On' if isChecked else 'Off'
        self.switchButton.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
