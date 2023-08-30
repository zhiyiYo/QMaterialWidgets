# coding:utf-8
from typing import List, Union
from math import sin, cos, radians, atan, degrees

from PyQt5.QtCore import Qt, pyqtSignal, QTime, QRectF, QPoint, QRect, pyqtProperty, QRegularExpression
from PyQt5.QtGui import QIntValidator, QPainter, QPen, QPainterPath, QFont, QRegularExpressionValidator
from PyQt5.QtWidgets import (QWidget, QLineEdit, QApplication, QLabel, QHBoxLayout, QVBoxLayout,
                             QPushButton, QFrame)

from ...common.style_sheet import MaterialStyleSheet, themeColor, palette
from ...common.font import setFont
from ...common.icon import Action, MaterialIcon
from ..widgets.button import TextPushButton
from ..widgets.line_edit import LineEdit, LineEditIcon
from ..dialog_box.mask_dialog_base import MaskDialogBase


class TimeLineEdit(QLineEdit):
    """ Time line edit """

    focused = pyqtSignal()
    valueChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__('00', parent)
        self.setSelected(False)
        self.setFixedSize(76, 64)
        self.setAlignment(Qt.AlignCenter)
        self.textEdited.connect(self._onTextEdited)

    def focusInEvent(self, e):
        super().focusInEvent(e)
        self.setSelected(True)
        self.focused.emit()

    def setSelected(self, isSelected: bool):
        self.isSelected = isSelected
        self.setProperty('selected', isSelected)
        self.setStyle(QApplication.style())

    def value(self) -> int:
        return 0 if not self.text() else int(self.text())

    def setValue(self, value: int):
        self.setText(str(value).zfill(2))

    def _onTextEdited(self, text):
        if self.validator().validate(text, 0)[0] == QIntValidator.Acceptable:
            self.valueChanged.emit(self.value())

    def contextMenuEvent(self, e):
        pass

    def paintEvent(self, e):
        super().paintEvent(e)
        if not self.hasFocus():
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setBrush(Qt.NoBrush)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect().adjusted(2, 2, -2, -2)), 8, 8)
        painter.strokePath(path, QPen(themeColor(), 2))


class HourLineEdit(TimeLineEdit):
    """ Hour time line edit """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setValidator(QRegularExpressionValidator(QRegularExpression('^([0][0-9]|[1-9]|1[0-2])$')))


class MinuteLineEdit(TimeLineEdit):
    """ Minute time line edit """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setValidator(QRegularExpressionValidator(QRegularExpression('^([0-5][0-9]|0[0-9]|[1-9])$')))


