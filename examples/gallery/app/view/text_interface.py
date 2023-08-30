# coding:utf-8
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCompleter
from qmaterialwidgets import (LineEdit, FilledLineEdit, SearchLineEdit, FilledSearchLineEdit,
                              TextEdit, FilledTextEdit, SpinBox, TimeEdit, DateTimeEdit, DateEdit,
                              DoubleSpinBox)

from .gallery_interface import GalleryInterface
from ..common.translator import Translator


class TextInterface(GalleryInterface):
    """ Text interface """

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.text,
            subtitle="qmaterialwidgets.components.widgets",
            parent=parent
        )
        self.setObjectName('textInterface')

        # line edit
        lineEdit = LineEdit(self)
        lineEdit.setLabel('JoJo')
        lineEdit.setText(self.tr('ko no dio da！'))
        lineEdit.setClearButtonEnabled(True)
        lineEdit.setFixedWidth(250)
        self.addExampleCard(
            title=self.tr("A outlined line edit"),
            widget=lineEdit,
            sourcePath='https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/line_edit/demo.py'
        )

        # line edit with completer
        lineEdit = self.createSearchLineEdit(False)
        stands = [
            "Star Platinum", "Hierophant Green",
            "Made in Haven", "King Crimson",
            "Silver Chariot", "Crazy diamond",
            "Metallica", "Another One Bites The Dust",
            "Heaven's Door", "Killer Queen",
            "The Grateful Dead", "Stone Free",
            "The World", "Sticky Fingers",
            "Ozone Baby", "Love Love Deluxe",
            "Hermit Purple", "Gold Experience",
            "King Nothing", "Paper Moon King",
            "Scary Monster", "Mandom",
            "20th Century Boy", "Tusk Act 4",
            "Ball Breaker", "Sex Pistols",
            "D4C • Love Train", "Born This Way",
            "SOFT & WET", "Paisley Park",
            "Wonder of U", "Walking Heart",
            "Cream Starter", "November Rain",
            "Smooth Operators", "The Matte Kudasai"
        ]
        completer = QCompleter(stands, lineEdit)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        lineEdit.setCompleter(completer)
        self.addExampleCard(
            title=self.tr("A autosuggest line edit"),
            widget=lineEdit,
            sourcePath='https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/line_edit/demo.py'
        )

        # line edit in error state
        lineEdit = self.createSearchLineEdit()
        lineEdit.setError(True)
        self.addExampleCard(
            title=self.tr("A line edit in the error state"),
            widget=lineEdit,
            sourcePath='https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/line_edit/demo.py'
        )

        # filled line edit
        self.addExampleCard(
            title=self.tr("A filled line edit"),
            widget=self.createFilledLineEdit(False),
            sourcePath='https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/line_edit/demo.py'
        )

        lineEdit = self.createFilledLineEdit()
        lineEdit.setError(True)
        self.addExampleCard(
            title=self.tr("A filled line edit in the error state"),
            widget=lineEdit,
            sourcePath='https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/line_edit/demo.py'
        )

        # spin box
        spinBox = SpinBox(self)
        spinBox.setLabel(self.tr('Label'))
        self.addExampleCard(
            title=self.tr("A spin box"),
            widget=spinBox,
            sourcePath='https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/spin_box/demo.py'
        )

        # double spin box
        spinBox = DoubleSpinBox(self)
        spinBox.setLabel(self.tr('Double'))
        self.addExampleCard(
            title=self.tr("A double spin box"),
            widget=spinBox,
            sourcePath='https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/spin_box/demo.py'
        )

        # date edit
        spinBox = DateEdit(self)
        spinBox.setLabel(self.tr('Date'))
        self.addExampleCard(
            title=self.tr("A date edit"),
            widget=spinBox,
            sourcePath='https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/spin_box/demo.py'
        )

        # time edit
        spinBox = TimeEdit(self)
        spinBox.setLabel(self.tr('Time'))
        self.addExampleCard(
            title=self.tr("A time edit"),
            widget=spinBox,
            sourcePath='https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/spin_box/demo.py'
        )

        # date time edit
        spinBox = DateTimeEdit(self)
        spinBox.setLabel(self.tr('Date time'))
        self.addExampleCard(
            title=self.tr("A date time edit"),
            widget=spinBox,
            sourcePath='https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/spin_box/demo.py'
        )

        # text edit
        textEdit = TextEdit(self)
        textEdit.setLabel(self.tr('Multiline'))
        self.addExampleCard(
            title=self.tr("A multiline text edit"),
            widget=textEdit,
            sourcePath='https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/text_edit/demo.py'
        )

        # filled text edit
        textEdit = FilledTextEdit(self)
        textEdit.setLabel(self.tr('Multiline'))
        self.addExampleCard(
            title=self.tr("A filled multiline text edit"),
            widget=textEdit,
            sourcePath='https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/text_edit/demo.py'
        )

    def createSearchLineEdit(self, placeholder=True):
        lineEdit = SearchLineEdit(self)
        lineEdit.setLabel(self.tr('Stand'))
        lineEdit.setClearButtonEnabled(True)
        lineEdit.setFixedWidth(250)

        if placeholder:
            lineEdit.setPlaceholderText(self.tr('Type a stand name'))

        return lineEdit

    def createFilledLineEdit(self, placeholder=True):
        lineEdit = FilledSearchLineEdit(self)
        lineEdit.setLabel('Filled')
        lineEdit.setClearButtonEnabled(True)
        lineEdit.setFixedWidth(250)

        if placeholder:
            lineEdit.setPlaceholderText(self.tr('hint text'))

        return lineEdit
