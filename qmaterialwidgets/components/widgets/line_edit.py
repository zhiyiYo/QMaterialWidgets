# coding: utf-8
from enum import Enum
from typing import List, Union
from PyQt5.QtCore import (QSize, Qt, QRectF, pyqtSignal, QPoint, QTimer, QEvent,
                            QAbstractItemModel, QPropertyAnimation, QEasingCurve, pyqtProperty,
                            QParallelAnimationGroup)
from PyQt5.QtGui import QPainter, QPainterPath, QIcon, QColor, QPen
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLineEdit, QToolButton, QTextEdit,
                               QPlainTextEdit, QCompleter, QLabel, QWidget, QAction)


from ...common.style_sheet import MaterialStyleSheet, themeColor, palette, Theme, qconfig
from ...common.icon import isDarkTheme, MaterialIconBase, drawIcon, Action
from ...common.icon import FluentIcon as FIF
from ...common.font import setFont
from ...common.color import mixColor
from ...common.animation import BackgroundAnimationWidget
from .button import TransparentToggleToolButton
from .menu import LineEditMenu, TextEditMenu, RoundMenu, MenuAnimationType, IndicatorMenuItemDelegate
from .scroll_bar import SmoothScrollDelegate
from .icon_widget import IconWidget


class LineEditButton(TransparentToggleToolButton):
    """ Line edit button """

    def _postInit(self):
        self.action = None
        self.setFixedSize(32, 32)
        self.setIconSize(QSize(20, 20))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName('lineEditButton')

    def setAction(self, action: QAction):
        self.action = action
        self.clicked.connect(action.trigger)
        action.toggled.connect(self._onActionToggled)
        action.changed.connect(self._onActionChanged)

    def _onActionChanged(self):
        self.setIcon(self.action.icon())
        self.setText(self.action.text())
        self.setToolTip(self.action.toolTip())

    def _onActionToggled(self, isChecked: bool):
        self.setCheckable(True)
        self.setChecked(isChecked)


class LineEditIcon(MaterialIconBase, Enum):
    """ Line edit icon """

    ADD = "Add"
    MINUS = "Minus"
    CLEAR = "Clear"
    ERROR = "Error"
    SEARCH = "Search"
    CALENDAR = "Calendar"
    SCHEDULE = "Schedule"
    ARROW_DROP_DOWN = "ArrowDropDown"

    def path(self, theme=Theme.AUTO) -> str:
        return f":/qmaterialwidgets/images/line_edit/{self.value}.svg"

    def render(self, painter, rect, theme=Theme.AUTO, indexes=None, **attributes):
        color = palette.error if self == LineEditIcon.ERROR else palette.onSurfaceVariant
        super().render(painter, rect, theme, indexes, fill=color.name())