class PeriodSelector(QWidget):
    """ Period selector """

    periodChanged = pyqtSignal(bool)

    def __init__(self, orientation: Qt.Orientation, parent=None):
        super().__init__(parent)
        self.AMPushButton = QPushButton('AM', self)
        self.PMPushButton = QPushButton('PM', self)
        self.orientation = orientation

        if orientation == Qt.Orientation.Horizontal:
            self.setLayout(QHBoxLayout(self))
            self.AMPushButton.setFixedSize(87, 30)
            self.PMPushButton.setFixedSize(87, 30)
        else:
            self.setLayout(QVBoxLayout(self))
            self.AMPushButton.setFixedSize(42, 33)
            self.PMPushButton.setFixedSize(42, 33)

        self.AMPushButton.setObjectName('AMPushButton')
        self.PMPushButton.setObjectName('PMPushButton')
        self.AMPushButton.setProperty(
            'horizontal', orientation == Qt.Horizontal)
        self.PMPushButton.setProperty(
            'horizontal', orientation == Qt.Horizontal)

        self.setPeriod(True)
        self.layout().setSpacing(1)
        self.layout().setContentsMargins(1, 1, 1, 1)
        self.layout().addWidget(self.AMPushButton)
        self.layout().setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self.PMPushButton)
        self.layout().setSizeConstraint(QHBoxLayout.SizeConstraint.SetFixedSize)
        self.AMPushButton.clicked.connect(self._onButtonClicked)
        self.PMPushButton.clicked.connect(self._onButtonClicked)

    def _onButtonClicked(self):
        isAM = self.sender() == self.AMPushButton
        if isAM == self.isAM:
            return

        self.setPeriod(isAM)
        self.periodChanged.emit(isAM)

    def setPeriod(self, isAM: bool):
        self.isAM = isAM
        self.AMPushButton.setProperty('selected', isAM)
        self.PMPushButton.setProperty('selected', not isAM)
        self.setStyle(QApplication.style())

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.NoBrush)

        if self.orientation == Qt.Orientation.Horizontal:
            self._drawHorizon(painter)
        else:
            self._drawVertical(painter)

        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 8, 8)

    def _drawHorizon(self, painter: QPainter):
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)

        w, h = self.width(), self.height()
        rw, rh = (w-3)/2, h-2

        # draw highlight background
        if self.isAM:
            rect = QRectF(1, 1, rw, rh)
            path.addRoundedRect(rect, 8, 8)
            path.addRect(rw-10, 1, 10, rh)
        else:
            rect = QRectF(rw+1, 1, rw, rh)
            path.addRoundedRect(rect, 8, 8)
            path.addRect(rw+1, 1, 10, rh)

        painter.fillPath(path.simplified(), palette.tertiaryContainer)

        # draw separator
        painter.setPen(palette.outline)
        x = self.AMPushButton.geometry().right() + 1
        painter.drawLine(x, 1, x, self.height() - 1)

    def _drawVertical(self, painter: QPainter):
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)

        w, h = self.width(), self.height()
        rw, rh = w-2, (h-3)/2

        # draw highlight background
        if self.isAM:
            rect = QRectF(1, 1, rw, rh)
            path.addRoundedRect(rect, 8, 8)
            path.addRect(1, rh-9, rw, 10)
        else:
            rect = QRectF(1, rh+1, rw, rh)
            path.addRoundedRect(rect, 8, 8)
            path.addRect(1, rh+1, rw, 10)

        painter.fillPath(path.simplified(), palette.tertiaryContainer)

        # draw separator
        painter.setPen(palette.outline)
        y = self.AMPushButton.geometry().bottom() + 1
        painter.drawLine(1, y, self.width() - 1, y)


class TimeEditWidget(QWidget):
    """ Time edit widget """

    timeChanged = pyqtSignal(QTime)

    def __init__(self, orientation: Qt.Orientation, parent=None):
        super().__init__(parent)
        self.time = QTime.currentTime()
        self.orientation = orientation

        if orientation == Qt.Orientation.Horizontal:
            self.setLayout(QVBoxLayout(self))
        else:
            self.setLayout(QHBoxLayout(self))

        self.hBoxLayout = QHBoxLayout()
        self.hourLineEdit = HourLineEdit(self)
        self.minuteLineEdit = MinuteLineEdit(self)
        self.separatorLabel = QLabel(':', self)
        self.periodSelector = PeriodSelector(orientation, self)

        self.__initWidget()

    def __initWidget(self):
        self.separatorLabel.setObjectName('separatorLabel')
        self.hourLineEdit.setSelected(True)
        self.separatorLabel.setFixedWidth(24)
        self.separatorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__initLayout()

        self.periodSelector.periodChanged.connect(self._onTimeEdited)
        self.minuteLineEdit.valueChanged.connect(self._onTimeEdited)
        self.hourLineEdit.valueChanged.connect(self._onTimeEdited)
        self.hourLineEdit.focused.connect(self._onLineEditFocused)
        self.minuteLineEdit.focused.connect(self._onLineEditFocused)

        MaterialStyleSheet.TIME_PICKER.apply(self)

    def __initLayout(self):
        self.layout().setContentsMargins(0, 0, 0, 0)

        if self.orientation == Qt.Orientation.Vertical:
            self.layout().setSpacing(12)
        else:
            self.layout().setSpacing(16)

        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.layout().setSizeConstraint(QHBoxLayout.SizeConstraint.SetFixedSize)

        self.hBoxLayout.addWidget(self.hourLineEdit)
        self.hBoxLayout.addWidget(self.separatorLabel)
        self.hBoxLayout.addWidget(self.minuteLineEdit)
        self.layout().addLayout(self.hBoxLayout)
        self.layout().addWidget(self.periodSelector)

    def setTime(self, time: QTime):
        self.time = time
        self.minuteLineEdit.setValue(time.minute())

        # convert 24-hour to AM/PM hour
        h = time.hour()
        if 12 <= h < 24:
            self.periodSelector.setPeriod(False)
            h = 12 if h == 12 else h - 12
        else:
            self.periodSelector.setPeriod(True)
            h = 0 if h == 24 else h

        self.hourLineEdit.setValue(h)

    def _onTimeEdited(self):
        time = self.currentTime()
        if time.isValid():
            self.timeChanged.emit(self.currentTime())

    def currentTime(self):
        h, m = self.hourLineEdit.value(), self.minuteLineEdit.value()
        if not (0 <= h <= 12 or 0 <= m <= 59):
            return QTime(-1, -1)

        # convert AM/PM hour to 24-hour
        if self.periodSelector.isAM:
            h = 0 if h == 12 else h
        else:
            h = h if h == 12 else h + 12

        return QTime(h, m)

    def _onLineEditFocused(self):
        if self.sender() is self.hourLineEdit:
            self.minuteLineEdit.setSelected(False)
        else:
            self.hourLineEdit.setSelected(False)


