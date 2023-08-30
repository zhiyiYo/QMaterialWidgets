# coding: utf-8
from typing import List, Optional, Union

from PyQt5.QtCore import Qt, QMargins, QModelIndex, QItemSelectionModel, pyqtProperty, QRectF
from PyQt5.QtGui import QPainter, QColor, QKeyEvent, QPalette, QBrush, QPainterPath
from PyQt5.QtWidgets import (QStyledItemDelegate, QApplication, QStyleOptionViewItem,
                             QTableView, QTableWidget, QWidget, QTableWidgetItem, QHeaderView)

from ...common.font import getFont
from ...common.style_sheet import isDarkTheme, MaterialStyleSheet, themeColor
from .line_edit import LineEdit
from .ripple import RippleOverlayWidget, RippleAnimation
from .scroll_bar import SmoothScrollDelegate


class TableItemDelegate(QStyledItemDelegate):

    def __init__(self, parent: QTableView):
        super().__init__(parent)
        self.hoverRow = -1
        self.pressedRow = -1
        self.selectedRows = set()

    def setHoverRow(self, row: int):
        self.hoverRow = row

    def setPressedRow(self, row: int):
        self.pressedRow = row

    def setSelectedRows(self, indexes: List[QModelIndex]):
        self.selectedRows.clear()
        for index in indexes:
            self.selectedRows.add(index.row())
            if index.row() == self.pressedRow:
                self.pressedRow = -1

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        lineEdit = LineEdit(parent)
        lineEdit.setText(option.text)
        lineEdit.setClearButtonEnabled(True)
        return lineEdit

    def updateEditorGeometry(self, editor: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
        rect = option.rect
        y = rect.y() + (rect.height() - editor.height()) // 2
        x, w = rect.x(), rect.width()
        editor.setGeometry(x, y, w, rect.height())

    def _drawBackground(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        """ draw row background """
        if index.data(Qt.ItemDataRole.BackgroundRole):
            painter.setBrush(index.data(Qt.ItemDataRole.BackgroundRole))
            painter.drawRect(option.rect)

        isHover = self.hoverRow == index.row()
        isPressed = self.pressedRow == index.row()
        isAlternate = index.row() % 2 == 0 and self.parent().alternatingRowColors()
        isDark = isDarkTheme()

        c = 255 if isDark else 0
        alpha = 0

        if index.row() not in self.selectedRows:
            if isPressed:
                alpha = 9 if isDark else 6
            elif isHover:
                alpha = 12
            elif isAlternate:
                alpha = 10
        else:
            if isPressed:
                alpha = 15 if isDark else 9
            elif isHover:
                alpha = 25
            else:
                alpha = 17

        painter.setBrush(QColor(c, c, c, alpha))
        painter.drawRect(option.rect)

    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex):
        super().initStyleOption(option, index)

        # font
        option.font = index.data(Qt.FontRole) or getFont(13)

        # text color
        textColor = Qt.white if isDarkTheme() else Qt.black
        textBrush = index.data(Qt.ForegroundRole)   # type: QBrush
        if textBrush is not None:
            textColor = textBrush.color()

        option.palette.setColor(QPalette.Text, textColor)
        option.palette.setColor(QPalette.HighlightedText, textColor)

    def paint(self, painter, option, index):
        painter.save()
        painter.setPen(Qt.NoPen)
        painter.setRenderHint(QPainter.Antialiasing)

        # set clipping rect of painter to avoid painting outside the borders
        painter.setClipping(True)
        painter.setClipRect(option.rect)

        # draw highlight background
        self._drawBackground(painter, option, index)

        painter.restore()
        super().paint(painter, option, index)


class TableHeader(QHeaderView):
    """ table header """

    def __init__(self, orientation: Qt.Orientation, parent=None):
        super().__init__(orientation, parent)
        self.lightBackgroundColor = QColor(0, 0, 0, 0)
        self.darkBackgroundColor = QColor(0, 0, 0, 0)

    def setCustomBackgroundColor(self, light, dark):
        """ set the custom background color

        Parameters
        ----------
        light, dark: str | Qt.GlobalColor | QColor
            background color in light/dark theme mode
        """
        self.lightBackgroundColor = QColor(light)
        self.darkBackgroundColor = QColor(dark)
        self.viewport().update()

    def paintEvent(self, e):
        painter = QPainter(self.viewport())
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.darkBackgroundColor if isDarkTheme() else self.lightBackgroundColor)
        painter.drawRect(self.rect())
        super().paintEvent(e)


