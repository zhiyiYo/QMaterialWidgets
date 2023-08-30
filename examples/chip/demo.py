# coding:utf-8
import sys
from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QVBoxLayout, QHBoxLayout

from qmaterialwidgets import (InputChip, StrongBodyLabel, palette, FluentIcon, setTheme, Theme,
                              ElevatedInputChip, FilterChip, RoundMenu, Action, ElevatedFilterChip)


class ChipView(QFrame):
    """ Chip view """

    def __init__(self, title: str, parent=None):
        super().__init__(parent=parent)
        self.vBoxLayout = QVBoxLayout(self)

        self.vBoxLayout.setSpacing(15)
        self.vBoxLayout.setContentsMargins(30, 15, 30, 20)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(StrongBodyLabel(title, self))

        self.setStyleSheet(f"""
            ChipView {{
                border: 1px solid {palette.outlineVariant.name()};
                border-radius: 14px;
                background: {palette.surface.name()};
        }}""")

    def addChips(self, chips: list):
        """ add chips """
        layout = QHBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(0, 0, 0, 0)
        for chip in chips:
            layout.addWidget(chip, 0, Qt.AlignmentFlag.AlignLeft)

        self.vBoxLayout.addLayout(layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        self.setStyleSheet('Demo{background:white}')

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.setContentsMargins(30, 30, 30, 30)
        self.vBoxLayout.setSpacing(30)

        # input chips
        self.addInputChips()

        # filter chips
        self.addFilterChips()

    def addInputChips(self):
        self.inputChip1 = InputChip('Label', self)
        self.inputChip2 = InputChip('Label', self)
        self.inputChip3 = InputChip('Label', self, FluentIcon.CAR)
        self.inputChip4 = InputChip('Label', self, FluentIcon.CAR)
        self.elevatedInputChip1 = ElevatedInputChip('Label', self, FluentIcon.CAR)

        self.inputChip5 = InputChip('Label', self)
        self.inputChip6 = InputChip('Label', self)
        self.inputChip7 = InputChip('Label', self, FluentIcon.CAR)
        self.inputChip8 = InputChip('Label', self, FluentIcon.CAR)
        self.elevatedInputChip2 = ElevatedInputChip('Label', self, FluentIcon.CAR)
        self.selectableInputs = [
            self.inputChip5, self.inputChip6, self.inputChip7,
            self.inputChip8, self.elevatedInputChip2
        ]

        self.inputChip2.setClosable(True)
        self.inputChip4.setClosable(True)
        self.inputChip6.setClosable(True)
        self.inputChip8.setClosable(True)
        for chip in self.selectableInputs:
            chip.setCheckable(True)
            chip.setChecked(True)

        self.addChipView('Input chips', [
            [self.inputChip1, self.inputChip2, self.inputChip3, self.inputChip4, self.elevatedInputChip1],
            self.selectableInputs,
        ])

    def addFilterChips(self):
        self.dropMenu = RoundMenu(parent=self)
        self.dropMenu.addActions([
            Action(FluentIcon.BUS, 'Bus'),
            Action(FluentIcon.TRAIN, 'Train'),
        ])

        self.filterChip1 = FilterChip('Label', self)
        self.filterChip2 = FilterChip('Label', self)
        self.filterChip3 = FilterChip('Label', self, FluentIcon.CAR)
        self.filterChip4 = FilterChip('Label', self, FluentIcon.CAR)
        self.elevatedFilterChip1 = ElevatedFilterChip('Label', self, FluentIcon.CAR)

        self.filterChip5 = FilterChip('Label', self)
        self.filterChip6 = FilterChip('Label', self)
        self.filterChip7 = FilterChip('Label', self, FluentIcon.CAR)
        self.filterChip8 = FilterChip('Label', self, FluentIcon.CAR)
        self.elevatedFilterChip2 = ElevatedFilterChip('Label', self, FluentIcon.CAR)
        self.selectableFilters = [
            self.filterChip5, self.filterChip6, self.filterChip7,
            self.filterChip8, self.elevatedFilterChip2
        ]

        self.filterChip2.setMenu(self.dropMenu)
        self.filterChip4.setMenu(self.dropMenu)
        self.filterChip6.setMenu(self.dropMenu)
        self.filterChip8.setMenu(self.dropMenu)

        for chip in self.selectableFilters:
            chip.setCheckable(True)
            chip.setChecked(True)

        self.addChipView('Filter chips', [
            [self.filterChip1, self.filterChip2, self.filterChip3, self.filterChip4, self.elevatedFilterChip1],
            self.selectableFilters,
        ])

    def addChipView(self, title: str, chips: List[list]):
        """ add chip view """
        view = ChipView(title, self)
        for row in chips:
            view.addChips(row)

        self.vBoxLayout.addWidget(view)


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