class TimeDial(QWidget):
    """ Time dial """

    valueChanged = pyqtSignal(int)

    def __init__(self, min: int, max: int, labels: List[str], parent=None):
        super().__init__(parent=parent)
        self.min = min
        self.max = max
        self.labels = labels
        self.value = min
        self.setFixedSize(210, 210)
        setFont(self)

    def setValue(self, value):
        if self.value == value:
            return

        self.value = value
        self.update()

    def format(self, value: int):
        return str(value)

    def mousePressEvent(self, e):
        self.setCursor(Qt.CursorShape.SizeAllCursor)
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self._updateValue(e.pos())

    def mouseMoveEvent(self, e):
        self._updateValue(e.pos())

    def _updateValue(self, pos: QPoint):
        value = self._angleToValue(self._posToAngle(pos))
        ov = self.value
        self.setValue(value)

        if ov != self.value:
            self.valueChanged.emit(self.value)

    def _posToAngle(self, pos: QPoint) -> int:
        r = self.width() / 2
        x = pos.x() - r
        y = r - pos.y()
        if abs(y) < 1e-6:
            y = 1e-6 if y >= 0 else -1e-6

        angle = degrees(atan(x / y))
        if x < 0 and y > 0:
            angle += 360
        elif x < 0 or y < 0:
            angle += 180

        return angle

    def _valueToAngle(self, value) -> int:
        raise NotImplementedError

    def _angleToValue(self, angle: float) -> int:
        raise NotImplementedError

    def _labelToAngle(self, label: str) -> int:
        raise NotImplementedError

    def _angleToRect(self, angle: float):
        w, h = self.width(), self.height()
        xc, yc = w / 2, h / 2
        aw, ah = 38, 38
        r = w / 2 - 4 - aw / 2
        x = int(xc + r * sin(radians(angle)))
        y = int(yc - r * cos(radians(angle)))
        return QRect(int(x-aw/2), int(y-ah/2), aw, ah)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.NoPen)

        # draw background
        painter.setBrush(palette.surfaceContainerHighest)
        painter.drawEllipse(self.rect())

        self._drawHandle(painter)
        self._drawLabels(painter)

    def _drawLabels(self, painter):
        painter.setPen(palette.onSurface)
        painter.setFont(self.font())
        for label in self.labels:
            angle = self._labelToAngle(label)
            if self.value != self._angleToValue(angle):
                painter.drawText(self._angleToRect(
                    angle), Qt.AlignCenter, label)

    def _drawHandle(self, painter: QPainter):
        painter.save()
        painter.setPen(Qt.NoPen)
        painter.setBrush(themeColor())

        # draw center dot
        painter.translate(self.rect().center())
        painter.drawEllipse(QPoint(), 3, 3)

        # draw selector track
        r = self.width() // 2
        angle = self._valueToAngle(self.value)
        rect = self._angleToRect(angle).translated(-r, -r)
        painter.setPen(QPen(themeColor(), 2))
        painter.drawLine(QPoint(), rect.center())

        # draw selector container
        painter.setBrush(themeColor())
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(rect)

        # draw dial label
        if self.format(self.value) in self.labels:
            painter.setPen(palette.onPrimary)
            painter.drawText(rect, Qt.AlignCenter, self.format(self.value))
        else:
            painter.setBrush(palette.onPrimary)
            painter.drawEllipse(rect.center(), 3, 3)

        painter.restore()


