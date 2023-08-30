# coding:utf-8
from typing import List, Union

from PyQt5.QtCore import Qt, QModelIndex, QItemSelectionModel, pyqtProperty, QRectF
from PyQt5.QtGui import QPainterPath
from PyQt5.QtWidgets import QListView, QListWidgetItem, QListView, QListWidget, QStyleOptionViewItem, QWidget

from .scroll_bar import SmoothScrollDelegate
from .table_view import TableItemDelegate
from .ripple import RippleOverlayWidget, RippleAnimation
from ...common.style_sheet import MaterialStyleSheet, themeColor, isDarkTheme
from ...common.font import getFont


class ListItemDelegate(TableItemDelegate):
    """ List item delegate """

    def __init__(self, parent: QListView):
        super().__init__(parent)

    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex):
        super().initStyleOption(option, index)
        option.font = index.data(Qt.FontRole) or getFont(14)


class ListBase:
    """ List base class """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.delegate = ListItemDelegate(self)
        self.scrollDelegate = SmoothScrollDelegate(self)

        self.itemHeight = 46
        self.ripple = RippleOverlayWidget(self)
        self._isSelectRightClickedRow = False

        MaterialStyleSheet.LIST_VIEW.apply(self)
        self.setItemDelegate(self.delegate)
        self.setMouseTracking(True)

        self.entered.connect(lambda i: self._setHoverRow(i.row()))
        self.pressed.connect(lambda i: self._setPressedRow(i.row()))

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
        QListView.leaveEvent(self, e)
        self._setHoverRow(-1)

    def resizeEvent(self, e):
        QListView.resizeEvent(self, e)
        self.viewport().update()

    def keyPressEvent(self, e):
        QListView.keyPressEvent(self, e)
        self.updateSelectedRows()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton or self._isSelectRightClickedRow:
            QListView.mousePressEvent(self, e)
            return self._updateRipple(e.pos())

        index = self.indexAt(e.pos())
        if index.isValid():
            self._setPressedRow(index.row())

        QWidget.mousePressEvent(self, e)

    def mouseReleaseEvent(self, e):
        QListView.mouseReleaseEvent(self, e)
        self.updateSelectedRows()

        if self.indexAt(e.pos()).row() < 0 or e.button() == Qt.RightButton:
            self._setPressedRow(-1)

    def setItemDelegate(self, delegate: ListItemDelegate):
        self.delegate = delegate
        super().setItemDelegate(delegate)

    def clearSelection(self):
        QListView.clearSelection(self)
        self.updateSelectedRows()

    def setCurrentIndex(self, index: QModelIndex):
        QListView.setCurrentIndex(self, index)
        self.updateSelectedRows()

    def updateSelectedRows(self):
        self._setSelectedRows(self.selectedIndexes())

    def _updateRipple(self, pos):
        if not self.currentItem():
            return

        path = QPainterPath()
        itemRect = self.visualItemRect(self.currentItem())
        path.addRect(QRectF(0, itemRect.y(), self.width(), self.itemHeight))
        self.ripple.setClipPath(path)

        ripple = RippleAnimation(pos, self.ripple, self)
        ripple.setColor(Qt.white if isDarkTheme() else Qt.black)
        radius = max(pos.x(), self.width() - pos.x())
        ripple.setRadiusEndValue(radius)
        ripple.setOpacityStartValue(0.15)
        ripple.setRadiusDuration(1000)
        ripple.setOpacityDuration(1000)
        self.ripple.addRipple(ripple)


class ListWidget(ListBase, QListWidget):
    """ List widget """

    def __init__(self, parent=None):
        super().__init__(parent)

    def setCurrentItem(self, item: QListWidgetItem, command: Union[QItemSelectionModel.SelectionFlag, QItemSelectionModel.SelectionFlags] = None):
        self.setCurrentRow(self.row(item), command)

    def setCurrentRow(self, row: int, command: Union[QItemSelectionModel.SelectionFlag, QItemSelectionModel.SelectionFlags] = None):
        if not command:
            super().setCurrentRow(row)
        else:
            super().setCurrentRow(row, command)

        self.updateSelectedRows()

    def isSelectRightClickedRow(self):
        return self._isSelectRightClickedRow

    def setSelectRightClickedRow(self, isSelect: bool):
        self._isSelectRightClickedRow = isSelect

    selectRightClickedRow = pyqtProperty(bool, isSelectRightClickedRow, setSelectRightClickedRow)


class ListView(ListBase, QListView):
    """ List view """

    def __init__(self, parent=None):
        super().__init__(parent)

    def isSelectRightClickedRow(self):
        return self._isSelectRightClickedRow

    def setSelectRightClickedRow(self, isSelect: bool):
        self._isSelectRightClickedRow = isSelect

    selectRightClickedRow = pyqtProperty(bool, isSelectRightClickedRow, setSelectRightClickedRow)