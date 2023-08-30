# coding:utf-8
from PySide6.QtCore import Qt

from qmaterialwidgets import (TextPushButton, MessageBox, TeachingTip, TeachingTipTailPosition,
                            InfoBarIcon, Flyout, FlyoutView, TeachingTipView, FlyoutAnimationType,
                            FilledPushButton)
from ..common.translator import Translator
from .gallery_interface import GalleryInterface


class DialogInterface(GalleryInterface):
    """ Dialog interface """

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.dialogs,
            subtitle='qmaterialwidgets.components.dialog_box',
            parent=parent
        )
        self.setObjectName('dialogInterface')

        button = TextPushButton(self.tr('Show message box'))
        button.clicked.connect(self.showMessageDialog)
        self.addExampleCard(
            self.tr('A message box with mask'),
            button,
            'https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/message_dialog/demo.py'
        )

        self.simpleFlyoutButton = TextPushButton(self.tr('Show flyout'))
        self.simpleFlyoutButton.clicked.connect(self.showSimpleFlyout)
        self.addExampleCard(
            self.tr('A simple flyout'),
            self.simpleFlyoutButton,
            'https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/flyout/demo.py'
        )

        self.complexFlyoutButton = TextPushButton(self.tr('Show flyout'))
        self.complexFlyoutButton.clicked.connect(self.showComplexFlyout)
        self.addExampleCard(
            self.tr('A flyout with image and button'),
            self.complexFlyoutButton,
            'https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/flyout/demo.py'
        )

        self.teachingButton = TextPushButton(self.tr('Show teaching tip'))
        self.teachingButton.clicked.connect(self.showBottomTeachingTip)
        self.addExampleCard(
            self.tr('A teaching tip'),
            self.teachingButton,
            'https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/teaching_tip/demo.py'
        )

        self.teachingRightButton = TextPushButton(self.tr('Show teaching tip'))
        self.teachingRightButton.clicked.connect(self.showLeftBottomTeachingTip)
        self.addExampleCard(
            self.tr('A teaching tip with image and button'),
            self.teachingRightButton,
            'https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/teaching_tip/demo.py'
        )

    def showMessageDialog(self):
        title = self.tr('This is a message dialog with mask')
        content = self.tr(
            "If the content of the message box is veeeeeeeeeeeeeeeeeeeeeeeeeery long, it will automatically wrap like this.")
        w = MessageBox(title, content, self.window())
        if w.exec():
            print('Yes button is pressed')
        else:
            print('Cancel button is pressed')

    def showBottomTeachingTip(self):
        TeachingTip.create(
            target=self.teachingButton,
            icon=InfoBarIcon.SUCCESS,
            title='Lesson 4',
            content=self.tr("With respect, let's advance towards a new stage of the spin."),
            isClosable=True,
            tailPosition=TeachingTipTailPosition.BOTTOM,
            duration=-1,
            parent=self
        )

    def showLeftBottomTeachingTip(self):
        pos = TeachingTipTailPosition.LEFT_BOTTOM
        view = TeachingTipView(
            icon=None,
            title='Lesson 5',
            content=self.tr("The shortest shortcut is to take a detour."),
            image=":/gallery/images/Gyro.jpg",
            isClosable=True,
            tailPosition=pos,
        )

        button = FilledPushButton('Action')
        button.setFixedWidth(120)
        view.addWidget(button, align=Qt.AlignRight)

        t = TeachingTip.make(view, self.teachingRightButton, 3000, pos, self)
        view.closed.connect(t.close)

    def showSimpleFlyout(self):
        Flyout.create(
            icon=InfoBarIcon.SUCCESS,
            title='Lesson 3',
            content=self.tr('Believe in the spin, just keep believing!'),
            target=self.simpleFlyoutButton,
            parent=self.window()
        )

    def showComplexFlyout(self):
        view = FlyoutView(
            title=self.tr('Julius·Zeppeli'),
            content=self.tr("Where the tennis ball will land when it touches the net, no one can predict. \nIf that moment comes, I hope the 'goddess' exists. \nIn that case, I would accept it no matter which side the ball falls on."),
            image=':/gallery/images/SBR.jpg',
        )

        # add button to view
        button = FilledPushButton('Action')
        button.setFixedWidth(120)
        view.addWidget(button, align=Qt.AlignRight)

        # adjust layout (optional)
        view.widgetLayout.insertSpacing(1, 5)
        view.widgetLayout.insertSpacing(0, 5)
        view.widgetLayout.addSpacing(5)

        # show view
        Flyout.make(view, self.complexFlyoutButton, self.window(), FlyoutAnimationType.SLIDE_RIGHT)