class HourDial(TimeDial):
    """ Hour dial """

    def __init__(self, parent=None):
        super().__init__(1, 12, ['12', '1', '2', '3', '4',
                                 '5', '6', '7', '8', '9', '10', '11'], parent)

    def _valueToAngle(self, value) -> int:
        return (value % 12) * 30

    def _labelToAngle(self, label: str) -> int:
        return (int(label) % 12) * 30

    def _angleToValue(self, angle: float) -> int:
        value = round(angle / 30)
        return 12 if value == 0 else value


class MinuteDial(TimeDial):
    """ Minute dial """

    def __init__(self, parent=None):
        super().__init__(0, 59, ['00', '05', '10', '15', '20',
                                 '25', '30', '35', '40', '45', '50', '55'], parent)

    def _valueToAngle(self, value) -> int:
        return value * 6

    def _labelToAngle(self, label: str) -> int:
        return int(label) * 6

    def _angleToValue(self, angle: float) -> int:
        return round(angle / 6) % 60

    def format(self, value: int):
        return str(value).zfill(2)


class TimeDialView(QWidget):
    """ Time dial view """

    minuteChanged = pyqtSignal(int)
    hourChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hourDial = HourDial(self)
        self.minuteDial = MinuteDial(self)

        self.hourDial.valueChanged.connect(self.hourChanged)
        self.minuteDial.valueChanged.connect(self.minuteChanged)
        self.setFixedSize(210, 210)
        self.setCurrentDial(True)

    def setCurrentDial(self, isHour: bool):
        self.isHour = isHour
        self.hourDial.setVisible(isHour)
        self.minuteDial.setVisible(not isHour)

    def setTime(self, time: QTime):
        # convert 24-hour to AM/PM hour
        h = time.hour()
        if 12 <= h < 24:
            h = 12 if h == 12 else h - 12
        else:
            h = 12 if h in [24, 0] else h

        self.hourDial.setValue(h)
        self.minuteDial.setValue(time.minute())

    def hour(self):
        return self.hourDial.value

    def minute(self):
        return self.minuteDial.value


