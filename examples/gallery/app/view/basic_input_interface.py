# coding:utf-8
from PySide2.QtCore import Qt, QSize, QUrl
from PySide2.QtWidgets import QWidget, QVBoxLayout, QButtonGroup, QHBoxLayout
from qmaterialwidgets import (Action, OutlinedPushButton, TransparentToolButton, FilledPushButton,
                             RadioButton, CheckBox, Slider, SwitchButton, RoundMenu, FluentIcon,
                             FilledToolButton, TransparentToggleToolButton, TransparentToolButton,
                             OutlinedToolButton, TonalPushButton, TonalToolButton, TextPushButton,
                             ElevatedPushButton, OutlinedToggleToolButton, FilledToggleToolButton,
                             PrimaryFloatingActionButton, SurfaceFloatingActionButton,
                             SecondaryFloatingActionButton, TertiaryFloatingActionButton, ComboBox,
                             FilledComboBox)

from .gallery_interface import GalleryInterface
from ..common.translator import Translator


class BasicInputInterface(GalleryInterface):
    """ Basic input interface """

    def __init__(self, parent=None):
        translator = Translator()
        super().__init__(
            title=translator.basicInput,
            subtitle='qmaterialwidgets.components.widgets',
            parent=parent
        )
        self.setObjectName('basicInputInterface')

        # elevated push button
        self.addExampleCard(
            self.tr('Outlined push button'),
            ElevatedPushButton(self.tr('Elevated push button'), self, FluentIcon.BUS),
            'https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/button/demo.py'
        )

        # Floating action push button
        self.addExampleCard(
            self.tr('Floating action push button'),
            self.createPushFAB(),
            'https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/button/demo.py'
        )

        # Floating action tool button
        self.addExampleCard(
            self.tr('Floating action tool button'),
            self.createToolFAB(),
            'https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/button/demo.py'
        )

        # Filled push button
        self.addExampleCard(
            self.tr('Filled push button'),
            FilledPushButton(self.tr('Accent style button')),
            'https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/button/demo.py'
        )

        # Filled tool button
        self.addExampleCard(
            self.tr('Filled tool button'),
            FilledToolButton(FluentIcon.BASKETBALL),
            'https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/button/demo.py'
        )

        # outlined push button
        self.addExampleCard(
            self.tr('Outlined push button'),
            OutlinedPushButton(self.tr('Outlined push button')),
            'https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/button/demo.py'
        )

        # outlined button
        button = OutlinedToolButton(':/gallery/images/kunkun.png')
        button.setIconSize(QSize(30, 30))
        button.setFixedSize(50, 50)
        self.addExampleCard(
            self.tr('Outlined tool button'),
            button,
            'https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/button/demo.py'
        )

        # text push button
        self.addExampleCard(
            self.tr('Tonal push button'),
            TextPushButton(self.tr('Text push button')),
            'https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/button/demo.py'
        )

        # tonal push button
        self.addExampleCard(
            self.tr('Tonal push button'),
            TonalPushButton(self.tr('Tonal push button')),
            'https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/button/demo.py'
        )

        # tonal tool button
        self.addExampleCard(
            self.tr('Tonal tool button'),
            TonalToolButton(FluentIcon.GITHUB),
            'https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/button/demo.py'
        )

        # transparent tool button
        self.addExampleCard(
            self.tr('Transparent tool button'),
            TransparentToolButton(FluentIcon.BOOK_SHELF, self),
            'https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/button/demo.py'
        )

        # 2-state check box
        self.addExampleCard(
            self.tr('Two-state CheckBox'),
            CheckBox(self.tr('Two-state CheckBox')),
            'https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/check_box/demo.py'
        )

        # 3-state check box
        checkBox = CheckBox(self.tr('Three-state CheckBox'))
        checkBox.setTristate(True)
        self.addExampleCard(
            self.tr('Three-state CheckBox'),
            checkBox,
            'https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/check_box/demo.py'
        )

        # combo box
        self.addExampleCard(
            self.tr('A combo box with items'),
            self.createComboBox(ComboBox),
            'https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/combo_box/demo.py'
        )

        # editable combo box
        self.addExampleCard(
            self.tr('An editable combo box'),
            self.createEditableComboBox(ComboBox),
            'https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/combo_box/demo.py'
        )

        # filled combo box
        self.addExampleCard(
            self.tr('A filled combo box with items'),
            self.createComboBox(FilledComboBox),
            'https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/combo_box/demo.py'
        )

        # editable filled combo box
        self.addExampleCard(
            self.tr('A editable filled combo box'),
            self.createEditableComboBox(FilledComboBox),
            'https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/combo_box/demo.py'
        )

        # radio button
        radioWidget = QWidget()
        radioLayout = QVBoxLayout(radioWidget)
        radioLayout.setContentsMargins(2, 0, 0, 0)
        radioLayout.setSpacing(15)
        radioButton1 = RadioButton(self.tr('Star Platinum'), radioWidget)
        radioButton2 = RadioButton(self.tr('Crazy Diamond'), radioWidget)
        radioButton3 = RadioButton(self.tr('Soft and Wet'), radioWidget)
        buttonGroup = QButtonGroup(radioWidget)
        buttonGroup.addButton(radioButton1)
        buttonGroup.addButton(radioButton2)
        buttonGroup.addButton(radioButton3)
        radioLayout.addWidget(radioButton1)
        radioLayout.addWidget(radioButton2)
        radioLayout.addWidget(radioButton3)
        radioButton1.click()
        self.addExampleCard(
            self.tr('Radio button'),
            radioWidget,
            'https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/radio_button/demo.py'
        )

        # horizontal slider
        slider = Slider(Qt.Horizontal)
        slider.setRange(0, 100)
        slider.setValue(30)
        slider.setMinimumWidth(200)
        self.addExampleCard(
            self.tr('Horizontal slider'),
            slider,
            'https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/slider/demo.py'
        )

        # switch button
        self.switchButton = SwitchButton(self.tr('Off'))
        self.switchButton.checkedChanged.connect(self.onSwitchCheckedChanged)
        self.addExampleCard(
            self.tr('Switch button'),
            self.switchButton,
            'https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/switch_button/demo.py'
        )

        # Filled toggle tool button
        self.addExampleCard(
            self.tr('Filled toggle tool button'),
            FilledToggleToolButton(FluentIcon.GITHUB, self),
            'https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/button/demo.py'
        )

        # Outlined toggle tool button
        self.addExampleCard(
            self.tr('Outlined toggle tool button'),
            OutlinedToggleToolButton(FluentIcon.BRIGHTNESS, self),
            'https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/button/demo.py'
        )

        # Transparent toggle tool button
        self.addExampleCard(
            self.tr('Transparent toggle tool button'),
            TransparentToggleToolButton(FluentIcon.BASKETBALL, self),
            'https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/button/demo.py'
        )

    def createComboBox(self, Combo):
        comboBox = Combo()
        comboBox.setLabel(self.tr('Wife'))
        comboBox.addItems(['shoko 🥰', '西宫硝子 😊', '一级棒卡哇伊的硝子酱 😘'])
        comboBox.setCurrentIndex(0)
        comboBox.setMinimumWidth(230)
        return comboBox

    def createEditableComboBox(self, Combo):
        comboBox = Combo()
        comboBox.setEditable(True)
        comboBox.addItems([
            self.tr('Star Platinum'),
            self.tr('Crazy Diamond'),
            self.tr("Gold Experience"),
            self.tr('Sticky Fingers'),
        ])
        comboBox.setLabel(self.tr('Stand'))
        comboBox.setPlaceholderText(self.tr('Choose your stand'))
        comboBox.setMinimumWidth(230)
        return comboBox

    def onSwitchCheckedChanged(self, isChecked):
        if isChecked:
            self.switchButton.setText(self.tr('On'))
        else:
            self.switchButton.setText(self.tr('Off'))

    def createStandMenu(self, button):
        menu = RoundMenu(parent=self)
        menu.addActions([
            Action(self.tr('Star Platinum'), triggered=lambda b=button: b.setText(self.tr('Star Platinum'))),
            Action(self.tr('Crazy Diamond'), triggered=lambda b=button: b.setText(self.tr('Crazy Diamond'))),
            Action(self.tr("Gold Experience"), triggered=lambda b=button: b.setText(self.tr("Gold Experience"))),
            Action(self.tr('Sticky Fingers'), triggered=lambda b=button: b.setText(self.tr('Sticky Fingers'))),
        ])
        return menu

    def createPushFAB(self):
        w = self.createToolFAB()
        for i in range(w.layout().count()):
            button = w.layout().itemAt(i).widget()  # type: SurfaceFloatingActionButton
            button.setText('FAB')

        return w

    def createToolFAB(self):
        w = QWidget(self)
        layout = QHBoxLayout(w)
        layout.setSpacing(15)
        layout.setContentsMargins(10, 13, 10, 13)
        layout.addWidget(SurfaceFloatingActionButton(FluentIcon.BUS))
        layout.addWidget(PrimaryFloatingActionButton(FluentIcon.TRAIN))
        layout.addWidget(SecondaryFloatingActionButton(FluentIcon.CAR))
        layout.addWidget(TertiaryFloatingActionButton(FluentIcon.SHOPPING_CART))
        return w