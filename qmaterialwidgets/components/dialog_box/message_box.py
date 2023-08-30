# coding:utf-8
from typing import Union
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QEvent, QSize
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QLabel, QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QDialogButtonBox

from ...common.auto_wrap import TextWrap
from ...common.icon import MaterialIconBase
from ...common.style_sheet import MaterialStyleSheet
from ..widgets.button import TextPushButton, FilledPushButton

from ..widgets.icon_widget import IconWidget
from .mask_dialog_base import MaskDialogBase



class DialogButtonBox(QDialogButtonBox):
    """ Dialog button box """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setOrientation(Qt.Horizontal)
        self.setContentsMargins(24, 6, 24, 20)
        self.layout().setSpacing(10)


class MessageBox(MaskDialogBase):
    """ Dialog box """

    def __init__(self, title: str, content: str, parent=None, icon: Union[MaterialIconBase, QIcon, str] = None):
        super().__init__(parent=parent)
        self.content = content
        self.titleLabel = QLabel(title, self.widget)
        self.contentLabel = QLabel(content, self.widget)
        self.iconWidget = IconWidget(self.widget)

        self.buttonGroup = DialogButtonBox(self.widget)
        self.yesButton = FilledPushButton(self.tr('OK'), self.buttonGroup)
        self.cancelButton = TextPushButton(self.tr('Cancel'), self.buttonGroup)

        self.vBoxLayout = QVBoxLayout(self.widget)
        self.textLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()

        self.setIcon(icon)
        self.__initWidgets()

    def __initWidgets(self):
        self._setQss()
        self.__initLayout()

        self.iconWidget.setFixedSize(24, 24)
        self.yesButton.setAttribute(Qt.WidgetAttribute.WA_LayoutUsesWidgetRect)
        self.cancelButton.setAttribute(Qt.WidgetAttribute.WA_LayoutUsesWidgetRect)
        self.yesButton.setFocus()
        self._adjustText()

        self.buttonGroup.rejected.connect(self.reject)
        self.buttonGroup.accepted.connect(self.accept)

    def __initLayout(self):
        self.vBoxLayout.setSpacing(12)
        self.vBoxLayout.setContentsMargins(0, 24, 0, 0)
        self.vBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignHCenter)
        self.vBoxLayout.addLayout(self.textLayout)
        self.vBoxLayout.addLayout(self.buttonLayout)
        self.vBoxLayout.setSizeConstraint(QVBoxLayout.SetMinimumSize)

        self.textLayout.setSpacing(12)
        self.textLayout.setContentsMargins(24, 0, 24, 0)
        self.textLayout.addWidget(self.titleLabel, 0, Qt.AlignTop)
        self.textLayout.addWidget(self.contentLabel, 0, Qt.AlignTop)

        self.buttonLayout.setSpacing(0)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.addWidget(self.buttonGroup, 0, Qt.AlignRight)
        self.buttonLayout.setAlignment(Qt.AlignRight)
        self.buttonGroup.addButton(self.cancelButton, QDialogButtonBox.RejectRole)
        self.buttonGroup.addButton(self.yesButton, QDialogButtonBox.AcceptRole)

    def eventFilter(self, obj, e: QEvent):
        if obj is self.window():
            if e.type() == QEvent.Resize:
                self._adjustText()

        return super().eventFilter(obj, e)

    def _adjustText(self):
        if self.isWindow():
            if self.parent():
                w = max(self.titleLabel.width(), self.parent().width())
                chars = max(min(w / 9, 140), 30)
            else:
                chars = 100
        else:
            w = max(self.titleLabel.width(), self.window().width())
            chars = max(min(w / 9, 100), 30)

        self.contentLabel.setText(TextWrap.wrap(self.content, chars, False)[0])

    def _setQss(self):
        self.titleLabel.setObjectName("titleLabel")
        self.contentLabel.setObjectName("contentLabel")
        MaterialStyleSheet.MESSAGE_BOX.apply(self)

    def addButton(self, button: QPushButton, role: QDialogButtonBox.ButtonRole):
        """ add button to dialog button box """
        self.buttonGroup.addButton(button, role)

    def setIcon(self, icon: Union[MaterialIconBase, QIcon, str]):
        self.iconWidget.setIcon(icon or QIcon())

        hasIcon = not self.iconWidget.icon.isNull()
        self.iconWidget.setVisible(hasIcon)

        if hasIcon:
            self.titleLabel.setAlignment(Qt.AlignCenter)
        else:
            self.titleLabel.setAlignment(Qt.AlignLeft)

    def setIconSize(self, size: QSize):
        self.iconWidget.setFixedSize(size)