class LineEditBase(BackgroundAnimationWidget, QLineEdit):
    """ Line edit """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._isClearButtonEnabled = False
        self._completer = None  # type: QCompleter
        self._completerMenu = None  # type: CompleterMenu
        self._isError = False

        self.hBoxLayout = QHBoxLayout(self)
        self.clearButton = LineEditButton(LineEditIcon.CLEAR, self)
        self.errorIcon = IconWidget(LineEditIcon.ERROR, self)
        self.labelLabel = LineEditLabel(self)
        self.leadingButton = None
        self.trailingButton = None

        self.__initWidgets()

    def __initWidgets(self):
        self.errorIcon.hide()
        self.clearButton.hide()
        self.errorIcon.setFixedSize(22, 22)

        self.hBoxLayout.setSpacing(3)
        self.hBoxLayout.setContentsMargins(8, 4, 8, 4)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.clearButton, 0, Qt.AlignmentFlag.AlignRight)

        self.clearButton.clicked.connect(self.clear)
        self.textChanged.connect(self.__onTextChanged)
        self.textEdited.connect(self.__onTextEdited)

        MaterialStyleSheet.LINE_EDIT.apply(self)

        self.setTextMargins(13, 0, 12, 0)
        self.setClearButtonEnabled(True)
        self.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)
        self.setFixedHeight(40)
        setFont(self)

        self.setLabel('')
        self.labelLabel.move(14, (self.height()-24)//2)

    def setClearButtonEnabled(self, enable: bool):
        self._isClearButtonEnabled = enable
        m = self.textMargins()
        r = 12+48*enable if self.trailingButton else 12+36*enable
        self.setTextMargins(m.left(), m.top(), r, m.bottom())

    def isClearButtonEnabled(self) -> bool:
        return self._isClearButtonEnabled

    def setCompleter(self, completer: QCompleter):
        self._completer = completer

    def completer(self):
        return self._completer

    def setError(self, isError: bool):
        self._isError = isError
        self.labelLabel.setError(isError)
        self.errorIcon.setVisible(isError)
        self.update()

        if isError:
            self.clearButton.hide()

    def isError(self):
        return self._isError

    def setLabel(self, label: str):
        self.labelLabel.setText(label)
        self.labelLabel.adjustSize()
        self.labelLabel.setVisible(bool(label))

        m = self.textMargins()

        if label:
            self.setFixedHeight(56)
            self.setTextMargins(m.left(), 16, m.right(), m.bottom())
        else:
            self.setFixedHeight(40)
            self.setTextMargins(m.left(), 0, m.right(), m.bottom())

        if not self.labelLabel.isUp:
            self.labelLabel.move(self.labelLabel.x(), (self.height()-24)//2)

        if not self.leadingButton:
            x = self.labelLabel.x()
        else:
            x = self.labelLabel.upPos.x()

        self.labelLabel.setUpDownPos(
            QPoint(x, 6),
            QPoint(self.labelLabel.x(), self._labelDownY())
        )

    def getLabel(self):
        return self.labelLabel.text()

    def _labelDownY(self):
        return self.height()//2 - 11

    def focusOutEvent(self, e):
        super().focusOutEvent(e)
        self.clearButton.hide()

        if not (self.text() or self.placeholderText()):
            self.labelLabel.down()

    def focusInEvent(self, e):
        super().focusInEvent(e)

        if self.isClearButtonEnabled() and not self.isError():
            self.clearButton.setVisible(bool(self.text()))

        if not (self.text() or self.placeholderText()):
            self.labelLabel.up()

    def __onTextChanged(self, text):
        """ text changed slot """
        if self.isClearButtonEnabled() and not self.isError():
            self.clearButton.setVisible(bool(text) and self.hasFocus())

        if self.text() and not self.labelLabel.isUp:
            self.labelLabel.up()

    def __onTextEdited(self, text):
        if not self.completer():
            return

        if self.text():
            QTimer.singleShot(50, self._showCompleterMenu)
        elif self._completerMenu:
            self._completerMenu.close()

    def _showCompleterMenu(self):
        if not self.completer() or not self.text():
            return

        # create menu
        if not self._completerMenu:
            self._completerMenu = CompleterMenu(self)

        # add menu items
        self.completer().setCompletionPrefix(self.text())
        changed = self._completerMenu.setCompletion(
            self.completer().completionModel())

        # show menu
        if changed:
            self._completerMenu.popup()

    def setLeadingAction(self, action: QAction) -> LineEditButton:
        """ set leading action """
        self.labelLabel.move(48, self.labelLabel.y())
        self.labelLabel.setUpDownPos(QPoint(48, 6), QPoint(48, self.height()//2-12))

        m = self.textMargins()
        self.setTextMargins(46, m.top(), m.right(), m.bottom())

        self.leadingButton = LineEditButton(action.icon(), self)
        self.leadingButton.setAction(action)
        self.hBoxLayout.insertWidget(0, self.leadingButton, 0, Qt.AlignmentFlag.AlignLeft)
        return self.leadingButton

    def setTrailingAction(self, action: QAction) -> LineEditButton:
        m = self.textMargins()
        self.setTextMargins(m.left(), m.top(), m.right()+36, m.bottom())

        self.trailingButton = LineEditButton(action.icon(), self)
        self.trailingButton.setAction(action)
        self.hBoxLayout.addWidget(self.trailingButton, 0, Qt.AlignmentFlag.AlignRight)

        return self.trailingButton

    def setPlaceholderText(self, text: str) -> None:
        super().setPlaceholderText(text)
        self.labelLabel.up()

    def contextMenuEvent(self, e):
        menu = LineEditMenu(self)
        menu.exec_(e.globalPos())

    def resizeEvent(self, e):
        self.errorIcon.move(self.width() - 36, self.height()//2 - 11)

    label = pyqtProperty(str, getLabel, setLabel)


class LineEditLabel(QLabel):
    """ Line edit label """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.isUp = False
        self.isError = False
        self._color = palette.onSurfaceVariant
        self.upPos = QPoint(0, 0)
        self.downPos = QPoint(0, 0)

        self.posAni = QPropertyAnimation(self, b'pos', self)
        self.fontSizeAni = QPropertyAnimation(self, b'fontSize', self)
        self.colorAni = QPropertyAnimation(self, b'color', self)

        self.labelAniGroup = QParallelAnimationGroup(self)

        self.posAni.setDuration(150)
        self.colorAni.setDuration(150)
        self.fontSizeAni.setDuration(150)
        self.labelAniGroup.addAnimation(self.posAni)
        self.labelAniGroup.addAnimation(self.colorAni)
        self.labelAniGroup.addAnimation(self.fontSizeAni)
        self.labelAniGroup.finished.connect(self._onAniFinished)

        qconfig.themeChanged.connect(self._updateColor)

        MaterialStyleSheet.LINE_EDIT.apply(self)
        self.installEventFilter(self)
        setFont(self, 16)

    def eventFilter(self, obj, e):
        if obj is self:
            if e.type() == QEvent.Type.EnabledChange:
                self._updateColor()

        return super().eventFilter(obj, e)

    def _updateColor(self):
        self.setError(self.isError)

    @pyqtProperty(int)
    def fontSize(self):
        return self.font().pixelSize()

    @fontSize.setter
    def fontSize(self, size: int):
        font = self.font()
        font.setPixelSize(size)
        self.setFont(font)

    @pyqtProperty(QColor)
    def color(self):
        return self._color

    @color.setter
    def color(self, color: QColor):
        self._color = color
        self.update()

    def up(self):
        if self.isUp:
            return

        self.labelAniGroup.stop()
        self.posAni.setEndValue(self.upPos)
        self.colorAni.setEndValue(palette.error if self.isError else themeColor())
        self.fontSizeAni.setEndValue(12)
        self.labelAniGroup.start()

    def down(self):
        if not self.isUp:
            return

        self.labelAniGroup.stop()
        self.posAni.setEndValue(self.downPos)
        self.colorAni.setEndValue(palette.error if self.isError else palette.onSurfaceVariant)
        self.fontSizeAni.setEndValue(16)
        self.labelAniGroup.start()

    def isMoving(self):
        return self.labelAniGroup.state() == QPropertyAnimation.State.Running

    def setUpDownPos(self, up: QPoint, down: QPoint):
        self.upPos = up
        self.downPos = down

    def setError(self, isError: bool):
        self.isError = isError

        if isError:
            color = palette.error
        elif not self.isEnabled():
            color = QColor(255, 255, 255, 110) if isDarkTheme() else QColor(0, 0, 0, 110)
        elif self.isUp:
            color = themeColor()
        else:
            color = palette.onSurfaceVariant

        self.colorAni.stop()
        self.colorAni.setEndValue(color)
        self.color = color

    def _onAniFinished(self):
        self.isUp = not self.isUp

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.TextAntialiasing | QPainter.Antialiasing)
        painter.setPen(self.color)
        painter.drawText(self.rect(), Qt.AlignLeft, self.text())


class FilledLineEdit(LineEditBase):
    """ Filled line edit """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._bottomBorderSize = 0
        self.bottomBorderAni = QPropertyAnimation(self, b'bottomBorderSize', self)

        self.bottomBorderAni.setStartValue(0)
        self.bottomBorderAni.setDuration(310)
        self.bottomBorderAni.setEasingCurve(QEasingCurve.Type.OutQuad)

    @pyqtProperty(float)
    def bottomBorderSize(self):
        return self._bottomBorderSize

    @bottomBorderSize.setter
    def bottomBorderSize(self, size: float):
        self._bottomBorderSize = size
        self.update()

    def _normalBackgroundColor(self):
        return palette.surfaceContainerHighest

    def _hoverBackgroundColor(self):
        return mixColor(palette.onSurface, self._normalBackgroundColor(), 0.08)

    def _pressedBackgroundColor(self):
        return self._normalBackgroundColor()

    def _disabledBackgroundColor(self):
        return QColor(0, 0, 0, 10)

    def _focusInBackgroundColor(self):
        return self._normalBackgroundColor()

    def focusInEvent(self, e):
        super().focusInEvent(e)
        self.bottomBorderAni.stop()
        self.bottomBorderAni.setEndValue(1)
        self.bottomBorderAni.start()

    def focusOutEvent(self, e):
        super().focusOutEvent(e)
        self.bottomBorderAni.stop()
        self.bottomBorderAni.setEndValue(0)
        self.bottomBorderAni.start()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        path.addRoundedRect(QRectF(self.rect()), 5, 5)
        path.addRect(0, self.height()-6, 6, 6)
        path.addRect(self.width()-6, self.height()-6, 6, 6)
        painter.fillPath(path.simplified(), self.backgroundColor)

        painter.end()

        super().paintEvent(e)
        painter.begin(self)

        if not self.isEnabled() and not self.isError():
            painter.setOpacity(0.32)

        if self.isError():
            pen = QPen(palette.error, 2 if self.hasFocus() else 1)
        else:
            pen = QPen(palette.onSurfaceVariant, 1)

        h = self.height()
        painter.setPen(pen)
        painter.drawLine(0, h-pen.width(), self.width(), h-pen.width())

        if self.bottomBorderSize == 0 or self.isError():
            return

        w = self.width() / 2
        x1, x2 = int(w * (1 - self.bottomBorderSize)), int(w * (1 + self.bottomBorderSize))
        painter.setPen(QPen(themeColor(), 2))
        painter.drawLine(x1, h-2, x2, h-2)



class CompleterMenu(RoundMenu):
    """ Completer menu """

    def __init__(self, lineEdit: LineEditBase):
        super().__init__()
        self.items = []
        self.lineEdit = lineEdit

        self.view.setObjectName('completerListWidget')
        self.view.setItemDelegate(IndicatorMenuItemDelegate())
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.installEventFilter(self)
        self.setItemHeight(33)

    def setCompletion(self, model: QAbstractItemModel):
        """ set the completion model """
        items = []
        for i in range(model.rowCount()):
            for j in range(model.columnCount()):
                items.append(model.data(model.index(i, j)))

        if self.items == items and self.isVisible():
            return False

        self.clear()
        self.items = items

        # add items
        for i in items:
            self.addAction(
                QAction(i, triggered=lambda c, x=i: self.lineEdit.setText(x)))

        return True

    def eventFilter(self, obj, e: QEvent):
        if e.type() != QEvent.KeyPress:
            return super().eventFilter(obj, e)

        # redirect input to line edit
        self.lineEdit.event(e)
        self.view.event(e)

        if e.key() == Qt.Key_Escape:
            self.close()
        if e.key() in [Qt.Key_Enter, Qt.Key_Return] and self.view.currentRow() >= 0:
            self.lineEdit.setText(self.view.currentItem().text())
            self.close()

        return super().eventFilter(obj, e)

    def popup(self):
        """ show menu """
        if not self.items:
            return self.close()

        # adjust menu size
        p = self.lineEdit
        if self.view.width() < p.width():
            self.view.setMinimumWidth(p.width())
            self.adjustSize()

        # show menu
        x = -self.width()//2 + self.layout().contentsMargins().left() + p.width()//2
        y = p.height() - self.layout().contentsMargins().top() + 5
        pos = p.mapToGlobal(QPoint(x, y))

        aniType = MenuAnimationType.FADE_IN_DROP_DOWN
        self.view.adjustSize(pos, aniType)

        if self.view.height() < 100 and self.view.itemsHeight() > self.view.height():
            aniType = MenuAnimationType.FADE_IN_PULL_UP
            pos = p.mapToGlobal(QPoint(x, 0))
            self.view.adjustSize(pos, aniType)

        # update border style
        self.view.setProperty('dropDown', aniType ==
                              MenuAnimationType.FADE_IN_DROP_DOWN)
        self.view.setStyle(QApplication.style())

        self.adjustSize()
        self.exec(pos, aniType=aniType)

        # remove the focus of menu
        self.view.setFocusPolicy(Qt.NoFocus)
        self.setFocusPolicy(Qt.NoFocus)
        p.setFocus()


class OutlinedEditBase:
    """ Outlined edit base class """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._borderColor = palette.outline
        self.borderColorAni = QPropertyAnimation(self, b'borderColor', self)
        self.borderColorAni.setDuration(200)

    @pyqtProperty(QColor)
    def borderColor(self):
        return self._borderColor

    @borderColor.setter
    def borderColor(self, color: QColor):
        self._borderColor = color
        self.update()

    def setError(self, isError: bool):
        super().setError(isError)

        if isError:
            self.borderColor = palette.error
        else:
            self.borderColor = themeColor() if self.hasFocus() else palette.outline

    def _updateBorderColor(self):
        self.setError(self.isError())

    def focusInEvent(self, e):
        super().focusInEvent(e)
        self.highlightBorder()

    def highlightBorder(self):
        self.borderColorAni.stop()
        self.borderColorAni.setEndValue(palette.error if self.isError() else themeColor())
        self.borderColorAni.start()

    def focusOutEvent(self, e):
        super().focusOutEvent(e)
        self.resetBorder()

    def resetBorder(self):
        self.borderColorAni.stop()
        self.borderColorAni.setEndValue(palette.error if self.isError() else palette.outline)
        self.borderColorAni.start()

    def paintEvent(self, e):
        super().paintEvent(e)

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        painter.setPen(self.borderColor)

        if not self.isEnabled():
            painter.setOpacity(0.32)

        r, d, w, h = 5, 10, self.width(), self.height()
        pt = 12 if self.label else 0
        if not self.label or not self.labelLabel.isUp:
            return painter.drawRoundedRect(self.rect().adjusted(1, pt+1, -1, -1), r, r)

        # draw outline
        pw = 2 if self.hasFocus() else 1
        painter.setPen(QPen(self.borderColor, pw))
        path = QPainterPath()

        # top right line
        lw = self.labelLabel.fontMetrics().boundingRect(self.label).width()
        path.moveTo(21 + lw, pw+pt)
        path.lineTo(w - r - pw, pw+pt)

        # top right arc
        path.arcTo(w - d - 1, pw + pt, d, d, 90, -90)

        # right line
        y = pw - 1 if self.hasFocus() else pw
        path.lineTo(w - 1, h - r - y)

        # bottom right arc
        path.arcTo(w - d - 1, h - d - y, d, d, 0, -90)

        # bottom line
        path.lineTo(r + pw, h - y)

        # bottom left arc
        path.arcTo(pw, h - d - y, d, d, -90, -90)

        # left line
        path.lineTo(pw, r + pt + pw)

        # top left arc
        path.arcTo(pw, pw + pt, d, d, -180, -90)

        # top left line
        path.lineTo(12, pw+pt)

        painter.drawPath(path)


class LineEdit(OutlinedEditBase, LineEditBase):
    """ Line edit """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.labelLabel.move(16, (self.height()-24)//2)
        qconfig.themeChanged.connect(self._updateBorderColor)
        self.setLabel('')

    def setLabel(self, label: str):
        super().setLabel(label)
        m = self.textMargins()

        if label:
            self.setFixedHeight(68)
            self.setTextMargins(m.left(), 14, m.right(), m.bottom())
            self.hBoxLayout.setContentsMargins(8, 16, 8, 4)
        else:
            self.setFixedHeight(40)
            self.setTextMargins(m.left(), 0, m.right(), m.bottom())
            self.hBoxLayout.setContentsMargins(8, 4, 8, 4)

        if not self.labelLabel.isUp:
            self.labelLabel.move(self.labelLabel.x(), self._labelDownY())

        self.labelLabel.downPos.setY(self._labelDownY())

    def setLeadingAction(self, action: QAction) -> LineEditButton:
        """ set leading action """
        button = super().setLeadingAction(action)

        if self.labelLabel.isUp:
            self.labelLabel.move(16, self.labelLabel.y())

        self.labelLabel.setUpDownPos(QPoint(16, 6), QPoint(48, self._labelDownY()))
        return button

    def _labelDownY(self):
        return self.height()//2-6

    def resizeEvent(self, e):
        dy = 5 if self.label else 11
        self.errorIcon.move(self.width() - 36, self.height()//2 - dy)


class SearchLineEditBase:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.searchButton = self.setLeadingAction(Action(LineEditIcon.SEARCH, 'Search'))
        self.searchButton.clicked.connect(self.search)
        self.clearButton.clicked.connect(self.clearSignal)
        self.setClearButtonEnabled(True)

    def search(self):
        """ emit search signal """
        text = self.text().strip()
        if text:
            self.searchSignal.emit(text)
        else:
            self.clearSignal.emit()


class FilledSearchLineEdit(SearchLineEditBase, FilledLineEdit):
    """ Filled search line edit """

    searchSignal = pyqtSignal(str)
    clearSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)



class SearchLineEdit(SearchLineEditBase, LineEdit):
    """ Search line edit """

    searchSignal = pyqtSignal(str)
    clearSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)


class TextEditBase(QTextEdit):
    """ Text edit base class """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._isError = False
        self.scrollDelegate = SmoothScrollDelegate(self)
        self.labelLabel = LineEditLabel(self)

        MaterialStyleSheet.LINE_EDIT.apply(self)
        self.textChanged.connect(self.__onTextChanged)

        setFont(self)
        self.labelLabel.move(13, 15)
        self.setLabel('')

    def focusOutEvent(self, e):
        super().focusOutEvent(e)
        if not (self.toPlainText() or self.placeholderText()):
            self.labelLabel.down()

    def focusInEvent(self, e):
        super().focusInEvent(e)
        if not (self.toPlainText() or self.placeholderText()):
            self.labelLabel.up()

    def __onTextChanged(self):
        """ text changed slot """
        if self.toPlainText() and not self.labelLabel.isUp:
            self.labelLabel.up()

    def contextMenuEvent(self, e):
        menu = TextEditMenu(self)
        menu.exec_(e.globalPos())

    def setError(self, isError: bool):
        self._isError = isError
        self.labelLabel.setError(isError)
        self.setProperty('isError', isError)
        self.setStyle(QApplication.style())

    def isError(self):
        return self._isError

    def setLabel(self, label: str):
        self.labelLabel.setText(label)
        self.labelLabel.adjustSize()
        self.labelLabel.setVisible(bool(label))

        self.setProperty('hasLabel', bool(label))
        self.setStyle(QApplication.style())

        if not self.labelLabel.isUp:
            self.labelLabel.move(self.labelLabel.x(), 6)

        self.labelLabel.setUpDownPos(
            QPoint(13, 6),
            QPoint(13, 15)
        )

    def getLabel(self):
        return self.labelLabel.text()

    label = pyqtProperty(str, getLabel, setLabel)


class FilledTextEdit(TextEditBase):
    """ Text edit """

    def __init__(self, parent=None):
        super().__init__(parent=parent)


class OutlinedLayer(OutlinedEditBase, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.labelLabel = self.parent().labelLabel

    def hasFocus(self) -> bool:
        return self.parent().hasFocus()

    @property
    def label(self):
        return self.parent().label

    def isError(self):
        return self.parent().isError()


class TextEdit(TextEditBase):
    """ Text edit """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.outlinedLayer = OutlinedLayer(self)
        self.labelLabel.move(15, 25)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.outlinedLayer.resize(self.size())

    def focusInEvent(self, e):
        super().focusInEvent(e)
        self.outlinedLayer.highlightBorder()

    def focusOutEvent(self, e):
        super().focusOutEvent(e)
        self.outlinedLayer.resetBorder()

    def setLabel(self, label: str):
        super().setLabel(label)

        if not self.labelLabel.isUp:
            self.labelLabel.move(15, 25)

        self.labelLabel.setUpDownPos(
            QPoint(15, 6),
            QPoint(15, 25)
        )
