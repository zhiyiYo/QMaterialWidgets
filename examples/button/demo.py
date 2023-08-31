# coding:utf-8
import sys
from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout

from qmaterialwidgets import (OutlinedPushButton, FluentIcon, setTheme, Theme, TextPushButton,
                              StrongBodyLabel, FilledPushButton, ElevatedPushButton, TonalPushButton,
                              TransparentToolButton, FilledToolButton, TransparentToggleToolButton,
                              TonalToolButton, OutlinedToolButton, FilledToggleToolButton, OutlinedToggleToolButton,
                              OutlinedDropDownPushButton, FilledDropDownPushButton, RoundMenu, Action,
                              TextDropDownPushButton, ElevatedDropDownPushButton, TonalDropDownPushButton, palette)



class ButtonView(QWidget):

    def __init__(self, title: str, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = StrongBodyLabel(title, self)
        self.vBoxLayout = QVBoxLayout(self)

        self.vBoxLayout.setSpacing(16)
        self.vBoxLayout.setContentsMargins(30, 0, 30, 20)
        self.vBoxLayout.addWidget(self.titleLabel)

    def addButtons(self, buttons: list):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignLeft)

        for button in buttons:
            layout.addWidget(button)

        self.vBoxLayout.addLayout(layout)



class Widget(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        self.setStyleSheet('Widget{background: '+palette.surface.name()+'}')

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(15)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.setContentsMargins(0, 30, 0, 30)

    def addButtons(self, title: list, buttons: list):
        view = ButtonView(title, self)
        view.addButtons(buttons)
        self.vBoxLayout.addWidget(view)


class Demo1(Widget):

    def __init__(self):
        super().__init__()

        # transparent buttons
        self.transparentButton1 = TransparentToolButton(FluentIcon.SETTING, self)
        self.transparentButton2 = TransparentToolButton(FluentIcon.SETTING, self)
        self.transparentToggleButton1 = TransparentToggleToolButton(FluentIcon.GITHUB, self)
        self.transparentToggleButton2 = TransparentToggleToolButton(FluentIcon.GITHUB, self)
        self.transparentButton2.setEnabled(False)
        self.transparentToggleButton1.setChecked(True)
        self.transparentToggleButton2.setEnabled(False)
        self.addButtons('Transparent buttons', [
            self.transparentButton1, self.transparentButton2,
            self.transparentToggleButton1, self.transparentToggleButton2
        ])

        # filled buttons
        self.filledButton1 = FilledToolButton(FluentIcon.GITHUB, self)
        self.filledButton2 = FilledToolButton(FluentIcon.GITHUB, self)
        self.filledToggleButton1 = FilledToggleToolButton(FluentIcon.GITHUB, self)
        self.filledToggleButton2 = FilledToggleToolButton(FluentIcon.GITHUB, self)
        self.filledButton2.setEnabled(False)
        self.filledToggleButton1.setChecked(True)
        self.filledToggleButton2.setEnabled(False)
        self.addButtons('Filled buttons', [
            self.filledButton1, self.filledButton2,
            self.filledToggleButton1, self.filledToggleButton2,
        ])

        # tonal butons
        self.tonalButton1 = TonalToolButton(FluentIcon.TRAIN, self)
        self.tonalButton2 = TonalToolButton(FluentIcon.TRAIN, self)
        self.tonalButton2.setEnabled(False)
        self.addButtons('Tonal buttons', [self.tonalButton1, self.tonalButton2])

        # outlined butons
        self.outlinedButton1 = OutlinedToolButton(FluentIcon.BUS, self)
        self.outlinedButton2 = OutlinedToolButton(FluentIcon.BUS, self)
        self.outlinedToggleButton1 = OutlinedToggleToolButton(FluentIcon.BUS, self)
        self.outlinedToggleButton2 = OutlinedToggleToolButton(FluentIcon.BUS, self)
        self.outlinedButton2.setEnabled(False)
        self.outlinedToggleButton1.setChecked(True)
        self.outlinedToggleButton2.setEnabled(False)
        self.addButtons('Outlined buttons', [
            self.outlinedButton1, self.outlinedButton2,
            self.outlinedToggleButton1, self.outlinedToggleButton2,
        ])



class Demo2(Widget):

    def __init__(self):
        super().__init__()
        self.dropDownMenu = RoundMenu(parent=self)
        self.dropDownMenu.addActions([
            Action(FluentIcon.SEND_FILL, 'Send'),
            Action(FluentIcon.SAVE, 'Save'),
        ])

        # outlined buttons
        self.filledButton1 = FilledPushButton('Label', self)
        self.filledButton2 = FilledPushButton('Label', self)
        self.filledButton3 = FilledPushButton('Label', self, FluentIcon.GITHUB)
        self.filledButton4 = FilledPushButton('Label', self, FluentIcon.GITHUB)
        self.filledButton5 = FilledDropDownPushButton('Label', self, FluentIcon.GITHUB)
        self.filledButton2.setEnabled(False)
        self.filledButton4.setEnabled(False)
        self.filledButton5.setMenu(self.dropDownMenu)
        self.addButtons('Filled buttons', [
            self.filledButton1, self.filledButton2,
            self.filledButton3, self.filledButton4,
            self.filledButton5
        ])

        # outlined buttons
        self.outlinedButton1 = OutlinedPushButton('Label', self)
        self.outlinedButton2 = OutlinedPushButton('Label', self)
        self.outlinedButton3 = OutlinedPushButton('Label', self, FluentIcon.GITHUB)
        self.outlinedButton4 = OutlinedPushButton('Label', self, FluentIcon.GITHUB)
        self.outlinedButton5 = OutlinedDropDownPushButton('Label', self, FluentIcon.GITHUB)
        self.outlinedButton5.setMenu(self.dropDownMenu)
        self.outlinedButton2.setEnabled(False)
        self.outlinedButton4.setEnabled(False)
        self.addButtons('Outlined buttons', [
            self.outlinedButton1, self.outlinedButton2,
            self.outlinedButton3, self.outlinedButton4,
            self.outlinedButton5
        ])

        # text buttons
        self.textButton1 = TextPushButton('Label', self)
        self.textButton2 = TextPushButton('Label', self)
        self.textButton3 = TextPushButton('Label', self, FluentIcon.TRAIN)
        self.textButton4 = TextPushButton('Label', self, FluentIcon.TRAIN)
        self.textButton5 = TextDropDownPushButton('Label', self, FluentIcon.TRAIN)
        self.textButton5.setMenu(self.dropDownMenu)
        self.textButton2.setEnabled(False)
        self.textButton4.setEnabled(False)
        self.addButtons('Text buttons', [
            self.textButton1, self.textButton2,
            self.textButton3, self.textButton4,
            self.textButton5
        ])

        # elevated buttons
        self.elevatedButton1 = ElevatedPushButton('Label', self)
        self.elevatedButton2 = ElevatedPushButton('Label', self)
        self.elevatedButton3 = ElevatedPushButton('Label', self, FluentIcon.BUS)
        self.elevatedButton4 = ElevatedPushButton('Label', self, FluentIcon.BUS)
        self.elevatedButton5 = ElevatedDropDownPushButton('Label', self, FluentIcon.BUS)
        self.elevatedButton5.setMenu(self.dropDownMenu)
        self.elevatedButton2.setEnabled(False)
        self.elevatedButton4.setEnabled(False)
        self.addButtons('Elevated buttons', [
            self.elevatedButton1, self.elevatedButton2,
            self.elevatedButton3, self.elevatedButton4,
            self.elevatedButton5
        ])

        # elevated buttons
        self.tonalButton1 = TonalPushButton('Label', self)
        self.tonalButton2 = TonalPushButton('Label', self)
        self.tonalButton3 = TonalPushButton('Label', self, FluentIcon.BUS)
        self.tonalButton4 = TonalPushButton('Label', self, FluentIcon.BUS)
        self.tonalButton5 = TonalDropDownPushButton('Label', self, FluentIcon.BUS)
        self.tonalButton5.setMenu(self.dropDownMenu)
        self.tonalButton2.setEnabled(False)
        self.tonalButton4.setEnabled(False)
        self.addButtons('Tonal buttons', [
            self.tonalButton1, self.tonalButton2,
            self.tonalButton3, self.tonalButton4,
            self.tonalButton5
        ])

        self.resize(500, 500)



if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w1 = Demo1()
    w1.show()
    w2 = Demo2()
    w2.show()
    app.exec()