class TimePickerView(QFrame):
    """ Time picker view """

    timeChanged = pyqtSignal(QTime)
    rejected = pyqtSignal()
    accepted = pyqtSignal()

    def __init__(self, time: QTime = None, orientation=Qt.Orientation.Horizontal, parent=None):
        super().__init__(parent=parent)
        self.orientation = orientation

        self.selectTimeLabel = QLabel(self.tr('Select time'), self)
        self.timeEdit = TimeEditWidget(orientation, self)
        self.timeDial = TimeDialView(self)

        self.yesButton = TextPushButton(self.tr('OK'), self)
        self.cancelButton = TextPushButton(self.tr('Cancel'), self)

        self.vBoxLayout = QVBoxLayout(self)
        self.buttonLayout = QHBoxLayout()

        if orientation == Qt.Orientation.Horizontal:
            self.timeLayout = QHBoxLayout()
        else:
            self.timeLayout = QVBoxLayout()

        self.originalTime = time
        self.setTime(self.originalTime or QTime.currentTime())
        self.__initWidget()

    def __initWidget(self):
        setFont(self.selectTimeLabel, 14, QFont.Weight.DemiBold)
        self.selectTimeLabel.setObjectName('selectTimeLabel')
        MaterialStyleSheet.TIME_PICKER.apply(self)

        self.timeEdit.timeChanged.connect(self._onTimeEdited)
        self.timeEdit.hourLineEdit.focused.connect(
            lambda: self.timeDial.setCurrentDial(True))
        self.timeEdit.minuteLineEdit.focused.connect(
            lambda: self.timeDial.setCurrentDial(False))

        self.timeDial.minuteChanged.connect(self._onDialMinuteChanged)
        self.timeDial.hourChanged.connect(self._onDialHourChanged)

        self.cancelButton.clicked.connect(self.rejected)
        self.yesButton.clicked.connect(self._onYesButtonClicked)

        self.__initLayout()

    def __initLayout(self):
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.vBoxLayout.addWidget(self.selectTimeLabel)
        self.vBoxLayout.addLayout(self.timeLayout)
        self.vBoxLayout.addLayout(self.buttonLayout)

        self.buttonLayout.setAlignment(Qt.AlignRight)
        self.buttonLayout.addWidget(self.cancelButton, 0, Qt.AlignRight)
        self.buttonLayout.addWidget(self.yesButton, 0, Qt.AlignRight)
        self.buttonLayout.setContentsMargins(0, 16, 20, 16)

        self.timeLayout.setContentsMargins(20, 0, 20, 8)
        self.timeLayout.addWidget(self.timeEdit, 0)
        self.timeLayout.addWidget(self.timeDial, 0, Qt.AlignCenter)

        if self.orientation == Qt.Orientation.Horizontal:
            self.timeLayout.setSpacing(40)
        else:
            self.timeLayout.setSpacing(20)

    def _onDialHourChanged(self, hour: int):
        self.timeEdit.hourLineEdit.setValue(hour)
        self.setTime(self.timeEdit.currentTime())

    def _onDialMinuteChanged(self, minute: int):
        self.setTime(QTime(self.time.hour(), minute))

    def _onTimeEdited(self, time: QTime):
        self.time = time
        self.timeDial.setTime(time)

    def _onYesButtonClicked(self):
        self.accepted.emit()
        if self.time != self.originalTime:
            self.timeChanged.emit(self.time)

    def setTime(self, time: QTime):
        self.time = time
        self.timeEdit.setTime(time)
        self.timeDial.setTime(time)


class TimePickerDialog(MaskDialogBase):
    """ Time picker dialog """

    timeChanged = pyqtSignal(QTime)

    def __init__(self, time: QTime = None, orientation=Qt.Orientation.Horizontal, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self.widget)
        self.picker = TimePickerView(time, orientation, self.widget)

        self.hBoxLayout.addWidget(self.picker)

        self.hBoxLayout.setSizeConstraint(
            QHBoxLayout.SizeConstraint.SetMinimumSize)
        self.picker.timeChanged.connect(self.timeChanged)
        self.picker.accepted.connect(self.accept)
        self.picker.rejected.connect(self.reject)
        MaterialStyleSheet.TIME_PICKER.apply(self)

    def setTime(self, time: QTime):
        self.picker.setTime(time)


class TimePicker(LineEdit):
    """ Time picker """

    timeChanged = pyqtSignal(QTime)

    def __init__(self, parent=None, time: QTime = None, orientation=Qt.Orientation.Horizontal):
        super().__init__(parent)
        self._time = time or QTime()
        self._format = 'h:mm AP'
        self.orientation = orientation

        self.setLabel(self.tr('Time'))
        self.setPlaceholderText(self.tr('Pick a time'))
        self.setReadOnly(True)
        self.setTrailingAction(Action(LineEditIcon.SCHEDULE, 'Time'))
        self.setClearButtonEnabled(False)
        self.setMinimumWidth(200)

        self.trailingButton.clicked.connect(self.showDialog)

    def showDialog(self):
        w = TimePickerDialog(self.time, self.orientation, self.window())
        w.timeChanged.connect(self._onTimeChanged)
        w.exec()

    def setTime(self, time: QTime):
        self._time = time
        self.setText(time.toString(self._format))

    def _onTimeChanged(self, time):
        self.setTime(time)
        self.timeChanged.emit(time)

    def getTime(self):
        return self._time

    def setFormat(self, format: Union[Qt.DateFormat, str]):
        self._format = format
        self.setText(self.time.toString(format))

    def getFormat(self):
        return self._format

    time = pyqtProperty(QTime, getTime, setTime)
    timeFormat = pyqtProperty(Qt.DateFormat, getFormat, setFormat)