class TableBase:
    """ Table base class """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setHorizontalHeader(TableHeader(Qt.Orientation.Horizontal, self))

        self.delegate = TableItemDelegate(self)
        self.scrollDelagate = SmoothScrollDelegate(self)
        self.ripple = RippleOverlayWidget(self)

        self.itemHeight = 46
        self._isSelectRightClickedRow = False

        # set style sheet
        MaterialStyleSheet.TABLE_VIEW.apply(self)

        self.setShowGrid(False)
        self.setMouseTracking(True)
        self.setAlternatingRowColors(False)
        self.setItemDelegate(self.delegate)
        self.setSelectionBehavior(TableWidget.SelectionBehavior.SelectRows)
        self.removeEventFilter(self.ripple)

        self.entered.connect(lambda i: self._setHoverRow(i.row()))
        self.pressed.connect(lambda i: self._setPressedRow(i.row()))
        self.verticalHeader().sectionClicked.connect(self.selectRow)

    def showEvent(self, e):
        QTableView.showEvent(self, e)
        self.resizeRowsToContents()

    def _setHoverRow(self, row: int):
        """ set hovered row """
        self.delegate.setHoverRow(row)
        self.viewport().update()

    def _setPressedRow(self, row: int):
        """ set pressed row """
        self.delegate.setPressedRow(row)
        self.viewport().update()

    def _setSelectedRows(self, indexes: List[QModelIndex]):
        self.delegate.setSelectedRows(indexes)
        self.viewport().update()

    def leaveEvent(self, e):
        QTableView.leaveEvent(self, e)
        self._setHoverRow(-1)

    def resizeEvent(self, e):
        QTableView.resizeEvent(self, e)
        self.viewport().update()
        self.ripple.resize(self.size())

    def keyPressEvent(self, e: QKeyEvent):
        QTableView.keyPressEvent(self, e)
        self.updateSelectedRows()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton or self._isSelectRightClickedRow:
            QTableView.mousePressEvent(self, e)
            return self._updateRipple(e.pos())

        index = self.indexAt(e.pos())
        if index.isValid():
            self._setPressedRow(index.row())

        QWidget.mousePressEvent(self, e)

    def mouseReleaseEvent(self, e):
        QTableView.mouseReleaseEvent(self, e)
        self.updateSelectedRows()

        if self.indexAt(e.pos()).row() < 0 or e.button() == Qt.RightButton:
            self._setPressedRow(-1)

    def _updateRipple(self, pos):
        if not self.currentItem():
            return

        itemRect = self.visualItemRect(self.currentItem())
        y = itemRect.y()
        if self.horizontalHeader().isVisible():
            y += self.horizontalHeader().height()

        rect = QRectF(0, y, self.width(), self.itemHeight)
        path = QPainterPath()
        path.addRect(rect)
        self.ripple.setClipPath(path)

        ripple = RippleAnimation(pos, self.ripple, self)
        ripple.setColor(Qt.white if isDarkTheme() else Qt.black)
        radius = max(pos.x(), self.width() - pos.x())
        ripple.setRadiusEndValue(radius)

        ripple.setOpacityStartValue(0.15)
        ripple.setRadiusDuration(1200)
        ripple.setOpacityDuration(1200)
        self.ripple.addRipple(ripple)

    def setItemDelegate(self, delegate: TableItemDelegate):
        self.delegate = delegate
        super().setItemDelegate(delegate)

    def setHorizonHeaderBackgroundColor(self, light: QColor, dark: QColor):
        self.horizontalHeader().setCustomBackgroundColor(light, dark)

    def selectAll(self):
        QTableView.selectAll(self)
        self.updateSelectedRows()

    def selectRow(self, row: int):
        QTableView.selectRow(self, row)
        self.updateSelectedRows()

    def clearSelection(self):
        QTableView.clearSelection(self)
        self.updateSelectedRows()

    def setCurrentIndex(self, index: QModelIndex):
        QTableView.setCurrentIndex(self, index)
        self.updateSelectedRows()

    def updateSelectedRows(self):
        self._setSelectedRows(self.selectedIndexes())


class TableWidget(TableBase, QTableWidget):
    """ Table widget """

    def __init__(self, parent=None):
        super().__init__(parent)

    def setCurrentCell(self, row: int, column: int, command: Union[QItemSelectionModel.SelectionFlag, QItemSelectionModel.SelectionFlags] = None):
        self.setCurrentItem(self.item(row, column), command)

    def setCurrentItem(self, item: QTableWidgetItem, command: Union[QItemSelectionModel.SelectionFlag, QItemSelectionModel.SelectionFlags] = None):
        if not command:
            super().setCurrentItem(item)
        else:
            super().setCurrentItem(item, command)

        self.updateSelectedRows()

    def isSelectRightClickedRow(self):
        return self._isSelectRightClickedRow

    def setSelectRightClickedRow(self, isSelect: bool):
        self._isSelectRightClickedRow = isSelect

    selectRightClickedRow = pyqtProperty(bool, isSelectRightClickedRow, setSelectRightClickedRow)



class TableView(TableBase, QTableView):
    """ Table view """

    def __init__(self, parent=None):
        super().__init__(parent)

    def isSelectRightClickedRow(self):
        return self._isSelectRightClickedRow

    def setSelectRightClickedRow(self, isSelect: bool):
        self._isSelectRightClickedRow = isSelect

    selectRightClickedRow = pyqtProperty(bool, isSelectRightClickedRow, setSelectRightClickedRow)