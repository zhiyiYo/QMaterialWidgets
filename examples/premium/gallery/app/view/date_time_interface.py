# coding:utf-8
from PySide6.QtCore import Qt
from qmaterialwidgets import TimePicker, CalendarPicker

from .gallery_interface import GalleryInterface
from ..common.translator import Translator


class DateTimeInterface(GalleryInterface):
    """ Date time interface """

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.dateTime,
            subtitle='qmaterialwidgets.components.date_time',
            parent=parent
        )
        self.setObjectName('dateTimeInterface')

        # calendar picker
        self.addExampleCard(
            title=self.tr('A simple CalendarPicker'),
            widget=CalendarPicker(self),
            sourcePath='https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/calendar_picker/demo.py'
        )

        w = CalendarPicker(self)
        w.setDateFormat(Qt.TextDate)
        self.addExampleCard(
            title=self.tr('A CalendarPicker in another format'),
            widget=w,
            sourcePath='https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/calendar_picker/demo.py'
        )

        # AM/PM time picker
        self.addExampleCard(
            title=self.tr('A simple TimePicker'),
            widget=TimePicker(self),
            sourcePath='https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/date_time/demo.py'
        )

